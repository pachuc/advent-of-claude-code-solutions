#!/usr/bin/env python3
"""Verification script to test the solution logic."""

from solution import parse_input, count_neighbors, get_next_state, simulate_step, calculate_resource_value

def test_neighbor_counting():
    """Test that neighbor counting works correctly."""
    grid = [
        ['.', '|', '#'],
        ['|', '.', '|'],
        ['#', '|', '.']
    ]

    # Interior cell (1, 1) - should have 8 neighbors
    trees = count_neighbors(grid, 1, 1, '|')
    lumberyards = count_neighbors(grid, 1, 1, '#')
    open_ground = count_neighbors(grid, 1, 1, '.')

    print(f"Test 1 - Interior cell neighbor counting:")
    print(f"  Trees: {trees} (expected: 4)")
    print(f"  Lumberyards: {lumberyards} (expected: 2)")
    print(f"  Open ground: {open_ground} (expected: 2)")

    assert trees == 4, f"Expected 4 trees, got {trees}"
    assert lumberyards == 2, f"Expected 2 lumberyards, got {lumberyards}"
    assert open_ground == 2, f"Expected 2 open ground, got {open_ground}"
    print("  PASS\n")

def test_corner_bounds():
    """Test that corner cells only count 3 neighbors."""
    grid = [
        ['.', '|', '#'],
        ['|', '#', '|'],
        ['#', '|', '.']
    ]

    # Top-left corner (0, 0) - should only have 3 neighbors
    trees = count_neighbors(grid, 0, 0, '|')
    lumberyards = count_neighbors(grid, 0, 0, '#')

    print(f"Test 2 - Corner cell bounds checking:")
    print(f"  Trees from (0,0): {trees} (expected: 2)")
    print(f"  Lumberyards from (0,0): {lumberyards} (expected: 1)")

    assert trees == 2, f"Expected 2 trees, got {trees}"
    assert lumberyards == 1, f"Expected 1 lumberyard, got {lumberyards}"
    print("  PASS\n")

def test_open_ground_rule():
    """Test open ground transformation."""
    # Should become trees (3 tree neighbors)
    grid = [
        ['|', '|', '|'],
        ['.', '.', '.'],
        ['.', '.', '.']
    ]

    next_state = get_next_state(grid, 1, 1)
    print(f"Test 3 - Open ground with 3 trees:")
    print(f"  Next state: {next_state} (expected: |)")
    assert next_state == '|', f"Expected '|', got '{next_state}'"
    print("  PASS\n")

def test_tree_rule():
    """Test tree transformation."""
    # Should become lumberyard (3 lumberyard neighbors)
    grid = [
        ['#', '#', '#'],
        ['|', '|', '|'],
        ['.', '.', '.']
    ]

    next_state = get_next_state(grid, 1, 1)
    print(f"Test 4 - Tree with 3 lumberyards:")
    print(f"  Next state: {next_state} (expected: #)")
    assert next_state == '#', f"Expected '#', got '{next_state}'"
    print("  PASS\n")

def test_lumberyard_rules():
    """Test lumberyard transformation rules."""
    # Should stay (has both tree and lumberyard)
    grid1 = [
        ['#', '|', '.'],
        ['#', '#', '.'],
        ['.', '.', '.']
    ]
    next_state1 = get_next_state(grid1, 1, 1)
    print(f"Test 5a - Lumberyard with tree and lumberyard neighbors:")
    print(f"  Next state: {next_state1} (expected: #)")
    assert next_state1 == '#', f"Expected '#', got '{next_state1}'"
    print("  PASS")

    # Should become open (has lumberyard but no trees)
    grid2 = [
        ['#', '.', '.'],
        ['#', '#', '.'],
        ['.', '.', '.']
    ]
    next_state2 = get_next_state(grid2, 1, 1)
    print(f"Test 5b - Lumberyard with lumberyard but no tree neighbors:")
    print(f"  Next state: {next_state2} (expected: .)")
    assert next_state2 == '.', f"Expected '.', got '{next_state2}'"
    print("  PASS")

    # Should become open (has trees but no lumberyard)
    grid3 = [
        ['|', '|', '.'],
        ['|', '#', '.'],
        ['.', '.', '.']
    ]
    next_state3 = get_next_state(grid3, 1, 1)
    print(f"Test 5c - Lumberyard with trees but no other lumberyard neighbors:")
    print(f"  Next state: {next_state3} (expected: .)")
    assert next_state3 == '.', f"Expected '.', got '{next_state3}'"
    print("  PASS\n")

def test_simultaneous_updates():
    """Test that all cells update simultaneously."""
    grid = [
        ['.', '.', '.'],
        ['|', '|', '|'],
        ['.', '.', '.']
    ]

    new_grid = simulate_step(grid)

    expected = [
        ['.', '|', '.'],
        ['|', '|', '|'],
        ['.', '|', '.']
    ]

    print(f"Test 6 - Simultaneous updates:")
    print("  Original:")
    for row in grid:
        print(f"    {''.join(row)}")
    print("  After 1 step:")
    for row in new_grid:
        print(f"    {''.join(row)}")
    print("  Expected:")
    for row in expected:
        print(f"    {''.join(row)}")

    assert new_grid == expected, f"Grid mismatch"
    print("  PASS\n")

def test_resource_calculation():
    """Test resource value calculation."""
    grid = [
        ['|', '|', '#'],
        ['#', '.', '|'],
        ['|', '#', '#']
    ]

    value = calculate_resource_value(grid)
    print(f"Test 7 - Resource calculation:")
    print(f"  Trees: 4, Lumberyards: 4")
    print(f"  Resource value: {value} (expected: 16)")
    assert value == 16, f"Expected 16, got {value}"
    print("  PASS\n")

def test_input_parsing():
    """Test that input parsing works correctly."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    grid = parse_input(input_text)

    print(f"Test 8 - Input parsing:")
    print(f"  Grid dimensions: {len(grid)}x{len(grid[0])} (expected: 50x50)")
    assert len(grid) == 50, f"Expected 50 rows, got {len(grid)}"
    assert len(grid[0]) == 50, f"Expected 50 cols, got {len(grid[0])}"

    # Check first few characters match
    assert grid[0][0] == '|', f"Expected grid[0][0]='|', got '{grid[0][0]}'"
    assert grid[0][1] == '|', f"Expected grid[0][1]='|', got '{grid[0][1]}'"
    assert grid[0][2] == '#', f"Expected grid[0][2]='#', got '{grid[0][2]}'"
    print("  PASS\n")

if __name__ == '__main__':
    print("Running verification tests...\n")
    print("="*60)

    try:
        test_input_parsing()
        test_neighbor_counting()
        test_corner_bounds()
        test_open_ground_rule()
        test_tree_rule()
        test_lumberyard_rules()
        test_simultaneous_updates()
        test_resource_calculation()

        print("="*60)
        print("\nAll tests PASSED! ✓\n")

    except AssertionError as e:
        print("="*60)
        print(f"\nTest FAILED: {e}\n")
        exit(1)
