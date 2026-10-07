#!/bin/python3
'''
This file contains leetcode problems
that you might get asked in a technical interview.
The unifying idea is that many complicated looking problems
can be solved by "just" sorting the input in a clever way.
'''


def merge_intervals(intervals):
    '''
    LeetCode 56 -- Merge Intervals
    Difficulty: Medium

    Given a list of intervals where each interval is [start, end], merge
    all overlapping intervals and return the non-overlapping intervals
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
        # an interval is a [start, end] pair
        return interval[0]


def max_profit_assignment(difficulty, profit, worker):
    '''
    LeetCode 826 -- Most Profit Assigning Work
    Difficulty: Medium

    You have n jobs.  Job i has difficulty difficulty[i] and profit
    profit[i].  You also have workers where worker[j] is the maximum job
    difficulty that worker j can handle.  Each worker can complete at
    most one job, but the same job may be taken by multiple workers.
    Return the maximum total profit.

    >>> max_profit_assignment([2,4,6,8,10], [10,20,30,40,50], [4,5,6,7])
    100
    >>> max_profit_assignment([85,47,57], [24,66,99], [40,25,25])
    0
    >>> max_profit_assignment([1,2,3], [10,20,30], [3,3,3])
    90

    Hint: zip difficulty with profit and sort the jobs by difficulty;
    sort the workers as well.  Sweeping the two lists together, a worker
    takes the largest profit among the jobs they can handle.
    '''
    def key(job):
        # a job is a (difficulty, profit) pair
        return job[0]


def rank_teams(votes):
    '''
    LeetCode 1366 -- Rank Teams by Votes
    Difficulty: Medium

    Given a list of strings where each string is one voter's ranking of
    all teams (best team first), return a single string giving the
    teams ranked from best to worst.  Teams are sorted first by how many
    voters placed them in position 0 (descending), then by position 1
    votes, and so on.  Ties are broken alphabetically.

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
    import functools

    def cmp(a, b):
        # a comes first when a+b is the larger number
        if a + b > b + a:
            return -1
        return 1 if b + a > a + b else 0


def max_ice_cream(costs, coins):
    '''
    LeetCode 1833 -- Maximum Ice Cream Bars
    Difficulty: Medium

    It costs costs[i] to buy the i-th ice cream bar.  You have `coins`
    coins.  Return the maximum number of bars you can buy.

    >>> max_ice_cream([1,3,2,4,1], 7)
    4
    >>> max_ice_cream([10,6,8,7,7,8], 5)
    0
    >>> max_ice_cream([1,6,3,1,2,5], 20)
    6

    Hint: the bars do not interact, so buy the cheapest ones first.
    Sort the costs and subtract from `coins` until it runs out; the
    number of bars bought is the answer.
    '''


def two_city_sched_cost(costs):
    '''
    LeetCode 1029 -- Two City Scheduling
    Difficulty: Medium

    You have 2n people.  Person i has costs[i] = [costA, costB], the
    cost to fly them to city A or city B respectively.  Send exactly n
    people to each city, minimizing the total cost.  Return the minimum
    cost.

    >>> two_city_sched_cost([[10,20],[30,200],[400,50],[30,20]])
    110
    >>> two_city_sched_cost([[259,770],[448,54],[926,667],
    ...                      [184,139],[840,118],[577,469]])
    1859

    Hint: fly everyone to city B as a baseline.  Moving one person to
    city A changes the total by costA - costB, and exactly n people must
    move, so sort by that difference and move the n smallest.

    '''
    def key(cost):
        # sort by the extra cost of choosing city A
        return cost[0] - cost[1]
