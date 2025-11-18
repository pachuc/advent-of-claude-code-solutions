# Test Plan: Spreadsheet Evenly Divisible Values (Part 2)

## Testing Objective
Verify that the solution correctly identifies evenly divisible pairs in each row and calculates the correct sum across all rows.

## Test Strategy Overview
1. Validate with the provided example from problem statement
2. Test the pair-finding logic with edge cases
3. Verify correct handling of file parsing
4. Run against actual input and validate result format
5. Sanity check the final answer

## Test 1: Provided Example Validation

### Purpose
Verify the algorithm works correctly with the example from `problem.md`

### Test Data
```
5 9 2 8
9 4 7 3
3 8 6 5
```

### Expected Behavior
- Row 1 [5, 9, 2, 8]: Find pair (8, 2), result = 8 // 2 = 4
- Row 2 [9, 4, 7, 3]: Find pair (9, 3), result = 9 // 3 = 3
- Row 3 [3, 8, 6, 5]: Find pair (6, 3), result = 6 // 3 = 2
- Sum: 4 + 3 + 2 = 9

### Test Steps
1. Create a test file with the example data
2. Run the solution against this file
3. Verify output is exactly `9`

### Pass Criteria
- Output matches expected value of 9

## Test 2: Single Row Edge Cases

### Purpose
Test pair-finding logic with various row configurations

### Test Cases

#### Test 2a: Minimal Row (2 numbers)
- Input: `[6, 3]`
- Expected: 6 // 3 = 2
- Validates: Minimum possible row size

#### Test 2b: Pair at Beginning
- Input: `[8, 2, 5, 7]`
- Expected: 8 // 2 = 4
- Validates: Early termination when pair found first

#### Test 2c: Pair at End
- Input: `[5, 7, 8, 2]`
- Expected: 8 // 2 = 4
- Validates: Full iteration needed to find pair

#### Test 2d: Larger Numbers
- Input: `[100, 50, 23, 17]`
- Expected: 100 // 50 = 2
- Validates: Works with larger values

#### Test 2e: Division Result Greater Than 2
- Input: `[20, 4, 7, 11]`
- Expected: 20 // 4 = 5
- Validates: Division results other than 2 or 3

### Test Steps
For each test case:
1. Create a single-row test file
2. Run solution
3. Verify output matches expected result

### Pass Criteria
- All single-row tests produce correct division results

## Test 3: File Parsing Edge Cases

### Purpose
Verify robust handling of file format variations

### Test Cases

#### Test 3a: Empty Lines
- Input file with blank lines between data rows
- Expected: Empty lines ignored, correct sum calculated
- Validates: `if line:` check works correctly

#### Test 3b: Trailing Whitespace
- Input rows with trailing spaces/tabs
- Expected: Whitespace stripped, correct parsing
- Validates: `strip()` function works

#### Test 3c: Multiple Spaces Between Numbers
- Input: `"5    9    2    8"` (multiple spaces)
- Expected: Correct parsing with `split()`
- Validates: `split()` handles multiple whitespace

### Test Steps
1. Create test files with each edge case
2. Run solution
3. Verify correct parsing and calculation

### Pass Criteria
- All file format variations parse correctly

## Test 4: Pair Detection Logic

### Purpose
Verify the nested loop correctly identifies all possible pairs regardless of position

### Test Cases

#### Test 4a: First Number Divisible
- Input: `[10, 3, 2, 7]`
- Expected: 10 // 2 = 5
- Validates: Finds pair where first number is dividend

#### Test 4b: Second Number Divisible
- Input: `[3, 15, 7, 2]`
- Expected: 15 // 3 = 5
- Validates: Finds pair where second number is dividend

#### Test 4c: Order Independence - Comprehensive
- Input rows with pair (8, 2) at different positions:
  - `[8, 2]` - positions (0, 1) - Expected: 4
  - `[2, 8]` - positions (0, 1) reversed - Expected: 4
  - `[5, 8, 2]` - positions (1, 2) - Expected: 4
  - `[8, 5, 2]` - positions (0, 2) - Expected: 4
  - `[2, 5, 8]` - positions (0, 2) reversed - Expected: 4
- Validates: Pair detection works regardless of number order or position in array

#### Test 4d: No Division by Zero
- Input: `[10, 5, 0, 2]` (contains zero)
- Expected: 10 // 5 = 2 (should find 10/5, not attempt 5/0)
- Validates: Algorithm never attempts division by zero

### Test Steps
1. Test each scenario individually
2. Verify correct pair identified
3. Verify correct division result calculated
4. Confirm zero division never occurs

### Pass Criteria
- Pair detection is order-independent
- Pair detection is position-independent
- Always finds the unique divisible pair
- No division by zero errors occur

## Test 5: Actual Input Validation

### Purpose
Run against the actual puzzle input and verify result properties

### Test Data
Use `input.md` (16 rows of real data)

### Test Steps
1. Run solution against `input.md`
2. Verify output is a single integer
3. Verify output is positive
4. Verify output is reasonable (sanity check)

### Expected Behavior
- Output format: Single integer printed to stdout
- Value should be positive
- Based on 16 rows with ~16 numbers each:
  - Minimum reasonable: ~16 (if all divisions result in 1)
  - Maximum reasonable: ~100,000 (if some large numbers divide evenly)

### Sanity Checks
- Result should be > 0
- Result should be < 1,000,000 (very conservative upper bound)
- Result should be different from Part 1 answer (39126)

### Pass Criteria
- Solution runs without errors
- Output is a single positive integer
- Output is within reasonable bounds

## Test 6: Algorithm Correctness Verification (Optional)

### Purpose
Optionally manually verify a subset of rows from actual input for additional confidence

### Test Steps (Optional - Test 1 is primary validation)
1. Select first row from `input.md`
2. Manually find the divisible pairs:
   - Row 1: `179 2358 5197 867 163 4418 3135 5049 187 166 4682 5080 5541 172 4294 1397`
   - Check pairs systematically to find which divide evenly
   - Example: 5049 / 867 = 5.82... (no), 4418 / 179 = 24.68... (no), continue...
3. Once found, verify division result
4. Compare with solution output

### Note
This test is **supplementary** to Test 1 (provided example validation). Test 1 is the critical validation test. This test provides additional confidence but is not required if Test 1 passes, since the provided example fully validates the algorithm correctness.

### Pass Criteria
- If performed, manual calculation should match solution output for tested row(s)

## Test 7: Performance Validation

### Purpose
Ensure solution completes in reasonable time

### Test Steps
1. Run solution against `input.md`
2. Measure execution time (can use `time` command: `time python solution.py`)

### Expected Performance
- Should complete in < 100 milliseconds
- With O(16 × 16²) ≈ 4,096 operations, should be nearly instantaneous
- Parsing and I/O should dominate runtime, not algorithm

### Pass Criteria
- Execution completes in under 100ms (conservative: under 1 second acceptable)
- No performance degradation compared to Part 1 solution

## Test 8: Regression Check Against Part 1

### Purpose
Verify Part 2 uses same input and parsing as Part 1, but different calculation

### Test Steps
1. Verify Part 2 reads from same `input.md` file
2. Confirm Part 2 parses 16 rows (same as Part 1)
3. Add debug output to count rows parsed (or verify through code inspection)
4. Verify Part 2 produces different answer than Part 1 (39126)
5. Verify both solutions run without errors on same input

### Verification Method
Can add temporary debug output:
```python
print(f"Rows parsed: {len(rows)}")  # Should be 16
```

### Pass Criteria
- Same input file used (`input.md`)
- Same number of rows parsed (16 rows)
- Different answer produced (Part 2 ≠ 39126, since calculation method differs)
- Both solutions successfully process the same input data

## Overall Test Execution Plan

### Phase 1: Unit Testing
1. Run Test 1 (provided example) - MUST PASS
2. Run Test 2 (single row edge cases)
3. Run Test 4 (pair detection logic)

### Phase 2: Integration Testing
1. Run Test 3 (file parsing edge cases)
2. Run Test 5 (actual input validation)

### Phase 3: Verification
1. Run Test 6 (optional manual verification of sample rows)
2. Run Test 7 (performance check)
3. Run Test 8 (regression check against Part 1)

### Success Criteria
- **Test 1 MUST pass** (provided example = 9) - This is the critical validation
- All edge case tests should pass (Tests 2-4)
- Actual input should produce valid integer output (Test 5)
- No runtime errors or exceptions
- Performance under 100ms (or at least under 1 second)
- Regression check confirms same input processing as Part 1 (Test 8)

### Priority Levels
- **Critical**: Test 1 (example validation)
- **High**: Tests 2-5 (edge cases, pair detection, actual input)
- **Medium**: Tests 7-8 (performance, regression)
- **Low**: Test 6 (optional manual verification)

## Expected Final Result
The solution should produce a single integer answer that represents the sum of division results across all 16 rows in `input.md`. This answer will be different from the Part 1 answer of 39126.
