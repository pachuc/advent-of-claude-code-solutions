# Testing Plan: Finding the Lowest House Number with Sufficient Presents

## Testing Objectives
1. Verify divisor sum calculation is correct
2. Confirm present calculation follows the rules (10× divisor sum)
3. Ensure search finds the LOWEST house meeting criteria
4. Validate against known examples from problem statement
5. Verify solution works for the actual input (34,000,000)

## Test Categories

### 1. Unit Tests: Divisor Sum Function

**Test 1.1: Small Numbers with Known Divisors**
- Input: n = 1
- Expected divisors: [1]
- Expected sum: 1
- Verification: Manual calculation

**Test 1.2: Prime Number**
- Input: n = 7
- Expected divisors: [1, 7]
- Expected sum: 8
- Verification: Primes only have divisors 1 and themselves

**Test 1.3: Composite Number**
- Input: n = 6
- Expected divisors: [1, 2, 3, 6]
- Expected sum: 12
- Verification: Manual calculation

**Test 1.4: Perfect Square**
- Input: n = 9
- Expected divisors: [1, 3, 9]
- Expected sum: 13
- Verification: Ensure sqrt(n) not counted twice

**Test 1.5: Larger Composite**
- Input: n = 12
- Expected divisors: [1, 2, 3, 4, 6, 12]
- Expected sum: 28
- Verification: Manual calculation

**Test 1.6: Perfect Square (Larger)**
- Input: n = 16
- Expected divisors: [1, 2, 4, 8, 16]
- Expected sum: 31
- Verification: Ensure 4 (sqrt) counted only once

### 2. Unit Tests: Present Calculation

**Test 2.1: House 1**
- Input: house = 1
- Divisor sum: 1
- Expected presents: 10
- Verification: Matches problem example

**Test 2.2: House 2**
- Input: house = 2
- Divisor sum: 1 + 2 = 3
- Expected presents: 30
- Verification: Matches problem example

**Test 2.3: House 3**
- Input: house = 3
- Divisor sum: 1 + 3 = 4
- Expected presents: 40
- Verification: Matches problem example

**Test 2.4: House 4**
- Input: house = 4
- Divisor sum: 1 + 2 + 4 = 7
- Expected presents: 70
- Verification: Matches problem example

**Test 2.5: House 6**
- Input: house = 6
- Divisor sum: 1 + 2 + 3 + 6 = 12
- Expected presents: 120
- Verification: Matches problem example

### 3. Integration Tests: Find Lowest House

**Test 3.1: Small Target (From Examples)**
- Target: 130 presents
- Expected result: Check houses 1-10 manually
- House 6: divisors [1,2,3,6], sum = 12, presents = 120 (not enough)
- House 8: divisors [1,2,4,8], sum = 15, presents = 150 (first to meet)
- Expected: 8
- Verification: First house ≥ 130
- Also verify: House 7 has divisors [1,7], sum = 8, presents = 80 < 130

**Test 3.2: Medium Target**
- Target: 1000 presents
- Run algorithm
- Verify result house has presents ≥ 1000
- Verify result - 1 house has presents < 1000
- Verification: Boundary checking

**Test 3.3: Highly Composite Target**
- Target: 500 presents
- Run algorithm and verify result
- Check that result is a relatively small number
- Verification: Algorithm finds solution efficiently

**Test 3.4: Lower Bound Heuristic Validation**
- Target: 130 presents
- Lower bound calculation: 130 / 72 = 1.8 → start at house 1
- Verify that starting at house 1 successfully finds house 8
- Purpose: Ensures lower bound heuristic doesn't skip the answer
- For target 34,000,000: verify 34,000,000 / 72 = 472,222
- The actual answer should be ≥ 472,222 for the heuristic to be safe

### 4. Validation Tests: Problem Requirements

**Test 4.1: Monotonicity Check**
- Verify that if house H has X presents, we correctly identify H
- Check that house H-1 has < target presents
- Ensures we found the LOWEST house

**Test 4.2: Off-by-One Validation**
- For found solution house N:
  - Verify presents(N) ≥ target
  - Verify presents(N-1) < target (if N > 1)
- Critical: Ensures we didn't overshoot or undershoot

### 5. Edge Case Tests

**Test 5.1: Target = 10**
- Smallest possible meaningful target
- Expected: House 1 (receives exactly 10)
- Verification: Boundary case

**Test 5.2: Target = 11**
- Expected: House 2 (receives 30)
- Verification: First house not meeting criteria

**Test 5.3: Target Requiring Large House**
- Use actual input: 34,000,000
- Run algorithm
- Verify solution
- Expected runtime: < 1 minute

### 6. Correctness Verification Strategy

**Step 6.1: Manual Verification of Examples**
- Calculate presents for houses 1-10 manually
- Compare with function output
- Ensure 100% match

**Step 6.2: Result Validation**
For the final answer with target 34,000,000:
1. Record the house number found (let's call it H)
2. Calculate presents(H) - should be ≥ 34,000,000
3. Calculate presents(H-1) - should be < 34,000,000
4. Document both values as proof of correctness

**Step 6.3: Cross-Verification**
- Calculate divisor sum independently:
  - List all divisors manually (for smaller tests)
  - Use mathematical properties to verify
  - Ensure no divisors missed or double-counted

### 7. Performance Tests

**Test 7.1: Runtime Measurement**
- Measure time to find solution for target 34,000,000
- Expected: < 30 seconds (well-optimized code should achieve 10-20 seconds)
- If slower than 30 seconds, review algorithm implementation
- If slower than 60 seconds, there's likely a bug

**Test 7.2: Divisor Function Performance**
- Test divisor_sum on large numbers (e.g., 1,000,000)
- Should complete in < 1 millisecond
- Verify O(sqrt(n)) complexity by timing divisor_sum(1,000,000) and divisor_sum(4,000,000)
- The second should take ~2x as long (sqrt ratio)

### 8. Test Execution Plan

**Phase 1: Unit Tests (Run First)**
1. Test divisor_sum with values: 1, 6, 7, 9, 12, 16, 20
2. Test calculate_presents with houses: 1, 2, 3, 4, 6, 8, 9
3. Compare all results with manually calculated values

**Phase 2: Small Integration Tests**
1. Test find_lowest_house with targets: 10, 30, 40, 70, 120, 130
2. Verify each result manually
3. For each test, verify that lower_bound = target/72 doesn't exceed the actual result

**Phase 3: Final Solution Test**
1. Run with actual input: 34,000,000
2. Record result house number
3. Validate result as described in 6.2

**Phase 4: Verification**
1. Calculate presents for result house
2. Calculate presents for (result - 1) house
3. Confirm result is truly the lowest

## Test Documentation Format

For each test, record:
```
Test ID: [e.g., 1.1]
Input: [input values]
Expected Output: [what should happen]
Actual Output: [what actually happened]
Execution Time: [milliseconds/seconds - for performance-critical tests]
Status: PASS/FAIL
Notes: [any observations]
```

## Acceptance Criteria

Solution is correct if:
1. All unit tests pass (divisor sums match manual calculations)
2. All example tests pass (houses 1-6 match problem statement)
3. Result for 34,000,000 satisfies:
   - presents(result) ≥ 34,000,000
   - presents(result - 1) < 34,000,000
4. Lower bound heuristic validation passes (result ≥ target/72)
5. Algorithm completes in reasonable time (< 30 seconds preferred, < 60 seconds maximum)

## Known Edge Cases from Problem Domain

1. **Perfect Squares**: Ensure square root counted only once
2. **Prime Numbers**: Only have divisors 1 and self
3. **Highly Composite Numbers**: Have many divisors (e.g., 120, 240, 360)
4. **House 1**: Special case with only one divisor
5. **Large Houses**: Ensure no integer overflow (Python handles this)

## Debugging Strategy

If tests fail:
1. **Divisor sum wrong**: Print all divisors found, check for duplicates or missing
2. **Wrong house found**: Print presents for houses around the result
3. **Too slow**: Profile the divisor_sum function, check starting bound
4. **Off by one**: Carefully verify boundary condition in search loop
