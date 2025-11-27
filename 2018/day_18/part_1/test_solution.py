#!/usr/bin/env python3
"""Test suite for lumber collection area simulation."""

from solution import (
    parse_input,
    count_neighbors,
    get_next_state,
    simulate_step,
    simulate,
    calculate_resource_value
)


def test_parse_input():
    """Test 1: Verify grid parsing."""
    print("Test 1: Parsing Input...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    grid = parse_input(input_text)

    # Check dimensions
    assert len(grid) == 50, f"Expected 50 rows, got {len(grid)}"
    assert len(grid[0]) == 50, f"Expected 50 cols, got {len(grid[0])}"

    # Spot check known positions (from first line: ||#.#..|||......#........#.|.......#....#||...##|.)
    assert grid[0][0] == '|', f"Expected '|' at (0,0), got {grid[0][0]}"
    assert grid[0][1] == '|', f"Expected '|' at (0,1), got {grid[0][1]}"
    assert grid[0][2] == '#', f"Expected '#' at (0,2), got {grid[0][2]}"

    # Verify only valid characters
    valid_chars = {'.', '|', '#'}
    for row in grid:
        for cell in row:
            assert cell in valid_chars, f"Invalid character found: {cell}"

    print("  ✓ Grid dimensions: 50x50")
    print("  ✓ Spot checks passed")
    print("  ✓ All characters valid")
    print()


def test_neighbor_counting_interior():
    """Test 2: Verify 8-neighbor counting for interior cell."""
    print("Test 2: Neighbor Counting - Interior Cell...")

    grid = [
        ['.', '|', '#'],
        ['|', '.', '|'],
        ['#', '|', '.']
    ]

    # At (1,1), neighbors are: (0,0)='.', (0,1)='|', (0,2)='#',
    #                           (1,0)='|', (1,2)='|',
    #                           (2,0)='#', (2,1)='|', (2,2)='.'
    # Trees: 4, Lumberyards: 2, Open: 2
    trees = count_neighbors(grid, 1, 1, '|')
    lumberyards = count_neighbors(grid, 1, 1, '#')
    open_ground = count_neighbors(grid, 1, 1, '.')

    assert trees == 4, f"Expected 4 trees, got {trees}"
    assert lumberyards == 2, f"Expected 2 lumberyards, got {lumberyards}"
    assert open_ground == 2, f"Expected 2 open ground, got {open_ground}"

    print("  ✓ Trees count: 4")
    print("  ✓ Lumberyards count: 2")
    print("  ✓ Open ground count: 2")
    print()


def test_neighbor_counting_corner():
    """Test 3: Verify bounds checking for corner cell."""
    print("Test 3: Neighbor Counting - Corner Cell...")

    grid = [
        ['.', '|', '#'],
        ['|', '#', '|'],
        ['#', '|', '.']
    ]

    # Top-left corner (0,0) has only 3 neighbors: (0,1), (1,0), (1,1)
    trees = count_neighbors(grid, 0, 0, '|')
    lumberyards = count_neighbors(grid, 0, 0, '#')

    assert trees == 2, f"Expected 2 trees, got {trees}"
    assert lumberyards == 1, f"Expected 1 lumberyard, got {lumberyards}"

    print("  ✓ Corner cell trees: 2")
    print("  ✓ Corner cell lumberyards: 1")
    print("  ✓ No out-of-bounds access")
    print()


def test_transformation_open_ground():
    """Test 5: Test open ground → trees transformation."""
    print("Test 5: Transformation - Open Ground...")

    # Case A: Should become trees (3 adjacent trees)
    grid_a = [
        ['|', '|', '|'],
        ['.', '.', '.'],
        ['.', '.', '.']
    ]
    result_a = get_next_state(grid_a, 1, 1)
    assert result_a == '|', f"Expected '|', got {result_a}"

    # Case B: Should stay open (2 adjacent trees)
    grid_b = [
        ['|', '|', '.'],
        ['.', '.', '.'],
        ['.', '.', '.']
    ]
    result_b = get_next_state(grid_b, 1, 1)
    assert result_b == '.', f"Expected '.', got {result_b}"

    print("  ✓ Becomes trees with 3+ tree neighbors")
    print("  ✓ Stays open with <3 tree neighbors")
    print()


def test_transformation_trees():
    """Test 6: Test trees → lumberyard transformation."""
    print("Test 6: Transformation - Trees...")

    # Case A: Should become lumberyard (3 adjacent lumberyards)
    grid_a = [
        ['#', '#', '#'],
        ['|', '|', '|'],
        ['.', '.', '.']
    ]
    result_a = get_next_state(grid_a, 1, 1)
    assert result_a == '#', f"Expected '#', got {result_a}"

    # Case B: Should stay trees (2 adjacent lumberyards)
    grid_b = [
        ['#', '#', '.'],
        ['|', '|', '|'],
        ['.', '.', '.']
    ]
    result_b = get_next_state(grid_b, 1, 1)
    assert result_b == '|', f"Expected '|', got {result_b}"

    print("  ✓ Becomes lumberyard with 3+ lumberyard neighbors")
    print("  ✓ Stays trees with <3 lumberyard neighbors")
    print()


def test_transformation_lumberyard():
    """Test 7: Test lumberyard persistence/conversion."""
    print("Test 7: Transformation - Lumberyard...")

    # Case A: Should stay lumberyard (has both 1+ tree and 1+ lumberyard)
    grid_a = [
        ['#', '|', '.'],
        ['#', '#', '.'],
        ['.', '.', '.']
    ]
    result_a = get_next_state(grid_a, 1, 1)
    assert result_a == '#', f"Expected '#' (stay), got {result_a}"

    # Case B: Should become open (has lumberyard but no trees)
    grid_b = [
        ['#', '.', '.'],
        ['#', '#', '.'],
        ['.', '.', '.']
    ]
    result_b = get_next_state(grid_b, 1, 1)
    assert result_b == '.', f"Expected '.' (no trees), got {result_b}"

    # Case C: Should become open (has trees but no lumberyard)
    grid_c = [
        ['|', '|', '.'],
        ['|', '#', '.'],
        ['.', '.', '.']
    ]
    result_c = get_next_state(grid_c, 1, 1)
    assert result_c == '.', f"Expected '.' (no lumberyard), got {result_c}"

    # Case D: Should become open (isolated lumberyard)
    grid_d = [
        ['.', '.', '.'],
        ['.', '#', '.'],
        ['.', '.', '.']
    ]
    result_d = get_next_state(grid_d, 1, 1)
    assert result_d == '.', f"Expected '.' (isolated), got {result_d}"

    print("  ✓ Stays lumberyard with both trees and lumberyards")
    print("  ✓ Becomes open without trees")
    print("  ✓ Becomes open without lumberyards")
    print("  ✓ Becomes open when isolated")
    print()


def test_simultaneous_update():
    """Test 8: Verify simultaneous updates."""
    print("Test 8: Simultaneous Update Verification...")

    initial = [
        ['.', '.', '.'],
        ['|', '|', '|'],
        ['.', '.', '.']
    ]

    expected = [
        ['.', '|', '.'],
        ['|', '|', '|'],
        ['.', '|', '.']
    ]

    result = simulate_step(initial)

    # Verify result matches expected
    for row in range(3):
        for col in range(3):
            assert result[row][col] == expected[row][col], \
                f"Mismatch at ({row},{col}): expected {expected[row][col]}, got {result[row][col]}"

    print("  ✓ Simultaneous updates work correctly")
    print("  ✓ Grid matches expected state after one step")
    print()


def test_resource_calculation():
    """Test 10: Verify resource value calculation."""
    print("Test 10: Resource Value Calculation...")

    grid = [
        ['|', '|', '#'],
        ['#', '.', '|'],
        ['|', '#', '#']
    ]

    # Manual count: 4 trees, 4 lumberyards
    result = calculate_resource_value(grid)
    expected = 4 * 4  # 16

    assert result == expected, f"Expected {expected}, got {result}"

    print("  ✓ Resource value calculated correctly: 16")
    print()


def test_actual_input():
    """Test 11: Verify solution with actual input."""
    print("Test 11: Actual Input - Full Simulation...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    grid = parse_input(input_text)

    # Verify dimensions
    assert len(grid) == 50, "Grid should be 50x50"
    assert len(grid[0]) == 50, "Grid should be 50x50"

    # Run simulation
    final_grid = simulate(grid, minutes=10)

    # Calculate result
    result = calculate_resource_value(final_grid)

    # Count trees and lumberyards
    trees = sum(row.count('|') for row in final_grid)
    lumberyards = sum(row.count('#') for row in final_grid)

    print(f"  ✓ Grid dimensions: 50x50")
    print(f"  ✓ Simulation completed 10 iterations")
    print(f"  ✓ Final state: {trees} trees, {lumberyards} lumberyards")
    print(f"  ✓ Resource value: {result}")

    # Sanity checks
    assert trees > 0, "Should have some trees"
    assert lumberyards > 0, "Should have some lumberyards"
    assert result > 0, "Resource value should be positive"

    print()


def run_all_tests():
    """Run all test cases."""
    print("=" * 60)
    print("LUMBER COLLECTION AREA SIMULATION - TEST SUITE")
    print("=" * 60)
    print()

    tests = [
        test_parse_input,
        test_neighbor_counting_interior,
        test_neighbor_counting_corner,
        test_transformation_open_ground,
        test_transformation_trees,
        test_transformation_lumberyard,
        test_simultaneous_update,
        test_resource_calculation,
        test_actual_input
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            print()
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            print()
            failed += 1

    print("=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
