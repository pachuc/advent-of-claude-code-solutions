from collections import deque

def is_open_space(x, y, favorite_number):
    """
    Determine if a coordinate (x, y) is an open space or a wall.

    Rules:
    1. Calculate: x*x + 3*x + 2*x*y + y + y*y
    2. Add the favorite number
    3. Count the number of 1 bits in binary representation
    4. Even count = open space, Odd count = wall
    """
    if x < 0 or y < 0:
        return False

    value = x*x + 3*x + 2*x*y + y + y*y
    value += favorite_number

    # Count 1 bits in binary representation
    ones_count = bin(value).count('1')

    # Even count means open space
    return ones_count % 2 == 0


def find_shortest_path(start, target, favorite_number):
    """
    Find the shortest path from start to target using BFS.

    Args:
        start: tuple (x, y) starting position
        target: tuple (x, y) target position
        favorite_number: int used for maze generation

    Returns:
        int: minimum number of steps to reach target
    """
    # Handle edge case where start is target
    if start == target:
        return 0

    # BFS initialization
    queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
    visited = {start}

    # Four possible directions: up, down, right, left
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        x, y, steps = queue.popleft()

        # Try all four directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if this is the target
            if (nx, ny) == target:
                return steps + 1

            # Validate the new position
            if (nx >= 0 and ny >= 0 and
                (nx, ny) not in visited and
                is_open_space(nx, ny, favorite_number)):

                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    raise ValueError(f"No path found from {start} to {target}")


if __name__ == "__main__":
    # Read the favorite number from input
    with open('input.md', 'r') as f:
        FAVORITE_NUMBER = int(f.read().strip())

    # Define start and target positions
    START = (1, 1)
    TARGET = (31, 39)

    # Find and print the shortest path
    result = find_shortest_path(START, TARGET, FAVORITE_NUMBER)
    print(result)
