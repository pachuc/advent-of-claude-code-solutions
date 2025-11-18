def get_neighbor_sum(x, y, grid):
    """
    Calculate sum of all adjacent cells (8 neighbors) that have been filled.

    Args:
        x, y: Coordinates of the position
        grid: Dictionary mapping (x, y) to values

    Returns:
        Sum of all adjacent filled cells
    """
    # Define 8 neighbor offsets (including diagonals)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    total = 0
    for dx, dy in neighbors:
        neighbor_pos = (x + dx, y + dy)
        if neighbor_pos in grid:
            total += grid[neighbor_pos]

    return total


def generate_spiral_values(threshold):
    """
    Generate spiral values until one exceeds threshold.
    Each value is the sum of all adjacent filled squares.

    Args:
        threshold: The value to exceed

    Returns:
        First value that exceeds threshold
    """
    # Initialize grid with first square
    grid = {(0, 0): 1}

    # Check edge case where threshold is 0
    if 1 > threshold:
        return 1

    # Initialize spiral movement state
    x, y = 0, 0
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # RIGHT, UP, LEFT, DOWN
    dir_idx = 0  # Start facing RIGHT
    steps_in_direction = 1
    steps_taken = 0
    direction_changes = 0

    # Main loop: generate positions 2, 3, 4, ...
    while True:
        # Move to next position in spiral
        x += directions[dir_idx][0]
        y += directions[dir_idx][1]
        steps_taken += 1

        # Check if we need to turn (AFTER moving)
        if steps_taken == steps_in_direction:
            dir_idx = (dir_idx + 1) % 4
            direction_changes += 1
            steps_taken = 0

            # Increase step count every 2 turns
            if direction_changes % 2 == 0:
                steps_in_direction += 1

        # Calculate value for current position
        value = get_neighbor_sum(x, y, grid)

        # Store in grid
        grid[(x, y)] = value

        # Check termination condition
        if value > threshold:
            return value


def verify_solution():
    """
    Run verification tests to ensure correctness.
    """
    print("Running verification tests...\n")

    # Test 3.1: First 23 values match example
    expected = [1, 1, 2, 4, 5, 10, 11, 23, 25, 26, 54, 57, 59, 122, 133, 142, 147, 304, 330, 351, 362, 747, 806]

    # Generate first 23 values by using thresholds
    print("Test 3.1: Verifying first 23 values match example")
    grid = {(0, 0): 1}
    x, y = 0, 0
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    dir_idx = 0
    steps_in_direction = 1
    steps_taken = 0
    direction_changes = 0

    values = [1]  # First value

    for i in range(22):  # Generate 22 more values
        x += directions[dir_idx][0]
        y += directions[dir_idx][1]
        steps_taken += 1

        if steps_taken == steps_in_direction:
            dir_idx = (dir_idx + 1) % 4
            direction_changes += 1
            steps_taken = 0
            if direction_changes % 2 == 0:
                steps_in_direction += 1

        value = get_neighbor_sum(x, y, grid)
        grid[(x, y)] = value
        values.append(value)

    # Compare
    all_match = True
    for i, (actual, exp) in enumerate(zip(values, expected), 1):
        if actual != exp:
            print(f"  Position {i}: Expected {exp}, got {actual} ✗")
            all_match = False

    if all_match:
        print(f"  All 23 values match! ✓")
    else:
        print(f"  Actual values: {values}")
        print(f"  Expected:      {expected}")

    print()

    # Test 3.2: Small threshold examples
    print("Test 3.2: Small threshold examples")
    test_cases = [
        (0, 1),
        (1, 2),
        (2, 4),
        (10, 11),
        (25, 26),
        (800, 806)
    ]

    for threshold, expected in test_cases:
        result = generate_spiral_values(threshold)
        status = "✓" if result == expected else "✗"
        print(f"  Threshold {threshold}: Expected {expected}, got {result} {status}")

    print()


def main():
    # Read input
    with open('input.md', 'r') as f:
        threshold = int(f.read().strip())

    # Calculate result
    result = generate_spiral_values(threshold)

    # Output result
    print(result)


if __name__ == "__main__":
    main()
