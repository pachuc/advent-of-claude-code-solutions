from solution import parse_input

def count_combinations_bitmask(containers, target):
    """
    Count combinations using bit manipulation approach.
    This is an alternative implementation for verification.

    Iterates through all 2^n subsets using bitmask.
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


if __name__ == '__main__':
    # Parse input from 'input.md'
    containers = parse_input('input.md')

    # Get result from bit manipulation method
    result = count_combinations_bitmask(containers, target=150)

    print(f"Bit manipulation approach: {result}")
