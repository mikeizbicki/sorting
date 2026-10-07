#!/bin/python3
'''
This file contains leetcode problems
that you might get asked in a technical interview.
The unifying idea is that many complicated looking problems
can be solved by "just" sorting the input in a clever way.
Solving these problems will help prepare you get a job;
it will also help you understand the versatility of sorting.

For every problem, I have provided both a hint and
a key/cmp function that will give you a good sorted order.
'''


def merge_intervals(intervals):
    '''
    LeetCode 56 -- Merge Intervals
    Difficulty: Medium

    Given a list of intervals where each interval is [start, end],
    merge all overlapping intervals and return the non-overlapping intervals
    that cover every input interval.

    >>> merge_intervals([[1,3],[2,6],[8,10],[15,18]])
    [[1, 6], [8, 10], [15, 18]]
    >>> merge_intervals([[1,4],[4,5]])
    [[1, 5]]
    >>> merge_intervals([[1, 4], [0, 4]])
    [[0, 4]]
    >>> merge_intervals([])
    []

    Hint: sorting the intervals by their start point brings overlapping
    intervals next to each other, so a single left-to-right pass is
    enough.  Whenever the next interval starts at or before the end of
    the last merged one, extend it; otherwise start a new interval.
    '''
    def key(interval):
        return interval[0]


def rank_teams(votes):
    '''
    LeetCode 1366 -- Rank Teams by Votes
    Difficulty: Medium

    In a special ranking system, each voter gives a rank from highest to lowest to all teams participating in the competition.

    The ordering of teams is decided by who received the most position-one votes.
    If two or more teams tie in the first position,
    we consider the second position to resolve the conflict,
    if they tie again, we continue this process until the ties are resolved.
    If two or more teams are still tied after considering all positions,
    we rank them alphabetically based on their team letter.

    You are given an array of strings votes which is the votes of all voters in the ranking systems. Sort all teams according to the ranking system described above.

    >>> rank_teams(["ABC","ACB","ABC","ACB","ACB"])
    'ACB'
    >>> rank_teams(["WXYZ","XYZW"])
    'XWYZ'
    >>> rank_teams(["ZMNAGUEDSJYLBOPHRQICWFXTVK"])
    'ZMNAGUEDSJYLBOPHRQICWFXTVK'

    Hint: build a table counts[team][i] = how many voters ranked that
    team in position i.  Teams are then ordered by their count vector,
    highest first, with the alphabet as the final tie-break.  Negating
    the counts turns the descending order into an ordinary sort key.
    '''
    # counts[team][i] is the number of voters who ranked `team`
    # in position i -- fill this in before sorting.
    counts = {}

    def key(team):
        # negated counts sort descending; the letter breaks ties
        return tuple(-n for n in counts[team]) + (team,)


def largest_number(nums):
    '''
    LeetCode 179 -- Largest Number
    Difficulty: Medium

    Given a list of non-negative integers, arrange them to form the
    largest possible number and return that number as a string.

    >>> largest_number([10, 2])
    '210'
    >>> largest_number([3, 30, 34, 5, 9])
    '9534330'
    >>> largest_number([0, 0])
    '0'
    >>> largest_number([1])
    '1'

    Hint: compare two numbers as strings: a should come before b when
    a + b is a larger number than b + a.  That is a comparison and not a
    key, so wrap it with functools.cmp_to_key.  The all-zeros input must
    come out as the single string '0'.
    '''
    def cmp(a, b):
        if a + b > b + a:
            return -1
        return 1 if b + a > a + b else 0


def two_city_sched_cost(costs):
    '''
    LeetCode 1029 -- Two City Scheduling
    Difficulty: Medium

    You are planning to interview 2n people.
    Given the array costs where costs[i] = [aCosti, bCosti],
    the cost of flying the ith person to city a is aCosti,
    and the cost of flying the ith person to city b is bCosti.

    Return the minimum cost to fly every person to a city such that exactly n people arrive in each city.

    >>> two_city_sched_cost([[10,20],[30,200],[400,50],[30,20]])
    110
    >>> two_city_sched_cost([[259,770],[448,54],[926,667],
    ...                      [184,139],[840,118],[577,469]])
    1859

    Hint:
    Imagine flying everyone to city B as a baseline.
    Moving one person to city A changes the total by costA - costB,
    and exactly n people must move,
    so sort by that difference and move the n smallest.

    '''
    def key(cost):
        return cost[0] - cost[1]
