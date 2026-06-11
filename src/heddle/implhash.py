"""Implementation hashing over a normalised AST.

sha256 of `ast.dump` for the named function/class, so formatting and comment
changes never bust the verification cache. Docstrings are stripped before
dumping — they are documentation, not behaviour.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

from .errors import HeddleError

_DEF_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def _strip_docstrings(node: ast.AST) -> ast.AST:
    for child in ast.walk(node):
        if isinstance(child, (*_DEF_NODES, ast.Module)) and child.body:
            first = child.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                child.body = child.body[1:] or [ast.Pass()]
    return node


def _find_def(tree: ast.Module, qualname: str) -> ast.AST | None:
    """Resolve a possibly-dotted name (e.g. 'Class.method') to its def node."""
    scope: list[ast.AST] = list(tree.body)
    node: ast.AST | None = None
    for part in qualname.split("."):
        node = next(
            (n for n in scope if isinstance(n, _DEF_NODES) and n.name == part),
            None,
        )
        if node is None:
            return None
        scope = list(getattr(node, "body", []))
    return node


def impl_hash(root: Path, impl: str, contract: str | None = None) -> str:
    """Hash the implementation referenced by 'path/to/file.py::qualname'."""
    path_str, _, qualname = impl.partition("::")
    path = root / path_str
    if not path.is_file():
        raise HeddleError("impl_not_found", f"implementation file '{path_str}' does not exist", contract=contract)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as e:
        raise HeddleError("impl_syntax_error", f"'{path_str}' line {e.lineno}: {e.msg}", contract=contract)

    node = _find_def(tree, qualname)
    if node is None:
        raise HeddleError("impl_not_found", f"no function or class '{qualname}' in '{path_str}'", contract=contract)

    dumped = ast.dump(_strip_docstrings(node), annotate_fields=True, include_attributes=False)
    return hashlib.sha256(dumped.encode("utf-8")).hexdigest()
