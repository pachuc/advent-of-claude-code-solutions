def read_input(filename: str = 'input.md') -> int:
    """Read and parse the grid serial number from input file."""
    try:
        with open(filename, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading input: {e}")
        raise


def calculate_power_level(x: int, y: int, serial_number: int) -> int:
    """Calculate power level for a fuel cell at position (x, y).

    Algorithm:
    1. Calculate rack_id = x + 10
    2. Start with power_level = rack_id * y
    3. Add the grid serial number to power_level
    4. Multiply power_level by rack_id
    5. Extract only the hundreds digit of the power_level
    6. Subtract 5 from the result
    """
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    # Extract hundreds digit: (power_level // 100) % 10
    hundreds_digit = (power_level // 100) % 10
    return hundreds_digit - 5


def build_power_grid(serial_number: int, grid_size: int = 300) -> list:
    """Build the complete power grid.

    Returns a 2D list where grid[y][x] represents the power level
    at coordinates (x, y) in the problem's coordinate system.
    Grid uses 1-based indexing with row/column 0 as padding.
    """
    grid = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]
    for y in range(1, grid_size + 1):
        for x in range(1, grid_size + 1):
            grid[y][x] = calculate_power_level(x, y, serial_number)
    return grid


def build_summed_area_table(grid: list, grid_size: int = 300) -> list:
    """Build summed-area table for O(1) rectangle sum queries.

    SAT[y][x] = sum of all grid values from (1,1) to (x,y) inclusive.
    Uses 1-based indexing with row/column 0 as 0-padding for boundary handling.
    """
    sat = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]

    for y in range(1, grid_size + 1):
        for x in range(1, grid_size + 1):
            sat[y][x] = (grid[y][x] +      # Current cell value
                        sat[y-1][x] +      # Sum above
                        sat[y][x-1] -      # Sum to left
                        sat[y-1][x-1])     # Subtract overlap
    return sat


def get_square_sum(sat: list, x: int, y: int, size: int) -> int:
    """Calculate sum of a square using summed-area table in O(1) time.

    Args:
        sat: Summed-area table
        x: X coordinate of top-left corner (1-based)
        y: Y coordinate of top-left corner (1-based)
        size: Size of the square

    Returns:
        Sum of all values in the square
    """
    # Calculate coordinates of bottom-right corner
    x2 = x + size - 1
    y2 = y + size - 1

    # Use SAT formula with boundary-safe indices
    return (sat[y2][x2] -
            sat[y-1][x2] -
            sat[y2][x-1] +
            sat[y-1][x-1])


def find_max_power_square_any_size(sat: list, grid_size: int = 300) -> tuple:
    """Find the square of any size with maximum total power.

    Returns: ((x, y, size), max_power) where (x,y) is top-left coordinate
    """
    max_power = float('-inf')
    best_x, best_y, best_size = 0, 0, 0

    # Iterate through all possible square sizes
    for size in range(1, grid_size + 1):
        # For this size, iterate through all valid positions
        for y in range(1, grid_size - size + 2):
            for x in range(1, grid_size - size + 2):
                power = get_square_sum(sat, x, y, size)

                if power > max_power:
                    max_power = power
                    best_x, best_y, best_size = x, y, size

    return (best_x, best_y, best_size), max_power


def format_output(coord: tuple) -> str:
    """Format coordinate as X,Y,size string."""
    return f"{coord[0]},{coord[1]},{coord[2]}"


def main():
    # Step 1: Read input
    serial_number = read_input('input.md')

    # Step 2: Build power grid
    grid = build_power_grid(serial_number)

    # Step 3: Build summed-area table
    sat = build_summed_area_table(grid)

    # Step 4: Find maximum power square of any size
    max_coord, max_power = find_max_power_square_any_size(sat)

    # Step 5: Format and output result
    result = format_output(max_coord)
    print(result)
    return result


if __name__ == "__main__":
    main()
