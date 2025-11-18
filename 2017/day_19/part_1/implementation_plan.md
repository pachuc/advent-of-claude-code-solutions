# Implementation Plan: Network Packet Routing

## Problem Analysis

We need to trace a path through an ASCII art routing diagram, collecting letters along the way. The packet follows lines (`|`, `-`), turns at corners (`+`), and passes through letters (A-Z).

### Coordinate System Convention:
- **Grid indexing**: `grid[row][col]` where row 0 is the top, col 0 is the leftmost
- **Direction vectors**: `(delta_row, delta_col)` - row offset first, then column offset
- **Starting position**: Always in row 0 (top row), moving DOWN initially

### Key Observations:
1. The input is a large 2D grid (approximately 200 rows, very wide)
2. There is exactly one starting point (vertical `|` at top row)
3. The path is continuous with no ambiguous junctions
4. We must track direction and only turn when necessary
5. Letters are part of the path and should not cause direction changes
6. At `+` characters, we turn ONLY if we cannot continue straight
7. When paths cross, we continue straight in the current direction

### Algorithm Complexity:
- **Time Complexity**: O(W × H) where W is width and H is height
  - In the worst case, we visit each cell once
  - Path tracing is linear in path length, which is at most W × H
- **Space Complexity**: O(W × H) for storing the grid
  - Additional O(L) for collecting letters where L is number of letters

This is optimal since we must at least read the entire input once.

## Implementation Steps

### Step 0: Inspect Input File
**Goal**: Validate the input file format and understand its characteristics.

**Actions**:
- Check that input.md exists and is readable
- Verify it contains ASCII art diagram as expected
- Check for the presence of a starting `|` in the top row
- Note grid dimensions (rows and approximate width)
- Check for any unusual formatting (tabs, different line endings, etc.)

**Why this matters**:
- Validates our assumptions before implementation
- Helps identify any preprocessing needed
- Ensures the file matches problem description

### Step 1: Parse Input Grid
**Goal**: Convert the input file into a 2D grid structure that's easy to navigate.

**Approach**:
- Read the input file line by line
- Store as a list of strings (preserving exact spacing)
- Track grid dimensions (max width and height)
- Handle different line ending formats (normalize to \n)

**Implementation Details**:
```python
def parse_input(filename):
    with open(filename, 'r') as f:
        # Read entire file, which handles different line endings
        content = f.read()
        lines = content.splitlines()

    # Don't strip lines - preserve exact spacing
    # Remove completely empty lines at the end if present
    while lines and not lines[-1].strip():
        lines.pop()

    # Pad lines to same width for uniform access
    # Using spaces for padding since that's what empty grid cells are
    max_width = max(len(line) for line in lines) if lines else 0
    grid = [line.ljust(max_width) for line in lines]
    return grid
```

**Why this approach**:
- `splitlines()` handles both \n and \r\n line endings
- Preserves exact layout including trailing spaces within the diagram
- Uniform width simplifies boundary checking
- List of strings is memory-efficient and easy to index
- Removes trailing empty lines that might exist at file end

### Step 2: Find Starting Position
**Goal**: Locate the unique vertical `|` character in the top row.

**Approach**:
- Scan the first row (index 0) for `|` character
- This is the entry point where packet enters from above

**Implementation Details**:
```python
def find_start(grid):
    if not grid:
        return None
    for col, char in enumerate(grid[0]):
        if char == '|':
            return (0, col)  # (row, col)
    return None
```

**Edge Cases**:
- Empty grid (shouldn't happen per problem)
- No starting `|` found (shouldn't happen per problem)

### Step 3: Define Direction System
**Goal**: Create a consistent way to represent and manipulate directions.

**Approach**:
- Use direction vectors (delta_row, delta_col)
- Define four cardinal directions: UP, DOWN, LEFT, RIGHT
- Create helper function to get perpendicular directions

**Implementation Details**:
```python
# Direction vectors: (row_delta, col_delta)
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

def get_perpendicular(direction):
    """Get the two perpendicular directions."""
    if direction in [UP, DOWN]:
        return [LEFT, RIGHT]
    else:  # LEFT or RIGHT
        return [UP, DOWN]
```

**Why this approach**:
- Simple and efficient
- Easy to apply: `new_pos = (row + dr, col + dc)`
- Perpendicular logic is straightforward

### Step 4: Implement Path Following Logic
**Goal**: Traverse the path from start to end, collecting letters.

**Approach**:
- Start at the starting position moving DOWN
- At each step:
  1. Collect letter if current character is A-Z
  2. Try to continue in current direction
  3. If can't continue, try perpendicular directions
  4. Stop when no valid moves exist

**Implementation Details**:
```python
def is_valid_position(grid, row, col):
    """Check if position is within grid bounds."""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def is_path_char(char):
    """Check if character is part of the path.

    Valid path characters are:
    - Pipe symbols: | (vertical)
    - Dash symbols: - (horizontal)
    - Plus symbols: + (corners/junctions)
    - Uppercase letters: A-Z (markers on the path)
    """
    return char in '|-+' or (char.isupper() and char.isalpha())

def get_next_position(grid, row, col, direction):
    """Get next valid position and direction."""
    current_char = grid[row][col]

    # Try continuing in current direction first
    next_row, next_col = row + direction[0], col + direction[1]
    if is_valid_position(grid, next_row, next_col):
        next_char = grid[next_row][next_col]
        if is_path_char(next_char):
            return (next_row, next_col, direction)

    # If can't continue straight, try turning (perpendicular directions)
    # This happens at '+' or when we reach a dead end
    for new_direction in get_perpendicular(direction):
        next_row, next_col = row + new_direction[0], col + new_direction[1]
        if is_valid_position(grid, next_row, next_col):
            next_char = grid[next_row][next_col]
            if is_path_char(next_char):
                return (next_row, next_col, new_direction)

    # No valid move found - end of path
    return None

def follow_path(grid, start_row, start_col):
    """Follow the path and collect letters.

    Starting from the top of the diagram, we move DOWN onto the path.
    We collect letters as we encounter them, and stop when we reach
    the end of the path (no valid next move).

    IMPORTANT: We collect the letter at the CURRENT position BEFORE
    attempting to move to the next position. This ensures we collect
    the last letter before the path ends.
    """
    letters = []
    row, col = start_row, start_col
    direction = DOWN  # Per problem: packet starts by moving DOWN from top

    while True:
        current_char = grid[row][col]

        # Collect letter if present at current position
        if current_char.isalpha() and current_char.isupper():
            letters.append(current_char)

        # Try to move to next position
        next_move = get_next_position(grid, row, col, direction)
        if next_move is None:
            break  # End of path - no valid continuation

        row, col, direction = next_move

    return ''.join(letters)
```

**Key Decision Points**:
- **When to turn**: Only when we can't continue straight AND at a valid turning point
- **Path validation**: A character is valid if it's `|`, `-`, `+`, or uppercase letter
- **Termination**: Stop when no valid next move exists

**Why this approach**:
- Greedy forward movement matches problem description
- No backtracking needed (path is unambiguous)
- Efficient: O(path_length) time

### Step 5: Main Function
**Goal**: Orchestrate the solution from input to output.

**Implementation Details**:
```python
def main():
    grid = parse_input('input.md')
    start = find_start(grid)

    if start is None:
        print("No starting position found")
        return

    result = follow_path(grid, start[0], start[1])
    print(result)

if __name__ == "__main__":
    main()
```

## Potential Issues and Mitigations

### Issue 1: Line Width Inconsistencies
**Problem**: Input lines may have different lengths.
**Mitigation**: Pad all lines to max width during parsing.

### Issue 2: Crossing Paths and Plus Sign Behavior
**Problem**: The path might cross itself, or a `+` might appear where we can continue straight.
**Critical Rule**: Per problem description, "When lines cross: Continue straight in the current direction (don't turn)."
**Mitigation**:
- Always try to continue straight FIRST before considering turns
- Only turn when we CANNOT continue straight (dead end or `+` with no straight continuation)
- A `+` does NOT force a turn - it only indicates a possible turning point
- Example: If moving DOWN and encounter a `+` with valid path below, continue DOWN (don't turn)

**Test case needed**:
```
     |
     A
     +
     B
```
Should produce "AB" (continue straight through the `+`), NOT turn left/right.

### Issue 3: Letters on Path
**Problem**: Letters are part of the path but shouldn't affect direction.
**Mitigation**: Treat letters as valid path characters, continue straight through them.

### Issue 4: Boundary Checking
**Problem**: Accessing out-of-bounds positions.
**Mitigation**: Always validate position before accessing grid.

### Issue 5: Input File Format Variations
**Problem**: File might have Windows line endings (\r\n), tabs, or trailing whitespace.
**Mitigation**:
- Use `splitlines()` which handles different line ending formats
- Don't strip individual lines (preserve spacing within diagram)
- Remove only completely empty trailing lines at end of file
- Pad lines with spaces (not tabs) to uniform width

## Optimization Considerations

Given the input size (~200 lines, ~200 characters wide):
- **Not needed**: The grid is small enough to fit in memory
- **Path length**: Maximum ~40,000 cells, practically much smaller
- **Simple traversal**: O(n) traversal is fast enough

No special optimizations needed - straightforward implementation will be efficient.

## File Structure

```
solution.py          # Main implementation file
input.md            # Input data (provided)
implementation_plan.md  # This file
test_plan.md        # Testing plan
```

## Implementation Order

1. Parse input function
2. Find start function
3. Direction system and helpers
4. Path following logic
5. Main function
6. Test with provided example
7. Run on actual input
