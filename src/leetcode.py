#!/bin/python3
'''
This file contains "leetcode style" interview problems that are solved by
sorting the input first.  Every function in this file should be implemented
using `merge_sorted` (or `quick_sort`) from src/sorting.py.
You may not use python's built-in `sorted` function or the `list.sort`
method anywhere in this file.

The unifying idea is that many problems that look like they require a clever
insight are really just "sort, then do a single linear scan".  This is the
same pattern that appears all over data science: pandas' `groupby` and
`value_counts` operations, database merge-joins, and the k-nearest-neighbor
algorithm all begin by sorting, and the entire algorithmic content is the
choice of comparison function (`cmp`).  The comparator is what encodes
"which order does this problem actually want".
'''

from src.sorting import merge_sorted, cmp_standard


def _cmp_pair_first(a, b):
    '''
    comparator that sorts 2-tuples by their first element

    >>> _cmp_pair_first((1, 99), (2, 0))
    -1
    >>> _cmp_pair_first((5, 0), (4, 99))
    1
    '''
    return cmp_standard(a[0], b[0])


def merge_intervals(intervals):
    '''
    LeetCode 56 -- Merge Intervals
    Difficulty: Medium

    Given a list of intervals where each interval is [start, end], merge
    all overlapping intervals and return the non-overlapping intervals
    that cover every input interval.

    Data science motivation:
    Merging intervals is exactly the operation you need when you
    deduplicate overlapping time windows in a log or sensor stream --
    two readings with overlapping capture windows describe a single
    event and should be joined.

    >>> merge_intervals([[1,3],[2,6],[8,10],[15,18]])
    [[1, 6], [8, 10], [15, 18]]
    >>> merge_intervals([[1,4],[4,5]])
    [[1, 5]]
    >>> merge_intervals([[1, 4], [0, 4]])
    [[0, 4]]
    >>> merge_intervals([])
    []

    HINT:
    Sort the intervals by their start point using `merge_sorted` with a
    comparator that compares `a[0]` and `b[0]` (see `_cmp_pair_first`
    above).  Once the list is sorted by start, any two intervals that
    overlap must be adjacent.  Walk the sorted list once, keeping a
    "current" interval; if the next interval's start is <= the current
    end, extend the current end to their max.  Otherwise, emit the
    current interval and start a new one.

    Do not modify the caller's list.
    '''
    intervals = merge_sorted([list(iv) for iv in intervals], cmp=_cmp_pair_first)
    result = []
    for start, end in intervals:
        if result and start <= result[-1][1]:
            if end > result[-1][1]:
                result[-1][1] = end
        else:
            result.append([start, end])
    return result


def max_profit_assignment(difficulty, profit, worker):
    '''
    LeetCode 826 -- Most Profit Assigning Work
    Difficulty: Medium

    You have n jobs.  Job i has difficulty difficulty[i] and profit
    profit[i].  You also have workers where worker[j] is the maximum job
    difficulty that worker j can handle.  Each worker can complete at
    most one job, but the same job may be taken by multiple workers.
    Return the maximum total profit.

    Data science motivation:
    This is the simplest "resource allocation" pattern.  Every scheduler
    and job-placement system eventually reduces a batch of work to a
    greedy assignment problem like this one, and the answer to the batch
    is just the sum of per-worker answers computed in sorted order.

    >>> max_profit_assignment([2,4,6,8,10], [10,20,30,40,50], [4,5,6,7])
    100
    >>> max_profit_assignment([85,47,57], [24,66,99], [40,25,25])
    0
    >>> max_profit_assignment([1,2,3], [10,20,30], [3,3,3])
    90

    HINT:
    Pair each difficulty with its profit, and sort the pairs by
    difficulty using `merge_sorted` with a comparator on `[0]`.  Sort a
    copy of the workers ascending as well.  Then walk the workers from
    least capable to most, advancing a pointer through the sorted jobs
    while job difficulty <= worker ability, and track the maximum profit
    seen so far.  Each worker takes that running maximum.  This is a
    simple sweep after two sorts; every worker's answer is a prefix
    statistic of the sorted job list.

    Do not modify any of the input lists.
    '''
    jobs = merge_sorted(list(zip(difficulty, profit)), cmp=_cmp_pair_first)
    workers = merge_sorted(list(worker))
    total = 0
    best = 0
    i = 0
    for ability in workers:
        while i < len(jobs) and jobs[i][0] <= ability:
            if jobs[i][1] > best:
                best = jobs[i][1]
            i += 1
        total += best
    return total


def rank_teams(votes):
    '''
    LeetCode 1366 -- Rank Teams by Votes
    Difficulty: Medium

    Given a list of strings where each string is one voter's ranking of
    all teams (best team first), return a single string giving the
    teams ranked from best to worst.  Teams are sorted first by how many
    voters placed them in position 0 (descending), then by position 1
    votes, and so on.  Ties are broken alphabetically.

    Data science motivation:
    This is rank aggregation -- the same idea behind Borda counts,
    approval voting, and the rank-based meta-features you would feed to a
    recommendation system.  Instead of collapsing each team to a single
    scalar (like a mean rank), we compare entire vote vectors
    position-by-position.

    >>> rank_teams(["ABC","ACB","ABC","ACB","ACB"])
    'ACB'
    >>> rank_teams(["WXYZ","XYZW"])
    'XWYZ'
    >>> rank_teams(["ZMNAGUEDSJYLBOPHRQICWFXTVK"])
    'ZMNAGUEDSJYLBOPHRQICWFXTVK'

    HINT:
    First count, for each team and each rank position, the number of
    ballots that put that team at that position.  Then define a
    comparator on teams: compare vote-count vectors position-by-position
    using `cmp_standard(count_b, count_a)` (higher count first), and
    break ties with `cmp_standard(a, b)` on the team letter.  Pass this
    comparator to `merge_sorted` and join the result.
    '''
    if not votes:
        return ''
    n = len(votes[0])
    teams = list(set(votes[0]))
    counts = {t: [0] * n for t in teams}
    for ballot in votes:
        for pos, t in enumerate(ballot):
            counts[t][pos] += 1

    def cmp_team(a, b):
        for i in range(n):
            if counts[a][i] != counts[b][i]:
                return cmp_standard(counts[b][i], counts[a][i])
        return cmp_standard(a, b)

    return ''.join(merge_sorted(teams, cmp=cmp_team))


def _cmp_concat(a, b):
    '''
    comparator used by `largest_number`; sorts numbers so that
    concatenating them in the returned order yields the largest string.

    >>> _cmp_concat(2, 10)
    -1
    >>> _cmp_concat(10, 2)
    1
    >>> _cmp_concat(3, 3)
    0
    '''
    return cmp_standard(str(b) + str(a), str(a) + str(b))


def largest_number(nums):
    '''
    LeetCode 179 -- Largest Number
    Difficulty: Medium

    Given a list of non-negative integers, arrange them to form the
    largest possible number and return that number as a string.

    Data science motivation:
    The trap here is that the numerically correct comparison is the
    WRONG comparison.  `2` must come before `10`, even though 10 > 2.
    This is a good reminder that "sort by value" is a modelling
    decision, not a truth -- the same way that a fraud-detection model
    might want to sort accounts by some non-obvious derived score.

    >>> largest_number([10, 2])
    '210'
    >>> largest_number([3, 30, 34, 5, 9])
    '9534330'
    >>> largest_number([0, 0])
    '0'
    >>> largest_number([1])
    '1'

    HINT:
    Define a comparator on the STRING representations of the numbers:
    `a` comes before `b` iff `str(a)+str(b)` is lexicographically
    larger than `str(b)+str(a)` (see `_cmp_concat` above).  This is a
    valid total order because it is exactly lexicographic order on the
    infinite periodic words `aaaa...` and `bbbb...`; when the comparator
    returns 0 the two numbers are powers of a common word, so either
    order gives the same concatenation.  Sort with `merge_sorted` using
    `_cmp_concat`, join the strings, strip leading zeros, and special
    case the all-zeros input to return '0'.

    Do not modify the input list.
    '''
    if not nums:
        return '0'
    nums = merge_sorted(list(nums), cmp=_cmp_concat)
    s = ''.join(str(n) for n in nums).lstrip('0')
    return s if s else '0'


def max_ice_cream(costs, coins):
    '''
    LeetCode 1833 -- Maximum Ice Cream Bars
    Difficulty: Medium

    It costs costs[i] to buy the i-th ice cream bar.  You have `coins`
    coins.  Return the maximum number of bars you can buy.

    Data science motivation:
    Choosing the cheapest items first is the discrete analogue of the
    fractional-knapsack greedy rule: sort by unit cost, then take from
    the front until you run out of budget.  The same reasoning
    underlies column selection under a memory budget when you know the
    exact compressed size of each column.

    >>> max_ice_cream([1,3,2,4,1], 7)
    4
    >>> max_ice_cream([10,6,8,7,7,8], 5)
    0
    >>> max_ice_cream([1,6,3,1,2,5], 20)
    6

    HINT:
    Sort the costs ascending with `merge_sorted`.  Then walk from
    cheapest to most expensive; each time you can afford the current
    cost, buy it.  Exchange argument: if the optimal selection skipped a
    cheaper bar in favor of an expensive one, swapping them never
    increases total cost, so the greedy prefix of the sorted list is
    always optimal.

    Do not modify the input list.
    '''
    costs = merge_sorted(list(costs))
    total = 0
    for c in costs:
        if c > coins:
            break
        coins -= c
        total += 1
    return total


def _cmp_delta(a, b):
    '''
    comparator that sorts a list of [costA, costB] pairs by the
    difference costB - costA.

    >>> _cmp_delta([10, 20], [30, 200])
    -1
    >>> _cmp_delta([30, 200], [10, 20])
    1
    '''
    return cmp_standard(a[1] - a[0], b[1] - b[0])


def two_city_sched_cost(costs):
    '''
    LeetCode 1029 -- Two City Scheduling
    Difficulty: Medium

    You have 2n people.  Person i has costs[i] = [costA, costB], the
    cost to fly them to city A or city B respectively.  Send exactly n
    people to each city, minimizing the total cost.  Return the minimum
    cost.

    Data science motivation:
    This is the "balanced assignment" pattern.  Whenever you must put
    equal numbers of items into two groups but items have different
    costs in each group, the answer is to sort by the difference in
    costs.  The same idea appears in A/B test bucketing, treatment vs.
    control allocation, and data-sharding under capacity constraints.

    >>> two_city_sched_cost([[10,20],[30,200],[400,50],[30,20]])
    110
    >>> two_city_sched_cost([[259,770],[448,54],[926,667],
    ...                      [184,139],[840,118],[577,469]])
    1859

    HINT:
    For each person, `costB - costA` is the "extra cost of sending them
    to B instead of A".  Start with everyone sent to A; you must now
    switch exactly n people to B, and each switch has a fixed delta.
    Pick the n people with the SMALLEST (most negative) delta -- i.e.
    sort by `costB - costA` ascending with `merge_sorted` and
    `_cmp_delta`, send the first n to B and the remaining n to A.
    Exchange argument: any two people i, j whose deltas are out of
    order could be swapped to lower total cost, contradicting the sort.

    Do not modify the input list.
    '''
    if not costs:
        return 0
    n = len(costs) // 2
    ordered = merge_sorted([list(c) for c in costs], cmp=_cmp_delta)
    total = 0
    for i, (a, b) in enumerate(ordered):
        total += b if i < n else a
    return total
