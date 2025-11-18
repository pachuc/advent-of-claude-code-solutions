"""
Test suite for Part 2: Maximum Distance During Journey
"""

from solution import find_max_distance, calculate_distance, DIRECTION_DELTAS


def test_basic_functionality():
    """Test basic functionality with simple paths"""
    print("Testing basic functionality...")

    # Test 1.1: Simple linear path
    moves = ['ne', 'ne', 'ne']
    result = find_max_distance(moves)
    assert result == 3, f"Test 1.1 failed: expected 3, got {result}"
    print("✓ Test 1.1 passed: Simple linear path (ne,ne,ne) = 3")

    # Test 1.2: Path returning to origin (CRITICAL TEST)
    moves = ['ne', 'ne', 'sw', 'sw']
    result = find_max_distance(moves)
    assert result == 2, f"Test 1.2 failed: expected 2, got {result}"
    print("✓ Test 1.2 passed: Path returning to origin (ne,ne,sw,sw) = 2")

    # Test 1.3: Oscillating path
    moves = ['n', 's', 'n', 's', 'n']
    result = find_max_distance(moves)
    assert result == 1, f"Test 1.3 failed: expected 1, got {result}"
    print("✓ Test 1.3 passed: Oscillating path (n,s,n,s,n) = 1")


def test_edge_cases():
    """Test edge cases"""
    print("\nTesting edge cases...")

    # Test 2.1: Empty input
    moves = []
    result = find_max_distance(moves)
    assert result == 0, f"Test 2.1 failed: expected 0, got {result}"
    print("✓ Test 2.1 passed: Empty input = 0")

    # Test 2.2: Single move
    moves = ['n']
    result = find_max_distance(moves)
    assert result == 1, f"Test 2.2 failed: expected 1, got {result}"
    print("✓ Test 2.2 passed: Single move (n) = 1")

    # Test 2.2 Extended: All six directions
    for direction in ['n', 'ne', 'se', 's', 'sw', 'nw']:
        moves = [direction]
        result = find_max_distance(moves)
        assert result == 1, f"Test 2.2 failed for {direction}: expected 1, got {result}"
    print("✓ Test 2.2 extended passed: All six directions = 1")

    # Test 2.3: Immediate return to origin
    moves = ['n', 's']
    result = find_max_distance(moves)
    assert result == 1, f"Test 2.3 failed: expected 1, got {result}"
    print("✓ Test 2.3 passed: Immediate return to origin (n,s) = 1")


def test_complex_paths():
    """Test complex paths"""
    print("\nTesting complex paths...")

    # Test 3.1: Spiral pattern
    moves = ['ne', 'se', 's', 'sw', 'nw', 'n', 'ne', 'se']
    result = find_max_distance(moves)
    assert result == 2, f"Test 3.1 failed: expected 2, got {result}"
    print("✓ Test 3.1 passed: Spiral pattern = 2")

    # Test 3.2: Path with multiple peaks
    moves = ['ne', 'ne', 'ne', 'sw', 'sw', 'sw', 'ne', 'ne', 'ne', 'ne', 'sw', 'sw', 'sw', 'sw']
    result = find_max_distance(moves)
    assert result == 4, f"Test 3.2 failed: expected 4, got {result}"
    print("✓ Test 3.2 passed: Path with multiple peaks = 4")

    # Test 3.3: Example from Part 1
    moves = ['ne', 'ne', 's', 's']
    result = find_max_distance(moves)
    assert result == 2, f"Test 3.3 failed: expected 2, got {result}"
    print("✓ Test 3.3 passed: Part 1 example (ne,ne,s,s) = 2")


def test_validation():
    """Test input validation"""
    print("\nTesting validation...")

    # Test 4.1: Invalid direction
    try:
        moves = ['ne', 'invalid', 'se']
        result = find_max_distance(moves)
        assert False, "Test 4.1 failed: should have raised ValueError"
    except ValueError as e:
        assert "Invalid direction" in str(e), f"Test 4.1 failed: wrong error message: {e}"
        print("✓ Test 4.1 passed: Invalid direction raises ValueError")


def test_cube_coordinate_invariant():
    """Verify cube coordinate invariant is maintained"""
    print("\nTesting cube coordinate invariant...")

    moves = ['ne', 'ne', 'sw', 'sw', 'n', 's', 'se', 'nw']
    x, y, z = 0, 0, 0

    for move in moves:
        dx, dy, dz = DIRECTION_DELTAS[move]
        x += dx
        y += dy
        z += dz
        assert x + y + z == 0, f"Invariant violated after {move}: x={x}, y={y}, z={z}, sum={x+y+z}"

    print("✓ Test 4.3 passed: Cube coordinate invariant maintained")


def run_all_tests():
    """Run all test suites"""
    print("=" * 60)
    print("Running Part 2 Test Suite")
    print("=" * 60)

    test_basic_functionality()
    test_edge_cases()
    test_complex_paths()
    test_validation()
    test_cube_coordinate_invariant()

    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
