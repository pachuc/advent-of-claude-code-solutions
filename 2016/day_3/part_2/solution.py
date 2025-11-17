def read_input(filename='input.md'):
    """Read triangle specifications from input file."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def parse_line(line):
    """
    Parse a line containing three space-separated integers.

    Args:
        line: String with three integers

    Returns:
        tuple: (a, b, c) as integers, or None if invalid
    """
    parts = line.strip().split()
    if len(parts) != 3:
        return None
    try:
        a, b, c = int(parts[0]), int(parts[1]), int(parts[2])
        return (a, b, c)
    except ValueError:
        return None


def is_valid_triangle(a, b, c):
    """
    Check if three sides can form a valid triangle.

    Triangle inequality theorem: sum of any two sides must be
    greater than the third side.

    Args:
        a, b, c: Integer side lengths

    Returns:
        bool: True if valid triangle, False otherwise
    """
    return (a + b > c) and (a + c > b) and (b + c > a)


def count_valid_triangles_vertical(filename='input.md'):
    """
    Count valid triangles from input file, reading vertically by columns.

    The input is processed in groups of 3 consecutive rows.
    Each column within a group represents one triangle.

    Args:
        filename: Path to input file

    Returns:
        int: Number of valid triangles
    """
    count = 0
    lines = read_input(filename)

    # Process lines in groups of 3
    # range(0, len(lines) - 2, 3) ensures we only iterate when we have at least 3 complete lines
    for i in range(0, len(lines) - 2, 3):
        # Parse the 3 rows
        row1 = parse_line(lines[i])
        row2 = parse_line(lines[i + 1])
        row3 = parse_line(lines[i + 2])

        # Skip if any row is invalid
        if None in (row1, row2, row3):
            continue

        # Extract triangles from columns
        # Column 1: first value from each row
        triangle1 = (row1[0], row2[0], row3[0])
        # Column 2: second value from each row
        triangle2 = (row1[1], row2[1], row3[1])
        # Column 3: third value from each row
        triangle3 = (row1[2], row2[2], row3[2])

        # Validate each triangle
        for triangle in [triangle1, triangle2, triangle3]:
            if is_valid_triangle(*triangle):
                count += 1

    return count


def main():
    """Main entry point."""
    result = count_valid_triangles_vertical('input.md')
    print(result)


if __name__ == '__main__':
    main()
