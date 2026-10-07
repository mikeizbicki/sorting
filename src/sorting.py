#!/bin/python3
'''
Python provides built-in sort/sorted functions that use timsort internally.
You cannot use these built-in functions anywhere in this file.

Every function in this file takes a comparator `cmp` as input
which controls how the elements of the list should be compared against each other:
If cmp(a, b) returns -1, then a < b;
if cmp(a, b) returns  1, then a > b;
if cmp(a, b) returns  0, then a == b.

Every sorting function in this file also takes a boolean `reverse` parameter.
When reverse=True, the elements are sorted in the opposite order,
equivalently, the result of every call to cmp is negated.
'''

import math
import random

def cmp_standard(a, b):
    '''
    used for sorting from lowest to highest

    >>> cmp_standard(125, 322)
    -1
    >>> cmp_standard(523, 322)
    1
    >>> cmp_standard(322, 322)
    0
    '''
    if a < b:
        return -1
    if b < a:
        return 1
    return 0


def cmp_reverse(a, b):
    '''
    used for sorting from highest to lowest

    >>> cmp_reverse(125, 322)
    1
    >>> cmp_reverse(523, 322)
    -1
    >>> cmp_reverse(322, 322)
    0
    '''


def cmp_invert(cmp):
    '''
    Returns a new comparator that is the exact opposite of the input cmp.
    If cmp sorts from lowest to highest, then cmp_invert(cmp) sorts from
    highest to lowest.

    This is how the `reverse=True` parameter of the sorting functions can be
    implemented elegantly: instead of writing a separate descending branch
    inside of each of merge_sorted, quick_sorted, and quick_sort,
    you can simply sort using the inverted comparator.

    >>> cmp_invert(cmp_standard)(125, 322)
    1
    >>> cmp_invert(cmp_standard)(523, 322)
    -1
    >>> cmp_invert(cmp_invert(cmp_standard))(523, 322)
    1
    >>> cmp_invert(cmp_standard)(322, 322)
    0
    '''
    def inverted(a, b):
        return -cmp(a, b)
    return inverted


def cmp_last_digit(a, b):
    '''
    used for sorting based on the last digit only

    >>> cmp_last_digit(125, 322)
    1
    >>> cmp_last_digit(523, 322)
    1
    >>> cmp_last_digit(120, 121)
    -1
    '''
    return cmp_standard(a % 10, b % 10)


def cmp_nan_last(a, b):
    '''
    NaN stands for "not a number".
    It is the float value that python uses to represent a missing or error value.
    It shows up whenever an operation has an undefined result:

    >>> float('inf') - float('inf')
    nan

    The important property of NaN is that it is not equal to itself:

    >>> float('nan') == float('nan')
    False

    This means that cmp_standard is not a valid comparator for NaN values.
    It returns 0 for both cmp_standard(float('nan'), 1) and
    cmp_standard(1, float('nan')), even though NaN does not equal 1,
    so the recursive sorting algorithms cannot tell where a NaN belongs.
    Real-world data sets are full of missing values
    (pandas produces them for every missing entry in a dataframe,
    and reading a csv file produces them for every empty cell),
    so we need a comparator that gives NaN a fixed position in the sort order.

    This comparator sorts all NaN values last and
    sorts all other values  with cmp_standard.

    >>> cmp_nan_last(1, 2)
    -1
    >>> cmp_nan_last(float('nan'), 2)
    1
    >>> cmp_nan_last(2, float('nan'))
    -1
    >>> cmp_nan_last(float('nan'), float('nan'))
    0
    '''
    if math.isnan(a):
        if math.isnan(b):
            return 0
        return 1
    if math.isnan(b):
        return -1
    return cmp_standard(a, b)


def cmp_nan_first(a, b):
    '''
    This is *almost* the inverse of cmp_nan_last.
    It puts all nan values at the front,
    but maintains the cmp_standard ordering for non-nan values.

    >>> cmp_nan_first(float('nan'), 2)
    -1
    >>> cmp_nan_first(2, float('nan'))
    1
    >>> cmp_nan_first(1, 2)
    -1
    >>> cmp_nan_first(2, 1)
    1
    >>> cmp_nan_first(float('nan'), float('nan'))
    0
    '''


def _natural_chunks(s):
    '''
    Splits the string s into a list of alternating non-digit and digit
    chunks, where every digit chunk is converted into an int.

    >>> _natural_chunks('file10.txt')
    ['file', 10, '.txt']
    >>> _natural_chunks('1a2')
    [1, 'a', 2]
    '''
    chunks = []
    for c in s:
        if c.isdigit():
            if chunks and isinstance(chunks[-1], int):
                chunks[-1] = chunks[-1] * 10 + int(c)
            else:
                chunks.append(int(c))
        elif chunks and isinstance(chunks[-1], str):
            chunks[-1] += c
        else:
            chunks.append(c)
    return chunks


def cmp_natural(a, b):
    '''
    Used for sorting strings that contain numbers,
    and is sometimes called "natural sort" or "human sort".

    The problem is that strings compare lexicographically,
    so the standard comparator claims that 'file10' comes before 'file2':

    >>> cmp_standard('file10', 'file2')
    -1

    This is a constant annoyance when sorting file names.
    This comparator fixes the problem by comparing the digit chunks of the
    strings as numbers and the remaining chunks as strings.

    >>> cmp_natural('file10', 'file2')
    1
    >>> cmp_natural('file2', 'file10')
    -1
    >>> cmp_natural('file2', 'file2')
    0
    >>> cmp_natural('a1', 'a')
    1
    '''
    a_chunks = _natural_chunks(a)
    b_chunks = _natural_chunks(b)
    for a_chunk, b_chunk in zip(a_chunks, b_chunks):
        if isinstance(a_chunk, int) != isinstance(b_chunk, int):
            return -1 if isinstance(a_chunk, int) else 1
        result = cmp_standard(a_chunk, b_chunk)
        if result != 0:
            return result
    return cmp_standard(len(a_chunks), len(b_chunks))


def _merged(xs, ys, cmp=cmp_standard, reverse=False):
    '''
    Assumes that both xs and ys are sorted,
    and returns a new list containing the elements of both xs and ys.
    Runs in linear time.

    NOTE:
    In python, helper functions are frequently prepended with the _.
    This is a signal to users of a library that these functions are for "internal use only",
    and not part of the "public interface".

    This _merged function could be implemented as a local function within the merge_sorted scope rather than a global function.
    The downside of this is that the function can then not be tested on its own.
    Typically, you should only implement a function as a local function if it cannot function on its own
    (like the go functions from binary search).
    If it's possible to make a function stand-alone,
    then you probably should do that and write test cases for the stand-alone function.

    >>> _merged([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    >>> _merged([5, 3, 1], [6, 4, 2], reverse=True)
    [6, 5, 4, 3, 2, 1]
    >>> _merged([1, 3, float('nan')], [2], cmp=cmp_nan_last)
    [1, 2, 3, nan]
    '''


def merge_sorted(xs, cmp=cmp_standard, reverse=False):
    '''
    Merge sort is the standard O(n log n) sorting algorithm.
    Recall that the merge sort pseudo code is:

        if xs has 1 element
            it is sorted, so return xs
        else
            divide the list into two halves left,right
            sort the left
            sort the right
            merge the two sorted halves

    You should return a sorted version of the input list xs.
    You should not modify the input list xs in any way.

    >>> merge_sorted([3, 1, 2])
    [1, 2, 3]
    >>> merge_sorted([3, 1, 2], reverse=True)
    [3, 2, 1]
    >>> merge_sorted([3, 1, 2], cmp=cmp_invert(cmp_standard))
    [3, 2, 1]
    >>> merge_sorted(['file10', 'file2', 'file1'], cmp=cmp_natural)
    ['file1', 'file2', 'file10']
    '''


def quick_sorted(xs, cmp=cmp_standard, reverse=False):
    '''
    Quicksort is like mergesort,
    but it uses a different strategy to split the list.
    Instead of splitting the list down the middle,
    a "pivot" value is randomly selected, 
    and the list is split into a "less than" sublist and a "greater than" sublist.

    The pseudocode is:

        if xs has 1 element
            it is sorted, so return xs
        else
            select a pivot value p
            put all the values less than p in a list
            put all the values greater than p in a list
            put all the values equal to p in a list
            sort the greater/less than lists recursively
            return the concatenation of (less than, equal, greater than)

    You should return a sorted version of the input list xs.
    You should not modify the input list xs in any way.

    >>> quick_sorted([3, 1, 2])
    [1, 2, 3]
    >>> quick_sorted([3, 1, 2], reverse=True)
    [3, 2, 1]
    >>> quick_sorted([float('nan'), 1, 5, 2, 3], cmp=cmp_nan_last)
    [1, 2, 3, 5, nan]
    >>> quick_sorted([float('nan'), 1, 5, 2, 3], cmp=cmp_nan_first)
    [nan, 1, 2, 3, 5]
    '''


def quick_sort(xs, cmp=cmp_standard, reverse=False):
    '''
    The main advantage of quick_sort is that it can be implemented "in-place".
    This means that no extra lists are allocated,
    or that the algorithm uses Theta(1) additional memory.
    Merge sort, on the other hand, must allocate intermediate lists for the merge step,
    and has a Theta(n) memory requirement.
    Even though quick sort and merge sort both have the same Theta(n log n) runtime,
    this more efficient memory usage typically makes quick sort faster in practice.
    (We say quick sort has a lower "constant factor" in its runtime.)
    The downside of implementing quick sort in this way is that it will no longer be a [stable sort](https://en.wikipedia.org/wiki/Sorting_algorithm#Stability),
    but this is typically inconsequential.

    Follow the pseudocode of the Lomuto partition scheme given on wikipedia
    (https://en.wikipedia.org/wiki/Quicksort#Algorithm)
    to implement quick_sort as an in-place algorithm.
    You should directly modify the input xs variable instead of returning a copy of the list.

    >>> xs = [3, 1, 2]
    >>> quick_sort(xs)
    >>> xs
    [1, 2, 3]
    >>> xs = [3, 1, 2]
    >>> quick_sort(xs, reverse=True)
    >>> xs
    [3, 2, 1]
    >>> xs = ['file10', 'file2']
    >>> quick_sort(xs, cmp=cmp_natural)
    >>> xs
    ['file2', 'file10']
    '''
