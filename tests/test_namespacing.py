"""Subdirectories under contracts/ act as namespaces — ISSUES: contract names
are global. `contracts/ns/foo.yaml` is the contract `ns/foo`; the same short
name can coexist in different folders. Names that would escape contracts/ are
refused."""

from __future__ import annotations

import textwrap

import pytest

from heddle import api
from heddle.contract import parse_contract
from heddle.errors import HeddleError
from heddle.indexer import index
from heddle.project import db_path, init_project
from heddle.store import Store


def _project(tmp_path):
    init_project(tmp_path)
    return tmp_path, Store(db_path(tmp_path))


def _write(root, relpath: str, body: str) -> None:
    f = root / "contracts" / relpath
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(textwrap.dedent(body).strip() + "\n")


def test_nested_contract_indexes_with_namespaced_name(tmp_path):
    root, store = _project(tmp_path)
    _write(root, "billing/Invoice.yaml", """
        name: billing/Invoice
        signature: "dataclass: total: float"
    """)
    index(root, store)
    assert store.contract_names() == ["billing/Invoice"]


def test_cross_namespace_dependency_resolves(tmp_path):
    root, store = _project(tmp_path)
    _write(root, "core/Money.yaml", """
        name: core/Money
        signature: "dataclass: cents: int"
    """)
    _write(root, "billing/Invoice.yaml", """
        name: billing/Invoice
        signature: "(amount: Money) -> Invoice"
        deps: [core/Money]
    """)
    index(root, store)
    assert store.deps_of("billing/Invoice") == ["core/Money"]
    packet = api.get_contract(root, store, "billing/Invoice")
    assert [d["name"] for d in packet["deps"]] == ["core/Money"]


def test_same_stem_in_two_namespaces_coexist(tmp_path):
    root, store = _project(tmp_path)
    _write(root, "a/Thing.yaml", 'name: a/Thing\nsignature: "() -> A"\n')
    _write(root, "b/Thing.yaml", 'name: b/Thing\nsignature: "() -> B"\n')
    index(root, store)
    assert store.contract_names() == ["a/Thing", "b/Thing"]
    # distinct identities -> distinct hashes
    hashes = store.contract_hashes()
    assert hashes["a/Thing"] != hashes["b/Thing"]


def test_put_contract_creates_namespace_directory(tmp_path):
    root, store = _project(tmp_path)
    out = api.put_contract(root, store, "ns/New", 'name: ns/New\nsignature: "() -> None"\n')
    assert out["name"] == "ns/New"
    assert (root / "contracts" / "ns" / "New.yaml").is_file()
    assert store.get_contract("ns/New") is not None


def test_flat_names_still_work(tmp_path):
    root, store = _project(tmp_path)
    _write(root, "Plain.yaml", 'name: Plain\nsignature: "() -> None"\n')
    index(root, store)
    assert store.contract_names() == ["Plain"]


@pytest.mark.parametrize("bad", ["../evil", "/etc/passwd", "a/../../b", "ns//x"])
def test_parse_rejects_unsafe_names(bad):
    with pytest.raises(HeddleError) as e:
        parse_contract(f'name: "{bad}"\nsignature: "() -> None"\n')
    assert e.value.code == "invalid_name"


def test_parse_rejects_backslash_name():
    with pytest.raises(HeddleError) as e:
        parse_contract("name: 'a\\\\b'\nsignature: \"() -> None\"\n")
    assert e.value.code == "invalid_name"


def test_put_contract_rejects_escaping_name(tmp_path):
    root, store = _project(tmp_path)
    with pytest.raises(HeddleError) as e:
        api.put_contract(root, store, "../evil", 'name: "../evil"\nsignature: "() -> None"\n')
    assert e.value.code in ("invalid_name", "unsafe_name")
    assert not (root.parent / "evil.yaml").exists()  # nothing written outside contracts/
