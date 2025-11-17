def calculate_ribbon_for_present(length, width, height):
    """
    Calculate ribbon needed for a single present.

    Args:
        length, width, height: dimensions of the present

    Returns:
        Total ribbon needed (wrapping + bow)
    """
    # Wrapping ribbon: smallest perimeter
    # Optimization: use 2 smallest dimensions
    dimensions = sorted([length, width, height])
    wrapping_ribbon = 2 * (dimensions[0] + dimensions[1])

    # Bow ribbon: volume
    bow_ribbon = length * width * height

    return wrapping_ribbon + bow_ribbon


def parse_line(line):
    """
    Parse a line to extract dimensions.

    Args:
        line: string in format "LxWxH"

    Returns:
        Tuple of (length, width, height)
    """
    parts = line.strip().split('x')
    return int(parts[0]), int(parts[1]), int(parts[2])


def calculate_total_ribbon(input_file):
    """
    Calculate total ribbon needed for all presents.

    Args:
        input_file: path to input file

    Returns:
        Total feet of ribbon needed
    """
    total_ribbon = 0

    with open(input_file, 'r') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                length, width, height = parse_line(line)
                ribbon = calculate_ribbon_for_present(length, width, height)
                total_ribbon += ribbon

    return total_ribbon


def run_tests():
    """Run basic tests to verify correctness."""
    # Test example 1: 2x3x4
    assert calculate_ribbon_for_present(2, 3, 4) == 34, "Example 1 failed"

    # Test example 2: 1x1x10
    assert calculate_ribbon_for_present(1, 1, 10) == 14, "Example 2 failed"

    # Test dimension order independence (validates sorting optimization)
    assert calculate_ribbon_for_present(2, 3, 4) == calculate_ribbon_for_present(3, 4, 2), "Order independence failed"
    assert calculate_ribbon_for_present(2, 3, 4) == calculate_ribbon_for_present(4, 2, 3), "Order independence failed"

    # Test cube (all dimensions equal)
    assert calculate_ribbon_for_present(5, 5, 5) == 145, "Cube test failed"

    # Test flat box
    assert calculate_ribbon_for_present(1, 10, 20) == 222, "Flat box failed"

    # Test minimum dimensions
    assert calculate_ribbon_for_present(1, 1, 1) == 5, "Minimum dimensions failed"

    # Test parsing
    assert parse_line("29x13x26") == (29, 13, 26), "Parsing failed"
    assert parse_line("1x2x3\n") == (1, 2, 3), "Parsing with newline failed"

    # Test first three lines of actual input
    result = 0
    result += calculate_ribbon_for_present(29, 13, 26)  # 9880
    result += calculate_ribbon_for_present(11, 11, 14)  # 1738
    result += calculate_ribbon_for_present(27, 2, 5)    # 284
    assert result == 11902, f"First 3 lines failed: expected 11902, got {result}"

    print("All tests passed!")


def main():
    """Main entry point."""
    import sys

    # Check if running tests
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
        return

    # Determine input file (default or command-line argument)
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    result = calculate_total_ribbon(input_file)
    print(result)


if __name__ == '__main__':
    main()
