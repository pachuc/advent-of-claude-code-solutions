# Testing Plan: Sporifica Virus Simulation

## Testing Strategy

Since this is a scripting problem (not production code), we focus on:
1. **Correctness verification** - ensuring the algorithm produces correct results
2. **Key edge cases** - testing boundary conditions and special scenarios
3. **Example validation** - matching expected outputs from problem statement

We do NOT need: extensive error handling, input validation, scalability tests, or production-grade testing infrastructure.

## Test 1: Example Input Validation

**Objective:** Verify solution matches the provided example

**Input:**
```
..#
#..
...
```

**Expected Outputs:**
- After 7 bursts: 5 infections
- After 70 bursts: 41 infections
- After 10,000 bursts: 5587 infections

**Test Steps:**
1. Create a test file `test_example.txt` with the 3x3 example grid
2. Modify code temporarily to run 7 bursts, verify output = 5
3. Modify code to run 70 bursts, verify output = 41
4. Modify code to run 10,000 bursts, verify output = 5587

**Pass Criteria:** All three burst counts match expected values exactly

**Implementation:**
```python
# Create separate test function or modify main() temporarily
def test_example():
    test_input = """..#
#..
..."""
    # Parse and simulate
    # Assert results match
```

## Test 2: Actual Input Execution

**Objective:** Generate answer for the actual puzzle input

**Input:** The 25x25 grid provided in `input.md`

**Test Steps:**
1. Run `python solution.py` with input.md
2. Record the output value
3. Visual inspection: ensure output is a reasonable integer (likely 1000-8000 range)
4. If submitting to Advent of Code, verify acceptance

**Pass Criteria:**
- Program runs without errors
- Outputs a single integer
- Value is within plausible range for 10,000 bursts

## Test 3: Initial State Verification

**Objective:** Ensure parsing correctly identifies starting position and infected nodes

**Test Case 3a: Center Position Calculation**

**Input:** 3x3 grid (example)
```
..#
#..
...
```

**Coordinate System Reference:**
```
    0 1 2  (x)
0   . . #
1   # . .
2   . . .
(y)
```

**Expected:**
- Grid dimensions: 3x3
- Center position: (1, 1) - the middle '.' in second row

**Test Steps:**
1. Add debug print in `parse_input()` to output center position
2. Verify center = (1, 1) for 3x3 grid
3. Verify center = (12, 12) for 25x25 grid (0-indexed)

**Test Case 3b: Initial Infected Nodes**

**Input:** Example 3x3 grid (see coordinate grid above)

**Expected Infected Positions (using x=column, y=row):**
- (2, 0) - the '#' at position [row 0, col 2] (top-right)
- (0, 1) - the '#' at position [row 1, col 0] (middle-left)

**Test Steps:**
1. Add debug print to output infected_nodes set
2. Verify set contains exactly {(2, 0), (0, 1)} for example
3. Count '#' characters in actual input (should be ~200-300)
4. Verify infected_nodes set size matches count

**Pass Criteria:** Correct center calculation and infected node identification matching coordinate system

## Test 4: Direction System Verification

**Objective:** Verify turning logic works correctly

**Test Case 4a: Turn Left**
- Start facing UP (direction_idx = 0)
- Turn left → should face LEFT (direction_idx = 3)
- Turn left again → should face DOWN (direction_idx = 2)

**Test Case 4b: Turn Right**
- Start facing UP (direction_idx = 0)
- Turn right → should face RIGHT (direction_idx = 1)
- Turn right again → should face DOWN (direction_idx = 2)

**Test Steps:**
1. Create unit test or manual verification
2. Test modulo arithmetic: `(0 - 1) % 4 = 3` ✓
3. Test: `(0 + 1) % 4 = 1` ✓

**Pass Criteria:** Direction indices wrap correctly 0→3→2→1→0

## Test 5: Movement Verification

**Objective:** Ensure carrier moves correctly in each direction

**Test Case:** Manual trace of first few bursts on example

**Coordinate System:**
```
    0 1 2  (x)
0   . . #
1   # . .
2   . . .
(y)
```

**Starting state:**
- Position: (1, 1)  [middle '.' at row 1, col 1]
- Direction: UP (index 0)
- Current node: clean (middle '.')

**Burst 1:**
1. Turn: clean node → turn LEFT → direction index = (0-1)%4 = 3 → now facing LEFT
2. Toggle: clean → infect (1, 1) → count = 1
3. Move: LEFT = (-1, 0) → position = (1-1, 1+0) = (0, 1)

**Burst 2:**
- Position: (0, 1)  [the '#' at row 1, col 0]
- Direction: LEFT (index 3)
- Current node: infected (the '#' initially at this position)
1. Turn: infected → turn RIGHT → direction index = (3+1)%4 = 0 → now facing UP
2. Toggle: infected → clean (0, 1) → count = 1 (unchanged)
3. Move: UP = (0, -1) → position = (0+0, 1-1) = (0, 0)

**Test Steps:**
1. Add debug prints showing position, direction, action after each burst
2. Manually trace first 7 bursts
3. Verify final count = 5 after 7 bursts

**Pass Criteria:** Movement follows expected pattern, count matches

## Test 6: Toggle Logic Verification

**Objective:** Ensure infection state changes correctly

**Test Scenarios:**

**Scenario A: Clean node visited**
- Node starts clean (not in infected_nodes set)
- After burst: node should be in infected_nodes set
- infection_count should increment

**Scenario B: Infected node visited**
- Node starts infected (in infected_nodes set)
- After burst: node should NOT be in infected_nodes set
- infection_count should NOT increment

**Scenario C: Node revisited multiple times**
- Clean → infected (count +1)
- Later visit: infected → clean (count unchanged)
- Later visit: clean → infected (count +1)

**Test Steps:**
1. Create minimal test with controlled movements
2. Track infected_nodes set state after each burst
3. Verify toggles occur correctly

**Pass Criteria:** Set membership changes correctly, counter only increments on infections

## Test 7: Edge Cases

**Test Case 7a: Starting on Infected Node**

**Input:** Grid where center is already infected
```
###
###
###
```

**Expected Behavior:**
- First burst: turn RIGHT (infected), clean center, move
- Should not count initial infected nodes

**Test Case 7b: All Clean Grid**

**Input:**
```
...
...
...
```

**Expected Behavior:**
- Always turn LEFT (clean nodes)
- Should create spiral pattern of infections
- After 7 bursts: should have 7 infections

**Test Case 7c: Single Row/Column**

Not applicable (input is always odd square grid per problem)

**Test Steps:**
1. Create test grids for scenarios 7a and 7b
2. Run simulation
3. Verify reasonable infection counts

**Pass Criteria:** No crashes, logical infection counts

## Test 8: Infection Counter Accuracy

**Objective:** Verify we only count NEW infections, not initial state

**Test:**
1. Count initial '#' in input grid (let's say N infected)
2. (Theoretical) Run simulation for 0 bursts → count should be 0
   - This test is optional/theoretical unless `num_bursts` is parameterized
3. Run for 10,000 bursts → count should be much larger than N
4. Verify we never count initial infected nodes

**Pass Criteria:** Counter only increments when clean→infected transition occurs

**Note:** The 0-burst test requires making burst count configurable (e.g., command-line arg). This is optional for validation but confirms the counter starts at 0.

## Test 9: Data Structure Integrity

**Objective:** Ensure set operations work correctly throughout simulation

**Test Steps:**
1. Verify infected_nodes is a set (not list) for O(1) operations
2. After simulation, check that infected_nodes contains only unique positions
3. Optional: track set size over time (should grow and shrink)

**Pass Criteria:** No duplicate positions, efficient lookups

## Test 9b: Infinite Grid Verification

**Objective:** Confirm carrier can move beyond initial 25x25 grid bounds

**Test Steps:**
1. After 10,000 bursts, add debug print to show min/max x and y coordinates visited
2. Verify that some coordinates are < 0 or >= 25
3. This confirms the sparse set representation handles infinite grid correctly

**Expected:**
- After 10,000 bursts, carrier should have visited positions outside [0, 24] range
- Example: might see coordinates like (-5, 30) or similar

**Pass Criteria:** Carrier successfully moves beyond initial grid boundaries

## Test 10: Final Validation Checklist

Before submitting solution:

- [ ] Example test passes (5587 infections for 10k bursts)
- [ ] Sub-tests pass (7 bursts = 5, 70 bursts = 41)
- [ ] Actual input runs without errors
- [ ] Output is single integer to stdout
- [ ] No debug prints in final version
- [ ] Code follows problem rules exactly (turn, toggle, move order)
- [ ] Initial infected nodes not counted in result

## Debugging Strategy

If tests fail:

**Tip:** Use a DEBUG flag in the code to easily toggle debug prints on/off:
```python
DEBUG = True  # Set to False for final submission
if DEBUG:
    print(f"Burst {i}: pos={pos}, dir={dir_idx}, infected={is_infected}")
```

1. **Wrong count for example:**
   - Add debug prints for first 10 bursts showing position, direction, and action
   - Verify turn direction (left on clean, right on infected)
   - Check toggle logic (add when clean, remove when infected)
   - Verify movement direction vectors match coordinate system

2. **Off-by-one errors:**
   - Check center calculation (should be width//2, height//2)
   - Verify 0-indexed coordinates consistently used
   - Check direction vector signs align with coordinate system
   - Print parsed infected positions and compare with visual grid

3. **Set operations:**
   - Print infected_nodes set before/after toggles
   - Verify using `in` operator correctly
   - Check add() vs remove() calls
   - Ensure infected_nodes is a set, not a list

4. **Coordinate system misalignment:**
   - Print the coordinate grid with positions labeled
   - Verify (x, y) = (column, row) mapping
   - Check that UP decreases y, DOWN increases y, etc.

## Performance Validation

**Objective:** Ensure solution runs efficiently

**Test:**
- Time execution: `time python solution.py`
- **Expected:** ~0.01-0.1 seconds for Python with set operations
- **Acceptable:** < 1 second
- **Warning threshold:** > 0.5 seconds indicates likely inefficiency
- If slower: check for inefficient operations (list scans instead of set lookups)

**Performance Targets:**
- 10,000 iterations × O(1) operations = very fast
- If runtime > 1 second, investigate:
  - Using list instead of set for infected_nodes
  - Unnecessary string operations or prints in loop
  - Reading file multiple times

**Pass Criteria:** Completes in < 1 second (preferably < 0.1 seconds)

## Summary

**Minimum Required Tests:**
1. Example validation (5587 for 10k bursts) - MUST PASS
2. Actual input execution - MUST RUN
3. First 7 bursts trace = 5 infections - SHOULD PASS

**Optional But Recommended:**
- Sub-example validation (70 bursts = 41)
- Center position verification
- Direction system unit tests

**Success Criteria:**
- All required tests pass
- Solution produces correct answer for actual input
- Code is clean and readable
