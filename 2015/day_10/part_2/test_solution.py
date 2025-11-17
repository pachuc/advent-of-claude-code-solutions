import itertools
from solution import look_and_say


def test_single_transformations():
    """Test single look-and-say transformations."""
    test_cases = [
        ("1", "11"),
        ("11", "21"),
        ("21", "1211"),
        ("1211", "111221"),
        ("111221", "312211"),
        ("3", "13"),
        ("1111", "41"),
        ("1234", "11121314"),
        ("1112", "3112"),
        ("1122", "2122"),
    ]

    print("Testing single transformations:")
    all_passed = True
    for input_str, expected in test_cases:
        result = look_and_say(input_str)
        passed = result == expected
        all_passed = all_passed and passed
        status = "✓" if passed else "✗"
        print(f"{status} {input_str} -> {result} (expected {expected})")

    return all_passed


def test_multiple_iterations():
    """Test multiple iterations starting from '1'."""
    expected_sequence = [
        "1",
        "11",
        "21",
        "1211",
        "111221",
        "312211"
    ]

    print("\nTesting multiple iterations from '1':")
    current = "1"
    all_passed = True
    for i in range(len(expected_sequence)):
        passed = current == expected_sequence[i]
        all_passed = all_passed and passed
        status = "✓" if passed else "✗"
        print(f"{status} Iteration {i}: {current} (expected {expected_sequence[i]})")
        if i < len(expected_sequence) - 1:
            current = look_and_say(current)

    return all_passed


def test_edge_cases():
    """Test edge cases."""
    print("\nTesting edge cases:")
    test_cases = [
        ("", ""),  # Empty string
        ("5", "15"),  # Single non-1 digit
        ("1111111111", "101"),  # Ten 1s -> "101"
    ]

    all_passed = True
    for input_str, expected in test_cases:
        result = look_and_say(input_str)
        passed = result == expected
        all_passed = all_passed and passed
        status = "✓" if passed else "✗"
        if input_str == "":
            input_display = "(empty)"
        else:
            input_display = input_str
        print(f"{status} {input_display} -> {result} (expected {expected})")

    return all_passed


if __name__ == "__main__":
    print("=" * 60)
    print("Look-and-Say Unit Tests")
    print("=" * 60)
    print()

    test1_passed = test_single_transformations()
    test2_passed = test_multiple_iterations()
    test3_passed = test_edge_cases()

    print()
    print("=" * 60)
    if test1_passed and test2_passed and test3_passed:
        print("All tests PASSED!")
    else:
        print("Some tests FAILED!")
    print("=" * 60)
