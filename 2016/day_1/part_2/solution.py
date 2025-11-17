"""
Solution for Part 2: First Location Visited Twice
Find the Manhattan distance to the first position visited twice while following instructions.
"""

# Direction vectors: [North, East, South, West]
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_input(filename):
    """Parse input file and return list of (turn, steps) tuples"""
    with open(filename, 'r') as f:
        content = f.read().strip()
    # Split by comma and strip whitespace from each instruction
    instructions = [inst.strip() for inst in content.split(',')]
    parsed = [(inst[0], int(inst[1:])) for inst in instructions]
    return parsed


def turn_right(current_dir):
    """Turn right 90 degrees from current direction"""
    return (current_dir + 1) % 4


def turn_left(current_dir):
    """Turn left 90 degrees from current direction"""
    return (current_dir - 1) % 4


def calculate_manhattan_distance(x, y):
    """Calculate Manhattan distance from origin to (x, y)"""
    return abs(x) + abs(y)


def find_first_revisited_position(instructions):
    """
    Follow instructions and return the first position visited twice.
    Tracks every individual block visited, not just positions after each instruction.

    Returns:
        tuple (x, y): The first position visited twice

    Raises:
        ValueError: If no position is visited twice (unexpected for valid input)
    """
    x, y = 0, 0
    direction = 0  # Start facing North
    visited = set()
    visited.add((0, 0))  # Mark starting position as visited

    for turn, steps in instructions:
        # Apply turn
        if turn == 'R':
            direction = turn_right(direction)
        else:  # turn == 'L'
            direction = turn_left(direction)

        # Move forward one block at a time, checking each position
        dx, dy = DIRECTIONS[direction]
        for step in range(steps):
            x += dx
            y += dy
            if (x, y) in visited:
                # Found first revisit!
                return x, y
            visited.add((x, y))

    # If we get here, no position was visited twice
    raise ValueError("No position visited twice - unexpected!")


def verify_part2_example():
    """Verify implementation with the provided example"""
    # Example: R8, R4, R4, R8 → first revisit at (4, 0), distance 4
    test = [('R', 8), ('R', 4), ('R', 4), ('R', 8)]
    x, y = find_first_revisited_position(test)
    distance = calculate_manhattan_distance(x, y)

    assert (x, y) == (4, 0), f"Example failed: got {(x, y)}, expected (4, 0)"
    assert distance == 4, f"Example failed: got distance {distance}, expected 4"

    print("✓ Example passed: R8, R4, R4, R8 → first revisit at (4, 0), distance 4")


def test_edge_cases():
    """Test various edge cases"""
    print("\nRunning edge case tests...")

    # Test 1: Return to origin
    test1 = [('R', 1), ('R', 1), ('R', 1), ('R', 1)]
    x, y = find_first_revisited_position(test1)
    assert (x, y) == (0, 0), f"Return to origin failed: got {(x, y)}"
    print(f"✓ Test 1 passed: Return to origin → (0, 0), distance {calculate_manhattan_distance(x, y)}")

    # Test 2: Early revisit
    test2 = [('R', 2), ('L', 1), ('L', 1), ('L', 2)]
    x, y = find_first_revisited_position(test2)
    assert (x, y) == (1, 0), f"Early revisit failed: got {(x, y)}"
    print(f"✓ Test 2 passed: Early revisit → (1, 0), distance {calculate_manhattan_distance(x, y)}")

    # Test 3: Multiple revisits in single instruction (should stop at first)
    test3 = [('R', 5), ('R', 1), ('R', 1), ('R', 10)]
    x, y = find_first_revisited_position(test3)
    assert (x, y) == (4, 0), f"Multiple revisits failed: got {(x, y)}"
    print(f"✓ Test 3 passed: Stops at first revisit → (4, 0), distance {calculate_manhattan_distance(x, y)}")

    print("All edge case tests passed!")


def solve_part2(filename):
    """
    Solve Part 2 of the puzzle.

    Returns:
        tuple (distance, (x, y)): Manhattan distance and position of first revisit
    """
    instructions = parse_input(filename)
    revisited_x, revisited_y = find_first_revisited_position(instructions)
    distance = calculate_manhattan_distance(revisited_x, revisited_y)
    return distance, (revisited_x, revisited_y)


def main():
    # Verify implementation with example
    print("Verifying implementation with example...")
    verify_part2_example()

    # Test edge cases
    test_edge_cases()
    print()

    # Process actual input
    print("Processing actual input from input.md...")
    instructions = parse_input('input.md')
    print(f"Number of instructions: {len(instructions)}")

    distance, (x, y) = solve_part2('input.md')

    print(f"\nFirst position visited twice: ({x}, {y})")
    print(f"Manhattan distance: {distance}")

    # Sanity check
    total_steps = sum(steps for _, steps in instructions)
    assert 0 <= distance <= total_steps, \
        f"Result {distance} is outside valid range [0, {total_steps}]"
    print(f"Sanity check passed: {distance} is within bounds [0, {total_steps}]")


if __name__ == '__main__':
    main()
