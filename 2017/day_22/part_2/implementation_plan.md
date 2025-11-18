# Implementation Plan: Evolved Sporifica Virus Simulation (Part 2)

## Overview
Extend the Part 1 solution to support a 4-state infection cycle with more complex turning logic and run for 10 million bursts instead of 10 thousand.

## Key Differences from Part 1
1. **State model**: 4 states (CLEAN, WEAKENED, INFECTED, FLAGGED) vs 2 states
2. **Turn logic**: 4 different turn behaviors based on node state
3. **Iteration count**: 10,000,000 bursts (1000x more than Part 1)
4. **Counting**: Only count WEAKENED→INFECTED transitions

## Reusable Components from Part 1
- `parse_input()` function - can be reused as-is
- `DIRECTIONS` constant - identical direction system
- Overall simulation loop structure
- Input/output handling

## Implementation Steps

### Step 1: Define State Constants
Create integer constants for the 4 states:
```python
CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3
```

**Rationale**: Using integers (0-3) is more memory-efficient than strings or enums, which matters for 10M iterations. The states form a natural cycle: (state + 1) % 4.

### Step 2: Modify Data Structure for Node States
Change from a set-based approach (Part 1) to a dictionary-based approach:
- **Part 1**: Used `set` to track only infected nodes (2 states: in set = infected, not in set = clean)
- **Part 2**: Use `dict` mapping positions to state integers
- **Optimization**: Nodes not in dictionary are implicitly CLEAN (state 0)
- **Type**: `Dict[Tuple[int, int], int]` mapping (x, y) → state

**Rationale**: We need to track 4 states, not just 2. Dictionary allows sparse representation (only store non-clean nodes), crucial for memory efficiency on infinite grid.

### Step 3: Adapt parse_input() Function
Modify the existing `parse_input()` from Part 1 to return a dictionary instead of a set:

**Changes from Part 1**:
- Line 38: `infected_nodes = set()` → `node_states = {}`
- Line 42: `infected_nodes.add((x, y))` → `node_states[(x, y)] = INFECTED`
- Line 44: Return type changes from set to dict

**Implementation**:
```python
def parse_input(filename):
    """
    Read grid from file and return dict of node states.

    Args:
        filename: path to input file

    Returns:
        node_states: dict mapping (x, y) to state integer
        center: (x, y) tuple for starting position
    """
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    height = len(lines)
    width = len(lines[0]) if lines else 0

    # Calculate center position
    center_x = width // 2
    center_y = height // 2

    # Find all infected nodes and create state dictionary
    node_states = {}  # Changed from set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                node_states[(x, y)] = INFECTED  # Store as dict entry, not set member

    return node_states, (center_x, center_y)
```

**Notes**:
- All nodes marked with '#' start as INFECTED (state 2)
- No nodes start as WEAKENED or FLAGGED
- Nodes not in the dictionary are implicitly CLEAN (state 0)

### Step 4: Implement State-Based Turning Logic
For optimal performance, inline the turning logic directly in the main loop instead of using a helper function. The turning rules based on current state are:

- **CLEAN**: Turn LEFT (counter-clockwise) → `direction_idx = (direction_idx - 1) % 4`
- **WEAKENED**: No turn (continue straight) → no change to direction_idx
- **INFECTED**: Turn RIGHT (clockwise) → `direction_idx = (direction_idx + 1) % 4`
- **FLAGGED**: REVERSE (180 degrees) → `direction_idx = (direction_idx + 2) % 4`

**Rationale**: Inlining avoids function call overhead for 10M iterations. The logic is simple enough that a helper function doesn't improve readability significantly.

**Implementation approach**:
```python
# Get current state
current_state = states.get((pos_x, pos_y), CLEAN)

# Turn based on state (inlined for performance)
if current_state == CLEAN:
    direction_idx = (direction_idx - 1) % 4  # Left
elif current_state == WEAKENED:
    pass  # No turn
elif current_state == INFECTED:
    direction_idx = (direction_idx + 1) % 4  # Right
else:  # FLAGGED
    direction_idx = (direction_idx + 2) % 4  # Reverse
```

### Step 5: Implement State Transition Logic
The state cycle is deterministic: CLEAN(0) → WEAKENED(1) → INFECTED(2) → FLAGGED(3) → CLEAN(0)

**Implementation**: Inline the state advancement using modulo arithmetic: `(current_state + 1) % 4`

**Rationale**: This is a simple modulo operation. For 10M iterations, keeping this inline is faster than function call overhead.

### Step 6: Create Main Simulation Function
Adapt `simulate_virus()` from Part 1 with the following changes:

```python
def simulate_virus_evolved(node_states, start_pos, num_bursts=10000000):
    """
    Simulate evolved virus carrier with 4-state infection cycle.

    Args:
        node_states: dict mapping (x, y) to state integer
        start_pos: (x, y) starting position
        num_bursts: number of bursts to simulate (default 10 million)

    Returns:
        count of WEAKENED→INFECTED transitions
    """
    # Create mutable copy of node states
    states = dict(node_states)

    # Initialize carrier state
    pos_x, pos_y = start_pos
    direction_idx = 0  # Start facing UP (0=UP, 1=RIGHT, 2=DOWN, 3=LEFT)
    infection_count = 0

    # Run simulation
    for _ in range(num_bursts):
        # Get current node state (default to CLEAN if not in dict)
        current_state = states.get((pos_x, pos_y), CLEAN)

        # Step 1: Turn based on current state (inlined for performance)
        if current_state == CLEAN:
            direction_idx = (direction_idx - 1) % 4  # Left
        elif current_state == WEAKENED:
            pass  # No turn
        elif current_state == INFECTED:
            direction_idx = (direction_idx + 1) % 4  # Right
        else:  # FLAGGED
            direction_idx = (direction_idx + 2) % 4  # Reverse

        # Step 2: Advance state in cycle
        new_state = (current_state + 1) % 4

        # Count if transitioning WEAKENED → INFECTED
        if current_state == WEAKENED:  # and new_state will be INFECTED
            infection_count += 1

        # Update state (remove if returning to CLEAN to save memory)
        if new_state == CLEAN:
            states.pop((pos_x, pos_y), None)  # Remove to save memory
        else:
            states[(pos_x, pos_y)] = new_state

        # Step 3: Move forward
        dx, dy = DIRECTIONS[direction_idx]
        pos_x += dx
        pos_y += dy

    return infection_count
```

**Key optimizations**:
1. Use `dict.get()` with default for implicit CLEAN nodes
2. Remove nodes when they return to CLEAN state to save memory
3. Inline state advancement and turning logic to avoid function call overhead
4. Count infections before state update (when current is WEAKENED)

### Step 7: Update main() Function
Modify to call the new simulation function:

```python
def main():
    """Main entry point for the solution."""
    # Parse input (reuse from Part 1, adapted for dict)
    node_states, center = parse_input('input.md')

    # Run simulation for 10,000,000 bursts
    result = simulate_virus_evolved(node_states, center, 10000000)

    # Print result
    print(result)
```

### Step 8: Add Constants and Documentation
At the top of the file:
- No imports needed - using only built-in Python
- State constants (CLEAN, WEAKENED, INFECTED, FLAGGED)
- DIRECTIONS constant with explicit documentation
- Docstring explaining the problem

**Constants**:
```python
# Direction constants (screen coordinates: y increases downward)
# Direction indices: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
# Each tuple is (dx, dy) for movement
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# State constants for 4-state infection cycle
CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3
```

## Efficiency Considerations

### Time Complexity
- **Per burst**: O(1) - all operations are constant time (dict lookup, arithmetic, dict update)
- **Total**: O(n) where n = 10,000,000 bursts
- **Expected runtime**: Should complete in under 30 seconds on modern hardware

### Space Complexity
- **Dictionary size**: Will grow but remains bounded by visited area
- **Memory optimization**: Removing CLEAN nodes keeps dict size minimal
- **Expected**: Likely < 100,000 entries in dictionary (based on typical virus spread patterns)

### Potential Bottlenecks
1. **Dictionary operations**: Python dicts are highly optimized, should be fine
2. **Tuple hashing**: Position tuples (x, y) need hashing for dict keys - negligible overhead
3. **Range iteration**: 10M iterations - using `range()` is fine, no list materialization

### Not Needed (Script-Level Solution)
- No need for numpy or other libraries
- No need for parallel processing
- No need for progress bars or logging
- No need for input validation (trust the input format)

## File Structure
Single Python file: `solution.py`

**Complete structure**:
```python
# Docstring
"""
Evolved Sporifica Virus Simulation - Advent of Code 2017 Day 22 Part 2

Simulates a virus carrier with 4-state infection cycle.
"""

# Constants (no imports needed)
# Direction indices: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3

# Functions
def parse_input(filename): ...
def simulate_virus_evolved(node_states, start_pos, num_bursts): ...

# Main
def main(): ...

if __name__ == '__main__':
    main()
```

## Algorithm Summary
1. Parse input grid into dictionary of {position: INFECTED}
2. Initialize carrier at center, facing UP
3. For each of 10,000,000 bursts:
   - Get current node state (default CLEAN if not in dict)
   - Turn based on state (left/none/right/reverse)
   - Advance state in cycle (0→1→2→3→0)
   - Count if WEAKENED→INFECTED transition
   - Update dict (remove if CLEAN)
   - Move forward one step
4. Return infection count
