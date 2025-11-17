# Implementation Plan: LCD Screen Pixel Display Simulation

## Updates Based on Critique

This plan has been updated to address the following issues from the critique:

1. **Specific input handling**: Clarified reading from `input.md` with regex parsing
2. **Committed parsing approach**: Using regex for robustness (not string split)
3. **Rotation direction examples**: Added explicit examples showing RIGHT and DOWN rotations
4. **Display function**: Added for visual verification (important for Advent of Code)
5. **Output format**: Specified exact format (just the integer, no extra text)
6. **Basic validation**: Added assertions for bounds checking

## Problem Analysis

We need to simulate a 50x6 pixel LCD screen that processes a series of instructions to light up pixels. The three operations are:
1. **rect AxB**: Turn on pixels in an AxB rectangle at top-left
2. **rotate row y=A by B**: Rotate row A right by B positions (with wrapping)
3. **rotate column x=A by B**: Rotate column A down by B positions (with wrapping)

**Input size**: 194 instructions
**Screen size**: 50 pixels × 6 pixels = 300 total pixels

### Algorithm Efficiency Considerations
- The screen size is small (300 pixels), so efficiency is not a major concern
- Each operation is O(1) or O(screen_width) or O(screen_height), all very fast
- Total time complexity: O(n × max(width, height)) where n = number of instructions (~194)
- This is perfectly reasonable and will execute instantly

## Step-by-Step Implementation Plan

### Step 1: Initialize the Screen Data Structure
- Create a 2D array/list to represent the screen: 6 rows × 50 columns
- Initialize all pixels to `False` (OFF state) or 0
- Choice: Use a list of lists: `screen[row][col]`
- This provides O(1) access time for any pixel

### Step 2: Read and Parse Input Instructions
**Input file**: `input.md` - contains one instruction per line (ignore markdown formatting if present)

**Parsing approach**: Use regular expressions for robust pattern matching
- Define three regex patterns:
  - Rectangle: `r"rect (\d+)x(\d+)"` → captures width and height
  - Row rotation: `r"rotate row y=(\d+) by (\d+)"` → captures row index and shift amount
  - Column rotation: `r"rotate column x=(\d+) by (\d+)"` → captures column index and shift amount

**Implementation**:
```python
import re

rect_pattern = re.compile(r"rect (\d+)x(\d+)")
row_pattern = re.compile(r"rotate row y=(\d+) by (\d+)")
col_pattern = re.compile(r"rotate column x=(\d+) by (\d+)")

# For each line:
# - Try matching against each pattern
# - Extract integer values from matched groups
# - Store as structured instruction (type, param1, param2)
```

**Basic validation** (to catch implementation errors):
- Assert row index < 6 (screen height)
- Assert column index < 50 (screen width)
- Assert rect dimensions are positive

### Step 3: Implement Rectangle Operation
**Function**: `rect(screen, width, height)`
- Parameters:
  - `screen`: 2D array representing the display
  - `width`: Number of columns (A)
  - `height`: Number of rows (B)
- Logic:
  - Iterate through rows 0 to height-1
  - For each row, iterate through columns 0 to width-1
  - Set `screen[row][col] = True` (turn pixel ON)
- Time complexity: O(width × height)

### Step 4: Implement Row Rotation Operation
**Function**: `rotate_row(screen, row_index, shift_amount)`
- Parameters:
  - `screen`: 2D array
  - `row_index`: Which row to rotate (A)
  - `shift_amount`: How many positions to shift RIGHT (B)
- Logic:
  - Extract the entire row: `row = screen[row_index]`
  - Normalize shift amount: `shift_amount = shift_amount % len(row)` (handles shifts larger than width)
  - Perform circular rotation to the RIGHT:
    - **Use list slicing**: `rotated = row[-shift_amount:] + row[:-shift_amount]`
    - **How this works**:
      - `row[-shift_amount:]` takes last N elements (these wrap to the front)
      - `row[:-shift_amount]` takes all but last N elements (these shift right)
      - Example: `[1,2,3,4,5]` rotated right by 2 → `[4,5,1,2,3]`
  - Replace the row in screen: `screen[row_index] = rotated`
- Time complexity: O(screen_width) = O(50)

### Step 5: Implement Column Rotation Operation
**Function**: `rotate_column(screen, col_index, shift_amount)`
- Parameters:
  - `screen`: 2D array
  - `col_index`: Which column to rotate (A)
  - `shift_amount`: How many positions to shift DOWN (B)
- Logic:
  - Extract the entire column: `column = [screen[row][col_index] for row in range(len(screen))]`
  - Normalize shift amount: `shift_amount = shift_amount % len(column)`
  - Perform circular rotation DOWNWARD:
    - **Use list slicing**: `rotated = column[-shift_amount:] + column[:-shift_amount]`
    - **How this works**: Same as row rotation, but applied vertically
      - `column[-shift_amount:]` takes bottom N elements (these wrap to the top)
      - `column[:-shift_amount]` takes all but bottom N elements (these shift down)
      - Example: `[1,2,3,4,5,6]` rotated down by 2 → `[5,6,1,2,3,4]`
  - Replace the column values in screen:
    - `for row in range(len(screen)): screen[row][col_index] = rotated[row]`
- Time complexity: O(screen_height) = O(6)

### Step 6: Process All Instructions Sequentially
**Function**: `process_instructions(screen, instructions)`
- For each instruction in order:
  - Parse the instruction to determine type and parameters
  - Call the appropriate function:
    - If "rect": call `rect(screen, width, height)`
    - If "rotate row": call `rotate_row(screen, row_index, shift_amount)`
    - If "rotate column": call `rotate_column(screen, col_index, shift_amount)`
  - The screen is modified in-place, maintaining state between operations

### Step 7: Count Lit Pixels
**Function**: `count_lit_pixels(screen)`
- Iterate through all rows and columns
- Count pixels where value is `True` (or 1)
- Return the total count
- Implementation options:
  - Nested loop with counter
  - List comprehension with sum: `sum(sum(row) for row in screen)`
- Time complexity: O(width × height) = O(300)

### Step 8: Add Display Function (for debugging/verification)
**Function**: `display_screen(screen)`
- Print the screen in a readable format
- Use '#' for ON pixels, '.' for OFF pixels
- This helps verify the solution visually (Advent of Code problems often spell letters)
- Implementation:
  ```python
  def display_screen(screen):
      for row in screen:
          print(''.join('#' if pixel else '.' for pixel in row))
  ```

### Step 9: Main Program Flow
```
1. Initialize 6×50 screen with all pixels OFF
2. Read input file (input.md)
3. Parse all instructions into a list using regex patterns
4. Process each instruction sequentially
5. Count total lit pixels
6. Print the result as a single integer (for answer submission)
7. Optionally: Display the screen visually for verification
```

**Output format**: Print only the integer count on a single line
- Example: `121` (not "The answer is 121" or other formatting)
- This allows easy copy-paste for answer submission

## Data Structure Summary
- **Screen**: `List[List[bool]]` - 6 rows × 50 columns
  - Alternative: `List[List[int]]` using 0/1 for OFF/ON
- **Instructions**: `List[str]` - raw instruction strings

## Parsing Strategy (Detailed)
**Chosen approach**: Regular expressions (for robustness and clarity)

```python
import re

# Compile patterns once for efficiency
rect_pattern = re.compile(r"rect (\d+)x(\d+)")
row_pattern = re.compile(r"rotate row y=(\d+) by (\d+)")
col_pattern = re.compile(r"rotate column x=(\d+) by (\d+)")

# Parse each line
for line in input_lines:
    line = line.strip()

    if match := rect_pattern.match(line):
        width, height = int(match.group(1)), int(match.group(2))
        rect(screen, width, height)

    elif match := row_pattern.match(line):
        row_idx, shift = int(match.group(1)), int(match.group(2))
        rotate_row(screen, row_idx, shift)

    elif match := col_pattern.match(line):
        col_idx, shift = int(match.group(1)), int(match.group(2))
        rotate_column(screen, col_idx, shift)
```

## Edge Cases to Handle in Implementation
1. **Rotation amount larger than dimension**: Use modulo to normalize
2. **Zero-sized rectangles**: rect 0x0 should do nothing (edge case, unlikely in input)
3. **Rotation by 0**: Should leave row/column unchanged
4. **Full rotation**: Rotating by exactly width/height should return to original state

## Expected Output
A single integer representing the count of lit pixels after all operations.

**Output format**: Just the number, nothing else
- Good: `121`
- Bad: `The answer is: 121`
- Bad: `Lit pixels: 121`

This is important for Advent of Code answer submission.
