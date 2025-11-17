from solution import calculate_decompressed_length_recursive

def test_solution():
    tests = [
        # Basic examples from problem statement
        ("(3x3)XYZ", 9),
        ("X(8x2)(3x3)ABCY", 20),
        ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),

        # Edge cases
        ("ADVENT", 6),
        ("", 0),
        ("(0x5)ABC", 3),

        # Regression tests from Part 1
        ("A(1x5)BC", 7),
        ("(3x3)XYZ", 9),
        ("A(2x2)BCD(2x2)EFG", 11),
        ("(6x1)(1x3)A", 3),  # Different from Part 1's 6

        # Whitespace tests
        ("(3x3) XY", 6),
        ("(4x2)A B ", 4),
    ]

    passed = 0
    failed = 0

    for i, (input_str, expected) in enumerate(tests):
        result = calculate_decompressed_length_recursive(input_str)
        if result == expected:
            print(f"Test {i+1} PASSED: '{input_str}' → {result}")
            passed += 1
        else:
            print(f"Test {i+1} FAILED: '{input_str}' → {result} (expected {expected})")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == '__main__':
    test_solution()
