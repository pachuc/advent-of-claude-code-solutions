def parse_input(filename):
    """
    Read container capacities from input file.

    Args:
        filename: Path to input file (expected: 'input.md')

    Returns:
        list of integers representing container capacities
    """
    containers = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        value = int(line)
                        if value >= 0:  # Filter out negative values
                            containers.append(value)
                    except ValueError:
                        # Skip lines that can't be converted to integers
                        pass
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return []

    return containers


def count_combinations(containers, target, index=0, current_sum=0):
    """
    Count all combinations of containers that sum to target.

    Args:
        containers: List of container capacities
        target: Target volume (150 liters)
        index: Current position in containers list
        current_sum: Running sum of selected containers

    Returns:
        Number of valid combinations
    """
    # Base case: found exact match (can return immediately - pruning optimization)
    if current_sum == target:
        return 1

    # Base case: exceeded target (prune branch)
    if current_sum > target:
        return 0

    # Base case: no more containers to check
    if index >= len(containers):
        return 0

    # Recursive case: try including and excluding current container
    include = count_combinations(containers, target, index + 1, current_sum + containers[index])
    exclude = count_combinations(containers, target, index + 1, current_sum)

    return include + exclude


def main():
    """
    Main execution function.
    """
    # Parse input from 'input.md'
    containers = parse_input('input.md')

    # Handle empty input
    if not containers:
        print(0)
        return

    # Count combinations
    result = count_combinations(containers, target=150)

    # Output result
    print(result)


if __name__ == '__main__':
    main()
