from solution import spiral_manhattan_distance

def test_examples():
    """Test the provided examples"""
    assert spiral_manhattan_distance(1) == 0, "Failed for n=1"
    assert spiral_manhattan_distance(12) == 3, "Failed for n=12"
    assert spiral_manhattan_distance(23) == 2, "Failed for n=23"
    assert spiral_manhattan_distance(1024) == 31, "Failed for n=1024"
    print("✓ Example tests passed")


def test_ring_boundaries():
    """Test corner and edge values of rings"""
    # Ring 1 (values 2-9)
    assert spiral_manhattan_distance(2) == 1, "Failed for n=2"
    assert spiral_manhattan_distance(3) == 2, "Failed for n=3"
    assert spiral_manhattan_distance(4) == 1, "Failed for n=4"
    assert spiral_manhattan_distance(5) == 2, "Failed for n=5"
    assert spiral_manhattan_distance(9) == 2, "Failed for n=9"

    # Ring 2 (values 10-25)
    assert spiral_manhattan_distance(10) == 3, "Failed for n=10"
    assert spiral_manhattan_distance(11) == 2, "Failed for n=11"
    assert spiral_manhattan_distance(13) == 4, "Failed for n=13"
    assert spiral_manhattan_distance(17) == 4, "Failed for n=17"
    assert spiral_manhattan_distance(21) == 4, "Failed for n=21"
    assert spiral_manhattan_distance(25) == 4, "Failed for n=25"
    print("✓ Ring boundary tests passed")


def test_middle_positions():
    """Test middle of each side (minimum distance for ring)"""
    # Ring 1 middle positions (distance = 1)
    assert spiral_manhattan_distance(2) == 1, "Failed for n=2"
    assert spiral_manhattan_distance(4) == 1, "Failed for n=4"
    assert spiral_manhattan_distance(6) == 1, "Failed for n=6"
    assert spiral_manhattan_distance(8) == 1, "Failed for n=8"

    # Ring 2 middle positions (distance = 2)
    assert spiral_manhattan_distance(11) == 2, "Failed for n=11"
    assert spiral_manhattan_distance(15) == 2, "Failed for n=15"
    assert spiral_manhattan_distance(19) == 2, "Failed for n=19"
    assert spiral_manhattan_distance(23) == 2, "Failed for n=23"
    print("✓ Middle position tests passed")


def test_perfect_squares():
    """Test perfect squares of odd numbers (bottom-right corners)"""
    assert spiral_manhattan_distance(9) == 2, "Failed for n=9 (3²)"
    assert spiral_manhattan_distance(25) == 4, "Failed for n=25 (5²)"
    assert spiral_manhattan_distance(49) == 6, "Failed for n=49 (7²)"
    assert spiral_manhattan_distance(121) == 10, "Failed for n=121 (11²)"
    print("✓ Perfect square tests passed")


def test_sequential():
    """Test first 10 values"""
    expected = [0, 1, 2, 1, 2, 1, 2, 1, 2, 3]
    for i, exp in enumerate(expected, 1):
        result = spiral_manhattan_distance(i)
        assert result == exp, f"n={i}: expected {exp}, got {result}"
    print("✓ Sequential tests passed")


def test_actual_input():
    """Test with the actual problem input"""
    result = spiral_manhattan_distance(289326)
    assert isinstance(result, int), "Result should be an integer"
    assert result > 0, "Result should be positive"

    # Verify it's within reasonable bounds
    # sqrt(289326) ≈ 538.08, ceil to odd = 539
    # ring = 539 // 2 = 269
    # Distance should be between 269 (min for ring) and 538 (max for ring)
    assert 269 <= result <= 538, f"Result {result} outside expected range [269, 538]"
    print(f"✓ Actual input test passed: result = {result}")
    return result


def test_coordinates_verification():
    """Verify coordinates for specific test cases"""
    # We'll compute coordinates inline to verify the math is correct
    import math

    def get_coordinates(n):
        """Helper function to get coordinates"""
        if n == 1:
            return (0, 0)

        side_length = math.ceil(math.sqrt(n))
        if side_length % 2 == 0:
            side_length += 1
        ring = side_length // 2

        max_prev_ring = (2 * ring - 1) ** 2
        position_in_ring = n - max_prev_ring - 1

        side_len = 2 * ring
        side_index = position_in_ring // side_len
        offset = position_in_ring % side_len

        if side_index == 0:
            x, y = ring, -ring + 1 + offset
        elif side_index == 1:
            x, y = ring - 1 - offset, ring
        elif side_index == 2:
            x, y = -ring, ring - 1 - offset
        else:
            x, y = -ring + 1 + offset, -ring

        return (x, y)

    # Verify specific coordinates from the grid
    assert get_coordinates(1) == (0, 0), "Failed coordinates for n=1"
    assert get_coordinates(2) == (1, 0), "Failed coordinates for n=2"
    assert get_coordinates(3) == (1, 1), "Failed coordinates for n=3"
    assert get_coordinates(4) == (0, 1), "Failed coordinates for n=4"
    assert get_coordinates(5) == (-1, 1), "Failed coordinates for n=5"
    assert get_coordinates(11) == (2, 0), "Failed coordinates for n=11"
    assert get_coordinates(12) == (2, 1), "Failed coordinates for n=12"
    assert get_coordinates(13) == (2, 2), "Failed coordinates for n=13"
    assert get_coordinates(23) == (0, -2), "Failed coordinates for n=23"

    print("✓ Coordinate verification tests passed")


def run_all_tests():
    """Run complete test suite"""
    print("Running test suite...\n")
    test_examples()
    test_ring_boundaries()
    test_middle_positions()
    test_perfect_squares()
    test_sequential()
    test_coordinates_verification()
    result = test_actual_input()
    print("\n✅ All tests passed!")
    return result


if __name__ == "__main__":
    run_all_tests()
