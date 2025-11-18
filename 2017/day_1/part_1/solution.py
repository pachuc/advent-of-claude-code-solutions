def solve_captcha(digits: str) -> int:
    """
    Calculate the sum of all digits that match the next digit in a circular sequence.

    Args:
        digits: A string of numeric digits

    Returns:
        The sum of all digits that match their next neighbor (circular)
    """
    total_sum = 0
    n = len(digits)

    for i in range(n):
        next_i = (i + 1) % n
        if digits[i] == digits[next_i]:
            total_sum += int(digits[i])

    return total_sum


def run_tests():
    """Run all test cases to verify the solution."""
    print("Running tests...")

    # Provided examples
    assert solve_captcha("1122") == 3, "Example 1 failed"
    assert solve_captcha("1111") == 4, "Example 2 failed"
    assert solve_captcha("1234") == 0, "Example 3 failed"
    assert solve_captcha("91212129") == 9, "Example 4 failed"
    print("✓ All provided examples passed")

    # Edge cases
    assert solve_captcha("5") == 5, "Single digit test failed"
    assert solve_captcha("7") == 7, "Single digit variant failed"
    assert solve_captcha("88") == 16, "Two matching digits failed"
    assert solve_captcha("12") == 0, "Two non-matching digits failed"
    assert solve_captcha("9999999999") == 90, "All same digit failed"
    assert solve_captcha("123456789") == 0, "No matches failed"
    assert solve_captcha("5123125") == 5, "Only circular match failed"
    assert solve_captcha("121212") == 0, "Alternating pattern failed"
    assert solve_captcha("001100") == 1, "Zero digits failed"
    assert solve_captcha("1112223333") == 15, "Multiple consecutive matches failed"
    assert solve_captcha("11") == 2, "No double counting test failed"
    print("✓ All edge case tests passed")

    print("\nAll tests passed!")


if __name__ == "__main__":
    # Run tests first
    run_tests()

    # Read and solve the actual input
    print("\nSolving actual input...")
    with open("input.md", "r") as f:
        content = f.read()

    digits = content.strip()
    result = solve_captcha(digits)

    print(f"\nResult: {result}")
