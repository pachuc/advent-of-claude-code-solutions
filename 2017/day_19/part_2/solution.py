#!/usr/bin/env python3
"""
Network Packet Routing Solution - Part 2: Step Counter

This script traces a path through an ASCII art routing diagram,
counting the total number of steps taken.
"""

# Direction vectors: (row_delta, col_delta)
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


def parse_input(filename):
    """Parse the input file into a 2D grid.

    Args:
        filename: Path to input file

    Returns:
        List of strings representing the grid, with uniform width
    """
    with open(filename, 'r') as f:
        content = f.read()
        lines = content.splitlines()

    # Remove completely empty lines at the end
    while lines and not lines[-1].strip():
        lines.pop()

    # Pad lines to same width for uniform access
    max_width = max(len(line) for line in lines) if lines else 0
    grid = [line.ljust(max_width) for line in lines]
    return grid


def find_start(grid):
    """Find the starting position (the | in the first row).

    Args:
        grid: The parsed grid

    Returns:
        Tuple of (row, col) or None if not found
    """
    if not grid:
        return None
    for col, char in enumerate(grid[0]):
        if char == '|':
            return (0, col)
    return None


def get_perpendicular(direction):
    """Get the two perpendicular directions.

    Args:
        direction: Current direction tuple

    Returns:
        List of two perpendicular direction tuples
    """
    if direction in [UP, DOWN]:
        return [LEFT, RIGHT]
    else:  # LEFT or RIGHT
        return [UP, DOWN]


def is_valid_position(grid, row, col):
    """Check if position is within grid bounds.

    Args:
        grid: The parsed grid
        row: Row index
        col: Column index

    Returns:
        True if position is valid, False otherwise
    """
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def is_path_char(char):
    """Check if character is part of the path.

    Valid path characters are:
    - Pipe symbols: | (vertical)
    - Dash symbols: - (horizontal)
    - Plus symbols: + (corners/junctions)
    - Uppercase letters: A-Z (markers on the path)

    Args:
        char: Character to check

    Returns:
        True if character is part of path, False otherwise
    """
    return char in '|-+' or (char.isupper() and char.isalpha())


def get_next_position(grid, row, col, direction):
    """Get next valid position and direction.

    The algorithm prioritizes continuing straight. Only when we cannot
    continue straight do we try turning (perpendicular directions).

    Args:
        grid: The parsed grid
        row: Current row
        col: Current column
        direction: Current direction tuple

    Returns:
        Tuple of (next_row, next_col, next_direction) or None if end of path
    """
    # Try continuing in current direction first
    next_row, next_col = row + direction[0], col + direction[1]
    if is_valid_position(grid, next_row, next_col):
        next_char = grid[next_row][next_col]
        if is_path_char(next_char):
            return (next_row, next_col, direction)

    # If can't continue straight, try turning (perpendicular directions)
    for new_direction in get_perpendicular(direction):
        next_row, next_col = row + new_direction[0], col + new_direction[1]
        if is_valid_position(grid, next_row, next_col):
            next_char = grid[next_row][next_col]
            if is_path_char(next_char):
                return (next_row, next_col, new_direction)

    # No valid move found - end of path
    return None


def follow_path(grid, start_row, start_col):
    """Follow the path and count the total number of steps.

    Starting from the top of the diagram, we move DOWN onto the path.
    We count every position visited, and stop when we reach
    the end of the path (no valid next move).

    Args:
        grid: The parsed grid
        start_row: Starting row position
        start_col: Starting column position

    Returns:
        Integer representing total number of steps taken
    """
    steps = 0
    row, col = start_row, start_col
    direction = DOWN  # Packet starts by moving DOWN from top

    while True:
        # Count the current position
        steps += 1

        # Try to move to next position
        next_move = get_next_position(grid, row, col, direction)
        if next_move is None:
            break  # End of path - no valid continuation

        row, col, direction = next_move

    return steps


def main():
    """Main function to solve the problem."""
    grid = parse_input('input.md')
    start = find_start(grid)

    if start is None:
        print("No starting position found")
        return

    result = follow_path(grid, start[0], start[1])
    print(result)


if __name__ == "__main__":
    main()
