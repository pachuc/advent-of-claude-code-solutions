# Implementation Plan: Light Grid Control System

## Problem Summary
Process 300 instructions to control a 1000x1000 grid of lights (1 million lights total). Each instruction can turn on, turn off, or toggle lights in a rectangular region. Count the total number of lights that are ON after all instructions are executed.

## Algorithm Analysis

### Data Structure Selection
**Grid Representation Options:**
1. **2D List/Array**: `[[False] * 1000 for _ in range(1000)]`
   - Memory: ~1MB (1 byte per boolean in Python)
   - Access time: O(1)
   - Simple and intuitive

2. **1D Array**: `[False] * 1000000` with index calculation `row * 1000 + col`
   - Memory: ~1MB
   - Access time: O(1)
   - Slightly faster due to better cache locality

3. **Set of ON coordinates**: `set()` storing only (x, y) of ON lights
   - Memory: Variable, worst case ~24MB (set overhead per tuple)
   - Best for sparse grids (few lights ON)
   - Given the input has many large rectangular regions being turned on, this is suboptimal

**Decision**: Use a **1D NumPy boolean array** or native Python list for optimal performance and memory efficiency.

### Time Complexity Analysis
- **Input parsing**: O(N) where N = 300 instructions
- **Grid operations**: For each instruction affecting rectangle (x1,y1) to (x2,y2):
  - Width × Height operations: O(W × H)
  - Worst case per instruction: O(1000 × 1000) = O(1,000,000)
- **Total worst case**: O(N × 1,000,000) = O(300,000,000) operations
- **Counting final lights**: O(1,000,000)

**Optimization consideration**: Python loops are slow. Using NumPy for rectangular operations would be significantly faster, but adds a dependency. For this problem, native Python with efficient iteration should suffice.

### Space Complexity
- Grid storage: O(1,000,000) = O(1M) bits ~ 125KB minimum
- Python boolean array: ~1MB
- No additional space needed beyond the grid

## Implementation Steps

### Step 1: Input Parsing Function
**Function**: `parse_instruction(line: str) -> tuple`
- **Purpose**: Extract command type and coordinates from instruction string
- **Implementation**:
  1. Strip whitespace from line
  2. Identify command type:
     - Check if line starts with "turn on"
     - Check if line starts with "turn off"
     - Otherwise, it's "toggle"
  3. Extract coordinate substring (after command, between "through")
  4. Parse coordinates using split and int conversion
  5. Return: `(command, x1, y1, x2, y2)`

**Coordinate System Convention**:
- First coordinate (before comma) = column (x-coordinate, horizontal position)
- Second coordinate (after comma) = row (y-coordinate, vertical position)
- Grid indexing: `row * 1000 + column` (row-major order)
- Example: coordinate "5,10" means column 5, row 10 → grid index = 10 * 1000 + 5

**Parsing Strategy**:
```python
def parse_instruction(line):
    line = line.strip()

    # Determine command type
    if line.startswith('turn on'):
        command = 'on'
        coords_part = line[8:]  # Skip "turn on "
    elif line.startswith('turn off'):
        command = 'off'
        coords_part = line[9:]  # Skip "turn off "
    elif line.startswith('toggle'):
        command = 'toggle'
        coords_part = line[7:]  # Skip "toggle "

    # Parse coordinates: "col1,row1 through col2,row2"
    start, end = coords_part.split(' through ')
    col1, row1 = map(int, start.split(','))
    col2, row2 = map(int, end.split(','))

    return command, col1, row1, col2, row2
```

### Step 2: Grid Initialization
**Function**: `initialize_grid() -> list`
- **Purpose**: Create 1000×1000 grid with all lights OFF
- **Implementation**:
  - Use list comprehension or NumPy
  - Option 1 (Native): `grid = [False] * 1000000`
  - Option 2 (NumPy): `grid = np.zeros((1000, 1000), dtype=bool)`

**Decision**: Start with native Python for simplicity. Can optimize with NumPy if performance is insufficient.

### Step 3: Command Application Functions

**CRITICAL**: Ensure correct coordinate-to-index mapping:
- Coordinates are (column, row)
- Grid index = `row * 1000 + column`

**Implementation approach**: Single dispatcher function for simplicity.

```python
def apply_instruction(grid, command, col1, row1, col2, row2):
    """Apply instruction to grid region.

    Args:
        grid: 1D list representing 1000x1000 grid
        command: 'on', 'off', or 'toggle'
        col1, row1: Top-left corner (inclusive)
        col2, row2: Bottom-right corner (inclusive)
    """
    for row in range(row1, row2 + 1):  # Inclusive range
        for col in range(col1, col2 + 1):
            idx = row * 1000 + col  # CORRECT: row-major indexing
            if command == 'on':
                grid[idx] = True
            elif command == 'off':
                grid[idx] = False
            elif command == 'toggle':
                grid[idx] = not grid[idx]
```

**Note**: Using explicit `col` and `row` naming to avoid x/y ambiguity.

### Step 4: Main Processing Loop
**Function**: `process_instructions(filename: str) -> int`
- **Purpose**: Read file, process all instructions, return count
- **Implementation**:
  1. Initialize grid
  2. Open input file
  3. For each line in file:
     - Skip empty lines
     - Parse instruction
     - Apply command to grid
  4. Count True values in grid
  5. Return count

```python
def process_instructions(filename):
    grid = [False] * 1000000

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            command, col1, row1, col2, row2 = parse_instruction(line)
            apply_instruction(grid, command, col1, row1, col2, row2)

    return sum(grid)  # Count True values
```

### Step 5: Count Final Lights
**Implementation**: Use Python's built-in `sum()` on boolean list
- `sum(grid)` works because `True == 1` and `False == 0` in Python
- Time complexity: O(1,000,000)
- Efficient and idiomatic

### Step 6: Main Entry Point
```python
def main():
    result = process_instructions('input.md')
    print(result)

if __name__ == '__main__':
    main()
```

## Code Structure

```
solution.py
├── parse_instruction(line: str) -> tuple
│   └── Extracts command and coordinates from instruction string
│   └── Returns: (command, col1, row1, col2, row2)
├── apply_instruction(grid: list, command: str, col1: int, row1: int, col2: int, row2: int) -> None
│   └── Applies a single instruction to the grid
│   └── Uses row-major indexing: idx = row * 1000 + col
├── process_instructions(filename: str) -> int
│   └── Main processing function: reads file, applies all instructions, counts lights
└── main()
    └── Entry point: calls process_instructions and prints result
```

## Optimization Considerations

### If Performance is Insufficient:
1. **Use NumPy for rectangular slicing** (vectorized operations):
   ```python
   import numpy as np
   grid = np.zeros((1000, 1000), dtype=bool)
   grid[x1:x2+1, y1:y2+1] = True  # Much faster than nested loops
   ```

2. **Use array.array for boolean storage** (more memory efficient):
   ```python
   from array import array
   grid = array('B', [0] * 1000000)  # Unsigned char array
   ```

3. **Parallelize instruction processing** (only if order-independent, which it isn't here)

### Current Approach Justification:
- Native Python is sufficient for 300 instructions × ~100K avg operations
- Expected runtime: 30-60 seconds on modern hardware (Python nested loops are slow)
- If runtime > 60s, switch to NumPy for vectorized operations
- Simpler code, no external dependencies
- Easy to debug and test

## Edge Cases Handled
1. **Single light**: Rectangles where x1==x2 and y1==y2
2. **Full grid**: Operations on entire 1000×1000 grid
3. **Overlapping instructions**: Later instructions override earlier ones (handled by sequential processing)
4. **Toggle on already-toggled lights**: Correctly flips state
5. **Empty input**: Returns 0 (all lights OFF)

## Expected Output Format
Single integer printed to stdout representing the count of lights that are ON.
