"""DSA S1 - G1 session 3 - Lab 5: sorting in use (records, duplicates, pairs, inversions).

Run the tests:  python test_lab5.py      Run the timings:  python lab5_applications_starter.py
Uses only what we have seen: loops, recursion, insertion / bubble / merge sort, sets as a black box.
Do not call sorted() or list.sort() in Tasks 1 to 4: use merge_sort / merge_sort_key.
"""
import random
import timeit


# ---------------------------------------------------------------------------
# Given: the merge sort of Lab 4 (stable, returns a NEW list). Do not edit.
# ---------------------------------------------------------------------------
def merge_sort(a):
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


# ---------------------------------------------------------------------------
# Task 1: sort records by one or several keys
# A record is a tuple (city, name, age).
# ---------------------------------------------------------------------------
def merge_sort_key(a, key):
    """Sort by key(x), stably, and return a new list."""
    if len(a) <= 1:
        return list(a)

    mid = len(a) // 2
    left = merge_sort_key(a[:mid], key)
    right = merge_sort_key(a[mid:], key)

    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1

    out.extend(left[i:])
    out.extend(right[j:])
    return out


def sort_two_passes(records):
    """Sort by city, then name within each city, using stable passes."""
    by_name = merge_sort_key(records, key=lambda record: record[1])
    return merge_sort_key(by_name, key=lambda record: record[0])


def sort_one_pass(records):
    """Sort by city, then name, using one tuple key."""
    return merge_sort_key(records, key=lambda record: (record[0], record[1]))


# ---------------------------------------------------------------------------
# Task 2: does a list contain a duplicate? Three ways, three costs.
# ---------------------------------------------------------------------------
def has_dup_nested(a):
    """Check every pair of positions. O(n^2) time."""
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] == a[j]:
                return True
    return False


def has_dup_sort(a):
    """Sort a copy, then compare neighbors. O(n log n) time."""
    ordered = merge_sort(a)
    for i in range(1, len(ordered)):
        if ordered[i] == ordered[i - 1]:
            return True
    return False


def has_dup_set(a):
    """Track seen items in a set. O(n) average time."""
    seen = set()
    for item in a:
        if item in seen:
            return True
        seen.add(item)
    return False


def dup_timings(sizes=(1000, 2000, 4000, 8000)):
    """Print timings for lists without duplicates and their doubling ratios."""
    print(f"{'n':>7} {'nested':>9} {'sort':>8} {'set':>8}")

    times = []
    for n in sizes:
        a = random.sample(range(10 * n), n)

        t_nested = min(
            timeit.timeit(lambda: has_dup_nested(a), number=1)
            for _ in range(2)
        )
        t_sort = min(
            timeit.timeit(lambda: has_dup_sort(a), number=1)
            for _ in range(2)
        )
        t_set = min(
            timeit.timeit(lambda: has_dup_set(a), number=1)
            for _ in range(2)
        )

        times.append((t_nested, t_sort, t_set))
        print(
            f"{n:>7} {t_nested * 1000:>9.1f} "
            f"{t_sort * 1000:>8.1f} {t_set * 1000:>8.1f}"
        )

    print("\nDoubling ratios (current size / previous size):")
    print(f"{'n':>7} {'nested':>9} {'sort':>8} {'set':>8}")
    for i in range(1, len(sizes)):
        ratios = [
            times[i][j] / times[i - 1][j] if times[i - 1][j] else 0
            for j in range(3)
        ]
        print(
            f"{sizes[i]:>7} {ratios[0]:>9.2f} "
            f"{ratios[1]:>8.2f} {ratios[2]:>8.2f}"
        )


# ---------------------------------------------------------------------------
# Task 3: is there a pair of items at different positions with a given sum?
# ---------------------------------------------------------------------------
def has_pair_brute(a, target):
    """Check every pair of positions. O(n^2) time."""
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] + a[j] == target:
                return True
    return False


def has_pair_sorted(a, target):
    """Sort a copy, then move two pointers inward. O(n log n) time."""
    ordered = merge_sort(a)
    lo = 0
    hi = len(ordered) - 1

    while lo < hi:
        total = ordered[lo] + ordered[hi]

        if total == target:
            return True
        elif total < target:
            lo += 1
        else:
            hi -= 1

    return False


def has_pair_set(a, target):
    """Check for each item's complement in a set. O(n) average time."""
    seen = set()
    for item in a:
        if target - item in seen:
            return True
        seen.add(item)
    return False


# ---------------------------------------------------------------------------
# Task 4 (stretch): count inversions with divide and conquer.
# An inversion is a pair of positions i < j with a[i] > a[j].
# ---------------------------------------------------------------------------
def insertion_shift_count(a):
    """Given: run insertion sort on a copy of a and return the number of shifts."""
    a = list(a)
    shifts = 0
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            shifts += 1
            j -= 1
        a[j + 1] = x
    return shifts


def count_inversions(a):
    """Count inversions in O(n log n) time without changing a."""
    def sort_and_count(items):
        if len(items) <= 1:
            return list(items), 0

        mid = len(items) // 2
        left, left_count = sort_and_count(items[:mid])
        right, right_count = sort_and_count(items[mid:])

        merged = []
        i = j = 0
        split_count = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                split_count += len(left) - i
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        total_count = left_count + right_count + split_count
        return merged, total_count

    return sort_and_count(a)[1]


if __name__ == "__main__":
    dup_timings()
