def solve_santa_delivery(input_string: str) -> int:
    """
    Calculate unique houses visited by Santa and Robo-Santa.

    Args:
        input_string: String of directional commands (^, v, <, >)

    Returns:
        int: Number of unique houses that received at least one present
    """
    # Direction mapping: character -> (dx, dy)
    directions = {
        '^': (0, 1),   # north
        'v': (0, -1),  # south
        '>': (1, 0),   # east
        '<': (-1, 0)   # west
    }

    # Initialize positions for both Santa and Robo-Santa
    santa_pos = [0, 0]
    robo_pos = [0, 0]

    # Set to track all visited houses
    visited = set()
    # Add starting position (both start here)
    visited.add((0, 0))

    # Process each command
    for i, direction in enumerate(input_string):
        # Get the direction change
        dx, dy = directions[direction]

        # Determine whose turn it is
        if i % 2 == 0:
            # Even index: Santa's turn
            santa_pos[0] += dx
            santa_pos[1] += dy
            visited.add((santa_pos[0], santa_pos[1]))
        else:
            # Odd index: Robo-Santa's turn
            robo_pos[0] += dx
            robo_pos[1] += dy
            visited.add((robo_pos[0], robo_pos[1]))

    return len(visited)


def main():
    # Read input from input.md
    with open('input.md', 'r') as f:
        input_string = f.read().strip()

    # Solve and print result
    result = solve_santa_delivery(input_string)
    print(f"Houses visited: {result}")

    return result


if __name__ == "__main__":
    main()
