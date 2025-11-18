"""
Hexagonal Grid Navigation Distance Solver

This solution calculates the minimum number of steps needed to reach
a final position on a hexagonal grid after following a series of moves.

Uses cube coordinates (x, y, z) where x + y + z = 0 for efficient
distance calculation.
"""

# Cube coordinate deltas for each direction
# Each direction maintains the invariant: x + y + z = 0
DIRECTION_DELTAS = {
    'n':  (0, 1, -1),   # North: y increases, z decreases
    'ne': (1, 0, -1),   # Northeast: x increases, z decreases
    'se': (1, -1, 0),   # Southeast: x increases, y decreases
    's':  (0, -1, 1),   # South: y decreases, z increases
    'sw': (-1, 0, 1),   # Southwest: x decreases, z increases
    'nw': (-1, 1, 0)    # Northwest: x decreases, y increases
}


def parse_input(filename='input.md'):
    """
    Read the input file and parse comma-separated moves.

    Args:
        filename: Path to input file

    Returns:
        List[str]: List of direction strings
    """
    with open(filename, 'r') as f:
        content = f.read().strip()

    # Handle empty input
    if not content:
        return []

    # Split by comma and strip whitespace from each move
    return [move.strip() for move in content.split(',') if move.strip()]


def calculate_final_position(moves):
    """
    Process all moves and calculate final cube coordinates.

    Args:
        moves: List of direction strings

    Returns:
        Tuple[int, int, int]: Final (x, y, z) cube coordinates
    """
    x, y, z = 0, 0, 0  # Start at origin

    for move in moves:
        # Input validation
        if move not in DIRECTION_DELTAS:
            raise ValueError(f"Invalid direction: '{move}'. Valid directions: n, ne, se, s, sw, nw")

        dx, dy, dz = DIRECTION_DELTAS[move]
        x += dx
        y += dy
        z += dz

    return (x, y, z)


def calculate_distance(x, y, z):
    """
    Calculate shortest distance from origin to (x, y, z) in hexagonal grid.

    The distance formula for cube coordinates is:
    distance = (|x| + |y| + |z|) / 2

    This works because in cube coordinates with x + y + z = 0,
    the Manhattan distance divided by 2 gives the actual hex distance.

    Args:
        x, y, z: Cube coordinates

    Returns:
        int: Minimum number of steps to reach position from origin
    """
    return (abs(x) + abs(y) + abs(z)) // 2


def solve():
    """
    Main solution function.

    Returns:
        int: Minimum number of steps to reach final position from origin
    """
    # Parse input
    moves = parse_input('input.md')

    # Calculate final position
    x, y, z = calculate_final_position(moves)

    # Calculate distance from origin
    distance = calculate_distance(x, y, z)

    return distance


if __name__ == '__main__':
    result = solve()
    print(result)
