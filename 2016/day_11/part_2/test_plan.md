# Testing Plan - RTG Transportation Part 2

## Testing Objectives
1. Verify the solution correctly adds the 4 new items to the initial state
2. Ensure the safety rules are properly enforced with the additional items
3. Validate that BFS finds the optimal (minimum step) solution
4. Confirm the output is a reasonable integer value
5. Test canonicalization works correctly with 7 element pairs

## Test Strategy

### Test 1: Verify Initial State Setup
**Purpose**: Confirm the 4 new items are correctly added to floor 0

**Approach**:
```python
# Add debug print after parsing and adding items
print(f"Floor 0 items: {initial_floors[0]}")
print(f"Total items on floor 0: {len(initial_floors[0])}")
```

**Expected Results**:
- Floor 0 should contain 8 items total:
  - strontium generator and microchip (from input)
  - plutonium generator and microchip (from input)
  - elerium generator and microchip (added manually)
  - dilithium generator and microchip (added manually)
- Verify output shows: `('elerium', 'G')`, `('elerium', 'M')`, `('dilithium', 'G')`, `('dilithium', 'M')`

**Pass Criteria**: All 8 expected items present on floor 0

---

### Test 2: Safety Rule Validation with New Items
**Purpose**: Ensure safety checks work correctly with elerium and dilithium items

**Test Cases**:

**Case 2a: Safe configuration - matching pairs**
```python
# Test floor with elerium pair
test_floor = {('elerium', 'G'), ('elerium', 'M')}
assert is_safe_floor(test_floor) == True
```

**Case 2b: Safe configuration - multiple matching pairs**
```python
# Test floor with both new pairs
test_floor = {('elerium', 'G'), ('elerium', 'M'), ('dilithium', 'G'), ('dilithium', 'M')}
assert is_safe_floor(test_floor) == True
```

**Case 2c: Unsafe configuration - unprotected microchip**
```python
# Elerium microchip with dilithium generator (should fry)
test_floor = {('elerium', 'M'), ('dilithium', 'G')}
assert is_safe_floor(test_floor) == False
```

**Case 2d: Safe configuration - microchips alone**
```python
# All 7 microchips together (no generators)
test_floor = {('elerium', 'M'), ('dilithium', 'M'), ('strontium', 'M'),
              ('plutonium', 'M'), ('thulium', 'M'), ('ruthenium', 'M'), ('curium', 'M')}
assert is_safe_floor(test_floor) == True
```

**Pass Criteria**: All safety assertions pass

---

### Test 3: Initial State Validity
**Purpose**: Verify the starting state is safe

**Approach**:
```python
# After creating initial_state
assert initial_state.is_valid() == True
print("Initial state is valid")
```

**Expected Result**:
- Initial state should be valid (no microchips are fried at start)
- Floor 0: strontium, plutonium, elerium, dilithium - all as matching pairs (safe)
- Floor 1: thulium generator, ruthenium pair, curium pair (safe)
- Floor 2: thulium microchip alone (safe)
- Floor 3: empty (safe)

**Pass Criteria**: Initial state passes validation

---

### Test 4: Goal State Detection
**Purpose**: Ensure goal detection works with all 14 items

**Approach**:
```python
# Create a goal state manually
goal_floors = (frozenset(), frozenset(), frozenset(),
               frozenset([('elerium', 'G'), ('elerium', 'M'), ('dilithium', 'G'),
                         ('dilithium', 'M'), ('strontium', 'G'), ('strontium', 'M'),
                         ('plutonium', 'G'), ('plutonium', 'M'), ('thulium', 'G'),
                         ('thulium', 'M'), ('ruthenium', 'G'), ('ruthenium', 'M'),
                         ('curium', 'G'), ('curium', 'M')]))
goal_state = State(elevator_floor=3, floors=goal_floors)
assert goal_state.is_goal() == True
```

**Pass Criteria**: Goal state is correctly identified

---

### Test 5: Move Generation Validation
**Purpose**: Verify valid moves are generated correctly from initial state

**Approach**:
```python
# Generate moves from initial state
valid_moves = generate_valid_moves(initial_state)
print(f"Number of valid first moves: {len(valid_moves)}")

# Verify all generated moves are valid
for move in valid_moves:
    assert move.is_valid() == True

# Verify moves are logical (from floor 0 to floor 1)
for move in valid_moves:
    assert move.elevator_floor == 1, "All first moves should be to floor 1"

# Check that items moved make sense (1-2 items left floor 0)
initial_count = len(initial_state.floors[0])
for move in valid_moves:
    items_moved = initial_count - len(move.floors[0])
    assert 1 <= items_moved <= 2, "Should move 1-2 items per move"
```

**Expected Results**:
- Some number of valid moves should be generated (likely dozens given 8 items on floor 0)
- All moves should be to floor 1 (can only go up from floor 0)
- All moves should carry 1-2 items
- All resulting states should pass safety validation
- First moves should be logical (moving items up from floor 0)

**Pass Criteria**:
- All generated moves are valid states
- All moves go to floor 1
- All moves carry 1-2 items

---

### Test 6: Canonicalization with 7 Element Pairs
**Purpose**: Verify state canonicalization works correctly with more elements

**Test Cases**:

**Case 6a: Equivalent states are canonicalized identically**
```python
# Two states that differ only in element names but have same structure
state1_floors = (
    frozenset([('elerium', 'G'), ('elerium', 'M')]),
    frozenset([('dilithium', 'G'), ('dilithium', 'M')]),
    frozenset(),
    frozenset()
)
state1 = State(elevator_floor=0, floors=state1_floors)

state2_floors = (
    frozenset([('dilithium', 'G'), ('dilithium', 'M')]),
    frozenset([('elerium', 'G'), ('elerium', 'M')]),
    frozenset(),
    frozenset()
)
state2 = State(elevator_floor=0, floors=state2_floors)

# These should canonicalize to the same state
canonical1 = canonicalize_state(state1)
canonical2 = canonicalize_state(state2)
assert canonical1 == canonical2
```

**Case 6b: Different states remain different after canonicalization**
```python
# State with split pair vs. matched pair should be different
state1_floors = (
    frozenset([('elerium', 'G'), ('dilithium', 'M')]),
    frozenset(),
    frozenset(),
    frozenset()
)
state1 = State(elevator_floor=0, floors=state1_floors)

state2_floors = (
    frozenset([('elerium', 'G'), ('elerium', 'M')]),
    frozenset(),
    frozenset(),
    frozenset()
)
state2 = State(elevator_floor=0, floors=state2_floors)

canonical1 = canonicalize_state(state1)
canonical2 = canonicalize_state(state2)
assert canonical1 != canonical2
```

**Pass Criteria**: Canonicalization correctly identifies equivalent and different states

---

### Test 7: Solution Existence and Reasonableness
**Purpose**: Verify the BFS finds a solution and it's reasonable

**Approach**:
```python
min_steps = solve(initial_state)
print(f"Minimum steps: {min_steps}")

# Reasonableness checks
assert min_steps > 0, "Solution should require at least 1 step"
assert min_steps > 37, "Part 2 should take more steps than Part 1 (37 steps)"
assert min_steps < 200, "Solution should be found in reasonable number of steps"

# Run twice to verify determinism (BFS should always find same answer)
min_steps_2 = solve(initial_state)
assert min_steps == min_steps_2, "Solution should be deterministic"
```

**Expected Results**:
- Solution should exist (not return -1)
- Should be greater than Part 1's answer (37 steps) due to more items
- Should be less than some reasonable upper bound (e.g., 200 steps)
- Typical estimate: Part 1 with 10 items = 37 steps, Part 2 with 14 items likely ~55-65 steps
- Both runs should produce identical results (BFS is deterministic when using consistent state ordering)

**Pass Criteria**:
- `min_steps > 37` (more than Part 1)
- `min_steps < 200` (reasonable upper bound)
- `min_steps` is an integer
- Second run produces same result (determinism check)

---

### Test 8: Complete Integration Test
**Purpose**: Run the full solution end-to-end

**Approach**:
```bash
python part_2_solution.py
```

**Expected Output**:
- A single integer printed to stdout
- Integer should be > 37 and < 200
- Program should complete in reasonable time (< 5 minutes)

**Pass Criteria**:
- Program completes without errors
- Output is a valid integer in expected range
- No exceptions or infinite loops

---

### Test 9: Edge Case - Verify All Items Reach Floor 3
**Purpose**: Ensure the solution actually moves all 14 items to floor 3

**Approach**:
This is implicitly tested by the `is_goal()` method, but we can add verification:
```python
# Add assertion in solve() when goal is found
if next_state.is_goal():
    # Verify all 14 items are on floor 3
    assert len(next_state.floors[3]) == 14
    assert len(next_state.floors[0]) == 0
    assert len(next_state.floors[1]) == 0
    assert len(next_state.floors[2]) == 0
    return steps + 1
```

**Pass Criteria**: Goal state has all 14 items on floor 3, others empty

---

### Test 10: Performance Validation
**Purpose**: Ensure solution completes in reasonable time and canonicalization is effective

**Approach**:
```python
import time
start_time = time.time()
min_steps = solve(initial_state)
elapsed_time = time.time() - start_time
print(f"Solution found in {elapsed_time:.2f} seconds")

# Also print visited set size to validate canonicalization effectiveness
# This requires modifying solve() to return or print visited set size
print(f"Visited states explored: {len(visited)}")
```

**Expected Results**:
- Should complete in under 5 minutes
- Likely to complete in 10-120 seconds depending on hardware
- Visited set size should be in the thousands to tens of thousands (not millions)
- If it takes longer or visited set is enormous, canonicalization may not be working correctly

**Pass Criteria**:
- Completes in reasonable time (< 5 minutes)
- Visited set size is reasonable (< 100,000 states)

---

## Test Execution Order

1. **Test 1**: Verify initial state setup (quick validation)
2. **Test 2**: Safety rule validation (unit test)
3. **Test 3**: Initial state validity (integration check)
4. **Test 4**: Goal state detection (unit test)
5. **Test 5**: Move generation (integration check)
6. **Test 6**: Canonicalization (unit test - critical for performance)
7. **Test 9**: Add goal verification (modify solve function)
8. **Test 10**: Performance validation (full run with timing)
9. **Test 7**: Solution reasonableness (full run validation)
10. **Test 8**: Complete integration test (final verification)

## Success Criteria Summary

The solution passes if:
1. ✓ Initial state correctly contains all 8 items on floor 0 (including 4 new items)
2. ✓ Safety rules correctly validate all test cases
3. ✓ Initial state is valid
4. ✓ Goal state detection works with 14 items
5. ✓ Generated moves are all valid
6. ✓ Canonicalization correctly identifies equivalent states
7. ✓ Solution exists and is in range: 37 < min_steps < 200
8. ✓ Program completes without errors
9. ✓ Goal state has all 14 items on floor 3
10. ✓ Completes in under 5 minutes

## Debugging Strategies

If tests fail:

**If no solution found** (returns -1):
- Check if initial state is valid
- Verify move generation doesn't filter out all valid moves
- Check for bugs in safety validation (may be too restrictive)

**If solution takes too long**:
- Verify canonicalization is working (print visited set size periodically)
- Check for infinite loops in BFS
- Consider if state representation is causing hash collisions

**If solution is incorrect**:
- Verify goal state has all 14 items
- Check that BFS is correctly tracking steps
- Ensure moves are being generated correctly

**If answer seems too low/high**:
- Compare with Part 1 logic
- Verify all 4 new items were actually added
- Check item counts at each step

## Manual Verification

After getting a numeric answer, verify by:
1. Checking it's larger than Part 1's answer (37)
2. Ensuring it's plausible given 4 additional items (expected range: 55-65 steps)
3. Running twice to ensure deterministic result (BFS should always find same answer)
4. Checking visited set size is reasonable (thousands to tens of thousands, not millions) to confirm canonicalization is working

## Additional Optional Enhancement

### Test 11: Visited Set Size Monitoring (Optional)
**Purpose**: Validate canonicalization effectiveness by monitoring visited set growth

**Approach**:
Modify the `solve()` function to optionally print visited set size:
```python
def solve(initial_state, verbose=False):
    # ... existing code ...
    while queue:
        state, steps = queue.popleft()

        if verbose and len(visited) % 1000 == 0:
            print(f"Progress: {len(visited)} states visited, current depth: {steps}")

        # ... rest of solve logic ...

    if verbose:
        print(f"Total states visited: {len(visited)}")

    return -1
```

**Expected Results**:
- Visited set should grow steadily but not explosively
- Final size should be in thousands to tens of thousands
- If size exceeds 100,000, canonicalization may not be working optimally

**Pass Criteria**: Final visited set size < 100,000 states
