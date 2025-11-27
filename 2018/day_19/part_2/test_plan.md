# Test Plan - Day 19 Part 2

## Testing Objectives

1. **CRITICAL:** Verify algorithm interpretation using Part 1's known answer
2. Validate the sum of divisors algorithm implementation
3. Verify that target number N is correctly extracted from initialization
4. Confirm the final answer is correct for the given input
5. Ensure the solution completes in reasonable time

## Test Strategy Overview

Since this is a puzzle solution (not production code), we focus on:
- **Algorithm verification** using Part 1 as a test case (MOST IMPORTANT)
- **Correctness validation** of the core algorithms (sum of divisors)
- **Performance validation** to ensure it runs efficiently
- **Edge case handling** for divisor computation (especially perfect squares)
- **Target extraction validation** to ensure register 4 is captured correctly

## Test Categories

### 0. CRITICAL - Algorithm Verification Using Part 1

**Purpose:** Verify that our interpretation of the assembly code is correct BEFORE implementing Part 2

**This is the MOST IMPORTANT test and must pass before proceeding.**

**Test Approach:**
```python
def test_algorithm_verification():
    """
    Test that sum_of_divisors algorithm matches Part 1's known answer
    """
    # Parse input
    ip_register, instructions = parse_input(input_text)

    # Extract target for Part 1 (r0=0)
    target_part1, iterations = extract_target_number(
        ip_register, instructions, initial_r0=0
    )

    print(f"Part 1 target extracted: {target_part1} (after {iterations} iterations)")

    # Compute sum of divisors
    result = sum_of_divisors(target_part1)

    # Verify against known Part 1 answer
    expected = 1056
    assert result == expected, f"Algorithm verification FAILED: {result} != {expected}"

    print(f"✓ Algorithm verified: sum_of_divisors({target_part1}) = {result}")
    print(f"✓ Matches Part 1 answer: {expected}")
```

**Expected Results:**
- target_part1 = 989
- sum_of_divisors(989) = 1056
- Test PASSES

**If this test fails:** Do NOT proceed with Part 2. Re-analyze the assembly code.

### 1. Unit Tests - Sum of Divisors Algorithm

**Purpose:** Verify the divisor sum calculation is mathematically correct

**Test Cases:**

| Input N | Expected Sum | Divisors | Notes |
|---------|--------------|----------|-------|
| 1 | 1 | [1] | Minimal case |
| 6 | 12 | [1,2,3,6] | Perfect number example |
| 12 | 28 | [1,2,3,4,6,12] | Common test case |
| 16 | 31 | [1,2,4,8,16] | Perfect square - avoid double-counting |
| 25 | 31 | [1,5,25] | Perfect square (prime²) |
| 28 | 56 | [1,2,4,7,14,28] | Perfect number |
| 100 | 217 | [1,2,4,5,10,20,25,50,100] | Perfect square |
| 989 | 1056 | - | Part 1 target (CRITICAL verification) |

**Implementation:**
```python
def test_sum_of_divisors():
    """Test sum of divisors with known values"""
    # Basic cases
    assert sum_of_divisors(1) == 1, "Failed for n=1"
    assert sum_of_divisors(6) == 12, "Failed for n=6"
    assert sum_of_divisors(12) == 28, "Failed for n=12"
    assert sum_of_divisors(28) == 56, "Failed for n=28"

    # Perfect squares (CRITICAL - avoid double-counting)
    assert sum_of_divisors(16) == 31, "Failed for n=16 (perfect square)"
    assert sum_of_divisors(25) == 31, "Failed for n=25 (perfect square)"
    assert sum_of_divisors(100) == 217, "Failed for n=100 (perfect square)"

    # Part 1 verification (CRITICAL)
    assert sum_of_divisors(989) == 1056, "Failed for n=989 (Part 1 target)"

    # Prime numbers (sum should be n+1)
    assert sum_of_divisors(7) == 8, "Failed for n=7 (prime)"
    assert sum_of_divisors(97) == 98, "Failed for n=97 (prime)"

    print("✓ All divisor sum tests passed!")
```

**Critical Checks:**
- ✓ Verify 1 and N itself are both included
- ✓ Verify perfect squares don't double-count the square root (i == n//i case)
- ✓ Verify primes only have divisors 1 and themselves
- ✓ Verify Part 1 target (989) produces correct answer (1056)

### 2. Integration Test - Target Number Extraction

**Purpose:** Verify we correctly extract the target number from register 4

**Test Approach:**
```python
def test_target_extraction_part1():
    """Test extraction with Part 1 parameters (r0=0) - should get 989"""
    ip_register, instructions = parse_input(input_text)

    target, iterations = extract_target_number(
        ip_register, instructions, initial_r0=0
    )

    # Validation checks
    assert target == 989, f"Part 1 target should be 989, got {target}"
    assert iterations < 100, f"Should extract within 100 iterations, took {iterations}"

    print(f"✓ Part 1 extraction: target={target}, iterations={iterations}")

def test_target_extraction_part2():
    """Test extraction with Part 2 parameters (r0=1) - should get 10551389"""
    ip_register, instructions = parse_input(input_text)

    target, iterations = extract_target_number(
        ip_register, instructions, initial_r0=1
    )

    # Validation checks
    assert target > 0, "Target must be positive"
    assert target > 989, f"Part 2 target should be larger than Part 1 (989), got {target}"
    assert target < 10**10, f"Target seems unreasonably large: {target}"
    assert iterations < 1000, f"Should extract within 1000 iterations, took {iterations}"

    print(f"✓ Part 2 extraction: target={target}, iterations={iterations}")

    # Based on analysis, we expect target = 10551389
    expected = 10551389
    if target == expected:
        print(f"✓ Matches expected value: {expected}")

    return target
```

**Expected Behavior:**
- Part 1: target = 989, iterations < 100
- Part 2: target = 10551389, iterations < 100 (based on analysis, ~26 iterations)
- Target number is a positive integer
- Register 4 stabilizes (10 consecutive iterations unchanged)

### 3. Validation Test - Cross-Check with Part 1 Simulation

**Purpose:** Ensure Part 1 still works correctly and validates our approach

**Test Approach:**
```python
def test_part1_full_simulation():
    """
    Run complete Part 1 simulation and verify it produces 1056
    This confirms our CPU simulator is working correctly
    """
    ip_register, instructions = parse_input(input_text)

    # Run full Part 1 simulation (from part_1_solution.py)
    result = execute_program(ip_register, instructions, debug=False)

    expected = 1056
    assert result == expected, f"Part 1 simulation failed: {result} != {expected}"

    print(f"✓ Part 1 full simulation: {result}")
```

**Test Consistency Between Extraction and Simulation:**
```python
def test_extraction_matches_simulation():
    """
    Verify that our target extraction gives the same result as
    what the program would compute via simulation
    """
    ip_register, instructions = parse_input(input_text)

    # Extract target for Part 1
    target_part1, _ = extract_target_number(ip_register, instructions, initial_r0=0)

    # Compute using our optimized algorithm
    result_optimized = sum_of_divisors(target_part1)

    # Should match Part 1's known answer
    expected = 1056
    assert result_optimized == expected, \
        f"Extraction + optimization mismatch: {result_optimized} != {expected}"

    print(f"✓ Extraction + optimization matches Part 1: {result_optimized}")
```

### 4. Performance Test

**Purpose:** Ensure solution completes in reasonable time

**Test:**
```python
import time

def test_performance():
    """Test that complete solution runs efficiently"""
    start_time = time.time()

    # Parse input
    ip_register, instructions = parse_input(input_text)

    # Verify algorithm (Part 1)
    verify_start = time.time()
    verify_algorithm_with_part1(ip_register, instructions)
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

    print(f"✓ Performance test passed:")
    print(f"  - Verification: {verify_time:.3f}s")
    print(f"  - Extraction: {extract_time:.3f}s ({iterations} iterations)")
    print(f"  - Computation: {compute_time:.3f}s")
    print(f"  - Total: {total_time:.3f}s")
    print(f"  - Result: {result}")
```

**Expected Performance:**
- Verification (Part 1): < 0.1s
- Extraction (Part 2): < 0.1s (~26 iterations)
- Computation: < 0.1s (sqrt(10551389) ≈ 3248 iterations)
- Total runtime: < 1 second (well under 5 second limit)

### 5. Edge Case Tests

**Test A - Divisor Sum Edge Cases:**
```python
def test_divisor_sum_edge_cases():
    """Test edge cases in divisor summation"""
    # Edge cases
    assert sum_of_divisors(0) == 0, "Failed for n=0"
    assert sum_of_divisors(1) == 1, "Failed for n=1"
    assert sum_of_divisors(2) == 3, "Failed for n=2 (prime: 1+2)"

    # Large primes (sum should be prime + 1)
    assert sum_of_divisors(97) == 98, "Failed for n=97 (prime)"
    assert sum_of_divisors(991) == 992, "Failed for n=991 (prime)"

    # Perfect squares (avoid double-counting)
    assert sum_of_divisors(4) == 7, "Failed for n=4 (1+2+4)"
    assert sum_of_divisors(9) == 13, "Failed for n=9 (1+3+9)"
    assert sum_of_divisors(144) == 403, "Failed for n=144"

    print("✓ All edge case tests passed")
```

**Test B - Stability Detection:**
```python
def test_stability_detection():
    """
    Verify that register 4 stabilizes correctly during extraction
    """
    ip_register, instructions = parse_input(input_text)

    # For Part 1, manually verify r4 stabilizes at 989
    target_p1, iter_p1 = extract_target_number(ip_register, instructions, initial_r0=0)
    assert target_p1 == 989, f"Part 1 target should stabilize at 989, got {target_p1}"
    print(f"✓ Part 1 r4 stabilized at {target_p1} after {iter_p1} iterations")

    # For Part 2, manually verify r4 stabilizes at 10551389
    target_p2, iter_p2 = extract_target_number(ip_register, instructions, initial_r0=1)
    assert target_p2 == 10551389, f"Part 2 target should stabilize at 10551389, got {target_p2}"
    print(f"✓ Part 2 r4 stabilized at {target_p2} after {iter_p2} iterations")
```

### 6. Final Answer Validation

**Purpose:** Verify the final answer is reasonable and correct

**Sanity Checks:**
```python
def validate_final_answer(answer, target_n):
    """
    Perform sanity checks on the final answer
    """
    # Should be positive
    assert answer > 0, "Answer must be positive"

    # Should be larger than Part 1 answer
    assert answer > 1056, f"Part 2 answer should exceed Part 1 (1056), got {answer}"

    # Should be an integer
    assert isinstance(answer, int), "Answer must be integer"

    # Mathematical property: sum of divisors of N >= N + 1
    # (for N > 1, divisors include at least 1 and N)
    assert answer >= target_n + 1, \
        f"Sum of divisors ({answer}) should be at least N+1 ({target_n + 1})"

    # For our specific case, based on analysis
    expected_target = 10551389
    expected_answer = 10915260
    if target_n == expected_target:
        if answer == expected_answer:
            print(f"✓ Answer matches expected: {answer}")
        else:
            print(f"⚠ Answer {answer} differs from expected {expected_answer}")

    print(f"✓ Final answer validation passed: {answer}")
    print(f"  (Sum of divisors of {target_n})")

    return True
```

## Test Execution Plan

### Phase 0: CRITICAL - Algorithm Verification (MUST RUN FIRST)
1. **Test algorithm verification using Part 1**
   - Extract target for r0=0 (should get 989)
   - Compute sum_of_divisors(989) (should get 1056)
   - Verify matches Part 1 answer
   - **STOP if this fails** - re-analyze assembly code

### Phase 1: Unit Testing
1. Test `sum_of_divisors()` with known values (1, 6, 12, 28, 100, 989)
2. **CRITICAL:** Test perfect squares (16, 25, 100, 144) to verify no double-counting
3. Test primes (7, 97, 991) to verify sum = prime + 1
4. Test edge cases (0, 1, 2)

### Phase 2: Integration Testing
1. Test Part 1 target extraction (r0=0, should get 989)
2. Test Part 2 target extraction (r0=1, should get 10551389)
3. Verify stability detection works (10 consecutive unchanged iterations)
4. Verify extraction completes quickly (< 100 iterations)

### Phase 3: Cross-Validation
1. Run Part 1 full simulation (should get 1056)
2. Verify extraction + optimization matches simulation for Part 1
3. Confirm CPU simulator is working correctly

### Phase 4: End-to-End Testing
1. Run complete Part 2 solution on actual input
2. Measure performance (should be < 1 second total)
3. Validate final answer passes sanity checks
4. Verify answer matches expected (10915260)

## Success Criteria

The solution is considered correct if ALL of the following pass:

1. ✓ **CRITICAL:** Algorithm verification using Part 1 passes (sum_of_divisors(989) == 1056)
2. ✓ All unit tests for `sum_of_divisors()` pass (including perfect squares)
3. ✓ Target extraction for Part 1 produces 989
4. ✓ Target extraction for Part 2 produces 10551389
5. ✓ Solution completes in < 5 seconds (should be < 1 second)
6. ✓ Final answer matches expected: 10915260
7. ✓ Part 1 full simulation still produces 1056

**If any test fails:** Investigate immediately before proceeding to the next phase.

## Debugging Strategy

If tests fail, follow this troubleshooting guide:

### If Algorithm Verification Fails (Phase 0)
**CRITICAL - DO NOT PROCEED TO PART 2**
1. Re-run Part 1 full simulation - verify it still produces 1056
2. Check target extraction for Part 1 - should get 989
3. Manually verify sum_of_divisors(989):
   - Divisors of 989: 1, 23, 43, 989
   - Sum: 1 + 23 + 43 + 989 = 1056 ✓
4. If still failing, re-analyze the assembly code interpretation

### If Divisor Sum Tests Fail (Phase 1)
1. Check for off-by-one errors in loop bounds (`while i * i <= n`)
2. **Perfect square handling:** Verify `if i != n // i` condition
3. Test with manually calculated examples
4. Compare with naive O(N) implementation for small N:
   ```python
   def sum_divisors_naive(n):
       return sum(i for i in range(1, n+1) if n % i == 0)
   ```

### If Target Extraction Fails (Phase 2)
1. Increase iteration limit (try 5000 instead of 1000)
2. Add debug logging to see register 4 changes over time
3. Verify stability detection (10 consecutive unchanged iterations)
4. Check that initialization completes before entering main loop
5. Manually trace first 50 iterations to see r4 progression

### If Final Answer is Wrong (Phase 4)
1. Verify target extraction produced correct value (10551389)
2. Manually compute sum_of_divisors(10551389) with debug output
3. Check input parsing - ensure using correct input file
4. Verify r0 initialization is set to 1 (not 0)
5. Re-run algorithm verification to ensure it still passes

## Manual Verification Steps

1. **Inspect Target Number:**
   - Print the extracted target number N
   - Manually verify it's reasonable (not negative, not suspiciously small)

2. **Spot Check Divisors:**
   - For the extracted N, manually verify a few divisors
   - Example: if N=10000, check that 1, 2, 5, 10, 100, 1000, 10000 are included

3. **Compare with Part 1:**
   - Ensure Part 1 logic still produces 1056
   - This validates we didn't break existing functionality

## Test Implementation Template

```python
def run_all_tests():
    """
    Comprehensive test suite for Day 19 Part 2
    Tests run in order of importance
    """
    print("="*60)
    print("Day 19 Part 2 - Test Suite")
    print("="*60)

    # Parse input once
    with open('input.md', 'r') as f:
        input_text = f.read()
    ip_register, instructions = parse_input(input_text)

    # Phase 0: CRITICAL - Algorithm Verification
    print("\n[CRITICAL] Algorithm Verification...")
    print("-" * 60)
    test_algorithm_verification()

    # Phase 1: Unit Tests
    print("\n[Phase 1] Unit Tests - Sum of Divisors...")
    print("-" * 60)
    test_sum_of_divisors()
    test_divisor_sum_edge_cases()

    # Phase 2: Integration Tests
    print("\n[Phase 2] Integration Tests - Target Extraction...")
    print("-" * 60)
    test_target_extraction_part1()
    target = test_target_extraction_part2()
    test_stability_detection()

    # Phase 3: Cross-Validation
    print("\n[Phase 3] Cross-Validation...")
    print("-" * 60)
    test_part1_full_simulation()
    test_extraction_matches_simulation()

    # Phase 4: End-to-End & Performance
    print("\n[Phase 4] End-to-End & Performance...")
    print("-" * 60)
    test_performance()

    # Final validation
    print("\n[Final] Answer Validation...")
    print("-" * 60)
    result = sum_of_divisors(target)
    validate_final_answer(result, target)

    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED!")
    print("="*60)
    print(f"Final Answer: {result}")
```

## Notes

- Since this is a single-input puzzle, extensive input variation testing is not required
- Focus is on correctness of the algorithm and efficient execution
- The main risk is incorrect interpretation of the assembly code
- If the optimized approach fails, fall back to direct simulation with progress monitoring
