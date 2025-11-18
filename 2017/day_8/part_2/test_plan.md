# Test Plan - Part 2: Maximum Value During Execution

## Testing Objectives
1. Verify the solution correctly tracks maximum values during execution (not just final state)
2. Ensure the modification from Part 1 is correct
3. Validate against the provided example
4. Test edge cases specific to tracking intermediate maxima

## Test Strategy

### 1. Example Test (From Problem Statement)
**Purpose**: Validate basic correctness against known example

**Input**:
```
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
```

**Expected Execution Trace**:
- Instruction 1: `b inc 5 if a > 1` → a=0, condition false, no change. Registers: {}, max=0
- Instruction 2: `a inc 1 if b < 5` → b=0, condition true, a=1. Registers: {a:1}, max=1
- Instruction 3: `c dec -10 if a >= 1` → a=1, condition true, c=10. Registers: {a:1, c:10}, max=10
- Instruction 4: `c inc -20 if c == 10` → c=10, condition true, c=-10. Registers: {a:1, c:-10}, max=10

**Expected Output**: `10`

**Validation**:
- Create a test file with the example input
- Run solution
- Verify output is exactly `10`
- **Critical**: This demonstrates max was 10 during execution even though final max is only 1

### 2. Comparison with Part 1 Answer
**Purpose**: Ensure Part 2 answer is valid and logical

**Test**: Run solution on actual `input.md`

**Expected Properties**:
- Part 2 answer ≥ Part 1 answer (5221)
- Part 2 answer ≥ 5221 (since final state is one of the intermediate states)
- Part 2 answer should be reasonable (likely between 5221 and ~10000 given input size)

**Validation**:
```bash
python part_2_solution.py > part_2_output.txt
# Check that output >= 5221
```

### 3. Edge Case: All Negative Values
**Purpose**: Verify correct handling when all register values are negative

**Input**:
```
a dec 100 if b == 0
b dec 50 if a < 0
```

**Expected Execution**:
- Instruction 1: b=0, condition true, a=-100. max=0 (initial state better)
- Instruction 2: a=-100, condition true, b=-50. max=0

**Expected Output**: `0`

**Rationale**: All registers start at 0 (implicit initial state). Since all modifications result in negative values and we never exceed the initial 0, the maximum is 0. This validates that our initialization of `max_value_ever = 0` is correct - we're treating the implicit initial state (all registers at 0) as the baseline

### 4. Edge Case: Peak Early, Then Decline
**Purpose**: Verify maximum tracking across decreasing values

**Input**:
```
a inc 1000 if b == 0
a dec 999 if b == 0
```

**Expected Execution**:
- Instruction 1: b=0, condition true, a=1000. max=1000
- Instruction 2: b=0, condition true, a=1. max=1000

**Expected Output**: `1000`

**Rationale**: Peak occurred at instruction 1, should be retained even after decrease

### 5. Edge Case: Multiple Peaks
**Purpose**: Verify last maximum is used when there are ties

**Input**:
```
a inc 500 if b == 0
c inc 500 if b == 0
d inc 500 if b == 0
```

**Expected Execution**:
- All three instructions trigger, creating a=500, c=500, d=500
- max=500 throughout

**Expected Output**: `500`

### 6. Edge Case: Maximum at Final State
**Purpose**: Verify system works when peak occurs at the end (Part 2 == Part 1)

**Input**:
```
a inc 100 if b == 0
a inc 50 if b == 0
```

**Expected Execution**:
- Instruction 1: b=0, condition true, a=100. max=100
- Instruction 2: b=0, condition true, a=150. max=150

**Expected Output**: `150`

**Rationale**: When the maximum occurs at the final state, Part 2 answer should equal what Part 1 would return. This tests that our tracking works correctly when values only increase.

### 7. Edge Case: Empty or No Conditions Trigger
**Purpose**: Verify behavior when no modifications occur

**Input**:
```
a inc 100 if b > 5
c dec 50 if d != 0
```

**Expected Execution**:
- Both conditions false (all registers start at 0)
- No modifications

**Expected Output**: `0`

### 8. Edge Case: Single Instruction
**Purpose**: Verify minimal case works correctly

**Input**:
```
x inc 42 if y == 0
```

**Expected Execution**:
- Instruction 1: y=0, condition true, x=42. max=42

**Expected Output**: `42`

**Rationale**: Simplest non-trivial case - single instruction that triggers.

### 9. Verbose Mode Test
**Purpose**: Verify debugging output and trace execution

**Test Procedure**:
1. Modify `main()` temporarily to set `verbose=True`
2. Run with example input
3. Check output shows progression:
   ```
   After instruction 2: a = 1, max_ever = 1
   After instruction 3: c = 10, max_ever = 10
   After instruction 4: c = -10, max_ever = 10
   10
   ```

**Validation**: Trace matches expected execution from example test

### 10. Regression Test: Part 1 Logic Still Works
**Purpose**: Ensure final state calculation wasn't broken

**Test**:
1. In `process_instructions()`, also call `find_max_register_value(registers)` on final state
2. Compare with Part 1 answer from file for the full input
3. Should match exactly

**Validation**:
```python
# In main():
# Read Part 1 answer from file for comparison
with open('part_1_answer.txt', 'r') as f:
    expected_part1 = int(f.read().strip())

registers, max_during = process_instructions(instructions)
final_max = find_max_register_value(registers)
assert final_max == expected_part1, f"Part 1 logic broken: got {final_max}, expected {expected_part1}"
print(max_during)
```

**Note**: This makes the test more portable by reading the expected value from the Part 1 answer file instead of hard-coding 5221.

## Test Execution Order
1. **Example Test** - Quick validation of core logic
2. **Edge Case: Single Instruction** - Validates minimal case
3. **Edge Case: Peak Early** - Validates tracking works
4. **Edge Case: All Negative** - Validates initialization
5. **Edge Case: Multiple Peaks** - Validates tie handling
6. **Edge Case: Maximum at Final State** - Validates increasing values
7. **Edge Case: No Triggers** - Validates empty case
8. **Regression Test** - Validates Part 1 still works
9. **Full Input Test** - Get actual answer
10. **Verbose Mode Test** - Final verification (manual)

## Success Criteria
- [ ] Example test outputs exactly `10` (NOT 1 - this is the critical differentiator from Part 1)
- [ ] All edge case tests produce expected outputs
- [ ] Part 2 answer ≥ 5221 (Part 1 answer from part_1_answer.txt)
- [ ] Regression test confirms Part 1 logic intact
- [ ] Verbose mode shows correct execution trace
- [ ] Solution runs in < 1 second on full input
- [ ] Single instruction test works correctly
- [ ] Maximum at final state test validates increasing values

## Manual Verification Steps
After running automated tests:

1. **Sanity Check**: Is Part 2 answer > Part 1 answer?
   - If yes: Maximum occurred during execution (makes sense)
   - If equal: Maximum occurred at the final state (also valid)
   - If less: BUG - impossible scenario

2. **Magnitude Check**: Is answer reasonable?
   - Given ~1000 instructions with amounts ranging -1000 to +1000
   - Expected range: 5000-10000 seems reasonable
   - If answer > 100000: likely bug (accumulation error)

3. **Example Validation**: Does example output 10 (not 1)?
   - This is the key test that Part 2 differs from Part 1

## Debugging Checklist (If Tests Fail)
- [ ] Is `max_value_ever` initialized to 0 (not negative infinity)?
- [ ] Is maximum check inside the `if comparator(...)` block?
- [ ] Is maximum check after the register modification?
- [ ] Is the comparison using `max()` function correctly?
- [ ] Are we checking the updated register value (not the old value)?
- [ ] Is the correct value being printed in `main()`?

## Test File Structure
```
test_example.md          # Example from problem statement
test_single.md           # Single instruction test
test_negative.md         # All negative values test
test_peak_early.md       # Peak then decline test
test_multiple_peaks.md   # Multiple equal maxima test
test_max_at_end.md       # Maximum at final state test
test_no_trigger.md       # No conditions trigger test
```

These test files should be created alongside the solution for validation.

**Note**: The example test already validates handling of negative amounts (instruction 3: `c dec -10` increases c by 10), so a separate test for that edge case is not necessary.

## Performance Testing
**Not Critical** (since input is small), but for completeness:

- Run `time python part_2_solution.py`
- Expected runtime: < 0.1 seconds
- If > 1 second: investigate (likely I/O issue, not algorithm)

## Final Validation
Before submitting answer:
1. Run all edge case tests - all pass
2. Run example test - outputs 10 (NOT 1 - critical!)
3. Run full input - answer ≥ 5221
4. Check answer magnitude - reasonable range
5. Compare verbose trace for example - matches expected execution

## Summary

This test plan provides comprehensive validation with 10 different test cases covering:

1. **Correctness**: Example test proves Part 2 differs from Part 1 (10 vs 1)
2. **Edge Cases**: All negative, peak early, multiple peaks, max at end, no triggers, single instruction
3. **Regression**: Ensures Part 1 logic still works correctly
4. **Performance**: Validates O(n) runtime on full input
5. **Debugging**: Verbose mode for manual verification

**Critical Success Indicator**: The example test MUST output 10 (not 1). This is the defining test that proves we're tracking intermediate maxima correctly, not just final state.

**Expected Part 2 Answer**: Should be ≥ 5221 (Part 1 answer). If less, there's a bug. If equal, the maximum occurred at the final state (valid). If greater, the maximum occurred during execution (most likely scenario).
