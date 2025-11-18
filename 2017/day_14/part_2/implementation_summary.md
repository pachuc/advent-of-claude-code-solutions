# Implementation Summary: Disk Defragmentation - Region Counting (Part 2)

## Overview
Successfully implemented a solution to count distinct regions in a 128x128 grid representing disk usage. A region is defined as a group of orthogonally-adjacent "used" squares (1 bits).

## Solution Approach

### Algorithm: Connected Components with BFS
The solution uses a classic graph traversal approach to identify connected components in the grid:

1. **Grid Generation** (Reused from Part 1):
   - Generate 128x128 binary grid using knot hash algorithm
   - Each row is computed from `{key}-{row_number}`
   - Each knot hash produces 128 bits representing one row

2. **Region Counting** (New for Part 2):
   - Iterate through every cell in the grid
   - When finding an unvisited "used" cell (1 bit), increment region counter
   - Perform flood fill (BFS) to mark all connected cells as visited
   - Continue until all cells are processed

### Key Implementation Details

#### Flood Fill (BFS)
```python
def flood_fill_bfs(grid, start_row, start_col, visited):
    # Uses BFS to mark all orthogonally-connected cells
    # Only checks 4 directions: up, down, left, right (no diagonals)
```

**Why BFS over DFS:**
- BFS uses an explicit queue, avoiding potential stack overflow issues
- Python's default recursion limit (~1000) could be exceeded with recursive DFS on large regions
- More predictable performance for large grids

#### Region Counting
```python
def count_regions(grid):
    # Scans grid and counts distinct connected components
    # Uses visited set to ensure each region counted exactly once
```

**Key Features:**
- O(n) time complexity where n is grid size (128 × 128 = 16,384 cells)
- Each cell visited exactly once
- Space complexity O(n) for visited set

## Files Created

### solution.py
Main implementation file containing:
- **Knot Hash Functions** (copied from Part 1): All hash computation logic
- **Grid Generation** (from Part 1): `generate_grid()`, `hex_to_binary()`, etc.
- **Region Counting** (new): `flood_fill_bfs()`, `count_regions()`, `solve_part2()`
- **Test Functions**: Unit tests and integration tests
- **Main Execution**: Runs tests and computes final answer

Total lines: ~390 lines (includes comprehensive tests)

## Testing Process

### Unit Tests
All unit tests passed successfully:

1. **Flood Fill Tests**:
   - ✓ Single isolated cell
   - ✓ No diagonal connections (critical - ensures correct adjacency)
   - Verified BFS correctly identifies orthogonally-connected regions

2. **Region Counting Tests**:
   - ✓ Empty grid (0 regions)
   - ✓ Full grid (1 region - all connected)
   - ✓ Multiple distinct regions (4 regions)

3. **Grid Generation Validation**:
   - Verified grid consistency with Part 1 (8140 used squares for 'jxqlasbh')
   - Grid generation reused Part 1 code directly - no modifications needed

### Integration Tests

1. **Example Key Test (Critical Validation)**:
   - Input: `flqrgnkx`
   - Expected: 1242 regions
   - **Result: 1242 regions ✓**
   - This confirms the algorithm is correct

2. **Actual Input Test**:
   - Input: `jxqlasbh`
   - **Result: 1182 regions ✓**
   - Sanity checks passed (1 ≤ result ≤ 8140)

### Test Results Summary
```
Running tests...

Unit tests:
  ✓ Single cell test passed
  ✓ No diagonal connection test passed
  ✓ Empty grid test passed
  ✓ Full grid test passed
  ✓ Multiple regions test passed

Integration test:
  ✓ Example key test passed: 1242 regions

==================================================
ALL TESTS PASSED!
==================================================

Computing answer for actual input...
1182

FINAL ANSWER: 1182
```

## Key Design Decisions

### 1. Code Reuse from Part 1
- **Decision**: Copied all knot hash and grid generation functions from Part 1
- **Rationale**: Grid generation is identical between parts; no need to modify
- **Benefit**: Guaranteed consistency, reduced development time
- **Validation**: Confirmed 8140 used squares match Part 1 answer

### 2. Grid Representation
- **Decision**: Use list of strings (each row is a 128-character string of '0' and '1')
- **Rationale**:
  - Direct compatibility with Part 1 output
  - Simple and easy to debug
  - String indexing `grid[row][col] == '1'` is clean
- **Alternative considered**: List of lists of integers - rejected for unnecessary complexity

### 3. Visited Tracking
- **Decision**: Use `set()` of (row, col) tuples
- **Rationale**: O(1) lookup and insertion, automatic uniqueness handling
- **Benefit**: Efficient and simple

### 4. Flexible Grid Size
- **Decision**: Made functions work with any grid size (not hardcoded to 128x128)
- **Rationale**: Enables easier unit testing with smaller grids
- **Implementation**: Dynamically compute grid dimensions in functions
- **Benefit**: More robust and testable code

### 5. BFS Over Recursive DFS
- **Decision**: Use iterative BFS with deque
- **Rationale**: Avoids Python recursion limit issues
- **Benefit**: Handles arbitrarily large regions without stack overflow

## Performance

- **Grid Generation**: ~2-3 seconds (128 knot hash computations)
- **Region Counting**: <1 second (simple graph traversal)
- **Total Runtime**: ~3-4 seconds
- **Memory Usage**: <1 MB (grid + visited set)

Performance is well within acceptable limits for the problem size.

## Challenges and Solutions

### Challenge 1: Initial Index Error
- **Issue**: Test grids were small (7x7) but code was hardcoded to iterate 128x128
- **Solution**: Made grid functions dynamically determine dimensions
- **Result**: More flexible, testable code

### Challenge 2: Ensuring Correct Adjacency
- **Issue**: Must exclude diagonal connections
- **Solution**: Explicitly use only 4 direction vectors: `[(-1, 0), (1, 0), (0, -1), (0, 1)]`
- **Validation**: Unit test specifically verified diagonal cells not connected

### Challenge 3: Grid Consistency with Part 1
- **Issue**: Must ensure identical grid generation between parts
- **Solution**:
  - Copied functions verbatim from Part 1
  - Added assertion to verify 8140 used squares for input 'jxqlasbh'
- **Result**: Confirmed consistency

## Validation Against Requirements

✓ **Grid Generation**: Reused Part 1 logic, verified with 8140 used squares
✓ **Region Definition**: Orthogonal adjacency only (no diagonals)
✓ **Algorithm**: BFS flood fill for connected components
✓ **Example Test**: 1242 regions for 'flqrgnkx' ✓
✓ **Actual Input**: 1182 regions for 'jxqlasbh'
✓ **Edge Cases**: Empty grid, full grid, isolated cells
✓ **Boundary Checking**: All 4 edges and corners handled correctly

## Final Answer

**Input**: `jxqlasbh`
**Answer**: **1182 regions**

The solution correctly identifies 1182 distinct regions in the 128x128 grid, where regions are groups of orthogonally-adjacent used squares. This was validated against the known example which produced the expected result of 1242 regions.
