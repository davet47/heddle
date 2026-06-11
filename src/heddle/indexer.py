"""Rebuild the store from the contracts/ folder. The store is always derived."""

from __future__ import annotations

from pathlib import Path

from .contract import contract_hash, parse_contract
from .errors import HeddleError, unknown_name
from .implhash import impl_hash
from .project import contracts_dir
from .store import Store


def index(root: Path, store: Store) -> dict:
    """Parse every contract, validate cross-references, rebuild contracts/edges/impls.

    Verification rows are keyed by content hashes, so they survive reindexing;
    contracts whose hash changed get their dependents' verifications marked stale.
    """
    cdir = contracts_dir(root)
    if not cdir.is_dir():
        raise HeddleError("no_contracts", f"'{cdir}' does not exist")

    files = sorted(cdir.glob("*.yaml")) + sorted(cdir.glob("*.yml"))
    parsed: dict[str, tuple[dict, str]] = {}
    for f in files:
        data = parse_contract(f.read_text(encoding="utf-8"), expect_name=f.stem)
        parsed[data["name"]] = (data, f.read_text(encoding="utf-8"))

    # two-pass: all names known before deps are validated
    for name, (data, _) in parsed.items():
        for dep in data.get("deps", []):
            if dep not in parsed:
                raise unknown_name("unknown_dep", dep, list(parsed), contract=name)

    old_hashes = store.contract_hashes()
    changed: list[str] = []
    for name, (data, yaml_text) in parsed.items():
        chash = contract_hash(data)
        if old_hashes.get(name) != chash:
            changed.append(name)
        store.upsert_contract(name, chash, yaml_text)
        store.set_deps(name, data.get("deps", []))
        if "impl" in data:
            path_str = data["impl"].partition("::")[0]
            try:
                ihash = impl_hash(root, data["impl"], contract=name)
            except HeddleError:
                ihash = None  # missing impl shows up as dirty in status, not an index failure
            store.upsert_impl(name, ihash, path_str)

    removed = [n for n in old_hashes if n not in parsed]
    for name in removed:
        store.delete_contract(name)

    invalidated: set[str] = set()
    for name in changed + removed:
        invalidated.update(store.dependents_of(name, transitive=True))
        invalidated.add(name)
    store.mark_stale(sorted(invalidated & set(parsed)))

    return {
        "indexed": len(parsed),
        "changed": sorted(changed),
        "removed": sorted(removed),
        "invalidated": sorted(invalidated & set(parsed)),
    }
