# Implementation Plan: Lumber Collection Area - Part 2

## Overview
Simulate a 50x50 cellular automaton for 1,000,000,000 minutes using cycle detection to avoid computing all iterations. The Part 1 solution already handles the simulation logic; we need to extend it with cycle detection and modular arithmetic.

## Algorithm Efficiency Analysis
- **Input Size**: 50x50 grid = 2,500 cells
- **Target**: 1,000,000,000 iterations
- **Direct Simulation**: Would require ~2.5 trillion cell updates (infeasible)
- **Cycle Detection Approach**: Expected to find cycle within 1,000-10,000 iterations
- **Time Complexity**: O(k × n²) where k is iterations until cycle detected, n is grid dimension
- **Space Complexity**: O(k × n²) to store seen states in dictionary

## Step-by-Step Implementation Plan

### Step 1: Reuse Core Simulation Logic from Part 1
**File**: `part_1_solution.py` (lines 1-88)

**Action**: Copy the following functions that are already correct:
- `parse_input()` - Converts input text to 2D grid (with validation added)
- `count_neighbors()` - Counts adjacent cells of a specific type
- `get_next_state()` - Determines next state based on rules
- `simulate_step()` - Performs one iteration with simultaneous updates
- `calculate_resource_value()` - Counts trees × lumberyards

**Rationale**: These functions are working correctly for Part 1 and the transformation rules are identical in Part 2.

**Enhancement**: Add validation to `parse_input()`:
```python
def parse_input(input_text):
    """Parse the input text into a 2D grid."""
    lines = input_text.strip().split('\n')
    grid = []
    for line in lines:
        grid.append(list(line.strip()))

    # Validate grid dimensions
    assert len(grid) == 50, f"Expected 50 rows, got {len(grid)}"
    assert all(len(row) == 50 for row in grid), "Expected all rows to be 50 characters"

    return grid
```
This helps catch input file issues early.

### Step 2: Create Grid State Hashing Function
**New Function**: `grid_to_tuple(grid)`

**Purpose**: Convert 2D list to hashable representation for cycle detection

**Implementation Details**:
```python
def grid_to_tuple(grid):
    """Convert grid to immutable tuple for use as dictionary key."""
    return tuple(tuple(row) for row in grid)
```

**Why**: Python lists are not hashable and cannot be dictionary keys. We need an immutable representation to store in our seen_states dictionary.

**Note**: An alternative would be to use a string (`''.join(''.join(row) for row in grid)`), but tuples are more Pythonic and clearer in intent.

### Step 3: Implement Cycle Detection Logic
**New Function**: `simulate_with_cycle_detection(grid, target_minutes)`

**Algorithm**:
1. Initialize tracking structures:
   - `seen_states = {}` - Maps grid state → minute number when first seen
   - `minute = 0`
   - `current_grid = grid`

2. Main simulation loop:
   ```python
   while minute < target_minutes:
       state_key = grid_to_tuple(current_grid)

       if state_key in seen_states:
           # Cycle detected!
           cycle_start = seen_states[state_key]
           cycle_length = minute - cycle_start
           break

       seen_states[state_key] = minute
       current_grid = simulate_step(current_grid)
       minute += 1
   ```

3. If loop completes without cycle, return current_grid (unlikely with 1B iterations)

**Key Insight**: When we see a repeated state, we know all future states will repeat in the same pattern.

### Step 4: Calculate Final State Using Modular Arithmetic
**Logic within**: `simulate_with_cycle_detection()`

**When cycle is detected**:
1. We have:
   - `cycle_start`: The minute when the cycle begins (first occurrence of repeated state)
   - `cycle_length`: How many minutes the cycle spans (minute - cycle_start)
   - `target_minutes`: 1,000,000,000

2. Calculate which position in the cycle corresponds to target:
   ```python
   # How many minutes after the cycle starts do we need to reach target?
   remaining_minutes = target_minutes - cycle_start
   # Which position in the repeating cycle does this correspond to?
   position_in_cycle = remaining_minutes % cycle_length
   # Map back to the actual minute number we have stored
   final_minute = cycle_start + position_in_cycle
   ```

   **Why this works**: After `cycle_start`, the pattern repeats every `cycle_length` minutes.
   So minute `cycle_start + k` has the same state as minute `cycle_start + (k % cycle_length)`.

3. Retrieve the grid state at `final_minute` from our stored states:
   - We maintain a second dictionary: `states_by_minute = {}`
   - This stores the actual grid at each minute for retrieval

**Storage Strategy**: Store both mappings during simulation:
- `seen_states[grid_tuple] = minute` (for cycle detection)
- `states_by_minute[minute] = grid` (for retrieval)

**Why not reconstruct?**: We could save memory by only storing cycle states and reconstructing, but for expected cycle sizes (<10,000 iterations), storing all states uses acceptable memory and is simpler.

### Step 5: Retrieve and Calculate Final Answer
**Implementation**:
```python
# After calculating final_minute
final_grid = states_by_minute[final_minute]
return calculate_resource_value(final_grid)
```

**Verification**: The final_minute is guaranteed to be in range [cycle_start, cycle_start + cycle_length - 1], and we've stored all states from 0 to minute-1, so the lookup will always succeed.

### Step 6: Update Main Function
**Modifications to `main()`**:
```python
def main():
    with open('input.md', 'r') as f:
        input_text = f.read()

    grid = parse_input(input_text)

    # Use new function with cycle detection
    result = simulate_with_cycle_detection(grid, target_minutes=1_000_000_000)

    print(result)
```

## Complete Function Structure

### Functions to Keep from Part 1 (unchanged):
1. `parse_input(input_text)` → list[list[str]]
2. `count_neighbors(grid, row, col, target_type)` → int
3. `get_next_state(grid, row, col)` → str
4. `simulate_step(grid)` → list[list[str]]
5. `calculate_resource_value(grid)` → int

### New Functions for Part 2:
1. `grid_to_tuple(grid)` → tuple[tuple[str]]
2. `simulate_with_cycle_detection(grid, target_minutes)` → int

### Modified Function:
1. `main()` - Update to call new simulation function

## Detailed Implementation of Cycle Detection Function

```python
def simulate_with_cycle_detection(grid, target_minutes):
    """
    Simulate grid until cycle detected, then calculate final state.

    Returns the resource value at target_minutes.
    """
    seen_states = {}  # grid_tuple -> minute first seen
    states_by_minute = {}  # minute -> grid (for retrieval)

    current_grid = grid
    minute = 0

    while minute < target_minutes:
        # Convert to hashable form
        state_key = grid_to_tuple(current_grid)

        # Check for cycle
        if state_key in seen_states:
            cycle_start = seen_states[state_key]
            cycle_length = minute - cycle_start

            # Calculate which state in cycle = target minute
            remaining_minutes = target_minutes - cycle_start
            position_in_cycle = remaining_minutes % cycle_length
            final_minute = cycle_start + position_in_cycle

            # Get the grid at that minute
            final_grid = states_by_minute[final_minute]

            return calculate_resource_value(final_grid)

        # Store this state
        seen_states[state_key] = minute
        states_by_minute[minute] = [row[:] for row in current_grid]  # Deep copy

        # Simulate next step
        current_grid = simulate_step(current_grid)
        minute += 1

    # If we somehow reach target without cycle (very unlikely for large targets)
    # This should never happen for target_minutes = 1,000,000,000
    if target_minutes > 100000:
        raise RuntimeError(
            f"No cycle detected after {minute} iterations - this is unexpected! "
            "The cellular automaton should have entered a cycle by now."
        )
    return calculate_resource_value(current_grid)
```

## Memory Considerations

**Grid Storage**: Each grid is 50×50 = 2,500 characters

**Two Dictionaries Required**:
1. `seen_states`: Maps grid tuples to minute numbers
   - Stores tuples of tuples (immutable)
   - At 10,000 states: ~25 MB for tuple data + dict overhead

2. `states_by_minute`: Maps minute numbers to grid lists
   - Stores lists of lists (mutable, for deep copying)
   - At 10,000 states: ~25 MB for list data + dict overhead

**Total Memory Usage**:
- If cycle detected at minute 1,000: ~5 MB (both dictionaries)
- If cycle detected at minute 10,000: ~50 MB (both dictionaries)
- Python dict overhead: ~200-400 bytes per entry × 2 dictionaries
- Expected total: <100 MB worst case (well within reasonable limits)

**Why Both Dictionaries?**:
- `seen_states` needs hashable keys (tuples) for O(1) cycle detection
- `states_by_minute` provides O(1) retrieval of the actual grid for final answer
- The memory trade-off is acceptable given the expected cycle sizes

## Edge Cases to Handle

1. **Early cycles**: Cycle might start at minute 0 (initial grid repeats immediately)
   - Handled: Algorithm works correctly even if cycle_start = 0

2. **Late cycles**: Cycle might not appear until after many iterations
   - Handled: We continue iterating until cycle found, with safeguard at 100,000 iterations

3. **No cycle before target**: Extremely unlikely for cellular automata
   - Handled: Raises RuntimeError if no cycle found after 100,000 iterations

4. **Cycle of length 1**: Grid becomes static (same state every minute)
   - Handled: (1,000,000,000 - cycle_start) % 1 = 0, returns state at cycle_start

5. **Target minute falls on cycle boundary**: Target = cycle_start + k × cycle_length
   - Handled: Modulo operation returns 0, giving state at cycle_start

## Expected Runtime

- **Cycle detection phase**: 1,000-10,000 iterations
- **Per iteration cost**: 2,500 cell evaluations + dict operations
- **Expected total time**: <1 second on modern hardware

## Implementation Notes

1. **Deep copy grids**: Use `[row[:] for row in grid]` when storing to avoid references
2. **Tuple conversion**: Must be consistent - same grid always produces same tuple
3. **Off-by-one errors**: Be careful with minute numbering (0-indexed vs 1-indexed)
4. **Modular arithmetic**: Ensure cycle_start is subtracted before applying modulo
