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


def count_reachable_locations(start, max_steps, favorite_number, debug=False):
    """
    Count all distinct locations reachable within max_steps from start.

    Args:
        start: tuple (x, y) starting position
        max_steps: int maximum number of steps allowed
        favorite_number: int used for maze generation
        debug: bool if True, return (count, visited_set) for validation

    Returns:
        int: count of distinct reachable locations (including start)
        OR (int, set): (count, visited_set) if debug=True
    """
    # BFS initialization
    queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
    visited = {start}  # Track all visited locations

    # Four possible directions: up, down, right, left
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        x, y, steps = queue.popleft()

        # Only explore further if we haven't reached step limit
        if steps < max_steps:
            # Try all four directions
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                # Validate the new position
                if (nx >= 0 and ny >= 0 and
                    (nx, ny) not in visited and
                    is_open_space(nx, ny, favorite_number)):

                    visited.add((nx, ny))
                    queue.append((nx, ny, steps + 1))

    if debug:
        return len(visited), visited
    return len(visited)


if __name__ == "__main__":
    # Read the favorite number from input
    with open('input.md', 'r') as f:
        FAVORITE_NUMBER = int(f.read().strip())

    # Define start position and step limit
    START = (1, 1)
    MAX_STEPS = 50

    # Count and print reachable locations
    result = count_reachable_locations(START, MAX_STEPS, FAVORITE_NUMBER)
    print(result)
