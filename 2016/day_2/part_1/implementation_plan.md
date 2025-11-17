# Implementation Plan: Bathroom Keypad Code

## Problem Analysis
- Navigate a 3x3 numeric keypad using directional instructions (U/D/L/R)
- Start at position 5 (center of keypad)
- Each line of instructions produces one digit of the final code
- Invalid moves (off the grid) are ignored
- Position persists between instruction lines

## Algorithm Analysis
**Time Complexity**: O(n × m) where n = number of instruction lines, m = average length of each line
**Space Complexity**: O(1) - only tracking current position
**Efficiency**: Highly efficient - linear time, constant space. Input size doesn't matter.

## Implementation Steps

### Step 1: Define the Keypad Structure
Create a representation of the 3x3 keypad that allows:
- Easy position tracking (row, column coordinates)
- Simple validation of moves
- Efficient lookup of the button value at any position

**Approach**: Use coordinate-based positioning with 0-indexed coordinates:
```
Position (0,0) = 1, (0,1) = 2, (0,2) = 3
Position (1,0) = 4, (1,1) = 5, (1,2) = 6
Position (2,0) = 7, (2,1) = 8, (2,2) = 9
```

**Implementation Options**:
1. **2D Array** (explicit): `keypad = [[1,2,3], [4,5,6], [7,8,9]]` - access via `keypad[row][col]`
2. **Computed Formula**: `button = row * 3 + col + 1` - simpler, no data structure needed

Either approach is acceptable. The computed formula is slightly more elegant for a 3×3 grid.

### Step 2: Initialize Starting Position
- Start at button 5, which corresponds to position (1, 1) in 0-indexed coordinates
- Store current position as (row, col) tuple or separate variables

### Step 3: Create Movement Logic
Define a function/method to process each directional command:
- U (Up): row -= 1
- D (Down): row += 1
- L (Left): col -= 1
- R (Right): col += 1

**Boundary Validation**:
- Before applying any move, check if new position would be valid (0 <= row <= 2, 0 <= col <= 2)
- Only update position if the move is valid
- Otherwise, stay at current position

### Step 4: Process Instructions Line by Line
For each line of instructions:
1. Iterate through each character in the line
2. For each direction character, attempt to move
3. Apply boundary validation
4. Update position only if move is valid
5. After processing all characters in the line, record the current button value
6. Continue to next line with position unchanged (persistent state)

### Step 5: Build the Output Code
- Maintain a list or string to accumulate the digits
- After processing each line, append the current button value to the result
- Return the final code as a string

### Step 6: Read Input and Execute
1. Read all instruction lines from input file (read from "input.md")
2. Strip whitespace/newlines from each line
3. **Empty line handling**: Skip completely empty lines (they do not produce a digit)
4. Process each non-empty line through the main processing function
5. Output the resulting code to stdout as a single line

**Input Assumptions**:
- Direction characters are uppercase (U, D, L, R)
- Input is well-formed (only contains valid direction characters)
- No additional validation needed for invalid characters
- Input file path is "input.md" in the current directory

## Code Structure

```
Function: get_button_at_position(row, col)
- Input: row, col coordinates
- Output: button value (1-9)
- Logic: return keypad[row][col]

Function: move(current_row, current_col, direction)
- Input: current position and direction character
- Output: new position (row, col)
- Logic:
  - Calculate tentative new position based on direction
  - Validate new position (0 <= row <= 2 and 0 <= col <= 2)
  - Return new position if valid, else return current position unchanged

Note: Boundary validation is integrated into the move function for simplicity.

Function: find_bathroom_code(instructions)
- Input: list of instruction lines
- Output: string representing the bathroom code
- Logic:
  - Initialize position at (1, 1) for button 5
  - For each line in instructions:
    - For each character in line:
      - Update position using move()
    - Append button value to result
  - Return result string

Main execution:
- Read input file ("input.md")
- Parse into list of instruction lines (strip whitespace, skip empty lines)
- Call find_bathroom_code()
- Print result to stdout (single line output)
```

## Implementation Notes
- Use simple data structures (2D list for keypad, tuple/variables for position)
- No need for complex classes or abstractions for this script
- Input validation is minimal - assume well-formed input
- Focus on clarity and correctness over optimization (already O(n×m) which is optimal)
