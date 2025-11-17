def parse_input(filename='input.md'):
    """
    Read the first row from input file.

    Args:
        filename: path to input file (default: 'input.md')

    Returns:
        str: first row of tiles (stripped of whitespace)
    """
    with open(filename, 'r') as f:
        return f.readline().strip()


def is_trap(left, center, right):
    """
    Determine if a tile should be a trap based on the three tiles above it.

    The four trap conditions simplify to: a tile is a trap if left != right.

    Args:
        left: character for left tile ('^' or '.')
        center: character for center tile ('^' or '.')
        right: character for right tile ('^' or '.')

    Returns:
        bool: True if new tile is a trap, False if safe
    """
    return left != right


def generate_next_row(current_row):
    """
    Generate the next row based on current row using trap rules.

    Args:
        current_row: string representing current row

    Returns:
        str: next row as string
    """
    next_row = []
    row_len = len(current_row)

    for i in range(row_len):
        # Get left tile (out of bounds = safe)
        left = current_row[i-1] if i > 0 else '.'
        # Get center tile
        center = current_row[i]
        # Get right tile (out of bounds = safe)
        right = current_row[i+1] if i < row_len - 1 else '.'

        # Determine if this position is a trap
        if is_trap(left, center, right):
            next_row.append('^')
        else:
            next_row.append('.')

    return ''.join(next_row)


def count_safe_tiles(first_row, total_rows):
    """
    Count total safe tiles across all rows.

    Args:
        first_row: initial row configuration
        total_rows: number of rows to generate (including first)

    Returns:
        int: total count of safe tiles
    """
    safe_count = 0
    current_row = first_row

    for row_num in range(total_rows):
        # Count safe tiles (.) in current row
        safe_count += current_row.count('.')

        # Generate next row if not last row
        if row_num < total_rows - 1:
            current_row = generate_next_row(current_row)

    # Verify we processed the correct number of rows
    assert row_num == total_rows - 1, f"Expected to process {total_rows} rows, but stopped at row {row_num + 1}"

    return safe_count


def main():
    """
    Main entry point for the solution.

    Reads from 'input.md' and generates exactly 400,000 rows.
    """
    first_row = parse_input('input.md')

    # Input validation
    assert len(first_row) == 100, f"Input should be 100 characters, got {len(first_row)}"
    assert all(c in '.^' for c in first_row), "Input contains invalid characters"

    # Changed from 40 to 400,000 rows for Part 2
    result = count_safe_tiles(first_row, 400000)
    print(result)


if __name__ == '__main__':
    main()
