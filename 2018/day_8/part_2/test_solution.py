"""
Test suite for Tree Node Value Calculator (Part 2)
"""

from solution import calculate_root_value


def test_solution(input_data, expected_value, test_name):
    """
    Test runner that bypasses file I/O for simplicity.
    Parses input string directly and calls calculate_root_value.
    """
    data = [int(x) for x in input_data.split()]
    try:
        result = calculate_root_value(data)
        if result == expected_value:
            print(f"PASS: {test_name} (result={result})")
            return True
        else:
            print(f"FAIL: {test_name} (expected={expected_value}, got={result})")
            return False
    except Exception as e:
        print(f"ERROR: {test_name} - {e}")
        return False


def run_all_tests():
    """Run all test cases in sequence."""
    tests = [
        ("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2", 66, "Test 1: Example from problem"),
        ("0 3 10 20 30", 60, "Test 2: Single leaf node"),
        ("2 2 0 1 5 0 1 10 1 2", 15, "Test 3: Internal node with children"),
        ("2 4 0 1 5 0 1 10 0 3 5 4", 0, "Test 4: Invalid child references"),
        ("1 3 0 1 7 1 1 1", 21, "Test 5: Duplicate child references"),
        ("1 1 1 1 1 1 0 1 5 1 1 1", 5, "Test 6: Deep nesting"),
        ("3 3 0 1 10 0 1 20 0 1 30 1 2 3", 60, "Test 7: Wide tree"),
        ("1 0 0 1 5", 0, "Test 8: Node with zero metadata"),
    ]

    print("Running test suite...\n")
    passed = 0
    for input_data, expected, name in tests:
        if test_solution(input_data, expected, name):
            passed += 1

    print(f"\n{passed}/{len(tests)} tests passed")
    return passed == len(tests)


if __name__ == '__main__':
    run_all_tests()
