#!/usr/bin/env python3
"""Test script to verify safety validation function."""

from solution import is_safe_floor

def test_safety_validation():
    """Test all safety validation cases from test plan."""

    print("Testing safety validation function...")
    tests_passed = 0
    tests_total = 0

    # Test 1: Empty floor - safe
    tests_total += 1
    floor = set()
    result = is_safe_floor(floor)
    expected = True
    if result == expected:
        print(f"✓ Test 1 PASSED: Empty floor is safe")
        tests_passed += 1
    else:
        print(f"✗ Test 1 FAILED: Empty floor - Expected {expected}, got {result}")

    # Test 2: Only generators - safe
    tests_total += 1
    floor = {('A', 'G'), ('B', 'G')}
    result = is_safe_floor(floor)
    expected = True
    if result == expected:
        print(f"✓ Test 2 PASSED: Only generators is safe")
        tests_passed += 1
    else:
        print(f"✗ Test 2 FAILED: Only generators - Expected {expected}, got {result}")

    # Test 3: Only microchips - safe
    tests_total += 1
    floor = {('A', 'M'), ('B', 'M')}
    result = is_safe_floor(floor)
    expected = True
    if result == expected:
        print(f"✓ Test 3 PASSED: Only microchips is safe")
        tests_passed += 1
    else:
        print(f"✗ Test 3 FAILED: Only microchips - Expected {expected}, got {result}")

    # Test 4: Microchip with own generator - safe
    tests_total += 1
    floor = {('A', 'M'), ('A', 'G')}
    result = is_safe_floor(floor)
    expected = True
    if result == expected:
        print(f"✓ Test 4 PASSED: Microchip with own generator is safe")
        tests_passed += 1
    else:
        print(f"✗ Test 4 FAILED: Microchip with own generator - Expected {expected}, got {result}")

    # Test 5: Multiple pairs - safe
    tests_total += 1
    floor = {('A', 'M'), ('A', 'G'), ('B', 'M'), ('B', 'G')}
    result = is_safe_floor(floor)
    expected = True
    if result == expected:
        print(f"✓ Test 5 PASSED: Multiple pairs is safe")
        tests_passed += 1
    else:
        print(f"✗ Test 5 FAILED: Multiple pairs - Expected {expected}, got {result}")

    # Test 6: UNSAFE - Microchip with different generator
    tests_total += 1
    floor = {('A', 'M'), ('B', 'G')}
    result = is_safe_floor(floor)
    expected = False
    if result == expected:
        print(f"✓ Test 6 PASSED: Microchip with different generator is UNSAFE")
        tests_passed += 1
    else:
        print(f"✗ Test 6 FAILED: Microchip with different generator - Expected {expected}, got {result}")

    # Test 7: UNSAFE - Microchip with multiple generators, missing its own
    tests_total += 1
    floor = {('A', 'M'), ('B', 'G'), ('C', 'G')}
    result = is_safe_floor(floor)
    expected = False
    if result == expected:
        print(f"✓ Test 7 PASSED: Unprotected microchip with generators is UNSAFE")
        tests_passed += 1
    else:
        print(f"✗ Test 7 FAILED: Unprotected microchip with generators - Expected {expected}, got {result}")

    # Test 8: UNSAFE - One protected, one unprotected microchip
    tests_total += 1
    floor = {('A', 'M'), ('A', 'G'), ('B', 'M')}
    result = is_safe_floor(floor)
    expected = False
    if result == expected:
        print(f"✓ Test 8 PASSED: Mixed protected/unprotected is UNSAFE")
        tests_passed += 1
    else:
        print(f"✗ Test 8 FAILED: Mixed protected/unprotected - Expected {expected}, got {result}")

    print(f"\n{'='*60}")
    print(f"Safety Tests: {tests_passed}/{tests_total} passed")
    print(f"{'='*60}")

    return tests_passed == tests_total

if __name__ == '__main__':
    success = test_safety_validation()
    exit(0 if success else 1)
