import heapq

# Equipment types
TORCH = 0
CLIMBING_GEAR = 1
NEITHER = 2

# Region types
ROCKY = 0
WET = 1
NARROW = 2

# Equipment validity for each region type
VALID_EQUIPMENT = {
    ROCKY: {TORCH, CLIMBING_GEAR},     # Can't use neither
    WET: {CLIMBING_GEAR, NEITHER},      # Can't use torch
    NARROW: {TORCH, NEITHER}            # Can't use climbing gear
}


def parse_input(filename):
    """
    Parse the input file to extract depth and target coordinates.

    Expected format:
    depth: <integer>
    target: <X>,<Y>

    Returns:
        tuple: (depth, target_x, target_y)
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    depth = None
    target_x = None
    target_y = None

    for line in lines:
        line = line.strip()
        if line.startswith('depth:'):
            depth = int(line.split(':')[1].strip())
        elif line.startswith('target:'):
            coords = line.split(':')[1].strip()
            target_x, target_y = map(int, coords.split(','))

    return depth, target_x, target_y


def calculate_erosion_level(geologic_index, depth):
    """
    Calculate erosion level from geologic index.

    Formula: (geologic_index + depth) % 20183

    Args:
        geologic_index: The geologic index
        depth: Cave system depth

    Returns:
        int: Erosion level
    """
    return (geologic_index + depth) % 20183


def calculate_geologic_index(x, y, target_x, target_y, erosion_levels):
    """
    Calculate geologic index for position (x, y).

    Rules (in order of precedence):
    1. Cave mouth (0,0): return 0
    2. Target position: return 0
    3. Y == 0: return X * 16807
    4. X == 0: return Y * 48271
    5. Otherwise: return erosion_level(x-1, y) * erosion_level(x, y-1)

    Args:
        x, y: Current coordinates
        target_x, target_y: Target coordinates
        erosion_levels: 2D structure storing computed erosion levels

    Returns:
        int: Geologic index for the position
    """
    # Rule 1: Cave mouth
    if x == 0 and y == 0:
        return 0

    # Rule 2: Target position
    if x == target_x and y == target_y:
        return 0

    # Rule 3: Top edge (Y = 0)
    if y == 0:
        return x * 16807

    # Rule 4: Left edge (X = 0)
    if x == 0:
        return y * 48271

    # Rule 5: Interior cells
    return erosion_levels[y][x-1] * erosion_levels[y-1][x]


def build_cave_map(depth, target_x, target_y, margin=50):
    """
    Build a cave map extending beyond target by margin.

    The map uses [y][x] indexing: cave_map[y][x] gives the region type at position (x, y).

    Returns:
        2D list where cave_map[y][x] = region_type (ROCKY/WET/NARROW) for position (x, y)
    """
    max_x = target_x + margin
    max_y = target_y + margin

    # Initialize 2D arrays for erosion levels and cave map
    erosion_levels = [[0] * (max_x + 1) for _ in range(max_y + 1)]
    cave_map = [[0] * (max_x + 1) for _ in range(max_y + 1)]

    # Process row by row (y outer, x inner for dependency satisfaction)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            # Calculate geologic index
            geologic_index = calculate_geologic_index(x, y, target_x, target_y, erosion_levels)

            # Calculate erosion level
            erosion_level = calculate_erosion_level(geologic_index, depth)

            # Store erosion level for future dependencies
            erosion_levels[y][x] = erosion_level

            # Store region type
            cave_map[y][x] = erosion_level % 3

    return cave_map


def get_neighbors(state, cave_map, max_x, max_y):
    """
    Generate all valid transitions from current state.

    Args:
        state: (x, y, equipment) tuple
        cave_map: 2D array of region types
        max_x, max_y: Map boundaries

    Yields:
        (next_state, cost) tuples
    """
    x, y, equipment = state
    current_region = cave_map[y][x]

    # Equipment switches (cost = 7)
    for new_equipment in VALID_EQUIPMENT[current_region]:
        if new_equipment != equipment:
            yield ((x, y, new_equipment), 7)

    # Movement (cost = 1)
    # Try 4 directions: up, down, left, right
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = x + dx, y + dy

        # Check bounds (prevents negative coordinates)
        if 0 <= nx <= max_x and 0 <= ny <= max_y:
            dest_region = cave_map[ny][nx]

            # Check if current equipment is valid for destination
            if equipment in VALID_EQUIPMENT[dest_region]:
                yield ((nx, ny, equipment), 1)


def find_shortest_path(depth, target_x, target_y):
    """
    Find minimum time to reach target with torch equipped.

    Returns:
        int: Minimum time in minutes
    """
    # Build cave map with margin
    cave_map = build_cave_map(depth, target_x, target_y, margin=50)
    max_x = target_x + 50
    max_y = target_y + 50

    # Initialize Dijkstra's algorithm
    start_state = (0, 0, TORCH)
    goal_state = (target_x, target_y, TORCH)

    # Priority queue: (distance, state)
    pq = [(0, start_state)]
    distances = {start_state: 0}
    visited = set()

    while pq:
        current_dist, current_state = heapq.heappop(pq)

        # Skip if already visited
        if current_state in visited:
            continue

        visited.add(current_state)

        # Check if we reached goal
        if current_state == goal_state:
            return current_dist

        # Explore neighbors
        for next_state, cost in get_neighbors(current_state, cave_map, max_x, max_y):
            if next_state in visited:
                continue

            new_dist = current_dist + cost

            # Relaxation step
            if next_state not in distances or new_dist < distances[next_state]:
                distances[next_state] = new_dist
                heapq.heappush(pq, (new_dist, next_state))

    # Should never reach here with valid input
    raise Exception("No path found to target - try increasing margin")


def main():
    """
    Main entry point for the solution.
    """
    # Parse input
    depth, target_x, target_y = parse_input("input.md")

    # Find shortest path
    result = find_shortest_path(depth, target_x, target_y)

    # Print result
    print(result)


if __name__ == "__main__":
    main()
