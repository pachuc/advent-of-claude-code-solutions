# Testing Plan: Evolved Sporifica Virus Simulation (Part 2)

## Overview
Verify that the 4-state virus simulation correctly implements the evolved behavior and produces accurate results for both test cases and the actual input.

## Test Strategy
1. **Unit tests**: Validate individual components
2. **Integration tests**: Verify the full simulation with known examples
3. **Edge case tests**: Handle boundary conditions
4. **Performance validation**: Ensure solution completes in reasonable time

---

## 1. Unit Tests

### Test 1.1: State Constants
**Purpose**: Verify state constants are defined correctly

**Test**:
```python
assert CLEAN == 0
assert WEAKENED == 1
assert INFECTED == 2
assert FLAGGED == 3
```

**Expected**: All assertions pass

---

### Test 1.2: State Transition Cycle
**Purpose**: Verify state advancement follows the 4-state cycle

**Test**:
```python
assert (CLEAN + 1) % 4 == WEAKENED
assert (WEAKENED + 1) % 4 == INFECTED
assert (INFECTED + 1) % 4 == FLAGGED
assert (FLAGGED + 1) % 4 == CLEAN
```

**Expected**: Complete cycle 0→1→2→3→0

---

### Test 1.3: Turning Logic
**Purpose**: Verify turn direction for each state

**Test**: Check that turns are applied correctly
- CLEAN (0): Turn left → direction_idx decreases by 1 (mod 4)
- WEAKENED (1): No turn → direction_idx stays same
- INFECTED (2): Turn right → direction_idx increases by 1 (mod 4)
- FLAGGED (3): Reverse → direction_idx increases by 2 (mod 4)

**Method**:
```python
# Start facing UP (idx=0)
direction_idx = 0

# CLEAN: turn left
direction_idx = (direction_idx - 1) % 4  # Should be 3 (LEFT)
assert direction_idx == 3

# WEAKENED: no turn (from LEFT)
# direction_idx stays 3
assert direction_idx == 3

# INFECTED: turn right (from LEFT)
direction_idx = (direction_idx + 1) % 4  # Should be 0 (UP)
assert direction_idx == 0

# FLAGGED: reverse (from UP)
direction_idx = (direction_idx + 2) % 4  # Should be 2 (DOWN)
assert direction_idx == 2
```

**Expected**: All direction changes match specification

---

### Test 1.4: Input Parsing
**Purpose**: Verify parse_input() correctly reads grid and returns dict

**Test**: Create a small test file
```
..#
#..
...
```

**Expected output**:
- `node_states = {(2, 0): INFECTED, (0, 1): INFECTED}`
- `center = (1, 1)`

**Validation**:
- Dictionary has exactly 2 entries
- Both entries have value INFECTED (2)
- Center is at middle of 3x3 grid

---

## 2. Integration Tests

### Test 2.1: Small Example - 100 Bursts
**Purpose**: Verify against the provided test case

**Input**:
```
..#
#..
...
```

**Expected output**: **26 infections** after 100 bursts

**Test method**:
1. Create test input file with the 3x3 grid
2. Run simulation for 100 bursts
3. Compare result to expected value

**Validation**:
```python
result = simulate_virus_evolved(states, (1, 1), 100)
assert result == 26, f"Expected 26, got {result}"
```

---

### Test 2.2: Small Example - 10,000,000 Bursts
**Purpose**: Verify the full simulation with the large test case

**Input**:
```
..#
#..
...
```

**Expected output**: **2,511,944 infections** after 10,000,000 bursts

**Test method**:
1. Create test input file with the 3x3 grid
2. Run simulation for 10,000,000 bursts
3. Compare result to expected value

**Validation**:
```python
result = simulate_virus_evolved(states, (1, 1), 10000000)
assert result == 2511944, f"Expected 2,511,944, got {result}"
```

**Performance**: Should complete in reasonable time (< 60 seconds)

---

### Test 2.3: Actual Input - Full Simulation
**Purpose**: Solve the actual puzzle and verify answer

**Input**: The actual 25x25 grid from input.md

**Test method**:
1. Run simulation with actual input for 10,000,000 bursts
2. Verify result is reasonable (should be > 100,000 and < 10,000,000)
3. Record the answer

**Validation**:
- Answer is a positive integer
- Answer is less than 10,000,000 (can't infect more than total bursts)
- Solution completes in reasonable time

---

## 3. Edge Case Tests

### Test 3.1: Empty Grid
**Purpose**: Verify behavior with all CLEAN nodes

**Input**:
```
...
...
...
```
(All clean nodes)

**Expected behavior**:
- Simulation runs without errors
- Some infections occur (carrier will infect nodes as it moves)
- Result is > 0

---

### Test 3.2: Fully Infected Grid
**Purpose**: Verify behavior with all INFECTED nodes

**Input**:
```
###
###
###
```
(All infected nodes)

**Expected behavior**:
- Simulation runs without errors
- Carrier will turn these to FLAGGED, then CLEAN, then WEAKENED, then count infections
- Result is > 0

---

### Test 3.3: Single Node Grid
**Purpose**: Verify behavior with minimal grid (1x1)

**Input**:
```
.
```

**Expected behavior**:
- Center is (0, 0)
- Simulation runs without errors
- Carrier starts on CLEAN node

---

### Test 3.4: Large Grid Boundaries
**Purpose**: Verify carrier can move beyond initial grid

**Test**: Run simulation and verify that:
- Carrier position can go negative (e.g., pos_x < 0, pos_y < 0)
- Carrier position can exceed grid size
- No index errors occur when accessing beyond initial grid

**Validation**: Simulation completes successfully (implicit validation)

---

## 4. Correctness Validation Tests

### Test 4.1: Only Count WEAKENED→INFECTED
**Purpose**: Verify we only count the correct state transition

**Test approach**: Create a test version that tracks all transitions

**Implementation**:
```python
def test_only_weakened_to_infected_counted():
    """Verify only WEAKENED→INFECTED transitions are counted."""
    # Run modified simulation with transition counters
    transitions = {
        'clean_to_weakened': 0,
        'weakened_to_infected': 0,
        'infected_to_flagged': 0,
        'flagged_to_clean': 0
    }

    # In the simulation loop, track each type:
    # if current_state == CLEAN:
    #     transitions['clean_to_weakened'] += 1
    # elif current_state == WEAKENED:
    #     transitions['weakened_to_infected'] += 1
    # ... etc

    # Run for small number of bursts (e.g., 100)
    # Then verify: infection_count == transitions['weakened_to_infected']
```

**Validation**: The infection count must equal only the WEAKENED→INFECTED count, not the sum of all transitions

---

### Test 4.2: State Dictionary Memory Management
**Purpose**: Verify CLEAN nodes are removed from dictionary

**Test approach**: Monitor dictionary size during simulation

**Implementation**:
```python
# Run simulation for 10M bursts and check final dict size
result = simulate_virus_evolved(states, center, 10000000)
final_dict_size = len(states)

# Success criteria:
assert final_dict_size < 100000, f"Dict too large: {final_dict_size}"
```

**Success criteria**:
- Dictionary size should be < 100,000 entries after 10M bursts
- This confirms CLEAN nodes are being removed
- If dict size approaches 10M, nodes aren't being cleaned up properly

**Alternative test**: Check that a specific node that cycles back to CLEAN is removed from dict:
```python
# Track a specific node through its cycle
# When it returns to CLEAN state, verify it's not in the dictionary
```

---

### Test 4.3: Initial Infected Nodes Not Counted Immediately
**Purpose**: Verify we don't count nodes that start infected until they complete a cycle

**Test**:
- Input with some infected nodes (e.g., the 3x3 example)
- Initially infected nodes cycle: INFECTED → FLAGGED → CLEAN → WEAKENED → INFECTED
- They should only be counted when they transition WEAKENED→INFECTED (the 4th transition in the cycle)

**Implementation**:
```python
# Track the first few bursts manually
# For the 3x3 example with nodes at (2,0) and (0,1) starting as INFECTED:
# These nodes won't be counted immediately
# They must first become FLAGGED, then CLEAN, then WEAKENED
# Only then (after 3 more visits) will they be counted

# Run a small simulation and verify no immediate counting
# of initially infected nodes in the first burst
```

**Validation**: The infection count in burst 1 should only reflect nodes that were WEAKENED before that burst, not nodes that started INFECTED

---

### Test 4.4: Direction Cycling
**Purpose**: Verify direction indices wrap correctly

**Test**:
```python
# Test all 4 directions cycle correctly
for i in range(8):  # Go around twice
    idx = i % 4
    assert idx in [0, 1, 2, 3]
    assert DIRECTIONS[idx] in [(0, -1), (1, 0), (0, 1), (-1, 0)]
```

---

## 5. Performance Tests

### Test 5.1: Execution Time
**Purpose**: Ensure solution completes in reasonable time

**Test**: Time the full simulation with actual input

**Expected**:
- Completion time < 60 seconds (preferably < 30 seconds)
- No infinite loops
- No memory exhaustion

**Method**:
```python
import time
start = time.time()
result = simulate_virus_evolved(states, center, 10000000)
elapsed = time.time() - start
print(f"Time: {elapsed:.2f}s")
assert elapsed < 60, "Solution too slow"
```

---

### Test 5.2: Memory Usage
**Purpose**: Verify dictionary doesn't grow unbounded

**Test**: Check final dictionary size after full simulation

**Method**:
```python
# Run full simulation and check final size
states, center = parse_input('input.md')
result = simulate_virus_evolved(states, center, 10000000)
final_size = len(states)
print(f"Final dictionary size: {final_size}")

# Verify reasonable size
assert final_size < 100000, f"Dictionary too large: {final_size}"
```

**Expected**:
- Dictionary size < 100,000 entries (likely much smaller)
- Should not approach millions of entries
- Confirms CLEAN node removal is working

**Optional enhanced test**: Add print statements at intervals:
```python
# In simulation loop, add:
if burst_num % 1000000 == 0:
    print(f"Burst {burst_num}: dict size = {len(states)}")
```

---

## 6. Regression Test Against Part 1

### Test 6.1: Verify Part 1 Still Works
**Purpose**: Ensure we didn't break anything from Part 1

**Test**: Keep Part 1 solution and verify it still produces 5404

**Note**: This is informational only; Part 2 is a different algorithm

---

## 7. Final Validation Checklist

Before considering the solution complete, verify:

- [ ] **Unit tests pass**: State constants, transitions, and parsing work correctly
- [ ] **Small example (100 bursts)** produces exactly **26 infections**
- [ ] **Small example (10M bursts)** produces exactly **2,511,944 infections**
- [ ] **Actual input completes** in < 60 seconds (preferably < 30 seconds)
- [ ] **No runtime errors** or exceptions during execution
- [ ] **Output is a single integer** printed to stdout
- [ ] **Infinite grid handling**: No boundary errors when carrier moves far from origin
- [ ] **Correct counting**: Only WEAKENED→INFECTED transitions are counted
- [ ] **Memory efficiency**: Final dictionary size is reasonable (< 100K entries)
- [ ] **Code quality**: Clean, well-documented, follows implementation plan
- [ ] **Initially infected nodes**: Not counted until they complete a full 4-state cycle

---

## Test Execution Order

Run tests in this order to catch bugs early and save time:

1. **Unit tests** (1.1 - 1.4) - < 1 second total, verify components
2. **Small integration test** (2.1) - 100 bursts, < 1 second, verify logic
3. **Edge cases** (3.1 - 3.4) - < 5 seconds, verify robustness
4. **Correctness tests** (4.1 - 4.4) - < 5 seconds, verify specific requirements
5. **Large integration test** (2.2) - 10M bursts on small example, 10-30 seconds
6. **Performance test** (5.1) - Time the full solution, 10-30 seconds
7. **Final validation** (2.3) - Run actual input and get answer, 10-30 seconds

**Rationale**: If there's a bug in the core logic, tests 1-4 will catch it in < 10 seconds. Only proceed to expensive 10M-burst tests if early tests pass.

---

## Debugging Strategy

If tests fail:

1. **Wrong count on 100-burst test**:
   - Add debug output to print each burst's state
   - Manually trace first 5-10 bursts
   - Verify turning logic
   - Verify state transitions

2. **Wrong count on 10M-burst test**:
   - Verify 100-burst test passes first
   - Check for integer overflow (unlikely in Python)
   - Verify we're not double-counting

3. **Performance issues**:
   - Profile the code to find bottleneck
   - Ensure dictionary operations are O(1)
   - Check for unnecessary copying or allocations

4. **Memory issues**:
   - Verify CLEAN nodes are being removed
   - Check dictionary size during execution
   - Ensure no memory leaks in loop

---

## Success Criteria

The solution is correct when:
1. All unit tests pass
2. Small example (100 bursts) returns 26
3. Small example (10M bursts) returns 2,511,944
4. Actual input produces a reasonable answer
5. Execution completes in < 60 seconds
6. No errors or warnings during execution
