# Testing Plan: Network Packet Routing - Step Count (Part 2)

## Overview
This testing plan ensures the step-counting solution correctly counts every position visited along the path. Since we're reusing the Part 1 path-following algorithm, we focus on verifying the step count is accurate.

## Key Testing Focus Areas

Given that Part 2 reuses 95% of Part 1's code, testing focuses on:

1. **Step counting correctness** - Verify every position is counted exactly once
2. **Off-by-one prevention** - Ensure starting and ending positions are both counted
3. **Example validation** - Must produce exactly 38 for the problem's example
4. **Relationship with Part 1** - Step count should be significantly larger than letter count
5. **Edge cases** - Minimal paths, single positions, straight paths

**Critical implementation detail to verify**: The step counter increments BEFORE checking for the next move, not after.

## Test Categories

### 1. Example Test (Primary Validation)

**Purpose**: Verify the solution matches the known correct answer from the problem statement.

**Test Case**: Example diagram from the problem
```
     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
```

**Expected Result**: 38 steps

**How to Test**:
1. Create a file `test_example.txt` with the example diagram
2. Modify the script temporarily to read from `test_example.txt`
3. Run the script
4. Verify output is exactly `38`

**Validation Method**: Manual trace by directional segments (from problem statement)
- 6 steps down (including the first line at the top)
- 3 steps right
- 4 steps up
- 3 steps right
- 4 steps down
- 3 steps right
- 2 steps up
- 13 steps left (including the F it stops on)
- **Total: 6 + 3 + 4 + 3 + 4 + 3 + 2 + 13 = 38 ✓**

**Pass Criteria**: Output equals 38

---

### 2. Actual Input Test

**Purpose**: Solve the actual puzzle input and verify it produces a reasonable answer.

**Test Case**: The full routing diagram from `input.md`

**Expected Result**:
- Should be a positive integer
- Likely in the range of 5,000-50,000 based on input size
- Should be larger than the number of letters collected in Part 1 (9 letters: LOHMDQATP)

**How to Test**:
1. Run the script with the actual input: `python solution.py`
2. Verify output is a positive integer
3. Verify output is reasonable given the grid size (~200 rows)

**Validation Method**: Cross-reference with Part 1
- Part 1 collected 9 letters across its path
- Part 2 should count significantly more steps (the entire path length)
- The path includes all letters plus all `-`, `|`, and `+` characters

**Pass Criteria**:
- Output is a positive integer
- Output > 100 (minimum reasonable path length)
- Output < 100,000 (maximum reasonable given grid size)

---

### 3. Implementation Verification Checklist

**Purpose**: Code review to verify that steps are counted correctly for specific scenarios.

**Note**: These are code inspections, not executable tests. Review the implementation to ensure:

#### Verification 3a: Starting Position Included
**Check**: The very first position should be counted as step 1

**What to verify in code**:
- In the example, the first `|` at the top is step 1
- The algorithm should increment steps immediately upon entering the while loop
- The step counter starts at 0 and increments BEFORE checking for next move

**Code to inspect**: Check that `steps += 1` occurs before `get_next_position()`

**Why this matters**: If we increment after the move, we'd miss the starting position

#### Verification 3b: Ending Position Included
**Check**: The final position (where the path ends) should be counted

**What to verify in code**:
- In the example, `F` is the last position and should be counted
- The algorithm counts the position before breaking from the loop
- When `get_next_position()` returns `None`, we break, but we've already counted the current position

**Code to inspect**: Verify the increment happens before the break condition

**Why this matters**: If we increment after checking next move, we'd miss the final position

#### Verification 3c: Letters Count as Steps
**Check**: Letter positions should be counted just like any other path character

**What to verify in code**:
- In the example, A, B, C, D, E, F are all part of the 38 steps
- The algorithm should NOT skip letters or treat them specially
- Letters are path characters and contribute to the step count

**Code to inspect**: Ensure no special logic excludes letters from step count (unlike Part 1 which collected them)

#### Verification 3d: Corners Count as Steps
**Check**: `+` characters should be counted as steps

**What to verify in code**:
- In the example, each `+` is a step
- The algorithm treats `+` as any other path character

**Code to inspect**: Verify `+` is treated uniformly (no special casing)

---

### 4. Edge Case Testing

#### Test 4a: Minimal Path
**Purpose**: Test a very short path

**Test Case**: Create file `test_minimal.txt` with exact content:
```
|
A
|
```
(3 lines: vertical bar, letter A, vertical bar)

**Expected Result**: 3 steps
- Step 1: First `|` (starting position in row 0)
- Step 2: `A`
- Step 3: Last `|` (final position, no next move)

**How to Test**:
1. Create test file with content above
2. Modify script to read from `test_minimal.txt`
3. Run and verify output

**Pass Criteria**: Output equals 3

**Notes**: This also validates `find_start()` works for single-column paths

#### Test 4b: Straight Path (No Turns)
**Purpose**: Test a path with no corners

**Test Case**: Create file `test_straight.txt`:
```
|
|
|
|
|
```
(5 lines, all vertical bars)

**Expected Result**: 5 steps

**How to Test**: Create test file and run
**Pass Criteria**: Output equals 5

**Notes**: Tests purely vertical movement without any turns

#### Test 4c: Path with Multiple Letters
**Purpose**: Verify all letters are counted as steps (not collected)

**Test Case**: Create file `test_letters.txt`:
```
|
A
B
C
|
```
(5 lines: bar, A, B, C, bar)

**Expected Result**: 5 steps

**How to Test**: Create test file and run
**Pass Criteria**: Output equals 5

**Notes**: Unlike Part 1 which collected 3 letters, Part 2 counts all 5 positions equally

#### Test 4d: Single Position Path
**Purpose**: Test edge case of path with no continuation

**Test Case**: Create file `test_single.txt`:
```
|
```
(Single line with just a vertical bar)

**Expected Result**: 1 step
- Step 1: The `|` position
- No valid next move, so break immediately

**How to Test**: Create test file and run
**Pass Criteria**: Output equals 1

**Notes**: This is the absolute minimal valid path; tests that we count before checking next move

---

### 5. Algorithm Reuse Validation

**Purpose**: Confirm Part 1 algorithm behavior is preserved

**Test Cases**:
- Verify the Part 2 solution follows the exact same path as Part 1
- The path should visit positions in the same order

**How to Test**:
1. Add debug logging to both Part 1 and Part 2 to print (row, col) for each position
2. Run both solutions on the same input
3. Compare the position sequences

**Expected Result**:
- Both should visit identical positions in identical order
- Part 2 simply counts these positions instead of extracting letters

**Pass Criteria**: Position sequences match exactly

---

### 6. Comparison with Part 1

**Purpose**: Ensure Part 2 is a valid extension of Part 1

**Test**:
1. Run Part 1 solution on the example → should get "ABCDEF" (6 letters)
2. Run Part 2 solution on the example → should get 38 steps
3. Verify the relationship between step count and letter count

**Expected Relationship**:
- Part 2 step count should be SIGNIFICANTLY larger than Part 1 letter count
- Each letter in Part 1 is just one of many steps in Part 2
- Ratio should be at least 3-5x (for example: 38 steps / 6 letters ≈ 6.3x)

**Pass Criteria**:
- Step count > letter count (weak check)
- Step count ≥ letter count × 3 (stronger check)
- For the example: 38 ≥ 6 × 3 = 18 ✓
- For actual input: steps ≥ 9 × 3 = 27 (Part 1 found 9 letters: LOHMDQATP)

**Why this matters**: If step count is only slightly larger than letter count, something is wrong with the counting logic

---

### 7. Code Quality Checks

**Purpose**: Ensure the code is correct and maintainable

**Checks**:
1. [ ] No infinite loops (verified by Part 1 working correctly)
2. [ ] Proper termination condition (when `get_next_position()` returns None)
3. [ ] No off-by-one errors in step counting
4. [ ] Grid parsing handles variable-width lines (inherited from Part 1)
5. [ ] Starting position correctly identified (inherited from Part 1)
6. [ ] Step counter placement: `steps += 1` before `get_next_position()`
7. [ ] No accidental letter collection logic remaining from Part 1

**How to Test**: Code review and inspection

**Pass Criteria**: All checks pass

---

### 8. Performance Validation (Optional)

**Purpose**: Verify the solution runs efficiently

**Test**: Add timing to measure execution speed
```python
import time
start = time.time()
result = follow_path(grid, start[0], start[1])
elapsed = time.time() - start
print(f"Result: {result}")
print(f"Time: {elapsed:.3f} seconds")
```

**Expected Performance**:
- Should complete in well under 1 second (likely < 0.1 seconds)
- O(n) complexity where n is path length

**Pass Criteria**: Execution time < 1 second for actual input

---

## Testing Workflow

### Phase 1: Quick Validation
1. Run the example test → must get 38
2. If successful, proceed to Phase 2
3. If failed, debug the step counting logic

### Phase 2: Actual Solution
1. Run on actual input (`input.md`)
2. Verify output is a reasonable positive integer
3. Record the answer

### Phase 3: Edge Case Verification (Recommended)
1. Create minimal test cases (4a, 4b, 4c, 4d)
2. Run each and verify expected step counts
3. If all pass, high confidence in correctness
4. These tests are quick to create and run, providing additional validation

### Phase 4: Cross-Reference
1. Compare Part 2 output with Part 1 output
2. Verify Part 2 count > Part 1 letter count
3. Ensure both use the same input and path

---

## Expected Test Results Summary

| Test | Input | Expected Output | Importance |
|------|-------|----------------|------------|
| Example | Problem diagram | 38 | Critical |
| Actual Input | input.md | Positive integer (likely 5,000-50,000, definitely > 100) | Critical |
| Minimal Path (4a) | 3-line vertical path with letter | 3 | Medium |
| Straight Path (4b) | 5 vertical bars | 5 | Medium |
| Multiple Letters (4c) | 5-line path with 3 letters | 5 | Medium |
| Single Position (4d) | Just one `\|` | 1 | Medium |
| Part 1 Comparison | Same input as Part 1 | Steps ≥ 9 × 3 = 27 | High |

---

## Debugging Strategy (If Tests Fail)

### If Example Test Fails:

**Problem**: Output ≠ 38

**Potential Issues**:
1. **Output = 37**: Not counting starting position
   - Fix: Ensure `steps += 1` happens before checking `get_next_position()`
2. **Output = 39+**: Counting extra positions
   - Fix: Ensure we break immediately when `get_next_position()` returns None
3. **Output is way off**: Path-following logic broken
   - Fix: Compare with Part 1 solution; ensure no accidental modifications

**Debug Steps**:
1. Add print statements to log each (row, col) visited
2. Manually count the positions in the output
3. Compare with the expected path from the problem
4. Identify where the count diverges

### If Actual Input Test Fails:

**Problem**: Output seems unreasonable

**Debug Steps**:
1. Verify the grid is parsed correctly (check dimensions)
2. Verify starting position is found (should be in row 0)
3. Add logging to see the path being followed
4. Compare path with Part 1 solution to ensure they match
5. Count steps manually for a small section to verify increment logic

---

## Success Criteria

The solution is considered correct if:
1. [ ] Example test produces exactly 38
2. [ ] Actual input produces a reasonable positive integer (likely 5,000-50,000)
3. [ ] Code inspection shows correct step counting logic (count before move)
4. [ ] Step count is at least 3x the letter count from Part 1 (steps ≥ 27 for actual input)
5. [ ] All edge case tests pass (if run)
6. [ ] No off-by-one errors in step counting
7. [ ] Implementation verification checklist items all pass

---

## Final Validation

Before submitting the answer:
1. Run the solution one final time on `input.md`
2. Verify the output is printed clearly (just the integer)
3. Visually inspect the output to ensure it's reasonable
4. Submit with confidence!
