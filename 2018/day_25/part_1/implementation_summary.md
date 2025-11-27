# Implementation Summary: Four-Dimensional Constellation Grouping

## Problem Overview
The task was to count the number of distinct constellations formed by four-dimensional points in spacetime. Two points belong to the same constellation if they are connected either directly (Manhattan distance ≤ 3) or indirectly through a chain of intermediate points.

## Solution Approach

### Algorithm: Union-Find (Disjoint Set Union)
I implemented a Union-Find data structure with two key optimizations:
1. **Path Compression**: During find operations, flatten the tree structure by making nodes point directly to the root
2. **Union by Rank**: When merging sets, attach the smaller tree under the larger tree to keep depth minimal

### Implementation Steps
1. **Input Parsing**: Read and parse coordinates from the input file, handling empty lines and whitespace
2. **Union-Find Initialization**: Create parent and rank arrays for n points
3. **Manhattan Distance**: Calculate 4D Manhattan distance as the sum of absolute differences across all dimensions
4. **Build Constellations**: Compare all pairs of points (O(n²) comparisons) and union points within distance 3
5. **Count Components**: Count unique roots to determine the number of distinct constellations

### Time and Space Complexity
- **Time**: O(n² × α(n)) where α is the inverse Ackermann function (nearly constant)
- **Space**: O(n) for parent and rank arrays
- For n=1037 points: ~537,000 pairwise comparisons

## Files Created

### solution.py
Main implementation file containing:
- `solve(input_file)` - Main function that orchestrates the solution
- `find(x)` - Union-Find find operation with path compression
- `union(x, y)` - Union-Find union operation with union by rank
- `manhattan_distance(p1, p2)` - Calculates 4D Manhattan distance

## Testing Process

### Test Coverage
All tests passed successfully:

#### Provided Test Cases (4/4 passed)
1. **Test Case 1**: 8 points → 2 constellations ✓
2. **Test Case 2**: 10 points → 4 constellations ✓
3. **Test Case 3**: 10 points → 3 constellations ✓
4. **Test Case 4**: 10 points → 8 constellations ✓

#### Edge Cases (4/4 passed)
1. **Single point**: 1 → 1 constellation ✓
2. **Two connected points** (distance=3): 2 → 1 constellation ✓
3. **Two disconnected points** (distance=4): 2 → 2 constellations ✓
4. **Linear chain** (4 points): All connected through intermediate points → 1 constellation ✓

### Actual Input Results
- **Input size**: 1,037 four-dimensional points
- **Output**: 422 constellations
- **Execution time**: 0.372 seconds
- **Performance**: Well under the 1-second target

## Verification

### Algorithm Correctness
The Union-Find implementation was verified through:
- Transitive connectivity: Linear chain test confirmed points connect through intermediaries
- Boundary conditions: Distance=3 correctly connects, distance=4 correctly separates
- Negative coordinates: Test case 2 and 4 confirmed proper handling
- All dimensions contribute: Distance calculation verified across x, y, z, and w dimensions

### Code Quality
- Clean, readable implementation following the provided plan
- Proper handling of edge cases (empty input, single point, etc.)
- Efficient algorithms with appropriate optimizations
- Comments documenting key functions

## Key Insights

1. **Union-Find was the optimal choice**: The O(n²) pairwise comparison approach is acceptable for ~1000 points and simpler than building explicit adjacency lists
2. **Path compression is crucial**: Keeps find operations nearly constant time
3. **Manhattan distance threshold**: The ≤ 3 threshold (not < 3) is critical for correct connectivity
4. **Transitive closure**: The Union-Find automatically handles chains of connections without explicit DFS/BFS

## Final Answer
**422 constellations** found in the input data.
