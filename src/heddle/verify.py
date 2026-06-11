"""Hash-keyed verification: run pytest only on cache misses.

Verification key = sha256 over (contract_hash, impl_hash, transitive dep
contract hashes). A cached green result is valid iff the full key matches —
any contract edit anywhere in the dependency closure produces a new key.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

from . import tokens
from .errors import HeddleError, unknown_name
from .implhash import impl_hash
from .store import Store

SUMMARY_MAX_TOKENS = 40


def verification_key(store: Store, name: str, ihash: str) -> str:
    chash = store.get_contract(name)["hash"]
    hashes = store.contract_hashes()
    dep_part = ",".join(f"{d}={hashes[d]}" for d in store.transitive_deps(name) if d in hashes)
    raw = f"contract={chash}|impl={ihash}|deps={dep_part}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _failure_summary(stdout: str) -> str:
    """Assertion line + values, never a full traceback. ≤ ~40 tokens."""
    lines = stdout.splitlines()
    failed = next((l.strip() for l in lines if l.startswith("FAILED ")), "")
    # pytest prefixes assertion/error detail lines with 'E '
    detail = [l.strip()[2:].strip() for l in lines if l.strip().startswith("E ")]
    parts = []
    if failed:
        parts.append(failed.split(" - ")[0].removeprefix("FAILED "))
    parts.extend(detail[:3])
    summary = " | ".join(p for p in parts if p) or "tests failed (no assertion detail captured)"
    return tokens.truncate(re.sub(r"\s+", " ", summary), SUMMARY_MAX_TOKENS)


def _run_pytest(root: Path, node_ids: list[str]) -> tuple[bool, str]:
    proc = subprocess.run(
        # -B: regeneration loops rewrite source faster than mtime granularity,
        # so cached bytecode could silently test the previous weft
        [sys.executable, "-B", "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", *node_ids],
        cwd=root,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        timeout=300,
    )
    out = proc.stdout + "\n" + proc.stderr
    if proc.returncode in (2, 3, 4):  # interrupted / internal error / usage error
        raise HeddleError(
            "tests_failed_to_run",
            tokens.truncate("pytest could not run: " + re.sub(r"\s+", " ", out.strip()), 60),
        )
    return proc.returncode == 0, out


def verify_one(root: Path, store: Store, name: str) -> dict:
    """Verify a single contract. Returns {name, status, summary, key}."""
    row = store.get_contract(name)
    if row is None:
        raise unknown_name("unknown_contract", name, store.contract_names())
    data = yaml.safe_load(row["yaml"])

    if "impl" not in data:
        raise HeddleError("no_impl", f"'{name}' is spec-only (no impl) — nothing to verify", contract=name)
    if not data.get("tests"):
        raise HeddleError("no_tests", f"'{name}' has an impl but no tests — add pytest node IDs", contract=name)

    ihash = impl_hash(root, data["impl"], contract=name)  # always fresh from disk
    store.upsert_impl(name, ihash, data["impl"].partition("::")[0])
    key = verification_key(store, name, ihash)

    store.incr("verify_requests")
    cached = store.get_verification(key)
    if cached is not None and cached["status"] == "pass" and not cached["stale"]:
        store.incr("cache_hits")
        return {"name": name, "status": "cached-pass", "summary": cached["summary"], "key": key}

    store.incr("cache_misses")
    store.incr("test_runs")
    ok, out = _run_pytest(root, data["tests"])
    if ok:
        summary = ""
        store.record_verification(key, name, "pass", summary)
        return {"name": name, "status": "pass", "summary": summary, "key": key}

    summary = _failure_summary(out)
    store.record_verification(key, name, "fail", summary)
    return {"name": name, "status": "fail", "summary": summary, "key": key}
