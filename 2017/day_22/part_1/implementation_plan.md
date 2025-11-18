# Implementation Plan: Sporifica Virus Simulation

## Problem Analysis

We need to simulate a virus carrier on an infinite 2D grid that:
- Turns left/right based on current node state (clean/infected)
- Toggles infection state of current node
- Moves forward one step
- Counts infections over 10,000 bursts

**Input:** 25x25 grid with initial infected nodes marked as `#`
**Output:** Count of new infections after 10,000 bursts

## Coordinate System

**We will use a screen coordinate system:**
- X-axis: increases to the right (0 to width-1)
- Y-axis: increases downward (0 to height-1)
- Origin (0, 0) is at top-left corner

Example for 3x3 grid:
```
    0 1 2  (x)
0   . . #
1   # . .
2   . . .
(y)
```
- Center position: (1, 1)
- UP means decreasing y: (0, -1)
- DOWN means increasing y: (0, 1)
- LEFT means decreasing x: (-1, 0)
- RIGHT means increasing x: (1, 0)

## Algorithm Efficiency Considerations

- **Grid representation**: Use a dictionary/set to store only infected nodes (sparse representation)
  - Rationale: Infinite grid + mostly clean nodes = O(1) lookups, minimal memory
  - Time complexity per burst: O(1) for lookups and updates
  - Space complexity: O(infected_nodes) instead of O(grid_size)

- **Total complexity**: O(10,000) = O(1) for fixed number of bursts
- **No optimization needed**: 10,000 iterations with O(1) operations is trivial even for Python

## Step-by-Step Implementation

### Step 1: Parse Input Grid
**File:** `solution.py`

```python
def parse_input(filename):
    """
    Read grid from file and return set of infected positions.

    Returns:
        - infected_nodes: set of (x, y) tuples for infected nodes
        - center: (x, y) tuple for starting position
    """
```

**Implementation details:**
- Read all lines from input file (note: file is named 'input.md', not .txt)
- Determine grid dimensions (should be 25x25)
- Calculate center position: (width // 2, height // 2)
- Iterate through grid, storing (x, y) coordinates where char == '#'
  - For row index r, column index c: position is (c, r)
  - This aligns with our coordinate system (x=column, y=row)
- Return: set of infected positions, center coordinates
- **Verification step:** For the 3x3 example, should find infected nodes at (2, 0) and (0, 1)

### Step 2: Define Direction System
**File:** `solution.py`

```python
# Direction constants (using screen coordinates: y increases downward)
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # UP, RIGHT, DOWN, LEFT
# UP=0, RIGHT=1, DOWN=2, LEFT=3 as indices
```

**Implementation details:**
- Store directions as list of (dx, dy) tuples
- UP = (0, -1) - moving up decreases y (moves toward row 0)
- RIGHT = (1, 0) - moving right increases x (moves toward higher columns)
- DOWN = (0, 1) - moving down increases y (moves toward higher rows)
- LEFT = (-1, 0) - moving left decreases x (moves toward column 0)
- Use index to track current direction (0-3)
- Turn left: `direction_idx = (direction_idx - 1) % 4`
  - Example: UP (0) → LEFT (3), LEFT (3) → DOWN (2)
- Turn right: `direction_idx = (direction_idx + 1) % 4`
  - Example: UP (0) → RIGHT (1), RIGHT (1) → DOWN (2)

### Step 3: Initialize Simulation State
**File:** `solution.py`

```python
def simulate_virus(infected_nodes, start_pos, num_bursts=10000):
    """
    Simulate virus carrier for specified number of bursts.

    Args:
        infected_nodes: set of (x, y) infected positions
        start_pos: (x, y) starting position
        num_bursts: number of bursts to simulate

    Returns:
        count of new infections
    """
```

**Implementation details:**
- Create a mutable copy of infected_nodes (convert to set if not already)
- Initialize position: `pos_x, pos_y = start_pos`
- Initialize direction: `direction_idx = 0` (facing UP)
- Initialize infection counter: `infection_count = 0`

### Step 4: Implement Burst Logic Loop
**Main simulation loop - the core algorithm:**

```python
for _ in range(num_bursts):
    # Step 1: Turn based on current node state
    if (pos_x, pos_y) in infected_nodes:
        # Turn RIGHT
        direction_idx = (direction_idx + 1) % 4
    else:
        # Turn LEFT
        direction_idx = (direction_idx - 1) % 4

    # Step 2: Toggle infection state
    if (pos_x, pos_y) in infected_nodes:
        # Clean the infected node
        infected_nodes.remove((pos_x, pos_y))
    else:
        # Infect the clean node
        infected_nodes.add((pos_x, pos_y))
        infection_count += 1

    # Step 3: Move forward
    dx, dy = DIRECTIONS[direction_idx]
    pos_x += dx
    pos_y += dy
```

**Implementation details:**
- Execute exactly 10,000 iterations
- Each burst must follow the exact order: turn, toggle, move
- Only increment counter when a node becomes infected (not when cleaned)
- Use set operations for O(1) add/remove/contains

### Step 5: Main Function
**File:** `solution.py`

```python
def main():
    """Main entry point for the solution."""
    # Optional: Debug flag for testing
    # DEBUG = False  # Set to True to enable debug prints

    # Parse input
    infected_nodes, center = parse_input('input.md')

    # Optional: Verify parsing for debugging
    # if DEBUG:
    #     print(f"Grid center: {center}")
    #     print(f"Initial infected nodes: {len(infected_nodes)}")

    # Run simulation
    result = simulate_virus(infected_nodes, center, 10000)

    # Print result
    print(result)
```

**Implementation details:**
- Read from 'input.md' file (markdown format, not .txt)
- Call simulation with 10,000 bursts
- Print single integer result to stdout
- Optional DEBUG flag can be used during testing to add verification prints
- For final submission, ensure DEBUG mode is off or debug code is removed

### Step 6: Script Entry Point
```python
if __name__ == '__main__':
    main()
```

## Implementation Checklist

1. [ ] Define direction constants (UP, RIGHT, DOWN, LEFT as tuples)
2. [ ] Implement `parse_input()` function
   - Read file lines
   - Calculate center position
   - Build set of infected coordinates
3. [ ] Implement `simulate_virus()` function
   - Initialize state variables
   - Implement burst loop with exact ordering:
     - Turn left/right based on current state
     - Toggle infection state and count
     - Move forward in current direction
4. [ ] Implement `main()` function
5. [ ] Add script entry point
6. [ ] Test with example input (should get 5587)

## Data Structures

- **infected_nodes**: `set` of `(x, y)` tuples
  - Fast O(1) membership testing
  - Fast O(1) add/remove operations

- **position**: `(pos_x, pos_y)` tuple or separate variables

- **direction**: integer index (0-3) into DIRECTIONS list

## Edge Cases to Handle

- Grid boundaries: None (infinite grid, handled by sparse representation)
  - Carrier can move to negative coordinates or far beyond initial 25x25 grid
  - Set-based representation naturally handles this
- Starting position on infected node: Follow normal rules
  - Turn right, clean it, move forward
- Revisiting same node: Normal behavior, toggle state again
  - Can visit same node multiple times with different states
- Coordinate alignment: Verify parsing matches expected positions
  - For 3x3 example: infected at (2, 0) and (0, 1), center at (1, 1)

## Performance Expectations

- Runtime: < 1 second for 10,000 bursts
- Memory: Minimal, proportional to infected nodes count (likely < 10,000 nodes)
