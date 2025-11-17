# Test Plan: Conway's Game of Life Variant - Light Animation

## Testing Strategy Overview
We need to verify that our implementation correctly simulates the cellular automaton and produces the correct answer for the 100x100 grid after 100 steps.

**Testing Approach**: Since this is a one-off script (not production code), we'll use a pragmatic mix of:
1. **Automated assertions** for critical functionality
2. **Manual verification** with print statements and visual inspection
3. **The 6x6 example as ground truth** - if this passes, the implementation is likely correct

**Success Criteria**:
- 6x6 example produces exactly 4 lights after 4 steps with the correct pattern
- All state transition rules verified (18 combinations)
- Neighbor counting correct for corners, edges, and interior cells
- Synchronous updates verified (blinker pattern test)
- Full 100x100 simulation completes successfully
- Deterministic output (same result on multiple runs)

## Test Categories

### 1. Unit Tests - Component Validation

#### Test 1.1: Input Parsing
**Objective**: Verify that the grid is correctly parsed from the input file

**Test Cases**:
- **TC1.1.1**: Verify grid dimensions are exactly 100x100
  - Count rows: should be 100
  - Count columns in each row: should be 100

- **TC1.1.2**: Verify character mapping
  - Check that `#` characters are converted to True/1
  - Check that `.` characters are converted to False/0

- **TC1.1.3**: Spot check specific positions
  - Manually verify first row, first column against input.md
  - Verify last row, last column
  - Check a few random positions to ensure correct parsing

**How to Test**:
```python
grid = parse_input('input.md')
assert len(grid) == 100, f"Expected 100 rows, got {len(grid)}"
assert all(len(row) == 100 for row in grid), "Not all rows have 100 columns"

# Manual spot checks against input.md
# First row starts with: ###.##..##.#..#.##...
# So grid[0][0:3] should be [True, True, True]
assert grid[0][0:3] == [True, True, True], "First 3 cells of row 0 should be True"
assert grid[0][3] == False, "4th cell of row 0 should be False"

print("Input parsing: PASSED")
```

#### Test 1.2: Neighbor Counting
**Objective**: Verify the neighbor counting function works correctly

**Test Cases**:
- **TC1.2.1**: Corner cells (have only 3 neighbors maximum)
  - Test top-left corner (0, 0)
  - Test top-right corner (0, 99)
  - Test bottom-left corner (99, 0)
  - Test bottom-right corner (99, 99)

- **TC1.2.2**: Edge cells (have only 5 neighbors maximum)
  - Test top edge (0, 50)
  - Test bottom edge (99, 50)
  - Test left edge (50, 0)
  - Test right edge (50, 99)

- **TC1.2.3**: Interior cells (have all 8 neighbors)
  - Test center cell (50, 50)
  - Test various interior positions

- **TC1.2.4**: Known neighbor counts
  - Create small test grids with known configurations
  - Example:
    ```
    ###
    ###
    ###
    ```
    Center cell should have 8 neighbors
  - Example:
    ```
    #.#
    ...
    #.#
    ```
    Center cell should have 4 neighbors

**How to Test**:
```python
# Create test grids
test_grid = [[True, True, True],
             [True, True, True],
             [True, True, True]]
assert count_neighbors(test_grid, 1, 1) == 8

test_grid2 = [[True, False, True],
              [False, False, False],
              [True, False, True]]
assert count_neighbors(test_grid2, 1, 1) == 4
```

#### Test 1.3: State Transition Rules
**Objective**: Verify the state transition logic is correct

**Test Cases**:
- **TC1.3.1**: Light is ON - should stay ON
  - neighbor_count = 2 → stays ON ✓
  - neighbor_count = 3 → stays ON ✓

- **TC1.3.2**: Light is ON - should turn OFF
  - neighbor_count = 0 → turns OFF ✓
  - neighbor_count = 1 → turns OFF ✓
  - neighbor_count = 4 → turns OFF ✓
  - neighbor_count = 5 → turns OFF ✓
  - neighbor_count = 6 → turns OFF ✓
  - neighbor_count = 7 → turns OFF ✓
  - neighbor_count = 8 → turns OFF ✓

- **TC1.3.3**: Light is OFF - should turn ON
  - neighbor_count = 3 → turns ON ✓

- **TC1.3.4**: Light is OFF - should stay OFF
  - neighbor_count = 0 → stays OFF ✓
  - neighbor_count = 1 → stays OFF ✓
  - neighbor_count = 2 → stays OFF ✓
  - neighbor_count = 4 → stays OFF ✓
  - neighbor_count = 5 → stays OFF ✓
  - neighbor_count = 6 → stays OFF ✓
  - neighbor_count = 7 → stays OFF ✓
  - neighbor_count = 8 → stays OFF ✓

**How to Test**:
```python
# Test all combinations
for current_state in [True, False]:
    for neighbor_count in range(9):
        result = get_next_state(current_state, neighbor_count)
        # Verify against expected rules
```

#### Test 1.4: Synchronous Updates
**Objective**: Verify that all cells update simultaneously, not sequentially

**Test Case**:
- **TC1.4.1**: Blinker pattern (oscillates between two states)
  - Initial state:
    ```
    .....
    .###.
    .....
    ```
  - After 1 step should become:
    ```
    ..#..
    ..#..
    ..#..
    ```
  - After 2 steps should return to original:
    ```
    .....
    .###.
    .....
    ```
  - This verifies synchronous updates (sequential would produce different results)

**How to Test**:
```python
grid = create_blinker_pattern()
grid_step1 = simulate_step(grid)
grid_step2 = simulate_step(grid_step1)
assert grid == grid_step2  # Should be identical after 2 steps
```

### 2. Integration Tests - End-to-End Validation

#### Test 2.1: Example Case (6x6 Grid) - MOST IMPORTANT TEST
**Objective**: Verify the solution works correctly on the provided example. **This is the most critical test - if this passes, the implementation is very likely correct.**

**Test Case**:
- **TC2.1.1**: 6x6 grid example from problem statement
  - Initial state:
    ```
    .#.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####..
    ```
  - After 4 steps should have exactly 4 lights on
  - The final pattern should be:
    ```
    ......
    ......
    ..##..
    ..##..
    ......
    ......
    ```

**How to Test**:
```python
# Use the create_grid_from_string helper function
example_input = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

example_grid = create_grid_from_string(example_input)

# Simulate 4 steps and print each step for visual verification
for step in range(4):
    example_grid = simulate_step(example_grid)
    print(f"\nAfter step {step + 1}:")
    print_grid(example_grid)  # Helper to print grid visually

lights_on = count_lights(example_grid)
print(f"\nLights on after 4 steps: {lights_on}")
assert lights_on == 4, f"Expected 4 lights on, got {lights_on}"

# Verify the pattern is a 2x2 block at position (2,2)
assert example_grid[2][2] and example_grid[2][3], "Block top row missing"
assert example_grid[3][2] and example_grid[3][3], "Block bottom row missing"

print("6x6 Example test: PASSED ✓")
```

**Helper function for visualization**:
```python
def print_grid(grid):
    """Print grid in human-readable format"""
    for row in grid:
        print(''.join('#' if cell else '.' for cell in row))
```

#### Test 2.2: Intermediate State Monitoring
**Objective**: Monitor the simulation progression to detect anomalies

**Test Case**:
- **TC2.2.1**: Track light counts over all 100 steps
  - Count lights after each step
  - Look for suspicious patterns (sudden drops to 0, sudden jumps to max, etc.)
  - The count should vary but remain in a reasonable range

**How to Test**:
```python
grid = parse_input('input.md')
initial_count = count_lights(grid)
print(f"Initial lights on: {initial_count}")

counts = [initial_count]
for step in range(100):
    grid = simulate_step(grid)
    count = count_lights(grid)
    counts.append(count)

    # Print progress every 10 steps
    if (step + 1) % 10 == 0:
        print(f"Step {step + 1}: {count} lights on")

print(f"\nFinal lights on: {counts[-1]}")
print(f"Min/Max during simulation: {min(counts)} / {max(counts)}")

# Visual inspection of the progression
print("\nLight count progression (every 10 steps):")
for i in range(0, 101, 10):
    print(f"Step {i}: {counts[i]}")
```

**What to look for**:
- Counts should vary but stay within reasonable bounds
- No sudden drops to 0 (would indicate bug)
- No sudden jumps to 10000 (would indicate bug)
- Some variation is normal and expected

### 3. Edge Case Tests

#### Test 3.1: Boundary Conditions
**Objective**: Ensure edge and corner cells are handled correctly

**Test Cases**:
- **TC3.1.1**: All lights off
  - Grid with all lights off should remain all off forever

- **TC3.1.2**: All lights on
  - Verify behavior when entire grid is on (most cells should turn off due to overcrowding)

- **TC3.1.3**: Single light on
  - A single isolated light should turn off (0 neighbors)

- **TC3.1.4**: Patterns at edges
  - Test patterns that exist at grid boundaries
  - Verify no array out-of-bounds errors

#### Test 3.2: Known Conway's Game of Life Patterns
**Objective**: Test with known patterns to verify correctness

**Test Cases**:
- **TC3.2.1**: Still lifes (patterns that don't change)
  - Block pattern:
    ```
    ##
    ##
    ```
    Should remain unchanged

- **TC3.2.2**: Oscillators
  - Blinker (period 2) - already tested above

- **TC3.2.3**: Gliders (if we want to verify movement)
  - Not strictly necessary for this problem but good validation

### 4. Final Solution Validation

#### Test 4.1: Full Simulation and Answer Validation
**Objective**: Verify the solution produces the correct answer for the actual input

**Test Case**:
- **TC4.1.1**: Run the full simulation multiple times
  - Parse the 100x100 grid from input.md
  - Simulate 100 steps
  - Count final lights
  - Verify deterministic output (same result each time)

**How to Test**:
```python
# Run simulation multiple times to verify determinism
results = []
for run in range(3):
    grid = parse_input('input.md')
    for step in range(100):
        grid = simulate_step(grid)
    result = count_lights(grid)
    results.append(result)
    print(f"Run {run + 1}: {result} lights on")

# Verify all runs produce the same result
assert len(set(results)) == 1, f"Non-deterministic results: {results}"
print(f"\nDeterminism check: PASSED ✓")
print(f"Final answer: {results[0]} lights on after 100 steps")
```

**Post-solution verification**:
- Once we have an answer, verify it's reasonable (likely between 500-2500 based on typical Game of Life behavior)
- If submitting to Advent of Code, the submission system will confirm correctness

### 5. Performance Verification

#### Test 5.1: Runtime Check
**Objective**: Ensure the solution runs efficiently

**Test Case**:
- **TC5.1.1**: Time the full execution
  - Should complete in well under 1 second
  - Python with nested loops on 100x100 grid for 100 steps is ~1 million operations

**How to Test**:
```python
import time

grid = parse_input('input.md')
start = time.time()

for step in range(100):
    grid = simulate_step(grid)

elapsed = time.time() - start
result = count_lights(grid)

print(f"Execution time: {elapsed:.4f} seconds")
print(f"Result: {result} lights on")

if elapsed > 1.0:
    print("WARNING: Execution slower than expected (> 1 second)")
else:
    print("Performance check: PASSED ✓")
```

**Expected performance**:
- Optimized Python: 50-200ms
- Naive Python: 200-500ms
- If > 1 second: potential inefficiency, but still acceptable for this problem

### 6. Manual Verification Steps

#### Step 1: Visual Inspection of Initial Grid
- Print the initial parsed grid
- Visually compare first few rows with input.md
- Verify it "looks right"

#### Step 2: Trace Through Example
- Manually work through the 6x6 example step by step
- Verify each cell's next state for at least step 0→1
- Compare with code output

#### Step 3: Debug Output for First Few Steps
- Add print statements to show grid state after step 1, 2, 3
- Manually verify a few cells are transitioning correctly
- Check corner/edge cells specifically

#### Step 4: Light Count Progression
- Print the count after each of the 100 steps
- Check for reasonable progression (no impossible jumps)
- Final count should be reasonable (not 0, not 10000)

## Test Execution Order (Recommended)

### Phase 1: Core Functionality (MUST PASS)
1. **State Transition Rules** (Test 1.3)
   - Test all 18 combinations of (current_state, neighbor_count)
   - This is the core logic - must be 100% correct

2. **Neighbor Counting** (Test 1.2)
   - Test with small known grids
   - Verify corners, edges, and interior cells

3. **Synchronous Updates** (Test 1.4)
   - Blinker pattern test
   - Ensures simultaneous updates (not sequential)

### Phase 2: Integration Validation (CRITICAL)
4. **6x6 Example Test** (Test 2.1)
   - **MOST IMPORTANT TEST**
   - If this passes with correct pattern, implementation is very likely correct
   - This is our ground truth

### Phase 3: Full Solution
5. **Input Parsing** (Test 1.1)
   - Verify 100x100 grid parses correctly

6. **Full Simulation** (Test 2.2 + Test 4.1)
   - Run complete 100 steps on actual input
   - Monitor progression
   - Verify determinism

7. **Performance Check** (Test 5.1)
   - Time the execution

### Optional: Edge Cases (Test 3.1 → 3.2)
- Known Conway patterns
- Boundary conditions
- Only if you want extra confidence

## Success Criteria (Prioritized)

### Critical (Must Pass)
✓ **6x6 example produces exactly 4 lights after 4 steps** with correct 2x2 block pattern
✓ **All 18 state transition rules correct**
✓ **Neighbor counting correct** for test cases
✓ **Blinker pattern test passes** (verifies synchronous updates)
✓ **Deterministic output** (same result every run)

### Important (Should Pass)
✓ Input parsing correctly reads 100x100 grid
✓ No array out-of-bounds errors
✓ Runs in under 1 second

### Nice to Have
✓ Known Conway patterns work correctly
✓ Edge case handling verified

## Debugging Strategies

If tests fail:
1. **Print intermediate grids** - Visually inspect state transitions
2. **Test with smaller grids** - Easier to manually verify
3. **Check neighbor counting** - Most common source of errors
4. **Verify synchronous updates** - Ensure using separate grid for next state
5. **Boundary checking** - Off-by-one errors in row/col ranges

## Test Implementation Approach

**For a one-off script, we'll use a pragmatic approach**:

### Option 1: Inline Testing (Recommended for this problem)
- Add a `run_tests()` function at the top of `solution.py`
- Call it before running the main solution
- Use simple assertions and print statements
- If all tests pass, proceed to solve the actual problem

```python
def run_tests():
    """Run all tests to verify implementation"""
    print("=== Running Tests ===\n")

    # Test 1: State transitions
    print("Testing state transitions...")
    # ... test code ...
    print("✓ State transitions: PASSED\n")

    # Test 2: Neighbor counting
    print("Testing neighbor counting...")
    # ... test code ...
    print("✓ Neighbor counting: PASSED\n")

    # Test 3: 6x6 example (MOST IMPORTANT)
    print("Testing 6x6 example...")
    # ... test code ...
    print("✓ 6x6 Example: PASSED\n")

    print("=== All Tests Passed ===\n")

if __name__ == '__main__':
    run_tests()  # Run tests first
    main()       # Then solve the problem
```

### Option 2: Separate Test File
- Create `test_solution.py` if you prefer separation
- Import functions from `solution.py`
- Run tests manually before running the solution

### Helper Functions for Testing
```python
def print_grid(grid):
    """Print grid in human-readable format"""
    for row in grid:
        print(''.join('#' if cell else '.' for cell in row))

def grids_equal(grid1, grid2):
    """Compare two grids for equality"""
    if len(grid1) != len(grid2):
        return False
    return all(row1 == row2 for row1, row2 in zip(grid1, grid2))
```

## Key Insight: The 6x6 Example is Your Ground Truth

If the 6x6 example test passes with the correct final pattern, you can be **highly confident** the implementation is correct. This is because:
1. It tests the full integration of all components
2. It has a known, verified correct answer
3. It exercises all the core logic (parsing, neighbor counting, state transitions, synchronous updates)
4. Conway's Game of Life has consistent rules - if it works for 6x6, it will work for 100x100
