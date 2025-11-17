# Implementation Plan: Grid Computing Part 2 - Minimum Steps to Access Goal Data

## Problem Analysis

This is a **sliding puzzle problem** where we need to move goal data from position (max_x, 0) to (0, 0). This is similar to the classic 15-puzzle sliding tile game, where we need to move the goal data by shuffling it with an empty space while navigating around immovable wall nodes.

**Key Problem Characteristics:**
- Grid is arranged in a 2D coordinate system with (x, y) positions
- Goal starts at top-right corner (max_x, 0) and must reach top-left (0, 0)
- Exactly one empty node exists (Used = 0T) which acts as the "gap" for shuffling
- Wall nodes have data too large to move (typically 400-500T vs 90T normal capacity)
- Data can only move between adjacent nodes (up/down/left/right)
- Movement is valid only if destination has enough capacity

## Algorithm Choice: BFS State-Space Search

We'll use **BFS state-space search** to guarantee finding the minimum number of steps. This is the most reliable approach for sliding puzzle problems where we need an optimal solution.

**Why BFS over alternatives:**
- Guarantees optimal (minimum) solution
- Handles arbitrary wall configurations robustly
- Straightforward to implement and verify
- Performance is acceptable for the grid size (~1,000 nodes)

### State Representation
- **State**: `(goal_x, goal_y, empty_x, empty_y)` - tracks both goal and empty positions
- **Initial state**: `(34, 0, 8, 28)`
- **Target state**: `(0, 0, *, *)` - goal at origin, empty can be anywhere
- **State space size**: 35 × 29 × 35 × 29 ≈ 1 million possible states

### Key Movement Insight
When we move data FROM an adjacent node INTO the empty node:
- The adjacent node becomes the new empty position
- The old empty node is now filled with that data
- If the adjacent node was the goal, the goal position changes
- This is how we "move" the goal data across the grid

## Implementation Steps

### Step 1: Parse Input and Build Grid Structure
**File**: `solution.py`

**Function**: `parse_input(input_text) -> tuple`

Extend the Part 1 parsing logic to extract full grid structure AND pre-compute wall positions:

```python
import re

def parse_input(input_text):
    """
    Parse df output to extract complete grid structure.

    Returns:
        tuple: (nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions)
        - nodes_dict: {(x, y): {'size': int, 'used': int, 'avail': int}}
        - max_x, max_y: Grid dimensions (maximum coordinates)
        - empty_pos: (x, y) tuple of empty node
        - goal_pos: (x, y) tuple of goal node (max_x, 0)
        - wall_positions: set of (x, y) positions that cannot be moved
    """
```

**Implementation Details**:

1. **Reuse Part 1 structure**: Skip first 2 header lines, split lines into parts
2. **Extract coordinates** from filesystem path `/dev/grid/node-x{X}-y{Y}`:
   ```python
   # Parse: /dev/grid/node-x8-y28
   parts = line.split()
   filesystem = parts[0]  # "/dev/grid/node-x8-y28"

   # Extract coordinates with error handling
   match = re.search(r'x(\d+)-y(\d+)', filesystem)
   if not match:
       continue  # Skip malformed lines
   x = int(match.group(1))
   y = int(match.group(2))
   ```
3. **Extract data values** (reuse Part 1 logic):
   ```python
   size = int(parts[1][:-1])   # Remove 'T' suffix from "92T"
   used = int(parts[2][:-1])   # Remove 'T' suffix
   avail = int(parts[3][:-1])  # Remove 'T' suffix
   ```
4. **Build dictionary** keyed by (x, y) coordinates
5. **Track max_x and max_y** during parsing
6. **Find empty node** where used == 0
7. **Goal position** is (max_x, 0)
8. **Pre-compute wall positions**: After parsing, identify all nodes whose data is too large to move into the empty space

**Complete Validation** (added after critique):
```python
# Validate parsing results
empty_count = sum(1 for node in nodes_dict.values() if node['used'] == 0)
assert empty_count == 1, f"Expected 1 empty node, found {empty_count}"
assert len(nodes_dict) > 0, "Grid is empty"
assert empty_pos is not None, "No empty node found"
assert empty_pos in nodes_dict, "Empty position not in grid"
assert goal_pos in nodes_dict, "Goal position not in grid"

# Critical: Verify goal can actually be moved
empty_capacity = nodes_dict[empty_pos]['size']
goal_used = nodes_dict[goal_pos]['used']
assert goal_used <= empty_capacity, \
    f"Goal node cannot be moved! Goal has {goal_used}T but empty capacity is {empty_capacity}T"
```

**Pre-compute Walls** (optimization from critique):
```python
# After parsing, pre-compute which nodes are walls
# A wall is any node whose data is too large to fit in the empty space
empty_capacity = nodes_dict[empty_pos]['size']
wall_positions = {
    pos for pos, node in nodes_dict.items()
    if node['used'] > empty_capacity
}
```

This pre-computation avoids checking wall status inside the BFS loop, improving both performance and code clarity.

### Step 2: BFS State-Space Search Setup

Wall nodes are now pre-computed in Step 1 as `wall_positions` set, which will be passed to the BFS function. This provides:
- O(1) wall checking during BFS (set lookup vs dictionary access + comparison)
- Clear separation of concerns (parsing identifies walls, BFS uses them)
- Better code organization and testability

### Step 3: Implement BFS State-Space Search

**Function**: `find_minimum_steps(grid, max_x, max_y, wall_positions, initial_goal_pos, initial_empty_pos, target_pos) -> int`

This is the core algorithm that finds the minimum steps.

```python
from collections import deque

def find_minimum_steps(grid, max_x, max_y, wall_positions, initial_goal_pos, initial_empty_pos, target_pos):
    """
    Use BFS to find minimum steps to move goal to target.

    Args:
        grid: Dictionary {(x, y): {'size': int, 'used': int, 'avail': int}}
        max_x, max_y: Grid boundaries (maximum coordinates)
        wall_positions: Set of (x, y) positions that cannot be moved
        initial_goal_pos: Starting position of goal data (x, y)
        initial_empty_pos: Starting position of empty node (x, y)
        target_pos: Target position for goal data (x, y)

    Returns:
        int: Minimum number of steps, or None if no solution exists
    """
    # State: (goal_x, goal_y, empty_x, empty_y)
    initial_state = (initial_goal_pos[0], initial_goal_pos[1],
                     initial_empty_pos[0], initial_empty_pos[1])

    # Check if already at target
    if initial_goal_pos == target_pos:
        return 0

    # BFS initialization
    queue = deque([(initial_state, 0)])  # (state, steps)
    visited = {initial_state}

    while queue:
        state, steps = queue.popleft()
        goal_x, goal_y, empty_x, empty_y = state

        # Check if goal reached target
        if (goal_x, goal_y) == target_pos:
            return steps

        # Try moving data from each adjacent node into empty position
        # Directions: up, down, left, right
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # Calculate adjacent position
            adj_x = empty_x + dx
            adj_y = empty_y + dy

            # Check grid boundaries
            if not (0 <= adj_x <= max_x and 0 <= adj_y <= max_y):
                continue

            # Check if position exists in grid
            if (adj_x, adj_y) not in grid:
                continue

            # Check if this is a wall (pre-computed, O(1) set lookup)
            if (adj_x, adj_y) in wall_positions:
                continue  # Cannot move wall nodes

            # Create new state after moving data from adjacent into empty
            new_empty_x, new_empty_y = adj_x, adj_y

            # If we moved the goal, update goal position
            if (adj_x, adj_y) == (goal_x, goal_y):
                new_goal_x, new_goal_y = empty_x, empty_y
            else:
                new_goal_x, new_goal_y = goal_x, goal_y

            new_state = (new_goal_x, new_goal_y, new_empty_x, new_empty_y)

            # Add to queue if not visited
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, steps + 1))

    # No solution found - return None for clearer error handling
    return None
```

**Algorithm Explanation**:

1. **State representation**: Each state tracks where the goal and empty are
2. **Transitions**: From each state, try moving data from adjacent nodes into empty
3. **Move validation**: Check bounds, existence, and size constraints
4. **Goal tracking**: When we move the goal node, update goal position in state
5. **Termination**: When goal reaches (0, 0), return step count

### Step 4: Main Function

```python
def main():
    """Main entry point."""
    # Read input file
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input (now includes wall positions)
    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    # Target is (0, 0)
    target_pos = (0, 0)

    # Find minimum steps using BFS
    result = find_minimum_steps(
        nodes_dict, max_x, max_y, wall_positions, goal_pos, empty_pos, target_pos
    )

    # Handle result (improved error handling from critique)
    if result is None:
        print("Error: No solution found!", file=sys.stderr)
        sys.exit(1)

    # Print result
    print(result)

if __name__ == "__main__":
    main()
```

## Code Structure Summary

```python
import re
import sys
from collections import deque

def parse_input(input_text):
    """Parse df output and extract grid information with wall pre-computation."""
    nodes_dict = {}
    max_x = max_y = 0
    empty_pos = None

    lines = input_text.strip().split('\n')

    # Skip first 2 header lines
    for line in lines[2:]:
        # Parse each node with error handling
        # Extract coordinates and data
        # Build dictionary
        # Track max coordinates and empty position
        pass

    # Compute goal position
    goal_pos = (max_x, 0)

    # Pre-compute wall positions (optimization from critique)
    empty_capacity = nodes_dict[empty_pos]['size']
    wall_positions = {
        pos for pos, node in nodes_dict.items()
        if node['used'] > empty_capacity
    }

    # Comprehensive validation (from critique)
    # ... assertions here ...

    return nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions

def find_minimum_steps(grid, max_x, max_y, wall_positions, goal_pos, empty_pos, target_pos):
    """Use BFS to find minimum steps to move goal to target."""
    # BFS state-space search with pre-computed walls
    # Returns int (steps) or None (no solution)
    pass

def main():
    """Main entry point."""
    # Read, parse, solve, handle errors, print
    pass

if __name__ == "__main__":
    main()
```

## Optimization Considerations

### Memory Efficiency
- **State space**: ~1 million possible states maximum
- **Actual explored**: Likely 10,000-50,000 states due to walls and constraints
- **Memory per state**: 4 integers (16-32 bytes) + set overhead
- **Total memory**: ~1-2 MB for visited set - very manageable

### Time Complexity
- **BFS complexity**: O(V + E) where V = states, E = transitions
- **States explored**: 10,000-50,000 (estimated)
- **Transitions per state**: 4 (up, down, left, right)
- **Total operations**: ~40,000-200,000
- **Expected runtime**: 1-5 seconds in Python

### Alternative Approaches (Not Implemented)

**Pattern-Based Calculation**:
- Use BFS to move empty to (goal_x-1, 0)
- Then apply formula: `steps = bfs_distance + (goal_x - 2) * 5 + 2`
- This is faster but less general
- Works because goal travels in a straight line along y=0

**A* Search**:
- Use Manhattan distance as heuristic: `h = |goal_x - 0| + |goal_y - 0|`
- Would explore fewer states but adds priority queue overhead
- BFS is simpler and fast enough for this problem size

## Expected Behavior

Based on the grid analysis:
- The BFS will navigate the empty node around the wall at y=22
- Once the empty reaches the top row, it will shuffle with the goal
- The minimum path involves moving the empty north around the wall, then positioning it near the goal
- Expected result: 200-250 steps (estimated)

## Edge Cases Handled

1. **Wall nodes**: Pre-computed in parsing as `wall_positions` set, checked via O(1) set lookup
2. **Grid boundaries**: Explicit bounds checking: `0 <= x <= max_x and 0 <= y <= max_y`
3. **Non-existent nodes**: Check `if (x, y) not in grid` before accessing
4. **State cycles**: Tracked via `visited` set to prevent revisiting states
5. **Goal already at target**: Checked at start of BFS (returns 0 immediately)
6. **No solution**: Returns `None` if BFS exhausts without finding target, main() handles error
7. **Malformed input lines**: Regex match checked for `None` before use
8. **No empty node**: Validation assertion ensures exactly one empty node exists
9. **Goal is a wall**: Validation assertion ensures goal's data fits in empty capacity
10. **Empty position invalid**: Validation assertion ensures empty position is in grid

## Testing Strategy

Detailed testing will be in `test_plan.md`, but key validation points:

1. **Parse validation**: Verify grid dimensions, empty node, goal position
2. **Wall identification**: Check wall positions are correctly identified
3. **Input validation**: Ensure all assertions pass (goal is movable, empty exists, etc.)
4. **BFS correctness**: Ensure result is positive integer or None
5. **Part 1 compatibility**: Verify extended parser can still compute Part 1 answer (981)
6. **Performance**: Should complete in reasonable time (< 60 seconds)

## Connection to Part 1

The Part 1 solution provides:
- Proven parsing logic for df output
- Correct handling of 'T' suffix removal
- Line-skipping logic for headers

We extend this by:
- Adding coordinate extraction
- Building a full grid dictionary instead of just (used, avail) pairs
- Tracking positions and dimensions
