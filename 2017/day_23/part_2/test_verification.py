#!/usr/bin/env python3
"""
Comprehensive test suite for Part 2 solution verification.
Based on the testing plan in test_plan.md
"""

from solution import is_composite, count_composites

def test_primality_known_primes():
    """Test 1.1: Known Prime Numbers"""
    print("Test 1.1: Known Prime Numbers")
    test_cases = [2, 3, 5, 7, 11, 97, 997]
    for n in test_cases:
        result = is_composite(n)
        assert result == False, f"Expected {n} to be prime (not composite), but got composite"
        print(f"  ✓ {n} is correctly identified as prime")
    print("  PASSED\n")

def test_primality_known_composites():
    """Test 1.2: Known Composite Numbers"""
    print("Test 1.2: Known Composite Numbers")
    test_cases = [4, 6, 8, 9, 15, 100, 1000]
    for n in test_cases:
        result = is_composite(n)
        assert result == True, f"Expected {n} to be composite, but got prime"
        print(f"  ✓ {n} is correctly identified as composite")
    print("  PASSED\n")

def test_primality_edge_cases():
    """Test 1.3: Edge Cases"""
    print("Test 1.3: Edge Cases")
    assert is_composite(0) == True, "0 should be considered composite"
    print("  ✓ 0 is correctly identified as composite")
    assert is_composite(1) == True, "1 should be considered composite"
    print("  ✓ 1 is correctly identified as composite")
    print("  PASSED\n")

def test_primality_large_numbers():
    """Test 1.4: Large Numbers in Target Range"""
    print("Test 1.4: Large Numbers in Target Range")
    # Verified composite numbers in the target range
    test_cases = [106700, 106702, 106704]  # Even numbers are guaranteed composite
    for n in test_cases:
        result = is_composite(n)
        assert result == True, f"Expected {n} to be composite"
        print(f"  ✓ {n} is correctly identified as composite")

    # Also test a known prime in the range
    assert is_composite(106721) == False, "106721 should be prime"
    print(f"  ✓ 106721 is correctly identified as prime")
    print("  PASSED\n")

def test_range_count():
    """Test 3.1: Count Calculation"""
    print("Test 3.1: Count Calculation")
    b = 106700
    c = 123700
    step = 17

    count = 0
    current = b
    while current <= c:
        count += 1
        current += step

    assert count == 1001, f"Expected 1001 values, got {count}"
    print(f"  ✓ Exactly 1001 numbers in range [106700, 123700] with step 17")
    print("  PASSED\n")

def test_range_boundaries():
    """Test 3.2: Range Boundaries"""
    print("Test 3.2: Range Boundaries")
    values_checked = []
    current = 106700
    while current <= 123700:
        values_checked.append(current)
        current += 17

    assert values_checked[0] == 106700, f"First value should be 106700, got {values_checked[0]}"
    print(f"  ✓ First value is 106700")

    assert values_checked[-1] == 123700, f"Last value should be 123700, got {values_checked[-1]}"
    print(f"  ✓ Last value is 123700")

    assert len(values_checked) == 1001, f"Expected 1001 values, got {len(values_checked)}"
    print(f"  ✓ Total count is 1001")

    assert 123717 not in values_checked, "123717 should not be in the range"
    print(f"  ✓ 123717 is correctly excluded")
    print("  PASSED\n")

def test_range_step_size():
    """Test 3.3: Step Size Correctness"""
    print("Test 3.3: Step Size Correctness")
    current = 106700
    for i in range(10):
        expected = 106700 + i * 17
        assert current == expected, f"At step {i}, expected {expected}, got {current}"
        current += 17
    print(f"  ✓ First 10 steps increment correctly by 17")
    print("  PASSED\n")

def test_small_range_manual():
    """Test 4.1: Manual Verification on Small Range"""
    print("Test 4.1: Manual Verification on Small Range")
    # Values: 10, 15, 20, 25, 30 (all composite)
    h = count_composites(10, 30, 5)
    assert h == 5, f"Expected 5 composites, got {h}"
    print(f"  ✓ Correctly counted 5 composites in [10, 30] step 5")
    print("  PASSED\n")

def test_small_range_primes_only():
    """Test 4.2: Range with Only Primes"""
    print("Test 4.2: Range with Only Primes")
    # Values: 2, 3, 5, 7 (all prime)
    # Note: with step 1, we check 2,3,4,5,6,7
    # So actually: 2(prime), 3(prime), 4(composite), 5(prime), 6(composite), 7(prime)
    # Let's use a range with only primes by checking specific values
    # Actually, the test plan has a flaw - let's verify the specific case:
    # [2, 7] with step 1 gives us: 2, 3, 4, 5, 6, 7
    # Composites: 4, 6 -> count = 2, not 0
    # Let me check what the test actually expects...

    # The test plan says 0, but that's incorrect. Let me use the actual logic:
    # 2 (prime), 3 (prime), 4 (composite), 5 (prime), 6 (composite), 7 (prime)
    h = count_composites(2, 7, 1)
    assert h == 2, f"Expected 2 composites (4 and 6), got {h}"
    print(f"  ✓ Correctly counted 2 composites in [2, 7] step 1")
    print("  PASSED\n")

def test_small_range_composites_only():
    """Test 4.3: Range with Only Composites"""
    print("Test 4.3: Range with Only Composites")
    # Values: 4, 6, 8, 10 (all composite)
    h = count_composites(4, 10, 2)
    assert h == 4, f"Expected 4 composites, got {h}"
    print(f"  ✓ Correctly counted 4 composites in [4, 10] step 2")
    print("  PASSED\n")

def test_answer_sanity():
    """Test 5.2: Sanity Check on Final Answer"""
    print("Test 5.2: Sanity Check on Final Answer")
    result = count_composites(106700, 123700, 17)

    assert 0 <= result <= 1001, f"Answer {result} not in valid range [0, 1001]"
    print(f"  ✓ Answer {result} is within valid range [0, 1001]")

    assert result > 900, f"Answer {result} is too low (expected >900 based on prime density)"
    print(f"  ✓ Answer {result} is >900 (consistent with ~90%+ composite rate)")

    assert result < 1001, f"Answer {result} should be <1001 (some primes should exist)"
    print(f"  ✓ Answer {result} is <1001 (indicating some primes exist)")

    print("  PASSED\n")
    return result

def test_cross_reference_sympy():
    """Test 6.2: Cross-Reference with Mathematical Tools"""
    print("Test 6.2: Cross-Reference with sympy")
    try:
        import sympy

        values = range(106700, 123701, 17)
        expected = sum(1 for v in values if not sympy.isprime(v))

        result = count_composites(106700, 123700, 17)

        assert result == expected, f"Our result {result} doesn't match sympy's {expected}"
        print(f"  ✓ Our answer {result} matches sympy's answer {expected}")
        print("  PASSED\n")
        return result
    except ImportError:
        print("  ⚠ sympy not available, skipping this test")
        print("  SKIPPED\n")
        return None

def run_all_tests():
    """Run all tests and report results"""
    print("="*60)
    print("COMPREHENSIVE TEST SUITE FOR PART 2 SOLUTION")
    print("="*60)
    print()

    try:
        # Test 1: Primality Testing
        print("### Category 1: Primality/Composite Testing ###")
        test_primality_known_primes()
        test_primality_known_composites()
        test_primality_edge_cases()
        test_primality_large_numbers()

        # Test 3: Range and Counting Logic
        print("### Category 3: Range and Counting Logic ###")
        test_range_count()
        test_range_boundaries()
        test_range_step_size()

        # Test 4: Small-Scale Validation
        print("### Category 4: Small-Scale Validation ###")
        test_small_range_manual()
        test_small_range_primes_only()
        test_small_range_composites_only()

        # Test 5: Integration Testing
        print("### Category 5: Integration Testing ###")
        answer = test_answer_sanity()

        # Test 6: Algorithm Verification
        print("### Category 6: Algorithm Verification ###")
        sympy_answer = test_cross_reference_sympy()

        # Final Report
        print("="*60)
        print("TEST SUITE RESULTS: ALL TESTS PASSED ✓")
        print("="*60)
        print(f"\nFinal Answer: {answer}")
        if sympy_answer is not None:
            print(f"Verified with sympy: {sympy_answer}")
        print()

        return True, answer

    except AssertionError as e:
        print("="*60)
        print(f"TEST FAILED: {e}")
        print("="*60)
        return False, None
    except Exception as e:
        print("="*60)
        print(f"ERROR DURING TESTING: {e}")
        print("="*60)
        import traceback
        traceback.print_exc()
        return False, None

if __name__ == "__main__":
    success, answer = run_all_tests()
    if not success:
        exit(1)
