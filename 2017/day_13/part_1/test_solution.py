from solution import parse_input, is_caught, calculate_severity


def test_is_caught_function():
    """Test the is_caught function with various cases."""
    print("Testing is_caught function...")

    # Test cases from test plan
    assert is_caught(0, 3) == True, "Failed: depth=0, range=3"   # 0 % 4 = 0
    assert is_caught(1, 2) == False, "Failed: depth=1, range=2"  # 1 % 2 = 1
    assert is_caught(2, 2) == True, "Failed: depth=2, range=2"   # 2 % 2 = 0
    assert is_caught(6, 4) == True, "Failed: depth=6, range=4"   # 6 % 6 = 0
    assert is_caught(4, 4) == False, "Failed: depth=4, range=4"  # 4 % 6 = 4
    assert is_caught(8, 3) == True, "Failed: depth=8, range=3"   # 8 % 4 = 0
    assert is_caught(10, 3) == False, "Failed: depth=10, range=3" # 10 % 4 = 2

    print("  ✓ All is_caught tests passed")


def test_range_one_no_division_error():
    """Critical test: range=1 should not cause division by zero."""
    print("Testing range=1 edge case...")

    assert is_caught(0, 1) == True, "Failed: range=1 at depth=0"
    assert is_caught(5, 1) == True, "Failed: range=1 at depth=5"
    assert is_caught(100, 1) == True, "Failed: range=1 at depth=100"

    print("  ✓ Range=1 edge case handled correctly (no division errors)")


def test_example():
    """Test the provided example from problem statement."""
    print("Testing provided example...")

    layers = [(0, 3), (1, 2), (4, 4), (6, 4)]
    result = calculate_severity(layers)

    print(f"  Input: {layers}")
    print(f"  Expected: 24")
    print(f"  Got: {result}")

    assert result == 24, f"Failed: expected 24, got {result}"
    print("  ✓ Example test passed")


def test_range_one_severity():
    """Test severity calculation with range=1 scanners."""
    print("Testing severity with range=1...")

    layers = [(0, 1), (5, 1), (10, 1)]
    result = calculate_severity(layers)
    expected = 0 * 1 + 5 * 1 + 10 * 1  # = 15

    print(f"  Input: {layers}")
    print(f"  Expected: {expected}")
    print(f"  Got: {result}")

    assert result == expected, f"Failed: expected {expected}, got {result}"
    print("  ✓ Range=1 severity test passed")


def test_no_caught():
    """Test case where no layers catch the packet."""
    print("Testing scenario with no catches...")

    layers = [(1, 3), (3, 5)]
    result = calculate_severity(layers)

    # Layer 1, range 3: period = 4, 1 % 4 = 1 → not caught
    # Layer 3, range 5: period = 8, 3 % 8 = 3 → not caught

    print(f"  Input: {layers}")
    print(f"  Expected: 0")
    print(f"  Got: {result}")

    assert result == 0, f"Failed: expected 0, got {result}"
    print("  ✓ No-catch test passed")


def test_all_caught():
    """Test case where all layers catch the packet."""
    print("Testing scenario where all catch...")

    layers = [(0, 2), (2, 2), (4, 3)]
    result = calculate_severity(layers)

    # Layer 0: always caught → 0×2 = 0
    # Layer 2, range 2: period = 2, 2 % 2 = 0 → caught → 2×2 = 4
    # Layer 4, range 3: period = 4, 4 % 4 = 0 → caught → 4×3 = 12
    expected = 0 + 4 + 12  # = 16

    print(f"  Input: {layers}")
    print(f"  Expected: {expected}")
    print(f"  Got: {result}")

    assert result == expected, f"Failed: expected {expected}, got {result}"
    print("  ✓ All-catch test passed")


def test_empty_input():
    """Test with empty layers list."""
    print("Testing empty input...")

    layers = []
    result = calculate_severity(layers)

    print(f"  Input: {layers}")
    print(f"  Expected: 0")
    print(f"  Got: {result}")

    assert result == 0, f"Failed: expected 0, got {result}"
    print("  ✓ Empty input test passed")


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("Running Unit Tests")
    print("=" * 60)

    test_is_caught_function()
    test_range_one_no_division_error()
    test_example()
    test_range_one_severity()
    test_no_caught()
    test_all_caught()
    test_empty_input()

    print("=" * 60)
    print("All tests passed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
