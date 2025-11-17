import json
from solution import sum_numbers


def test_examples():
    """Test the provided examples from the problem statement."""
    print("=" * 60)
    print("EXAMPLE TESTS")
    print("=" * 60)

    tests = [
        ([1, 2, 3], 6, "Simple array"),
        ([1, {"c": "red", "b": 2}, 3], 4, "Array with red object"),
        ({"d": "red", "e": [1, 2, 3, 4], "f": 5}, 0, "Top-level object with red"),
        ([1, "red", 5], 6, "Red string in array"),
    ]

    passed = 0
    for i, (input_data, expected, description) in enumerate(tests, 1):
        result = sum_numbers(input_data)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result == expected:
            passed += 1
        print(f"Example {i} - {description}:")
        print(f"  {status} (expected {expected}, got {result})")

    print(f"\nExamples Passed: {passed}/{len(tests)}\n")
    return passed == len(tests)


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("=" * 60)
    print("EDGE CASE TESTS")
    print("=" * 60)

    tests = [
        ({}, 0, "Empty object"),
        ([], 0, "Empty array"),
        ([-5, 10, -3], 2, "Negative numbers"),
        ({"a": {"b": "red", "c": 5}, "d": 10}, 10, "Nested red object"),
        ({"red": 10, "blue": 5}, 15, "Red as key (not value)"),
        ({"a": "red", "b": "red", "c": 10}, 0, "Multiple red values"),
        ({"a": {"b": {"c": {"d": 1}}}}, 1, "Deep nesting"),
        ({"a": {"b": {"c": {"d": "red", "e": 10}}}}, 0, "Deep nesting with red at bottom"),
        ([1, {"a": 2}, 3, [4, 5], {"b": "red", "c": 6}], 15, "Mixed structures"),
        ({"a": [1, "red", 3], "b": 5}, 9, "Red in nested array inside object"),
        ({"a": "Red", "b": 10}, 10, "Case sensitivity (capital R)"),
        ([0, 1, {"a": 0}, 2], 3, "Zero values"),
        ([1.5, 2.5, 3.0], 7.0, "Floating point numbers"),
        ({"a": None, "b": 5, "c": None}, 5, "Null values"),
        ({"a": True, "b": 5, "c": False}, 5, "Boolean values (not counted as numbers)"),
        ({"a": " red ", "b": 10}, 10, "Red with spaces (not exact match)"),
        ({"a": "RED", "b": 10, "c": "Red"}, 10, "Red uppercase/mixed case"),
        ({"a": 16711680, "b": 10}, 16711690, "Numeric red (NOT string, should count)"),
    ]

    passed = 0
    for input_data, expected, description in tests:
        result = sum_numbers(input_data)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result == expected:
            passed += 1
        print(f"{description}:")
        print(f"  {status} (expected {expected}, got {result})")

    print(f"\nEdge Cases Passed: {passed}/{len(tests)}\n")
    return passed == len(tests)


def test_logic_verification():
    """Verify core filtering logic."""
    print("=" * 60)
    print("LOGIC VERIFICATION TESTS")
    print("=" * 60)

    tests = [
        ({"x": "red", "y": 100, "z": {"a": 50}}, 0, "Object with red filters everything"),
        ({"x": "blue", "y": 100}, 100, "Object without red processes normally"),
        (["red", "red", "red", 10], 10, "Array always processes all elements"),
        ({"a": "red", "b": 10}, 0, "String red triggers filter"),
        ({"a": 123, "b": 10}, 133, "Non-string values don't trigger filter"),
    ]

    passed = 0
    for input_data, expected, description in tests:
        result = sum_numbers(input_data)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result == expected:
            passed += 1
        print(f"{description}:")
        print(f"  {status} (expected {expected}, got {result})")

    print(f"\nLogic Tests Passed: {passed}/{len(tests)}\n")
    return passed == len(tests)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AUTOMATED TEST SUITE FOR JSON NUMBER SUMMATION")
    print("=" * 60 + "\n")

    all_passed = True

    # Run all test suites
    all_passed &= test_examples()
    all_passed &= test_edge_cases()
    all_passed &= test_logic_verification()

    # Final summary
    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED - Review output above")
    print("=" * 60)
