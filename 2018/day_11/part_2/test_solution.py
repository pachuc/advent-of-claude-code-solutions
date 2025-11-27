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
    """Test 1: Power level calculation (reused from Part 1)"""
    print("Test 1: Power level calculation...")
    assert calculate_power_level(3, 5, 8) == 4, "Failed: (3,5) with serial 8"
    assert calculate_power_level(122, 79, 57) == -5, "Failed: (122,79) with serial 57"
    assert calculate_power_level(217, 196, 39) == 0, "Failed: (217,196) with serial 39"
    assert calculate_power_level(101, 153, 71) == 4, "Failed: (101,153) with serial 71"
    print("  ✓ All power level calculations correct")


def test_summed_area_table():
    """Test 2: SAT construction"""
    print("\nTest 2: Summed-area table construction...")
    # Create a simple 3x3 grid for manual verification
    test_grid = [
        [0, 0, 0, 0],  # padding row
        [0, 1, 2, 3],  # row 1
        [0, 4, 5, 6],  # row 2
        [0, 7, 8, 9]   # row 3
    ]

    sat = build_summed_area_table(test_grid, 3)

    # Verify SAT values (cumulative sums from (1,1))
    assert sat[1][1] == 1, f"Failed: sat[1][1] = {sat[1][1]}, expected 1"
    assert sat[1][3] == 6, f"Failed: sat[1][3] = {sat[1][3]}, expected 6"  # 1+2+3
    assert sat[2][2] == 12, f"Failed: sat[2][2] = {sat[2][2]}, expected 12"  # 1+2+4+5
    assert sat[3][3] == 45, f"Failed: sat[3][3] = {sat[3][3]}, expected 45"  # sum of 1-9
    print("  ✓ SAT construction correct")


def test_square_sum_retrieval():
    """Test 3: Square sum retrieval using SAT"""
    print("\nTest 3: Square sum retrieval...")
    # Using the same 3x3 test grid
    test_grid = [
        [0, 0, 0, 0],
        [0, 1, 2, 3],
        [0, 4, 5, 6],
        [0, 7, 8, 9]
    ]
    sat = build_summed_area_table(test_grid, 3)

    # 1x1 squares
    assert get_square_sum(sat, 1, 1, 1) == 1, "Failed: 1x1 at (1,1)"
    assert get_square_sum(sat, 3, 3, 1) == 9, "Failed: 1x1 at (3,3)"

    # 2x2 squares
    assert get_square_sum(sat, 1, 1, 2) == 12, "Failed: 2x2 at (1,1)"  # 1+2+4+5
    assert get_square_sum(sat, 2, 2, 2) == 28, "Failed: 2x2 at (2,2)"  # 5+6+8+9

    # 3x3 square
    assert get_square_sum(sat, 1, 1, 3) == 45, "Failed: 3x3 at (1,1)"

    # Test with uniform grid (catches overlap correction errors)
    uniform_grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1],
    ]
    uniform_sat = build_summed_area_table(uniform_grid, 4)

    # For uniform grid of 1s, a KxK square should sum to K*K
    assert get_square_sum(uniform_sat, 1, 1, 4) == 16, "Failed: 4x4 uniform grid"
    assert get_square_sum(uniform_sat, 2, 2, 3) == 9, "Failed: 3x3 uniform grid"
    assert get_square_sum(uniform_sat, 2, 2, 2) == 4, "Failed: 2x2 uniform grid"
    print("  ✓ Square sum retrieval correct")


def test_boundary_conditions():
    """Test 4: Boundary conditions"""
    print("\nTest 4: Boundary conditions...")
    grid = build_power_grid(2568)
    sat = build_summed_area_table(grid)

    # Size 1 at corner positions
    power_1_1 = get_square_sum(sat, 1, 1, 1)
    power_300_300 = get_square_sum(sat, 300, 300, 1)
    assert power_1_1 == grid[1][1], "Failed: 1x1 at (1,1)"
    assert power_300_300 == grid[300][300], "Failed: 1x1 at (300,300)"

    # Size 300 (entire grid) - only valid position is (1,1)
    entire_grid_sum = get_square_sum(sat, 1, 1, 300)
    assert entire_grid_sum == sat[300][300], "Failed: 300x300 grid sum"

    # Large square near edge
    power_bottom_right = get_square_sum(sat, 299, 299, 2)
    assert isinstance(power_bottom_right, int), "Failed: 2x2 at edge returned non-int"
    print("  ✓ Boundary conditions handled correctly")


def test_provided_examples():
    """Test 5: Validate against provided examples"""
    print("\nTest 5: Testing with provided examples...")

    # Test Case 1: Serial Number 18
    print("  Testing serial 18...")
    start = time.time()
    grid = build_power_grid(18)
    sat = build_summed_area_table(grid)
    coord, power = find_max_power_square_any_size(sat)
    elapsed = time.time() - start

    result = format_output(coord)
    print(f"    Result: {result}, Power: {power}, Time: {elapsed:.2f}s")
    assert coord == (90, 269, 16), f"Failed: Expected (90,269,16), got {coord}"
    assert power == 113, f"Failed: Expected power 113, got {power}"
    assert result == "90,269,16", f"Failed: Format error"
    print("  ✓ Serial 18 correct")

    # Test Case 2: Serial Number 42
    print("  Testing serial 42...")
    start = time.time()
    grid = build_power_grid(42)
    sat = build_summed_area_table(grid)
    coord, power = find_max_power_square_any_size(sat)
    elapsed = time.time() - start

    result = format_output(coord)
    print(f"    Result: {result}, Power: {power}, Time: {elapsed:.2f}s")
    assert coord == (232, 251, 12), f"Failed: Expected (232,251,12), got {coord}"
    assert power == 119, f"Failed: Expected power 119, got {power}"
    assert result == "232,251,12", f"Failed: Format error"
    print("  ✓ Serial 42 correct")


def test_part1_cross_validation():
    """Test 6: Cross-validation with Part 1 answer"""
    print("\nTest 6: Cross-validation with Part 1...")
    serial = 2568
    grid = build_power_grid(serial)
    sat = build_summed_area_table(grid)

    # Find best 3x3 square specifically
    max_power_3x3 = float('-inf')
    best_coord_3x3 = None

    for y in range(1, 299):  # 1 to 298
        for x in range(1, 299):
            power = get_square_sum(sat, x, y, 3)
            if power > max_power_3x3:
                max_power_3x3 = power
                best_coord_3x3 = (x, y)

    print(f"  Best 3x3 square: {best_coord_3x3}, Power: {max_power_3x3}")
    assert best_coord_3x3 == (21, 68), f"Failed: Expected (21,68), got {best_coord_3x3}"
    print("  ✓ Matches Part 1 answer")


def test_actual_input():
    """Test 7: Run with actual input"""
    print("\nTest 7: Running with actual input (serial 2568)...")
    start = time.time()

    grid = build_power_grid(2568)
    sat = build_summed_area_table(grid)
    coord, power = find_max_power_square_any_size(sat)

    elapsed = time.time() - start
    result = format_output(coord)

    # Verify format
    parts = result.split(',')
    assert len(parts) == 3, f"Failed: Invalid format {result}"

    x, y, size = map(int, parts)
    assert 1 <= x <= 300, f"Failed: x={x} out of range"
    assert 1 <= y <= 300, f"Failed: y={y} out of range"
    assert 1 <= size <= 300, f"Failed: size={size} out of range"
    assert x + size - 1 <= 300, f"Failed: Square doesn't fit horizontally"
    assert y + size - 1 <= 300, f"Failed: Square doesn't fit vertically"

    print(f"  Solution: {result}")
    print(f"  Total power: {power}")
    print(f"  Runtime: {elapsed:.2f}s")

    if elapsed < 5:
        print("  ✓ Excellent performance")
    elif elapsed < 10:
        print("  ✓ Good performance")
    elif elapsed < 15:
        print("  ✓ Acceptable performance")
    else:
        print("  ⚠ Performance could be better")

    return result


def run_all_tests():
    """Run all tests in sequence"""
    print("=" * 60)
    print("RUNNING ALL TESTS")
    print("=" * 60)

    # Phase 1: Unit tests
    print("\n[PHASE 1: UNIT TESTS]")
    test_power_level_calculation()
    test_summed_area_table()
    test_square_sum_retrieval()
    test_boundary_conditions()

    # Phase 2: Integration tests
    print("\n[PHASE 2: INTEGRATION TESTS]")
    test_provided_examples()
    test_part1_cross_validation()

    # Phase 3: Final test
    print("\n[PHASE 3: FINAL TEST]")
    result = test_actual_input()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print(f"\nFinal Answer: {result}")

    return result


if __name__ == "__main__":
    run_all_tests()
