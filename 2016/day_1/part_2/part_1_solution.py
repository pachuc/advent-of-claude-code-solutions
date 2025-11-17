"""
Solution for Taxicab Distance Calculator
Calculate Manhattan distance from origin after following turn-and-move instructions.
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


def follow_instructions(instructions):
    """Follow all instructions and return final position (x, y)"""
    x, y = 0, 0
    direction = 0  # Start facing North

    for turn, steps in instructions:
        # Apply turn
        if turn == 'R':
            direction = turn_right(direction)
        else:  # turn == 'L'
            direction = turn_left(direction)

        # Move forward
        dx, dy = DIRECTIONS[direction]
        x += dx * steps
        y += dy * steps

    return x, y


def calculate_manhattan_distance(x, y):
    """Calculate Manhattan distance from origin to (x, y)"""
    return abs(x) + abs(y)


def verify_with_examples():
    """Verify implementation with provided examples"""
    # Example 1: R2, L3 → distance 5
    test1 = [('R', 2), ('L', 3)]
    x, y = follow_instructions(test1)
    assert (x, y) == (2, 3), f"Example 1 failed: got {(x, y)}, expected (2, 3)"
    assert calculate_manhattan_distance(x, y) == 5
    print("✓ Example 1 passed: R2, L3 → distance 5")

    # Example 2: R2, R2, R2 → distance 2
    test2 = [('R', 2), ('R', 2), ('R', 2)]
    x, y = follow_instructions(test2)
    assert (x, y) == (0, -2), f"Example 2 failed: got {(x, y)}, expected (0, -2)"
    assert calculate_manhattan_distance(x, y) == 2
    print("✓ Example 2 passed: R2, R2, R2 → distance 2")

    # Example 3: R5, L5, R5, R3 → distance 12
    test3 = [('R', 5), ('L', 5), ('R', 5), ('R', 3)]
    x, y = follow_instructions(test3)
    assert (x, y) == (10, 2), f"Example 3 failed: got {(x, y)}, expected (10, 2)"
    assert calculate_manhattan_distance(x, y) == 12
    print("✓ Example 3 passed: R5, L5, R5, R3 → distance 12")

    print("All examples verified successfully!")


def sanity_check(instructions, result):
    """Verify the result is within reasonable bounds"""
    total_steps = sum(steps for _, steps in instructions)
    max_distance = total_steps
    min_distance = 0

    assert min_distance <= result <= max_distance, \
        f"Result {result} is outside valid range [{min_distance}, {max_distance}]"

    print(f"Sanity check passed: {result} is within bounds [0, {max_distance}]")


def main():
    # Verify implementation with examples
    print("Verifying implementation with examples...")
    verify_with_examples()
    print()

    # Process actual input
    print("Processing actual input from input.md...")
    instructions = parse_input('input.md')
    print(f"Number of instructions: {len(instructions)}")

    final_x, final_y = follow_instructions(instructions)
    print(f"Final position: ({final_x}, {final_y})")

    distance = calculate_manhattan_distance(final_x, final_y)

    # Sanity check the result
    sanity_check(instructions, distance)
    print()

    print(f"Manhattan distance: {distance}")


if __name__ == '__main__':
    main()
