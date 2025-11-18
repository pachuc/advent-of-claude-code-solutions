# Testing Plan: Spiral Memory Stress Test (Part 2)

## Testing Objectives
1. Verify spiral traversal follows correct order (RIGHT → UP → LEFT → DOWN pattern)
2. Validate neighbor sum calculations for all 8 directions
3. Confirm correct termination (first value exceeding threshold)
4. Test with known examples from problem statement

## Test Categories

### 1. Unit Tests for Helper Functions

#### Test 1.1: `get_neighbor_sum()` - Empty Grid
**Purpose**: Verify handling of position with no neighbors
**Setup**:
- Grid: `{(0,0): 1}`
- Test position: `(1, 0)` (second square in spiral)
**Expected**: Sum = 1 (only neighbor is square at (0,0))
**Verification**: Direct calculation

#### Test 1.2: `get_neighbor_sum()` - Multiple Neighbors
**Purpose**: Verify correct summation of all 8 neighbors
**Setup**:
- Grid with multiple filled squares:
  ```
  (0,0) = 1
  (1,0) = 1
  (1,1) = 2
  ```
- Test position: `(0, 1)` (fourth square in spiral)
**Expected**: Sum = 1 + 1 + 2 = 4 (neighbors at (0,0), (1,0), (1,1))
**Verification**: Manual count of neighbors

#### Test 1.3: `get_neighbor_sum()` - All 8 Directions
**Purpose**: Ensure all 8 neighbor offsets are checked correctly
**Setup**:
- **NOTE**: This is a UNIT TEST with a manually constructed grid (not from spiral generation)
- Create grid with center position surrounded by 8 neighbors:
  ```
  (0,2)=1  (1,2)=1  (2,2)=1
  (0,1)=1  (1,1)=?  (2,1)=1
  (0,0)=1  (1,0)=1  (2,0)=1
  ```
- Test position: `(1, 1)`
**Expected**: Sum = 8 (all 8 neighbors have value 1)
**Verification**: Count all neighbor offsets
**Implementation**: Manually construct the grid dictionary for this test

### 2. Spiral Traversal Tests

#### Test 2.1: First 10 Positions
**Purpose**: Verify spiral follows correct coordinate sequence
**Expected Sequence**:
1. (0, 0) - center
2. (1, 0) - right
3. (1, 1) - up
4. (0, 1) - left
5. (-1, 1) - left
6. (-1, 0) - down
7. (-1, -1) - down
8. (0, -1) - right
9. (1, -1) - right
10. (2, -1) - right

**Verification**:
- Instrument code to print coordinates of first 10 squares
- Manually verify against expected sequence
- Check pattern: 1R, 1U, 2L, 2D, 3R, ...

#### Test 2.2: Direction Changes
**Purpose**: Verify direction changes happen at correct intervals
**Pattern**: Steps before turning: 1, 1, 2, 2, 3, 3, 4, 4, ...
**Verification**:
- Track direction changes in first 20 squares
- Confirm steps_in_direction increments correctly every 2 turns

### 3. Value Generation Tests

#### Test 3.1: First 23 Values Match Example
**Purpose**: Verify complete correctness using problem's example grid
**Problem Example Grid**:
```
147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...
```

**Expected Values in Spiral Order** (first 23):
1. 1 (initial)
2. 1
3. 2
4. 4
5. 5
6. 10
7. 11
8. 23
9. 25
10. 26
11. 54
12. 57
13. 59
14. 122
15. 133
16. 142
17. 147
18. 304
19. 330
20. 351
21. 362
22. 747
23. 806

**Verification Method**:
- Generate first 23 values
- Compare each against expected sequence
- This is the **PRIMARY CORRECTNESS TEST** - if this passes, algorithm is correct

**How to Extract from Grid**:
Read the grid in spiral order (not row by row):
- Start at center: 1
- Go right: 1
- Go up: 2
- Go left: 4, then 5
- Go down: 10, then 11
- Go right: 23, 25, 26
- Go up: 54, 57, 59
- Go left: 122, 133, 142, 147
- Go down: 304, 330, 351, 362
- Go right: 747, 806, ...

#### Test 3.2: Small Threshold Examples
**Purpose**: Test termination condition with small thresholds
**Test Cases**:
- Threshold = 0 → First value > 0 is 1
- Threshold = 1 → First value > 1 is 2
- Threshold = 2 → First value > 2 is 4
- Threshold = 10 → First value > 10 is 11
- Threshold = 25 → First value > 25 is 26
- Threshold = 800 → First value > 800 is 806

**Verification**: Direct comparison with expected sequence

### 4. Main Input Test

#### Test 4.1: Actual Input (289326)
**Purpose**: Solve the actual puzzle
**Input**: 289326
**Verification Strategy**:
- Run the program with actual input
- **Primary checks**:
  - Result > 289326 ✓
  - Result is an integer ✓
  - Program terminates in reasonable time (< 1 second) ✓
- **Enhanced verification** (verify it's FIRST value exceeding threshold):
  - Modify code to also track the previous value generated
  - Verify that previous_value ≤ 289326 < result
  - This confirms result is truly the FIRST value exceeding threshold
- **Reasonableness check**:
  - Based on growth pattern (example shows 806), expect result in range 289327 - 500000
  - Values grow exponentially in outer rings, so this range is reasonable
- **Consistency check**:
  - Run the program multiple times to ensure consistent output (no randomness)

### 5. Edge Cases and Boundary Conditions

#### Test 5.1: Threshold = 0
**Purpose**: Minimum threshold
**Expected**: 1 (first value written)

#### Test 5.2: Threshold = First Value
**Purpose**: Threshold equals starting value
**Input**: threshold = 1
**Expected**: 2 (first value > 1)

#### Test 5.3: Threshold Between Values
**Purpose**: Threshold not exactly matching any generated value
**Input**: threshold = 3
**Expected**: 4 (next value in sequence after passing threshold)

#### Test 5.4: Threshold Exactly Matches Generated Value
**Purpose**: Boundary condition where threshold equals a generated value
**Input**: threshold = 25
**Expected**: 26 (must be strictly greater, not equal)

### 6. Algorithm Correctness Checks

#### Test 6.1: No Value Skipped or Overwritten
**Purpose**: Ensure spiral doesn't skip positions or overwrite values
**Method**:
- Generate first 50 values
- Verify each position has exactly one value
- Check no coordinate appears twice in the grid
- Verify grid size equals number of iterations + 1 (for initial square)
- **Additional check**: Verify no value in grid is ever modified after being set

#### Test 6.2: No Value Used Before Generated
**Purpose**: Ensure neighbor sums only use previously generated values
**Method**:
- For each generated square, verify all neighbors used in sum were generated earlier
- Track generation order and validate neighbor lookups
- This ensures we're not accidentally looking ahead in the spiral

### 7. Performance Tests

#### Test 7.1: Execution Time
**Purpose**: Verify reasonable performance
**Expected**:
- For threshold 289326, expect ~100-1000 iterations
- Should complete in < 1 second
**Verification**: Time the execution

#### Test 7.2: Memory Usage
**Purpose**: Ensure no memory issues
**Expected**:
- Dictionary size should be reasonable (< 10000 entries)
- No memory leaks
**Verification**: Check grid size after execution

## Testing Workflow

### Phase 1: Unit Testing
1. Test `get_neighbor_sum()` with Tests 1.1-1.3
2. Fix any issues found
3. Verify all 8 neighbor directions are covered
4. **Recommended**: Use print statements for verification (not full pytest framework needed)

### Phase 2: Spiral Validation
1. Run Test 2.1 to validate coordinate sequence
2. Verify direction changes (Test 2.2)
3. Ensure spiral pattern is correct before testing values
4. **Debug tool**: Use visual grid printing to see spiral pattern

### Phase 3: Value Validation
1. **CRITICAL**: Run Test 3.1 (first 23 values)
2. If fails, debug value calculation and/or spiral traversal
3. Run Test 3.2 with small thresholds
4. Verify termination logic works correctly

### Phase 4: Final Verification
1. Run Test 4.1 with actual input (289326)
2. **Enhanced**: Verify previous value ≤ 289326 < result
3. Verify result is reasonable and > threshold
4. Run performance tests (7.1, 7.2)
5. **Regression**: Save the correct answer for future verification

### Phase 5: Edge Cases
1. Run all edge case tests (5.1-5.4)
2. Verify boundary conditions handled correctly

### Testing Implementation Approach
For this puzzle-solving script, use **inline verification** rather than formal test framework:
- Add debug prints during development
- Create a separate `verify()` function that runs all checks
- Use assertions for critical checks (can be removed in final version)
- Visual grid printing for debugging spiral pattern

Example structure:
```python
def verify_solution():
    # Test 3.1: First 23 values
    expected = [1, 1, 2, 4, 5, 10, 11, 23, 25, 26, ...]
    # Run and compare

    # Test small thresholds
    # etc.
```

## Success Criteria

**Minimum Requirements**:
- ✓ Test 3.1 passes (first 23 values match example)
- ✓ Test 4.1 produces result > 289326
- ✓ Program terminates in < 1 second
- ✓ No crashes or infinite loops

**Full Validation**:
- ✓ All unit tests pass
- ✓ Spiral traversal matches expected pattern
- ✓ All edge cases handled correctly
- ✓ Value sequence exactly matches problem example

## Debug Strategies

**If value sequence is wrong**:
1. Print first 10 coordinates to verify spiral traversal
2. Print first 10 values with their coordinates
3. Manually verify neighbor sums for first few squares
4. Check neighbor offset calculations
5. **Visual debugging**: Implement and use `print_grid()` to see the spiral pattern in 2D
6. Compare against worked example in implementation plan (iterations 1-6)

**If spiral order is wrong**:
1. Verify direction vectors: [(1,0), (0,1), (-1,0), (0,-1)]
2. Check step counting logic (1,1,2,2,3,3,...)
3. Verify direction change happens at right time (AFTER movement, not before)
4. Print direction changes with coordinates
5. **Common off-by-one errors**:
   - Not handling (0,0) before loop starts
   - Turning before moving vs. turning after moving
   - Resetting steps_taken at wrong time
   - Incrementing steps_in_direction at wrong time

**If program doesn't terminate**:
1. Add iteration counter and print every 100 iterations
2. Verify threshold comparison is correct (> not >=)
3. Check that values are actually increasing (should grow exponentially)
4. Add safety limit (e.g., stop after 10000 iterations with error message)
5. Print last few values generated to see if growth pattern is correct

**Visual Grid Debug Function**:
```python
def print_grid(grid, size=5):
    """Print grid centered at (0,0) for visual inspection"""
    for y in range(size, -size-1, -1):
        row = []
        for x in range(-size, size+1):
            if (x, y) in grid:
                row.append(f"{grid[(x, y)]:>5}")
            else:
                row.append("    .")
        print(" ".join(row))
```
Use this to visually verify the spiral pattern matches the expected grid.
