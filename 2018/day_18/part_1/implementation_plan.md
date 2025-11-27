# Implementation Plan: Lumber Collection Area Simulation

## Problem Summary
Simulate a 50x50 cellular automaton grid for 10 iterations with transformation rules based on adjacent cells, then calculate resource value (trees × lumberyards).

## Algorithm Analysis

### Time Complexity
- Grid size: 50×50 = 2,500 cells
- Iterations: 10
- Per cell: Check 8 neighbors (constant time)
- **Overall: O(iterations × rows × cols) = O(10 × 50 × 50) = O(25,000)** - Very efficient

### Space Complexity
- Two grids needed (current and next state): O(2 × 50 × 50) = O(5,000) - Minimal memory usage
- **Overall: O(rows × cols)** - No scalability concerns

### Algorithm Choice
**Cellular Automaton with Double Buffering**
- Use two 2D arrays to avoid state interference during simultaneous updates
- Swap references after each iteration instead of copying data
- This is the standard approach for cellular automata and optimal for this problem size

## Step-by-Step Implementation Plan

### Step 1: Parse Input Grid
**File:** `solution.py`
**Function:** `parse_input(input_text: str) -> list[list[str]]`

- Read the input text file/string
- Split by newlines to get each row
- Convert each row into a list of characters
- Return 2D list structure: `grid[row][col]`
- Strip any trailing whitespace from each line to avoid issues

**Data Structure:**
```python
grid = [
    ['.', '|', '#', ...],  # row 0
    ['|', '#', '.', ...],  # row 1
    ...
]
```

### Step 2: Implement Neighbor Counting
**Function:** `count_neighbors(grid, row, col, target_type) -> int`

**Purpose:** Count how many of the 8 adjacent cells match a specific type

**Implementation:**
- Define 8 direction offsets: `[(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]`
- For each direction:
  - Calculate neighbor position: `(row + dr, col + dc)`
  - **Bounds checking:** Verify `0 <= new_row < 50` and `0 <= new_col < 50`
  - If valid and matches `target_type`, increment counter
- Return count

**Parameters:**
- `grid`: Current state of the grid
- `row, col`: Position to check neighbors for
- `target_type`: Character to count ('|' or '#')

### Step 3: Implement Transformation Rules
**Function:** `get_next_state(grid, row, col) -> str`

**Purpose:** Determine what a cell becomes based on current state and neighbors

**Implementation:**
```python
current = grid[row][col]

if current == '.':  # Open ground
    trees = count_neighbors(grid, row, col, '|')
    return '|' if trees >= 3 else '.'

elif current == '|':  # Trees
    lumberyards = count_neighbors(grid, row, col, '#')
    return '#' if lumberyards >= 3 else '|'

elif current == '#':  # Lumberyard
    trees = count_neighbors(grid, row, col, '|')
    lumberyards = count_neighbors(grid, row, col, '#')
    return '#' if (trees >= 1 and lumberyards >= 1) else '.'
```

**Note:** The `count_neighbors` function only counts the 8 surrounding cells and never includes the center cell itself. The lumberyard rule requires at least 1 **other** lumberyard (among the 8 neighbors) AND at least 1 tree (among the 8 neighbors) to persist.

### Step 4: Implement Single Iteration Step
**Function:** `simulate_step(grid) -> list[list[str]]`

**Purpose:** Perform one minute of simulation (simultaneous updates)

**Implementation:**
- Create new empty grid of same dimensions
- **Critical:** Use the OLD grid for all neighbor calculations
- For each cell (row, col):
  - Call `get_next_state(grid, row, col)`
  - Store result in `new_grid[row][col]`
- Return `new_grid`

**Why double buffering:**
- All transformations must use the state at the START of the minute
- If we modify in-place, later cells would see updated values from earlier cells
- This would violate the "simultaneous update" requirement

### Step 5: Implement Main Simulation Loop
**Function:** `simulate(grid, minutes=10) -> list[list[str]]`

**Implementation:**
```python
current_grid = grid
for _ in range(minutes):
    current_grid = simulate_step(current_grid)
return current_grid
```

**Note:** Creating a new grid each iteration is simple and efficient for this problem size (10 iterations × 2,500 cells).

### Step 6: Calculate Resource Value
**Function:** `calculate_resource_value(grid) -> int`

**Purpose:** Count trees and lumberyards, return their product

**Implementation:**
- Initialize `trees = 0`, `lumberyards = 0`
- Iterate through entire grid:
  - If cell == '|': increment `trees`
  - If cell == '#': increment `lumberyards`
- Return `trees * lumberyards`

**Time Complexity:** O(rows × cols) = O(2,500) - Single pass

### Step 7: Main Entry Point
**Function:** `main()`

**Implementation:**
```python
def main():
    # Read input
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse grid
    grid = parse_input(input_text)

    # Simulate 10 minutes
    final_grid = simulate(grid, minutes=10)

    # Calculate and print result
    result = calculate_resource_value(final_grid)
    print(result)

if __name__ == '__main__':
    main()
```

**Note:** The filename 'input.md' is hardcoded for simplicity. This is acceptable for a one-off script.

## Code Structure

```
solution.py
├── parse_input(input_text) -> grid
├── count_neighbors(grid, row, col, target_type) -> int
├── get_next_state(grid, row, col) -> str
├── simulate_step(grid) -> new_grid
├── simulate(grid, minutes) -> final_grid
├── calculate_resource_value(grid) -> int
└── main()
```

## Implementation Order
1. `parse_input()` - Foundation for everything
2. `count_neighbors()` - Core helper function
3. `get_next_state()` - Transformation logic
4. `simulate_step()` - Single iteration
5. `simulate()` - Full simulation
6. `calculate_resource_value()` - Final calculation
7. `main()` - Tie everything together

## Key Implementation Considerations

### Bounds Checking
- Always validate `0 <= row < 50` and `0 <= col < 50` before accessing grid
- Edge cells have fewer than 8 neighbors - this is expected and handled naturally

### Simultaneous Updates
- **Critical:** Never modify the grid in-place during an iteration
- Always read from old state, write to new state
- This is the most common bug in cellular automaton implementations

### Grid Indexing
- Use `grid[row][col]` consistently (row-major order)
- First index is Y-axis (row), second is X-axis (column)

### Performance
- No optimization needed for this problem size
- Straightforward nested loops are perfectly adequate
- Total operations: ~250,000 (trivial for modern computers)

## No Special Edge Cases
- Input is guaranteed to be 50×50
- All three transformation rules are well-defined
- No ambiguous cases in the rules
- Simple integer multiplication for final result
