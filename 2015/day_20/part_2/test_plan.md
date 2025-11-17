# Testing Plan: Elf Present Delivery (Part 2)

## Testing Strategy Overview

We need to verify that our solution correctly:
1. Finds divisors with the 50-house constraint
2. Calculates presents accurately
3. Identifies the lowest house number meeting the target
4. Handles the actual input correctly

## Unit Tests

### Test 1: Divisor Finding with 50-House Limit

**Function**: `get_divisors_with_limit(house_num, max_visits=50)`

#### Test Case 1.1: Small house number (all divisors valid)
- **Input**: house_num = 12, max_visits = 50
- **Expected**: {1, 2, 3, 4, 6, 12}
- **Reasoning**: 12/1=12, 12/2=6, 12/3=4, 12/4=3, 12/6=2, 12/12=1 (all ≤ 50)

#### Test Case 1.2: Boundary case (exactly at limit)
- **Input**: house_num = 100, max_visits = 50
- **Expected**: Should include divisor 2 (100/2=50, exactly at limit)
- **Reasoning**: Verify that ≤ 50 includes exactly 50

#### Test Case 1.3: Large house number (some divisors filtered)
- **Input**: house_num = 120, max_visits = 50
- **Constraint**: Include divisor d only if 120/d ≤ 50
- **Analysis**:
  - Divisor 1: 120/1 = 120 > 50, EXCLUDE
  - Divisor 2: 120/2 = 60 > 50, EXCLUDE
  - Divisor 3: 120/3 = 40 ≤ 50, INCLUDE
  - (All larger divisors will satisfy the constraint)
- **Expected**: {3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120}

#### Test Case 1.4: Perfect square (avoid duplicates)
- **Input**: house_num = 100, max_visits = 50
- **Expected**: Should include 10 only once (not duplicated), and verify correct count
- **Analysis**:
  - Divisors of 100: 1, 2, 4, 5, 10, 20, 25, 50, 100
  - Divisor 1: 100/1 = 100 > 50, EXCLUDE
  - All others: 100/d ≤ 50, INCLUDE
- **Expected**: {2, 4, 5, 10, 20, 25, 50, 100} (exactly 8 divisors, 10 appears once)
- **Reasoning**: Verify no duplicate counting for √N and that the set has exactly 8 elements

#### Test Case 1.5: Prime number within limit
- **Input**: house_num = 47, max_visits = 50
- **Expected**: {1, 47}
- **Reasoning**: Primes only have two divisors

### Test 2: Present Calculation

**Function**: `calculate_presents(house_num, multiplier=11, max_visits=50)`

#### Test Case 2.1: House 1
- **Input**: house_num = 1
- **Expected**: 11 (only elf 1 visits, delivers 11×1 = 11)
- **Reasoning**: Minimal case

#### Test Case 2.2: House 2
- **Input**: house_num = 2
- **Expected**: 33 (elf 1 delivers 11, elf 2 delivers 22)
- **Reasoning**: 2/1=2 ≤ 50 ✓, 2/2=1 ≤ 50 ✓

#### Test Case 2.3: House 100
- **Input**: house_num = 100
- **Constraint**: Include divisor d only if 100/d ≤ 50
- **Analysis**:
  - Divisor 1: 100/1 = 100 > 50, EXCLUDE
  - Divisor 2: 100/2 = 50 ≤ 50, INCLUDE (boundary case)
  - All larger divisors: 100/d < 50, INCLUDE
  - Divisors of 100: 1, 2, 4, 5, 10, 20, 25, 50, 100
  - Valid: 2, 4, 5, 10, 20, 25, 50, 100
- **Expected**: 11 × (2 + 4 + 5 + 10 + 20 + 25 + 50 + 100) = 11 × 216 = 2376
- **Reasoning**: Verify constraint filtering works correctly, especially at boundary (100/2 = exactly 50)

#### Test Case 2.4: House 60
- **Input**: house_num = 60
- **Constraint**: Include divisor d only if 60/d ≤ 50
- **Analysis**:
  - Divisor 1: 60/1 = 60 > 50, EXCLUDE
  - Divisor 2: 60/2 = 30 ≤ 50, INCLUDE
  - All larger divisors: 60/d < 30 ≤ 50, INCLUDE
  - Divisors of 60: 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60
  - Valid divisors: 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60
- **Expected**: 11 × (2+3+4+5+6+10+12+15+20+30+60) = 11 × 167 = 1837
- **Reasoning**: Verify multiple divisors calculation

#### Test Case 2.5: House 51 (critical edge case - first house excluding elf 1)
- **Input**: house_num = 51
- **Constraint**: Include divisor d only if 51/d ≤ 50
- **Analysis**:
  - Divisor 1: 51/1 = 51 > 50, EXCLUDE (this is the KEY test!)
  - Divisor 3: 51/3 = 17 ≤ 50, INCLUDE
  - Divisor 17: 51/17 = 3 ≤ 50, INCLUDE
  - Divisor 51: 51/51 = 1 ≤ 50, INCLUDE
  - Divisors of 51: 1, 3, 17, 51
  - Valid divisors: 3, 17, 51
- **Expected**: 11 × (3 + 17 + 51) = 11 × 71 = 781
- **Reasoning**: Verify that elf 1 is correctly excluded when house > 50

### Test 3: Full Search Function

**Function**: `find_lowest_house(target, multiplier=11, max_visits=50)`

#### Test Case 3.1: Very low target
- **Input**: target = 100
- **Expected**: Should be a small house number
- **Manual verification** (all divisors satisfy constraint for small houses):
  - House 1: 11 × (1) = 11 (too low)
  - House 2: 11 × (1+2) = 33 (too low)
  - House 3: 11 × (1+3) = 44 (too low)
  - House 4: 11 × (1+2+4) = 77 (too low)
  - House 5: 11 × (1+5) = 66 (too low)
  - House 6: 11 × (1+2+3+6) = 132 (PASSES!)
- **Expected**: 6
- **Reasoning**: Verify search finds first house meeting criteria. Note: house 6 gets 132, not 121.

#### Test Case 3.2: Small target requiring constraint consideration
- **Input**: target = 800
- **Expected**: A house where the 50-house limit matters
- **Reasoning**: Verify constraint is actually applied in search

### Test 4: Integration Test with Example Scenario

#### Test Case 4.1: Manual walkthrough for house 120
- **Setup**: Calculate manually and verify code matches
- **House 120 divisors**: 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120
- **Constraint**: Include divisor d only if 120/d ≤ 50
- **Analysis**:
  - Divisor 1: 120/1 = 120 > 50, EXCLUDE
  - Divisor 2: 120/2 = 60 > 50, EXCLUDE
  - Divisor 3: 120/3 = 40 ≤ 50, INCLUDE
  - All larger divisors satisfy the constraint
  - Keep: 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120
- **Calculation**: 11 × (3+4+5+6+8+10+12+15+20+24+30+40+60+120)
  - Sum: 357
  - Total: 11 × 357 = 3927 presents
- **Expected**: calculate_presents(120) should return 3927

## Edge Cases and Special Scenarios

### Edge Case 1: House Number 50 (boundary case)
- **Significance**: Boundary case for the 50-visit limit - all divisors should still be valid
- **Test**: Verify house 50's divisors are handled correctly
- **Constraint**: Include divisor d only if 50/d ≤ 50
- **Analysis**:
  - Divisor 1: 50/1 = 50 ≤ 50, INCLUDE (exactly at boundary)
  - Divisor 2: 50/2 = 25 ≤ 50, INCLUDE
  - All divisors of 50 satisfy the constraint
  - Divisors of 50: 1, 2, 5, 10, 25, 50
- **Expected**: 11 × (1+2+5+10+25+50) = 11 × 93 = 1023

### Edge Case 2: House Number 51 (first exclusion)
- **Significance**: First house where elf 1 stops (51/1 = 51 > 50)
- **Test**: Verify elf 1 is correctly excluded
- **As verified in Test Case 2.5 above**: Should get 781 presents

### Edge Case 3: House Number 1 (minimal case)
- **Significance**: Smallest possible house, should include only elf 1
- **Test**: Verify house 1 is handled correctly with constraint
- **Constraint**: Include divisor d only if 1/d ≤ 50
- **Analysis**:
  - Divisor 1: 1/1 = 1 ≤ 50, INCLUDE
  - Only divisor of 1 is 1
- **Expected**: 11 × 1 = 11
- **Reasoning**: Ensure edge case isn't broken by constraint logic

### Edge Case 4: Large House Numbers (performance test)
- **Test**: Verify performance doesn't degrade significantly for large houses
- **Method**: Time the calculation for house numbers around 500,000-1,000,000
- **Expected**: Should complete in milliseconds per house

## Final Validation Tests

### Validation Test 1: Monotonicity Check
- **Method**: Check several consecutive houses to verify present counts can increase
- **Purpose**: Sanity check that the search will eventually find the answer
- **Test**: Calculate presents for houses 100, 200, 300, 400, 500
- **Expected**: Values should generally trend upward (not strictly, but on average)

### Validation Test 2: Verify Answer is Actually Lowest
- **Method**: After finding the answer, verify house (answer - 1) has fewer presents
- **Purpose**: Confirm we didn't skip the actual lowest house
- **Test**: If answer is N, verify calculate_presents(N-1) < target

### Validation Test 3: Actual Input Execution
- **Input**: 34,000,000
- **Method**: Run the full solution and verify:
  1. Returns a single integer
  2. The returned house has >= 34,000,000 presents
  3. The previous house has < 34,000,000 presents
  4. Completes in reasonable time (<5 minutes)

## Testing Implementation Approach

### Manual Testing
1. Create a test script `test_solution.py`
2. Import functions from main solution
3. Implement each test case with assertions
4. Print results for verification

### Test Structure
```python
def test_divisors():
    # Run Test 1.x cases
    assert get_divisors_with_limit(12, 50) == {1,2,3,4,6,12}
    assert get_divisors_with_limit(100, 50) == {2,4,5,10,20,25,50,100}
    assert len(get_divisors_with_limit(100, 50)) == 8  # Verify no duplicates
    # ... more tests

def test_presents():
    # Run Test 2.x cases
    assert calculate_presents(1) == 11
    assert calculate_presents(6) == 132  # Fixed calculation
    assert calculate_presents(51) == 781  # Elf 1 excluded
    # ... more tests

def test_search():
    # Run Test 3.x cases
    assert find_lowest_house(100) == 6
    # ... more tests

def test_edge_cases():
    # Boundary cases
    assert calculate_presents(1) == 11  # Minimal
    assert calculate_presents(50) == 1023  # At boundary
    assert calculate_presents(51) == 781  # Past boundary
    pass

def test_final_answer():
    # Run full solution and validate
    pass
```

## Performance Testing

### Performance Test 1: Single House Calculation Speed
- **Method**: Time how long it takes to calculate presents for house 786,240 (highly composite)
- **Expected**: < 0.01 seconds

### Performance Test 2: Search Progress and Runtime
- **Method**: Add optional progress printing every 10,000 houses during search
- **Purpose**: Verify search is making progress and estimate completion time
- **Expected**:
  - Steady progress with reasonable speed
  - Total runtime should be under 2 minutes for the full solution
  - With optimized starting point (target // 500 ≈ 68,000), should check 600K-800K houses
  - At ~0.001 seconds per house = 600-800 seconds worst case, but likely much faster

## Success Criteria

The solution is correct if:
1. All unit tests pass
2. Edge cases are handled correctly
3. The answer for 34,000,000 is verified (house N has >= target, house N-1 has < target)
4. Solution completes in reasonable time
5. Manual verification of a few intermediate houses confirms calculation correctness
