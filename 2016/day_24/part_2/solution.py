from collections import deque

def parse_grid(grid_lines):
    """
    Parse the grid to find all numbered locations.

    Args:
        grid_lines: List of strings representing the grid

    Returns:
        Dictionary mapping location numbers to (row, col) coordinates
    """
    locations = {}
    for row, line in enumerate(grid_lines):
        for col, cell in enumerate(line):
            if cell.isdigit():
                locations[int(cell)] = (row, col)
    return locations


def calculate_distances(grid, locations):
    """
    Calculate shortest distances between all pairs of numbered locations using BFS.

    Args:
        grid: 2D grid as list of strings
        locations: Dictionary of location number to coordinates

    Returns:
        distances: 2D list of distances indexed by normalized location indices
        location_mapping: Dictionary mapping original location numbers to normalized indices
    """
    # Create normalized mapping (0 to N-1)
    sorted_locations = sorted(locations.keys())
    location_mapping = {loc_num: idx for idx, loc_num in enumerate(sorted_locations)}
    N = len(locations)

    # Initialize distance matrix
    distances = [[float('inf')] * N for _ in range(N)]
    for i in range(N):
        distances[i][i] = 0

    # For each location, run BFS to find distances to all other locations
    for start_loc_num, start_coords in locations.items():
        start_idx = location_mapping[start_loc_num]
        queue = deque([(start_coords[0], start_coords[1], 0)])
        visited = {start_coords}

        while queue:
            row, col, dist = queue.popleft()

            # Check if this is a numbered location
            if grid[row][col].isdigit():
                dest_loc_num = int(grid[row][col])
                dest_idx = location_mapping[dest_loc_num]
                distances[start_idx][dest_idx] = min(distances[start_idx][dest_idx], dist)

            # Explore 4 directions
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dr, col + dc

                # Check bounds and if passable
                if (0 <= new_row < len(grid) and
                    0 <= new_col < len(grid[0]) and
                    grid[new_row][new_col] != '#' and
                    (new_row, new_col) not in visited):

                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, dist + 1))

    return distances, location_mapping


def solve_tsp(distances, location_mapping, start_location=0):
    """
    Solve TSP using dynamic programming with bitmask.
    Modified for Part 2: Must return to starting location after visiting all locations.

    Args:
        distances: 2D list indexed by normalized location indices
        location_mapping: Dictionary mapping original location numbers to normalized indices
        start_location: Original location number to start from

    Returns:
        Minimum number of steps to visit all locations and return to start
    """
    N = len(distances)
    start_idx = location_mapping[start_location]

    # dp[mask][current] = minimum distance to reach current with visited set = mask
    dp = [[float('inf')] * N for _ in range(1 << N)]
    dp[1 << start_idx][start_idx] = 0

    # Iterate through all masks
    for mask in range(1 << N):
        for current in range(N):
            # Skip if current is not in mask or state is unreachable
            if not (mask & (1 << current)) or dp[mask][current] == float('inf'):
                continue

            # Try going to each unvisited location
            for next_loc in range(N):
                if not (mask & (1 << next_loc)):
                    new_mask = mask | (1 << next_loc)
                    dp[new_mask][next_loc] = min(
                        dp[new_mask][next_loc],
                        dp[mask][current] + distances[current][next_loc]
                    )

    # Part 2 modification: Add return distance to start location
    full_mask = (1 << N) - 1
    return min(dp[full_mask][i] + distances[i][start_idx] for i in range(N))


def main():
    """Main function to solve the air duct robot pathfinding problem (Part 2: Round Trip)."""
    # Read input from input.md
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Strip markdown formatting if present and clean lines
    grid = []
    for line in lines:
        line = line.rstrip('\n')
        # Skip empty lines or markdown code fences
        if line and not line.startswith('```'):
            grid.append(line)

    # Parse grid to find locations
    locations = parse_grid(grid)
    assert 0 in locations, "Starting location 0 not found!"

    print(f"Found {len(locations)} locations: {sorted(locations.keys())}")

    # Calculate pairwise distances
    distances, location_mapping = calculate_distances(grid, locations)

    # Verify all locations are reachable
    for i in range(len(distances)):
        for j in range(len(distances)):
            if distances[i][j] == float('inf'):
                print(f"Warning: Location {i} to {j} is unreachable!")

    # Optional: Print distance matrix for debugging
    print("\nDistance matrix:")
    sorted_locs = sorted(locations.keys())
    print("   ", " ".join(f"{loc:3d}" for loc in sorted_locs))
    for i, loc_i in enumerate(sorted_locs):
        row_str = " ".join(f"{distances[i][j]:3.0f}" if distances[i][j] != float('inf') else "inf"
                          for j in range(len(distances)))
        print(f"{loc_i:2d}: {row_str}")

    # Solve TSP starting from location 0 (round trip)
    min_steps = solve_tsp(distances, location_mapping, start_location=0)

    print(f"\nMinimum steps required (round trip): {min_steps}")
    return min_steps


if __name__ == "__main__":
    main()
