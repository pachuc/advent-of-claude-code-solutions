# Testing Plan: Cave Navigation with Tool Switching

## Testing Strategy Overview

This plan covers:
1. **Unit tests** for individual components
2. **Integration tests** for pathfinding logic
3. **Validation tests** using provided example
4. **Regression tests** against Part 1 functionality
5. **Edge case tests** for boundary conditions

## Test 1: Validate Cave Map Generation

**Purpose**: Ensure cave map correctly extends beyond target and matches Part 1 logic

**Test Cases**:

### 1.1: Cave Map Consistency with Part 1
```python
# Test that region types match Part 1 within target bounds
depth = 510
target_x, target_y = 10, 10

cave_map = build_cave_map(depth, target_x, target_y, margin=0)

# Verify specific known values from example
# Note: cave_map uses [y][x] indexing, so cave_map[y][x] = region at position (x, y)
assert cave_map[0][0] == ROCKY  # Cave mouth at (0, 0) is always rocky
assert cave_map[target_y][target_x] == ROCKY  # Target is always rocky

# Cross-check erosion levels with Part 1 implementation
# For position at x=1, y=0 (row 0, column 1):
# geologic_index = 1 * 16807 = 16807
# erosion_level = (16807 + 510) % 20183 = 17317
# type = 17317 % 3 = 1 (WET)
assert cave_map[0][1] == WET  # Position (x=1, y=0) should be WET
```

**Expected**: All assertions pass, confirming cave generation is correct.

### 1.2: Extended Map Beyond Target
```python
# Test that map extends properly beyond target
cave_map = build_cave_map(depth, target_x, target_y, margin=50)

# Should have regions beyond target
assert len(cave_map) > target_y  # More rows than target_y
assert len(cave_map[0]) > target_x  # More columns than target_x

# Extended regions should follow same rules
# Verify a region beyond target has valid type (0, 1, or 2)
# Use +5 to stay safely within margin=50 bounds
assert cave_map[target_y + 5][target_x + 5] in {ROCKY, WET, NARROW}
```

**Expected**: Map successfully extends beyond target with valid region types.

## Test 2: Equipment and Region Validation

**Purpose**: Verify equipment constraints are correctly enforced

**Test Cases**:

### 2.1: Valid Equipment Sets
```python
# Rocky regions
assert get_valid_equipment(ROCKY) == {TORCH, CLIMBING_GEAR}
assert NEITHER not in get_valid_equipment(ROCKY)

# Wet regions
assert get_valid_equipment(WET) == {CLIMBING_GEAR, NEITHER}
assert TORCH not in get_valid_equipment(WET)

# Narrow regions
assert get_valid_equipment(NARROW) == {TORCH, NEITHER}
assert CLIMBING_GEAR not in get_valid_equipment(NARROW)
```

**Expected**: All assertions pass.

### 2.2: Movement Validation
```python
# Can move from rocky (with torch) to rocky
assert can_move(TORCH, ROCKY) == True

# Cannot move from rocky (with neither) - neither invalid for rocky
assert can_move(NEITHER, ROCKY) == False

# Cannot move from wet (with climbing gear) to narrow - CG not valid in narrow
assert can_move(CLIMBING_GEAR, NARROW) == False

# Can move from wet (with neither) to narrow
assert can_move(NEITHER, NARROW) == True

# Cannot move with torch into wet region
assert can_move(TORCH, WET) == False
```

**Expected**: Movement validation correctly enforces equipment constraints.

## Test 3: State Transition Generation

**Purpose**: Verify get_neighbors generates all valid transitions correctly

**Test Cases**:

### 3.1: Equipment Switching Transitions
```python
# At position (5, 5) in a ROCKY region
# Valid equipment: TORCH, CLIMBING_GEAR
# Current: TORCH

# Create small test cave
cave_map = [[ROCKY] * 10 for _ in range(10)]
state = (5, 5, TORCH)
neighbors = list(get_neighbors(state, cave_map, 9, 9))

# Should have one equipment switch: TORCH -> CLIMBING_GEAR (cost 7)
switch_neighbors = [(s, c) for s, c in neighbors if c == 7]
assert len(switch_neighbors) == 1
assert switch_neighbors[0] == ((5, 5, CLIMBING_GEAR), 7)
```

**Expected**: Exactly one equipment switch transition with cost 7.

### 3.2: Movement Transitions
```python
# At position (5, 5, TORCH) in ROCKY region
# All adjacent regions are ROCKY (torch valid everywhere)

cave_map = [[ROCKY] * 10 for _ in range(10)]
state = (5, 5, TORCH)
neighbors = list(get_neighbors(state, cave_map, 9, 9))

# Should have 4 movement transitions (up, down, left, right)
move_neighbors = [(s, c) for s, c in neighbors if c == 1]
assert len(move_neighbors) == 4

expected_positions = {(4, 5), (6, 5), (5, 4), (5, 6)}
actual_positions = {(x, y) for (x, y, e), c in move_neighbors}
assert actual_positions == expected_positions

# All should keep same equipment
assert all(e == TORCH for (x, y, e), c in move_neighbors)
```

**Expected**: Four movement transitions in cardinal directions, all cost 1.

### 3.3: Blocked Movement (Equipment Invalid)
```python
# At position (0, 0, TORCH)
# Right cell (1, 0) is WET (can't use torch there)

cave_map = [[ROCKY, WET, ROCKY]]
state = (0, 0, TORCH)
neighbors = list(get_neighbors(state, cave_map, 2, 0))

# Should NOT have movement to (1, 0)
move_neighbors = [(s, c) for s, c in neighbors if c == 1]
positions = [(x, y) for (x, y, e), c in move_neighbors]
assert (1, 0) not in positions
```

**Expected**: Invalid movements are filtered out.

### 3.4: Boundary Conditions
```python
# At corner (0, 0), should only have 2 movement options (right, down)
cave_map = [[ROCKY] * 5 for _ in range(5)]
state = (0, 0, TORCH)
neighbors = list(get_neighbors(state, cave_map, 4, 4))

move_neighbors = [(s, c) for s, c in neighbors if c == 1]
assert len(move_neighbors) == 2
positions = {(x, y) for (x, y, e), c in move_neighbors}
assert positions == {(1, 0), (0, 1)}
```

**Expected**: Boundary checks prevent out-of-bounds transitions.

## Test 4: Example Validation

**Purpose**: Verify solution matches provided example

**Test Case**:

```python
# Given example
depth = 510
target_x, target_y = 10, 10

result = find_shortest_path(depth, target_x, target_y)

# Expected: 45 minutes
assert result == 45
```

**Expected output**: `45`

**Failure mode**: If result ≠ 45:
- Check cave map generation (verify indexing is [y][x])
- Add debug logging to trace the path found
- Verify equipment switching costs (should be 7, not 1)
- Verify we're requiring torch at target
- Check that starting equipment is TORCH

## Test 5: Actual Input Validation

**Purpose**: Solve the actual puzzle input

**Test Case**:

```python
depth = 3558
target_x, target_y = 15, 740

result = find_shortest_path(depth, target_x, target_y)

# Result should be positive integer
assert isinstance(result, int)
assert result > 0

# Sanity check: minimum possible is Manhattan distance
manhattan = target_x + target_y  # 15 + 740 = 755
assert result >= manhattan

# Upper bound: Based on example, ratio of actual/manhattan is ~2.25 (45/20)
# Use factor of 3 as reasonable upper bound
assert result < manhattan * 3  # Should be less than 2265

print(f"Actual input result: {result}")
print(f"Manhattan distance: {manhattan}")
print(f"Ratio: {result / manhattan:.2f}")
```

**Expected**: Result is reasonable integer value (likely in range 755-1700).

## Test 6: Edge Cases

**Purpose**: Test boundary conditions and special cases

### 6.1: Starting Equipment Validation
```python
# Verify pathfinding starts with TORCH at (0, 0)
# Create a simple test case
depth = 510
target_x, target_y = 1, 0

result = find_shortest_path(depth, target_x, target_y)

# Should be able to reach (1, 0) in at least 1 minute
assert result >= 1
assert isinstance(result, int)
```

### 6.2: Adjacent Target
```python
# Target at (1, 0) - one step away
# Verify optimal path is found quickly
depth = 510
target_x, target_y = 1, 0

import time
start = time.time()
result = find_shortest_path(depth, target_x, target_y)
elapsed = time.time() - start

# Should complete very quickly (< 0.1 seconds)
assert elapsed < 0.1
assert result >= 1  # At minimum, one move
```

### 6.3: Boundary Checks
```python
# Verify that negative coordinates are not explored
# This is implicit in the bounds checking, but we can verify
# by checking that the algorithm doesn't crash on edge positions

depth = 510
target_x, target_y = 2, 2

# Should successfully find path without trying negative coordinates
result = find_shortest_path(depth, target_x, target_y)
assert result > 0
```

### 6.4: Multiple Equipment Switches
```python
# The provided example already tests this (3 switches for 10,10 case)
# This is covered in Test 4
# Note: This validates that equipment switching logic works correctly
```

## Test 7: Performance Validation

**Purpose**: Ensure solution runs in reasonable time

**Test Case**:

```python
import time

depth = 3558
target_x, target_y = 15, 740

start_time = time.time()
result = find_shortest_path(depth, target_x, target_y)
end_time = time.time()

elapsed = end_time - start_time

print(f"Runtime: {elapsed:.2f} seconds")

# Should complete in under 10 seconds
assert elapsed < 10.0
```

**Expected**: Runtime < 10 seconds (likely < 5 seconds).

## Test 8: Path Reconstruction (Debug)

**Purpose**: For debugging, optionally reconstruct the path to verify correctness

**Method**:

Modify Dijkstra to track parent pointers:
```python
# In Dijkstra's loop, track:
parent = {}  # state -> (parent_state, action)

# Then reconstruct path from target back to start
def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current][0]
    path.reverse()
    return path
```

**Validation**:
- Count movement steps vs switches
- Verify equipment is valid at each position
- Verify total cost matches result

## Test 9: Regression Test Against Part 1

**Purpose**: Ensure Part 1 functionality still works (if Part 1 code is reused)

**Test Case**:

```python
# Verify that the cave generation produces correct risk levels
# We can use our own cave_map to calculate risk and compare to Part 1 answer

depth = 3558
target_x, target_y = 15, 740

# Build cave map (no margin needed for risk calculation)
cave_map = build_cave_map(depth, target_x, target_y, margin=0)

# Calculate total risk
total_risk = 0
for y in range(target_y + 1):
    for x in range(target_x + 1):
        total_risk += cave_map[y][x]

# Should match Part 1 answer
assert total_risk == 11810

print("Part 1 regression test passed")
```

**Expected**: Part 1 answer is still correct (11810).

## Testing Execution Order

1. **Unit tests first** (Tests 2, 3): Validate individual components
2. **Cave generation** (Test 1): Ensure map building works
3. **Example validation** (Test 4): Verify against known answer
4. **Actual input** (Test 5): Solve the puzzle
5. **Edge cases** (Test 6): Ensure robustness
6. **Performance** (Test 7): Check runtime
7. **Regression** (Test 9): Ensure Part 1 still works
8. **Path reconstruction** (Test 8): Only if debugging needed

## Success Criteria

✅ All unit tests pass
✅ Example returns 45
✅ Actual input returns reasonable value (755-1500 range)
✅ Runtime < 10 seconds
✅ Part 1 regression test passes

## Debugging Strategy

If tests fail:

1. **Wrong answer on example**:
   - Add logging to trace path
   - Verify equipment switching cost (7 not 1)
   - Check equipment validity constraints
   - Verify target requires torch

2. **Timeout or very slow**:
   - Reduce margin size
   - Check for infinite loops
   - Verify visited set is working
   - Profile with cProfile

3. **No path found**:
   - Check margin is large enough
   - Verify transitions are bidirectional
   - Check boundary conditions

4. **Part 1 regression fails**:
   - Ensure cave generation logic unchanged
   - Check geologic_index calculation

## Final Validation

Before submitting:
- Run solution on example: should output `45`
- Run solution on actual input: should output reasonable integer
- Verify output is just the number (no extra text)
- Check runtime is acceptable
