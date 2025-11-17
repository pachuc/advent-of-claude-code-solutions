# Test Plan: Conway's Game of Life with Stuck Corners

## Testing Strategy

Given this is a script to solve a specific problem (not production code), we focus on:
1. Correctness verification with the given input
2. Key edge cases related to the corner constraint
3. Validation of Conway's rules implementation
4. Small example from problem statement

## Test Cases

### Test 1: Minimal Corner Test (3×3 Grid)
**Objective:** Quick sanity check of basic functionality

**Input:** 3×3 grid, all OFF initially
```
...
...
...
```

**Process:**
1. Force corners to ON: positions (0,0), (0,2), (2,0), (2,2)
2. Grid becomes:
```
#.#
...
#.#
```
3. Run one step
4. Each corner has only 1 neighbor (diagonal corner) → would turn OFF by rules
5. But corners are forced ON after rules
6. Expected result: corners ON, everything else OFF
7. Final count should be 4

**Why Important:** Simplest possible test to verify corner forcing and basic logic

### Test 2: Small Example Verification (6×6 Grid, 5 Steps)
**Objective:** Verify implementation with a small multi-step example

**Input:** 6×6 grid (using a simple pattern, not from problem statement)
```
.#.#.#
...##.
#....#
..#...
#.#..#
####..
```

**Process:**
1. Force corners to ON initially
2. Run 5 iterations
3. Count final ON lights
4. Problem statement mentions a 6×6 example yields 17 after 5 steps
5. Verify our result is reasonable (between 4 and 36)

**Note:** The problem statement mentions this example but doesn't provide the exact initial configuration. This test uses a synthetic pattern to verify multi-step simulation works correctly.

**Why Important:** Small enough to debug manually if needed, large enough to test multiple iterations

### Test 3: Corner Persistence Check
**Objective:** Verify corners remain ON even when they should turn OFF by standard rules

**Scenario:** Create a grid where corners have 0 or 1 neighbors (should turn OFF by rules)
**Expected:** Corners stay ON after each step

**Test Data:**
```
#.......#
.........
.........
... (all off) ...
.........
#.......#
```

**Validation:**
- After each iteration, check grid[0][0], grid[0][99], grid[99][0], grid[99][99] are all True
- Corners should never be False at any step

**Why Important:** Tests the core special constraint of the problem

### Test 4: Neighbor Counting Accuracy
**Objective:** Verify neighbor counting works correctly for corners, edges, and interior

**Sub-tests:**

**4a: Corner cell neighbor counting**
```python
test_grid = [
    [#, #, .],
    [#, ., .],
    [., ., .]
]
```
- Cell (0,0) has 3 possible neighbor positions: (0,1), (1,0), (1,1)
- Of these, 2 are ON: (0,1)=# and (1,0)=#
- Expected count: 2

**4b: Edge cell neighbor counting**
```python
test_grid = [
    [., #, .],
    [#, #, #],
    [., ., .]
]
```
- Cell (0,1) has 5 possible neighbor positions (top row, middle)
- Neighbors: (0,0), (0,2), (1,0), (1,1), (1,2)
- Of these, 3 are ON
- Expected count: 3

**4c: Interior cell neighbor counting**
```python
test_grid = [
    [#, #, #],
    [#, #, #],
    [#, #, #]
]
```
- Cell (1,1) has all 8 neighbors in bounds
- All 8 are ON
- Expected count: 8

**Why Important:** Incorrect neighbor counting will propagate errors through all iterations

### Test 5: Conway's Rules Application
**Objective:** Verify standard Conway's Game of Life rules work correctly

**Sub-tests:**

**5a: ON cell with 2 neighbors stays ON**
```
...
###
...
```
Cell (1,1) is ON and has 2 ON neighbors (1,0) and (1,2), should stay ON

**5b: ON cell with 3 neighbors stays ON**
```
.#.
###
...
```
Cell (1,1) is ON and has 3 ON neighbors, should stay ON

**5c: ON cell with <2 neighbors turns OFF (underpopulation)**
```
.#.
...
...
```
Cell (0,1) is ON but has 0 neighbors, should turn OFF

**5d: ON cell with >3 neighbors turns OFF (overpopulation)**
```
###
###
...
```
Cell (0,1) is ON and has 4 neighbors, should turn OFF

**5e: OFF cell with exactly 3 neighbors turns ON (birth)**
```
###
.#.
...
```
Cell (1,1) is OFF and has 3 ON neighbors, should turn ON

**Why Important:** Core Conway's rules must work correctly

### Test 6: Simultaneous Update Verification
**Objective:** Ensure all cells update based on the same generation (no cascading)

**Test Data:** Oscillator pattern (blinker)
```
Initial (Step 0):
.....
.###.
.....
```

**Expected behavior:**
Step 1:
```
..#..
..#..
..#..
```
(Vertical line)

Step 2:
```
.....
.###.
.....
```
(Back to horizontal - same as step 0)

**Validation:**
- Run 2 steps and verify we get back to original pattern
- Cell (1,1) should have 2 neighbors in step 0, stay ON
- Cell (0,1) should have 3 neighbors in step 0, turn ON in step 1

**Why Important:** Detects if implementation incorrectly updates in-place instead of creating new grid

### Test 7: All Lights OFF (Except Corners)
**Objective:** Verify behavior when most lights are OFF

**Input:** 100×100 grid with all cells OFF initially
```
. . . ... .
. . . ... .
...
. . . ... .
```

**Process:**
1. Force corners to ON initially
2. After forcing, corners (0,0), (0,99), (99,0), (99,99) are ON, all others OFF
3. Run several steps

**Analysis:**
- Corner (0,0) has neighbors at (0,1), (1,0), (1,1) - all OFF → would turn OFF, but forced ON
- Cell (1,1) has 8 neighbors including corner (0,0) → only 1 ON → stays OFF (needs 3 to birth)
- In a 100×100 grid, corners are too far apart to interact
- No cell can have exactly 3 ON neighbors

**Expected:**
- Corners remain ON indefinitely
- No new lights are born
- Final count should be 4 after any number of steps

**Why Important:** Tests edge case of sparse grid and verifies corners don't enable births

### Test 8: All Lights ON
**Objective:** Verify behavior with dense grid

**Input:** Grid with all lights ON (100×100 all '#')

**Expected:**
- Most interior cells have 8 neighbors → will turn OFF (overpopulation)
- Edge cells have 5 neighbors → will turn OFF
- Corners have 3 neighbors → would stay ON anyway, plus forced ON

**Validation:** Run a few steps and ensure it stabilizes (doesn't grow unbounded)

**Why Important:** Tests behavior with dense population

### Test 9: Initial State Verification
**Objective:** Verify input parsing and initial setup are correct

**Process:**
1. Parse input.md
2. Check dimensions: should be 100 rows × 100 columns
3. Count ON lights in parsed state (before forcing corners)
4. Force corners ON
5. Verify all 4 corners are ON: grid[0][0], grid[0][99], grid[99][0], grid[99][99]

**Validation:**
- Grid has exactly 100 rows
- Each row has exactly 100 columns
- Initial count is reasonable (between 0 and 10,000)
- After forcing, corners are all True

**Why Important:** Catches parsing errors and dimension issues before simulation

### Test 10: Final Answer Validation
**Objective:** Verify the actual solution with the provided input

**Input:** The full 100×100 grid from input.md
**Process:**
1. Run complete simulation (100 steps)
2. Count final ON lights
3. Verify result is reasonable (between 4 and 10,000)

**Validation Checks:**
- Result >= 4 (at minimum, corners are ON)
- Result <= 10,000 (can't exceed grid size)
- Result is a reasonable number for this type of problem

**Optional Check:**
- Run for 101 steps and compare to 100-step result to observe if pattern is still changing or has stabilized

**Why Important:** This is the actual problem we need to solve

### Test 11: Grid Dimensions and Indices Verification
**Objective:** Ensure we're correctly handling the 100×100 grid

**Implementation:**
```python
grid = parse_input('input.md')
assert len(grid) == 100, f"Expected 100 rows, got {len(grid)}"
assert all(len(row) == 100 for row in grid), "All rows must have 100 columns"

# Verify corner indices are correct (0-based indexing)
force_corners_on(grid)
assert grid[0][0] == True, "Top-left corner should be ON"
assert grid[0][99] == True, "Top-right corner should be ON"
assert grid[99][0] == True, "Bottom-left corner should be ON"
assert grid[99][99] == True, "Bottom-right corner should be ON"

# Verify we're not trying to access grid[100][100]
# (This would raise IndexError if attempted)
```

**Why Important:** Off-by-one errors in dimensions would cause index errors or wrong answer

## Test Execution Strategy

### Phase 1: Unit Tests (Individual Functions)
1. Test `count_neighbors()` with corner, edge, and interior cells
2. Test `parse_input()` returns correct dimensions
3. Test `force_corners_on()` sets all 4 corners

### Phase 2: Integration Tests (Single Step)
1. Test `simulate_step()` with small grids (3×3, 6×6)
2. Verify known patterns (blinker, block, etc.)
3. Verify corner forcing happens after rule application

### Phase 3: End-to-End Tests
1. Run 6×6 example for 5 steps → expect 17
2. Run full input for 100 steps → verify reasonable output

### Phase 4: Manual Verification
1. Print initial state (with corners forced)
2. Print state after step 1
3. Manually verify a few cells followed rules correctly
4. Print final state
5. Manually count ON lights in a few rows to spot-check

## Debugging Checklist

If tests fail, check:

1. **Wrong count:**
   - Are corners being forced AFTER rule application?
   - Is neighbor counting excluding the cell itself?

2. **Index errors:**
   - Are boundary checks using < 100 not <= 100?
   - Are we checking row AND col are in range?

3. **Rules not working:**
   - Are we reading from old grid and writing to new grid?
   - Are we checking birth condition (exactly 3) vs survival (2 or 3)?

4. **Corners turning OFF:**
   - Is force_corners_on() called after simulate_step()?
   - Are corner indices correct?

## Expected Behavior Summary

- **Initial:** Corners forced ON, input pattern otherwise preserved
- **During:** Corners always ON, other cells follow Conway's rules
- **Final:** Some stable or oscillating pattern with corners ON
- **Count:** Reasonable number between 4 and ~5,000 (typical for such inputs)

## Quick Validation Test

The simplest executable test to verify basic correctness (Test 1):

```python
# 3×3 grid, all OFF initially
grid = [[False]*3 for _ in range(3)]
force_corners_on(grid)  # (0,0), (0,2), (2,0), (2,2) turn ON

# After forcing, we have:
# # . #
# . . .
# # . #

# Count initial: should be 4
assert count_on_lights(grid) == 4

# Run one step
grid = simulate_step(grid)

# Analysis:
# - Each corner has 1 neighbor (diagonal corner) → would turn OFF by rules
# - But corners are forced ON after rule application
# - Edge cells like (0,1) have 2 corner neighbors → stays OFF (needs 3 to birth)
# - Center cell (1,1) has 4 corner neighbors → stays OFF
# Expected result: corners ON, everything else OFF

assert count_on_lights(grid) == 4, f"Expected 4, got {count_on_lights(grid)}"
```

If this passes, basic logic is likely correct.
