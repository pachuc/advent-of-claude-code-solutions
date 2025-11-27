# Implementation Plan: Fuel Cell Power Grid - Part 2

## Problem Summary
Find the square of **any size** (1x1 to 300x300) with the largest total power in a 300x300 grid. Return the identifier as `X,Y,size`.

## Key Differences from Part 1
- Part 1: Only checked 3x3 squares (~88,804 squares)
- Part 2: Must check all square sizes from 1 to 300 (~26.6 million squares)
- Performance is critical - naive approach would be O(n^5) which is too slow

## Algorithm Strategy: Summed-Area Table (Integral Image)

### Why This Approach?
- **Naive approach**: O(n^5) - For each of 300 sizes, check ~300x300 positions, sum ~size^2 cells
  - Estimated operations: 300 × 300 × 300 × avg(150^2) ≈ 6 billion operations
- **Summed-area table**: O(n^3) - Precompute cumulative sums, then O(1) lookups per square
  - Estimated operations: 300 × 300 × 300 ≈ 27 million operations (~200x speedup)

### Summed-Area Table Concept
A summed-area table (SAT) allows us to calculate the sum of any rectangular region in O(1) time after O(n^2) preprocessing.

**SAT Definition**: `SAT[y][x]` = sum of all grid values from `(1,1)` to `(x,y)` inclusive

**Rectangle Sum Formula**: For a rectangle from `(x1,y1)` to `(x2,y2)`:
```
sum = SAT[y2][x2] - SAT[y1-1][x2] - SAT[y2][x1-1] + SAT[y1-1][x1-1]
```

**For a square of size S at position (x,y)**:
```
sum = SAT[y+S-1][x+S-1] - SAT[y-1][x+S-1] - SAT[y+S-1][x-1] + SAT[y-1][x-1]
```

## Implementation Steps

### Step 1: Reuse Part 1 Code Structure
**File**: Adapt from `part_1_solution.py`

**Reusable components**:
- `read_input()` - identical
- `calculate_power_level()` - identical
- `build_power_grid()` - identical

**Components to modify**:
- `find_max_power_square()` - needs complete rewrite for variable sizes
- `calculate_square_power()` - can be removed (replaced by SAT lookup)
- `format_output()` - needs to include size parameter

### Step 2: Build Summed-Area Table
**Function**: `build_summed_area_table(grid: list, grid_size: int = 300) -> list`

**Algorithm**:
```python
# Create SAT with 1-based indexing and 0-padding on edges for boundary handling
# sat[0][x] and sat[y][0] are all 0, allowing safe access to sat[y-1][x-1] when y=1 or x=1
sat = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]

# Build using dynamic programming
for y in range(1, grid_size + 1):
    for x in range(1, grid_size + 1):
        sat[y][x] = (grid[y][x] +      # Current cell value
                     sat[y-1][x] +      # Sum above
                     sat[y][x-1] -      # Sum to left
                     sat[y-1][x-1])     # Subtract overlap
return sat
```

**Complexity**: O(n^2) where n=300
**Memory**: ~300×300×4 bytes = ~360 KB (negligible)

**Note**: Both `grid` and `sat` use 1-based indexing (coordinates 1-300) with row/column 0 as padding.

### Step 3: Calculate Square Sum Using SAT
**Function**: `get_square_sum(sat: list, x: int, y: int, size: int) -> int`

**Algorithm**:
```python
# Calculate coordinates of bottom-right corner
x2 = x + size - 1
y2 = y + size - 1

# Use SAT formula with boundary checks
return (sat[y2][x2] -
        sat[y-1][x2] -
        sat[y2][x-1] +
        sat[y-1][x-1])
```

**Complexity**: O(1) per square
**Note**: Since SAT is 0-padded, accessing `sat[y-1][x-1]` when y=1 or x=1 is safe (returns 0)

### Step 4: Search All Squares of All Sizes
**Function**: `find_max_power_square_any_size(sat: list, grid_size: int = 300) -> tuple`

**Algorithm**:
```python
max_power = float('-inf')
best_x, best_y, best_size = 0, 0, 0

# Iterate through all possible square sizes
for size in range(1, grid_size + 1):
    # For this size, iterate through all valid positions
    for y in range(1, grid_size - size + 2):
        for x in range(1, grid_size - size + 2):
            power = get_square_sum(sat, x, y, size)

            if power > max_power:
                max_power = power
                best_x, best_y, best_size = x, y, size

return (best_x, best_y, best_size), max_power
```

**Complexity**: O(n^3) where n=300
- Outer loop: 300 iterations (sizes)
- Middle/inner loops: ~300×300 for each size (fewer as size increases)
- Total: ~27 million iterations, each doing O(1) work

**Optimization note**: The loop bounds ensure squares fit in the grid:
- For size=1: positions from (1,1) to (300,300)
- For size=300: only position (1,1)

### Step 5: Update Output Formatting
**Function**: `format_output(coord: tuple) -> str`

**Algorithm**:
```python
# coord is now (x, y, size)
return f"{coord[0]},{coord[1]},{coord[2]}"
```

### Step 6: Main Function Integration
**Function**: `main()`

**Flow**:
```python
def main():
    # Step 1: Read input
    serial_number = read_input('input.md')

    # Step 2: Build power grid (reuse from Part 1)
    grid = build_power_grid(serial_number)

    # Step 3: Build summed-area table
    sat = build_summed_area_table(grid)

    # Step 4: Find maximum power square of any size
    max_coord, max_power = find_max_power_square_any_size(sat)

    # Step 5: Format and output result
    result = format_output(max_coord)
    print(result)
    return result
```

## Performance Estimates

### Time Complexity
- Build power grid: O(n^2) = 90,000 operations
- Build SAT: O(n^2) = 90,000 operations
- Search all squares: O(n^3) = 27,000,000 operations
- **Total**: O(n^3) ≈ 27 million simple arithmetic operations

### Expected Runtime
- Modern CPU: ~1-10 billion simple operations/second
- Estimated runtime: **2-5 seconds** (acceptable for this problem)

### Space Complexity
- Power grid: 300×300 integers = ~360 KB
- Summed-area table: 300×300 integers = ~360 KB
- **Total**: O(n^2) ≈ 720 KB (negligible)

## Alternative Optimizations (Not Implemented)

### Early Termination
- Could track maximum possible power for remaining sizes
- Likely minimal benefit since we need to check most squares anyway

### Parallel Processing
- Could parallelize outer loop (by size)
- Python GIL limits effectiveness for CPU-bound tasks
- Added complexity not worth it for ~5 second runtime

### Incremental Calculation
- For size S+1, reuse calculations from size S
- More complex code, marginal improvement over SAT approach

## Code Structure

```
part_2_solution.py
├── read_input()                          [Reused from Part 1]
├── calculate_power_level()               [Reused from Part 1]
├── build_power_grid()                    [Reused from Part 1]
├── build_summed_area_table()             [NEW]
├── get_square_sum()                      [NEW]
├── find_max_power_square_any_size()      [NEW - replaces Part 1's find_max_power_square]
├── format_output()                       [Modified to include size]
└── main()                                [Modified workflow]
```

## Implementation Checklist

1. [ ] Copy reusable functions from Part 1
2. [ ] Implement `build_summed_area_table()` with proper boundary handling
3. [ ] Implement `get_square_sum()` for O(1) square sum lookup
4. [ ] Implement `find_max_power_square_any_size()` with triple-nested loop
5. [ ] Update `format_output()` to include size parameter
6. [ ] Update `main()` to use new workflow with SAT
7. [ ] Add verification step against Part 1 answer (3x3 square should be at 21,68)
8. [ ] Test with example inputs (serial 18 → 90,269,16, serial 42 → 232,251,12)
