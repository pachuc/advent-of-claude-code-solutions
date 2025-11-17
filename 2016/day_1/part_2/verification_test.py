"""
Comprehensive verification test for Part 2 solution
"""
from solution import (
    find_first_revisited_position,
    calculate_manhattan_distance,
    parse_input,
    solve_part2
)

def test_example():
    """Test the provided example from the problem"""
    print("Testing example: R8, R4, R4, R8")
    instructions = [('R', 8), ('R', 4), ('R', 4), ('R', 8)]

    # Manually trace the path
    # Start at (0,0) facing North
    # R8 (turn right to East): (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0)
    # R4 (turn right to South): (8,-1), (8,-2), (8,-3), (8,-4)
    # R4 (turn right to West): (7,-4), (6,-4), (5,-4), (4,-4)
    # R8 (turn right to North): (4,-3), (4,-2), (4,-1), (4,0) <- STOP! This was visited during R8

    x, y = find_first_revisited_position(instructions)
    distance = calculate_manhattan_distance(x, y)

    assert (x, y) == (4, 0), f"Expected (4, 0), got ({x}, {y})"
    assert distance == 4, f"Expected distance 4, got {distance}"

    print(f"  ✓ Found first revisit at ({x}, {y}), distance = {distance}")
    return True

def test_starting_position_tracking():
    """Test that starting position (0,0) is properly tracked"""
    print("\nTesting that starting position is tracked (R1, R1, R1, R1)")
    # This creates a 1x1 square returning to origin
    instructions = [('R', 1), ('R', 1), ('R', 1), ('R', 1)]

    x, y = find_first_revisited_position(instructions)
    distance = calculate_manhattan_distance(x, y)

    assert (x, y) == (0, 0), f"Expected (0, 0), got ({x}, {y})"
    assert distance == 0, f"Expected distance 0, got {distance}"

    print(f"  ✓ Correctly returns to origin at ({x}, {y}), distance = {distance}")
    return True

def test_step_by_step_tracking():
    """Test that individual steps are tracked, not just endpoints"""
    print("\nTesting step-by-step tracking")
    # R5, R1, R1, R10 should stop at (4,0) during the R10 instruction
    instructions = [('R', 5), ('R', 1), ('R', 1), ('R', 10)]

    x, y = find_first_revisited_position(instructions)
    distance = calculate_manhattan_distance(x, y)

    # Should stop at (4, 0) which was visited during R5
    # NOT at (5, 0) or any other position
    assert (x, y) == (4, 0), f"Expected (4, 0), got ({x}, {y})"
    assert distance == 4, f"Expected distance 4, got {distance}"

    print(f"  ✓ Stops immediately at first revisit ({x}, {y}), distance = {distance}")
    return True

def test_actual_input():
    """Test with actual puzzle input"""
    print("\nTesting actual puzzle input")

    distance, (x, y) = solve_part2('input.md')

    print(f"  First revisit at: ({x}, {y})")
    print(f"  Manhattan distance: {distance}")

    # Sanity checks
    assert isinstance(distance, int), "Distance should be an integer"
    assert distance > 0, "Distance should be positive"
    assert distance == 159, f"Expected distance 159 from implementation summary, got {distance}"
    assert (x, y) == (9, -150), f"Expected (9, -150) from implementation summary, got ({x}, {y})"

    # Compare with Part 1 answer
    part1_answer = 300
    if distance < part1_answer:
        print(f"  ✓ Distance {distance} < Part 1 answer {part1_answer} (expected)")
    else:
        print(f"  ⚠ Warning: Distance {distance} >= Part 1 answer {part1_answer}")

    # Check bounds
    instructions = parse_input('input.md')
    total_steps = sum(steps for _, steps in instructions)
    assert 0 <= distance <= total_steps, f"Distance {distance} outside bounds [0, {total_steps}]"
    print(f"  ✓ Distance {distance} within bounds [0, {total_steps}]")

    return True

def test_negative_coordinates():
    """Test that negative coordinates work correctly"""
    print("\nTesting negative coordinates")
    # L5, L5 should go to (-5, -5)
    instructions = [('L', 5), ('L', 5)]

    # This should NOT find a revisit
    # Start: (0,0) facing North
    # L5 (turn left to West): (-1,0), (-2,0), (-3,0), (-4,0), (-5,0)
    # L5 (turn left to South): (-5,-1), (-5,-2), (-5,-3), (-5,-4), (-5,-5)
    # No revisits occur

    try:
        x, y = find_first_revisited_position(instructions)
        # If we get here, it found a revisit (unexpected)
        print(f"  ⚠ Unexpected revisit at ({x}, {y})")
        return False
    except ValueError as e:
        # Expected - no revisit
        print(f"  ✓ No revisit found (expected): {e}")
        return True

def main():
    print("=" * 60)
    print("VERIFICATION TEST SUITE FOR PART 2")
    print("=" * 60)

    tests = [
        test_example,
        test_starting_position_tracking,
        test_step_by_step_tracking,
        test_negative_coordinates,
        test_actual_input,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        print("\nFinal answer: 159")
        return True
    else:
        print(f"\n✗ {failed} test(s) failed")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
