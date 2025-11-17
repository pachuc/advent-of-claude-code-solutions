# Implementation Plan: LCD Screen Character Recognition (Part 2)

## Overview
Part 2 builds directly on Part 1 by reusing the screen simulation logic but adding OCR (Optical Character Recognition) to read the letters displayed on the screen. Instead of counting pixels, we need to decode the actual text message.

## Key Insights
- **Reuse Part 1 code**: The screen simulation logic from `part_1_solution.py` is 100% reusable
- **Part 1 verified correctness**: We know the Part 1 solution works (119 lit pixels), so we can trust the screen state generation
- **OCR challenge**: The main new challenge is recognizing 5×6 pixel patterns as letters
- **Letter format**: Each letter is exactly 5 pixels wide × 6 pixels tall, so 10 possible letters on a 50-pixel wide screen

## Algorithm Efficiency Analysis
- **Time Complexity**: O(n) where n is the number of instructions (already optimal from Part 1)
- **Space Complexity**: O(1) - fixed 50×6 grid (300 pixels)
- **OCR Complexity**: O(1) - maximum 10 letters, each 5×6 = 30 pixel comparisons per letter
- **Overall**: Very efficient, no optimization needed for the input size

## Step-by-Step Implementation Plan

### Step 1: Reuse Part 1 Screen Simulation
**Action**: Copy the core functions from `part_1_solution.py`

**Functions to reuse**:
- `initialize_screen(width, height)` - Create the 50×6 grid
- `rect(screen, width, height)` - Turn on rectangular regions
- `rotate_row(screen, row_index, shift_amount)` - Rotate rows right
- `rotate_column(screen, col_index, shift_amount)` - Rotate columns down
- `parse_and_execute_instruction(screen, instruction)` - Parse and execute instructions
- `display_screen(screen)` - Visualize the screen (useful for debugging)

**Why**: These functions are already correct and tested. No need to rewrite.

### Step 2: Run Part 1 Code to Display Screen
**Action**: Execute Part 1 logic to see the actual screen output

**Implementation**:
```python
# Quick script to see what's on the screen
screen = initialize_screen(50, 6)
with open('input.md', 'r') as f:
    for line in f:
        if line.strip():
            parse_and_execute_instruction(screen, line.strip())

print("Final screen:")
display_screen(screen)
print(f"\nPixel count: {sum(sum(row) for row in screen)}")  # Should be 119
```

**Why**: We need to see the actual letters before building the pattern database. This also verifies Part 1 logic is working.

### Step 3: Manually Identify Letters
**Action**: Visually inspect the 50×6 screen output and identify which letters appear

**Process**:
1. Look at the screen output with column guides (every 5 pixels)
2. Identify each 5×6 block as a letter
3. Make a list of unique letters that appear (e.g., "Z, F, H, S, O, G, P")
4. Manually transcribe each letter's 5×6 pixel pattern

**Example**:
If columns 0-4 show:
```
####.
...#.
..#..
.#...
#....
####.
```
This might be the letter 'Z'.

**Note**: This step is manual but critical. Take time to accurately transcribe patterns.

### Step 4: Create Letter Pattern Database
**Action**: Define a dictionary mapping 5×6 pixel patterns to letters

**Implementation approach**:
```python
LETTER_PATTERNS = {
    'A': [
        '.##..',
        '#..#.',
        '#..#.',
        '####.',
        '#..#.',
        '#..#.'
    ],
    'B': [
        '###..',
        '#..#.',
        '###..',
        '#..#.',
        '#..#.',
        '###..'
    ],
    # ... more letters
}
```

**Considerations**:
- Store patterns as lists of strings for easy comparison
- Use '.' for OFF pixels, '#' for ON pixels
- Only define the letters that actually appear in the output (discovered in Step 3)
- Each pattern should be a list of exactly 6 strings, each exactly 5 characters long
- Advent of Code 2016 uses a consistent 5×6 pixel font across all LCD problems

**Important**: Based on Step 3, only add the letters you actually see. This is more efficient than defining all 26 letters upfront.

### Step 5: Implement Screen-to-Pattern Conversion
**Action**: Create a function to extract a 5×6 block from the screen

**Function signature**:
```python
def extract_letter(screen, column_start):
    """
    Extract a 5-pixel wide, 6-pixel tall region from the screen

    Args:
        screen: 2D array of boolean values (50×6)
        column_start: Starting column index (0, 5, 10, 15, ..., 45)

    Returns:
        List of 6 strings, each 5 characters wide
    """
```

**Implementation details**:
- Iterate through all 6 rows
- For each row, extract columns [column_start : column_start + 5]
- Convert boolean values to '#' (True) or '.' (False)
- Return as a list of 6 strings

### Step 6: Implement Pattern Matching
**Action**: Create a function to match extracted patterns against the letter database

**Function signature**:
```python
def recognize_letter(pattern):
    """
    Match a 5×6 pattern against known letter patterns

    Args:
        pattern: List of 6 strings, each 5 characters wide

    Returns:
        The recognized letter (A-Z) or '?' if not recognized
    """
```

**Implementation logic**:
```python
def recognize_letter(pattern):
    # Try to match against known patterns
    for letter, known_pattern in LETTER_PATTERNS.items():
        if pattern == known_pattern:
            return letter

    # If no match found, print the pattern to help debug
    print("ERROR: Unrecognized pattern found:")
    for i, line in enumerate(pattern):
        print(f"  Row {i}: '{line}'")
    print()
    return '?'  # Return '?' to indicate failure but continue
```

**Why print the pattern**: If a pattern isn't recognized, we need to see it to add it to the database.

### Step 7: Implement Full OCR Function
**Action**: Create the main OCR function that processes the entire screen

**Function signature**:
```python
def decode_screen(screen):
    """
    Read all letters from the 50×6 screen

    Args:
        screen: 2D array of boolean values (50×6)

    Returns:
        String of decoded letters (e.g., "ABCDEFGH")
    """
```

**Implementation logic**:
```python
def decode_screen(screen):
    result = ""

    # Check all 10 possible letter positions
    for col_start in range(0, 50, 5):
        pattern = extract_letter(screen, col_start)

        # Check if this 5x6 block is entirely blank
        if all(line == '.....' for line in pattern):
            # Skip blank regions (don't add spaces to output)
            continue

        # Recognize the letter and add to result
        letter = recognize_letter(pattern)
        result += letter

    return result
```

**Key decisions**:
- Use `range(0, 50, 5)` to iterate through all 10 positions (columns 0, 5, 10, ..., 45)
- Skip entirely blank 5×6 regions (all dots) - don't add them to output
- This handles trailing spaces and gaps between letter groups
- If a pattern is unrecognized, '?' is added to the result (from `recognize_letter()`)

### Step 8: Create Main Solving Function
**Action**: Tie everything together in a `solve()` function

**Function signature**:
```python
def solve(input_file):
    """
    Main solving function for Part 2

    Args:
        input_file: Path to the instruction file

    Returns:
        The decoded message string
    """
```

**Implementation steps**:
1. Initialize a 50×6 screen (all OFF)
2. Read instructions from the input file
3. Process each instruction using `parse_and_execute_instruction()`
4. Display the final screen (for debugging/verification)
5. Decode the screen using `decode_screen()`
6. Return the decoded message

### Step 9: Add Debug Visualization
**Action**: Enhance the display function to show column boundaries

**Function signature**:
```python
def display_screen_with_guides(screen):
    """
    Display screen with column guides to help identify letter boundaries
    """
```

**Implementation**:
- Print column numbers above the screen (every 5 columns)
- Print the screen with visual separators every 5 columns (optional)
- This helps verify that letters are being extracted correctly

### Step 10: Test and Verify
**Action**: Run the complete solution and verify the output

**Process**:
1. Run the complete `solve()` function
2. Verify pixel count is 119 (regression test for Part 1)
3. Check that no '?' characters appear in output (all patterns recognized)
4. Visually compare the decoded message with the screen display
5. If any '?' appears, the error output will show the missing pattern - add it to LETTER_PATTERNS and re-run

**Success criteria**:
- Pixel count = 119
- Output is a string of uppercase letters (A-Z only)
- No '?' characters in output
- Output length is reasonable (8-10 characters based on screen width)
- Visual inspection confirms the decoded message matches the screen

## Code Structure

```python
import re

# ============ PART 1 REUSED CODE ============
def initialize_screen(width, height): ...
def rect(screen, width, height): ...
def rotate_row(screen, row_index, shift_amount): ...
def rotate_column(screen, col_index, shift_amount): ...
def parse_and_execute_instruction(screen, instruction): ...
def display_screen(screen): ...

# ============ PART 2 NEW CODE ============

# Letter pattern database
LETTER_PATTERNS = {
    # Add patterns as we discover them
}

def extract_letter(screen, column_start): ...
def recognize_letter(pattern): ...
def decode_screen(screen): ...
def display_screen_with_guides(screen): ...

def solve(input_file):
    # Initialize and process screen (Part 1 logic)
    screen = initialize_screen(50, 6)

    with open(input_file, 'r') as f:
        for line in f:
            if line.strip():
                parse_and_execute_instruction(screen, line.strip())

    # Visualize (for debugging)
    print("Final screen:")
    display_screen(screen)
    print()

    # Decode and return
    message = decode_screen(screen)
    return message

if __name__ == "__main__":
    result = solve('input.md')
    print(f"Decoded message: {result}")
```

## Implementation Order (UPDATED)
1. **Copy Part 1 functions** (5 minutes)
2. **Run Part 1 code to display screen** (2 minutes)
3. **Manually identify and transcribe letter patterns** (15-20 minutes - most critical step!)
4. **Build LETTER_PATTERNS dictionary** (5 minutes)
5. **Implement extract_letter() function** (5 minutes)
6. **Implement recognize_letter() function** (5 minutes)
7. **Implement decode_screen() function** (5 minutes)
8. **Implement solve() and test** (5-10 minutes)

**Total estimated time**: 45-60 minutes

**Note**: The order has been updated to discover letters first (Step 2-3) before implementing OCR functions (Step 5-7). This is more efficient than the original plan.

## Potential Challenges
1. **Pattern identification**: Manually identifying letter patterns from pixel output can be error-prone
   - **Solution**: Use careful visual inspection, perhaps zoom in or print larger

2. **Pattern variations**: Letters might have slightly different representations
   - **Solution**: The Advent of Code typically uses consistent fonts, so this is unlikely

3. **Spaces vs letters**: Need to distinguish blank regions from actual letters
   - **Solution**: Check if all pixels in a 5×6 region are OFF before attempting recognition

4. **Off-by-one errors**: Column indices must be exact (0, 5, 10, ...)
   - **Solution**: Use range(0, 50, 5) to ensure correct stepping

## Testing Strategy
See `test_plan.md` for comprehensive testing approach.
