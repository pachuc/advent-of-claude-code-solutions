def parse_instruction(line):
    """Parse an instruction line to extract command and coordinates.

    Args:
        line: Instruction string like "turn on 0,0 through 999,999"

    Returns:
        tuple: (command, col1, row1, col2, row2)
               command is 'on', 'off', or 'toggle'
               coordinates are (column, row) format
    """
    line = line.strip()

    # Determine command type
    if line.startswith('turn on'):
        command = 'on'
        coords_part = line[8:]  # Skip "turn on "
    elif line.startswith('turn off'):
        command = 'off'
        coords_part = line[9:]  # Skip "turn off "
    elif line.startswith('toggle'):
        command = 'toggle'
        coords_part = line[7:]  # Skip "toggle "
    else:
        raise ValueError(f"Unknown command in line: {line}")

    # Parse coordinates: "col1,row1 through col2,row2"
    start, end = coords_part.split(' through ')
    col1, row1 = map(int, start.split(','))
    col2, row2 = map(int, end.split(','))

    return command, col1, row1, col2, row2


def apply_instruction(grid, command, col1, row1, col2, row2):
    """Apply instruction to grid region.

    Args:
        grid: 1D list representing 1000x1000 grid
        command: 'on', 'off', or 'toggle'
        col1, row1: Top-left corner (inclusive)
        col2, row2: Bottom-right corner (inclusive)
    """
    for row in range(row1, row2 + 1):  # Inclusive range
        for col in range(col1, col2 + 1):
            idx = row * 1000 + col  # Row-major indexing
            if command == 'on':
                grid[idx] = True
            elif command == 'off':
                grid[idx] = False
            elif command == 'toggle':
                grid[idx] = not grid[idx]


def process_instructions(filename):
    """Process all instructions from file and return count of lights ON.

    Args:
        filename: Path to input file

    Returns:
        int: Number of lights that are ON after processing all instructions
    """
    grid = [False] * 1000000

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            command, col1, row1, col2, row2 = parse_instruction(line)
            apply_instruction(grid, command, col1, row1, col2, row2)

    return sum(grid)  # Count True values


def main():
    result = process_instructions('input.md')
    print(result)


if __name__ == '__main__':
    main()
