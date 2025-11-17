# Implementation Plan: Santa's Basement Entry Position

## Problem Summary
Find the 1-indexed position of the first character in a string of parentheses that causes Santa to reach floor -1 (basement) for the first time. Santa starts at floor 0, `(` means up one floor, `)` means down one floor.

## Algorithm Analysis

### Complexity Requirements
- **Time Complexity**: O(n) where n is the length of the input string
  - We need to process characters sequentially until we find the first basement entry
  - In worst case, we may need to scan the entire string
  - No way to avoid linear scan since we must process in order
- **Space Complexity**: O(1)
  - Only need to track current floor and position counter
  - Input string is read-only, no additional data structures needed

### Algorithm Efficiency
- **Best Case**: O(1) - if first character is `)`, immediate basement entry
- **Average Case**: O(n) - will likely find basement entry somewhere in middle
- **Worst Case**: O(n) - basement entry at end or never reached
- Given the input is a long string (~7000 characters based on input.md), O(n) linear scan is optimal and efficient

## Implementation Steps

### Step 1: Input Reading
- Read the input from `input.md`
- Strip any trailing whitespace/newlines to get clean string (Advent of Code inputs typically have trailing newlines)
- The input is a single line of parentheses characters
- **Assumption**: Input contains only `(` and `)` characters (guaranteed by problem statement)
- No validation needed beyond basic file reading (script context)

### Step 2: Core Algorithm Implementation
Create a function `find_basement_position(instructions: str) -> int`:

**Algorithm Logic:**
1. Initialize `current_floor = 0` (Santa starts at ground floor)
2. Iterate through each character with enumeration for position tracking
3. For each character at index `i`:
   - If character is `(`: increment `current_floor` by 1
   - If character is `)`: decrement `current_floor` by 1
   - Check if `current_floor == -1`
   - If yes: return `i + 1` (convert 0-indexed to 1-indexed position)
4. If loop completes without finding basement: return None or -1 (error case)

**Key Implementation Details:**
- Use enumerate() to get both index and character in single pass
- Convert index to 1-indexed position by adding 1 before returning
- Early exit as soon as floor -1 is reached (optimization)
- No need to track entire floor history, only current floor

### Step 3: Main Execution Flow
```python
def main():
    # Read input
    with open('input.md', 'r') as f:
        instructions = f.read().strip()

    # Find basement position
    position = find_basement_position(instructions)

    # Output result
    print(position)
```

### Step 4: Edge Cases to Handle
While we don't need extensive error handling for a script, we should handle:
1. **Empty string**: Return None or handle gracefully (unlikely given problem context)
2. **Never reaching basement**: Return None or -1 if we complete without finding -1
   - Note: Advent of Code problem likely guarantees basement is reached, but defensive programming is good practice
3. **File reading**: Basic try-catch for file operations (optional)

## Code Structure

```python
def find_basement_position(instructions: str) -> int:
    """
    Find the 1-indexed position where Santa first enters basement (floor -1).

    Args:
        instructions: String of '(' and ')' characters

    Returns:
        1-indexed position of first basement entry, or None if never reached
    """
    current_floor = 0

    for index, char in enumerate(instructions):
        if char == '(':
            current_floor += 1
        elif char == ')':
            current_floor -= 1

        # Check if we've entered the basement
        if current_floor == -1:
            return index + 1  # Convert to 1-indexed

    return None  # Never reached basement

def main():
    # Read input
    with open('input.md', 'r') as f:
        instructions = f.read().strip()

    # Find and print result
    result = find_basement_position(instructions)
    print(result)

if __name__ == "__main__":
    main()
```

## Performance Considerations

### Why This Algorithm is Optimal
1. **Single Pass**: We only traverse the string once
2. **Early Exit**: Stop immediately when floor -1 is found
3. **Constant Space**: No additional data structures, only 2 integer variables
4. **No String Operations**: Direct character comparison, no string manipulation

### Input Size Analysis
- Input length: ~7000 characters
- Operations per character: 2 (increment/decrement + comparison)
- Total operations: ~14,000
- Expected runtime: < 1ms on modern hardware
- Memory usage: Negligible (only 2 integers + input string reference)

### Alternative Approaches (and why they're not needed)
1. **Two-pass approach**: Would be O(2n), worse than our O(n)
2. **Tracking all floor values**: O(n) space, unnecessary
3. **String indexing without enumerate**: More verbose, same complexity
4. **Recursion**: Adds stack overhead, no benefit for sequential problem

## File Naming
- Main solution file: `solution.py`
- Contains both the algorithm function and main execution

## Expected Output Format
- Single integer printed to stdout
- Represents the 1-indexed position
- Based on examples: likely a value between 1 and length of input
