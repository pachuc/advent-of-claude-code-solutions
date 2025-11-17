from solution import calculate_encoded_difference, solve


def test_examples():
    """Test cases from problem statement"""
    print("Testing example cases...")

    test_cases = [
        ('""', 4),
        ('"abc"', 4),
        ('"aaa\\"aaa"', 6),
        ('"\\x27"', 5),
    ]

    for input_str, expected_diff in test_cases:
        result = calculate_encoded_difference(input_str)
        status = "PASS" if result == expected_diff else "FAIL"
        print(f"  {status}: {repr(input_str)} -> diff={result} (expected {expected_diff})")
        if result != expected_diff:
            print(f"    Original length: {len(input_str)}")
            print(f"    Calculated encoded length: {len(input_str) + result}")

    print()


def test_edge_cases():
    """Test edge cases"""
    print("Testing edge cases...")

    # Test with only backslashes
    test_input = '"\\\\"'  # Represents a string with two backslashes
    result = calculate_encoded_difference(test_input)
    print(f"  Only backslashes {repr(test_input)}: diff={result} (expected 6)")

    # Test with only quotes
    test_input = '"\\"\\"'  # Represents escaped quotes
    result = calculate_encoded_difference(test_input)
    print(f"  Only quotes {repr(test_input)}: diff={result} (expected 8)")

    # Test with no special characters
    test_input = '"abcdef"'
    result = calculate_encoded_difference(test_input)
    print(f"  No special chars {repr(test_input)}: diff={result} (expected 4)")

    # Test consecutive backslashes
    test_input = '"\\\\\\\\"'  # Four backslashes
    result = calculate_encoded_difference(test_input)
    print(f"  Four backslashes {repr(test_input)}: diff={result} (expected 6)")

    print()


def test_real_input_samples():
    """Test a few lines from the actual input"""
    print("Testing sample lines from input.md...")

    # Line 1: "azlgxdbljwygyttzkfwuxv"
    line1 = '"azlgxdbljwygyttzkfwuxv"'
    diff1 = calculate_encoded_difference(line1)
    print(f"  Line 1: diff={diff1} (expected 4 for no special chars)")

    # Line 2: "v\xfb\"lgs\"kvjfywmut\x9cr"
    # This has backslashes and quotes
    line2 = '"v\\xfb\\"lgs\\"kvjfywmut\\x9cr"'
    diff2 = calculate_encoded_difference(line2)
    print(f"  Line 2: diff={diff2}")

    print()


def test_full_input():
    """Test against actual input file"""
    print("Testing full input.md file...")

    result = solve('input.md')
    print(f"  Total difference for input.md: {result}")

    # Sanity checks
    with open('input.md', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    min_expected = len(lines) * 4  # Minimum is 4 per line
    print(f"  Sanity check - minimum (4 per line × {len(lines)} lines): {min_expected}")
    print(f"  Result > minimum: {result > min_expected}")

    print()


if __name__ == "__main__":
    test_examples()
    test_edge_cases()
    test_real_input_samples()
    test_full_input()
    print("All tests completed!")
