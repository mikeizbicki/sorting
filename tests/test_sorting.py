import ast
import copy
import math
from functools import cmp_to_key
from pathlib import Path

from hypothesis import given
import hypothesis.strategies as st
import timeit

from src.sorting import (
    _merged,
    cmp_invert,
    cmp_last_digit,
    cmp_nan_first,
    cmp_nan_last,
    cmp_natural,
    cmp_reverse,
    cmp_standard,
    merge_sorted,
    quick_sort,
    quick_sorted,
)

ints = st.lists(st.integers())


@given(str1=ints, str2=ints)
def test___merged(str1, str2):
    str1_sorted = sorted(str1)
    str2_sorted = sorted(str2)
    str12_sorted = sorted(str1 + str2)
    assert _merged(str1_sorted, str2_sorted) == str12_sorted


@given(str1=ints, str2=ints)
def test___merged_cmp1(str1, str2):
    str1_sorted = list(reversed(sorted(str1)))
    str2_sorted = list(reversed(sorted(str2)))
    str12_sorted = list(reversed(sorted(str1 + str2)))
    assert _merged(str1_sorted, str2_sorted, cmp=cmp_reverse) == str12_sorted


@given(str1=ints, str2=ints)
def test___merged_reverse(str1, str2):
    str1_sorted = sorted(str1, reverse=True)
    str2_sorted = sorted(str2, reverse=True)
    str12_sorted = sorted(str1 + str2, reverse=True)
    assert _merged(str1_sorted, str2_sorted, reverse=True) == str12_sorted


@given(str1=ints)
def test__merge_sorted(str1):
    assert merge_sorted(list(str1)) == sorted(str1)


@given(str1=ints)
def test__merge_sorted_memory(str1):
    str1_copy = copy.deepcopy(str1)
    str1 = list(str1)
    merge_sorted(str1)
    assert str1_copy == str1


@given(str1=ints)
def test__merge_sorted_cmp1(str1):
    assert merge_sorted(list(str1), cmp_reverse) == list(reversed(sorted(str1)))


@given(str1=ints)
def test__merge_sorted_cmp2(str1):
    assert (
        merge_sorted(list(str1), cmp_reverse)
        == list(sorted(str1, key=cmp_to_key(cmp_reverse)))
    )


@given(str1=ints)
def test__merge_sorted_reverse(str1):
    assert merge_sorted(list(str1), reverse=True) == sorted(str1, reverse=True)


@given(str1=ints)
def test__quick_sorted(str1):
    assert quick_sorted(list(str1)) == sorted(str1)


@given(str1=ints)
def test__quick_sorted_cmp1(str1):
    assert quick_sorted(list(str1), cmp_reverse) == list(reversed(sorted(str1)))


@given(str1=ints)
def test__quick_sorted_cmp2(str1):
    assert (
        quick_sorted(list(str1), cmp_reverse)
        == list(sorted(str1, key=cmp_to_key(cmp_reverse)))
    )


@given(str1=ints)
def test__quick_sorted_reverse(str1):
    assert quick_sorted(list(str1), reverse=True) == sorted(str1, reverse=True)


@given(str1=ints)
def test__quick_sorted_memory(str1):
    str1_copy = copy.deepcopy(str1)
    str1 = list(str1)
    quick_sorted(str1)
    assert str1


@given(str1=ints)
def test__quick_sort(str1):
    str1 = list(str1)
    quick_sort(str1)
    assert str1 == sorted(str1)


@given(str1=ints)
def test__quick_sort_reverse(str1):
    str1 = list(str1)
    quick_sort(str1, reverse=True)
    assert str1 == sorted(str1, reverse=True)


def test__cmp_invert():
    assert cmp_invert(cmp_standard)(1, 2) == 1
    assert cmp_invert(cmp_standard)(2, 1) == -1
    assert cmp_invert(cmp_standard)(1, 1) == 0


@given(str1=ints)
def test__merge_sorted_inverted(str1):
    assert (
        merge_sorted(list(str1), cmp=cmp_invert(cmp_standard))
        == sorted(str1, reverse=True)
    )


@given(vals=st.lists(st.floats(allow_nan=False)))
def test__merge_sorted_nan_last(vals):
    result = merge_sorted(list(vals) + [float('nan')], cmp=cmp_nan_last)
    assert math.isnan(result[-1])
    assert result[:-1] == sorted(vals)


@given(vals=st.lists(st.floats(allow_nan=False), max_size=5))
def test__quick_sorted_nan_first(vals):
    nan = float('nan')
    result = quick_sorted(list(vals) + [nan, nan], cmp=cmp_nan_first)
    assert all(math.isnan(x) for x in result[:2])
    assert result[2:] == sorted(vals)


def test__cmp_natural():
    names = ['file10', 'file2', 'file1', 'file100', 'a']
    assert merge_sorted(names, cmp=cmp_natural) == [
        'a', 'file1', 'file2', 'file10', 'file100',
    ]
    assert cmp_natural('file02', 'file2') == 0
    assert cmp_natural('x2y10', 'x2y9') == 1


@given(nums=st.lists(st.integers(min_value=0), min_size=1, unique=True))
def test__merge_sorted_natural(nums):
    names = ['file{}'.format(n) for n in nums]
    expected = ['file{}'.format(n) for n in sorted(nums)]
    assert merge_sorted(names, cmp=cmp_natural) == expected


@given(nums=st.lists(st.integers(min_value=0), min_size=1, unique=True))
def test__quick_sort_natural(nums):
    names = ['file{}'.format(n) for n in nums]
    quick_sort(names, cmp=cmp_natural)
    assert names == ['file{}'.format(n) for n in sorted(nums)]
