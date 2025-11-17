def has_non_overlapping_pair(s: str) -> bool:
    """
    Check if string contains a pair of two letters that appears at least twice
    without overlapping.

    Example: 'xyxy' has 'xy' appearing twice without overlapping -> True
             'aaa' has 'aa' but it overlaps -> False
    """
    for i in range(len(s) - 1):
        pair = s[i:i+2]
        # Search for the same pair starting from i+2 to avoid overlap
        if pair in s[i+2:]:
            return True
    return False


def has_repeat_with_one_between(s: str) -> bool:
    """
    Check if string contains at least one letter which repeats with exactly
    one letter between them.

    Example: 'xyx' has 'x' repeating with 'y' between -> True
             'aaa' has 'a' repeating with 'a' between -> True
    """
    for i in range(len(s) - 2):
        if s[i] == s[i+2]:
            return True
    return False


def is_nice(s: str) -> bool:
    """
    Check if a string is 'nice' - must satisfy BOTH conditions:
    1. Has a non-overlapping pair
    2. Has a letter that repeats with one between
    """
    return has_non_overlapping_pair(s) and has_repeat_with_one_between(s)


def test():
    """Run test cases to verify the implementation"""
    print("Testing has_non_overlapping_pair...")
    # Basic cases
    assert has_non_overlapping_pair("xyxy") == True, "Failed: xyxy"
    assert has_non_overlapping_pair("aabcdefgaa") == True, "Failed: aabcdefgaa"
    assert has_non_overlapping_pair("aaa") == False, "Failed: aaa"
    assert has_non_overlapping_pair("abcdefgh") == False, "Failed: abcdefgh"
    assert has_non_overlapping_pair("aaaa") == True, "Failed: aaaa"
    assert has_non_overlapping_pair("abcabc") == True, "Failed: abcabc"
    assert has_non_overlapping_pair("xyyx") == False, "Failed: xyyx"
    assert has_non_overlapping_pair("abc") == False, "Failed: abc"
    assert has_non_overlapping_pair("abcdefab") == True, "Failed: abcdefab"
    print("✓ All has_non_overlapping_pair tests passed")

    print("\nTesting has_repeat_with_one_between...")
    # Basic cases
    assert has_repeat_with_one_between("xyx") == True, "Failed: xyx"
    assert has_repeat_with_one_between("abcdefeghi") == True, "Failed: abcdefeghi"
    assert has_repeat_with_one_between("aaa") == True, "Failed: aaa"
    assert has_repeat_with_one_between("abcdef") == False, "Failed: abcdef"
    assert has_repeat_with_one_between("aba") == True, "Failed: aba"
    assert has_repeat_with_one_between("xyzaz") == True, "Failed: xyzaz"
    assert has_repeat_with_one_between("abacad") == True, "Failed: abacad"
    assert has_repeat_with_one_between("ab") == False, "Failed: ab"
    assert has_repeat_with_one_between("abca") == False, "Failed: abca"
    print("✓ All has_repeat_with_one_between tests passed")

    print("\nTesting is_nice (integration)...")
    # Provided examples
    assert is_nice("qjhvhtzxzqqjkmpb") == True, "Failed: qjhvhtzxzqqjkmpb (should be nice)"
    assert is_nice("xxyxx") == True, "Failed: xxyxx (should be nice)"
    assert is_nice("uurcxstgmygtbstg") == False, "Failed: uurcxstgmygtbstg (should be naughty)"
    assert is_nice("ieodomkazucvgmuy") == False, "Failed: ieodomkazucvgmuy (should be naughty)"

    # Additional edge cases
    assert is_nice("abcdefgh") == False, "Failed: abcdefgh"
    assert is_nice("") == False, "Failed: empty string"
    assert is_nice("a") == False, "Failed: single character"
    assert is_nice("xyxyx") == True, "Failed: xyxyx"
    assert is_nice("aaaaaaa") == True, "Failed: aaaaaaa"
    assert is_nice("ababab") == True, "Failed: ababab"
    print("✓ All integration tests passed")

    print("\n✅ All tests passed!")


def main():
    """Main function to read input and count nice strings"""
    with open('input.md', 'r') as f:
        lines = f.read().strip().split('\n')

    nice_count = 0
    for line in lines:
        line = line.strip()
        if line and is_nice(line):
            nice_count += 1

    print(nice_count)


if __name__ == "__main__":
    # Run tests first
    test()
    print("\n" + "="*50)
    print("Running solution on input.md...")
    print("="*50 + "\n")
    # Run main solution
    main()
