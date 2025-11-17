from solution import (
    increment_password,
    has_increasing_straight,
    has_forbidden_chars,
    has_two_pairs,
    is_valid_password,
    skip_forbidden_chars,
    find_next_password
)


def test_increment_password():
    print("Testing increment_password...")
    assert increment_password('abcdefgh') == 'abcdefgi'
    assert increment_password('abcdefgz') == 'abcdefha'
    assert increment_password('abcdezzz') == 'abcdfaaa'
    assert increment_password('abcdefzz') == 'abcdegaa'
    assert increment_password('azzzzzzz') == 'baaaaaaa'
    assert increment_password('zzzzzzzz') == 'aaaaaaaa'
    print("✓ All increment_password tests passed")


def test_has_increasing_straight():
    print("\nTesting has_increasing_straight...")
    assert has_increasing_straight('abcdefgh') == True
    assert has_increasing_straight('abxdefgh') == True
    assert has_increasing_straight('xxxabcxx') == True
    assert has_increasing_straight('xxxxxxab') == False
    assert has_increasing_straight('abxdxfxh') == False
    assert has_increasing_straight('xyzxxxxx') == True
    print("✓ All has_increasing_straight tests passed")


def test_has_forbidden_chars():
    print("\nTesting has_forbidden_chars...")
    assert has_forbidden_chars('abcdefgh') == False
    assert has_forbidden_chars('abciefgh') == True
    assert has_forbidden_chars('abcoefgh') == True
    assert has_forbidden_chars('abclefgh') == True
    assert has_forbidden_chars('ghijklmn') == True
    assert has_forbidden_chars('aaaaaaaa') == False
    print("✓ All has_forbidden_chars tests passed")


def test_has_two_pairs():
    print("\nTesting has_two_pairs...")
    assert has_two_pairs('abcdffaa') == True
    assert has_two_pairs('abbceffg') == True
    assert has_two_pairs('aabbccdd') == True
    assert has_two_pairs('abbcdefg') == False
    assert has_two_pairs('abcdefgh') == False
    assert has_two_pairs('aaaa') == False  # Same letter
    assert has_two_pairs('aaaabbbb') == True  # 'aa' and 'bb'
    assert has_two_pairs('aabcdefg') == False  # only one pair
    print("✓ All has_two_pairs tests passed")


def test_skip_forbidden_chars():
    print("\nTesting skip_forbidden_chars...")
    assert skip_forbidden_chars('abciefgh') == 'abcjaaaa'
    assert skip_forbidden_chars('ghijklmn') == 'ghjaaaaa'
    assert skip_forbidden_chars('abcoefgh') == 'abcpaaaa'
    assert skip_forbidden_chars('abclefgh') == 'abcmaaaa'
    assert skip_forbidden_chars('aaaaaaai') == 'aaaaaaaj'
    print("✓ All skip_forbidden_chars tests passed")


def test_is_valid_password():
    print("\nTesting is_valid_password...")
    assert is_valid_password('hijklmmn') == False  # Has forbidden chars
    assert is_valid_password('abbceffg') == False  # No straight
    assert is_valid_password('abbcegjk') == False  # Only one pair
    assert is_valid_password('abcdffaa') == True   # All requirements met
    assert is_valid_password('ghjaabcc') == True   # All requirements met
    print("✓ All is_valid_password tests passed")


def test_find_next_password_examples():
    print("\nTesting find_next_password with Part One examples...")
    print("Testing: 'abcdefgh' -> expected 'abcdffaa'")
    result1 = find_next_password('abcdefgh')
    print(f"  Result: {result1}")
    assert result1 == 'abcdffaa', f"Expected 'abcdffaa', got '{result1}'"

    print("Testing: 'ghijklmn' -> expected 'ghjaabcc'")
    result2 = find_next_password('ghijklmn')
    print(f"  Result: {result2}")
    assert result2 == 'ghjaabcc', f"Expected 'ghjaabcc', got '{result2}'"

    print("✓ All find_next_password tests passed")


if __name__ == '__main__':
    test_increment_password()
    test_has_increasing_straight()
    test_has_forbidden_chars()
    test_has_two_pairs()
    test_skip_forbidden_chars()
    test_is_valid_password()
    test_find_next_password_examples()
    print("\n" + "="*50)
    print("All tests passed successfully!")
    print("="*50)
