import re


def parse_instruction(line):
    """
    Parse a single instruction line into components.

    Args:
        line: String like "turn on 0,0 through 999,999"

    Returns:
        Tuple (command, x1, y1, x2, y2) or None if invalid
    """
    pattern = r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)'
    match = re.match(pattern, line.strip())
    if match:
        command = match.group(1)
        x1, y1, x2, y2 = map(int, [match.group(2), match.group(3),
                                    match.group(4), match.group(5)])
        return (command, x1, y1, x2, y2)
    return None


def initialize_grid():
    """
    Create a 1000x1000 grid with all lights at brightness 0.

    Returns:
        2D list grid[row][column] = grid[y][x]
    """
    return [[0] * 1000 for _ in range(1000)]


def process_instruction(grid, command, x1, y1, x2, y2):
    """
    Apply a single instruction to the grid.

    Args:
        grid: 2D list representing light grid
        command: "turn on", "turn off", or "toggle"
        x1, y1: Top-left corner (X=column, Y=row)
        x2, y2: Bottom-right corner (inclusive)

    Note: Input coordinates are (X,Y) where X=column, Y=row
          Grid access is grid[row][column] = grid[y][x]
    """
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if command == "turn on":
                grid[y][x] += 1
            elif command == "turn off":
                grid[y][x] = max(0, grid[y][x] - 1)
            elif command == "toggle":
                grid[y][x] += 2


def calculate_total_brightness(grid):
    """
    Calculate the sum of all brightness values in the grid.

    Args:
        grid: 2D list representing light grid

    Returns:
        Integer total brightness
    """
    total = 0
    for row in grid:
        total += sum(row)
    return total


def main():
    # 1. Read and parse input
    instructions = []
    with open('input.md', 'r') as f:
        for line in f:
            parsed = parse_instruction(line)
            if parsed:
                instructions.append(parsed)

    print(f"Parsed {len(instructions)} instructions")

    # 2. Initialize grid
    grid = initialize_grid()

    # 3. Process all instructions
    for command, x1, y1, x2, y2 in instructions:
        process_instruction(grid, command, x1, y1, x2, y2)

    # 4. Calculate and output result
    total_brightness = calculate_total_brightness(grid)

    # Sanity check: no negative brightness
    min_brightness = min(min(row) for row in grid)
    assert min_brightness >= 0, f"Found negative brightness: {min_brightness}"

    print(f"Total brightness: {total_brightness}")
    return total_brightness


if __name__ == "__main__":
    main()
