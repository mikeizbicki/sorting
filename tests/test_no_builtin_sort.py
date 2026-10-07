from pathlib import Path
import ast


SOURCE = Path(__file__).resolve().parent.parent / 'src' / 'sorting.py'
BANNED = {'sorted', 'sort'}


def _banned_calls(tree):
    """Yield (lineno, name) for every call to sorted() or .sort()."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                name = func.id
            else:
                name = getattr(func, 'attr', None)
            if name in BANNED:
                yield node.lineno, name


def test_no_builtin_sort():
    tree = ast.parse(SOURCE.read_text(), filename=str(SOURCE))
    offenders = list(_banned_calls(tree))
    assert not offenders, 'built-in sort used: {}'.format(offenders)
