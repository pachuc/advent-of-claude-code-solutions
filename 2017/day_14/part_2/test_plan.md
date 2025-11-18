# Test Plan: Disk Defragmentation - Region Counting (Part 2)

## Testing Strategy
Validate the connected components algorithm through unit tests, integration tests, and verification against known examples.

## Test Categories

### 1. Grid Generation Validation (Reuse from Part 1)

#### Test 1.1: Grid Format and Dimensions
**Purpose**: Verify generate_grid returns correct format and dimensions

**Test Case**:
```python
def test_grid_format_and_dimensions():
    grid = generate_grid('test')

    # Check it's a list
    assert isinstance(grid, list), "Grid should be a list"
    assert len(grid) == 128, f"Expected 128 rows, got {len(grid)}"

    # Check each row is a string of length 128 with only binary chars
    for i, row in enumerate(grid):
        assert isinstance(row, str), f"Row {i} should be string, got {type(row)}"
        assert len(row) == 128, f"Row {i} has {len(row)} chars, expected 128"
        assert all(c in '01' for c in row), f"Row {i} contains non-binary chars"
```

**Expected**: All assertions pass

#### Test 1.2: Grid Consistency with Part 1
**Purpose**: Verify grid generation produces same results as Part 1

**Test Case**:
```python
def test_grid_consistency():
    key = 'jxqlasbh'
    grid = generate_grid(key)

    # Count total used squares
    total_used = sum(row.count('1') for row in grid)
    expected = 8140  # From part_1_answer.txt

    assert total_used == expected, f"Expected {expected} used squares, got {total_used}"
```

**Expected**: 8140 used squares (matches Part 1 answer)

#### Test 1.3: Grid Content Validation
**Purpose**: Verify grid contains only valid binary values

**Test Case**:
```python
def test_grid_content():
    grid = generate_grid('test')
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            assert cell in ['0', '1'], f"Invalid cell at ({row_idx}, {col_idx}): {cell}"
```

**Expected**: All cells are '0' or '1'

### 2. Flood Fill Algorithm Tests

#### Test 2.1: Single Cell Region
**Purpose**: Test flood fill on isolated single cell

**Test Case**:
```python
def test_flood_fill_single_cell():
    # Create small 3x3 grid with single used cell in center
    grid = [
        '000',
        '010',
        '000'
    ]
    visited = set()
    flood_fill_bfs(grid, 1, 1, visited)

    assert (1, 1) in visited, "Center cell should be visited"
    assert len(visited) == 1, f"Expected 1 visited cell, got {len(visited)}"
```

**Expected**: Only center cell visited

#### Test 2.2: Horizontal Line Region
**Purpose**: Test flood fill on horizontal connected cells

**Test Case**:
```python
def test_flood_fill_horizontal():
    grid = [
        '000',
        '111',
        '000'
    ]
    visited = set()
    flood_fill_bfs(grid, 1, 0, visited)

    assert (1, 0) in visited
    assert (1, 1) in visited
    assert (1, 2) in visited
    assert len(visited) == 3, f"Expected 3 visited cells, got {len(visited)}"
```

**Expected**: All three cells in middle row visited

#### Test 2.3: Vertical Line Region
**Purpose**: Test flood fill on vertical connected cells

**Test Case**:
```python
def test_flood_fill_vertical():
    grid = [
        '010',
        '010',
        '010'
    ]
    visited = set()
    flood_fill_bfs(grid, 0, 1, visited)

    assert len(visited) == 3, f"Expected 3 visited cells, got {len(visited)}"
    assert (0, 1) in visited
    assert (1, 1) in visited
    assert (2, 1) in visited
```

**Expected**: All three cells in middle column visited

#### Test 2.4: L-Shape Region
**Purpose**: Test flood fill on non-linear connected shape

**Test Case**:
```python
def test_flood_fill_l_shape():
    grid = [
        '100',
        '100',
        '111'
    ]
    visited = set()
    flood_fill_bfs(grid, 0, 0, visited)

    expected_cells = {(0,0), (1,0), (2,0), (2,1), (2,2)}
    assert len(visited) == 5, f"Expected 5 visited cells, got {len(visited)}"
    assert visited == expected_cells, f"Visited cells mismatch: {visited}"
```

**Expected**: L-shape fully connected (5 cells)

#### Test 2.5: Diagonal Non-Connection
**Purpose**: Verify diagonal cells are NOT treated as connected

**Test Case**:
```python
def test_flood_fill_no_diagonal():
    grid = [
        '101',
        '010',
        '101'
    ]
    visited = set()
    flood_fill_bfs(grid, 1, 1, visited)

    # Only center cell should be in this region
    assert len(visited) == 1, f"Expected 1 visited cell, got {len(visited)}"
    assert visited == {(1, 1)}, f"Only center should be visited: {visited}"
```

**Expected**: Only center cell visited, diagonal cells not connected

#### Test 2.6: Complex Connected Region
**Purpose**: Test larger irregular shape

**Test Case**:
```python
def test_flood_fill_complex():
    grid = [
        '11010',
        '01110',
        '00100',
        '01110',
        '00100'
    ]

    # Test top-left region: (0,0) and (0,1) are connected
    visited = set()
    flood_fill_bfs(grid, 0, 0, visited)
    assert len(visited) == 2, f"Expected 2 cells in top-left region, got {len(visited)}"
    assert visited == {(0, 0), (0, 1)}, "Top-left region should be just (0,0) and (0,1)"

    # Test center plus-sign region
    # Starting from (1,1), should reach: (1,1), (1,2), (1,3), (2,2), (3,1), (3,2), (3,3), (4,2)
    visited.clear()
    flood_fill_bfs(grid, 1, 1, visited)
    assert len(visited) == 8, f"Expected 8 cells in center region, got {len(visited)}"

    # Test isolated cell at (0,3)
    visited.clear()
    flood_fill_bfs(grid, 0, 3, visited)
    assert len(visited) == 1, f"Expected 1 cell (isolated), got {len(visited)}"
    assert visited == {(0, 3)}, "Should be single isolated cell"
```

**Expected**: Correctly identifies separate regions and complex shapes
**Note**: Since flood_fill_bfs no longer returns region size, we test by checking len(visited)

### 3. Region Counting Tests

#### Test 3.1: Empty Grid
**Purpose**: Test grid with no used squares

**Test Case**:
```python
def test_count_regions_empty():
    grid = ['0' * 128 for _ in range(128)]
    count = count_regions(grid)
    assert count == 0, f"Expected 0 regions, got {count}"
```

**Expected**: 0 regions

#### Test 3.2: Full Grid
**Purpose**: Test grid completely filled

**Test Case**:
```python
def test_count_regions_full():
    grid = ['1' * 128 for _ in range(128)]
    count = count_regions(grid)
    assert count == 1, f"Expected 1 region (all connected), got {count}"
```

**Expected**: 1 region (entire grid is connected)

#### Test 3.3: Checkerboard Pattern
**Purpose**: Test maximum isolated regions

**Test Case**:
```python
def test_count_regions_checkerboard():
    # Create 4x4 checkerboard for simplicity
    grid = [
        '0101',
        '1010',
        '0101',
        '1010'
    ]
    count = count_regions(grid)
    # Each '1' is isolated (8 total ones)
    assert count == 8, f"Expected 8 isolated regions, got {count}"
```

**Expected**: 8 regions (each cell isolated)

#### Test 3.4: Multiple Distinct Regions
**Purpose**: Test grid with several separate regions

**Test Case**:
```python
def test_count_regions_multiple():
    grid = [
        '1100110',
        '1100110',
        '0000000',
        '0111000',
        '0111000',
        '0000011',
        '0000011'
    ]
    count = count_regions(grid)
    # Should find 4 distinct regions:
    # - Top-left 2x2
    # - Top-right 2x2
    # - Middle 2x3
    # - Bottom-right 2x2
    assert count == 4, f"Expected 4 regions, got {count}"
```

**Expected**: 4 distinct regions

#### Test 3.5: Small Grid with Multiple Clear Regions
**Purpose**: Test multiple distinct regions in a small grid

**Test Case**:
```python
def test_count_regions_small_example():
    # 8x8 grid with 4 clear distinct regions
    grid = [
        '11000110',
        '11000110',
        '00000000',
        '01110000',
        '01110000',
        '00000011',
        '00000011',
        '00000000'
    ]
    count = count_regions(grid)
    # 4 distinct regions:
    # - Top-left 2x2: (0,0)-(1,1)
    # - Top-right 2x2: (0,5)-(1,6)
    # - Middle 2x3: (3,1)-(4,3)
    # - Bottom-right 2x2: (5,6)-(6,7)
    assert count == 4, f"Expected 4 regions, got {count}"
```

**Expected**: Exactly 4 regions detected

### 4. Integration Tests

#### Test 4.1: Example Key Test
**Purpose**: Validate against known answer for example key

**Test Case**:
```python
def test_example_key():
    result = solve_part2('flqrgnkx')
    expected = 1242
    assert result == expected, f"Expected {expected} regions, got {result}"
```

**Expected**: 1242 regions

**Critical**: This is the most important test - if this passes, the solution is very likely correct

#### Test 4.2: Actual Input Test
**Purpose**: Solve for actual puzzle input and validate reasonableness

**Test Case**:
```python
def test_actual_input():
    key = 'jxqlasbh'
    result = solve_part2(key)

    # We know from Part 1 that there are 8140 used squares
    # So regions must be between 1 (all connected) and 8140 (all isolated)
    assert 1 <= result <= 8140, f"Result {result} outside valid range [1, 8140]"

    # Sanity check: with 8140 used squares, we'd expect hundreds to low thousands of regions
    # (not 1, which would mean entire grid connected in one component)
    # (not 8140, which would mean every cell is isolated)
    assert result > 100, f"Result {result} seems suspiciously low (all connected?)"
    assert result < 5000, f"Result {result} seems suspiciously high (mostly isolated?)"

    print(f"Actual input 'jxqlasbh' has {result} regions")
```

**Expected**: Result between 100 and 5000 (reasonable range for this problem)

### 5. Edge Cases and Boundary Tests

#### Test 5.1: Corner Cells
**Purpose**: Verify boundary checking for corner cells

**Test Case**:
```python
def test_corners():
    # Test each corner can be visited without index errors
    grid = ['1' + '0' * 127 for _ in range(128)]  # Top-left corner
    visited = set()
    flood_fill_bfs(grid, 0, 0, visited)
    assert (0, 0) in visited

    # Test bottom-right corner
    grid = ['0' * 127 + '1' if i == 127 else '0' * 128 for i in range(128)]
    visited.clear()
    flood_fill_bfs(grid, 127, 127, visited)
    assert (127, 127) in visited
```

**Expected**: No index errors, corners handled correctly

#### Test 5.2: Edge Cells
**Purpose**: Verify boundary checking for edge cells

**Test Case**:
```python
def test_edges():
    # Top edge
    grid = ['1' * 128] + ['0' * 128 for _ in range(127)]
    count = count_regions(grid)
    assert count == 1, f"Top edge should be one region, got {count}"

    # Left edge
    grid = ['1' + '0' * 127 for _ in range(128)]
    count = count_regions(grid)
    assert count == 1, f"Left edge should be one region, got {count}"
```

**Expected**: Edge cells properly connected

#### Test 5.3: Already Visited Cells
**Purpose**: Ensure algorithm doesn't revisit cells

**Test Case**:
```python
def test_no_revisit():
    grid = ['111', '111', '111']
    visited = set()
    visited.add((0, 0))  # Pre-mark one cell as visited

    flood_fill_bfs(grid, 1, 1, visited)

    # Should visit 8 new cells (9 total - 1 pre-visited) = 9 total in visited set
    assert len(visited) == 9, f"Expected 9 cells total in visited set, got {len(visited)}"
    assert (0, 0) in visited, "Pre-visited cell should still be in set"
```

**Expected**: Pre-visited cells skipped, total 9 cells in visited set

### 6. Performance Tests

#### Test 6.1: Runtime Performance
**Purpose**: Ensure solution completes in reasonable time

**Test Case**:
```python
import time

def test_performance():
    start = time.time()
    result = solve_part2('flqrgnkx')
    elapsed = time.time() - start

    # Grid generation: ~1-2s, Region counting: <0.1s → Total should be < 3s
    assert elapsed < 3.0, f"Solution took {elapsed:.2f}s, should be under 3s"
    print(f"Performance: {elapsed:.2f}s for full 128x128 grid")
```

**Expected**: Completes in under 3 seconds

#### Test 6.2: Memory Usage
**Purpose**: Verify reasonable memory consumption

**Test Case**:
```python
import sys

def test_memory():
    grid = generate_grid('test')
    grid_size = sys.getsizeof(grid)

    # Grid should be reasonably sized (rough estimate: < 1MB)
    assert grid_size < 1_000_000, f"Grid size {grid_size} bytes seems too large"
```

**Expected**: Memory usage under 1 MB

## Test Execution Order

1. **Quick Unit Tests** (Run first for fast feedback):
   - Flood fill tests (2.1-2.6) - small grids, very fast
   - Region counting tests (3.1-3.5) - small grids, very fast

2. **Grid Generation Tests** (Run second):
   - Grid generation tests (1.1-1.3) - includes Part 1 validation

3. **Critical Integration Test** (Run third):
   - Example key test (4.1) - **CRITICAL VALIDATION** - must pass for correctness

4. **Edge Cases** (Run fourth):
   - Boundary tests (5.1-5.3)

5. **Actual Input** (Run fifth):
   - Actual input test (4.2) - solve the puzzle

6. **Performance** (Run last):
   - Runtime and memory tests (6.1-6.2)

This order provides fast feedback from unit tests, validates correctness early, then tests edge cases and performance.

## Success Criteria

### Must Pass:
- ✓ Grid consistency test (1.2) - confirms Part 1 integration
- ✓ Diagonal non-connection test (2.5) - confirms correct adjacency
- ✓ Example key test (4.1) - confirms overall correctness
- ✓ All boundary tests (5.1-5.2) - confirms no index errors

### Should Pass:
- All unit tests (1.x, 2.x, 3.x)
- Actual input sanity check (4.2)
- Performance tests (6.1-6.2)

## Validation Strategy

1. **Compare with Part 1**: Ensure grid has exactly 8140 used squares for input `jxqlasbh`
2. **Verify Example**: Must get 1242 regions for `flqrgnkx`
3. **Sanity Check Result**: For `jxqlasbh`, result should be between 1 and 8140
4. **Visual Inspection**: Can manually verify small test grids

## Debugging Checklist

If tests fail:

1. **Grid generation mismatch**:
   - Compare Part 1 and Part 2 grid generation
   - Verify knot hash implementation
   - Check hex-to-binary conversion

2. **Wrong region count**:
   - Print grid and visited sets for small test cases
   - Verify 4-connectivity only (no diagonals)
   - Check boundary conditions
   - Ensure visited set persists across flood fills

3. **Index errors**:
   - Verify bounds checking: `0 <= row < 128 and 0 <= col < 128`
   - Check neighbor calculation
   - Test corner and edge cases

4. **Performance issues**:
   - Use BFS instead of recursive DFS
   - Ensure visited set is being used correctly
   - Profile grid generation vs region counting
