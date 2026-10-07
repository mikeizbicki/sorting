import doctest

from src import sorting


def test_doctests():
    results = doctest.testmod(sorting, verbose=False)
    assert results.failed == 0
