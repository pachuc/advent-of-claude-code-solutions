#!/usr/bin/env python3
"""
Comprehensive test verification for Day 19 Part 2
"""

import sys
sys.path.insert(0, '.')
from solution import sum_of_divisors, extract_target_number, parse_input, verify_algorithm_with_part1

def test_sum_of_divisors():
    """Test sum of divisors with known values"""
    print("\n[Test 1] Testing sum_of_divisors function...")
    print("-" * 60)

    test_cases = [
        (1, 1, [1]),
        (6, 12, [1, 2, 3, 6]),
        (12, 28, [1, 2, 3, 4, 6, 12]),
        (28, 56, [1, 2, 4, 7, 14, 28]),
        (16, 31, [1, 2, 4, 8, 16]),  # Perfect square
        (25, 31, [1, 5, 25]),  # Perfect square
        (100, 217, [1, 2, 4, 5, 10, 20, 25, 50, 100]),  # Perfect square
        (989, 1056, None),  # Part 1 target - CRITICAL
    ]

    all_passed = True
    for n, expected, divisors in test_cases:
        result = sum_of_divisors(n)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_passed = False
        print(f"  sum_of_divisors({n}) = {result} (expected {expected}) [{status}]")
        if divisors:
            actual_sum = sum(divisors)
            if actual_sum != expected:
                print(f"    WARNING: Manual calculation gives {actual_sum}")

    return all_passed


def test_perfect_squares():
    """Test perfect squares to ensure no double-counting"""
    print("\n[Test 2] Testing perfect squares (avoid double-counting)...")
    print("-" * 60)

    test_cases = [
        (4, 7),    # 1 + 2 + 4
        (9, 13),   # 1 + 3 + 9
        (16, 31),  # 1 + 2 + 4 + 8 + 16
        (144, 403), # Many divisors
    ]

    all_passed = True
    for n, expected in test_cases:
        result = sum_of_divisors(n)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_passed = False
        print(f"  sum_of_divisors({n}) = {result} (expected {expected}) [{status}]")

    return all_passed


def test_primes():
    """Test prime numbers (sum should be n+1)"""
    print("\n[Test 3] Testing prime numbers (sum = n+1)...")
    print("-" * 60)

    primes = [2, 3, 5, 7, 11, 13, 97, 991]
    all_passed = True

    for p in primes:
        result = sum_of_divisors(p)
        expected = p + 1
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_passed = False
        print(f"  sum_of_divisors({p}) = {result} (expected {expected}) [{status}]")

    return all_passed


def test_algorithm_verification():
    """CRITICAL: Verify algorithm using Part 1"""
    print("\n[Test 4] CRITICAL - Algorithm Verification with Part 1...")
    print("-" * 60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    ip_register, instructions = parse_input(input_text)

    # Extract target for Part 1 (r0=0)
    target_part1, iterations = extract_target_number(ip_register, instructions, initial_r0=0)
    print(f"  Part 1 target: {target_part1} (after {iterations} iterations)")

    # Compute sum
    result = sum_of_divisors(target_part1)
    print(f"  sum_of_divisors({target_part1}) = {result}")

    # Should match Part 1 answer
    expected = 1056
    status = "PASS" if result == expected else "FAIL"
    print(f"  Expected Part 1 answer: {expected} [{status}]")

    return result == expected


def test_part2_extraction():
    """Test target extraction for Part 2"""
    print("\n[Test 5] Testing Part 2 target extraction...")
    print("-" * 60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    ip_register, instructions = parse_input(input_text)

    # Extract target for Part 2 (r0=1)
    target_part2, iterations = extract_target_number(ip_register, instructions, initial_r0=1)
    print(f"  Part 2 target: {target_part2} (after {iterations} iterations)")

    # Verify it's reasonable
    all_passed = True

    if target_part2 <= 0:
        print(f"  FAIL: Target must be positive")
        all_passed = False

    if target_part2 <= 989:
        print(f"  FAIL: Part 2 target should be larger than Part 1 (989)")
        all_passed = False

    if target_part2 > 10**10:
        print(f"  WARNING: Target seems very large")

    if iterations > 100:
        print(f"  WARNING: Took many iterations ({iterations})")

    # Check expected value
    expected = 10551389
    if target_part2 == expected:
        print(f"  PASS: Matches expected value {expected}")
    else:
        print(f"  INFO: Got {target_part2}, expected {expected}")

    return all_passed


def test_final_answer():
    """Verify final answer"""
    print("\n[Test 6] Testing final answer...")
    print("-" * 60)

    with open('input.md', 'r') as f:
        input_text = f.read()

    ip_register, instructions = parse_input(input_text)

    # Extract target for Part 2
    target, iterations = extract_target_number(ip_register, instructions, initial_r0=1)
    print(f"  Target: {target}")

    # Compute answer
    answer = sum_of_divisors(target)
    print(f"  Answer: {answer}")

    # Sanity checks
    all_passed = True

    if answer <= 0:
        print(f"  FAIL: Answer must be positive")
        all_passed = False

    if answer <= 1056:
        print(f"  FAIL: Part 2 answer should exceed Part 1 (1056)")
        all_passed = False

    if answer < target + 1:
        print(f"  FAIL: Sum of divisors should be at least n+1")
        all_passed = False

    # Check expected
    expected = 10915260
    if answer == expected:
        print(f"  PASS: Matches expected answer {expected}")
    else:
        print(f"  INFO: Got {answer}, expected {expected}")

    return all_passed, answer


def test_manually_verify_989():
    """Manually verify divisors of 989"""
    print("\n[Test 7] Manually verifying divisors of 989...")
    print("-" * 60)

    # 989 = 23 * 43
    # Divisors: 1, 23, 43, 989
    # Sum: 1 + 23 + 43 + 989 = 1056

    divisors = []
    n = 989
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)

    print(f"  Divisors of 989: {divisors}")
    manual_sum = sum(divisors)
    print(f"  Manual sum: {manual_sum}")

    computed = sum_of_divisors(989)
    print(f"  Computed sum: {computed}")

    status = "PASS" if manual_sum == computed == 1056 else "FAIL"
    print(f"  [{status}]")

    return manual_sum == computed == 1056


def main():
    """Run all tests"""
    print("=" * 60)
    print("Day 19 Part 2 - Comprehensive Test Verification")
    print("=" * 60)

    tests = [
        ("Sum of Divisors - Basic", test_sum_of_divisors),
        ("Perfect Squares", test_perfect_squares),
        ("Prime Numbers", test_primes),
        ("Manual Verification of 989", test_manually_verify_989),
        ("Algorithm Verification (CRITICAL)", test_algorithm_verification),
        ("Part 2 Target Extraction", test_part2_extraction),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nERROR in {name}: {e}")
            results.append((name, False))

    # Final answer test
    try:
        passed, answer = test_final_answer()
        results.append(("Final Answer", passed))
    except Exception as e:
        print(f"\nERROR in Final Answer test: {e}")
        results.append(("Final Answer", False))
        answer = None

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        if not result:
            all_passed = False
        print(f"  {name}: [{status}]")

    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED!")
        print(f"Final Answer: {answer}")
    else:
        print("SOME TESTS FAILED - See details above")
    print("=" * 60)

    return all_passed, answer


if __name__ == '__main__':
    passed, answer = main()
    sys.exit(0 if passed else 1)
