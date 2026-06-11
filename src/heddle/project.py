"""Project layout: a heddle project is any directory with a .heddle/ marker.

contracts/ holds one YAML file per unit; .heddle/store.db is derived state.
"""

from __future__ import annotations

from pathlib import Path

from .errors import HeddleError

HEDDLE_DIR = ".heddle"
CONTRACTS_DIR = "contracts"
DB_NAME = "store.db"


def find_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for candidate in (cur, *cur.parents):
        if (candidate / HEDDLE_DIR).is_dir():
            return candidate
    raise HeddleError("no_project", f"no {HEDDLE_DIR}/ found in '{cur}' or any parent — run `heddle init` first")


def db_path(root: Path) -> Path:
    return root / HEDDLE_DIR / DB_NAME


def contracts_dir(root: Path) -> Path:
    return root / CONTRACTS_DIR


def contract_path(root: Path, name: str) -> Path:
    return contracts_dir(root) / f"{name}.yaml"


def init_project(root: Path) -> list[str]:
    """Create .heddle/ and contracts/. Returns the paths created."""
    created = []
    for d in (root / HEDDLE_DIR, contracts_dir(root)):
        if not d.exists():
            d.mkdir(parents=True)
            created.append(str(d))
    return created
