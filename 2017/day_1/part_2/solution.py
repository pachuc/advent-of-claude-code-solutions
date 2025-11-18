def solve_captcha(digits: str) -> int:
    """
    Calculate the sum of all digits that match the digit halfway around
    the circular sequence.

    Args:
        digits: A string of numeric digits (must have even length)

    Returns:
        The sum of all digits that match their halfway-around counterpart
    """
    total_sum = 0
    n = len(digits)
    step = n // 2  # Halfway point (guaranteed to be integer)

    for i in range(n):
        halfway_i = (i + step) % n
        if digits[i] == digits[halfway_i]:
            total_sum += int(digits[i])

    return total_sum


def test_provided_examples():
    """Test the provided examples from the problem statement."""
    print("Testing provided examples...")

    assert solve_captcha("1212") == 6, \
        f"Example 1 failed: Expected 6, got {solve_captcha('1212')}"
    print("  ✓ Example 1: '1212' -> 6")

    assert solve_captcha("1221") == 0, \
        f"Example 2 failed: Expected 0, got {solve_captcha('1221')}"
    print("  ✓ Example 2: '1221' -> 0")

    assert solve_captcha("123425") == 4, \
        f"Example 3 failed: Expected 4, got {solve_captcha('123425')}"
    print("  ✓ Example 3: '123425' -> 4")

    assert solve_captcha("123123") == 12, \
        f"Example 4 failed: Expected 12, got {solve_captcha('123123')}"
    print("  ✓ Example 4: '123123' -> 12")

    assert solve_captcha("12131415") == 4, \
        f"Example 5 failed: Expected 4, got {solve_captcha('12131415')}"
    print("  ✓ Example 5: '12131415' -> 4")

    print("✓ All provided examples passed")


def test_length_variations():
    """Test different sequence lengths."""
    print("Testing length variations...")

    assert solve_captcha("12") == 0, "Minimum even (no match) failed"
    print("  ✓ Length 2 (no match): '12' -> 0")

    assert solve_captcha("11") == 2, "Minimum even (match) failed"
    print("  ✓ Length 2 (match): '11' -> 2")

    assert solve_captcha("5555") == 20, "Length 4 all same failed"
    print("  ✓ Length 4 (all same): '5555' -> 20")

    assert solve_captcha("121212") == 0, "Length 6 alternating failed"
    print("  ✓ Length 6 (alternating): '121212' -> 0")

    assert solve_captcha("12341234") == 20, "Length 8 pattern failed"
    print("  ✓ Length 8 (pattern): '12341234' -> 20")

    assert solve_captcha("1234512345") == 30, "Length 10 pattern failed"
    print("  ✓ Length 10 (pattern): '1234512345' -> 30")

    print("✓ All length variation tests passed")


def test_digit_patterns():
    """Test specific digit patterns."""
    print("Testing digit patterns...")

    assert solve_captcha("0000") == 0, "All zeros failed"
    print("  ✓ All zeros: '0000' -> 0")

    assert solve_captcha("9999") == 36, "All nines failed"
    print("  ✓ All nines: '9999' -> 36")

    assert solve_captcha("12345678") == 0, "No matches failed"
    print("  ✓ No matches: '12345678' -> 0")

    assert solve_captcha("10000001") == 0, "Zeros only match failed"
    print("  ✓ Zeros only match: '10000001' -> 0")

    assert solve_captcha("12344321") == 0, "Palindrome pattern failed"
    print("  ✓ Palindrome pattern: '12344321' -> 0")

    print("✓ All digit pattern tests passed")


def test_symmetric_matching():
    """Verify symmetric matching behavior."""
    print("Testing symmetric matching...")

    # Detailed walkthrough for '1212':
    # Position 0 ('1') vs Position 2 ('1') -> match, add 1
    # Position 1 ('2') vs Position 3 ('2') -> match, add 2
    # Position 2 ('1') vs Position 0 ('1') -> match, add 1
    # Position 3 ('2') vs Position 1 ('2') -> match, add 2
    # Total: 6 (each matching pair contributes twice)

    result = solve_captcha("1212")
    assert result == 6, f"Symmetric matching failed: expected 6, got {result}"
    print("  ✓ Symmetric matching verified: '1212' -> 6")
    print("    (Each position matches its halfway counterpart)")

    print("✓ Symmetric matching test passed")


def test_circular_wrapping():
    """Test circular wrapping at boundaries."""
    print("Testing circular wrapping...")

    assert solve_captcha("123423") == 10, "Wrap test 1 failed"
    print("  ✓ Wrap test 1: '123423' -> 10")

    assert solve_captcha("12121212") == 12, "Wrap test 2 failed"
    print("  ✓ Wrap test 2: '12121212' -> 12")

    print("✓ All circular wrapping tests passed")


def run_tests():
    """Run all test cases to verify the solution."""
    print("=" * 60)
    print("RUNNING COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print()

    print("=== Category 1: Provided Examples ===")
    test_provided_examples()
    print()

    print("=== Category 2: Length Variations ===")
    test_length_variations()
    print()

    print("=== Category 3: Digit Patterns ===")
    test_digit_patterns()
    print()

    print("=== Category 4: Symmetric Matching ===")
    test_symmetric_matching()
    print()

    print("=== Category 5: Circular Wrapping ===")
    test_circular_wrapping()
    print()

    print("=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    # Run tests first to validate logic
    run_tests()

    # Read and solve the actual input
    print("\n" + "=" * 60)
    print("SOLVING ACTUAL INPUT")
    print("=" * 60)

    with open("input.md", "r") as f:
        content = f.read()

    digits = content.strip()

    # Verify input properties
    print(f"Input length: {len(digits)}")
    print(f"Step size (halfway): {len(digits) // 2}")
    assert len(digits) % 2 == 0, "Input must have even length"
    print("✓ Input has even length")
    print()

    # Calculate result
    print("Calculating result...")
    result = solve_captcha(digits)

    print()
    print("=" * 60)
    print(f"RESULT: {result}")
    print("=" * 60)
