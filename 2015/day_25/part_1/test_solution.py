from solution import parse_input, calculate_position, generate_code, solve
import time


def test_position_calculations():
    """Test position calculation formula."""
    print("Testing position calculations...")
    assert calculate_position(1, 1) == 1, "Failed: (1,1) should be position 1"
    assert calculate_position(2, 1) == 2, "Failed: (2,1) should be position 2"
    assert calculate_position(1, 2) == 3, "Failed: (1,2) should be position 3"
    assert calculate_position(4, 2) == 12, "Failed: (4,2) should be position 12"
    assert calculate_position(1, 5) == 15, "Failed: (1,5) should be position 15"
    assert calculate_position(1, 6) == 21, "Failed: (1,6) should be position 21"
    assert calculate_position(6, 1) == 16, "Failed: (6,1) should be position 16"
    # CRITICAL: Test actual input position
    assert calculate_position(2978, 3083) == 18361853, "Failed: (2978,3083) should be position 18361853"
    print("  All position calculation tests passed!")


def test_code_generation():
    """Test code generation for small positions."""
    print("\nTesting code generation...")
    assert generate_code(1) == 20151125, "Failed: position 1 should be 20151125"
    assert generate_code(2) == 31916031, "Failed: position 2 should be 31916031"
    assert generate_code(3) == 18749137, "Failed: position 3 should be 18749137"
    print("  All code generation tests passed!")


def test_grid_values():
    """Test code generation matches sample grid values."""
    print("\nTesting grid values against sample...")
    test_cases = [
        ((1, 1), 20151125),
        ((1, 2), 18749137),
        ((1, 3), 17289845),
        ((1, 4), 30943339),
        ((1, 5), 10071777),
        ((1, 6), 33511524),
        ((2, 1), 31916031),
        ((3, 1), 16080970),
        ((2, 2), 21629792),
        ((3, 3), 1601130),
        ((4, 2), 32451966),
        ((6, 6), 27995004),
    ]

    for (row, col), expected in test_cases:
        pos = calculate_position(row, col)
        code = generate_code(pos)
        assert code == expected, f"Failed for ({row},{col}): got {code}, expected {expected}"
        print(f"  ({row},{col}) -> position {pos} -> code {code} OK")

    print("  All grid validation tests passed!")


def test_input_parsing():
    """Test parsing of input format."""
    print("\nTesting input parsing...")
    input_text = "To continue, please consult the code grid in the manual.  Enter the code at row 2978, column 3083."
    row, col = parse_input(input_text)
    assert row == 2978, f"Expected row 2978, got {row}"
    assert col == 3083, f"Expected col 3083, got {col}"
    print(f"  Parsed row={row}, col={col} - OK")


def test_performance():
    """Test that solution completes in reasonable time."""
    print("\nTesting performance with actual input...")
    input_text = "Enter the code at row 2978, column 3083."
    start = time.time()
    result = solve(input_text)
    elapsed = time.time() - start
    print(f"  Completed in {elapsed:.2f} seconds")
    assert elapsed < 3.0, f"Too slow: {elapsed:.2f} seconds (threshold: 3.0s)"
    assert isinstance(result, int), f"Result should be integer, got {type(result)}"
    print(f"  Result: {result}")
    print("  Performance test passed!")
    return result


if __name__ == "__main__":
    print("Running tests...\n")
    print("="*50)
    test_position_calculations()
    test_code_generation()
    test_grid_values()
    test_input_parsing()
    result = test_performance()
    print("="*50)
    print("\nAll tests passed!")
    print(f"\nFinal answer for (2978, 3083): {result}")
