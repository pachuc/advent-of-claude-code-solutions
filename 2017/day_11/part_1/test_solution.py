"""
Test suite for Hexagonal Grid Navigation Distance solver
"""

from solution import (
    DIRECTION_DELTAS,
    parse_input,
    calculate_final_position,
    calculate_distance,
    solve
)


def test_examples():
    """Test all provided examples."""
    print("\n1. Testing Examples from Problem Statement...")
    test_cases = [
        ("ne,ne,ne", 3),
        ("ne,ne,sw,sw", 0),
        ("ne,ne,s,s", 2),
        ("se,sw,se,sw,sw", 3)
    ]

    for input_str, expected in test_cases:
        moves = input_str.split(',')
        x, y, z = calculate_final_position(moves)
        distance = calculate_distance(x, y, z)
        assert distance == expected, f"Failed for {input_str}: got {distance}, expected {expected}"
        print(f"  ✓ {input_str} → {distance}")

    print("  All example tests passed!")


def test_edge_cases():
    """Test edge cases."""
    print("\n2. Testing Edge Cases...")
    test_cases = [
        ("", 0),  # Empty input
        ("n", 1),  # Single move
        ("n,ne,se,s,sw,nw", 0),  # All six directions (should return to origin)
        (",".join(["n"] * 10), 10)  # Many moves in same direction
    ]

    for input_str, expected in test_cases:
        # Parse like the actual implementation
        if input_str:
            moves = [move.strip() for move in input_str.split(',') if move.strip()]
        else:
            moves = []

        x, y, z = calculate_final_position(moves)
        distance = calculate_distance(x, y, z)
        assert distance == expected, f"Failed for '{input_str}': got {distance}, expected {expected}"
        print(f"  ✓ '{input_str[:20]}{'...' if len(input_str) > 20 else ''}' → {distance}")

    print("  All edge case tests passed!")


def test_cube_coordinate_invariant():
    """Verify cube coordinate invariant is maintained."""
    print("\n3. Testing Cube Coordinate Invariant (x + y + z = 0)...")

    # Test that all direction deltas sum to 0
    for direction, (dx, dy, dz) in DIRECTION_DELTAS.items():
        assert dx + dy + dz == 0, f"Direction {direction} breaks invariant"
    print("  ✓ All direction deltas maintain invariant")

    # Test that all positions maintain invariant
    test_inputs = [
        "ne,ne,ne",
        "ne,ne,sw,sw",
        "se,sw,se,sw,sw",
        "n,s,ne,sw,nw,se"
    ]

    for input_str in test_inputs:
        moves = input_str.split(',')
        x, y, z = calculate_final_position(moves)
        assert x + y + z == 0, f"Position ({x},{y},{z}) breaks invariant for {input_str}"

    print("  ✓ All positions maintain invariant")
    print("  Cube coordinate invariant verified!")


def test_distance_calculation():
    """Test distance calculation for known positions."""
    print("\n4. Testing Distance Calculation...")
    test_cases = [
        ((1, 0, -1), 1),    # One NE
        ((2, 0, -2), 2),    # Two NE
        ((1, 1, -2), 2),    # NE + N
        ((3, -1, -2), 3),   # Complex
        ((0, 0, 0), 0),     # Origin
        ((-5, 2, 3), 5)     # Negative coordinates
    ]

    for (x, y, z), expected in test_cases:
        distance = calculate_distance(x, y, z)
        assert distance == expected, f"Distance for ({x},{y},{z}): got {distance}, expected {expected}"
        print(f"  ✓ ({x}, {y}, {z}) → {distance}")

    print("  Distance calculation tests passed!")


def test_opposite_directions():
    """Test that opposite directions cancel out."""
    print("\n5. Testing Opposite Directions...")
    opposite_pairs = [
        ("n,s", 0),
        ("ne,sw", 0),
        ("se,nw", 0),
        ("n,s,n,s,ne,sw,ne,sw", 0)
    ]

    for input_str, expected in opposite_pairs:
        moves = input_str.split(',')
        x, y, z = calculate_final_position(moves)
        distance = calculate_distance(x, y, z)
        assert distance == expected, f"Failed for {input_str}: got {distance}, expected {expected}"
        print(f"  ✓ {input_str} → {distance}")

    print("  Opposite direction tests passed!")


def test_path_equivalence():
    """Test that different paths to same position have same distance."""
    print("\n6. Testing Path Equivalence...")

    # Verify that the same final position results in the same distance
    # regardless of the path taken
    test_cases = [
        # Two paths that both end at position (2, 0, -2)
        (["ne", "ne"], ["n", "se", "ne"]),
    ]

    for path1, path2 in test_cases:
        x1, y1, z1 = calculate_final_position(path1)
        x2, y2, z2 = calculate_final_position(path2)

        # Verify both paths reach same position
        assert (x1, y1, z1) == (x2, y2, z2), f"Paths should lead to same position"

        # Verify same distance
        dist1 = calculate_distance(x1, y1, z1)
        dist2 = calculate_distance(x2, y2, z2)
        assert dist1 == dist2, f"Same position, different distances: {dist1} vs {dist2}"
        print(f"  ✓ {','.join(path1)} ≡ {','.join(path2)} → position ({x1},{y1},{z1}), distance {dist1}")

    print("  Path equivalence tests passed!")


def test_input_validation():
    """Test input parsing and validation."""
    print("\n7. Testing Input Validation...")

    # Test whitespace handling
    test_inputs = [
        "ne,ne,ne",
        "ne,ne,ne\n",
        "ne, ne, ne",
        " ne , ne , ne "
    ]

    expected_moves = ["ne", "ne", "ne"]
    for input_str in test_inputs:
        if input_str:
            moves = [move.strip() for move in input_str.strip().split(',') if move.strip()]
        else:
            moves = []
        assert moves == expected_moves, f"Whitespace handling failed for '{input_str}'"
    print("  ✓ Whitespace handling correct")

    # Test invalid direction detection
    invalid_inputs = [
        "ne,east,ne",  # Invalid direction
        "ne,nn,ne",    # Typo
    ]

    for input_str in invalid_inputs:
        moves = [move.strip() for move in input_str.split(',') if move.strip()]
        try:
            calculate_final_position(moves)
            assert False, f"Should have raised ValueError for invalid input: {input_str}"
        except ValueError as e:
            # Expected - invalid direction should raise ValueError
            assert "Invalid direction" in str(e)
    print("  ✓ Invalid direction detection works")

    print("  Input validation tests passed!")


def test_actual_input():
    """Test the actual input file."""
    print("\n8. Testing Actual Input...")

    # Parse actual input
    moves = parse_input('input.md')

    # Verify parsing
    assert len(moves) > 0, "Input should not be empty"
    assert all(isinstance(move, str) and move for move in moves), "All moves should be non-empty strings"
    assert all(move in DIRECTION_DELTAS for move in moves), "All moves should be valid directions"

    # Verify no whitespace in parsed moves
    assert all(move == move.strip() for move in moves), "Moves should have whitespace stripped"

    # Calculate solution
    x, y, z = calculate_final_position(moves)
    distance = calculate_distance(x, y, z)

    # Sanity checks
    assert distance >= 0, "Distance should be non-negative"
    assert distance <= len(moves), "Distance can't exceed total moves"
    assert isinstance(distance, int), "Distance should be an integer"

    # Verify invariant
    assert x + y + z == 0, f"Final position should maintain cube coordinate invariant"

    print(f"  ✓ Total moves: {len(moves)}")
    print(f"  ✓ Final position: ({x}, {y}, {z})")
    print(f"  ✓ Distance: {distance}")
    print("  Actual input test passed!")

    return distance


def run_all_tests():
    """Run all test suites."""
    print("=" * 60)
    print("Running Hexagonal Grid Distance Tests")
    print("=" * 60)

    test_examples()
    test_edge_cases()
    test_cube_coordinate_invariant()
    test_distance_calculation()
    test_opposite_directions()
    test_path_equivalence()
    test_input_validation()
    distance = test_actual_input()

    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print(f"✓ Final Answer: {distance}")
    print("=" * 60)

    return distance


if __name__ == '__main__':
    run_all_tests()
