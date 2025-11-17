#!/usr/bin/env python3
"""Comprehensive test suite to verify the Part 2 solution."""

from solution import (
    increment_password,
    has_increasing_straight,
    has_forbidden_chars,
    has_two_pairs,
    is_valid_password,
    find_next_password
)


def test_output_format():
    """Test that output has correct format."""
    print("\n=== Test 1: Output Format ===")
    output = "vzcaabcc"

    # Check length
    assert len(output) == 8, f"Expected length 8, got {len(output)}"
    print(f"✓ Length is 8: {output}")

    # Check lowercase
    assert output.islower(), "Output must be lowercase"
    print(f"✓ All lowercase: {output}")

    # Check alphabetic
    assert output.isalpha(), "Output must be alphabetic"
    print(f"✓ All alphabetic: {output}")

    # Check different from Part 1
    assert output != "vzbxxyzz", "Part 2 answer must differ from Part 1"
    print(f"✓ Different from Part 1: vzbxxyzz -> {output}")

    # Check greater than Part 1 answer
    assert output > "vzbxxyzz", f"{output} should be > 'vzbxxyzz'"
    print(f"✓ Greater than Part 1: vzbxxyzz < {output}")


def test_password_requirements():
    """Test that output meets all three password requirements."""
    print("\n=== Test 2: Password Requirements ===")
    output = "vzcaabcc"

    # Requirement 1: No forbidden chars
    print("\nRequirement 1: No forbidden characters (i, o, l)")
    assert not has_forbidden_chars(output), f"Output should not have forbidden chars: {output}"
    print(f"✓ No 'i', 'o', or 'l' in: {output}")

    # Requirement 2: Has increasing straight
    print("\nRequirement 2: At least one increasing straight (3 consecutive letters)")
    assert has_increasing_straight(output), f"Output should have increasing straight: {output}"

    # Find and display the straight
    for i in range(len(output) - 2):
        if (ord(output[i+1]) == ord(output[i]) + 1 and
            ord(output[i+2]) == ord(output[i+1]) + 1):
            straight = output[i:i+3]
            print(f"✓ Found increasing straight: '{straight}' at positions {i}-{i+2}")
            break

    # Requirement 3: Has two different pairs
    print("\nRequirement 3: At least two different non-overlapping pairs")
    assert has_two_pairs(output), f"Output should have two pairs: {output}"

    # Find and display the pairs
    pairs = []
    i = 0
    while i < len(output) - 1:
        if output[i] == output[i+1]:
            pairs.append((output[i]*2, i))
            i += 2
        else:
            i += 1

    unique_pairs = set(p[0] for p in pairs)
    print(f"✓ Found {len(unique_pairs)} different pairs:")
    for pair, pos in pairs:
        print(f"  - '{pair}' at positions {pos}-{pos+1}")

    assert len(unique_pairs) >= 2, f"Need at least 2 different pairs, found {len(unique_pairs)}"

    # Overall validation
    print("\n=== Overall Validation ===")
    assert is_valid_password(output), f"Output should be valid: {output}"
    print(f"✓ Password '{output}' passes ALL requirements")


def test_part1_regression():
    """Test Part 1 examples to ensure algorithm is correct."""
    print("\n=== Test 3: Part 1 Regression Tests ===")

    # Validation examples
    print("\nValidation examples:")
    assert is_valid_password('hijklmmn') == False, "hijklmmn should be invalid (forbidden chars)"
    print("✓ hijklmmn is invalid (forbidden chars)")

    assert is_valid_password('abbceffg') == False, "abbceffg should be invalid (no straight)"
    print("✓ abbceffg is invalid (no straight)")

    assert is_valid_password('abbcegjk') == False, "abbcegjk should be invalid (one pair only)"
    print("✓ abbcegjk is invalid (one pair only)")

    assert is_valid_password('abcdffaa') == True, "abcdffaa should be valid"
    print("✓ abcdffaa is valid")

    assert is_valid_password('ghjaabcc') == True, "ghjaabcc should be valid"
    print("✓ ghjaabcc is valid")

    # Complete examples
    print("\nComplete examples:")
    result1 = find_next_password('abcdefgh')
    assert result1 == 'abcdffaa', f"Expected 'abcdffaa', got '{result1}'"
    print(f"✓ abcdefgh -> {result1}")

    result2 = find_next_password('ghijklmn')
    assert result2 == 'ghjaabcc', f"Expected 'ghjaabcc', got '{result2}'"
    print(f"✓ ghijklmn -> {result2}")


def test_starting_password():
    """Test that we're starting from the correct password."""
    print("\n=== Test 4: Starting Password ===")
    with open('part_1_answer.txt', 'r') as f:
        start = f.read().strip()

    assert start == 'vzbxxyzz', f"Expected 'vzbxxyzz', got '{start}'"
    print(f"✓ Starting password from Part 1: {start}")

    # Verify it's valid
    assert is_valid_password(start), f"Part 1 answer should be valid: {start}"
    print(f"✓ Part 1 answer is valid")

    # Check it has the expected properties
    print(f"  - Has straight 'xyz' at positions 5-7")
    print(f"  - Has pairs 'xx' and 'zz'")


def test_increment_logic():
    """Test the increment logic works correctly."""
    print("\n=== Test 5: Increment Logic ===")

    # Test basic increment
    assert increment_password('aaaaaaaa') == 'aaaaaaab'
    print("✓ aaaaaaaa -> aaaaaaab")

    # Test wrap-around
    assert increment_password('aaaaaaaz') == 'aaaaaaba'
    print("✓ aaaaaaaz -> aaaaaaba")

    # Test multiple wrap-arounds
    assert increment_password('vzbxxyzz') == 'vzbxxzaa'
    print("✓ vzbxxyzz -> vzbxxzaa")

    # Test all z's
    assert increment_password('zzzzzzzz') == 'aaaaaaaa'
    print("✓ zzzzzzzz -> aaaaaaaa (full wrap)")


def test_solution_end_to_end():
    """Test the complete solution from Part 1 answer."""
    print("\n=== Test 6: End-to-End Solution ===")

    start = 'vzbxxyzz'
    result = find_next_password(start)

    print(f"Input:  {start}")
    print(f"Output: {result}")

    assert result == 'vzcaabcc', f"Expected 'vzcaabcc', got '{result}'"
    print(f"✓ Solution correct: {result}")


def main():
    """Run all tests."""
    print("="*60)
    print("PART 2 SOLUTION VERIFICATION")
    print("="*60)

    try:
        test_starting_password()
        test_increment_logic()
        test_part1_regression()
        test_output_format()
        test_password_requirements()
        test_solution_end_to_end()

        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
        print("\nFinal Answer: vzcaabcc")
        return True
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
