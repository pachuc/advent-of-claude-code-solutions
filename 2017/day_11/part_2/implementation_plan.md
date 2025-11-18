# Implementation Plan - Part 2: Maximum Distance During Journey

## Overview
Adapt the Part 1 solution to track the maximum distance from origin reached at any point during the hexagonal grid navigation, rather than just the final distance.

## Key Changes from Part 1
- Part 1 calculated distance only after all moves were complete
- Part 2 requires calculating distance after **each individual move** and tracking the maximum
- Core logic (cube coordinates, direction deltas, distance formula) remains identical

## Algorithm

### High-Level Approach
1. Parse the comma-separated input moves (reuse Part 1 parser)
2. Start at origin (0, 0, 0) in cube coordinates
3. **For each move in sequence:**
   - Apply the direction delta to current position
   - Calculate distance from origin to new position
   - Update maximum distance if current distance is greater
4. Return the maximum distance encountered

### Detailed Steps

#### Step 1: Reuse Part 1 Infrastructure
- **DIRECTION_DELTAS dictionary**: Identical to Part 1
  - Maps each direction ('n', 'ne', 'se', 's', 'sw', 'nw') to (dx, dy, dz) tuple
- **parse_input() function**: Can be reused without modification
  - Reads input.md file
  - Returns list of move strings
- **calculate_distance() function**: Can be reused without modification
  - Takes (x, y, z) cube coordinates
  - Returns (|x| + |y| + |z|) // 2

#### Step 2: Modify the Position Tracking Logic
Create a new function `find_max_distance(moves)` that:
1. Initialize position: `x, y, z = 0, 0, 0`
2. Initialize max_distance: `max_distance = 0`
3. Loop through each move:
   ```python
   for move in moves:
       # Input validation (same as Part 1)
       if move not in DIRECTION_DELTAS:
           raise ValueError(f"Invalid direction: '{move}'. Valid directions: n, ne, se, s, sw, nw")

       # Apply move
       dx, dy, dz = DIRECTION_DELTAS[move]
       x += dx
       y += dy
       z += dz

       # Calculate current distance from origin
       current_distance = calculate_distance(x, y, z)

       # Update maximum
       max_distance = max(max_distance, current_distance)
   ```
4. Return max_distance

**Note on Input Validation**: The `find_max_distance()` function must include the same input validation logic as Part 1's `calculate_final_position()`. This ensures invalid moves are caught during traversal.

#### Step 3: Update Main solve() Function
- Call parse_input() to get moves
- Call find_max_distance(moves) instead of calculate_final_position()
- Return the maximum distance

## Data Structures
- **Cube coordinates (x, y, z)**: Integers representing position with invariant x + y + z = 0
- **max_distance**: Integer tracking the furthest point reached
- **moves**: List of strings, each being a valid direction

## Time Complexity
- **O(n)** where n is the number of moves in the input
- Each move requires:
  - O(1) coordinate update
  - O(1) distance calculation
  - O(1) max comparison
- Single pass through the move list

## Space Complexity
- **O(n)** for storing the list of moves from input
- **O(1)** for position tracking variables and max_distance
- Could be optimized to O(1) total if we process moves in streaming fashion, but not necessary for this problem

## Edge Cases to Handle
1. **Empty input**: No moves → max_distance = 0 (already at origin)
2. **Single move**: max_distance should be 1 (one step from origin)
3. **Moves that return to origin**: max_distance could be anywhere along the path, not necessarily at the end
   - Example: "ne,ne,sw,sw" returns to origin but max_distance = 2 (after first two moves)
4. **Invalid moves**: Raise ValueError (same as Part 1)

## Example Trace
Input: `ne,ne,sw,sw`

| Step | Move | Position (x,y,z) | Distance | Max Distance |
|------|------|------------------|----------|--------------|
| 0    | -    | (0,0,0)          | 0        | 0            |
| 1    | ne   | (1,0,-1)         | 1        | 1            |
| 2    | ne   | (2,0,-2)         | 2        | 2            |
| 3    | sw   | (1,0,-1)         | 1        | 2            |
| 4    | sw   | (0,0,0)          | 0        | 2            |

Final answer: 2 (even though we end at origin)

## Implementation Structure

```
part_2_solution.py
│
├── DIRECTION_DELTAS (constant dict)
│
├── parse_input(filename='input.md')
│   └── Returns: List[str] of moves
│
├── calculate_distance(x, y, z)
│   └── Returns: int distance from origin
│
├── find_max_distance(moves)
│   ├── Initialize position (0, 0, 0)
│   ├── Initialize max_distance = 0
│   ├── For each move:
│   │   ├── Update position
│   │   ├── Calculate current distance
│   │   └── Update max_distance
│   └── Returns: int max_distance
│
└── solve()
    ├── Parse input
    ├── Call find_max_distance()
    └── Returns: int result
```

## Code Reuse Strategy
The Part 1 solution is well-structured and can be adapted efficiently:
- **Copy** `DIRECTION_DELTAS`, `parse_input()`, `calculate_distance()` unchanged
- **Refactor** the position tracking logic into `find_max_distance()` with max tracking
- **Simplify** solve() to call the new function

This minimizes code changes while clearly expressing the Part 2 logic.
