# Problem Report: Cave Navigation with Tool Switching

## Objective
Find the minimum time (in minutes) to navigate from the cave entrance to the target location, accounting for movement time and tool-switching constraints.

## Context from Part 1
In Part 1, we calculated the risk level for a cave system by determining the type of each region (rocky, wet, or narrow) based on geologic and erosion calculations. We established:

- Each region has a **type** determined by its erosion level modulo 3:
  - `erosion_level % 3 = 0`: **rocky**
  - `erosion_level % 3 = 1`: **wet**
  - `erosion_level % 3 = 2`: **narrow**

- **Erosion level calculation**: `(geologic_index + depth) % 20183`

- **Geologic index rules** (first applicable):
  1. Region at `0,0` (cave mouth): `0`
  2. Region at target coordinates: `0`
  3. If `Y = 0`: `X * 16807`
  4. If `X = 0`: `Y * 48271`
  5. Otherwise: `erosion_level(X-1, Y) * erosion_level(X, Y-1)`

Part 1 answer: **11810** (total risk for the rectangular region from `0,0` to target)

## Part 2: Navigation Problem

### Starting Conditions
- **Start position**: `0,0` (cave mouth)
- **Start equipment**: Torch equipped
- **Goal**: Reach target coordinates with torch equipped

### Equipment and Region Constraints
You have access to three equipment states: **torch**, **climbing gear**, or **neither**.

Equipment restrictions by region type:
- **Rocky regions**: Can use climbing gear OR torch (NOT neither)
- **Wet regions**: Can use climbing gear OR neither (NOT torch)
- **Narrow regions**: Can use torch OR neither (NOT climbing gear)

### Actions and Time Costs

1. **Move to adjacent region** (up, down, left, right - no diagonals):
   - Cost: **1 minute**
   - Constraint: Current equipment must be valid for the destination region

2. **Switch equipment**:
   - Cost: **7 minutes**
   - Constraint: New equipment must be valid for current region
   - Can switch between any two valid equipment options for the current region

### Important Rules
- The target is always in a **rocky** region
- You must have the **torch equipped** when you reach the target
- Regions with negative X or Y coordinates are solid rock (cannot be traversed)
- The optimal path may extend beyond the target's X or Y coordinates
- You need to explore regions beyond the target boundary to find the fastest route

## Input Specification
Same as Part 1:
```
depth: <integer>
target: <X>,<Y>
```

Example:
```
depth: 3558
target: 15,740
```

## Output Specification
A single integer representing the minimum number of minutes required to reach the target with the torch equipped.

## Example
Given:
- depth = 510
- target = 10,10

The minimum time to reach the target is **45 minutes**:
- 21 minutes switching tools (3 switches × 7 minutes each)
- 24 minutes moving (24 moves × 1 minute each)

## Algorithm Approach
This is a **shortest path problem** with state-dependent movement costs. Recommended approach:

1. **Build the cave map** using Part 1's algorithm (may need to extend beyond target coordinates)
2. **Model the state space** as `(x, y, equipment)` tuples
3. **Use Dijkstra's algorithm or A*** to find the shortest path from `(0, 0, torch)` to `(target_x, target_y, torch)`
4. **Edge weights**:
   - Moving to adjacent cell with same equipment: 1 minute
   - Switching equipment at same position: 7 minutes
5. **Validate transitions**: Ensure equipment is valid for both current and destination regions

## Important Notes
- The cave extends infinitely, so you must determine an appropriate search boundary
- Consider that the optimal path might go around difficult terrain
- The state space is 3x larger than just positions (due to equipment states)
- The target must be reached specifically with the torch, not just any valid equipment
