# Implementation Plan: Disk Defragmentation - Region Counting (Part 2)

## Overview
Count the total number of distinct regions in a 128x128 disk grid where regions are groups of orthogonally-adjacent "used" squares. This builds directly on Part 1's grid generation.

## Algorithm: Flood Fill with BFS/DFS for Connected Components

### Time Complexity
- **Grid Generation**: O(128 × 128) = O(16,384) cells, but each cell requires a knot hash computation
  - Knot hash: O(64 rounds × 256 operations) = O(16,384) per hash
  - Total for grid: O(128 × 16,384) ≈ O(2,097,152) operations
- **Region Counting**: O(128 × 128) = O(16,384) for BFS/DFS traversal
  - Each cell visited exactly once
  - Each cell's neighbors checked at most once
- **Overall**: Dominated by grid generation, but still efficient for 128×128 grid

### Space Complexity
- Grid storage: O(128 × 128) = O(16,384) cells
- Visited set: O(16,384) cells in worst case
- BFS queue: O(16,384) in worst case (all cells in one region)
- **Overall**: O(16,384) which is acceptable

## Implementation Steps

### Step 1: Reuse Grid Generation from Part 1
**Objective**: Generate the 128x128 binary grid

**Implementation**:
1. Copy all knot hash functions from `part_1_solution.py`:
   - `compute_knot_hash()`
   - `hex_to_binary()`
   - `generate_row_input()`
   - All supporting knot hash functions

2. Create a new function `generate_grid(key)`:
   - Input: key string
   - Output: 128×128 grid as list of lists (or list of strings)
   - Process:
     ```python
     def generate_grid(key):
         grid = []
         for row in range(128):
             row_input = generate_row_input(key, row)
             hash_hex = compute_knot_hash(row_input)
             hash_binary = hex_to_binary(hash_hex)
             grid.append(hash_binary)  # Store as string or convert to list
         return grid
     ```

**Why this approach**:
- Reuses proven code from Part 1
- Grid generation is identical between parts
- Clear separation of concerns

### Step 2: Implement Flood Fill (BFS)
**Objective**: Mark all cells in a connected region as visited

**Implementation**:
1. Create `flood_fill_bfs(grid, start_row, start_col, visited)`:
   - Input: grid, starting coordinates, visited set
   - Output: None (modifies visited set in-place)
   - Purpose: Mark all cells in this region as visited
   - Algorithm:
     ```python
     def flood_fill_bfs(grid, start_row, start_col, visited):
         from collections import deque

         queue = deque([(start_row, start_col)])
         visited.add((start_row, start_col))

         while queue:
             row, col = queue.popleft()

             # Check all 4 orthogonal neighbors
             for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                 new_row, new_col = row + dr, col + dc

                 # Check bounds
                 if 0 <= new_row < 128 and 0 <= new_col < 128:
                     # Check if used and not visited
                     if (new_row, new_col) not in visited:
                         if grid[new_row][new_col] == '1':
                             visited.add((new_row, new_col))
                             queue.append((new_row, new_col))
     ```

**Why BFS over DFS**:
- BFS uses explicit queue, less risk of stack overflow
- Python's recursion limit (default ~1000) could be exceeded with DFS on large regions
- BFS is iterative and more predictable for large grids

**Alternative**: DFS with explicit stack is also acceptable and would be similar complexity

**Design Note**: Function doesn't return region size to keep it focused on a single purpose (marking visited cells). Region size can be computed separately if needed for debugging.

### Step 3: Implement Region Counter
**Objective**: Count all distinct regions in the grid

**Implementation**:
1. Create `count_regions(grid)`:
   - Input: 128×128 grid
   - Output: Total number of regions
   - Algorithm:
     ```python
     def count_regions(grid):
         visited = set()
         region_count = 0

         for row in range(128):
             for col in range(128):
                 # Check if cell is used and not yet visited
                 if grid[row][col] == '1' and (row, col) not in visited:
                     # Found a new region
                     region_count += 1
                     # Mark all cells in this region as visited
                     flood_fill_bfs(grid, row, col, visited)

         return region_count
     ```

**Key logic**:
- Iterate through every cell in the grid
- When we find an unvisited "used" cell, we've found a new region
- Flood fill marks all connected cells as visited
- This ensures each region is counted exactly once

### Step 4: Main Solution Function
**Objective**: Combine grid generation and region counting with validation

**Implementation**:
```python
def solve_part2(key):
    # Step 1: Generate grid (reuse from Part 1)
    grid = generate_grid(key)

    # CRITICAL VALIDATION: Verify grid matches Part 1 expectations
    # This ensures Part 1 and Part 2 use identical grid generation
    if key == 'jxqlasbh':
        total_used = sum(row.count('1') for row in grid)
        assert total_used == 8140, f"Grid mismatch: expected 8140 used squares, got {total_used}"

    # Step 2: Count regions
    region_count = count_regions(grid)

    # Sanity check: regions must be between 1 and total used squares
    total_used = sum(row.count('1') for row in grid)
    assert 1 <= region_count <= total_used, f"Invalid region count: {region_count}"

    return region_count
```

**Why this validation is important**:
- Ensures Part 1 and Part 2 grid generation are identical
- Catches potential bugs in grid generation early
- Validates result is in reasonable range

### Step 5: Testing Infrastructure
**Objective**: Validate correctness with known test case

**Implementation**:
1. Test with example key `flqrgnkx`:
   ```python
   def test_example():
       result = solve_part2('flqrgnkx')
       expected = 1242
       assert result == expected, f"Expected {expected}, got {result}"
       print(f"✓ Example test passed: {result} regions")
   ```

2. Unit tests for helper functions:
   - Test `generate_grid()` produces correct dimensions
   - Test `flood_fill_bfs()` on small synthetic grids
   - Test edge cases (empty grid, full grid, single cell)

### Step 6: Main Execution
**Objective**: Solve for actual puzzle input

**Implementation**:
```python
def main():
    # Read input
    with open('input.md', 'r') as f:
        key = f.read().strip()

    # Solve
    result = solve_part2(key)

    # Output
    print(result)
    return result

if __name__ == "__main__":
    print("Running tests...\n")
    test_example()

    print("\nComputing answer for actual input...")
    result = main()
    print(f"\nFINAL ANSWER: {result}")
```

## Code Structure

```
# Knot Hash Functions (from Part 1)
- initialize_list()
- reverse_circular()
- parse_input_as_ascii()
- knot_hash_rounds()
- create_dense_hash()
- to_hex_string()
- compute_knot_hash()

# Grid Generation (from Part 1, refactored)
- hex_to_binary()
- generate_row_input()
- generate_grid()  # NEW: wraps Part 1 logic

# Region Counting (NEW for Part 2)
- flood_fill_bfs()  # Marks all cells in a region as visited (no return value)
- count_regions()   # Main counting logic, returns total regions

# Solution
- solve_part2()     # Combines grid generation + counting + validation

# Testing
- test_example()
- test_flood_fill()
- test_edge_cases()

# Main
- main()
```

## Key Implementation Details

### Grid Representation
**Decision: Use list of strings** (each row is a 128-character string of '0' and '1')

**Rationale**:
1. **Direct compatibility**: Matches Part 1 output format exactly, no conversion needed
2. **Simplicity**: Can reuse Part 1's `hex_to_binary()` function directly
3. **Debugging**: Easy to print and inspect (just print the row string)
4. **Performance**: String indexing `grid[row][col] == '1'` is negligible compared to knot hash computation
5. **Consistency**: Same data structure throughout the solution

**Alternative considered**: List of lists of integers (0 and 1)
- Would require converting each binary string to list: `[int(c) for c in hash_binary]`
- Adds extra step and memory allocation
- No meaningful performance benefit for our use case
- Rejected in favor of simplicity

### Visited Tracking
- Use a `set()` of tuples `(row, col)`
- O(1) lookup and insertion
- Automatically handles uniqueness

### Neighbor Iteration
- Use direction vectors: `[(-1, 0), (1, 0), (0, -1), (0, 1)]`
- Up, Down, Left, Right
- Makes code clean and avoids diagonal checks

### Boundary Checking
- Always check: `0 <= row < 128 and 0 <= col < 128`
- Do this BEFORE checking cell value to avoid index errors

## Expected Output
- For test key `flqrgnkx`: **1242 regions**
- For puzzle input `jxqlasbh`: **?** (to be computed)

## Performance Considerations
- Grid generation takes ~1-2 seconds (128 knot hashes)
- Region counting takes <0.1 seconds (simple graph traversal)
- Total runtime should be under 3 seconds
- Memory usage is minimal (< 1 MB for all data structures)

## Potential Issues and Mitigations

1. **Stack overflow with recursive DFS**
   - Mitigation: Use iterative BFS with deque

2. **Off-by-one errors in grid indexing**
   - Mitigation: Careful boundary checks, test with small grids

3. **Missing diagonal exclusion**
   - Mitigation: Only use 4 direction vectors, never 8

4. **Grid generation mismatch from Part 1**
   - Mitigation: Reuse exact same functions, verify with Part 1 answer (8140 used squares)
