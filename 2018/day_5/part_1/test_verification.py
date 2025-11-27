#!/usr/bin/env python3
"""
Verification test script for polymer reaction solution.
Tests all examples from the problem statement and edge cases.
"""

from solution import reacts, react_polymer

def test_reacts():
    """Test the reacts() function."""
    print("Testing reacts() function...")
    test_cases = [
        (('a', 'A'), True, "Same letter, opposite case"),
        (('A', 'a'), True, "Same letter, opposite case (reversed)"),
        (('b', 'B'), True, "Same letter, opposite case"),
        (('a', 'a'), False, "Same letter, same case"),
        (('A', 'A'), False, "Same letter, same case"),
        (('a', 'b'), False, "Different letters, same case"),
        (('a', 'B'), False, "Different letters, different case"),
        (('Z', 'z'), True, "Same letter, opposite case"),
    ]

    passed = 0
    failed = 0

    for (a, b), expected, description in test_cases:
        result = reacts(a, b)
        if result == expected:
            print(f"  ✓ PASS: {description} - reacts('{a}', '{b}') = {result}")
            passed += 1
        else:
            print(f"  ✗ FAIL: {description} - reacts('{a}', '{b}') = {result}, expected {expected}")
            failed += 1

    print(f"reacts() tests: {passed} passed, {failed} failed\n")
    return failed == 0

def test_examples():
    """Test all examples from the problem statement."""
    print("Testing examples from problem statement...")
    test_cases = [
        ("aA", 0, "Simple single reaction"),
        ("abBA", 0, "Chain reaction"),
        ("abAB", 4, "No reactions possible"),
        ("aabAAB", 6, "Same polarity units"),
        ("dabAcCaCBAcCcaDA", 10, "Complex reduction"),
    ]

    passed = 0
    failed = 0

    for polymer, expected, description in test_cases:
        result = react_polymer(polymer)
        if result == expected:
            print(f"  ✓ PASS: {description}")
            print(f"    Input: '{polymer}' -> Output: {result}")
            passed += 1
        else:
            print(f"  ✗ FAIL: {description}")
            print(f"    Input: '{polymer}' -> Output: {result} (expected {expected})")
            _, final = react_polymer(polymer, return_polymer=True)
            print(f"    Final polymer: '{final}'")
            failed += 1

    print(f"Example tests: {passed} passed, {failed} failed\n")
    return failed == 0

def test_edge_cases():
    """Test edge cases."""
    print("Testing edge cases...")
    test_cases = [
        ("", 0, "Empty string"),
        ("a", 1, "Single character"),
        ("aa", 2, "Two characters, same case"),
        ("aAaAaA", 0, "All units react (long chain)"),
        ("AaAaAa", 0, "All units react (reversed)"),
        ("aAbBcC", 0, "Alternating non-reactive"),
        ("abcCBA", 0, "Complete cascading reaction"),
        ("xabBAy", 2, "Partial cascading"),
        ("aBcDeFg", 7, "No reactions at all"),
        ("aAbBcCdD", 0, "Multiple separate reactions"),
        ("aBbCcDdEeFfG", 2, "Order preservation (should be 'aG')"),
    ]

    passed = 0
    failed = 0

    for polymer, expected, description in test_cases:
        result = react_polymer(polymer)
        if result == expected:
            print(f"  ✓ PASS: {description}")
            print(f"    Input: '{polymer}' -> Output: {result}")
            passed += 1
        else:
            print(f"  ✗ FAIL: {description}")
            print(f"    Input: '{polymer}' -> Output: {result} (expected {expected})")
            _, final = react_polymer(polymer, return_polymer=True)
            print(f"    Final polymer: '{final}'")
            failed += 1

    print(f"Edge case tests: {passed} passed, {failed} failed\n")
    return failed == 0

def verify_order_preservation():
    """Verify that the order of non-reactive units is preserved."""
    print("Verifying order preservation...")
    polymer = "aBbCcDdEeFfG"
    _, final = react_polymer(polymer, return_polymer=True)

    if final == "aG":
        print(f"  ✓ PASS: Order preserved correctly")
        print(f"    Input: '{polymer}' -> Final: '{final}'")
        return True
    else:
        print(f"  ✗ FAIL: Order not preserved")
        print(f"    Input: '{polymer}' -> Final: '{final}' (expected 'aG')")
        return False

def verify_no_reactions_in_final(test_cases):
    """Verify that the final polymer has no reactive adjacent pairs."""
    print("Verifying no reactive pairs in final polymer...")
    passed = 0
    failed = 0

    for polymer, _, description in test_cases:
        _, final = react_polymer(polymer, return_polymer=True)

        # Check for reactive adjacent pairs
        has_reactive_pair = False
        for i in range(len(final) - 1):
            if reacts(final[i], final[i+1]):
                has_reactive_pair = True
                print(f"  ✗ FAIL: {description}")
                print(f"    Found reactive pair at positions {i},{i+1}: '{final[i]}{final[i+1]}'")
                print(f"    Final polymer: '{final}'")
                failed += 1
                break

        if not has_reactive_pair:
            passed += 1

    if failed == 0:
        print(f"  ✓ All final polymers have no reactive pairs")

    print(f"No-reaction verification: {passed} passed, {failed} failed\n")
    return failed == 0

def main():
    """Run all verification tests."""
    print("=" * 70)
    print("POLYMER REACTION SOLUTION VERIFICATION")
    print("=" * 70)
    print()

    all_passed = True

    # Test reacts function
    if not test_reacts():
        all_passed = False

    # Test examples
    if not test_examples():
        all_passed = False

    # Test edge cases
    if not test_edge_cases():
        all_passed = False

    # Verify order preservation
    if not verify_order_preservation():
        all_passed = False

    print()

    # Verify no reactions in final polymers
    all_test_cases = [
        ("aA", 0, "Simple single reaction"),
        ("abBA", 0, "Chain reaction"),
        ("abAB", 4, "No reactions possible"),
        ("aabAAB", 6, "Same polarity units"),
        ("dabAcCaCBAcCcaDA", 10, "Complex reduction"),
        ("", 0, "Empty string"),
        ("a", 1, "Single character"),
        ("xabBAy", 2, "Partial cascading"),
        ("aBcDeFg", 7, "No reactions at all"),
    ]

    if not verify_no_reactions_in_final(all_test_cases):
        all_passed = False

    print("=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED - Solution is correct!")
    else:
        print("✗ SOME TESTS FAILED - Solution has issues")
    print("=" * 70)

    return all_passed

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
