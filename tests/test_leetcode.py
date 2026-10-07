import doctest
import itertools
from functools import cmp_to_key

from hypothesis import assume, given
import hypothesis.strategies as st

from src import leetcode


def test_doctests():
    results = doctest.testmod(leetcode, verbose=False)
    assert results.failed == 0


# ---------------------------------------------------------------------------
# LeetCode 56 -- Merge Intervals
# ---------------------------------------------------------------------------

intervals = st.lists(
    st.lists(st.integers(min_value=-20, max_value=20), min_size=2, max_size=2).map(sorted),
    max_size=8,
)


def _merge_intervals_reference(intervals):
    result = []
    for start, end in sorted(intervals):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result


@given(intervals=intervals)
def test_merge_intervals(intervals):
    assert leetcode.merge_intervals(intervals) == _merge_intervals_reference(intervals)


# ---------------------------------------------------------------------------
# LeetCode 1366 -- Rank Teams by Votes
# ---------------------------------------------------------------------------

@given(
    teams=st.lists(st.sampled_from('ABCDE'), min_size=1, max_size=4, unique=True),
    data=st.data(),
)
def test_rank_teams(teams, data):
    votes = [
        ''.join(data.draw(st.lists(
            st.sampled_from(teams),
            min_size=len(teams),
            max_size=len(teams),
            unique=True,
        )))
        for _ in range(data.draw(st.integers(min_value=1, max_value=5)))
    ]
    counts = {team: [0] * len(teams) for team in teams}
    for vote in votes:
        for i, team in enumerate(vote):
            counts[team][i] += 1
    expected = ''.join(sorted(teams, key=lambda t: ([-n for n in counts[t]], t)))
    assert leetcode.rank_teams(votes) == expected


# ---------------------------------------------------------------------------
# LeetCode 179 -- Largest Number
# ---------------------------------------------------------------------------

def _largest_number_reference(nums):
    def cmp(a, b):
        if a + b > b + a:
            return -1
        return 1 if b + a > a + b else 0
    strs = sorted((str(n) for n in nums), key=cmp_to_key(cmp))
    result = ''.join(strs).lstrip('0')
    return result or '0'


@given(nums=st.lists(st.integers(min_value=0, max_value=10 ** 6), min_size=1, max_size=8))
def test_largest_number(nums):
    assert leetcode.largest_number(nums) == _largest_number_reference(nums)


# ---------------------------------------------------------------------------
# LeetCode 1029 -- Two City Scheduling
# ---------------------------------------------------------------------------

costs = st.lists(
    st.lists(st.integers(min_value=0, max_value=1000), min_size=2, max_size=2),
    min_size=2,
    max_size=6,
)


@given(costs=costs)
def test_two_city_sched_cost(costs):
    assume(len(costs) % 2 == 0)
    n = len(costs) // 2
    best = min(
        sum(costs[i][0] if i in a_indices else costs[i][1] for i in range(len(costs)))
        for a_indices in (
            set(indices) for indices in itertools.combinations(range(len(costs)), n)
        )
    )
    assert leetcode.two_city_sched_cost(costs) == best
