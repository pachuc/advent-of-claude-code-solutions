from solution import solve


def test_provided_examples():
    """Test all provided examples from the problem statement."""

    test_cases = [
        ("^WNE$", 3, "Example 1: Simple path"),
        ("^ENWWW(NEEE|SSE(EE|N))$", 10, "Example 2: Nested branches"),
        ("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18, "Example 3: Multiple empty branches"),
        ("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23, "Example 4: Complex nested"),
        ("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31, "Example 5: Deep nesting"),
    ]

    all_passed = True
    for i, (input_str, expected, description) in enumerate(test_cases, 1):
        result = solve(input_str)
        passed = result == expected
        all_passed = all_passed and passed

        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Test {i}: {status}")
        print(f"  Description: {description}")
        print(f"  Input: {input_str}")
        print(f"  Expected: {expected}")
        print(f"  Got: {result}")
        print()

    return all_passed


def test_simple_cases():
    """Test simple edge cases."""

    test_cases = [
        ("^N$", 1, "Single direction"),
        ("^NNN$", 3, "Multiple same direction"),
        ("^$", 0, "Empty regex"),
        ("^N(E|W)N$", 3, "Simple two-way branch"),
    ]

    all_passed = True
    for i, (input_str, expected, description) in enumerate(test_cases, 1):
        result = solve(input_str)
        passed = result == expected
        all_passed = all_passed and passed

        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Simple Test {i}: {status}")
        print(f"  Description: {description}")
        print(f"  Input: {input_str}")
        print(f"  Expected: {expected}")
        print(f"  Got: {result}")
        print()

    return all_passed


if __name__ == '__main__':
    print("=" * 60)
    print("TESTING SIMPLE CASES")
    print("=" * 60)
    simple_passed = test_simple_cases()

    print("\n" + "=" * 60)
    print("TESTING PROVIDED EXAMPLES")
    print("=" * 60)
    examples_passed = test_provided_examples()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if simple_passed and examples_passed:
        print("✓ All tests passed!")
    else:
        if not simple_passed:
            print("✗ Some simple tests failed")
        if not examples_passed:
            print("✗ Some example tests failed")
