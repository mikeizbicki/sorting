# Sorting
[![](https://github.com/mikeizbicki/sorting/workflows/tests-sorting/badge.svg)](https://github.com/mikeizbicki/sorting/actions?query=workflow%3Atests-sorting)
[![](https://github.com/mikeizbicki/sorting/workflows/tests-leetcode/badge.svg)](https://github.com/mikeizbicki/sorting/actions?query=workflow%3Atests-leetcode)

You will implement the merge and quick sort algorithms.

**Learning Objectives:**

1. understand how merge sort and quicksort work
1. practice recursion
1. practice using property-based tests

**Real-world application:**

Given a dataset, the first step of processing is almost always to sort the data.
This allows efficient lookups via binary search,
but it even makes sequential search significantly faster due to an optimization in modern CPUs called "branch prediction".
(See [the most upvoted stackoverflow question of all time](https://stackoverflow.com/questions/11227809/why-is-processing-a-sorted-array-faster-than-processing-an-unsorted-array) for details.)
Technical interviews therefore often require you to explain how the merge and quicksort algorithms work.

> **ASIDE:**
> Recall that Python uses the [TimSort](https://en.wikipedia.org/wiki/Timsort) algorithm.
> TimSort was named after the inventor [Tim Peters](https://en.wikipedia.org/wiki/Tim_Peters_(software_engineer)),
> who invented it specifically for python.
> Tim is one of the most influential early python programmers after Python's [BDFL](https://en.wikipedia.org/wiki/Benevolent_dictator_for_life) [Guido van Rossum](https://en.wikipedia.org/wiki/Guido_van_Rossum).
> Besides TimSort, he is most famous for developing the [Zen of Python](https://en.wikipedia.org/wiki/Zen_of_Python),
> which is a collection of sayings describing python's guiding philosophy.
> You can access the Zen of Python from within python by running the command
> ```
> >>> import this
> ```

In the real world, you should never implement your own sorting algorithm.
The algorithms built-in to standard libraries are highly optimized by highly skilled engineers,
and therefore will be much faster than anything you are likely to write.

So why are you implementing them in this assignment?
The divide-and-conquer strategy used in merge/quick sort turns out to be the most fundamental tool for building your own fast algorithms,
and the main purpose of this assignment is to practice this divde-and-conquer programming technique.
Next week, we will explore this strategy for massively parallel data analysis of multi-terabyte twitter data.
If you take CS148 (graph algorithms), you will explore many more variations of the divide and conquer technique for developing fast algorithms.
Data science tasks frequently rely on matrix multiplication and the fourier transform,
and the fastest versions of these algorithms are implemented via divide and conquer.

## Tasks

Complete the following tasks:

1. Fork the repo and enable github actions
1. Update the `README.md` file so that the test case badges point to your repo.
1. Implement all functions so that all test cases pass.

## Submission

Submit the link to your forked repository on canvas.
