from itertools import combinations


def parse_input(filename):
    """
    Read and parse container sizes from input file.

    Returns:
        list[int]: List of container capacities
    """
    containers = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                containers.append(int(line))
    return containers


def find_minimum_container_ways(containers, target):
    """
    Find number of ways to use minimum containers to reach target sum.

    Args:
        containers: list of container sizes
        target: target volume (150)

    Returns:
        int: Number of ways using minimum containers
    """
    # Iterate through possible combination sizes (k = 1, 2, 3, ...)
    for k in range(1, len(containers) + 1):
        valid_count = 0

        # Generate all combinations of k containers
        for combo in combinations(containers, k):
            if sum(combo) == target:
                valid_count += 1

        # If we found valid combinations at this size, k is the minimum
        if valid_count > 0:
            return valid_count

    # No solution found
    return 0


def main():
    """
    Main execution function.
    """
    TARGET = 150
    containers = parse_input('input.md')
    result = find_minimum_container_ways(containers, TARGET)
    print(result)


if __name__ == "__main__":
    main()
