def parse_input(input_text):
    """Parse the input text into a 2D grid."""
    lines = input_text.strip().split('\n')
    grid = []
    for line in lines:
        grid.append(list(line.strip()))
    return grid


def count_neighbors(grid, row, col, target_type):
    """Count how many of the 8 adjacent cells match the target type."""
    # Define 8 direction offsets
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    count = 0
    rows = len(grid)
    cols = len(grid[0])

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        # Bounds checking
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == target_type:
                count += 1

    return count


def get_next_state(grid, row, col):
    """Determine what a cell becomes based on current state and neighbors."""
    current = grid[row][col]

    if current == '.':  # Open ground
        trees = count_neighbors(grid, row, col, '|')
        return '|' if trees >= 3 else '.'

    elif current == '|':  # Trees
        lumberyards = count_neighbors(grid, row, col, '#')
        return '#' if lumberyards >= 3 else '|'

    elif current == '#':  # Lumberyard
        trees = count_neighbors(grid, row, col, '|')
        lumberyards = count_neighbors(grid, row, col, '#')
        return '#' if (trees >= 1 and lumberyards >= 1) else '.'

    return current


def simulate_step(grid):
    """Perform one minute of simulation with simultaneous updates."""
    rows = len(grid)
    cols = len(grid[0])

    # Create new grid for next state
    new_grid = []
    for row in range(rows):
        new_row = []
        for col in range(cols):
            new_row.append(get_next_state(grid, row, col))
        new_grid.append(new_row)

    return new_grid


def simulate(grid, minutes=10):
    """Simulate the grid for a specified number of minutes."""
    current_grid = grid
    for _ in range(minutes):
        current_grid = simulate_step(current_grid)
    return current_grid


def calculate_resource_value(grid):
    """Count trees and lumberyards, return their product."""
    trees = 0
    lumberyards = 0

    for row in grid:
        for cell in row:
            if cell == '|':
                trees += 1
            elif cell == '#':
                lumberyards += 1

    return trees * lumberyards


def main():
    # Read input
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse grid
    grid = parse_input(input_text)

    # Simulate 10 minutes
    final_grid = simulate(grid, minutes=10)

    # Calculate and print result
    result = calculate_resource_value(final_grid)
    print(result)


if __name__ == '__main__':
    main()
