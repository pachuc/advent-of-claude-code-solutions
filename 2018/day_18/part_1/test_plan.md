# Testing Plan: Lumber Collection Area Simulation

## Testing Strategy
Since we're writing a script to solve a specific problem (not production code), we'll focus on:
1. Verifying core logic correctness with simple test cases
2. Testing the actual input to get the solution
3. Validating edge cases relevant to the problem rules

**Note about Examples:** The problem statement mentions an example result (37 wooded acres × 31 lumberyards = 1,147) but this appears to be illustrative of the calculation, not a worked example with input. We will create our own small test cases to verify correctness.

## Test 1: Input Parsing
**Purpose:** Verify grid is read correctly

**Test Steps:**
1. Parse the input from `input.md`
2. Verify grid dimensions: `len(grid) == 50` and `len(grid[0]) == 50`
3. Spot check a few known positions from input:
   - `grid[0][0]` should be `'|'` (first character)
   - `grid[0][1]` should be `'|'` (second character)
   - `grid[0][2]` should be `'#'` (third character)
4. Verify all cells contain only valid characters: `'.'`, `'|'`, or `'#'`

**Expected Result:** Grid matches input file exactly

## Test 2: Neighbor Counting - Interior Cell
**Purpose:** Verify 8-neighbor counting works correctly

**Test Case:**
```
. | #
| X |
# | .
```
Where X is at position (1, 1)

**Setup:**
Create 3×3 test grid:
```python
grid = [
    ['.', '|', '#'],
    ['|', '.', '|'],
    ['#', '|', '.']
]
```

**Test:**
- `count_neighbors(grid, 1, 1, '|')` should return `3` (positions: top-middle, middle-right, bottom-middle)
- `count_neighbors(grid, 1, 1, '#')` should return `2` (positions: top-right, bottom-left)
- `count_neighbors(grid, 1, 1, '.')` should return `2` (positions: top-left, bottom-right)

**Important:** The center cell at (1, 1) is never counted as its own neighbor. Only the 8 surrounding cells are counted.

**Expected Result:** Counts match the actual neighbors in all 8 directions

## Test 3: Neighbor Counting - Corner Cell
**Purpose:** Verify bounds checking works (only 3 neighbors exist)

**Test Case:**
Top-left corner at (0, 0)

**Setup:**
```python
grid = [
    ['.', '|', '#'],
    ['|', '#', '|'],
    ['#', '|', '.']
]
```

**Test:**
- `count_neighbors(grid, 0, 0, '|')` should return `2`
- Valid neighbors for (0,0) are: (0,1)='|', (1,0)='|', (1,1)='#'
- Trees: (0,1) and (1,0) → count = 2
- Lumberyards: (1,1) → count = 1

**Expected Result:** Only counts the 3 valid neighbors (not the 5 out-of-bounds positions), doesn't crash

## Test 4: Neighbor Counting - Edge Cell
**Purpose:** Verify edge cells with 5 neighbors work correctly

**Test Case:**
Top edge, middle position (0, 1)

**Setup:** Same 3×3 grid as above

**Test:**
- `count_neighbors(grid, 0, 1, '|')` should count neighbors at: (0,0), (0,2), (1,0), (1,1), (1,2)
- Positions: '.', '#', '|', '#', '|' → 2 trees

**Expected Result:** Correctly counts 5 neighbors (no top row exists)

## Test 5: Transformation Rule - Open Ground
**Purpose:** Test open ground → trees transformation

**Test Cases:**

**Case A: Should become trees (3 adjacent trees)**
```python
grid = [
    ['|', '|', '|'],
    ['.', '.', '.'],
    ['.', '.', '.']
]
```
- `get_next_state(grid, 1, 1)` should return `'|'` (has 3 tree neighbors at top)

**Case B: Should stay open (2 adjacent trees)**
```python
grid = [
    ['|', '|', '.'],
    ['.', '.', '.'],
    ['.', '.', '.']
]
```
- `get_next_state(grid, 1, 1)` should return `'.'` (only 2 tree neighbors)

**Expected Result:** Becomes trees if ≥3 tree neighbors, stays open otherwise

## Test 6: Transformation Rule - Trees
**Purpose:** Test trees → lumberyard transformation

**Test Cases:**

**Case A: Should become lumberyard (3 adjacent lumberyards)**
```python
grid = [
    ['#', '#', '#'],
    ['|', '|', '|'],
    ['.', '.', '.']
]
```
- `get_next_state(grid, 1, 1)` should return `'#'` (has 3 lumberyard neighbors at top)

**Case B: Should stay trees (2 adjacent lumberyards)**
```python
grid = [
    ['#', '#', '.'],
    ['|', '|', '|'],
    ['.', '.', '.']
]
```
- `get_next_state(grid, 1, 1)` should return `'|'` (only 2 lumberyard neighbors)

**Expected Result:** Becomes lumberyard if ≥3 lumberyard neighbors, stays trees otherwise

## Test 7: Transformation Rule - Lumberyard
**Purpose:** Test lumberyard persistence/conversion to open ground

**Test Cases:**

**Case A: Should stay lumberyard (has both 1+ tree and 1+ lumberyard)**
```python
grid = [
    ['#', '|', '.'],
    ['#', '#', '.'],
    ['.', '.', '.']
]
```
- Center `#` at (1,1) has neighbors: 2 lumberyards, 1 tree → should stay `'#'`

**Case B: Should become open (has lumberyard but no trees)**
```python
grid = [
    ['#', '.', '.'],
    ['#', '#', '.'],
    ['.', '.', '.']
]
```
- Center `#` at (1,1) has neighbors: 2 lumberyards, 0 trees → should become `'.'`

**Case C: Should become open (has trees but no lumberyard)**
```python
grid = [
    ['|', '|', '.'],
    ['|', '#', '.'],
    ['.', '.', '.']
]
```
- Center `#` at (1,1) has neighbors: 3 trees, 0 other lumberyards → should become `'.'`

**Case D: Should become open (isolated lumberyard)**
```python
grid = [
    ['.', '.', '.'],
    ['.', '#', '.'],
    ['.', '.', '.']
]
```
- Center `#` at (1,1) has no neighbors → should become `'.'`

**Expected Result:** Stays lumberyard only if adjacent to ≥1 lumberyard AND ≥1 trees

## Test 8: Simultaneous Update Verification
**Purpose:** Verify all cells update based on the SAME starting state

**Test Case:**
```python
# Initial state
grid = [
    ['.', '.', '.'],
    ['|', '|', '|'],
    ['.', '.', '.']
]
```

**Manual Calculation:**
After 1 step:
- (0,0): open, has 2 tree neighbors → stays '.'
- (0,1): open, has 3 tree neighbors → becomes '|'
- (0,2): open, has 2 tree neighbors → stays '.'
- (1,0): tree, has 0 lumberyard neighbors → stays '|'
- (1,1): tree, has 0 lumberyard neighbors → stays '|'
- (1,2): tree, has 0 lumberyard neighbors → stays '|'
- (2,0): open, has 2 tree neighbors → stays '.'
- (2,1): open, has 3 tree neighbors → becomes '|'
- (2,2): open, has 2 tree neighbors → stays '.'

Expected:
```python
[
    ['.', '|', '.'],
    ['|', '|', '|'],
    ['.', '|', '.']
]
```

**Test:**
- Run `simulate_step(grid)`
- Verify result matches expected grid exactly
- This confirms simultaneous updates (not sequential)

**Expected Result:** Grid matches manual calculation

## Test 9: Multi-Step Simulation
**Purpose:** Verify simulation runs for multiple iterations correctly

**Test Case:**
Use the small 3×3 grid from Test 8 to verify the simulation can run multiple steps.

**Test Steps:**
1. Start with the same initial state as Test 8
2. Run `simulate(grid, minutes=2)`
3. Verify the simulation completes without errors
4. Verify the result is a valid grid (3×3 with only '.', '|', '#' characters)

**Note:** Test 8 already verifies one step works correctly. This test just ensures multiple iterations don't cause issues.

**Expected Result:** After 2 iterations, simulation completes successfully with a valid grid

## Test 10: Resource Value Calculation
**Purpose:** Verify counting and multiplication is correct

**Test Case:**
```python
grid = [
    ['|', '|', '#'],
    ['#', '.', '|'],
    ['|', '#', '#']
]
```

**Manual Count:**
- Trees (`'|'`): 4
- Lumberyards (`'#'`): 4
- Resource value: 4 × 4 = 16

**Test:**
- `calculate_resource_value(grid)` should return `16`

**Expected Result:** Returns 16

## Test 11: Actual Input - Full Simulation
**Purpose:** Solve the actual problem and verify reasonable output

**Test Steps:**
1. Load actual input from `input.md`
2. Parse grid (verify it's 50×50)
3. Run simulation for 10 minutes
4. Calculate resource value
5. Print result (should be a single integer on one line)

**Validation Checks:**
- Grid is 50×50 after parsing
- After 10 iterations, grid still has all three types of cells (sanity check)
- Resource value is a positive integer
- Trees count > 0 and lumberyards count > 0 (otherwise result would be 0)
- Output format: Single integer printed to stdout, nothing else

**Expected Result:**
- Program completes without errors
- Produces a reasonable integer result (likely in range 1,000-1,000,000)
- Output is exactly one integer (Advent of Code format)

## Test 12: Edge Case - All Same Type (Optional)
**Purpose:** Verify behavior when grid is homogeneous

**Note:** This test is optional as the actual input will be heterogeneous. Only run if time permits.

**Test Cases:**

**Case A: All open ground**
```python
grid = [
    ['.', '.', '.'],
    ['.', '.', '.'],
    ['.', '.', '.']
]
```
After 1 step: Should remain all '.' (no trees to spread)

**Case B: All trees**
```python
grid = [
    ['|', '|', '|'],
    ['|', '|', '|'],
    ['|', '|', '|']
]
```
After 1 step: Should remain all '|' (no lumberyards to convert)

**Case C: All lumberyards**
```python
grid = [
    ['#', '#', '#'],
    ['#', '#', '#'],
    ['#', '#', '#']
]
```
After 1 step: Each lumberyard has 8 or 5 or 3 lumberyard neighbors (edges/corners) but 0 trees
→ All should become '.'

**Expected Result:** Transformations follow rules even in edge cases

## Testing Execution Order

**Priority Tests (Must Run):**
1. **Parse input test** (Test 1) - Verify we can read data
2. **Neighbor counting tests** (Tests 2-4) - Core functionality
3. **Transformation rule tests** (Tests 5-7) - Verify each rule
4. **Simultaneous update test** (Test 8) - **CRITICAL** - Most important test
5. **Resource calculation test** (Test 10) - Verify final step
6. **Full simulation test** (Test 11) - Get the answer

**Optional Tests (If Time Permits):**
7. **Multi-step test** (Test 9) - Additional verification
8. **Edge cases** (Test 12) - Homogeneous grids

## Success Criteria

**Minimum requirements to consider solution correct:**
1. Parses 50×50 input correctly
2. Neighbor counting handles bounds correctly (corners, edges, interior)
3. All three transformation rules work correctly
4. Simultaneous updates work (not sequential)
5. Simulation runs for exactly 10 iterations
6. Resource value calculation is correct
7. Produces a final integer answer for the actual input

## Debugging Checklist

If output is incorrect, check:
- [ ] Grid indexing: `grid[row][col]` not `grid[col][row]`
- [ ] Simultaneous updates: using old state for all calculations in a step
- [ ] Neighbor bounds checking: not accessing out-of-bounds indices
- [ ] Lumberyard rule: needs BOTH ≥1 tree AND ≥1 lumberyard to persist
- [ ] Correct iteration count: exactly 10 iterations
- [ ] Resource calculation: trees × lumberyards (not +)
