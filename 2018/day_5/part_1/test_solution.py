#!/usr/bin/env python3
"""Test script for polymer reaction solution."""

from solution import reacts, react_polymer


def run_tests():
    """Run all test cases and report results."""
    test_cases = [
        ("aA", 0, "Simple single reaction"),
        ("abBA", 0, "Chain reaction"),
        ("abAB", 4, "No reactions possible"),
        ("aabAAB", 6, "Same polarity units"),
        ("dabAcCaCBAcCcaDA", 10, "Complex reduction"),
        ("", 0, "Empty string"),
        ("a", 1, "Single character"),
        ("aAaAaA", 0, "All units react"),
        ("aAbBcC", 0, "Alternating reactions"),
        ("aBbCcDdEeFfG", 2, "Order preservation"),
        ("abcCBA", 0, "Complete cascading"),
        ("xabBAy", 2, "Partial cascading"),
        ("aBcDeFg", 7, "No reactions at all"),
        ("aa", 2, "Same case, no reaction"),
        ("AaAaAa", 0, "All units react (reversed)"),
    ]

    passed = 0
    failed = 0

    print("Running test cases...\n")

    for polymer, expected, description in test_cases:
        result = react_polymer(polymer)
        if result == expected:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1

        print(f"{status}: {description}")
        print(f"  Input: '{polymer}' -> Output: {result} (expected {expected})")

        if result != expected:
            # Show final polymer for debugging
            _, final = react_polymer(polymer, return_polymer=True)
            print(f"  Final polymer: '{final}'")
        print()

    print(f"\nResults: {passed} passed, {failed} failed")

    # Test the reacts function separately
    print("\n" + "="*60)
    print("Testing reacts() function:")
    print("="*60)

    reaction_tests = [
        (('a', 'A'), True, "a and A should react"),
        (('A', 'a'), True, "A and a should react"),
        (('b', 'B'), True, "b and B should react"),
        (('a', 'a'), False, "a and a should not react"),
        (('A', 'A'), False, "A and A should not react"),
        (('a', 'b'), False, "a and b should not react"),
        (('a', 'B'), False, "a and B should not react"),
        (('Z', 'z'), True, "Z and z should react"),
    ]

    reaction_passed = 0
    reaction_failed = 0

    for (char1, char2), expected, description in reaction_tests:
        result = reacts(char1, char2)
        if result == expected:
            status = "✓ PASS"
            reaction_passed += 1
        else:
            status = "✗ FAIL"
            reaction_failed += 1
        print(f"{status}: {description} - reacts('{char1}', '{char2}') = {result}")

    print(f"\nReaction tests: {reaction_passed} passed, {reaction_failed} failed")

    return failed == 0 and reaction_failed == 0


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
