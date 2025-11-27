#!/usr/bin/env python3
"""
Comprehensive test suite for Day 19 Part 2
"""

from solution import (
    parse_input,
    sum_of_divisors,
    extract_target_number,
    verify_algorithm_with_part1,
    create_opcode_functions
)


def test_sum_of_divisors():
    """Test sum of divisors with known values"""
    print("\n[Test 1] Sum of Divisors - Basic Cases")
    print("-" * 60)

    # Basic cases
    assert sum_of_divisors(1) == 1, "Failed for n=1"
    print("  sum_of_divisors(1) = 1")

    assert sum_of_divisors(6) == 12, "Failed for n=6 (1+2+3+6)"
    print("  sum_of_divisors(6) = 12 (1+2+3+6)")

    assert sum_of_divisors(12) == 28, "Failed for n=12"
    print("  sum_of_divisors(12) = 28 (1+2+3+4+6+12)")

    assert sum_of_divisors(28) == 56, "Failed for n=28"
    print("  sum_of_divisors(28) = 56")

    print("\n[Test 2] Sum of Divisors - Perfect Squares")
    print("-" * 60)

    # Perfect squares (CRITICAL - avoid double-counting)
    assert sum_of_divisors(16) == 31, "Failed for n=16 (perfect square)"
    print("  sum_of_divisors(16) = 31 (1+2+4+8+16)")

    assert sum_of_divisors(25) == 31, "Failed for n=25 (perfect square)"
    print("  sum_of_divisors(25) = 31 (1+5+25)")

    assert sum_of_divisors(100) == 217, "Failed for n=100 (perfect square)"
    print("  sum_of_divisors(100) = 217")

    print("\n[Test 3] Sum of Divisors - Prime Numbers")
    print("-" * 60)

    # Prime numbers (sum should be n+1)
    assert sum_of_divisors(7) == 8, "Failed for n=7 (prime)"
    print("  sum_of_divisors(7) = 8 (1+7)")

    assert sum_of_divisors(97) == 98, "Failed for n=97 (prime)"
    print("  sum_of_divisors(97) = 98 (1+97)")

    print("\n[Test 4] Sum of Divisors - Part 1 Target")
    print("-" * 60)

    # Part 1 verification (CRITICAL)
    assert sum_of_divisors(989) == 1056, "Failed for n=989 (Part 1 target)"
    print("  sum_of_divisors(989) = 1056 (Part 1 verification)")

    print("\n  All divisor sum tests passed!")


def test_divisor_sum_edge_cases():
    """Test edge cases in divisor summation"""
    print("\n[Test 5] Sum of Divisors - Edge Cases")
    print("-" * 60)

    # Edge cases
    assert sum_of_divisors(0) == 0, "Failed for n=0"
    print("  sum_of_divisors(0) = 0")

    assert sum_of_divisors(2) == 3, "Failed for n=2 (prime: 1+2)"
    print("  sum_of_divisors(2) = 3 (1+2)")

    # Large primes
    assert sum_of_divisors(991) == 992, "Failed for n=991 (prime)"
    print("  sum_of_divisors(991) = 992 (1+991)")

    # Perfect squares
    assert sum_of_divisors(4) == 7, "Failed for n=4 (1+2+4)"
    print("  sum_of_divisors(4) = 7 (1+2+4)")

    assert sum_of_divisors(9) == 13, "Failed for n=9 (1+3+9)"
    print("  sum_of_divisors(9) = 13 (1+3+9)")

    assert sum_of_divisors(144) == 403, "Failed for n=144"
    print("  sum_of_divisors(144) = 403")

    print("\n  All edge case tests passed!")


def test_target_extraction_part1():
    """Test extraction with Part 1 parameters (r0=0) - should get 989"""
    print("\n[Test 6] Target Extraction - Part 1")
    print("-" * 60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    ip_register, instructions = parse_input(input_text)

    target, iterations = extract_target_number(
        ip_register, instructions, initial_r0=0
    )

    # Validation checks
    assert target == 989, f"Part 1 target should be 989, got {target}"
    print(f"  Target extracted: {target}")

    assert iterations < 100, f"Should extract within 100 iterations, took {iterations}"
    print(f"  Iterations: {iterations}")

    print("\n  Part 1 extraction test passed!")
    return target


def test_target_extraction_part2():
    """Test extraction with Part 2 parameters (r0=1) - should get 10551389"""
    print("\n[Test 7] Target Extraction - Part 2")
    print("-" * 60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    ip_register, instructions = parse_input(input_text)

    target, iterations = extract_target_number(
        ip_register, instructions, initial_r0=1
    )

    # Validation checks
    assert target > 0, "Target must be positive"
    print(f"  Target extracted: {target}")

    assert target > 989, f"Part 2 target should be larger than Part 1 (989), got {target}"
    print(f"  Target is larger than Part 1 (989)")

    assert target < 10**10, f"Target seems unreasonably large: {target}"
    print(f"  Target is reasonable (< 10^10)")

    assert iterations < 1000, f"Should extract within 1000 iterations, took {iterations}"
    print(f"  Iterations: {iterations}")

    # Based on analysis, we expect target = 10551389
    expected = 10551389
    if target == expected:
        print(f"  Matches expected value: {expected}")

    print("\n  Part 2 extraction test passed!")
    return target


def test_algorithm_verification():
    """Test that sum_of_divisors algorithm matches Part 1's known answer"""
    print("\n[Test 8] CRITICAL - Algorithm Verification")
    print("-" * 60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input
    ip_register, instructions = parse_input(input_text)

    # Extract target for Part 1 (r0=0)
    target_part1, iterations = extract_target_number(
        ip_register, instructions, initial_r0=0
    )

    print(f"  Part 1 target extracted: {target_part1} (after {iterations} iterations)")

    # Compute sum of divisors
    result = sum_of_divisors(target_part1)

    # Verify against known Part 1 answer
    expected = 1056
    assert result == expected, f"Algorithm verification FAILED: {result} != {expected}"

    print(f"  sum_of_divisors({target_part1}) = {result}")
    print(f"  Matches Part 1 answer: {expected}")

    print("\n  Algorithm verification PASSED!")


def test_stability_detection():
    """
    Verify that register 4 stabilizes correctly during extraction
    """
    print("\n[Test 9] Stability Detection")
    print("-" * 60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    ip_register, instructions = parse_input(input_text)

    # For Part 1, manually verify r4 stabilizes at 989
    target_p1, iter_p1 = extract_target_number(ip_register, instructions, initial_r0=0)
    assert target_p1 == 989, f"Part 1 target should stabilize at 989, got {target_p1}"
    print(f"  Part 1 r4 stabilized at {target_p1} after {iter_p1} iterations")

    # For Part 2, manually verify r4 stabilizes at 10551389
    target_p2, iter_p2 = extract_target_number(ip_register, instructions, initial_r0=1)
    assert target_p2 == 10551389, f"Part 2 target should stabilize at 10551389, got {target_p2}"
    print(f"  Part 2 r4 stabilized at {target_p2} after {iter_p2} iterations")

    print("\n  Stability detection test passed!")


def validate_final_answer(answer, target_n):
    """
    Perform sanity checks on the final answer
    """
    print("\n[Test 10] Final Answer Validation")
    print("-" * 60)

    # Should be positive
    assert answer > 0, "Answer must be positive"
    print(f"  Answer is positive: {answer}")

    # Should be larger than Part 1 answer
    assert answer > 1056, f"Part 2 answer should exceed Part 1 (1056), got {answer}"
    print(f"  Answer exceeds Part 1 (1056)")

    # Should be an integer
    assert isinstance(answer, int), "Answer must be integer"
    print(f"  Answer is an integer")

    # Mathematical property: sum of divisors of N >= N + 1
    # (for N > 1, divisors include at least 1 and N)
    assert answer >= target_n + 1, \
        f"Sum of divisors ({answer}) should be at least N+1 ({target_n + 1})"
    print(f"  Answer >= N+1 (mathematical property satisfied)")

    # For our specific case, based on analysis
    expected_target = 10551389
    expected_answer = 10915260
    if target_n == expected_target:
        if answer == expected_answer:
            print(f"  Answer matches expected: {answer}")
        else:
            print(f"  WARNING: Answer {answer} differs from expected {expected_answer}")

    print(f"\n  Final answer validation passed: {answer}")
    print(f"  (Sum of divisors of {target_n})")

    return True


def test_performance():
    """Test that complete solution runs efficiently"""
    import time

    print("\n[Test 11] Performance Test")
    print("-" * 60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    start_time = time.time()

    # Parse input
    ip_register, instructions = parse_input(input_text)

    # Verify algorithm (Part 1)
    verify_start = time.time()
    target_part1, _ = extract_target_number(ip_register, instructions, initial_r0=0)
    result_part1 = sum_of_divisors(target_part1)
    assert result_part1 == 1056
    verify_time = time.time() - verify_start

    # Extract target (Part 2)
    extract_start = time.time()
    target, iterations = extract_target_number(ip_register, instructions, initial_r0=1)
    extract_time = time.time() - extract_start

    # Compute result
    compute_start = time.time()
    result = sum_of_divisors(target)
    compute_time = time.time() - compute_start

    total_time = time.time() - start_time

    # Performance assertions
    assert verify_time < 1.0, f"Verification too slow: {verify_time:.3f}s"
    assert extract_time < 1.0, f"Extraction too slow: {extract_time:.3f}s"
    assert compute_time < 1.0, f"Computation too slow: {compute_time:.3f}s"
    assert total_time < 5.0, f"Total solution too slow: {total_time:.3f}s"

    print(f"  Verification: {verify_time:.3f}s")
    print(f"  Extraction: {extract_time:.3f}s ({iterations} iterations)")
    print(f"  Computation: {compute_time:.3f}s")
    print(f"  Total: {total_time:.3f}s")
    print(f"  Result: {result}")

    print("\n  Performance test passed!")

    return result, target


def run_all_tests():
    """
    Comprehensive test suite for Day 19 Part 2
    Tests run in order of importance
    """
    print("="*60)
    print("Day 19 Part 2 - Comprehensive Test Suite")
    print("="*60)

    # Phase 0: CRITICAL - Algorithm Verification
    test_algorithm_verification()

    # Phase 1: Unit Tests
    test_sum_of_divisors()
    test_divisor_sum_edge_cases()

    # Phase 2: Integration Tests
    test_target_extraction_part1()
    target = test_target_extraction_part2()
    test_stability_detection()

    # Phase 4: End-to-End & Performance
    result, target = test_performance()

    # Final validation
    validate_final_answer(result, target)

    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60)
    print(f"Final Answer: {result}")
    print("="*60)


if __name__ == '__main__':
    run_all_tests()
