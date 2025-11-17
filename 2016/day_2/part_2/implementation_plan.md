# Implementation Plan: Bathroom Keypad Code (Part 2)

## Problem Summary
Adapt the Part 1 solution to work with a diamond-shaped keypad layout instead of a rectangular 3x3 grid. The keypad has an irregular shape with valid buttons at specific positions and empty spaces elsewhere.

## Key Differences from Part 1
- **Keypad shape**: Diamond instead of rectangle
- **Button labels**: Mix of digits (1-9) and letters (A-D)
- **Validation**: Must check if a position contains a valid button, not just grid boundaries
- **Layout**:
  ```
      1
    2 3 4
  5 6 7 8 9
    A B C
      D
  ```

## Algorithm Approach

### Core Strategy
Reuse the Part 1 solution structure but modify the keypad representation and validation logic. The overall algorithm remains the same:
1. Start at position '5'
2. For each line of instructions, process each directional command
3. Move to new position if valid, otherwise stay put
4. Record the button value at the end of each line

### Runtime Complexity
- **Time**: O(n × m) where n is number of instruction lines and m is average characters per line
- **Space**: O(1) constant space (just tracking current position)
- This is optimal as we must process every instruction character

## Implementation Steps

### Step 1: Define the Diamond Keypad Layout
Create a coordinate-based mapping of the diamond-shaped keypad:

**Approach**: Use a dictionary mapping (row, col) tuples to button values
- Row 0: button '1' at column 2
- Row 1: buttons '2', '3', '4' at columns 1, 2, 3
- Row 2: buttons '5', '6', '7', '8', '9' at columns 0, 1, 2, 3, 4
- Row 3: buttons 'A', 'B', 'C' at columns 1, 2, 3
- Row 4: button 'D' at column 2

**Rationale**: A dictionary allows O(1) lookup to check if a position is valid and retrieve its button value. This is more efficient than checking boundaries on an irregular shape.

**Data structure**:
```python
keypad = {
    (0, 2): '1',
    (1, 1): '2', (1, 2): '3', (1, 3): '4',
    (2, 0): '5', (2, 1): '6', (2, 2): '7', (2, 3): '8', (2, 4): '9',
    (3, 1): 'A', (3, 2): 'B', (3, 3): 'C',
    (4, 2): 'D'
}
```

### Step 2: Modify the Movement Function
Adapt the `move()` function from Part 1:

**Coordinate System**:
We use a standard 2D coordinate system with origin at top-left:
```
       col: 0   1   2   3   4
row 0:          1
row 1:      2   3   4
row 2:  5   6   7   8   9
row 3:      A   B   C
row 4:          D
```

**Direction Mapping** (explicit):
- `U` (up): row - 1 (move up one row)
- `D` (down): row + 1 (move down one row)
- `L` (left): col - 1 (move left one column)
- `R` (right): col + 1 (move right one column)

**Changes needed**:
- Calculate new position based on direction using the mappings above
- Instead of checking rectangular bounds (0 <= row <= 2, 0 <= col <= 2), check if new position exists in keypad dictionary
- Return new position if it's a valid key in the dictionary, otherwise return current position

**Function signature**: `move(current_row, current_col, direction, keypad) -> (row, col)`

**Note**: Passing `keypad` as a parameter is a minor refactoring improvement over Part 1's hardcoded approach, making the function more testable and flexible.

### Step 3: Update Button Lookup Function
Modify `get_button_at_position()`:

**Changes needed**:
- Instead of indexing a 2D array, look up the position in the keypad dictionary
- Return the string value directly (could be digit or letter)

**Function signature**: `get_button_at_position(row, col, keypad) -> str`

**Note**: Like the move function, passing `keypad` as a parameter is a refactoring improvement over Part 1, making the code more modular.

### Step 4: Determine Starting Position
Find coordinates for button '5':

**Solution**: Button '5' is at position (2, 0) in the diamond layout

### Step 5: Adapt the Main Code Processing Logic
Reuse the `find_bathroom_code()` function from Part 1 with minimal changes:

**Changes needed**:
- Pass keypad dictionary to helper functions
- Starting position changes from (1, 1) to (2, 0)
- String concatenation remains the same (buttons are already strings)

**No changes needed**:
- Loop structure (iterate through lines, then characters)
- Code accumulation logic

### Step 6: Handle Input Reading
Reuse the input reading logic from Part 1 exactly:
- Read from 'input.md'
- Strip whitespace and skip empty lines
- No changes needed

### Step 7: Output the Result
Same as Part 1: print the accumulated code string

## Code Structure (based on Part 1)

```python
# Global or passed keypad dictionary
keypad = { ... }

def get_button_at_position(row, col, keypad):
    """Return button value at coordinates."""
    return keypad[(row, col)]

def move(current_row, current_col, direction, keypad):
    """Move if destination is valid, otherwise stay."""
    # Calculate new position
    # Check if new position in keypad
    # Return appropriate position

def find_bathroom_code(instructions, keypad):
    """Process instructions and build code."""
    row, col = 2, 0  # Start at '5'
    code = ""

    for line in instructions:
        for char in line:
            row, col = move(row, col, char, keypad)
        button = get_button_at_position(row, col, keypad)
        code += button

    return code

def main():
    """Read input and solve."""
    # Read input.md
    # Parse instructions
    # Call find_bathroom_code()
    # Print result
```

## Validation Against Example
Test with the example from problem description:
- Instructions: ULL, RRDDD, LURDL, UUUUD
- Expected output: 5DB3
- Start at (2, 0) which is '5'
- Trace through each instruction line to verify

## Edge Cases to Handle
1. **Invalid moves off diamond**: Moves to non-existent positions should be ignored
2. **Corner buttons**: Buttons 1, 5, 9, D have fewer valid moves
3. **Mixed output types**: Code contains both digits and letters (already strings, no conversion needed)

## Efficiency Considerations
- **Dictionary lookup**: O(1) for checking valid positions
- **No unnecessary iterations**: Process each character exactly once
- **Minimal memory**: Only store current position and result string
- **Input size**: 5 lines with ~200-300 characters each = ~1500 operations total (trivial)

## Testing Strategy Reference
The code should be tested with:
1. The provided example (expected: 5DB3)
2. The actual puzzle input
3. Edge cases like moves from corner buttons
