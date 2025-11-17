from solution import count_code_chars, count_memory_chars, calculate_difference, read_input


def test_examples():
    """Test with examples from problem statement."""
    print("\n=== Testing Examples from Problem Statement ===")
    # Using raw strings to preserve escape sequences
    test_cases = [
        (r'""', 2, 0),
        (r'"abc"', 5, 3),
        (r'"aaa\"aaa"', 10, 7),
        (r'"\x27"', 6, 1)
    ]

    for line, expected_code, expected_memory in test_cases:
        code = count_code_chars(line)
        memory = count_memory_chars(line)
        diff = code - memory
        print(f"  {line:20} -> code={code}, memory={memory}, diff={diff}")
        assert code == expected_code, f"Code count failed for {line}: expected {expected_code}, got {code}"
        assert memory == expected_memory, f"Memory count failed for {line}: expected {expected_memory}, got {memory}"

    # Test combined difference
    total_diff = sum(code - memory for _, code, memory in test_cases)
    print(f"  Combined difference: {total_diff}")
    assert total_diff == 12, f"Expected 12, got {total_diff}"
    print("✓ All examples from problem statement passed!")


def test_edge_cases():
    """Test edge cases."""
    print("\n=== Testing Edge Cases ===")
    edge_cases = [
        (r'""', 2, 0, "empty string"),
        (r'"a"', 3, 1, "single char"),
        (r'"\\"', 4, 1, "single backslash"),
        (r'"\\\\"', 6, 2, "two backslashes"),
        (r'"\""', 4, 1, "single quote"),
        (r'"\"\""', 6, 2, "two quotes"),
        (r'"\x00"', 6, 1, "hex null"),
        (r'"\xff"', 6, 1, "hex max"),
        (r'"\x27\x27"', 10, 2, "two hex escapes"),
        (r'"\x27\x27\x27"', 14, 3, "three hex escapes"),
        (r'"abc\x27"', 9, 4, "hex at end"),
        (r'"\\\""', 6, 2, "backslash + quote"),
        (r'"\\\x27"', 8, 2, "backslash + hex"),
    ]

    for line, expected_code, expected_memory, desc in edge_cases:
        code = count_code_chars(line)
        memory = count_memory_chars(line)
        diff = code - memory
        print(f"  {desc:20} -> code={code}, memory={memory}, diff={diff}")
        assert code == expected_code, f"Code failed for {desc}: expected {expected_code}, got {code}"
        assert memory == expected_memory, f"Memory failed for {desc}: expected {expected_memory}, got {memory}"

    print(f"✓ All {len(edge_cases)} edge cases passed!")


def test_sample_lines():
    """Test sample lines from actual input."""
    print("\n=== Testing Sample Lines from Input ===")
    # Read actual lines from input and test specific line numbers
    lines = read_input('input.md')
    samples = [
        (lines[1], "line 2"),  # Line 2 (0-indexed as 1)
        (lines[7], "line 8"),  # Line 8 (0-indexed as 7)
        (lines[75], "line 76"), # Line 76 (0-indexed as 75)
    ]

    for line, desc in samples:
        code = count_code_chars(line)
        memory = count_memory_chars(line)
        print(f"  {desc}: {line[:30]}... -> code={code}, memory={memory}, diff={code-memory}")
        print(f"  ✓ {desc} processed")

    print("✓ Sample lines from actual input processed!")

    # Now test with manually crafted cases we can verify
    print("\n=== Testing Manually Crafted Cases ===")
    manual_samples = [
        (r'"v\xfb\"lgs\"kvjfywmut\x9cr"', 28, 18, "manual hex+quote test"),
        (r'"kbngyfvvsdismznhar\\p\"\"gpryt\"jaeh"', 38, 32, "manual backslash+quote test"),
    ]

    for line, expected_code, expected_memory, desc in manual_samples:
        code = count_code_chars(line)
        memory = count_memory_chars(line)
        print(f"  {desc}: code={code} (expected {expected_code}), "
              f"memory={memory} (expected {expected_memory})")
        assert code == expected_code, f"Code mismatch for {desc}"
        assert memory == expected_memory, f"Memory mismatch for {desc}"
        print(f"  ✓ {desc} verified")

    print("✓ All manually crafted test cases verified!")


def test_full_input():
    """Test against full input."""
    print("\n=== Testing Full Input ===")
    lines = read_input('input.md')

    # Verify we read the correct number of lines
    print(f"  Read {len(lines)} lines")
    assert len(lines) == 300, f"Expected 300 lines, got {len(lines)}"

    # Calculate result
    result = calculate_difference(lines)

    # Sanity check the result
    assert isinstance(result, int), "Result should be an integer"
    print(f"  Final result: {result}")

    # Check if in expected range
    if 1200 <= result <= 1800:
        print(f"  ✓ Result is within expected range [1200, 1800]")
    else:
        print(f"  ⚠ Result {result} is outside expected range [1200, 1800] (may still be correct)")

    return result


if __name__ == '__main__':
    test_examples()
    test_edge_cases()
    test_sample_lines()
    result = test_full_input()
    print(f"\n{'='*50}")
    print(f"FINAL ANSWER: {result}")
    print(f"{'='*50}")
