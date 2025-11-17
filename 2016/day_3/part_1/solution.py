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


def count_valid_triangles(filename='input.md'):
    """
    Count valid triangles from input file.

    Args:
        filename: Path to input file

    Returns:
        int: Number of valid triangles
    """
    count = 0
    lines = read_input(filename)

    for line in lines:
        sides = parse_line(line)
        if sides is None:
            continue  # Skip invalid lines

        a, b, c = sides
        if is_valid_triangle(a, b, c):
            count += 1

    return count


def main():
    """Main entry point."""
    result = count_valid_triangles('input.md')
    print(result)


if __name__ == '__main__':
    main()
