# Implementation Plan: Stream Processing

## Problem Context
This solves **Advent of Code 2017, Day 9, Part 1**. Full problem description available in `problem.md`.

## Problem Summary
Parse a character stream containing nested groups and garbage to calculate a total score based on group nesting depth. Groups are delimited by `{}`, garbage by `<>`, and `!` acts as a cancellation character inside garbage.

## Requirements
- **Python Version**: Python 3.6+
- **Dependencies**: None (only built-in modules)
- **Input File**: `input.md` (single line of text)
- **Output**: Single integer printed to stdout

## Script Structure
The complete script will consist of:
1. Input reading function
2. Main processing function (`calculate_stream_score`)
3. Test suite (optional, for verification)
4. Main execution block

**Filename**: `solution.py`

## Algorithm Overview
Use a single-pass state machine approach to process the stream character by character, tracking:
- Current position in the stream
- Whether we're inside garbage
- Current nesting depth
- Total accumulated score

## Data Structures
- **Input**: String (the character stream)
- **State Variables**:
  - `in_garbage`: boolean - tracks if we're currently inside garbage
  - `depth`: integer - current nesting level (starts at 0)
  - `total_score`: integer - accumulated score (starts at 0)
  - `i`: integer - current index in the stream

## Step-by-Step Implementation

### Step 1: Set Up Main Function
```python
def calculate_stream_score(stream: str) -> int:
    """
    Calculate the total score for all groups in a character stream.

    Args:
        stream: The input character stream

    Returns:
        Total score of all groups
    """
```

### Step 2: Initialize State Variables
- `in_garbage = False` - we start outside garbage
- `depth = 0` - no groups opened yet
- `total_score = 0` - no score accumulated
- `i = 0` - start at the beginning

### Step 3: Main Loop - Iterate Through Stream
Use a while loop with manual index control to handle cancellation:
```python
while i < len(stream):
    char = stream[i]
    # Process character based on current state
    i += 1  # increment after processing (except for cancellation)
```

### Step 4: Handle Cancellation Character
When inside garbage, if we encounter `!`:
- Skip the next character entirely
- Increment index by 2 total (current `!` + next char)
```python
if in_garbage and char == '!':
    i += 1  # Skip the next character
    continue
```

### Step 5: Handle Garbage Start
When not in garbage and we see `<`:
- Set `in_garbage = True`
```python
if not in_garbage and char == '<':
    in_garbage = True
    continue
```

### Step 6: Handle Garbage End
When in garbage and we see `>`:
- Set `in_garbage = False`
```python
if in_garbage and char == '>':
    in_garbage = False
    continue
```

### Step 7: Handle Group Start
When not in garbage and we see `{`:
- **First**: Increment depth (to enter the new group)
- **Then**: Add the new depth value to total_score (this group's score equals its depth)
```python
if not in_garbage and char == '{':
    depth += 1          # Enter the group (now at depth 1, 2, 3, etc.)
    total_score += depth  # This group's score is its depth
    continue
```

**Important**: The order matters! We increment depth first, so `depth` represents the level of the group we just entered. A top-level group has depth 1, its children have depth 2, etc.

### Step 8: Handle Group End
When not in garbage and we see `}`:
- Decrement depth
```python
if not in_garbage and char == '}':
    depth -= 1
    continue
```

### Step 9: Handle Other Characters
All other characters (commas, letters, etc.) are ignored:
- Inside garbage: part of garbage content
- Outside garbage: separators (commas)

### Step 10: Return Result
After processing all characters, return `total_score`

## Implementation Order
1. Create the main function signature
2. Initialize all state variables
3. Implement the main while loop with index control
4. Add cancellation handling (must be first check when in garbage)
5. Add garbage boundary handling (`<` and `>`)
6. Add group boundary handling (`{` and `}`)
7. Implement input reading function
8. Implement main execution block
9. Test with provided examples

## Input Handling

### Step 11: Read Input File
Create a function to read and parse the input:
```python
def read_input(filename: str = 'input.md') -> str:
    """
    Read the input stream from a file.

    Args:
        filename: Path to input file

    Returns:
        The character stream as a string
    """
    with open(filename, 'r') as f:
        return f.read().strip()
```

**Note**: Using `strip()` to remove any trailing newlines or whitespace.

## Output Format

### Step 12: Main Execution Block
```python
if __name__ == '__main__':
    # Read input
    stream = read_input('input.md')

    # Calculate score
    result = calculate_stream_score(stream)

    # Print result
    print(f"Total score: {result}")
```

**Output Format**: Print the result with a clear label. For Advent of Code submission, you may want just the number:
```python
print(result)  # Just the number for easy copying
```

## Edge Cases to Handle
1. **Empty stream**: Return 0
2. **Nested cancellations**: `!!` cancels the second `!`
3. **Canceled garbage terminators**: `<!>` - the `>` is canceled, garbage continues
4. **Multiple consecutive groups**: `{}{}{}`
5. **Deep nesting**: Correctly track arbitrary nesting depth
6. **Garbage containing group characters**: `<{}>` - ignore the braces

## Complexity Analysis
- **Time Complexity**: O(n) where n is the length of the stream
  - Single pass through the entire string
  - Each character is processed exactly once (except canceled characters are skipped)
- **Space Complexity**: O(1)
  - Only uses a fixed number of variables regardless of input size
  - No additional data structures needed

## Why This Algorithm is Efficient
1. **Single Pass**: We only iterate through the stream once
2. **Constant Space**: No additional storage proportional to input size
3. **Simple State Machine**: Only 2 states (in/out of garbage), simple transitions
4. **Direct Calculation**: Score is calculated incrementally, no post-processing needed

Given the input size (appears to be ~20KB), this O(n) solution will handle it instantly.

## Python Implementation Notes
- Use a while loop instead of for loop to allow manual index control for cancellation
- Use boolean flag for garbage state rather than complex state tracking
- All operations are O(1) per character
- No need for recursion or stack data structures

## How to Run
```bash
# Run the solution
python solution.py

# Or with Python 3 explicitly
python3 solution.py
```

Expected output:
```
Total score: [calculated result]
```

## Complete Script Structure Overview

```python
# solution.py

def calculate_stream_score(stream: str) -> int:
    """Main processing function."""
    # ... implementation ...
    return total_score

def read_input(filename: str = 'input.md') -> str:
    """Read input from file."""
    with open(filename, 'r') as f:
        return f.read().strip()

if __name__ == '__main__':
    stream = read_input('input.md')
    result = calculate_stream_score(stream)
    print(f"Total score: {result}")
```

This structure keeps the code simple and focused - appropriate for a one-off script to solve an Advent of Code problem.
