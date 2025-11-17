# Test Plan: Safe Tile Counter (Part 2)

## Testing Overview
Since Part 2 uses the exact same algorithm as Part 1 (just with more rows), we can rely heavily on Part 1's validation. The testing focus is on:
1. Verifying the algorithm still works correctly
2. Ensuring the scale increase is handled properly
3. Basic sanity checks on the output

## Test Strategy

### 1. Algorithm Correctness Tests

#### Test 1.1: Small Example Verification
**Purpose**: Verify the core algorithm hasn't been broken during adaptation

**Test Case**: Use the example from Part 1 problem
- Input: `..^^.`
- Rows: 3
- Expected output: 6 safe tiles

**Steps**:
1. Modify `main()` temporarily to use test input
2. Set rows to 3
3. Manually verify:
   - Row 1: `..^^.` → 3 safe tiles
   - Row 2: `.^^^^` → 1 safe tile
   - Row 3: `^^..^` → 2 safe tiles
   - Total: 6 safe tiles

**Pass criteria**: Output equals 6

#### Test 1.2: Part 1 Regression Test
**Purpose**: Ensure Part 1 answer is still correct with reused code

**Test Case**:
- Input: actual input from `input.md`
- Rows: 40
- Expected output: 1989 (from `part_1_answer.txt`)

**Steps**:
1. Modify `main()` to use 40 rows instead of 400,000
2. Run with actual input
3. Compare output to 1989

**Pass criteria**: Output equals 1989

### 2. Boundary and Edge Case Tests

#### Test 2.1: Single Row
**Purpose**: Test minimal case

**Test Case**:
- Input: any valid row (e.g., `..^^.`)
- Rows: 1
- Expected: Count of safe tiles in that row only

**Steps**:
1. Set rows to 1
2. Use input `..^^.` (3 safe tiles)
3. Verify output is 3

**Pass criteria**: Output equals number of `.` in input row

#### Test 2.2: Trap Rule Verification
**Purpose**: Verify the `left != right` rule works correctly

**Test Case**: Manual spot checks on generated rows
- Input: `.^.^.`
- Rows: 2

**Steps**:
1. Calculate second row manually:
   - Position 0: left=`.`, right=`^` → trap (left≠right) → `^`
   - Position 1: left=`.`, right=`.` → safe (left=right) → `.`
   - Position 2: left=`^`, right=`^` → safe (left=right) → `.`
   - Position 3: left=`.`, right=`.` → safe (left=right) → `.`
   - Position 4: left=`^`, right=`.` → trap (left≠right) → `^`
   - Row 2: `^...^`
2. Add print statement to verify row 2 matches `^...^`
3. Count: Row 1 has 3 safe, Row 2 has 3 safe → total 6

**Pass criteria**: Row 2 matches manual calculation

#### Test 2.3: Boundary Handling (Out of Bounds = Safe)
**Purpose**: Verify edges are treated as safe tiles

**Test Case**:
- Input: `^....` (trap at left edge)
- Rows: 2

**Steps**:
1. Manually calculate row 2, position 0:
   - left=`.` (out of bounds, treated as safe)
   - center=`^`
   - right=`.`
   - left≠right? `.`≠`.` = False → safe → `.`
2. Verify first character of row 2 is `.`

**Pass criteria**: Edge positions correctly treat out-of-bounds as safe

### 3. Scale Tests

#### Test 3.1: Intermediate Scale Test
**Purpose**: Test with moderate row count before full 400k

**Test Case**:
- Input: actual input from `input.md`
- Rows: 1,000
- Expected: Some reasonable number > 1989

**Steps**:
1. Run with 1,000 rows
2. Verify it completes in reasonable time (< 1 second)
3. Verify output is a positive integer
4. Verify output > 1989 (more rows = more tiles)

**Pass criteria**:
- Completes successfully
- Output is proportionally larger than Part 1

#### Test 3.2: Extrapolation for Sanity Bounds
**Purpose**: Establish tighter bounds for Part 2 answer using intermediate scales

**Test Case**: Build confidence interval from multiple scale tests
- Run with 40, 400, 4,000, 40,000 rows
- Extrapolate to 400,000 rows
- Use this to validate final answer

**Steps**:
1. Run with 40 rows → get count C1 (should be 1989)
2. Run with 400 rows → get count C2
3. Run with 4,000 rows → get count C3
4. Run with 40,000 rows → get count C4
5. Calculate average tiles per row: C4 / 40,000
6. Extrapolate: expected_answer ≈ (C4 / 40,000) × 400,000
7. Use ±5% tolerance for final validation

**Pass criteria**: Final answer is within ±5% of extrapolated value

**Note**: Cellular automata patterns may have transient behavior initially, then stabilize to a consistent ratio. The 40,000-row test should give a stable ratio.

### 4. Full Solution Test

#### Test 4.1: Part 2 Full Execution
**Purpose**: Run the actual Part 2 solution

**Test Case**:
- Input: actual input from `input.md`
- Rows: 400,000
- Expected: Single positive integer output

**Steps**:
1. Run solution with 400,000 rows
2. Monitor execution time (should be < 30 seconds)
3. Verify output is a single integer
4. Verify output is significantly larger than 1989

**Pass criteria**:
- Completes in reasonable time
- Outputs single integer
- Output > 1,000,000 (rough sanity check)

#### Test 4.2: Output Format Validation
**Purpose**: Ensure output format is correct

**Steps**:
1. Run solution
2. Verify output is only a number (no extra text)
3. Verify it's on a single line
4. Verify it's a valid integer (no decimals, no scientific notation)

**Pass criteria**: Output is a plain integer

### 5. Sanity Checks

#### Test 5.1: Input Integrity
**Purpose**: Verify input file is read correctly

**Steps**:
1. Add debug print of first row after reading
2. Verify it matches expected: `.^^^^^.^^.^^^.^...^..^^.^.^..^^^^^^^^^^..^...^^.^..^^^^..^^^^...^.^.^^^^^^^^....^..^^^^^^.^^^.^^^.^^`
3. Verify length is 100 characters

**Pass criteria**: Input matches expected string

#### Test 5.2: Row Generation Doesn't Change Length
**Purpose**: Ensure all rows have same length as input

**Steps**:
1. Add assertion: `assert len(next_row) == len(current_row)`
2. Run with 100 rows
3. Verify no assertion errors

**Pass criteria**: All generated rows maintain input length

#### Test 5.3: Safe Count Reasonableness (Updated with Tighter Bounds)
**Purpose**: Verify count is in expected range using extrapolation

**Test Case**:
- Use results from Test 3.2 to extrapolate expected value
- Apply ±5% tolerance (tighter than original ±25%)

**Steps**:
1. Run full solution
2. Compare to extrapolated value from Test 3.2
3. Check output is within ±5% of extrapolation

**Pass criteria**: Output is within expected range based on extrapolation

**Fallback**: If Test 3.2 not run, use absolute bounds [0 < output < 40,000,000]

#### Test 5.4: Absolute Bounds Check
**Purpose**: Verify output is within trivial mathematical bounds

**Test Case**:
- Maximum possible: 400,000 rows × 100 chars = 40,000,000 (all safe)
- Minimum possible: 0 (all traps)
- Realistic minimum: > 1989 (more rows than Part 1)

**Steps**:
1. Verify: output > 1989
2. Verify: output < 40,000,000
3. Verify: output > 0

**Pass criteria**: All three bounds checks pass

#### Test 5.5: Row Count Verification (CRITICAL)
**Purpose**: Verify exactly 400,000 rows are processed

**Test Case**: Ensure no typos in row count (400,000 vs 40,000 vs 4,000,000)

**Steps**:
1. Add debug output in `count_safe_tiles()` showing final row number
2. OR add assertion after loop: `assert row_num == total_rows - 1`
3. For 400,000 rows, final row_num should be 399,999 (0-indexed)

**Pass criteria**: Verification shows exactly 400,000 rows processed

**Implementation**:
```python
# In count_safe_tiles, after loop:
assert row_num == total_rows - 1, f"Expected to process {total_rows} rows, but stopped at row {row_num}"
```

### 6. Performance Tests

#### Test 6.1: Execution Time
**Purpose**: Ensure solution runs in reasonable time

**Steps**:
1. Time the execution using `time python solution.py`
2. Verify completion in < 30 seconds

**Pass criteria**: Completes in under 30 seconds

#### Test 6.2: Memory Usage (Optional)
**Purpose**: Verify memory stays constant

**Steps**:
1. Monitor memory during execution (e.g., with `/usr/bin/time -v`)
2. Verify memory doesn't grow linearly with row count

**Pass criteria**: Memory usage stays under 100 MB

## Test Execution Order

1. **First**: Test 1.2 (Part 1 regression) - if this fails, algorithm is broken
2. **Second**: Test 1.1 (small example) - validates basic functionality
3. **Third**: Test 5.1 (input integrity) - validates input is correct
4. **Fourth**: Test 5.5 (row count verification) - CRITICAL - ensures 400,000 rows processed
5. **Fifth**: Test 2.2 (trap rule) - validates core logic
6. **Sixth**: Test 3.2 (extrapolation) - establishes expected bounds
7. **Seventh**: Test 4.1 (full solution) - the actual answer
8. **Eighth**: Test 5.3 (sanity check with tight bounds) - validates reasonableness
9. **Finally**: Test 5.4 (absolute bounds) - final verification

## Required Test Cases (Minimum)

For a script-level solution, we must validate:

1. ✅ **Part 1 regression test** (Test 1.2) - CRITICAL
2. ✅ **Row count verification** (Test 5.5) - CRITICAL (prevents 400k vs 40k typo)
3. ✅ **Small example test** (Test 1.1) - CRITICAL
4. ✅ **Input integrity** (Test 5.1) - IMPORTANT
5. ✅ **Absolute bounds check** (Test 5.4) - IMPORTANT
6. ✅ **Full solution execution** (Test 4.1) - CRITICAL

The other tests (extrapolation, tight bounds) are highly recommended for additional confidence but not strictly necessary for a working solution.

## Manual Verification Strategy

Since we can't verify the Part 2 answer directly (no known solution), we validate through:
1. **Algorithm correctness**: Part 1 works, Part 2 uses same algorithm
2. **Consistency**: Intermediate scales show linear growth
3. **Sanity bounds**: Output is in reasonable expected range
4. **No errors**: Code runs to completion without exceptions

## Common Issues to Watch For

| Issue | Detection | Resolution |
|-------|-----------|------------|
| Wrong row count parameter | Test 5.5 fails | Verify parameter is exactly 400,000 not 40,000 |
| Off-by-one in rows | Row count assertion fails | Check range in loop and final row_num |
| String immutability issues | Slow performance | Verify using list + join |
| File reading error | Test 5.1 fails | Check file path and parsing |
| Input validation missing | Silent failure | Add assertions for length and valid chars |
| Integer overflow | Incorrect output | Not a risk in Python |
| Typo in row count | Output order of magnitude wrong | Use Test 5.5 to catch early |

## Success Criteria

The solution is considered correct if:
1. ✅ Part 1 regression test passes (outputs 1989 for 40 rows)
2. ✅ Row count verification confirms exactly 400,000 rows processed
3. ✅ Small example test passes (outputs 6 for `..^^.` with 3 rows)
4. ✅ Input validation passes (100 chars, only '.^' characters)
5. ✅ Full solution completes in < 30 seconds
6. ✅ Absolute bounds check passes (1989 < output < 40,000,000)
7. ✅ Output is within ±5% of extrapolated value from intermediate scales (if Test 3.2 run)
8. ✅ Code runs without errors or exceptions

## Notes

- **No unit tests framework needed** - simple script with print statements suffices
- **No automated test harness** - manual execution is fine
- **No edge case exhaustion** - the algorithm is simple and Part 1 validated it
- **Focus on regression and sanity** - this is the pragmatic approach for a puzzle solution
