"""
Hexagonal Grid Navigation - Maximum Distance Tracker

This solution calculates the maximum distance from origin reached at any point
during a journey on a hexagonal grid, following a series of moves.

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


def find_max_distance(moves):
    """
    Process all moves and track the maximum distance from origin reached.

    Unlike Part 1 which only calculated the final distance, this function
    calculates the distance after EACH move and returns the maximum distance
    encountered during the entire journey.

    Args:
        moves: List of direction strings

    Returns:
        int: Maximum distance from origin reached at any point during journey
    """
    x, y, z = 0, 0, 0  # Start at origin
    max_distance = 0   # Track maximum distance

    for move in moves:
        # Input validation
        if move not in DIRECTION_DELTAS:
            raise ValueError(f"Invalid direction: '{move}'. Valid directions: n, ne, se, s, sw, nw")

        # Apply move
        dx, dy, dz = DIRECTION_DELTAS[move]
        x += dx
        y += dy
        z += dz

        # Calculate current distance from origin
        current_distance = calculate_distance(x, y, z)

        # Update maximum distance if current is greater
        max_distance = max(max_distance, current_distance)

    return max_distance


def solve():
    """
    Main solution function.

    Returns:
        int: Maximum distance from origin reached at any point during journey
    """
    # Parse input
    moves = parse_input('input.md')

    # Find maximum distance during journey
    max_distance = find_max_distance(moves)

    return max_distance


if __name__ == '__main__':
    result = solve()
    print(result)
