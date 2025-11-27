#!/usr/bin/env python3
"""Test verification for the Regular Map solution."""

from solution import solve

# Test cases from problem statement
test_cases = [
    ("^WNE$", 3),
    ("^ENWWW(NEEE|SSE(EE|N))$", 10),
    ("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18),
    ("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23),
    ("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31),
]

# Additional edge case tests
edge_cases = [
    ("^$", 0),  # Empty regex
    ("^N$", 1),  # Single direction
    ("^NNN$", 3),  # Multiple same direction
    ("^N(E|W)N$", 3),  # Simple two-way branch
]

def run_tests():
    """Run all test cases and report results."""
    print("=" * 60)
    print("Testing Provided Examples")
    print("=" * 60)

    all_passed = True
    for i, (regex, expected) in enumerate(test_cases, 1):
        result = solve(regex)
        passed = result == expected
        all_passed = all_passed and passed

        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Example {i}: {status}")
        if not passed:
            print(f"  Expected: {expected}")
            print(f"  Got:      {result}")
            print(f"  Input:    {regex[:50]}{'...' if len(regex) > 50 else ''}")

    print()
    print("=" * 60)
    print("Testing Edge Cases")
    print("=" * 60)

    for i, (regex, expected) in enumerate(edge_cases, 1):
        result = solve(regex)
        passed = result == expected
        all_passed = all_passed and passed

        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Edge Case {i}: {status}")
        if not passed:
            print(f"  Expected: {expected}")
            print(f"  Got:      {result}")
            print(f"  Input:    {regex}")

    print()
    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    run_tests()
