from collections import Counter
from solution import read_input, decode_message


def test_input_validation():
    """Validate input file structure."""
    lines = read_input('input.md')
    assert len(lines) == 598, f"Expected 598 lines, got {len(lines)}"

    for i, line in enumerate(lines):
        assert len(line) == 8, f"Line {i} has length {len(line)}, expected 8"
        assert all('a' <= c <= 'z' for c in line), f"Line {i} has invalid characters"

    print("✓ Input validation passed: 598 lines, all 8 characters, all lowercase")


def test_example():
    """Test with provided example."""
    lines = read_input('test_example.txt')
    result = decode_message(lines)
    assert result == "easter", f"Expected 'easter', got '{result}'"
    print("✓ Example test passed: 'easter'")


def test_actual_input():
    """Test with actual input."""
    lines = read_input('input.md')
    result = decode_message(lines)
    assert len(result) == 8, f"Expected length 8, got {len(result)}"
    assert all('a' <= c <= 'z' for c in result), "Invalid characters in output"
    print(f"✓ Actual input test passed: {result}")
    return result


def complete_manual_verification():
    """Manually verify ALL 8 columns - CRITICAL for correctness."""
    lines = read_input('input.md')
    result = decode_message(lines)

    print("\nComplete Manual Verification:")
    print("=" * 60)

    for pos in range(8):
        column = [line[pos] for line in lines]
        freq = Counter(column)
        most_common_char, count = freq.most_common(1)[0]

        # Display top 5 most common for verification
        top_5 = freq.most_common(5)
        freq_str = ", ".join([f"{char}({cnt})" for char, cnt in top_5])

        assert result[pos] == most_common_char, \
            f"Position {pos} failed: expected '{most_common_char}', got '{result[pos]}'"

        print(f"Position {pos}: {freq_str} → '{most_common_char}' ✓")

    print("=" * 60)
    print(f"✓ Complete manual verification passed!")
    print(f"✓ Final answer: {result}")
    return result


def test_single_line():
    """Test with single line."""
    lines = ["testmsg"]
    result = decode_message(lines)
    assert result == "testmsg", f"Expected 'testmsg', got '{result}'"
    print("✓ Single line test passed")


def test_unequal_lines():
    """Test that unequal line lengths raise error."""
    lines = ["abc", "abcd", "ab"]
    try:
        decode_message(lines)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Unequal lines test passed: {e}")


def run_all_tests():
    """Run all tests."""
    print("Running Signal Error Correction Tests...")
    print()
    test_example()
    test_input_validation()
    result = test_actual_input()
    print()
    complete_manual_verification()
    print()
    test_single_line()
    test_unequal_lines()
    print("\n" + "=" * 60)
    print(f"✓ ALL TESTS PASSED!")
    print(f"✓ Final verified answer: {result}")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
