# Implementation Plan: Spiral Memory Stress Test (Part 2)

## Problem Summary
Generate a spiral grid where each square's value equals the sum of all adjacent (8 neighbors) filled squares. Find the first value that exceeds 289326.

## Key Differences from Part 1
- Part 1: Calculate coordinates for a given square number and find Manhattan distance
- Part 2: Traverse spiral in order, calculate adjacent sums, find first value > threshold
- **Reusable**: Spiral traversal logic (directions, ring structure)
- **New**: Need to store values in a grid and calculate neighbor sums

## Algorithm Overview
Use **iterative spiral generation** with a dictionary to store coordinate-value mappings. Generate values on-the-fly until threshold is exceeded.

**Time Complexity**: O(n) where n is the number of squares generated (expected ~50-100 for this input based on the example grid showing values like 806)
**Space Complexity**: O(n) to store the generated grid

## Step-by-Step Implementation Plan

### Step 1: Set Up Data Structures
- Create a dictionary `grid = {}` to map `(x, y)` coordinates to values
- Initialize starting position: `(0, 0)` with value `1`
- Set current position `(x, y) = (0, 0)`
- Read threshold value from `input.md` (289326)

### Step 2: Define Spiral Navigation Logic
Reuse the spiral pattern from Part 1 but adapt for iterative generation:
- Direction vectors: `RIGHT = (1, 0)`, `UP = (0, 1)`, `LEFT = (-1, 0)`, `DOWN = (0, -1)`
- Cycle through directions: RIGHT → UP → LEFT → DOWN
- Track steps in current direction before turning
- Pattern: 1 right, 1 up, 2 left, 2 down, 3 right, 3 up, 4 left, 4 down, ...
  - Steps increase every 2 direction changes
  - Formula: After each pair of turns, increment step count

Implementation approach:
```python
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # RIGHT, UP, LEFT, DOWN
dir_idx = 0
steps_in_direction = 1
steps_taken = 0
direction_changes = 0
```

### Step 3: Define Neighbor Sum Calculation
Create a function `get_neighbor_sum(x, y, grid)`:
- Define 8 neighbor offsets: `[(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]`
- For each offset `(dx, dy)`:
  - Check if `(x+dx, y+dy)` exists in `grid`
  - If yes, add its value to the sum
- Return total sum

**Edge case**: First square (0,0) has no neighbors, manually set to 1

### Step 4: Main Generation Loop

**Critical: Loop Initialization**
The first position (0,0) needs special handling to avoid off-by-one errors:
- Initialize grid with `{(0,0): 1}` BEFORE the loop
- Check if this first value exceeds threshold (edge case: threshold = 0)
- If not, start spiral movement from (0,0) to generate subsequent positions

```python
# Initialize first square
grid = {(0, 0): 1}
if 1 > threshold:
    return 1

# Initialize spiral state for movement starting FROM (0,0)
x, y = 0, 0
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # R, U, L, D
dir_idx = 0  # Start facing RIGHT
steps_in_direction = 1
steps_taken = 0
direction_changes = 0

# Main loop: generate positions 2, 3, 4, ...
while True:
    1. Move to next position in spiral
       - x += directions[dir_idx][0]
       - y += directions[dir_idx][1]
       - steps_taken += 1

    2. Update direction if needed (AFTER moving)
       - if steps_taken == steps_in_direction:
           - dir_idx = (dir_idx + 1) % 4
           - direction_changes += 1
           - steps_taken = 0
           - if direction_changes % 2 == 0:
               - steps_in_direction += 1

    3. Calculate value for current position
       - value = get_neighbor_sum(x, y, grid)

    4. Store in grid
       - grid[(x, y)] = value

    5. Check termination condition
       - if value > threshold:
           - return value
```

**Why this structure works**:
- Position (0,0) is handled before loop (special case: initial value 1)
- First loop iteration moves from (0,0) to (1,0), then calculates value for (1,0)
- Direction changes happen AFTER movement, ensuring correct position before value calculation
- No positions are skipped or double-processed

### Step 5: Spiral Movement Details - Worked Example

Track movement state:
- `steps_in_direction`: How many steps to take before turning (1, 1, 2, 2, 3, 3, ...)
- `steps_taken`: Steps taken in current direction
- `direction_changes`: Number of times we've changed direction

**Avoiding Off-by-One Errors**:
1. Always move FIRST, then check if turn is needed
2. Reset `steps_taken` to 0 AFTER turning, not before
3. Increment `steps_in_direction` every 2 direction changes (not every turn)
4. Direction sequence: R(0) → U(1) → L(2) → D(3) → R(0)...

Movement Logic:
```python
# Move one step in current direction
x += directions[dir_idx][0]
y += directions[dir_idx][1]
steps_taken += 1

# Check if we need to turn (AFTER moving)
if steps_taken == steps_in_direction:
    dir_idx = (dir_idx + 1) % 4  # Turn to next direction
    direction_changes += 1
    steps_taken = 0

    # Increase step count every 2 turns
    if direction_changes % 2 == 0:
        steps_in_direction += 1
```

**Detailed Trace of First 6 Iterations**:

Initial state (before loop):
- Grid: {(0,0): 1}
- Position: (0, 0)
- dir_idx: 0 (RIGHT), steps_in_direction: 1, steps_taken: 0, direction_changes: 0

**Iteration 1** (generating value for position 2):
- MOVE: (0,0) → (1,0) [moved RIGHT]
- steps_taken: 0 → 1
- Turn check: 1 == 1? YES → turn to UP (dir_idx=1), direction_changes=1, steps_taken=0
- Calculate: neighbors of (1,0) = {(0,0): 1} → sum = 1
- Store: grid[(1,0)] = 1
- Check: 1 > threshold? If yes, return 1

**Iteration 2** (generating value for position 3):
- MOVE: (1,0) → (1,1) [moved UP]
- steps_taken: 0 → 1
- Turn check: 1 == 1? YES → turn to LEFT (dir_idx=2), direction_changes=2, steps_taken=0
- Since direction_changes % 2 == 0: steps_in_direction: 1 → 2
- Calculate: neighbors of (1,1) = {(0,0): 1, (1,0): 1} → sum = 2
- Store: grid[(1,1)] = 2
- Check: 2 > threshold? If yes, return 2

**Iteration 3** (generating value for position 4):
- MOVE: (1,1) → (0,1) [moved LEFT]
- steps_taken: 0 → 1
- Turn check: 1 == 2? NO
- Calculate: neighbors of (0,1) = {(0,0): 1, (1,0): 1, (1,1): 2} → sum = 4
- Store: grid[(0,1)] = 4
- Check: 4 > threshold? If yes, return 4

**Iteration 4** (generating value for position 5):
- MOVE: (0,1) → (-1,1) [moved LEFT]
- steps_taken: 1 → 2
- Turn check: 2 == 2? YES → turn to DOWN (dir_idx=3), direction_changes=3, steps_taken=0
- Calculate: neighbors of (-1,1) = {(0,0): 1, (0,1): 4} → sum = 5
- Store: grid[(-1,1)] = 5
- Check: 5 > threshold? If yes, return 5

**Iteration 5** (generating value for position 6):
- MOVE: (-1,1) → (-1,0) [moved DOWN]
- steps_taken: 0 → 1
- Turn check: 1 == 2? NO
- Calculate: neighbors of (-1,0) = {(0,0): 1, (-1,1): 5, (0,1): 4} → sum = 10
- Store: grid[(-1,0)] = 10
- Check: 10 > threshold? If yes, return 10

**Iteration 6** (generating value for position 7):
- MOVE: (-1,0) → (-1,-1) [moved DOWN]
- steps_taken: 1 → 2
- Turn check: 2 == 2? YES → turn to RIGHT (dir_idx=0), direction_changes=4, steps_taken=0
- Since direction_changes % 2 == 0: steps_in_direction: 2 → 3
- Calculate: neighbors of (-1,-1) = {(0,0): 1, (-1,0): 10} → sum = 11
- Store: grid[(-1,-1)] = 11
- Check: 11 > threshold? If yes, return 11

This trace demonstrates:
- Correct spiral order: (0,0) → (1,0) → (1,1) → (0,1) → (-1,1) → (-1,0) → (-1,-1) → ...
- Pattern: 1R, 1U, 2L, 2D, 3R, 3U, ...
- Values: 1, 1, 2, 4, 5, 10, 11 (matches expected sequence)

### Step 6: Code Structure
```python
def get_neighbor_sum(x, y, grid):
    """Calculate sum of all adjacent cells that have been filled"""
    # Define 8 neighbor offsets
    # Sum values from grid for each neighbor that exists
    # Return total sum

def generate_spiral_values(threshold):
    """Generate spiral values until one exceeds threshold"""
    # Initialize grid with (0,0) -> 1
    # Check if 1 > threshold (edge case)
    # Initialize spiral movement state
    # Main loop as described in Step 4
    # Return first value > threshold

def main():
    # Read threshold from input.md
    # Call generate_spiral_values(threshold)
    # Print result

# Optional debug function:
def print_grid(grid, size=5):
    """Print grid in 2D format for visual debugging"""
    # Useful for verifying spiral pattern visually
```

### Step 7: Input/Output Handling
- Read input: `with open('input.md', 'r') as f: threshold = int(f.read().strip())`
- Output: `print(result)` where result is the first value exceeding threshold

## Implementation Notes

### Coordinate System
- Origin (0, 0) at center (square 1)
- +X is right, +Y is up
- Matches Part 1 coordinate system for consistency

### Starting Sequence Verification
Based on problem description, first few values should be:
- Position (0,0): 1 (initial value)
- Position (1,0): 1 (neighbors: {(0,0): 1} → sum = 1)
- Position (1,1): 2 (neighbors: {(0,0): 1, (1,0): 1} → sum = 2)
- Position (0,1): 4 (neighbors: {(0,0): 1, (1,0): 1, (1,1): 2} → sum = 4)
- Position (-1,1): 5 (neighbors: {(0,0): 1, (0,1): 4} → sum = 5)
- Position (-1,0): 10 (neighbors: {(0,0): 1, (-1,1): 5, (0,1): 4} → sum = 10)
- Position (-1,-1): 11 (neighbors: {(0,0): 1, (-1,0): 10} → sum = 11)

Use this to verify spiral traversal is correct. If these values don't match, there's likely an off-by-one error in the spiral movement logic.

### Efficiency Considerations
- Dictionary lookup is O(1) average case
- We only generate values until threshold is exceeded (early termination)
- No need to pre-calculate grid size
- Expected iterations: ~50-100 based on example grid showing 806

### No Code Reuse from Part 1
Part 1's `spiral_manhattan_distance` function calculates coordinates for a given square number using mathematical formulas. Part 2 needs iterative generation in spiral order. The approaches are fundamentally different, so we'll write new code rather than trying to adapt Part 1's mathematical approach.

However, we can reference Part 1's coordinate system and spiral direction pattern for consistency.
