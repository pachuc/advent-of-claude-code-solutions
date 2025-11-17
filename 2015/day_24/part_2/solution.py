from itertools import combinations
from collections import Counter
from functools import lru_cache
import math


def parse_input(filename):
    """Parse the input file and return list of package weights."""
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]


def calculate_qe(group):
    """Calculate quantum entanglement (product of all weights in group)."""
    return math.prod(group)


def get_remaining(packages, first_group):
    """Get remaining packages after removing first_group using Counter."""
    package_counts = Counter(packages)
    first_group_counts = Counter(first_group)
    remaining_counts = package_counts - first_group_counts
    return list(remaining_counts.elements())


def can_split_into_three_groups(packages, target):
    """
    Check if packages can be split into exactly 3 groups, each with sum = target.
    Uses recursive backtracking with memoization.
    """
    # Quick check: total must equal 3 * target
    if sum(packages) != 3 * target:
        return False

    # Convert to tuple for caching
    packages_tuple = tuple(sorted(packages))
    return can_split_into_n_groups_cached(packages_tuple, target, 3)


@lru_cache(maxsize=None)
def can_split_into_n_groups_cached(packages_tuple, target, n_groups):
    """
    Cached recursive function to check if packages can be split into n_groups
    with each group summing to target.
    """
    packages = list(packages_tuple)

    # Base case: need 0 groups, should have 0 packages
    if n_groups == 0:
        return len(packages) == 0

    # Base case: need 1 group, check if sum equals target
    if n_groups == 1:
        return sum(packages) == target

    # Try to form one group with sum = target, then recurse on remaining
    # Try different sizes starting from smallest
    for group_size in range(1, len(packages) + 1):
        for combo in combinations(packages, group_size):
            if sum(combo) == target:
                # Found a valid group, check if remaining can form (n_groups - 1) groups
                remaining = get_remaining(packages, combo)
                remaining_tuple = tuple(sorted(remaining))
                if can_split_into_n_groups_cached(remaining_tuple, target, n_groups - 1):
                    return True

    return False


def solve(packages):
    """
    Find the minimum quantum entanglement of the first group when dividing
    packages into 4 equal-weight groups.
    """
    total_weight = sum(packages)

    # Check if divisible by 4
    if total_weight % 4 != 0:
        return None

    target = total_weight // 4
    min_qe = float('inf')
    found_valid = False

    # Try increasing first group sizes
    for group_size in range(1, len(packages)):
        current_size_has_valid = False

        for combo in combinations(packages, group_size):
            if sum(combo) == target:
                # Check if remaining can form 3 equal groups
                remaining = get_remaining(packages, combo)
                if can_split_into_three_groups(remaining, target):
                    current_size_has_valid = True
                    qe = calculate_qe(combo)
                    min_qe = min(min_qe, qe)

        # If we found valid configs at this size, don't check larger sizes
        if current_size_has_valid:
            return min_qe

    return None


if __name__ == "__main__":
    # Read input
    packages = parse_input('input.md')

    # Solve
    result = solve(packages)

    print(f"Minimum Quantum Entanglement: {result}")
