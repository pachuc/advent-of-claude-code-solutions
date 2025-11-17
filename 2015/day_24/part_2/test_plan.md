# Test Plan: Sleigh Package Balancing (4 Groups)

## Testing Strategy
Verify the solution correctly finds the minimum quantum entanglement for the optimal first group when dividing packages into 4 equal-weight groups.

## Test Categories

### 1. Example Test Case (From Problem Statement)
**Purpose**: Validate against known example

**Test Case 1.1: Simple Example**
- Input: [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
- Total: 60
- Target per group: 15
- Expected minimum first group size: 2
- Expected valid first groups to check: [11,4], [10,5], [8,7], [9,3,3] (if there were two 3s)
- Expected QE: 44 (from [11,4])

**Verification Steps**:
1. Check target calculation: 60 ÷ 4 = 15 ✓
2. Verify no size-1 group sums to 15 (11 is max, < 15) ✓
3. Check all size-2 groups that sum to 15:
   - [11,4]: QE = 44, remaining [1,2,3,5,7,8,9,10] must form 3 groups of 15
   - [10,5]: QE = 50, remaining [1,2,3,4,7,8,9,11] must form 3 groups of 15
   - [9,6]: Not possible (6 not in input)
   - [8,7]: QE = 56, remaining [1,2,3,4,5,9,10,11] must form 3 groups of 15
4. Verify [11,4] remaining can split:
   - Group 2: [7,8] = 15
   - Group 3: [5,10] = 15
   - Group 4: [1,2,3,9] = 15 ✓
5. Verify QE calculation: 11 × 4 = 44 ✓
6. Confirm 44 is minimum QE among valid size-2 first groups ✓

### 2. Actual Input Test
**Purpose**: Solve the actual problem

**Test Case 2.1: Given Input (28 primes)**
- Input: Prime numbers from input.md
- Total: 1480 (verify by summing all primes)
- Target per group: 370
- Expected: Unknown (this is what we're solving for)

**Verification Steps**:
1. Verify total sum calculation
2. Verify 1480 is divisible by 4
3. Check the returned first group sums to 370
4. Verify remaining packages can actually form 3 groups of 370
5. Verify QE calculation is correct (product of first group weights)
6. Manually verify no smaller first group size exists
7. Manually spot-check a few other same-size groups have higher QE

### 3. Edge Cases

**Test Case 3.1: Impossible Division**
- Input: [1, 2, 3]
- Total: 6
- Target: 1.5 (not an integer)
- Expected: None or error indication
- Verification: Code should detect total not divisible by 4

**Test Case 3.2: Divisible Total But No Valid Configuration**
- Input: [1, 1, 1, 9]
- Total: 12
- Target: 3
- Expected: None or error
- Verification: Total IS divisible by 4, but cannot form 4 groups of weight 3
  - Only way to make 3: [1,1,1], but then [9] remains (can't make 3 groups of 3)
  - This tests that algorithm properly validates remaining packages

**Test Case 3.3: Perfect Equal Groups**
- Input: [5, 5, 5, 5, 5, 5, 5, 5]
- Total: 40
- Target: 10
- Valid first groups: [5,5] (multiple such combinations exist)
- Expected QE: 25
- Verification: Check that any [5,5] pair works and QE = 25

**Test Case 3.4: Single Element Group**
- Input: [10, 5, 5, 5, 5, 5, 5]
- Total: 40
- Target: 10
- Minimum first group: [10] (size 1)
- Expected QE: 10
- Verification: Remaining [5,5,5,5,5,5] should form three [5,5] groups

**Test Case 3.5: All Packages Same Weight**
- Input: [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
- Total: 36
- Target: 9
- First group: [3, 3, 3] (size 3)
- Expected QE: 27
- Verification: Should correctly handle identical weights

### 4. Verification Tests

**Test 4.1: Quantum Entanglement Calculation**
- Verify QE for [11, 4]: 11 × 4 = 44 ✓
- Verify QE for [2, 3, 5]: 2 × 3 × 5 = 30 ✓
- Verify QE for [7]: 7 ✓
- Verify QE for [10, 10, 10]: 1000 ✓

**Test 4.2: Subset Sum Verification (can_split_into_three_groups)**
Test the helper function that checks if remaining packages can form 3 equal groups:
- **Test 4.2a**: Packages: [1, 2, 3, 4, 5, 6], Target: 7
  - Total = 21 = 3 × 7 ✓
  - Possible groups of 7: [1,6], [2,5], [3,4]
  - Valid split: Group1=[1,6], Group2=[2,5], Group3=[3,4] ✓
  - Should return True
- **Test 4.2b**: Packages: [1, 2, 3], Target: 10
  - Total = 6, need 3 × 10 = 30
  - Can't form even one group of 10
  - Should return False
- **Test 4.2c**: Packages: [10, 5, 5, 5], Target: 7
  - Total = 25, need 3 × 7 = 21
  - Total doesn't match (should fail immediately)
  - Should return False
- **Test 4.2d**: Packages: [1, 2, 3, 4, 5, 15], Target: 10
  - Total = 30 = 3 × 10 ✓
  - Can form: [1,2,3,4], [5,15] - only 2 groups, not 3
  - Should return False (tests that 2 groups ≠ 3 groups)

**Test 4.3: Minimum Size Finding**
Verify the algorithm correctly identifies minimum first group size:
- If size-2 groups work, should never try size-3
- If no size-1 works, should try size-2
- Should stop searching after finding valid configurations at minimum size

### 5. Algorithm Correctness Tests

**Test 5.1: Combination Generation**
Verify all combinations are generated correctly:
- For [1,2,3], size 2: should generate (1,2), (1,3), (2,3)
- Order doesn't matter, but all should be present

**Test 5.2: Remaining Packages Calculation (Critical for Duplicates)**
Test that removing first group from packages works correctly using Counter:
- Packages: [1,2,3,4,5], First: [2,4]
  - Remaining should be: [1,3,5] ✓
- **Handle duplicates (CRITICAL)**:
  - Packages: [1,1,2,3], First: [1,2]
  - Remaining should be: [1,3] (one 1 remains)
  - Counter([1,1,2,3]) - Counter([1,2]) = Counter([1,3]) ✓
- **Multiple duplicates**:
  - Packages: [5,5,5,5,5,5], First: [5,5]
  - Remaining should be: [5,5,5,5] (four 5s remain)
  - This is essential for correct verification ✓
- **No duplicates**: Should work identically to simple list removal

**Test 5.3: Early Termination**
Verify optimization works:
- Count how many combinations are checked
- Should stop after exhausting minimum size, not check larger sizes
- Add logging/counter to verify this behavior

### 6. Performance Tests

**Test 6.1: Timing with Timeout**
- Run on actual input (28 packages)
- **Hard timeout**: Must complete within 30 seconds
- Expected time: < 10 seconds with memoization
- If slower, memoization is not working correctly
- Measure and log actual runtime

**Test 6.2: Memoization Effectiveness**
- Add counter to track cache hits/misses on verification function
- With 28 packages, should see significant cache reuse
- Cache hit ratio should be > 50% for efficient memoization
- If no cache hits, verify @lru_cache is applied correctly

**Test 6.3: Large QE Calculation**
- Verify Python handles large integers correctly
- Test QE for large primes: [97, 101, 103, 107, 109, 113]
- Product = 97×101×103×107×109×113 = 1,366,233,039,751,171
- Verify no overflow or precision loss
- Python's arbitrary precision integers should handle this ✓

## Test Execution Plan

### Phase 1: Unit Testing
1. Test helper functions independently:
   - calculate_qe()
   - get_remaining()
   - can_split_into_three_groups()
2. Verify each with multiple inputs

### Phase 2: Integration Testing
1. Test main solve() function with example case
2. Verify output matches expected QE = 44

### Phase 3: Edge Case Testing
1. Run all edge cases from section 3
2. Verify proper handling of each

### Phase 4: Actual Input
1. Run on provided input.md
2. Verify result is sensible:
   - First group sums to 370
   - QE is a positive integer
   - Remaining packages can form 3 groups of 370

### Phase 5: Automated Verification of Final Answer
Create automated verification function to validate the solution:
1. **verify_solution(packages, first_group, target, qe)**:
   - Assert first_group is a subset of packages
   - Assert sum(first_group) == target
   - Assert len(first_group) is minimal (try smaller sizes, should fail)
   - Assert calculate_qe(first_group) == qe
   - Assert get_remaining works correctly
   - Assert remaining packages can form 3 groups of target weight
   - Assert no other same-size group has lower QE (check several)
2. Run this verification on the actual input result
3. Print detailed breakdown for manual inspection:
   - First group composition and QE
   - One example of how remaining packages split into 3 groups
   - Comparison with other same-size first groups

## Success Criteria
- All test cases pass
- Actual input produces a valid answer
- Manual verification confirms the answer is optimal
- Code runs in reasonable time (< 60 seconds)
- No crashes or errors on any test case

## Debugging Strategies
If tests fail:
1. Add print statements showing:
   - Total weight and target
   - Each first group candidate being tested
   - Whether remaining packages can form 3 groups
   - Current minimum QE
2. Test subset sum verification function independently
3. Manually trace through small examples
4. Check off-by-one errors in combination generation
5. Verify remaining packages calculation handles duplicates correctly

## Expected Outputs

For the actual input (28 primes summing to 1480):
- Target weight per group: 370
- Expected minimum first group size: Likely 3-5 packages (estimate)
- Expected QE: Unknown, but should be a large number (product of primes)
- The answer should be unique and verifiable

## Final Validation Checklist
- [ ] Example test case returns QE = 44
- [ ] Actual input completes without errors (< 30 seconds)
- [ ] Returned first group sums to exactly 370
- [ ] Remaining packages verified to form 3 groups of 370
- [ ] QE calculation verified to be correct (no overflow)
- [ ] No smaller first group size produces valid configurations
- [ ] All same-size first groups have QE >= returned value
- [ ] get_remaining() handles duplicates correctly (Counter-based)
- [ ] Memoization is active and effective (cache hit ratio > 50%)
- [ ] Helper functions tested independently with all edge cases
- [ ] Automated verification function passes all checks
