# Test Plan: Air Duct Robot Pathfinding

## Testing Strategy
Verify the correctness of the solution through a combination of unit tests for individual components and integration tests for the complete solution.

## Test Cases

### Test 1: Example from Problem Statement
**Input**:
```
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
```

**Expected Output**: 14 steps

**Verification Steps**:
1. **Parse grid** and verify locations found: {0, 1, 2, 3, 4}
2. **Manually verify distances** by tracing paths on the grid:
   - Location positions: 0=(1,1), 1=(1,3), 2=(1,9), 3=(3,9), 4=(3,1)
   - 0 to 1: horizontal 2 steps → distance = 2
   - 0 to 2: horizontal 8 steps → distance = 8
   - 0 to 3: down 2, right 8 → distance = 10
   - 0 to 4: down 2 steps → distance = 2
   - 1 to 2: horizontal 6 steps → distance = 6
   - 1 to 3: need to go around wall, calculate via BFS → verify with implementation
   - 1 to 4: need to go around wall, calculate via BFS → verify with implementation
   - 2 to 3: down 2 steps → distance = 2
   - 2 to 4: need to go around wall, calculate via BFS → verify with implementation
   - 3 to 4: horizontal 8 steps → distance = 8
3. **Verify BFS calculates these distances correctly** - print distance matrix and compare
4. **Verify optimal path**: One possible path is 0→4→3→2→1:
   - 0→4: 2 steps
   - 4→3: 8 steps
   - 3→2: 2 steps
   - 2→1: 6 steps
   - Total: 2+8+2+6 = 18 steps (but this may not be optimal!)
   - Need to verify TSP finds the actual minimum of 14
5. Check that solution matches expected output of 14

**Purpose**: Validate against known correct answer

**NOTE**: The distances listed in original plan were not verified. During implementation, compare BFS results with manual calculations for validation.

### Test 2: Actual Input File
**Input**: Read from `input.md`

**Expected Output**: Unknown (to be calculated)

**Verification Steps**:
1. Parse grid successfully and identify all numbered locations
2. Verify all locations are reachable from location 0 (no infinity distances)
3. Run complete algorithm and get a reasonable answer
4. Manually verify a few distance calculations using BFS
5. Check that the result is positive and less than grid_size * num_locations (loose upper bound)

**Purpose**: Verify solution works on the actual problem input

### Test 3: Minimal Case - Only Starting Location
**Input**:
```
###
#0#
###
```

**Expected Output**: 0 steps

**Verification Steps**:
1. Parse should find only location 0
2. TSP should return 0 (no other locations to visit)

**Purpose**: Test edge case with minimum locations

### Test 4: Two Locations
**Input**:
```
#####
#0.1#
#####
```

**Expected Output**: 2 steps

**Verification Steps**:
1. Parse finds locations 0 and 1
2. BFS calculates distance from 0 to 1: 2 steps
3. TSP returns 2 (only one path: 0→1)

**Purpose**: Test simplest non-trivial case

### Test 5: Linear Path
**Input**:
```
#########
#0.1.2.3#
#########
```

**Expected Output**: 6 steps (0→1→2→3)

**Verification Steps**:
1. Verify distances: 0-1: 2, 1-2: 2, 2-3: 2
2. TSP should find optimal path going in order
3. Alternative paths should be longer or equal

**Purpose**: Test when optimal solution is obvious

### Test 6: Star Configuration
**Input**:
```
#######
#..1..#
#.203.#
#..4..#
#######
```

**Expected Output**: To be calculated during implementation

**Verification Steps**:
1. Parse and verify location 0 is at center: (2,3)
2. Verify distances from 0 to each other location:
   - 0 to 1: up 1, no obstruction → 1 step
   - 0 to 2: left 1 → 1 step
   - 0 to 3: right 1 → 1 step
   - 0 to 4: down 1 → 1 step
3. Verify distances between non-center locations (all should be 2 steps via center or direct)
4. Calculate expected minimum manually:
   - Must visit all 5 locations starting from 0
   - Since 0 is at center with distance 1 to all others
   - Optimal might be: 0→1→(center area)→2→3→4 or similar
   - Need to calculate actual minimum path
5. Compare TSP result with manual calculation

**Purpose**: Test symmetric configuration

**NOTE**: Expected output needs to be calculated manually before verifying implementation.

## Component Testing

### Test BFS Implementation
**Test Function**: `test_bfs_distances()`

**Test Cases**:
1. **Direct path**: Verify BFS finds shortest path in straight line
2. **Path with obstacles**: Verify BFS routes around walls correctly
3. **Multiple paths**: Verify BFS finds shortest among multiple valid paths
4. **Path through numbered location**: Verify that numbered locations are treated as passable
   ```
   #####
   #0.1.2#
   #####
   ```
   Distance from 0 to 2 should be 4 (can go through location 1)
5. **Distance matrix symmetry**: Verify distances[i][j] == distances[j][i] for all pairs

**Verification Method**:
- Create small custom grids with known distances
- Run BFS and compare actual vs expected distances
- Manually trace BFS execution for correctness
- Automated assertion: check symmetry of distance matrix

### Test TSP Implementation
**Test Function**: `test_tsp_solver()`

**Test Cases**:
1. **3 locations**: Distance matrix with known optimal tour
   ```
   Example:
   distances = [[0, 2, 5], [2, 0, 3], [5, 3, 0]]
   location_mapping = {0: 0, 1: 1, 2: 2}
   Paths starting from 0:
   - 0→1→2 = 2 + 3 = 5 ✓
   - 0→2→1 = 5 + 3 = 8
   Optimal: 5 steps
   ```
2. **4 locations**: More complex case to verify DP transitions
   ```
   Example:
   distances = [[0, 1, 2, 3],
                [1, 0, 4, 5],
                [2, 4, 0, 6],
                [3, 5, 6, 0]]
   location_mapping = {0: 0, 1: 1, 2: 2, 3: 3}
   Calculate optimal path manually and verify
   ```
3. **Non-consecutive location numbers**: Test with locations like {0, 2, 5, 7}
   - Verify normalization mapping works correctly
   - Verify TSP still produces correct result

**Verification Method**:
- Manually calculate optimal tour for each test case
- Compare with algorithm output
- Verify DP table values at key states (initial and final)
- For small cases (≤ 5 locations), can verify by checking all permutations

### Test Grid Parsing
**Test Function**: `test_parse_grid()`

**Test Cases**:
1. Verify all numbered locations are found
2. Verify coordinates are correct (row, col)
3. Verify locations 0-9 are handled if present
4. Verify grid with no locations returns empty dict

**Verification Method**:
- Create grids with locations at known positions
- Parse and verify returned dictionary matches expected

## Integration Testing

### End-to-End Test
**Process**:
1. Run complete solution on example input
2. Run complete solution on actual input
3. Verify outputs are reasonable numbers
4. Check execution completes in reasonable time (< 5 seconds)

### Performance Testing
**Test Cases**:
1. Measure execution time for example input (should be instant)
2. Measure execution time for actual input (should be < 5 seconds)
3. Verify no stack overflow or memory issues

## Debugging and Validation Strategies

### Distance Matrix Validation
- Print distance matrix after BFS calculation
- Verify symmetry (distance from A to B should equal B to A)
- Spot-check a few distances manually on the grid
- Verify no infinity values (all locations reachable)

### TSP Validation
- Print intermediate DP states for small examples
- Verify that starting state is initialized correctly
- Check that all locations are visited in final state
- Compare result with brute-force for small inputs (≤ 5 locations)

### Output Validation
- Ensure output is a single integer
- Verify output is positive and reasonable (not 0 unless trivial case, not astronomically large)
- For the actual input with 8 locations and a grid of ~43x175 cells:
  - Lower bound: direct distances would be at minimum ~50-100 steps (rough estimate)
  - Upper bound: visiting all 8 locations in worst case ~500-800 steps (rough estimate)
  - These are very rough estimates; actual answer will be determined by BFS distances

## Error Scenarios to Consider

For an Advent of Code script, extensive error handling is not required since inputs are guaranteed to be valid. However, basic assertions are helpful for debugging:

1. **No location 0**: Add assertion that location 0 exists (problem guarantees this)
2. **Disconnected locations**: Assert that all locations are reachable from each other (no infinite distances)
3. **Grid format issues**: Basic validation that grid is not empty

**Note**: Since AoC inputs are well-formed, we don't need extensive error handling for invalid formats, empty grids, etc.

## Manual Verification Steps

After running the solution:
1. **Verify distance matrix** (if debug output enabled):
   - Check a few distances by hand on the grid
   - Verify symmetry: distances[i][j] == distances[j][i]
   - Ensure no infinite values (all locations reachable)
2. **Path reconstruction** (if implemented):
   - Identify the path the algorithm found
   - Manually count steps on the grid for that path
   - Verify it sums to the reported answer
3. **Sanity check**:
   - For small examples, try alternative paths manually
   - Verify TSP result is not obviously wrong

## Success Criteria

The solution is considered correct if:

- ✓ Solution produces correct output for example case (14 steps)
- ✓ Solution produces a reasonable answer for actual input (verified by submitting to AoC)
- ✓ BFS correctly calculates shortest paths between all location pairs
  - Distance matrix is symmetric: distances[i][j] == distances[j][i]
  - No infinite distances (all locations reachable)
- ✓ TSP solver finds optimal tour starting from location 0
  - Verified on small test cases with known answers
- ✓ Execution completes in reasonable time (< 5 seconds for actual input)
- ✓ Location number normalization works correctly for non-consecutive location numbers
- ✓ Numbered locations are correctly treated as passable cells during pathfinding

## Test Execution Priority

Execute tests in this order:

1. **Test 4** (Two locations) - simplest verification
2. **Test 5** (Linear path) - obvious optimal path
3. **Test 3** (Single location) - edge case
4. **Test 1** (Example from problem) - MUST PASS with output = 14
5. **Component tests** (BFS, TSP, parsing) - if any issues found
6. **Test 2** (Actual input) - get the final answer
7. **Test 6** (Star config) - optional validation test

## Key Improvements from Critique

Based on the critique feedback, this revised test plan addresses:

1. **Test 1 distances are now marked for manual verification** - original distances were not validated
2. **Test 6 expected output changed to "TBD"** - needs manual calculation before use
3. **Added distance matrix symmetry test** - automated check for distances[i][j] == distances[j][i]
4. **Added test for paths through numbered locations** - verify locations are passable
5. **Added test for non-consecutive location numbers** - verify normalization works
6. **Improved output validation ranges** - more realistic bounds based on grid analysis
7. **Simplified error scenarios** - focused on relevant assertions for AoC context
8. **Added test execution priority** - clear order for incremental validation
