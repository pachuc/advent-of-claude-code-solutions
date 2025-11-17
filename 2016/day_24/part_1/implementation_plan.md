# Implementation Plan: Air Duct Robot Pathfinding

## Problem Summary
Find the minimum number of steps for a robot to start at location `0` and visit all other numbered locations in a 2D grid with walls and passages. This is a Traveling Salesman Problem (TSP) variant.

## Algorithm Overview
1. **Parse the grid** to find all numbered locations and their coordinates
2. **Calculate pairwise distances** using BFS between all numbered locations
3. **Solve TSP** starting from location `0` using dynamic programming with bitmask
4. **Return minimum steps** required

## Detailed Implementation Steps

### Step 1: Parse the Input Grid
**Function**: `parse_grid(grid_lines)`

- **Input**: List of strings representing the grid
- **Output**: Dictionary mapping location numbers to (row, col) coordinates
- **Implementation**:
  - Iterate through each row and column of the grid
  - For each cell, check if it's a digit (0-9)
  - Store the digit and its coordinates in a dictionary
  - Example: `{0: (7, 142), 1: (20, 151), ...}`

### Step 2: Calculate Shortest Distances Between All Location Pairs
**Function**: `calculate_distances(grid, locations)`

- **Input**:
  - `grid`: 2D grid as list of strings
  - `locations`: Dictionary of location number to coordinates
- **Output**:
  - `distances`: 2D list of distances where `distances[i][j]` is the shortest distance between normalized location indices i and j
  - `location_mapping`: Dictionary mapping original location numbers to normalized indices (0 to N-1)
- **Implementation**:
  - **Create normalized mapping**:
    - Sort location numbers to ensure consistent ordering
    - Create mapping: `location_mapping = {loc_num: idx for idx, loc_num in enumerate(sorted(locations.keys()))}`
    - Create reverse mapping: `idx_to_loc = {idx: loc_num for loc_num, idx in location_mapping.items()}`
  - **Initialize distance matrix**:
    - `N = len(locations)`
    - `distances = [[float('inf')] * N for _ in range(N)]`
    - Set diagonal to 0: `distances[i][i] = 0` for all i
  - For each numbered location, run BFS to find shortest path to all other locations:
    - Get the normalized index for this location
    - **BFS Algorithm**:
      - Initialize queue with starting location coordinates and distance 0
      - Use a visited set to avoid revisiting cells
      - Explore 4 directions (up, down, left, right): `[(0,1), (0,-1), (1,0), (-1,0)]`
      - For each neighbor at (new_row, new_col):
        - Check bounds: `0 <= new_row < len(grid) and 0 <= new_col < len(grid[0])`
        - Check if passable: `grid[new_row][new_col] != '#'`
        - Check if not visited
        - If valid, add to queue with distance+1 and mark as visited
      - When encountering another numbered location, record the distance in the matrix
      - Continue until queue is empty
  - **Validation**:
    - Verify no infinite distances exist (all locations reachable from each other)
    - Verify symmetry: `distances[i][j] == distances[j][i]` for all i, j
  - Return both `distances` and `location_mapping`
  - **Complexity**: O(N * R * C) where N is number of locations, R*C is grid size

### Step 3: Solve TSP Using Dynamic Programming with Bitmask
**Function**: `solve_tsp(distances, location_mapping, start_location=0)`

- **Input**:
  - `distances`: 2D list indexed by normalized location indices [0 to N-1]
  - `location_mapping`: Dictionary mapping original location numbers to normalized indices
  - `start_location`: Original location number to start from (default 0)
- **Output**: Minimum number of steps to visit all locations starting from start_location
- **Implementation**:
  - **Location Number Normalization**:
    - Original location numbers may not be consecutive (e.g., 0, 1, 3, 5, 7)
    - Create mapping: `{original_num: index}` where index is 0 to (N-1)
    - Example: If locations are [0, 1, 3, 5, 7], mapping is {0:0, 1:1, 3:2, 5:3, 7:4}
    - This allows us to use a compact 2D list for distances and DP
  - Use dynamic programming with bitmask to represent visited locations
  - **State**: `dp[mask][current]` = minimum distance to reach normalized `current` index with visited set represented by `mask`
  - **Initialization**:
    - Get normalized start index: `start_idx = location_mapping[start_location]`
    - Create DP table: `dp = [[float('inf')] * N for _ in range(1 << N)]`
    - Set initial state: `dp[1 << start_idx][start_idx] = 0` (start at location 0 with only 0 visited)
    - All other states remain as `float('inf')`
  - **Transition**:
    - For each mask from 0 to (2^N - 1):
      - For each current location index that is set in mask:
        - If `dp[mask][current]` is infinity, skip
        - For each next location index not in mask:
          - Calculate `new_mask = mask | (1 << next)`
          - Update `dp[new_mask][next] = min(dp[new_mask][next], dp[mask][current] + distances[current][next])`
  - **Result**:
    - `full_mask = (1 << N) - 1` (all N locations visited)
    - Return `min(dp[full_mask][i])` for all normalized indices `i` (we can end at any location)
  - **Complexity**: O(2^N * N^2) where N is number of locations

### Step 4: Main Function
**Function**: `main()`

- **Steps**:
  1. **Read input**:
     - Read from `input.md` file
     - Strip any markdown formatting (code fences, etc.)
     - Handle potential trailing whitespace on lines
     - Store as list of strings (one per line)
  2. **Parse grid** to get location coordinates
     - Call `parse_grid(grid)` to get `locations` dictionary
     - Assert that location 0 exists: `assert 0 in locations, "Starting location 0 not found!"`
  3. **Calculate pairwise distances** using BFS
     - Call `calculate_distances(grid, locations)` to get `distances` matrix and `location_mapping`
     - Assert all locations reachable: check no `float('inf')` in distances (except diagonal initialization artifacts)
     - Optionally print distance matrix for debugging
  4. **Solve TSP** starting from location 0
     - Call `solve_tsp(distances, location_mapping, start_location=0)`
     - Get minimum number of steps
  5. **Print the result**:
     - Output single integer: the minimum number of steps
     - Optionally print the path taken (for verification)

## Data Structures

1. **Grid**: List of strings (each string is a row)
2. **Locations**: Dictionary `{location_number: (row, col)}` - original location numbers
3. **Location Mapping**: Dictionary `{original_location_number: normalized_index}` - maps locations to 0-(N-1)
4. **Distances**: 2D list `distances[i][j]` where i, j are normalized indices (0 to N-1)
5. **DP Table**: 2D list `dp[mask][normalized_idx]` where mask is an integer bitmask

## Time Complexity Analysis

- **Parsing**: O(R * C) - scan entire grid
- **BFS for all pairs**: O(N * R * C) where N is number of locations
- **TSP DP**: O(2^N * N^2)
- **Overall**: O(N * R * C + 2^N * N^2)

For the given input:
- Grid size: approximately 43 x 175 ≈ 7,525 cells
- Number of locations: 8 (0-7)
- BFS: 8 * 7,525 ≈ 60,200 operations
- TSP: 2^8 * 8^2 = 256 * 64 = 16,384 operations
- **Total is very manageable**

## Edge Cases to Handle

1. **Single location (only 0)**: Return 0 steps
2. **Two locations**: Direct distance from 0 to the other location
3. **Disconnected graph**: Not expected in valid inputs, but BFS will produce `float('inf')` distances - should assert this doesn't happen
4. **Multiple paths with same length**: Algorithm naturally finds minimum
5. **Non-consecutive location numbers**: Handled by normalization mapping (e.g., locations 0,1,3,5,7)
6. **Numbered locations as passable cells**: Treat them as open passages when pathfinding

## Implementation Notes

- Use `collections.deque` for efficient BFS queue operations
- Use bit manipulation for efficient mask operations
- Use 2D lists (not dictionaries) for distances and DP table for O(1) access
- **Always normalize location numbers to 0-indexed arrays** for DP - this is critical!
- Use `float('inf')` for unreachable states/distances
- Add optional debug output controlled by a flag to print:
  - Distance matrix
  - DP table (for small inputs)
  - Optimal path found (not just total distance)

## Validation and Debugging

- **Assert location 0 exists** in parsed locations
- **Assert all locations are reachable** (no infinite distances in final matrix)
- **Verify distance matrix symmetry** (distances[i][j] == distances[j][i])
- Print intermediate results when debugging:
  - Number of locations found
  - Distance matrix
  - Final result with path if tracking is implemented

## Key Improvements from Critique

Based on the critique feedback, this revised implementation plan clarifies:

1. **Explicit location number normalization strategy** - map original location numbers to 0-(N-1) indices
2. **Clear data structure choices** - use 2D lists (not dicts) for distances and DP for O(1) access
3. **Specified DP initialization** - use `float('inf')` for unreachable states, pre-allocate [2^N][N] table
4. **Input reading method specified** - read from `input.md` file with markdown stripping
5. **Added validation assertions** - location 0 exists, all reachable, matrix symmetric
6. **Debug output guidelines** - optional flags to print distance matrix, DP table, and path
7. **Clarified BFS passability** - numbered locations are treated as open passages
8. **Function signatures updated** - include location_mapping parameter for TSP function
