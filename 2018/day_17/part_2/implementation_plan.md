# Implementation Plan: Water Retention After Spring Dries Up (Part 2)

## Overview
Part 2 requires counting only the settled water tiles (`~`) that remain after the spring dries up, excluding flowing water (`|`). The Part 1 solution already tracks these separately, making this a simple modification.

## Key Insight
The Part 1 solution in `part_1_solution.py` already:
- Maintains two separate sets: `flowing_water` and `settled_water`
- Correctly simulates water flow with settling logic
- Counts both sets for the final answer: `flowing_water | settled_water`

For Part 2, we only need to count `settled_water`.

## Implementation Steps

### Step 0: Verify Part 1 Solution
**Action**: Confirm Part 1 solution produces the correct answer before proceeding
**Validation**:
- Run `part_1_solution.py` on `input.md`
- Verify output is exactly **41027** (from `part_1_answer.txt`)
- This ensures we're starting from a known-good baseline

### Step 1: Reuse Part 1 Code Structure
**Action**: Copy the entire Part 1 solution as a starting point
**Target filename**: `solution.py` (the Part 2 solution file)
**Rationale**: All the water simulation logic is correct and doesn't need modification
**Files to reuse**:
- All parsing functions (`parse_input`)
- All range functions (`get_y_range`, `get_x_range`)
- All simulation functions (`flow_down`, `spread_horizontal`, `settle_water`)
- The grid visualization function (for debugging)

### Step 2: Modify the Counting Logic
**Action**: Change the final counting to use only `settled_water`
**Location**: In the `solve()` function, around line 222 (note: line numbers are approximate references from Part 1 solution)

**Current Part 1 code**:
```python
water_in_range = {(x, y) for (x, y) in (flowing_water | settled_water) if min_y <= y <= max_y}
```

**Modified Part 2 code**:
```python
# Part 2: Count only settled water (water that remains after spring dries)
water_in_range = {(x, y) for (x, y) in settled_water if min_y <= y <= max_y}
```

**Explanation**:
- Remove the union operation (`flowing_water | settled_water`)
- Use only `settled_water` for the final count
- Still apply the y-range filter (`min_y <= y <= max_y`) - this is critical to count only water within the valid clay structure
- Add a comment explaining the Part 2 modification

### Step 3: Update Output Message
**Action**: Change the output message to reflect "settled water" instead of "water can reach"
**Location**: In the `if __name__ == '__main__'` block

**Current**:
```python
print(f"Water can reach {result} tiles")
```

**Modified**:
```python
print(f"Settled water remains in {result} tiles")
```

### Step 4: Verification (Critical Step)
**Action**: Test the solution thoroughly before considering it complete

**Test on Example First** (Highly Recommended):
- Run on the example from the problem description
- Expected result: **29** (instead of Part 1's 57)
- **Enable grid visualization** by uncommenting `print_grid()` to visually verify:
  - Settled water (`~`) vs flowing water (`|`)
  - Manually count the 29 settled tiles on the grid
  - This builds confidence before running on the large input

**Test on Actual Input**:
- Run on `input.md`
- Verify the result is less than the Part 1 answer (41027)
- Verify the result is greater than 0
- Expected range: approximately 20,000 - 30,000 tiles (50-70% of Part 1, though this can vary)

**Verification Checklist**:
- [ ] Example produces exactly 29
- [ ] Actual input produces result < 41027
- [ ] Actual input produces result > 10000 (reasonable lower bound)
- [ ] Sets are disjoint: `flowing_water & settled_water` is empty
- [ ] Y-range filtering is working correctly

## Algorithm Complexity Analysis

### Time Complexity
- **Parsing**: O(N) where N is the number of clay vein definitions
- **Simulation**: O(W × H) where W and H are the width and height of the grid
  - Each position is visited at most a constant number of times due to memoization via the sets
  - The recursive flow_down with horizontal spreading visits each reachable tile
- **Counting**: O(S) where S is the size of settled_water set
- **Overall**: O(N + W × H) - efficient for the given input size

### Space Complexity
- **Clay set**: O(C) where C is the total number of clay tiles
- **Flowing water set**: O(F) where F is flowing water tiles
- **Settled water set**: O(S) where S is settled water tiles
- **Recursion stack**: O(H) in worst case (vertical fall)
- **Overall**: O(C + F + S + H) - reasonable for the problem constraints

### Input Size Considerations
Looking at the input:
- Y-range: approximately 6 to 1694 (height ≈ 1688)
- X-range: approximately 216 to 644 (width ≈ 428)
- Total grid size: ~722,464 positions
- The recursive solution with memoization via sets should handle this efficiently
- Recursion limit is already increased to 10,000 in Part 1 solution (no change needed for Part 2)

## Expected Behavior
- **Part 1 answer**: 41027 (both flowing and settled water)
- **Part 2 answer**: Should be significantly less (only settled water)
- **Ratio**: Typically settled water is 50-70% of total water in these problems, though this heavily depends on the specific input structure (the example shows 29/57 = 51%)
- **Expected range**: Approximately 20,000 - 30,000 tiles (this is a rough estimate, actual value may vary)

## Code Changes Summary
1. **Line 222**: Change `flowing_water | settled_water` to just `settled_water`
2. **Line 232**: Update print message for clarity
3. **No other changes needed** - all simulation logic remains identical

## Why This Approach Works
The Part 1 solution correctly identifies:
- **Settled water (`~`)**: Water contained by clay walls on both sides
- **Flowing water (`|`)**: Water that's falling or overflowing

When the spring dries:
- Flowing water drains away (not counted)
- Settled water remains in containers (counted)

The existing `settled_water` set already contains exactly what Part 2 needs.
