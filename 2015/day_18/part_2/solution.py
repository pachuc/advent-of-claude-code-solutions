def parse_input(filename):
    """Read grid from file and convert to 2D boolean array"""
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                row = [char == '#' for char in line]
                grid.append(row)
    return grid


def count_neighbors(grid, row, col):
    """Count ON neighbors for cell at (row, col)"""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # 8 directions: up-left, up, up-right, left, right, down-left, down, down-right
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    count = 0
    for dr, dc in directions:
        neighbor_row = row + dr
        neighbor_col = col + dc

        # Check if neighbor is within bounds
        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
            if grid[neighbor_row][neighbor_col]:
                count += 1

    return count


def force_corners_on(grid):
    """Set all four corner lights to ON (modifies grid in-place)"""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if rows > 0 and cols > 0:
        grid[0][0] = True  # Top-left
        grid[0][cols - 1] = True  # Top-right
        grid[rows - 1][0] = True  # Bottom-left
        grid[rows - 1][cols - 1] = True  # Bottom-right


def simulate_step(grid):
    """Execute one step of Conway's Game of Life with corner constraint
    Returns a NEW grid; does not modify input grid"""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Create new grid for next state
    new_grid = [[False] * cols for _ in range(rows)]

    # Apply Conway's rules to all cells
    for row in range(rows):
        for col in range(cols):
            neighbors = count_neighbors(grid, row, col)
            current_state = grid[row][col]

            if current_state:  # Cell is ON
                # Stays ON if it has 2 or 3 neighbors
                new_grid[row][col] = neighbors == 2 or neighbors == 3
            else:  # Cell is OFF
                # Turns ON if it has exactly 3 neighbors
                new_grid[row][col] = neighbors == 3

    # Force corners to ON after applying rules
    force_corners_on(new_grid)

    return new_grid


def count_on_lights(grid):
    """Count total ON lights in grid"""
    return sum(sum(row) for row in grid)


def main():
    # Parse input
    grid = parse_input('input.md')

    # Verify dimensions
    print(f"Grid dimensions: {len(grid)}x{len(grid[0])}")

    # Initialize corners
    force_corners_on(grid)

    # Count initial lights
    initial_count = count_on_lights(grid)
    print(f"Initial lights ON: {initial_count}")

    # Run 100 iterations
    for step in range(100):
        grid = simulate_step(grid)

    # Count and output result
    result = count_on_lights(grid)
    print(f"Lights ON after 100 steps: {result}")
    return result


if __name__ == "__main__":
    main()
