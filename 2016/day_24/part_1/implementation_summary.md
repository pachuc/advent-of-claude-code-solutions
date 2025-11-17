# Implementation Summary: Air Duct Robot Pathfinding

## Problem Overview
The task was to solve a variant of the Traveling Salesman Problem (TSP) where a robot must start at location `0` and visit all other numbered locations in a 2D grid maze in the minimum number of steps.

## Solution Approach

### Algorithm Components

1. **Grid Parsing** (`parse_grid` function)
   - Scans the entire grid to identify all numbered locations (0-9)
   - Stores each location's coordinates as (row, col)
   - Returns a dictionary mapping location numbers to coordinates

2. **Distance Calculation** (`calculate_distances` function)
   - Uses Breadth-First Search (BFS) to find shortest paths between all pairs of numbered locations
   - Creates a normalized location mapping to convert potentially non-consecutive location numbers to 0-indexed array indices
   - Builds a symmetric distance matrix where `distances[i][j]` represents the shortest path between locations i and j
   - BFS treats numbered locations as passable cells (not walls)

3. **TSP Solver** (`solve_tsp` function)
   - Implements dynamic programming with bitmask to solve the TSP
   - State: `dp[mask][current]` = minimum distance to reach location `current` with visited set represented by `mask`
   - Initialization: Starts at location 0 with only that location visited
   - Transitions: For each state, tries moving to unvisited locations
   - Result: Finds minimum among all ending positions when all locations are visited

4. **Main Function**
   - Reads input from `input.md`
   - Orchestrates the parsing, distance calculation, and TSP solving
   - Outputs the minimum number of steps required

## Files Created

1. **solution.py** - Main solution file containing:
   - `parse_grid()` - Grid parser
   - `calculate_distances()` - BFS-based distance calculator
   - `solve_tsp()` - Dynamic programming TSP solver
   - `main()` - Entry point that orchestrates the solution

2. **test_solution.py** - Test suite containing:
   - `test_two_locations()` - Simple test with 2 locations
   - `test_linear_path()` - Test with locations in a straight line
   - `test_example()` - Test with the example from the problem statement

3. **test_example.txt** - Example input for manual testing

4. **implementation_summary.md** - This file

## Testing Process

### Unit Tests
All tests passed successfully:

1. **Two Locations Test**
   - Grid: `#0.1#`
   - Expected: 2 steps
   - Result: ✓ PASSED (2 steps)

2. **Linear Path Test**
   - Grid: `#0.1.2.3#`
   - Expected: 6 steps (0→1→2→3)
   - Result: ✓ PASSED (6 steps)

3. **Example Test** (from problem statement)
   - Grid: 5x11 grid with locations 0, 1, 2, 3, 4
   - Expected: 14 steps
   - Result: ✓ PASSED (14 steps)

   Distance matrix verified:
   ```
        0   1   2   3   4
    0:  0   2   8  10   2
    1:  2   0   6   8   4
    2:  8   6   0   2  10
    3: 10   8   2   0   8
    4:  2   4  10   8   0
   ```

### Actual Input Test
- Grid size: 43 x 175 cells
- Locations found: 8 (numbered 0-7)
- **Result: 428 steps**

Distance matrix for actual input:
```
     0   1   2   3   4   5   6   7
 0:  0  30  76  40 242 252 260 214
 1: 30   0  58  30 224 234 242 196
 2: 76  58   0  72 178 188 192 150
 3: 40  30  72   0 238 248 256 210
 4: 242 224 178 238  0  26  66  48
 5: 252 234 188 248 26   0  76  62
 6: 260 242 192 256 66  76   0  82
 7: 214 196 150 210 48  62  82   0
```

### Validation Checks
- ✓ Distance matrix is symmetric (distances[i][j] == distances[j][i])
- ✓ All locations are reachable from each other (no infinite distances)
- ✓ Location 0 exists in the input
- ✓ Execution completed in < 1 second

## Key Implementation Details

1. **Location Normalization**: The implementation correctly handles non-consecutive location numbers by creating a mapping from original location numbers to 0-indexed array positions. This ensures efficient array-based DP computation.

2. **BFS Implementation**: The BFS correctly treats numbered locations as passable cells, allowing paths to go through other numbered locations.

3. **DP Optimization**: The dynamic programming solution uses bitmasks to efficiently represent which locations have been visited, with time complexity O(2^N * N^2) where N is the number of locations.

4. **Distance Matrix Symmetry**: The implementation verifies that the distance matrix is symmetric, confirming correct BFS implementation.

## Complexity Analysis

- **Grid Parsing**: O(R * C) where R = rows, C = columns
- **Distance Calculation**: O(N * R * C) for N locations
- **TSP Solver**: O(2^N * N^2)
- **Overall**: O(N * R * C + 2^N * N^2)

For the actual input:
- Grid: ~43 x 175 ≈ 7,525 cells
- Locations: 8
- BFS operations: 8 * 7,525 ≈ 60,200
- DP operations: 2^8 * 64 = 16,384
- Total: Very fast execution (< 1 second)

## Conclusion

The solution successfully solves the air duct robot pathfinding problem using a combination of BFS for pairwise distances and dynamic programming for the TSP variant. All tests passed, including the critical example test that verified the expected output of 14 steps. The actual input was solved to find the minimum path of **428 steps** to visit all 8 locations starting from location 0.
