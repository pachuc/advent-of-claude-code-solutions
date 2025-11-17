"""
Solution for Package Balancing and Quantum Entanglement Optimization
Advent of Code 2015 - Day 24 Part 1
"""

from itertools import combinations
import math


def parse_input(filepath):
    """
    Parse input file and return list of package weights.

    Args:
        filepath: Path to input file

    Returns:
        List of integers representing package weights
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    packages = []
    for line in lines:
        line = line.strip()
        if line:  # Filter empty lines
            packages.append(int(line))

    return packages


def get_remaining_packages(packages, group1):
    """
    Remove group1 items from packages, handling duplicates correctly.

    Args:
        packages: List of all package weights
        group1: Tuple of weights in group 1

    Returns:
        List of remaining package weights
    """
    remaining = packages[:]  # Create a copy
    for item in group1:
        remaining.remove(item)  # Removes first occurrence
    return remaining


def can_partition_remaining(remaining_packages, target):
    """
    Check if remaining packages can be split into two groups of equal weight.
    Uses dynamic programming subset sum algorithm.

    Args:
        remaining_packages: List of remaining package weights
        target: Target weight for each group

    Returns:
        True if remaining can be split into two groups of target weight each
    """
    # Safety check: remaining packages must sum to exactly 2*target
    if sum(remaining_packages) != 2 * target:
        return False

    # We need to find one subset summing to target
    # The rest will automatically sum to target (since remaining sum = 2*target)
    dp = [False] * (target + 1)
    dp[0] = True

    for package in remaining_packages:
        # Traverse backwards to avoid using same package twice
        for w in range(target, package - 1, -1):
            if dp[w - package]:
                dp[w] = True

    return dp[target]


def calculate_qe(packages):
    """
    Calculate quantum entanglement (product of all package weights).

    Args:
        packages: List or tuple of package weights

    Returns:
        Product of all package weights
    """
    return math.prod(packages)


def solve(packages=None):
    """
    Main solver function to find optimal package configuration.

    Args:
        packages: List of package weights (if None, reads from input.md)

    Returns:
        Minimum quantum entanglement for optimal Group 1, or None if no solution
    """
    # Parse input if not provided
    if packages is None:
        packages = parse_input("input.md")

    # Input validation
    if not packages or any(p <= 0 for p in packages):
        return None  # Invalid input

    total_weight = sum(packages)

    if total_weight % 3 != 0:
        return None  # No solution possible

    target = total_weight // 3

    # Sort descending for better combinations (helps find smaller groups faster)
    packages.sort(reverse=True)

    # Find optimal configuration
    for group_size in range(1, len(packages)):
        valid_qe_values = []

        # Generate combinations of current size
        for group1 in combinations(packages, group_size):
            # Check if sums to target
            if sum(group1) != target:
                continue

            # Get remaining packages
            remaining = get_remaining_packages(packages, group1)

            # Validate remaining can be split into 2 equal groups
            if can_partition_remaining(remaining, target):
                qe = calculate_qe(group1)
                valid_qe_values.append(qe)

        # If we found valid configurations, return minimum QE
        if valid_qe_values:
            return min(valid_qe_values)

    return None  # No solution found


def main():
    """Main execution function."""
    result = solve()
    if result is not None:
        print(f"Quantum Entanglement: {result}")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
