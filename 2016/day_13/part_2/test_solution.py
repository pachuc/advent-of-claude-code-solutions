#!/usr/bin/env python3
"""Comprehensive test suite for Part 2 solution."""

from solution import is_open_space, count_reachable_locations

def test_is_open_space():
    """Test the maze generation logic."""
    print("Testing is_open_space function...")

    # Test with favorite number 1362 (actual input)
    assert is_open_space(1, 1, 1362) == True, "(1,1) should be open (start position)"
    assert is_open_space(31, 39, 1362) == True, "(31,39) should be open (Part 1 target)"

    # Test negative coordinates
    assert is_open_space(-1, 0, 1362) == False, "Negative x should return False"
    assert is_open_space(0, -1, 1362) == False, "Negative y should return False"
    assert is_open_space(-5, -5, 1362) == False, "Both negative should return False"

    # Test with favorite number 10 (example from Part 1)
    assert is_open_space(1, 1, 10) == True, "(1,1) should be open with favorite=10"
    assert is_open_space(7, 4, 10) == True, "(7,4) should be open with favorite=10"

    print("✓ All is_open_space tests passed!")


def test_small_step_limits():
    """Test with small step limits to verify correctness."""
    print("\nTesting small step limits...")

    favorite = 1362
    start = (1, 1)

    # max_steps = 0: only starting position
    count_0 = count_reachable_locations(start, 0, favorite)
    assert count_0 == 1, f"max_steps=0 should return 1, got {count_0}"
    print(f"  max_steps=0: {count_0} location(s)")

    # max_steps = 1: start + adjacent open spaces
    count_1 = count_reachable_locations(start, 1, favorite)
    assert count_1 >= 1, f"max_steps=1 should be >= 1, got {count_1}"
    print(f"  max_steps=1: {count_1} location(s)")

    # max_steps = 2
    count_2 = count_reachable_locations(start, 2, favorite)
    assert count_2 >= count_1, f"max_steps=2 should be >= max_steps=1"
    print(f"  max_steps=2: {count_2} location(s)")

    # max_steps = 5
    count_5 = count_reachable_locations(start, 5, favorite)
    assert count_5 >= count_2, f"max_steps=5 should be >= max_steps=2"
    print(f"  max_steps=5: {count_5} location(s)")

    print("✓ All small step limit tests passed!")


def test_monotonicity():
    """Test that count increases or stays same as steps increase."""
    print("\nTesting monotonicity...")

    favorite = 1362
    start = (1, 1)
    results = []

    for steps in range(0, 55, 5):
        count = count_reachable_locations(start, steps, favorite)
        results.append((steps, count))

    # Verify non-decreasing
    for i in range(len(results) - 1):
        steps_i, count_i = results[i]
        steps_j, count_j = results[i + 1]
        assert count_j >= count_i, f"Count decreased from steps={steps_i} ({count_i}) to steps={steps_j} ({count_j})"

    print("  Results:", results)
    print("✓ Monotonicity test passed!")


def test_boundary_condition():
    """Test max_steps=50 vs max_steps=51."""
    print("\nTesting boundary condition (50 vs 51 steps)...")

    favorite = 1362
    start = (1, 1)

    count_50 = count_reachable_locations(start, 50, favorite)
    count_51 = count_reachable_locations(start, 51, favorite)

    assert count_51 >= count_50, f"count_51 ({count_51}) should be >= count_50 ({count_50})"

    print(f"  max_steps=50: {count_50} locations")
    print(f"  max_steps=51: {count_51} locations")
    print(f"  Difference: {count_51 - count_50} new location(s) at step 51")
    print("✓ Boundary condition test passed!")


def test_part1_cross_validation():
    """
    Critical test: Part 1 found that (31, 39) is reachable in exactly 82 steps.
    This validates our step counting is precise.
    """
    print("\nTesting Part 1 cross-validation...")

    favorite = 1362
    start = (1, 1)
    target = (31, 39)

    # Test with max_steps = 50 (should NOT reach target)
    count_50, visited_50 = count_reachable_locations(start, 50, favorite, debug=True)
    assert target not in visited_50, f"{target} should NOT be reachable in 50 steps"
    print(f"  ✓ {target} NOT reachable in 50 steps (expected)")

    # Test with max_steps = 81 (should NOT reach target)
    count_81, visited_81 = count_reachable_locations(start, 81, favorite, debug=True)
    assert target not in visited_81, f"{target} should NOT be reachable in 81 steps"
    print(f"  ✓ {target} NOT reachable in 81 steps (expected)")

    # Test with max_steps = 82 (SHOULD reach target)
    count_82, visited_82 = count_reachable_locations(start, 82, favorite, debug=True)
    assert target in visited_82, f"{target} SHOULD be reachable in 82 steps"
    print(f"  ✓ {target} IS reachable in 82 steps (expected)")

    print("✓ Part 1 cross-validation passed! Step counting is precise.")


def test_reproducibility():
    """Test that the solution produces consistent results."""
    print("\nTesting reproducibility...")

    favorite = 1362
    start = (1, 1)
    max_steps = 50

    results = []
    for i in range(3):
        count = count_reachable_locations(start, max_steps, favorite)
        results.append(count)

    assert all(r == results[0] for r in results), f"Results not consistent: {results}"
    print(f"  All 3 runs returned: {results[0]}")
    print("✓ Reproducibility test passed!")


def test_bounds_check():
    """Verify result is within theoretical bounds."""
    print("\nTesting bounds check...")

    favorite = 1362
    start = (1, 1)
    max_steps = 50

    result = count_reachable_locations(start, max_steps, favorite)

    # Theoretical maximum with Manhattan distance 50: (50+1)^2 = 2601
    # Minimum: at least 1 (starting position)
    assert 1 <= result <= 2601, f"Result {result} outside theoretical bounds [1, 2601]"

    print(f"  Result: {result}")
    print(f"  Theoretical bounds: [1, 2601]")
    print("✓ Bounds check passed!")


def test_debug_parameter():
    """Test that debug parameter works correctly."""
    print("\nTesting debug parameter...")

    favorite = 1362
    start = (1, 1)

    # Without debug
    count_only = count_reachable_locations(start, 10, favorite, debug=False)
    assert isinstance(count_only, int), "Without debug should return int"

    # With debug
    count_debug, visited_debug = count_reachable_locations(start, 10, favorite, debug=True)
    assert isinstance(count_debug, int), "With debug should return int count"
    assert isinstance(visited_debug, set), "With debug should return set"
    assert count_debug == len(visited_debug), "Count should match visited set size"
    assert count_only == count_debug, "Count should be same with or without debug"

    print(f"  count_only: {count_only}")
    print(f"  count_debug: {count_debug}, visited set size: {len(visited_debug)}")
    print("✓ Debug parameter test passed!")


def main():
    """Run all tests."""
    print("="*70)
    print("COMPREHENSIVE TEST SUITE FOR PART 2 SOLUTION")
    print("="*70)

    try:
        test_is_open_space()
        test_small_step_limits()
        test_monotonicity()
        test_boundary_condition()
        test_part1_cross_validation()
        test_reproducibility()
        test_bounds_check()
        test_debug_parameter()

        print("\n" + "="*70)
        print("ALL TESTS PASSED! ✓")
        print("="*70)

        # Get final answer
        favorite = 1362
        start = (1, 1)
        max_steps = 50
        final_answer = count_reachable_locations(start, max_steps, favorite)

        print(f"\nFinal Answer: {final_answer}")
        print(f"This is the number of distinct locations reachable from {start}")
        print(f"within {max_steps} steps with favorite number {favorite}.")

        return final_answer

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return None
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()
