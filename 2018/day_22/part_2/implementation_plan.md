# Implementation Plan: Cave Navigation with Tool Switching

## Overview
This is a shortest path problem with state-dependent constraints. We need to find the minimum time to navigate from `(0,0)` with torch to `(target_x, target_y)` with torch, considering equipment switching costs and region-specific equipment constraints.

## Algorithm Choice: Dijkstra's Algorithm

**Why Dijkstra over A*?**
- All edge weights are positive (1 or 7 minutes)
- The cave can extend beyond target coordinates for optimal paths
- Manhattan distance heuristic may not be admissible due to equipment switching constraints
- Dijkstra guarantees correctness without heuristic tuning

**State Space**: `(x, y, equipment)` where equipment ∈ {torch, climbing_gear, neither}

**Time Complexity**: O(V log V + E) where V = positions × 3 equipment states, E = transitions
**Space Complexity**: O(positions × 3) for visited states and distances

## Code Reuse from Part 1

We can directly reuse:
1. `parse_input()` - Input parsing logic
2. `calculate_erosion_level()` - Erosion calculation
3. `calculate_geologic_index()` - Geologic index calculation (with modifications)
4. Core cave generation logic

**Key Modification**: We need to generate a larger cave map beyond the target since optimal paths may detour.

## Step-by-Step Implementation Plan

### Step 1: Define Constants and Data Structures
**File**: solution.py (top of file)

```python
# Equipment types
TORCH = 0
CLIMBING_GEAR = 1
NEITHER = 2

# Region types
ROCKY = 0
WET = 1
NARROW = 2

# Equipment validity for each region type
# VALID_EQUIPMENT[region_type] = set of valid equipment
VALID_EQUIPMENT = {
    ROCKY: {TORCH, CLIMBING_GEAR},     # Can't use neither
    WET: {CLIMBING_GEAR, NEITHER},      # Can't use torch
    NARROW: {TORCH, NEITHER}            # Can't use climbing gear
}
```

**Rationale**: Using integers instead of strings for faster comparison in tight loops.

### Step 2: Reuse and Adapt Cave Generation from Part 1
**Functions to port**:
- `parse_input()` - No changes needed
- `calculate_erosion_level()` - No changes needed
- `calculate_geologic_index()` - Modify to work with larger bounds

**New function**: `build_cave_map(depth, target_x, target_y, margin)`

```python
def build_cave_map(depth, target_x, target_y, margin=50):
    """
    Build a cave map extending beyond target by margin.

    The map uses [y][x] indexing: cave_map[y][x] gives the region type at position (x, y).

    Returns:
        2D list where cave_map[y][x] = region_type (ROCKY/WET/NARROW) for position (x, y)
    """
```

**Key considerations**:
- **Margin size**: Start with margin=50. This is sufficient because:
  - The example (10,10) achieves optimal in 45 minutes with minimal detour
  - Detours are expensive (7 minutes per equipment switch)
  - A margin of 50 provides ample room for pathfinding without excessive memory
  - For target at (15, 740), this creates a map of size 66 × 791 ≈ 52K cells
  - If no path is found (unlikely), we can increase margin
- The margin allows paths that detour around difficult terrain
- We'll compute region types (erosion_level % 3) and store them
- **Important**: Use consistent [y][x] indexing throughout: cave_map[y][x] represents position (x, y)

**Algorithm**:
1. Determine map bounds: `max_x = target_x + margin`, `max_y = target_y + margin`
2. Initialize 2D array for erosion levels: `erosion_levels[y][x]` and `cave_map[y][x]`
3. Iterate y from 0 to max_y, x from 0 to max_x (row-major order for dependencies)
4. For each position:
   - Calculate geologic index using Part 1 logic
   - Calculate erosion level: `(geologic_index + depth) % 20183`
   - Store erosion level: `erosion_levels[y][x] = erosion_level`
   - Store region type: `cave_map[y][x] = erosion_level % 3`
5. Return cave_map (we don't need to keep erosion_levels after building)

### Step 3: Implement Valid Transition Checks
**Function**: `get_valid_equipment(region_type)`

```python
def get_valid_equipment(region_type):
    """Return set of valid equipment for a region type."""
    return VALID_EQUIPMENT[region_type]
```

**Function**: `can_move(current_equipment, destination_region_type)`

```python
def can_move(current_equipment, destination_region_type):
    """Check if current equipment is valid for destination."""
    return current_equipment in VALID_EQUIPMENT[destination_region_type]
```

### Step 4: Generate State Transitions
**Function**: `get_neighbors(state, cave_map, max_x, max_y)`

```python
def get_neighbors(state, cave_map, max_x, max_y):
    """
    Generate all valid transitions from current state.

    Args:
        state: (x, y, equipment) tuple
        cave_map: 2D array of region types
        max_x, max_y: Map boundaries

    Yields:
        (next_state, cost) tuples
    """
```

**Transitions to generate**:

1. **Equipment switches** (cost = 7):
   - Get current region type: `current_region = cave_map[y][x]`
   - From current position, switch to other valid equipment for current region
   - For each equipment in `VALID_EQUIPMENT[current_region] - {current_equipment}`:
     - Yield `((x, y, new_equipment), 7)`

2. **Movement** (cost = 1):
   - Try 4 directions: up (y-1), down (y+1), left (x-1), right (x+1)
   - For each direction:
     - Calculate new position (nx, ny)
     - Check bounds: `0 <= nx <= max_x and 0 <= ny <= max_y`
       - This prevents negative coordinates (solid rock boundary per problem)
     - Get destination region: `dest_region = cave_map[ny][nx]`
     - Check if current equipment valid for destination: `equipment in VALID_EQUIPMENT[dest_region]`
     - Yield `((nx, ny, equipment), 1)`

**Rationale**: Generate all valid transitions to avoid conditional logic in main loop.

### Step 5: Implement Dijkstra's Shortest Path
**Function**: `find_shortest_path(depth, target_x, target_y)`

```python
import heapq

def find_shortest_path(depth, target_x, target_y):
    """
    Find minimum time to reach target with torch equipped.

    Returns:
        int: Minimum time in minutes
    """
```

**Algorithm**:

1. **Initialize**:
   - Build cave map with margin: `cave_map = build_cave_map(depth, target_x, target_y, margin=50)`
   - Get map bounds: `max_x = target_x + margin`, `max_y = target_y + margin`
   - Priority queue: `[(0, (0, 0, TORCH))]` - (distance, state)
   - Distances dict: `{(0, 0, TORCH): 0}`
   - Visited set: `set()` - tracks (x, y, equipment) states, not just positions

2. **Main loop**:
   ```python
   while priority_queue:
       current_dist, current_state = heapq.heappop(pq)

       # Skip if already visited (allows same position with different equipment)
       if current_state in visited:
           continue

       visited.add(current_state)

       # Check if we reached goal
       x, y, equipment = current_state
       if x == target_x and y == target_y and equipment == TORCH:
           return current_dist

       # Explore neighbors
       for next_state, cost in get_neighbors(current_state, cave_map, max_x, max_y):
           if next_state in visited:
               continue

           new_dist = current_dist + cost

           # Relaxation step
           if next_state not in distances or new_dist < distances[next_state]:
               distances[next_state] = new_dist
               heapq.heappush(pq, (new_dist, next_state))

   # Should never reach here with valid input
   raise Exception("No path found to target - try increasing margin")
   ```

3. **Return**: Once we pop `(target_x, target_y, TORCH)`, return its distance

**Optimization considerations**:
- Use tuple states for hashability
- Use set for O(1) visited checks
- Priority queue ensures we process shortest paths first

### Step 6: Handle Edge Cases and Boundary Conditions

**Boundary expansion**:
- Initial margin=50 should be sufficient for typical inputs
- The exception in Step 5 will catch if no path found
- For debugging, could add margin expansion logic, but shouldn't be needed

**Negative coordinates** (from problem statement):
- Problem states: "Regions with negative X or Y coordinates are solid rock"
- Our bounds check `0 <= nx` and `0 <= ny` prevents entering these regions
- This is handled naturally in get_neighbors() bounds checking

**Starting state validation**:
- We start at (0, 0) with TORCH equipped
- Cave mouth is always ROCKY (geologic_index = 0, erosion = depth % 20183, type varies)
- TORCH is valid in ROCKY regions, so starting state is always valid

**Target state validation**:
- Target is always ROCKY (per problem statement)
- We must reach target with TORCH equipped
- TORCH is valid in ROCKY, so goal state is always reachable

### Step 7: Main Function
**Function**: `main()`

```python
def main():
    # Parse input
    depth, target_x, target_y = parse_input("input.md")

    # Find shortest path
    result = find_shortest_path(depth, target_x, target_y)

    # Print result
    print(result)
```

## Implementation Order

1. **Copy Part 1 base functions** (parse_input, calculate_erosion_level, calculate_geologic_index)
2. **Define constants** (equipment types, region types, validity mapping)
3. **Implement cave map building** with margin support
4. **Implement transition validation** functions
5. **Implement neighbor generation** function
6. **Implement Dijkstra's algorithm** for pathfinding
7. **Implement main** function
8. **Test with example** (depth=510, target=10,10, expected=45)

## Expected Runtime Analysis

**Input**: depth=3558, target=(15,740)

**Map size**: With margin=50, map is ~66 × 791 ≈ 52,200 cells
**State space**: 52,200 × 3 equipment = ~156,600 states
**Transitions**: Each state has up to 6 transitions (4 moves + 2 switches)

**Dijkstra complexity**: O(V log V + E) = O(157K log 157K + 940K) ≈ O(16M operations)

**Expected runtime**: < 3 seconds on modern hardware

**Memory**: ~157K states × (24 bytes per entry in dict) ≈ 4MB

Note: Reduced from margin=100 based on analysis that detours are unlikely to extend far from target.

## Potential Optimizations (if needed)

1. **A* with admissible heuristic**: Use Manhattan distance / 2 (underestimate accounting for switches)
2. **Reduce margin**: Start with smaller margin, increase if needed
3. **Lazy map generation**: Generate cave regions on-demand rather than pre-computing
4. **Bidirectional search**: Search from both start and goal simultaneously

However, these optimizations should NOT be needed for the given input size.

## Code Structure Summary

```
solution.py
├── Constants (TORCH, CLIMBING_GEAR, NEITHER, ROCKY, WET, NARROW, VALID_EQUIPMENT)
├── parse_input(filename)
├── calculate_erosion_level(geologic_index, depth)
├── calculate_geologic_index(x, y, target_x, target_y, erosion_levels)
├── build_cave_map(depth, target_x, target_y, margin)
├── get_neighbors(state, cave_map, max_x, max_y)
└── find_shortest_path(depth, target_x, target_y)
└── main()
```

Total LOC estimate: ~200 lines including comments and whitespace.
