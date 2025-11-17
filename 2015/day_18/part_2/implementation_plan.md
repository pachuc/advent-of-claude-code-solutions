# Implementation Plan: Conway's Game of Life with Stuck Corners

## Problem Analysis

We need to simulate Conway's Game of Life for 100 steps on a 100x100 grid where the four corner lights are permanently stuck in the ON state. The goal is to count how many lights are ON after 100 iterations.

### Key Constraints:
- Grid size: 100x100 (10,000 cells)
- Iterations: 100 steps
- Special rule: Corner lights at (0,0), (0,99), (99,0), and (99,99) are always ON
- Input size: Relatively small (10,000 cells), so performance is not critical

### Algorithm Complexity:
- Time complexity per iteration: O(n × m) where n=m=100, so O(10,000) per step
- Total time: O(100 × 10,000) = O(1,000,000) operations - very manageable
- Space complexity: O(n × m) = O(10,000) for storing the grid

## Implementation Steps

### Step 1: Input Parsing
**Objective:** Read and parse the input grid from the file

**Details:**
- Read from the file 'input.md' (hardcoded path in same directory as script)
- Read the input file line by line
- Convert each line to a list/array representation
- Map '#' to True/1 (ON) and '.' to False/0 (OFF)
- Store as a 2D list: `grid[row][col]`
- Strip whitespace/newlines from each line
- Basic validation: Check that result has 100 rows and each row has 100 columns

**Data Structure Choice:**
- Use a 2D list of booleans: `grid[row][col]` where True = ON, False = OFF
- Python's True/False can be summed directly (True == 1, False == 0)

**Error Handling:**
- If file not found or dimensions wrong, print error message and exit
- This is a script, not production code, so basic error handling is sufficient

### Step 2: Initialize Corner Lights
**Objective:** Ensure all four corners are set to ON in the initial state

**Details:**
- Set grid[0][0] = True (top-left)
- Set grid[0][99] = True (top-right)
- Set grid[99][0] = True (bottom-left)
- Set grid[99][99] = True (bottom-right)

**Why:** The problem states corners must be forced ON before starting simulation

### Step 3: Implement Neighbor Counting Function
**Objective:** Create a function to count ON neighbors for any cell

**Function Signature:**
```python
def count_neighbors(grid, row, col) -> int
```

**Algorithm:**
- Define 8 directions: (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)
- For each direction, check if neighbor position is within bounds
- If valid and neighbor is ON, increment counter
- Return total count
- **Important**: Do NOT count the cell itself, only the 8 surrounding positions

**Edge Cases:**
- Corner cells: Only 3 valid neighbor positions (other 5 are out of bounds)
- Edge cells: Only 5 valid neighbor positions
- Interior cells: All 8 neighbor positions are valid
- Must handle boundary checking carefully: 0 <= neighbor_row < 100 and 0 <= neighbor_col < 100

### Step 4: Implement Single Step Simulation
**Objective:** Apply Conway's Game of Life rules for one iteration

**Function Signature:**
```python
def simulate_step(grid) -> new_grid
```

**Algorithm:**
1. Create a new grid (same dimensions) to store next state
2. For each cell (row, col) in the grid:
   - Count its ON neighbors using count_neighbors()
   - Apply standard Conway's rules (even to corners initially):
     - If cell is ON: stays ON if neighbors == 2 or 3, else turns OFF
     - If cell is OFF: turns ON if neighbors == 3, else stays OFF
   - Set new_grid[row][col] to computed state
3. **AFTER all cells are computed**, force corners to ON in the new grid:
   - new_grid[0][0] = True
   - new_grid[0][99] = True
   - new_grid[99][0] = True
   - new_grid[99][99] = True
4. Return new_grid (do NOT modify the original grid)

**Important:**
- Must evaluate ALL cells based on the CURRENT state (read from old grid, write to new grid)
- This ensures simultaneous updates as required by Conway's rules
- Corner forcing happens AFTER applying rules to all cells, including corners
- The function creates and returns a NEW grid; it does NOT modify the input grid in-place

### Step 5: Main Simulation Loop
**Objective:** Run 100 iterations of the simulation

**Algorithm:**
1. Load and parse input grid
2. Force initial corner lights to ON (before first iteration)
3. Loop 100 times:
   - grid = simulate_step(grid)
   - Note: simulate_step() internally forces corners after applying rules
4. Count total ON lights in final grid
5. Return/print the count

**Implementation:**
```python
# After parsing
force_corners_on(grid)

# Run simulation
for step in range(100):
    grid = simulate_step(grid)  # Returns new grid with corners forced
```

**Timing of Corner Forcing:**
- **Once BEFORE the loop**: Force corners on the initial parsed state
- **Within each iteration**: simulate_step() forces corners AFTER applying Conway's rules
- This ensures corners are always ON at the start and end of each step

### Step 6: Count Final ON Lights
**Objective:** Count how many lights are ON after 100 steps

**Algorithm:**
- Iterate through entire grid
- Count cells where value is True/ON
- Return count

**Implementation:**
```python
total_on = sum(sum(row) for row in grid)
```
(if using boolean/integer values where True=1)

### Step 7: Output Result
**Objective:** Print the final count

**Details:**
- Print single integer: the count of ON lights
- No additional formatting needed

## Code Structure

```python
def parse_input(filename):
    """Read grid from file and convert to 2D boolean array"""
    pass

def count_neighbors(grid, row, col):
    """Count ON neighbors for cell at (row, col)"""
    pass

def simulate_step(grid):
    """Execute one step of Conway's Game of Life with corner constraint
    Returns a NEW grid; does not modify input grid"""
    pass

def force_corners_on(grid):
    """Set all four corner lights to ON (modifies grid in-place)"""
    pass

def count_on_lights(grid):
    """Count total ON lights in grid"""
    pass

def main():
    # Parse input
    grid = parse_input('input.md')

    # Initialize corners
    force_corners_on(grid)

    # Run 100 iterations
    for step in range(100):
        grid = simulate_step(grid)

    # Count and output result
    result = count_on_lights(grid)
    print(result)

if __name__ == "__main__":
    main()
```

## Optimization Considerations

Given the small input size (100×100 grid, 100 iterations), optimization is not critical. However, some considerations:

1. **No optimization needed:** 1M operations complete in milliseconds
2. **Data structure:** Plain 2D list is sufficient; numpy would work but adds dependency
3. **In-place vs copy:** Creating new grid each step is cleaner and avoids bugs
4. **Pre-compute directions:** Store direction offsets to avoid recreating each time

## Potential Pitfalls to Avoid

1. **Simultaneous updates:** Must read from old state, write to new state (not in-place)
   - Create a NEW grid in simulate_step(), don't modify the input grid
2. **Corner forcing timing:** Must force corners AFTER applying rules
   - Within simulate_step(): apply rules first, THEN force corners on the new grid
   - Before simulation loop: force corners on initial state
3. **Boundary checking:** Must verify neighbor coordinates are within [0, 99] range
   - Use: `0 <= neighbor_row < 100 and 0 <= neighbor_col < 100`
4. **Off-by-one errors:** Grid indices are 0-99, not 1-100
   - Corners are at (0,0), (0,99), (99,0), (99,99) NOT (1,1), (100,100), etc.
5. **Neighbor counting:** Don't count the cell itself as its own neighbor
6. **Initial state:** Don't forget to force corners ON before first iteration
