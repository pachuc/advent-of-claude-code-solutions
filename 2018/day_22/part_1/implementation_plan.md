# Implementation Plan: Cave Risk Level Calculation

## Updates from Critique

This plan has been updated based on feedback to include:
1. **Explicit 2D array initialization syntax** - Added clear syntax for creating the erosion_levels array
2. **Loop order warnings** - Emphasized that y-outer, x-inner is the ONLY correct order
3. **Access pattern clarification** - Specified erosion_levels[y][x] for coordinates (x,y)
4. **Comments on constants** - Added recommendation to comment magic numbers in code
5. **Input assumptions** - Noted that we assume well-formed input per AoC standards

## Problem Analysis

We need to calculate the total risk level for a rectangular cave region from (0,0) to the target coordinates. The calculation involves:
1. Computing geologic indices based on specific rules with dependencies
2. Computing erosion levels from geologic indices
3. Determining region types and risk levels
4. Summing all risk levels in the target rectangle

**Input Size Consideration**: The target is (15, 740), meaning we need to compute 16 × 741 = 11,856 cells. This is manageable with proper algorithm design.

**Key Challenge**: The geologic index calculation has dependencies - most cells depend on erosion levels of their left and top neighbors. This requires careful ordering of computations.

## Algorithm Approach

**Strategy**: Dynamic Programming with row-by-row processing
- **Time Complexity**: O(X × Y) where X and Y are target coordinates
- **Space Complexity**: O(X × Y) to store all erosion levels (needed for dependency resolution)

**Why this approach?**
- We must compute cells in order to satisfy dependencies (cell at (x,y) needs erosion levels from (x-1,y) and (x,y-1))
- Processing row by row (or column by column) ensures dependencies are always available
- Memoization avoids recalculation

## Step-by-Step Implementation Plan

### Step 1: Input Parsing
**File**: `solution.py`

```python
def parse_input(filename):
    """
    Parse the input file to extract depth and target coordinates.

    Expected format:
    depth: <integer>
    target: <X>,<Y>

    Returns:
        tuple: (depth, target_x, target_y)
    """
```

**Implementation details**:
- Read file line by line
- Split on ":" to separate keys from values
- Strip whitespace
- Parse depth as integer
- Split target on "," and parse both coordinates as integers
- Return tuple of (depth, target_x, target_y)

**Error handling**: Basic file reading (file must exist)

---

### Step 2: Geologic Index Calculation
**File**: `solution.py`

```python
def calculate_geologic_index(x, y, target_x, target_y, erosion_levels):
    """
    Calculate geologic index for position (x, y).

    Rules (in order of precedence):
    1. Cave mouth (0,0): return 0
    2. Target position: return 0
    3. Y == 0: return X * 16807
    4. X == 0: return Y * 48271
    5. Otherwise: return erosion_level(x-1, y) * erosion_level(x, y-1)

    Args:
        x, y: Current coordinates
        target_x, target_y: Target coordinates
        erosion_levels: 2D structure storing computed erosion levels

    Returns:
        int: Geologic index for the position
    """
```

**Implementation details**:
- Use if-elif chain to check rules in order
- For rule 5, retrieve erosion levels from the data structure (must already be computed)
- Ensure erosion_levels structure is accessible (pass as parameter or use closure)

---

### Step 3: Erosion Level Calculation
**File**: `solution.py`

```python
def calculate_erosion_level(geologic_index, depth):
    """
    Calculate erosion level from geologic index.

    Formula: (geologic_index + depth) % 20183

    Args:
        geologic_index: The geologic index
        depth: Cave system depth

    Returns:
        int: Erosion level
    """
```

**Implementation details**:
- Simple modulo operation
- Magic number: 20183 (as specified in problem)

---

### Step 4: Region Type and Risk Level
**File**: `solution.py`

```python
def calculate_risk_level(erosion_level):
    """
    Calculate risk level from erosion level.

    Based on erosion_level % 3:
    - 0: rocky (risk = 0)
    - 1: wet (risk = 1)
    - 2: narrow (risk = 2)

    Args:
        erosion_level: The erosion level

    Returns:
        int: Risk level (0, 1, or 2)
    """
```

**Implementation details**:
- Return erosion_level % 3 (the risk level equals the modulo result)
- **Note**: This function could be inlined since it's a simple one-liner, but keeping it separate improves code readability

---

### Step 5: Main Calculation Loop
**File**: `solution.py`

```python
def calculate_total_risk(depth, target_x, target_y):
    """
    Calculate total risk level for the rectangular region.

    Process cells row by row (y from 0 to target_y, x from 0 to target_x)
    to ensure dependencies are always satisfied.

    Args:
        depth: Cave system depth
        target_x, target_y: Target coordinates

    Returns:
        int: Total risk level
    """
```

**Implementation details**:
- Initialize 2D array for erosion_levels (size: (target_y+1) × (target_x+1))
  - **Syntax**: `erosion_levels = [[0] * (target_x + 1) for _ in range(target_y + 1)]`
  - **Access pattern**: `erosion_levels[y][x]` for coordinates (x, y)
- Initialize total_risk = 0
- **CRITICAL**: Double loop MUST be in this order - outer loop for y (0 to target_y), inner loop for x (0 to target_x)
  - **Why**: This ensures dependencies are always satisfied before they're needed
  - **WARNING**: Reversing the loop order (x outer, y inner) will cause errors due to dependency violations
- For each (x, y):
  1. Calculate geologic_index using calculate_geologic_index()
  2. Calculate erosion_level using calculate_erosion_level()
  3. Store erosion_level in the 2D structure: `erosion_levels[y][x] = erosion_level`
  4. Calculate risk_level using calculate_risk_level()
  5. Add risk_level to total_risk
- Return total_risk

**Data Structure Choice**:
- Option 1: 2D list (list of lists) - good for dense rectangular regions
- Option 2: Dictionary with (x,y) tuples as keys - more flexible
- **Recommendation**: Use 2D list for better cache locality and simpler indexing
- **Note**: We assume input file is well-formed as per AoC standards; no extensive error handling needed

---

### Step 6: Main Function
**File**: `solution.py`

```python
def main():
    """
    Main entry point for the solution.
    """
```

**Implementation details**:
- Parse input from "input.md"
- Call calculate_total_risk()
- Print the result

---

## Complete Code Structure

```
solution.py
├── parse_input(filename) -> (depth, target_x, target_y)
├── calculate_geologic_index(x, y, target_x, target_y, erosion_levels) -> int
├── calculate_erosion_level(geologic_index, depth) -> int
├── calculate_risk_level(erosion_level) -> int
├── calculate_total_risk(depth, target_x, target_y) -> int
└── main()
```

## Implementation Order

1. Write parse_input() function
2. Write calculate_erosion_level() helper (simplest, no dependencies)
3. Write calculate_risk_level() helper (simple)
4. Write calculate_geologic_index() function
5. Write calculate_total_risk() main logic with loops
6. Write main() function
7. Test with example case (depth=510, target=10,10, expected=114)
8. Run with actual input

## Optimization Considerations

**Current approach is optimal for this problem size**:
- Time: O(X × Y) = O(15 × 740) ≈ 11,000 operations - very fast
- Space: O(X × Y) for erosion level storage - acceptable
- No further optimization needed

**Alternative approaches considered**:
- Computing on-demand with memoization: Same complexity, slightly more overhead
- Space optimization: Could use only two rows instead of full 2D array (current row and previous row), but not necessary for this input size

## Constants and Magic Numbers

- `16807`: Multiplier for geologic index when Y=0 (from problem specification)
- `48271`: Multiplier for geologic index when X=0 (from problem specification)
- `20183`: Modulo value for erosion level calculation (from problem specification)
- Risk levels: 0 (rocky), 1 (wet), 2 (narrow) - correspond to erosion_level % 3

**Recommendation**: Add comments in code near these constants referencing the problem specification

## Expected Runtime

For input size 16 × 741:
- Operations: ~12,000 cells × ~5 arithmetic operations each = ~60,000 operations
- Expected runtime: < 100ms (negligible)
