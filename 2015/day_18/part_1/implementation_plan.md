# Implementation Plan: Conway's Game of Life Variant - Light Animation

## Problem Overview
Simulate 100 steps of a cellular automaton (Conway's Game of Life variant) on a 100x100 grid and count the lights that are "on" after the simulation.

## Algorithm Analysis

### Time Complexity
- **Per Step**: O(n × m) where n=100, m=100 → O(10,000) operations
- **Total**: O(steps × n × m) = O(100 × 10,000) = O(1,000,000) operations
- This is very efficient and will run in milliseconds

### Space Complexity
- **Grid Storage**: O(n × m) = O(10,000) for the grid
- **Neighbor Counting**: We can use a boolean 2D array or similar structure
- Total space is manageable and won't cause memory issues

### Algorithm Choice
We'll use a **standard synchronous update approach**:
1. Store the current state in one grid
2. Calculate all next states based on the current state
3. Update the entire grid simultaneously
4. This ensures proper synchronous updates as required by the problem

## Implementation Steps

### Step 1: Input Parsing
**Objective**: Read and parse the grid from input file (supports any size, but our input is 100x100)

**Details**:
- Read the file line by line
- Convert each character to a boolean representation:
  - `#` → True (light is ON)
  - `.` → False (light is OFF)
- Store in a 2D list/array structure: `grid[row][col]`
  - **Coordinate System**: `grid[row][col]` where row is the first index (row-major order)
  - `grid[0][0]` is the top-left corner
  - `grid[99][99]` is the bottom-right corner (for our 100x100 input)
- Auto-detect grid size from file (count rows and columns per row)
- Validate all rows have the same length
- Validate only valid characters (`#` and `.`) are present

**Data Structure Choice**:
```python
# Use list of lists for simplicity and direct indexing
# Size is determined by the input file, not hardcoded
def parse_input(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                row = [c == '#' for c in line]
                grid.append(row)
    return grid
```

### Step 2: Neighbor Counting Function
**Objective**: Create a function to count the number of "on" neighbors for any given cell

**Function Signature**:
```python
def count_neighbors(grid, row, col):
    """Count the number of 'on' neighbors for cell at (row, col)"""
```

**Details**:
- The 8 possible neighbor offsets (including diagonals):
  - (-1, -1), (-1, 0), (-1, 1)
  - (0, -1),          (0, 1)
  - (1, -1),  (1, 0), (1, 1)
- For each offset, check:
  1. If the neighbor position is within grid bounds (0 ≤ new_row < rows, 0 ≤ new_col < cols)
  2. If the neighbor is "on" (True)
- Count and return the total number of "on" neighbors
- Edge/corner cells will naturally have fewer valid neighbors

**Implementation approach**:
- Use a loop over the 8 direction offsets
- Get grid dimensions: `rows = len(grid)`, `cols = len(grid[0])`
- Add boundary checking for each neighbor position
- Return the count

**Example**:
```python
def count_neighbors(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                count += 1
    return count
```

### Step 3: State Transition Function
**Objective**: Determine the next state of a single cell based on current state and neighbor count

**Function Signature**:
```python
def get_next_state(current_state, neighbor_count):
    """Determine next state based on current state and neighbor count"""
```

**Details**:
- Apply the transition rules:
  - **If current_state is ON (True)**:
    - Returns True if neighbor_count == 2 or neighbor_count == 3
    - Returns False otherwise
  - **If current_state is OFF (False)**:
    - Returns True if neighbor_count == 3
    - Returns False otherwise

**Implementation**:
```python
if current_state:
    return neighbor_count in [2, 3]
else:
    return neighbor_count == 3
```

### Step 4: Grid Update Function
**Objective**: Update the entire grid for one simulation step

**Function Signature**:
```python
def simulate_step(grid):
    """Perform one simulation step and return the new grid state"""
```

**Details**:
- Get grid dimensions: `rows = len(grid)`, `cols = len(grid[0])`
- Create a new grid of the same size to store the next state
- For each cell (row, col) in the current grid:
  1. Count neighbors using `count_neighbors(grid, row, col)`
  2. Get current state: `grid[row][col]`
  3. Calculate next state: `get_next_state(current_state, neighbor_count)`
  4. Store in new grid: `new_grid[row][col] = next_state`
- Return the new grid

**Critical**: We must use a separate grid for the next state to ensure all cells update based on the same current state (synchronous updates). This prevents cells that were already updated in this step from affecting the calculation of cells not yet updated.

**Example**:
```python
def simulate_step(grid):
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [[False for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            neighbor_count = count_neighbors(grid, row, col)
            current_state = grid[row][col]
            new_grid[row][col] = get_next_state(current_state, neighbor_count)

    return new_grid
```

### Step 5: Main Simulation Loop
**Objective**: Run the simulation for 100 steps

**Details**:
```python
current_grid = initial_grid
for step in range(100):
    current_grid = simulate_step(current_grid)
```

**Optimization considerations**:
- We could optimize by using numpy arrays, but given the small grid size (100x100) and number of steps (100), plain Python lists will be sufficient
- No need for early termination detection (checking for stable states or cycles) since we need exactly 100 steps

### Step 6: Count Final Lights
**Objective**: Count the number of "on" lights in the final grid

**Details**:
```python
count = sum(sum(row) for row in final_grid)
```

- Iterate through all cells in the final grid
- Count cells that are True/1
- Return the total count

### Step 7: Helper Function for Test Grids
**Objective**: Create a utility function to build grids from strings (useful for testing)

**Function Signature**:
```python
def create_grid_from_string(grid_string):
    """Create a grid from a multi-line string representation"""
```

**Details**:
- Takes a string with newlines representing the grid
- Each line becomes a row
- Each character is converted to boolean (`#` → True, `.` → False)
- Returns the grid in the same format as `parse_input`

**Example**:
```python
def create_grid_from_string(grid_string):
    lines = grid_string.strip().split('\n')
    grid = []
    for line in lines:
        row = [c == '#' for c in line]
        grid.append(row)
    return grid
```

### Step 8: Main Program Structure
**Objective**: Tie everything together

**Structure**:
```python
def main():
    # Step 1: Parse input
    grid = parse_input('input.md')

    # Step 2-5: Simulate 100 steps
    for step in range(100):
        grid = simulate_step(grid)

    # Step 6: Count and output result
    lights_on = count_lights(grid)
    print(f"Lights on after 100 steps: {lights_on}")

if __name__ == '__main__':
    main()
```

**Optional enhancements**:
- Add a progress indicator every 10 steps for user feedback
- Add a `--test` flag to run the 6x6 example first as validation
- Print initial light count for reference

## Code Organization

### Recommended File Structure
Single Python file: `solution.py`

### Function Order
1. `parse_input(filename)` - Parse the input file
2. `create_grid_from_string(grid_string)` - Helper to create grids from strings (for testing)
3. `count_neighbors(grid, row, col)` - Count neighbors for a cell
4. `get_next_state(current_state, neighbor_count)` - Determine next state
5. `simulate_step(grid)` - Perform one simulation step
6. `count_lights(grid)` - Count total "on" lights
7. `main()` - Main execution function

## Potential Optimizations (Not Required but Worth Noting)

1. **NumPy Arrays**: Could use numpy for faster array operations, but overhead may not be worth it for this size
2. **Sparse Representation**: If most lights are off, could track only "on" cells, but with 100x100 grid, this is unnecessary
3. **Early Termination**: Could detect stable states or cycles, but problem requires exactly 100 steps
4. **Pre-allocate Grids**: Reuse two grid buffers and swap between them instead of allocating new grid each step (minor optimization)

## Expected Runtime
- With Python lists: < 100ms
- The algorithm is highly efficient for this problem size

## Key Implementation Requirements for Testing

The implementation MUST support:
1. **Variable grid sizes**: Functions should work with any rectangular grid, not just 100x100
2. **Grid creation from strings**: The `create_grid_from_string` helper enables easy test case creation
3. **Intermediate state access**: Return the grid after each step so tests can inspect intermediate states
4. **Deterministic output**: No randomness - same input always produces same output

This design allows us to:
- Test the 6x6 example from the problem statement
- Create small test cases for manual verification
- Verify each component independently before running on the full 100x100 input
