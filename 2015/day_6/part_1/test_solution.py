from solution import parse_instruction, apply_instruction


def test_parsing():
    """Test that parsing correctly extracts commands and coordinates."""
    print("Testing parsing...")

    # Test turn on
    result = parse_instruction("turn on 887,9 through 959,629")
    assert result == ('on', 887, 9, 959, 629), f"Expected ('on', 887, 9, 959, 629), got {result}"

    # Test turn off
    result = parse_instruction("turn off 499,499 through 500,500")
    assert result == ('off', 499, 499, 500, 500), f"Expected ('off', 499, 499, 500, 500), got {result}"

    # Test toggle
    result = parse_instruction("toggle 0,0 through 999,0")
    assert result == ('toggle', 0, 0, 999, 0), f"Expected ('toggle', 0, 0, 999, 0), got {result}"

    # Test edge cases
    result = parse_instruction("turn on 0,0 through 0,0")
    assert result == ('on', 0, 0, 0, 0), f"Expected ('on', 0, 0, 0, 0), got {result}"

    result = parse_instruction("turn off 0,0 through 999,999")
    assert result == ('off', 0, 0, 999, 999), f"Expected ('off', 0, 0, 999, 999), got {result}"

    print("✓ Parsing tests passed")


def test_coordinate_system():
    """CRITICAL: Verify correct coordinate interpretation (col, row) -> grid[row*1000+col]"""
    print("Testing coordinate system...")

    grid = [False] * 1000000

    # Test: 3 columns (5-7) × 3 rows (10-12) = 9 lights
    apply_instruction(grid, 'on', 5, 10, 7, 12)
    assert sum(grid) == 9, f"Expected 9 lights, got {sum(grid)}"

    # Verify specific positions
    assert grid[10*1000 + 5] == True, "Position (col=5, row=10) should be ON"
    assert grid[10*1000 + 6] == True, "Position (col=6, row=10) should be ON"
    assert grid[10*1000 + 7] == True, "Position (col=7, row=10) should be ON"
    assert grid[12*1000 + 7] == True, "Position (col=7, row=12) should be ON"
    assert grid[10*1000 + 8] == False, "Position (col=8, row=10) should be OFF"

    print("✓ Coordinate system tests passed")


def test_grid_operations():
    """Test grid operations for correctness."""
    print("Testing grid operations...")

    # Test turn on single light
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 0, 0, 0, 0)
    assert sum(grid) == 1, f"Expected 1 light, got {sum(grid)}"
    assert grid[0] == True, "Grid[0] should be True"

    # Test rectangular region (3x3 = 9)
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 0, 0, 2, 2)
    assert sum(grid) == 9, f"Expected 9 lights, got {sum(grid)}"

    # Test asymmetric rectangle (3 wide × 11 tall = 33)
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 100, 200, 102, 210)
    assert sum(grid) == 33, f"Expected 33 lights (3×11), got {sum(grid)}"

    # Test toggle
    grid = [False] * 1000000
    apply_instruction(grid, 'toggle', 0, 0, 0, 0)
    assert grid[0] == True, "Grid[0] should be True after toggle from False"
    apply_instruction(grid, 'toggle', 0, 0, 0, 0)
    assert grid[0] == False, "Grid[0] should be False after second toggle"

    # Test turn off
    grid = [True] * 1000000
    apply_instruction(grid, 'off', 5, 5, 10, 10)
    # Turned off 6x6 = 36 lights
    assert sum(grid) == 1000000 - 36, f"Expected {1000000 - 36} lights, got {sum(grid)}"

    print("✓ Grid operation tests passed")


def test_examples():
    """Test examples from problem statement."""
    print("Testing examples from problem statement...")

    # Example 1: Turn on all lights
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 0, 0, 999, 999)
    assert sum(grid) == 1000000, f"Expected 1000000 lights, got {sum(grid)}"

    # Example 2: Toggle top row (row 0, all columns) after turning all on
    grid = [True] * 1000000
    apply_instruction(grid, 'toggle', 0, 0, 999, 0)
    assert sum(grid) == 999000, f"Expected 999000 lights, got {sum(grid)}"

    # Example 3: Turn off middle 4 lights (2×2)
    grid = [True] * 1000000
    apply_instruction(grid, 'off', 499, 499, 500, 500)
    assert sum(grid) == 999996, f"Expected 999996 lights, got {sum(grid)}"

    print("✓ Example tests passed")


def test_edge_cases():
    """Test edge cases."""
    print("Testing edge cases...")

    # Test empty grid
    grid = [False] * 1000000
    assert sum(grid) == 0, "Empty grid should have 0 lights on"

    # Test idempotent operations
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 5, 5, 10, 10)
    count1 = sum(grid)
    apply_instruction(grid, 'on', 5, 5, 10, 10)
    count2 = sum(grid)
    assert count1 == count2, "Turning on already-ON lights should not change count"

    # Test toggle twice returns to original
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 100, 100, 200, 200)
    count_initial = sum(grid)
    assert count_initial == 101 * 101, f"Expected {101*101} lights, got {count_initial}"
    apply_instruction(grid, 'toggle', 100, 100, 200, 200)
    assert sum(grid) == 0, "Toggle should turn all lights off"
    apply_instruction(grid, 'toggle', 100, 100, 200, 200)
    assert sum(grid) == count_initial, "Second toggle should restore original state"

    print("✓ Edge case tests passed")


if __name__ == '__main__':
    test_parsing()
    test_coordinate_system()
    test_grid_operations()
    test_examples()
    test_edge_cases()
    print("\n✅ All tests passed!")
