from solution import (
    increment_password,
    has_no_forbidden_chars,
    has_increasing_straight,
    has_two_pairs,
    is_valid_password,
    find_next_password
)

def test_increment():
    """Test the increment_password function."""
    print("Testing increment_password...")

    # Test 1.1: Basic increment
    assert increment_password("aaaaaaaa") == "aaaaaaab", "Test 1.1 failed"
    print("✓ Test 1.1: Basic increment")

    # Test 1.2: Single position carry
    assert increment_password("aaaaaaaz") == "aaaaaaba", "Test 1.2 failed"
    print("✓ Test 1.2: Single position carry")

    # Test 1.3: Multiple position carry
    assert increment_password("aaaaaazz") == "aaaaabaa", "Test 1.3 failed"
    print("✓ Test 1.3: Multiple position carry")

    # Test 1.4: Full carry propagation
    assert increment_password("azzzzzzz") == "baaaaaaa", "Test 1.4 failed"
    print("✓ Test 1.4: Full carry propagation")

    # Test 1.5: Forbidden character skip - 'i' (with carry)
    result = increment_password("aaaaaahz")
    assert result == "aaaaaaja", f"Test 1.5 failed: expected 'aaaaaaja', got '{result}'"
    print("✓ Test 1.5: Forbidden character skip - 'i' (with carry)")

    # Test 1.6: Forbidden character skip - 'o' (with carry)
    result = increment_password("aaaaaanz")
    assert result == "aaaaaapa", f"Test 1.6 failed: expected 'aaaaaapa', got '{result}'"
    print("✓ Test 1.6: Forbidden character skip - 'o' (with carry)")

    # Test 1.7: Forbidden character skip - 'l' (with carry)
    result = increment_password("aaaaaakz")
    assert result == "aaaaaama", f"Test 1.7 failed: expected 'aaaaaama', got '{result}'"
    print("✓ Test 1.7: Forbidden character skip - 'l' (with carry)")

    # Test 1.8: Forbidden character during carry
    result = increment_password("aaahzzzz")
    assert result == "aaajaaaa", f"Test 1.8 failed: expected 'aaajaaaa', got '{result}'"
    print("✓ Test 1.8: Forbidden character during carry propagation")

    print()


def test_forbidden_chars():
    """Test the has_no_forbidden_chars function."""
    print("Testing has_no_forbidden_chars...")

    # Test 2.1: Valid
    assert has_no_forbidden_chars("abcdefgh") == True, "Test 2.1 failed"
    print("✓ Test 2.1: No forbidden chars")

    # Test 2.2: Contains 'i'
    assert has_no_forbidden_chars("abcdefgi") == False, "Test 2.2 failed"
    print("✓ Test 2.2: Contains 'i'")

    # Test 2.3: Contains 'o'
    assert has_no_forbidden_chars("abcdofgh") == False, "Test 2.3 failed"
    print("✓ Test 2.3: Contains 'o'")

    # Test 2.4: Contains 'l'
    assert has_no_forbidden_chars("lbcdefgh") == False, "Test 2.4 failed"
    print("✓ Test 2.4: Contains 'l'")

    # Test 2.5: Multiple forbidden
    assert has_no_forbidden_chars("ioldefgh") == False, "Test 2.5 failed"
    print("✓ Test 2.5: Multiple forbidden chars")

    print()


def test_increasing_straight():
    """Test the has_increasing_straight function."""
    print("Testing has_increasing_straight...")

    # Test 2.6: At beginning
    assert has_increasing_straight("abcdefgh") == True, "Test 2.6 failed"
    print("✓ Test 2.6: Straight at beginning")

    # Test 2.7: At end
    assert has_increasing_straight("aaaaaxyz") == True, "Test 2.7 failed"
    print("✓ Test 2.7: Straight at end")

    # Test 2.8: In middle
    assert has_increasing_straight("aaabcdaa") == True, "Test 2.8 failed"
    print("✓ Test 2.8: Straight in middle")

    # Test 2.9: None present
    assert has_increasing_straight("aabbccdd") == False, "Test 2.9 failed"
    print("✓ Test 2.9: No straight")

    # Test 2.10: Non-consecutive
    assert has_increasing_straight("aaceggaa") == False, "Test 2.10 failed"
    print("✓ Test 2.10: Non-consecutive letters")

    print()


def test_two_pairs():
    """Test the has_two_pairs function."""
    print("Testing has_two_pairs...")

    # Test 2.11: Multiple valid pairs
    assert has_two_pairs("aabbccdd") == True, "Test 2.11 failed"
    print("✓ Test 2.11: Multiple valid pairs")

    # Test 2.12: Exactly two
    assert has_two_pairs("aabbcdee") == True, "Test 2.12 failed"
    print("✓ Test 2.12: Exactly two pairs")

    # Test 2.13: Only one pair
    assert has_two_pairs("aabcdefg") == False, "Test 2.13 failed"
    print("✓ Test 2.13: Only one pair")

    # Test 2.14: Same letter repeated
    assert has_two_pairs("aaaaabcd") == False, "Test 2.14 failed"
    print("✓ Test 2.14: Same letter repeated (only one unique pair)")

    # Test 2.15: Non-overlapping check
    assert has_two_pairs("aaabbbcd") == True, "Test 2.15 failed"
    print("✓ Test 2.15: Triple letters create pairs")

    # Test 2.16: Triple creates one pair
    assert has_two_pairs("aaabcdef") == False, "Test 2.16 failed"
    print("✓ Test 2.16: Triple creates only one pair")

    print()


def test_complete_validation():
    """Test the is_valid_password function."""
    print("Testing is_valid_password...")

    # Test 3.1: Valid password
    assert is_valid_password("abcdffaa") == True, "Test 3.1 failed"
    print("✓ Test 3.1: Valid password - all requirements")

    # Test 3.2: Has forbidden char
    assert is_valid_password("abciefaa") == False, "Test 3.2 failed"
    print("✓ Test 3.2: Invalid - has forbidden char")

    # Test 3.3: No straight
    assert is_valid_password("aabbccdd") == False, "Test 3.3 failed"
    print("✓ Test 3.3: Invalid - no straight")

    # Test 3.4: No pairs
    assert is_valid_password("abcdefgh") == False, "Test 3.4 failed"
    print("✓ Test 3.4: Invalid - no pairs")

    # Test 3.5: Only one pair
    assert is_valid_password("abcdefaa") == False, "Test 3.5 failed"
    print("✓ Test 3.5: Invalid - only one pair")

    print()


def test_end_to_end():
    """Test the find_next_password function with examples."""
    print("Testing find_next_password (end-to-end)...")

    # Test 4.1: Example from problem
    result = find_next_password("abcdefgh")
    assert result == "abcdffaa", f"Test 4.1 failed: expected 'abcdffaa', got '{result}'"
    print("✓ Test 4.1: Example 'abcdefgh' -> 'abcdffaa'")

    # Test 4.2: Example with forbidden characters
    result = find_next_password("ghijklmn")
    assert result == "ghjaabcc", f"Test 4.2 failed: expected 'ghjaabcc', got '{result}'"
    print("✓ Test 4.2: Example 'ghijklmn' -> 'ghjaabcc'")

    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Running Unit Tests")
    print("=" * 60)
    print()

    test_increment()
    test_forbidden_chars()
    test_increasing_straight()
    test_two_pairs()
    test_complete_validation()
    test_end_to_end()

    print("=" * 60)
    print("All tests passed!")
    print("=" * 60)
