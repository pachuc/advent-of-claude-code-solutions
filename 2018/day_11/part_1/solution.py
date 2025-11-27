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
    """
    grid = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]
    for y in range(1, grid_size + 1):
        for x in range(1, grid_size + 1):
            grid[y][x] = calculate_power_level(x, y, serial_number)
    return grid


def calculate_square_power(grid: list, top_left_x: int, top_left_y: int, size: int = 3) -> int:
    """Calculate total power of a square region."""
    total = 0
    for dy in range(size):
        for dx in range(size):
            total += grid[top_left_y + dy][top_left_x + dx]
    return total


def find_max_power_square(grid: list, grid_size: int = 300, square_size: int = 3) -> tuple:
    """Find the 3x3 square with maximum total power.

    Returns: (coordinate, max_power) where coordinate is (x, y)
    """
    max_power = float('-inf')
    max_coord = (0, 0)

    for y in range(1, grid_size - square_size + 2):
        for x in range(1, grid_size - square_size + 2):
            power = calculate_square_power(grid, x, y, square_size)
            if power > max_power:
                max_power = power
                max_coord = (x, y)

    return max_coord, max_power


def format_output(coord: tuple) -> str:
    """Format coordinate as X,Y string."""
    return f"{coord[0]},{coord[1]}"


def main():
    # Step 1: Read input
    serial_number = read_input('input.md')

    # Step 2-3: Build power grid
    grid = build_power_grid(serial_number)

    # Step 4-5: Find maximum power square
    max_coord, max_power = find_max_power_square(grid)

    # Step 6: Output result
    result = format_output(max_coord)
    print(result)
    return result


if __name__ == "__main__":
    main()
