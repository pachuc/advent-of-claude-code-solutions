# Test Plan: Marble Circle Game Part 2

## Testing Strategy

Since Part 2 uses the same algorithm as Part 1 with only the input scale changed, testing focuses on:
1. **CRITICAL**: Regression testing against Part 1 to validate algorithm correctness
2. Verifying the 100x multiplication is applied correctly
3. Establishing sanity bounds for the Part 2 answer
4. Validating output format

## Test Categories

### 1. **CRITICAL - Part 1 Regression Tests** (Must Pass Before Running Part 2)

**Purpose**: Validate that the copied algorithm is still correct

**Test Case 1.1**: Verify Part 1 answer without multiplication
- **Method**: Temporarily remove the `* 100` line from main()
- **Input**: 463 players, 71787 marbles (original values)
- **Expected**: 396136 (Part 1 answer from part_1_answer.txt)
- **Status**: MANDATORY - DO NOT PROCEED if this fails

**Test Case 1.2**: Run all Part 1 example test cases
- **Method**: Test with the following inputs (without 100x multiplication)
- **Test cases**:
  - 9 players, 25 marbles → expected 32
  - 10 players, 1618 marbles → expected 8317
  - 13 players, 7999 marbles → expected 146373
  - 17 players, 1104 marbles → expected 2764
  - 21 players, 6111 marbles → expected 54718
  - 30 players, 5807 marbles → expected 37305
- **Expected**: All should match exactly
- **Status**: MANDATORY - Validates algorithm correctness

### 2. Input Parsing and Multiplication Verification

**Purpose**: Verify that the last marble value is correctly multiplied by 100

**Test Case 2.1**: Verify multiplication is applied
- **Method**: Add temporary print statement: `print(f"Players: {num_players}, Last marble: {last_marble}")`
- **Expected output**: "Players: 463, Last marble: 7178700"
- **Verification**: Confirms multiplication happened before simulation

**Test Case 2.2**: Verify player count unchanged
- **Expected**: num_players = 463 (not multiplied)
- **Verification**: Visual check of printed values

### 3. Incremental Multiplier Tests (Sanity Check)

**Purpose**: Verify score increases monotonically with larger inputs

**Test Case 3.1**: Test with smaller multipliers
- **Method**: Temporarily change multiplication factor to verify behavior
- **Test scenarios**:
  - Multiplier = 2: 463 players, 143574 marbles
  - Multiplier = 5: 463 players, 358935 marbles
  - Multiplier = 10: 463 players, 717870 marbles
- **Expected**: Scores should increase monotonically
- **Verification**: Each larger multiplier should produce a higher score
- **Status**: Optional but recommended for confidence

**Test Case 3.2**: Manual trace for tiny example
- **Method**: Run with a very small example that can be manually verified
- **Example**: 3 players, last marble 50 (or 100)
- **Purpose**: Spot-check a few marble placements to verify scoring logic
- **Status**: Optional - provides additional confidence

### 4. Part 2 Answer Sanity Bounds

**Purpose**: Establish that the Part 2 answer is reasonable

**Test Case 4.1**: Minimum expected score
- **Part 1 baseline**: 463 players, 71787 marbles → score = 396,136
- **Part 2**: 463 players, 7,178,700 marbles (100x more)
- **Conservative estimate**: Score should be **at least 10x higher** = 3,960,000+
- **Likely range**: 20-100x higher due to more scoring opportunities
- **Expected**: Answer should be **at minimum 3.96 million**, likely much higher

**Test Case 4.2**: Score reasonableness check
- **With 100x more marbles**: More multiples of 23 = more scoring opportunities
- **Special placements**: ~312,117 special placements (vs ~3,121 in Part 1)
- **Expected magnitude**: Scores in the tens of millions are reasonable
- **Red flag**: If score < 3.96M, something is wrong

### 5. Output Format Validation

**Test Case 5.1**: Output is single integer
- **Expected**: One line containing only the integer result
- **Verification**: No extra text, debug output, or whitespace
- **Method**: Ensure all debug prints are removed before final run

**Test Case 5.2**: Output is positive integer
- **Expected**: Single positive integer > 3,960,000
- **Verification**: Visual inspection

## Testing Execution Plan

### Phase 1: CRITICAL Regression Testing (MUST DO FIRST)
**Do not proceed to Phase 2 until all these tests pass**

1. **Test Case 1.1**: Run solution without multiplication on Part 1 input
   - Temporarily comment out `last_marble = last_marble * 100`
   - Run with actual input (463 players, 71787 marbles)
   - **Expected**: Output = 396136
   - **Status**: MANDATORY PASS

2. **Test Case 1.2**: Run Part 1 example test cases
   - Test all 6 example cases from Part 1 problem
   - **Expected**: All match exactly
   - **Status**: MANDATORY PASS

3. **Verify**: If both pass, algorithm is correct. Re-enable multiplication and proceed.

### Phase 2: Multiplication Verification
1. Add temporary debug print: `print(f"DEBUG: {num_players} players, {last_marble} marbles")`
2. Run solution.py
3. **Expected first line**: "DEBUG: 463 players, 7178700 marbles"
4. Remove debug print after verification

### Phase 3: Main Execution
1. Execute: `python solution.py`
2. Expected runtime: 2-5 minutes
3. Capture output

### Phase 4: Output Validation
1. **Format**: Output should be single integer, no extra text
2. **Sanity check**: Output > 3,960,000 (at least 10x Part 1 score)
3. **Reasonableness**: Likely in range of 10M-100M

### Phase 5: Optional Confidence Tests (if suspicious)
1. Test with smaller multipliers (2x, 5x, 10x) - verify monotonic increase
2. Manual trace small example (3 players, 50-100 marbles)

## Success Criteria

The solution is correct if ALL of the following are true:

### Mandatory Criteria (Must Pass)
1. ✅ **Part 1 regression test passes** (Test Case 1.1) - OUTPUT = 396136
2. ✅ **Part 1 examples pass** (Test Case 1.2) - All 6 match
3. ✅ **Multiplication verified** - Debug shows 7,178,700 marbles
4. ✅ **Execution completes** - No errors or crashes
5. ✅ **Output format correct** - Single integer only
6. ✅ **Sanity bound met** - Output ≥ 3,960,000

### Secondary Criteria (Nice to Have)
- ⭕ Runtime < 5 minutes (acceptable even if longer)
- ⭕ Memory < 1GB (should be ~300-500MB)

## Verification Logic

**Why we can trust the answer without knowing the expected result:**

1. **Regression tests prove algorithm correctness**: If Part 1 test cases pass, the marble game simulation is implemented correctly
2. **Multiplication is trivial to verify**: Debug print confirms 100x multiplication
3. **Sanity bounds catch major errors**: Score < 3.96M indicates a bug
4. **Monotonic increase (optional test)**: Smaller multipliers should give smaller scores

## Key Test Scenarios Summary

| Priority | Test | Input | Expected | Purpose |
|----------|------|-------|----------|---------|
| **CRITICAL** | Part 1 regression | 463 players, 71787 marbles | 396136 | Proves algorithm is correct |
| **CRITICAL** | Part 1 examples | 6 test cases | All match | Validates implementation |
| **HIGH** | Multiplication check | Debug print | 7178700 marbles | Confirms 100x applied |
| **HIGH** | Sanity bound | Full Part 2 | ≥ 3,960,000 | Catches major errors |
| **MEDIUM** | Output format | Final output | Single integer | Submission format |
| Optional | Incremental test | 10x multiplier | Monotonic | Additional confidence |

## Debugging Strategy

**If Part 1 regression fails (Test 1.1 or 1.2)**:
- Problem: Code was not copied correctly from Part 1
- Solution: Re-copy part_1_solution.py exactly

**If Part 2 score < 3,960,000**:
- Check: Is multiplication actually applied? (debug print)
- Check: Is multiplication in correct location? (after parse, before simulate)
- Check: Any accidental division or modulo errors?

**If Part 2 score seems extremely high (> 1 billion)**:
- Unlikely but possible
- Double-check: No double-counting of scores
- Verify: Only one `* 100` multiplication

**If runtime > 10 minutes**:
- Check: Using deque (not list)
- Check: No debug=True parameter passed
- Note: 5-10 minutes is acceptable for 7.2M marbles

## Final Checklist

Before accepting the answer:
- [ ] Part 1 regression test passed (396136)
- [ ] All Part 1 examples passed
- [ ] Multiplication verified (7178700 marbles)
- [ ] Output is single integer
- [ ] Output ≥ 3,960,000
- [ ] No debug output in final run

## Summary

**This test plan prioritizes regression testing as the primary validation method.** Since Part 1 is known to be correct, proving that Part 2 uses the same algorithm (via regression tests) combined with verifying the 100x multiplication provides high confidence in the answer without needing the expected result.
