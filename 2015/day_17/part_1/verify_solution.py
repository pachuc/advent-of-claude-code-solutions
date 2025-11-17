from solution import parse_input


def count_combinations_iterative(containers, target):
    """
    Use bit manipulation to iterate through all 2^n subsets.
    Alternative implementation for verification.
    """
    count = 0
    n = len(containers)

    # Iterate through all possible subsets (2^n combinations)
    for mask in range(1 << n):  # 2^n
        subset_sum = 0
        for i in range(n):
            if mask & (1 << i):  # Check if i-th bit is set
                subset_sum += containers[i]

        if subset_sum == target:
            count += 1

    return count


def main():
    """Verify both implementations produce the same result."""
    from solution import count_combinations

    # Parse input
    containers = parse_input('input.md')

    # Run both implementations
    result_recursive = count_combinations(containers, 150)
    result_iterative = count_combinations_iterative(containers, 150)

    print(f"Recursive implementation result: {result_recursive}")
    print(f"Iterative implementation result: {result_iterative}")

    if result_recursive == result_iterative:
        print("\n✓ Both implementations agree!")
        print(f"✓ Answer verified: {result_recursive}")
    else:
        print("\n✗ Implementations disagree!")
        print(f"✗ Recursive: {result_recursive}, Iterative: {result_iterative}")


if __name__ == '__main__':
    main()
