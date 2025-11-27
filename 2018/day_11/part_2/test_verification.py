#!/usr/bin/env python3
"""Comprehensive verification tests for Part 2 solution."""

import time
from solution import (
    calculate_power_level,
    build_power_grid,
    build_summed_area_table,
    get_square_sum,
    find_max_power_square_any_size,
    format_output
)

def test_power_level_calculation():
    """Test 1: Verify power level calculations match examples."""
    print("Test 1: Power level calculation...")
    assert calculate_power_level(3, 5, 8) == 4, "Failed: (3,5) with serial 8"
    assert calculate_power_level(122, 79, 57) == -5, "Failed: (122,79) with serial 57"
    assert calculate_power_level(217, 196, 39) == 0, "Failed: (217,196) with serial 39"
    assert calculate_power_level(101, 153, 71) == 4, "Failed: (101,153) with serial 71"
    print("  ✓ All power level calculations correct")

def test_sat_construction():
    """Test 2: Verify summed-area table construction."""
    print("\nTest 2: SAT construction...")

    # Create a simple 3x3 grid for manual verification
    test_grid = [[0] * 4 for _ in range(4)]
    test_grid[1] = [0, 1, 2, 3]
    test_grid[2] = [0, 4, 5, 6]
    test_grid[3] = [0, 7, 8, 9]

    sat = build_summed_area_table(test_grid, 3)

    assert sat[1][1] == 1, f"Failed: SAT[1][1] should be 1, got {sat[1][1]}"
    assert sat[1][3] == 6, f"Failed: SAT[1][3] should be 6, got {sat[1][3]}"
    assert sat[2][2] == 12, f"Failed: SAT[2][2] should be 12, got {sat[2][2]}"
    assert sat[3][3] == 45, f"Failed: SAT[3][3] should be 45, got {sat[3][3]}"
    print("  ✓ SAT construction correct")

def test_square_sum_retrieval():
    """Test 3: Verify square sum calculations using SAT."""
    print("\nTest 3: Square sum retrieval...")

    # Using test grid from test 2
    test_grid = [[0] * 4 for _ in range(4)]
    test_grid[1] = [0, 1, 2, 3]
    test_grid[2] = [0, 4, 5, 6]
    test_grid[3] = [0, 7, 8, 9]
    sat = build_summed_area_table(test_grid, 3)

    # 1x1 squares
    assert get_square_sum(sat, 1, 1, 1) == 1, "Failed: 1x1 at (1,1)"
    assert get_square_sum(sat, 3, 3, 1) == 9, "Failed: 1x1 at (3,3)"

    # 2x2 squares
    assert get_square_sum(sat, 1, 1, 2) == 12, "Failed: 2x2 at (1,1)"
    assert get_square_sum(sat, 2, 2, 2) == 28, "Failed: 2x2 at (2,2)"

    # 3x3 square
    assert get_square_sum(sat, 1, 1, 3) == 45, "Failed: 3x3 at (1,1)"

    print("  ✓ Square sum retrieval correct")

def test_example_serial_18():
    """Test 4: Validate against serial number 18 example."""
    print("\nTest 4: Example - Serial 18...")
    start = time.time()

    grid = build_power_grid(18)
    sat = build_summed_area_table(grid)
    coord, power = find_max_power_square_any_size(sat)

    elapsed = time.time() - start

    result = format_output(coord)
    expected = "90,269,16"
    expected_power = 113

    print(f"  Result: {result}")
    print(f"  Power: {power}")
    print(f"  Time: {elapsed:.2f}s")

    assert result == expected, f"Failed: Expected {expected}, got {result}"
    assert power == expected_power, f"Failed: Expected power {expected_power}, got {power}"
    print(f"  ✓ Serial 18 correct: {result} (Power: {power})")

def test_example_serial_42():
    """Test 5: Validate against serial number 42 example."""
    print("\nTest 5: Example - Serial 42...")
    start = time.time()

    grid = build_power_grid(42)
    sat = build_summed_area_table(grid)
    coord, power = find_max_power_square_any_size(sat)

    elapsed = time.time() - start

    result = format_output(coord)
    expected = "232,251,12"
    expected_power = 119

    print(f"  Result: {result}")
    print(f"  Power: {power}")
    print(f"  Time: {elapsed:.2f}s")

    assert result == expected, f"Failed: Expected {expected}, got {result}"
    assert power == expected_power, f"Failed: Expected power {expected_power}, got {power}"
    print(f"  ✓ Serial 42 correct: {result} (Power: {power})")

def test_part1_cross_validation():
    """Test 6: Cross-validate with Part 1 answer (best 3x3 square)."""
    print("\nTest 6: Part 1 cross-validation...")

    serial = 2568
    grid = build_power_grid(serial)
    sat = build_summed_area_table(grid)

    # Find best 3x3 square
    max_power_3x3 = float('-inf')
    best_coord_3x3 = None

    for y in range(1, 299):
        for x in range(1, 299):
            power = get_square_sum(sat, x, y, 3)
            if power > max_power_3x3:
                max_power_3x3 = power
                best_coord_3x3 = (x, y)

    print(f"  Best 3x3 square: {best_coord_3x3}")
    print(f"  Power: {max_power_3x3}")

    # Part 1 answer was 21,68
    expected = (21, 68)
    assert best_coord_3x3 == expected, f"Failed: Expected {expected}, got {best_coord_3x3}"
    print(f"  ✓ Part 1 validation passed: Best 3x3 at {best_coord_3x3}")

def test_actual_input():
    """Test 7: Test with actual puzzle input."""
    print("\nTest 7: Actual input (serial 2568)...")
    start = time.time()

    serial = 2568
    grid = build_power_grid(serial)
    sat = build_summed_area_table(grid)
    coord, power = find_max_power_square_any_size(sat)

    elapsed = time.time() - start

    result = format_output(coord)
    x, y, size = coord

    print(f"  Result: {result}")
    print(f"  Power: {power}")
    print(f"  Time: {elapsed:.2f}s")

    # Verify format and constraints
    assert 1 <= x <= 300, f"X coordinate {x} out of range"
    assert 1 <= y <= 300, f"Y coordinate {y} out of range"
    assert 1 <= size <= 300, f"Size {size} out of range"
    assert x + size - 1 <= 300, f"Square extends beyond grid horizontally"
    assert y + size - 1 <= 300, f"Square extends beyond grid vertically"

    print(f"  ✓ Valid solution: {result} (Power: {power})")

    return result, power

def main():
    """Run all verification tests."""
    print("=" * 60)
    print("VERIFICATION TEST SUITE")
    print("=" * 60)

    try:
        # Unit tests
        test_power_level_calculation()
        test_sat_construction()
        test_square_sum_retrieval()

        # Example validation
        test_example_serial_18()
        test_example_serial_42()

        # Cross-validation
        test_part1_cross_validation()

        # Final test
        result, power = test_actual_input()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        print(f"\nFinal Answer: {result}")
        print(f"Total Power: {power}")

        return True

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
