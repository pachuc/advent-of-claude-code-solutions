# Implementation Plan: Fabric Claim Overlap

## Problem Summary
Calculate the number of square inches of fabric that are claimed by 2 or more Elves. Each claim specifies a rectangular area on a fabric grid (at least 1000x1000 inches), and we need to find overlapping regions.

## Algorithm Analysis

### Input Characteristics
- 1286 claims in the input file
- Each claim is a rectangle with position (left, top) and dimensions (width, height)
- Fabric size is at least 1000x1000 inches
- Rectangles are relatively small (max 29x29 from visual inspection)

### Approach Considerations

**Option 1: 2D Grid Array (Chosen)**
- Create a 2D array to represent the fabric
- For each claim, mark all cells it covers
- Count cells with 2+ claims
- Time: O(n * w * h) where n = number of claims, w/h = average dimensions
- Space: O(fabric_width * fabric_height)
- Pros: Simple, direct, easy to debug
- Cons: Uses more memory

**Option 2: Interval/Coordinate Compression**
- Use coordinate compression to only track unique x and y coordinates
- More space-efficient for sparse inputs
- Time: O(n * w * h + k log k) where k = unique coordinates
- Space: O(n + k²)
- Pros: More efficient for very large fabrics with sparse claims
- Cons: More complex implementation

**Decision**: Use Option 1 (2D Grid Array) because:
1. The fabric size is manageable (1000x1000 = 1M cells)
2. Simple and straightforward implementation
3. Based on the input, we have 1286 claims with small rectangles - the grid will be reasonably populated
4. Memory usage is acceptable (~1-4 MB for integers)

### Runtime Complexity
- Parsing: O(n) where n = number of claims
- Grid marking: O(n * w * h) where w, h are average width/height
- Counting overlaps: O(fabric_width * fabric_height)
- Overall: O(n * w * h + fabric_size)
- For our input: ~1286 * 20 * 20 + 1000 * 1000 ≈ 1.5M operations (very fast)

## Implementation Steps

### Step 1: Parse Input Claims
```python
import re
from collections import namedtuple

Claim = namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])

def parse_claim(line):
    """Parse a claim line into components.

    Format: #<ID> @ <left>,<top>: <width>x<height>
    Example: #123 @ 3,2: 5x4

    Returns: Claim namedtuple with (id, left, top, width, height)
    """
    # Use regex to extract all components
    pattern = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
    match = re.match(pattern, line.strip())

    if not match:
        raise ValueError(f"Invalid claim format: {line}")

    # Extract and convert to integers
    claim_id, left, top, width, height = map(int, match.groups())
    return Claim(claim_id, left, top, width, height)
```

**Implementation details:**
- **Chosen approach**: Use regex pattern `#(\d+) @ (\d+),(\d+): (\d+)x(\d+)` for robustness
- **Data structure**: Use namedtuple for best balance of efficiency and readability
- Strip whitespace before parsing to handle extra spaces
- Raise ValueError for malformed lines to aid debugging
- Convert all extracted values to integers using map(int, ...)

### Step 2: Determine Fabric Dimensions
```python
def get_fabric_dimensions(claims):
    """Calculate required fabric dimensions.

    Returns: (max_width, max_height)
    """
    # Iterate through claims
    # Find max(left + width) for width
    # Find max(top + height) for height
    # Ensure at least 1000x1000, but expand if needed
    max_width = max_height = 1000
    for claim in claims:
        _, left, top, width, height = claim
        max_width = max(max_width, left + width)
        max_height = max(max_height, top + height)
    return max_width, max_height
```

**Implementation details:**
- **Critical**: Must calculate actual dimensions from claims to avoid index out of bounds
- Problem states fabric is "at least 1000x1000", so some claims may extend beyond
- Use 1000x1000 as minimum, but expand based on actual claim positions
- This prevents index errors when claims extend to edges like (995,995) with 5x5 size

### Step 3: Create and Populate Fabric Grid
```python
def create_fabric_grid(width, height):
    """Create a 2D grid initialized to zeros.

    Returns: 2D list or numpy array
    """
    # Use list comprehension: [[0] * width for _ in range(height)]
    # Or numpy: np.zeros((height, width), dtype=int)
```

```python
def mark_claim_on_grid(grid, claim):
    """Mark a claim on the fabric grid.

    For each cell covered by the claim, increment its counter.

    Coordinate system: (0,0) is top-left corner
    - x increases rightward (left coordinate)
    - y increases downward (top coordinate)
    - Claim at (left, top) with (width, height) covers:
      rows from top to (top + height - 1), inclusive
      cols from left to (left + width - 1), inclusive
    """
    # Use namedtuple attributes for clarity
    for y in range(claim.top, claim.top + claim.height):
        for x in range(claim.left, claim.left + claim.width):
            grid[y][x] += 1
```

**Implementation details:**
- Grid indexing: `grid[row][column]` where row=y, column=x
- Coordinate system: (0,0) at top-left, x is horizontal (left), y is vertical (top)
- Each cell stores count of how many claims cover it
- Increment counter for each claim that covers the cell
- Rectangle at (left, top) with (width, height) covers cells:
  - From column 'left' to 'left + width - 1' (inclusive)
  - From row 'top' to 'top + height - 1' (inclusive)

### Step 4: Count Overlapping Cells
```python
def count_overlaps(grid):
    """Count cells with 2 or more claims.

    Returns: integer count
    """
    count = 0
    for row in grid:
        for cell in row:
            if cell >= 2:
                count += 1
    return count
```

**Implementation details:**
- Iterate through entire grid
- Count cells where value >= 2
- Alternative: use list comprehension or numpy for efficiency
- `sum(1 for row in grid for cell in row if cell >= 2)`

### Step 5: Main Program Flow
```python
def main():
    # 1. Read input file
    # Note: input.md is the provided input file (unusual .md extension but correct)
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # 2. Parse all claims (skip empty lines)
    claims = []
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            try:
                claims.append(parse_claim(line))
            except ValueError as e:
                print(f"Warning: Skipping malformed line: {e}")
                continue

    # 3. Determine required fabric dimensions
    # Must calculate from actual claims to avoid index errors
    fabric_width, fabric_height = get_fabric_dimensions(claims)

    # 4. Create fabric grid
    grid = create_fabric_grid(fabric_width, fabric_height)

    # 5. Mark all claims on grid
    for claim in claims:
        mark_claim_on_grid(grid, claim)

    # 6. Count overlapping cells
    overlap_count = count_overlaps(grid)

    # 7. Output result to stdout
    print(overlap_count)

if __name__ == '__main__':
    main()
```

## Data Structures

### Claim Representation
- **Chosen**: `namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])`
- Provides both efficiency (like tuple) and readability (like dict)
- Access fields by name: `claim.left` instead of `claim[1]`
- Immutable and lightweight

### Fabric Grid
- **2D List**: `[[0] * width for _ in range(height)]` - Pure Python, sufficient
- **Numpy Array**: `np.zeros((height, width), dtype=int)` - Faster, cleaner code
- **Recommendation**: Use 2D list (no external dependencies) unless numpy is available

## Edge Cases to Consider

1. **Empty input**: No claims (return 0)
2. **No overlaps**: All claims are disjoint (return 0)
3. **Complete overlap**: Multiple claims for the exact same area
4. **Single claim**: Only one claim (return 0)
5. **Adjacent claims**: Claims touch but don't overlap (return 0)
6. **Grid boundaries**: Claims at edges (0,0) and (999,999)
7. **Large rectangles**: Claims that cover large areas

## Optimization Notes

- **Memory**: 1000x1000 Python integers = ~8-28MB depending on values (acceptable)
  - Python integers are objects, not raw 4-byte ints
  - Actual size depends on values stored
  - Still well within acceptable range for modern systems
- **Speed**: ~1.5M operations (milliseconds on modern hardware)
- **Alternative optimizations** (not needed for this problem size):
  - Use byte array instead of integers (cells won't exceed 255 claims)
  - Use sparse matrix for very large grids
  - Use coordinate compression for huge fabric dimensions

## File Structure

```
solution.py
├── parse_claim()           # Parse single claim line
├── create_fabric_grid()    # Initialize grid
├── mark_claim_on_grid()    # Mark claim on grid
├── count_overlaps()        # Count cells with 2+ claims
└── main()                  # Main execution flow
```

## Expected Output Format
Single integer representing total square inches of overlap, printed to stdout.

## Updates Based on Critique

### Critical Fixes Applied

1. **Grid Size Determination (Step 2)**:
   - Changed from fixed 1000x1000 to dynamically calculated dimensions
   - Now calculates actual required size from claims to prevent index errors
   - Uses 1000x1000 as minimum but expands if claims extend beyond
   - Critical fix: prevents index out of bounds for claims like (995,995) with 5x5 size

2. **Parsing Implementation (Step 1)**:
   - Finalized approach: using regex pattern `#(\d+) @ (\d+),(\d+): (\d+)x(\d+)`
   - Chosen data structure: namedtuple for claim representation
   - Added error handling: raises ValueError for malformed input
   - Handles whitespace: strips input before parsing

3. **Main Program Flow (Step 5)**:
   - Added proper error handling for malformed input lines
   - Grid dimensions now calculated from claims (not hardcoded)
   - Added comment explaining unusual .md extension for input file
   - Added try-except block for parsing errors with warning messages

### Additional Improvements

4. **Coordinate System Documentation**:
   - Explicitly documented that (0,0) is top-left corner
   - Clarified x is horizontal (left), y is vertical (top)
   - Documented inclusive/exclusive edge behavior in mark_claim_on_grid

5. **Data Structure Choice**:
   - Finalized as namedtuple (not left ambiguous)
   - Updated all code examples to use `claim.left` notation
   - Provides clarity without sacrificing performance

6. **Memory Estimate Correction**:
   - Updated from ~4MB to ~8-28MB for Python integers
   - Acknowledged Python integers are objects, not raw 4-byte values
   - Conclusion unchanged: still acceptable for this problem

### Consistency with Test Plan

All implementation details now align with the test plan:
- Dynamic grid sizing matches Test 8 expectations
- Claim namedtuple matches Test 1 expectations
- Error handling matches Test 1.6 requirements
- Coordinate system matches Test 0 assumptions
