# Implementation Plan: Light Grid Brightness Control

## Problem Summary
Calculate the total brightness of a 1000x1000 grid of lights after executing a series of instructions. Each light starts at brightness 0, and instructions modify brightness levels within rectangular regions.

## Algorithm Analysis

### Input Characteristics
- Grid size: 1000x1000 = 1,000,000 lights
- Input: 300 instructions (as observed in input.md)
- Each instruction affects a rectangular region
- Worst case: single instruction affects entire grid (1,000,000 operations)
- Total operations: ~300 instructions × average region size

### Time Complexity Considerations
- **Direct simulation approach**: O(N × R) where N = number of instructions, R = average region size
  - With 300 instructions and average regions of ~100,000 lights: ~30,000,000 operations
  - This is acceptable for modern hardware (well under 1 second)
- **Memory**: O(1,000,000) = ~8MB for integer array (using int or long)
- **Alternative optimizations**: Could use event-based processing or coordinate compression, but unnecessary for this problem size

### Chosen Approach: Direct Simulation
Direct grid manipulation is optimal because:
1. Simple to implement and debug
2. Performance is acceptable (~30M operations is fast in Python with NumPy or even lists)
3. No complex data structures needed
4. Memory footprint is reasonable

## Implementation Steps

### Step 1: Parse Input Instructions
**Goal**: Convert text instructions into structured data

**Approach**:
- Read all lines from input file
- Use regular expressions to extract:
  - Command type: "turn on", "turn off", or "toggle"
  - Start coordinates: (x1, y1)
  - End coordinates: (x2, y2)
- Store as list of tuples: `[(command, x1, y1, x2, y2), ...]`

**Implementation details**:
```python
import re

def parse_instruction(line):
    # Pattern: (turn on|turn off|toggle) X1,Y1 through X2,Y2
    pattern = r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)'
    match = re.match(pattern, line.strip())
    if match:
        command = match.group(1)
        x1, y1, x2, y2 = map(int, [match.group(2), match.group(3),
                                    match.group(4), match.group(5)])
        return (command, x1, y1, x2, y2)
    return None
```

**Note on coordinate system**: The input format is `X,Y` where X is horizontal (column) and Y is vertical (row). In Python 2D lists, `grid[row][column]` means we should access as `grid[y][x]` to maintain correct coordinate mapping.

### Step 2: Initialize Grid
**Goal**: Create data structure to represent 1000x1000 grid

**Options**:
- **Option A**: 2D list `[[0]*1000 for _ in range(1000)]`
  - Pro: Native Python, no dependencies
  - Con: Slower for bulk operations
- **Option B**: NumPy array `numpy.zeros((1000, 1000), dtype=int)`
  - Pro: Faster for large operations
  - Con: Requires NumPy dependency
- **Option C**: 1D list with index calculation `[0] * 1_000_000`
  - Pro: Simpler memory layout, cache-friendly
  - Con: Need to calculate indices

**Chosen**: Option A (2D list) for simplicity and no external dependencies
- Performance is acceptable for this problem size
- More readable: `grid[x][y]` vs `grid[x * 1000 + y]`

**Implementation**:
```python
def initialize_grid():
    # Create 1000 rows x 1000 columns grid
    # Access pattern: grid[row][column] = grid[y][x]
    return [[0] * 1000 for _ in range(1000)]
```

### Step 3: Process Instructions
**Goal**: Apply each instruction to the grid in sequence

**Approach**:
- Iterate through parsed instructions in order
- For each instruction:
  - Identify the rectangular region (x1,y1) to (x2,y2) inclusive
  - Apply the appropriate operation to each light in the region
  - Operations:
    - "turn on": brightness += 1
    - "turn off": brightness -= 1 (minimum 0)
    - "toggle": brightness += 2

**Implementation details**:
```python
def process_instruction(grid, command, x1, y1, x2, y2):
    # Input coordinates are (X,Y) where X=column, Y=row
    # Grid access is grid[row][column] = grid[y][x]
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if command == "turn on":
                grid[y][x] += 1
            elif command == "turn off":
                grid[y][x] = max(0, grid[y][x] - 1)
            elif command == "toggle":
                grid[y][x] += 2
```

**Note on boundaries**: Both start and end coordinates are inclusive, hence `range(x1, x2 + 1)`

**CRITICAL: Coordinate System Convention**
- Input format: `X,Y` where X is horizontal (column), Y is vertical (row)
- Grid indexing: `grid[row][column]` following Python convention
- Therefore: **Always access as `grid[y][x]`** not `grid[x][y]`

### Step 4: Calculate Total Brightness
**Goal**: Sum all brightness values in the grid

**Approach**:
- Iterate through entire grid
- Accumulate sum of all brightness values
- Return final total

**Implementation**:
```python
def calculate_total_brightness(grid):
    total = 0
    for row in grid:
        total += sum(row)
    return total

# Alternative one-liner:
# return sum(sum(row) for row in grid)
```

### Step 5: Main Program Flow
**Goal**: Orchestrate all steps to produce final answer

**Structure**:
```python
def main():
    # 1. Read and parse input
    instructions = []
    with open('input.md', 'r') as f:
        for line in f:
            parsed = parse_instruction(line)
            if parsed:
                instructions.append(parsed)

    # 2. Initialize grid
    grid = initialize_grid()

    # 3. Process all instructions
    for command, x1, y1, x2, y2 in instructions:
        process_instruction(grid, command, x1, y1, x2, y2)

    # 4. Calculate and output result
    total_brightness = calculate_total_brightness(grid)
    print(total_brightness)

if __name__ == "__main__":
    main()
```

**Note**: Input file 'input.md' is hardcoded as this is a one-off script for a specific problem. For more flexibility, this could be made a command-line argument.

### Step 6: Verification and Sanity Checks
**Goal**: Ensure the solution produces reasonable output

**Checks to perform**:
1. Output should be a positive integer
2. Output should be in the millions range (based on 300 instructions affecting 1000x1000 grid)
3. No brightness values should be negative in final grid
4. Number of parsed instructions should match input line count (300)

**Implementation note**: For debugging, can add:
```python
# Sanity check: no negative brightness
min_brightness = min(min(row) for row in grid)
assert min_brightness >= 0, f"Found negative brightness: {min_brightness}"
```

## Code Structure

### File: solution.py
```
Imports:
- re (for regex parsing)

Functions:
1. parse_instruction(line) -> tuple or None
2. initialize_grid() -> list[list[int]]
3. process_instruction(grid, command, x1, y1, x2, y2) -> None (modifies grid)
4. calculate_total_brightness(grid) -> int
5. main() -> None

Entry point:
- if __name__ == "__main__": main()
```

## Performance Optimization Considerations

### Current Approach Performance
- Expected runtime: < 1 second for 300 instructions
- Memory: ~8MB for grid
- No optimization needed for correctness

### Potential Optimizations (if needed)
1. **NumPy arrays**: 10-100x faster for array operations
2. **Coordinate compression**: Track only modified regions
3. **Event-based processing**: Record changes as events, compute final state
4. **Sparse representation**: Only store non-zero brightness values

**Decision**: Stick with simple approach unless runtime exceeds 10 seconds

## Edge Cases to Handle
1. **Brightness floor**: Ensure brightness never goes below 0 with `max(0, value - 1)`
2. **Inclusive boundaries**: Use `range(x1, x2 + 1)` to include both endpoints
3. **Empty lines**: Skip lines that don't match the pattern
4. **Order dependency**: Process instructions sequentially (not in parallel)
5. **Coordinate system**: Always use `grid[y][x]` not `grid[x][y]` to match X=column, Y=row convention

## Error Handling Strategy
For this script-based solution, the approach is:
1. **File not found**: Let Python raise FileNotFoundError - acceptable for one-off script
2. **Invalid instruction format**: `parse_instruction()` returns `None`, which we skip silently
3. **Out-of-range coordinates**: Not expected in valid input; would cause IndexError if present
4. **Empty file**: Would result in 0 total brightness (correct behavior)

These are intentional design choices for a simple problem-solving script, not production code.

## Expected Output
- Single integer representing total brightness
- For the given input, expect a value in the range of millions (based on problem scale)
