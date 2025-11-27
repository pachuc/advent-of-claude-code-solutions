# Testing Plan: Lumber Collection Area - Part 2

## Overview
Verify that the cycle detection algorithm correctly identifies repeating patterns and calculates the resource value at minute 1,000,000,000 for the given input.

## Testing Strategy

We need to verify:
1. Core simulation logic still works (inherited from Part 1)
2. Cycle detection correctly identifies when states repeat
3. Modular arithmetic correctly calculates final state
4. Edge cases in cycle detection are handled
5. The final answer for the actual input is correct

## Test 1: Regression Test - Verify Part 1 Logic Still Works

**Purpose**: Ensure refactoring didn't break existing functionality

**Test Steps**:
1. Temporarily modify `main()` to use `target_minutes=10`
2. Run the Part 2 solution
3. Compare result with Part 1 answer: 604884
4. Restore to `target_minutes=1_000_000_000`

**Expected Result**: Should output `604884`

**Validation**:
```bash
python solution.py  # Modified temporarily to use minutes=10
# Should print: 604884
```

**Why This Matters**: If basic simulation is broken, cycle detection won't help. This ensures all reused functions from Part 1 still work correctly.

## Test 2: Verify Cycle Detection Occurs

**Purpose**: Confirm that a cycle is actually detected (not running 1B iterations)

**Test Steps**:
1. Add debug print statements to show when cycle is detected:
   ```python
   print(f"Cycle detected at minute {minute}")
   print(f"Cycle started at minute {cycle_start}")
   print(f"Cycle length: {cycle_length}")
   ```

2. Run the solution and observe output

**Expected Result**:
- Cycle should be detected well before 1,000,000,000 iterations
- Should complete in under 1 second
- Cycle detection message should appear

**What to Check**:
- `cycle_start` should be a reasonable number (likely < 1,000)
- `cycle_length` should be a reasonable number (likely 10-100)
- If runtime is >5 seconds, cycle detection might not be working

## Test 3: Small Grid Test - Verify Cycle Detection with Known Example

**Purpose**: Test cycle detection on a small grid where we can manually verify behavior

**Test Steps**:
1. Create a minimal test grid (3x3 or 4x4):
   ```python
   test_grid = [
       ['.', '.', '|'],
       ['|', '|', '|'],
       ['.', '#', '#']
   ]
   ```

2. Manually simulate 10-15 iterations to find the actual cycle:
   - Record the state after each iteration
   - Identify when a state repeats
   - Note the cycle_start and cycle_length

3. Run the code on this test grid with a large target (e.g., 1000)

4. Verify the code detects the same cycle_start and cycle_length

5. Manually calculate what state should be at minute 1000 using the formula

6. Verify the code returns the correct resource value

**Expected Result**: Code detects the same cycle we found manually and returns correct answer

**Example Verification**:
If manual simulation shows:
- States: A, B, C, D, C, D, C, D... (cycle detected at minute 4)
- cycle_start = 2, cycle_length = 2
- For target = 1000: (1000 - 2) % 2 = 0, so final_minute = 2 (state C)

**Why This Matters**: This validates the entire algorithm on a case we can fully verify by hand.

## Test 4: Verify Grid-to-Tuple Conversion

**Purpose**: Ensure grid hashing is deterministic and correct

**Test Steps**:
1. Create a test grid:
   ```python
   grid1 = [['|', '.'], ['#', '|']]
   grid2 = [['|', '.'], ['#', '|']]
   grid3 = [['.', '|'], ['#', '|']]

   tuple1 = grid_to_tuple(grid1)
   tuple2 = grid_to_tuple(grid2)
   tuple3 = grid_to_tuple(grid3)
   ```

2. Verify:
   - `tuple1 == tuple2` (same grids produce same tuples)
   - `tuple1 != tuple3` (different grids produce different tuples)
   - `hash(tuple1) == hash(tuple2)` (can be used as dict keys)

**Expected Result**: Identical grids produce identical tuples; different grids produce different tuples

## Test 5: Verify State Storage (Proper Copying)

**Purpose**: Ensure stored grids don't get mutated when current grid changes

**Test Steps**:
1. Store a grid in the states_by_minute dictionary
2. Simulate the next step (modifying current_grid)
3. Check that the stored grid hasn't changed

**Implementation**:
```python
states_by_minute = {}
grid = [['|', '.'], ['#', '|']]
# This creates a shallow copy of the outer list with shallow copies of inner lists
# For 2D grids of strings/chars, this is sufficient since strings are immutable
states_by_minute[0] = [row[:] for row in grid]

# Modify grid
grid[0][0] = '#'

# Check stored version unchanged
assert states_by_minute[0][0][0] == '|'
```

**Expected Result**: Stored grid should be independent of current grid

**Technical Note**: `[row[:] for row in grid]` creates a new outer list with new inner lists. This is sufficient for 2D grids of immutable elements (strings/chars). For nested mutable structures, you'd need `copy.deepcopy()`, but that's unnecessary here.

**Why This Matters**: If we store references instead of copies (e.g., just `states_by_minute[0] = grid`), all stored states would point to the same mutating grid object.

## Test 6: Run Full Solution on Actual Input

**Purpose**: Get the final answer for submission

**Test Steps**:
1. Ensure `input.md` is in the working directory
2. Run: `python solution.py`
3. Record the output (the resource value)

**Expected Behavior**:
- Should complete in <1 second
- Should output a single integer
- Should be different from Part 1 answer (604884)

**Validation Checks**:
- Output should be a reasonable number (likely in range 100,000-1,000,000)
- Should be reproducible (running twice gives same answer)

## Test 7: Boundary Condition - Cycle at Minute 0

**Purpose**: Handle edge case where grid immediately repeats

**Test Approach**:
This is unlikely with the given input but our algorithm should handle it:
- If cycle_start = 0 and cycle_length = 1 (grid never changes)
- Calculation: (1B - 0) % 1 = 0, final_minute = 0
- Should return resource value of initial grid

**How to Verify**: Code review to ensure no division by zero or index errors

## Test 8: Modular Arithmetic Edge Cases

**Purpose**: Verify correct calculation when target falls on special cycle positions

**Test Steps**:
1. Suppose we detect a cycle with:
   - cycle_start = 100
   - cycle_length = 28

2. Test the calculation for various targets:
   ```python
   # Targets that fall at cycle_start (should all give same result)
   test_targets = [100, 128, 156, 184, 212]
   for target in test_targets:
       remaining = target - 100
       position = remaining % 28
       assert position == 0  # All should return to cycle_start

   # Targets that are cycle_start + 1 (should all give same result)
   test_targets = [101, 129, 157, 185]
   for target in test_targets:
       remaining = target - 100
       position = remaining % 28
       assert position == 1  # All should be at position 1
   ```

3. Verify that the code handles targets exactly at cycle boundaries

**Expected Result**: Modular arithmetic correctly handles all positions in cycle

**Why This Matters**: Off-by-one errors in cycle calculation would show up here.

## Test 9: Resource Value Calculation Consistency

**Purpose**: Ensure resource value calculation is correct

**Test Steps**:
1. Create a known grid:
   ```python
   grid = [
       ['|', '|', '|'],
       ['#', '#', '.'],
       ['|', '.', '.']
   ]
   # Trees: 4, Lumberyards: 2, Value: 8
   ```

2. Verify: `calculate_resource_value(grid) == 8`

**Expected Result**: Should correctly count and multiply

## Test 10: Performance Test

**Purpose**: Ensure solution completes in reasonable time

**Test Steps**:
1. Time the execution: `time python solution.py`
2. Check runtime is <2 seconds

**Expected Result**:
- Should complete almost instantly (<1 second)
- If it takes longer, cycle might not be detected

**Performance Indicators**:
- ✓ Good: <1 second (cycle detected early)
- ⚠ Concerning: 1-5 seconds (cycle detected late)
- ✗ Problem: >5 seconds (cycle detection not working)

## Test 11: Input Validation

**Purpose**: Verify the input is parsed correctly and has expected dimensions

**Test Steps**:
1. After parsing the input, verify grid dimensions:
   ```python
   grid = parse_input(input_text)
   assert len(grid) == 50, f"Expected 50 rows, got {len(grid)}"
   assert all(len(row) == 50 for row in grid), "Not all rows are 50 chars"
   assert all(cell in '.#|' for row in grid for cell in row), "Invalid character found"
   ```

2. Verify that parse_input() correctly handles the actual input.md file

**Expected Result**: Grid is 50x50 and contains only valid characters

**Why This Matters**: Malformed input would cause incorrect results. Early validation catches file issues.

## Comprehensive Test Checklist

Before considering solution complete, verify:

- [ ] **Test 1**: Part 1 answer (10 minutes) still produces 604884
- [ ] **Test 2**: Cycle is detected (debug output shows cycle info)
- [ ] **Test 2**: Solution completes in <1 second
- [ ] **Test 3**: Small grid test validates cycle detection on known example
- [ ] **Test 4**: Grid-to-tuple conversion works correctly (same grids → same tuples)
- [ ] **Test 5**: Proper copying prevents state mutation
- [ ] **Test 6**: Full solution runs successfully on actual input
- [ ] **Test 7**: Boundary condition (cycle at minute 0) doesn't cause errors
- [ ] **Test 8**: Modular arithmetic handles cycle boundaries correctly
- [ ] **Test 9**: Resource value calculation is accurate
- [ ] **Test 10**: Performance is acceptable (<2 seconds)
- [ ] **Test 11**: Input validation confirms correct grid dimensions
- [ ] **General**: Output is reproducible (same answer on multiple runs)
- [ ] **General**: Output is a single integer with no extra text
- [ ] **General**: No errors or exceptions during execution

## Manual Verification Strategy

Since we don't have the "correct" answer beforehand:

1. **Consistency Check**: Run multiple times, ensure same answer
2. **Reasonableness Check**: Answer should be positive integer in plausible range
3. **Cycle Verification**: Print cycle_start and cycle_length to verify they're reasonable
4. **Sample Verification**: Manually verify a few states in the cycle match

## Debug Output Template

Add these debug statements to verify correctness:

```python
print(f"Cycle detected at minute {minute}")
print(f"Cycle starts at minute {cycle_start}")
print(f"Cycle length: {cycle_length}")
print(f"Target minute: {target_minutes}")
print(f"Position in cycle: {position_in_cycle}")
print(f"Using state from minute: {final_minute}")
print(f"Resource value: {result}")
```

## Expected Debug Output Pattern

For the actual input, expect something like:
```
Cycle detected at minute 550
Cycle starts at minute 450
Cycle length: 100
Target minute: 1000000000
Position in cycle: 50
Using state from minute: 500
Resource value: [ANSWER]
```

(Actual numbers will vary based on the real cycle in the input)

## Error Conditions to Watch For

1. **KeyError**: Trying to access state that wasn't stored → Check dictionary usage
2. **Infinite loop**: Never detecting cycle → Check tuple conversion
3. **Wrong answer**: Logic error in modular arithmetic → Verify calculation
4. **Memory error**: Storing too many states → Unlikely with expected cycle sizes

## Final Validation

The ultimate test is submitting to Advent of Code and getting "correct" response. Before submission:
- Ensure output is just the integer (no extra text)
- Verify it's different from Part 1 answer
- Check it's a positive integer
