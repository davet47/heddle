"""Impl hash stability: formatting/comments/docstrings must not change the
hash; logic changes must."""

import pytest

from heddle.errors import HeddleError
from heddle.implhash import impl_hash

BASE = '''
def total(items):
    """Sum the ok items."""
    # only the ok ones count
    return sum(i.value for i in items if i.ok)
'''


def write_and_hash(tmp_path, source: str) -> str:
    (tmp_path / "mod.py").write_text(source)
    return impl_hash(tmp_path, "mod.py::total")


def test_identical_source_same_hash(tmp_path):
    assert write_and_hash(tmp_path, BASE) == write_and_hash(tmp_path, BASE)


def test_comments_do_not_change_hash(tmp_path):
    a = write_and_hash(tmp_path, BASE)
    b = write_and_hash(tmp_path, BASE.replace("    # only the ok ones count\n", ""))
    assert a == b


def test_docstring_does_not_change_hash(tmp_path):
    a = write_and_hash(tmp_path, BASE)
    b = write_and_hash(tmp_path, BASE.replace('"""Sum the ok items."""', '"""Different docstring."""'))
    assert a == b


def test_formatting_does_not_change_hash(tmp_path):
    a = write_and_hash(tmp_path, BASE)
    reformatted = '''
def total(items):
    """Sum the ok items."""
    return sum(
        i.value
        for i in items
        if i.ok
    )
'''
    assert a == write_and_hash(tmp_path, reformatted)


def test_surrounding_code_does_not_change_hash(tmp_path):
    a = write_and_hash(tmp_path, BASE)
    b = write_and_hash(tmp_path, "import os\n\nUNRELATED = 1\n" + BASE)
    assert a == b


def test_logic_change_changes_hash(tmp_path):
    a = write_and_hash(tmp_path, BASE)
    b = write_and_hash(tmp_path, BASE.replace("if i.ok", "if not i.ok"))
    assert a != b


def test_class_and_method_resolution(tmp_path):
    (tmp_path / "mod.py").write_text(
        "class Calc:\n    def total(self, items):\n        return sum(items)\n"
    )
    assert impl_hash(tmp_path, "mod.py::Calc") != impl_hash(tmp_path, "mod.py::Calc.total")


def test_missing_function_raises(tmp_path):
    (tmp_path / "mod.py").write_text("x = 1\n")
    with pytest.raises(HeddleError) as exc:
        impl_hash(tmp_path, "mod.py::nope")
    assert exc.value.code == "impl_not_found"


def test_missing_file_raises(tmp_path):
    with pytest.raises(HeddleError) as exc:
        impl_hash(tmp_path, "absent.py::f")
    assert exc.value.code == "impl_not_found"


def test_syntax_error_raises(tmp_path):
    (tmp_path / "mod.py").write_text("def broken(:\n")
    with pytest.raises(HeddleError) as exc:
        impl_hash(tmp_path, "mod.py::broken")
    assert exc.value.code == "impl_syntax_error"
