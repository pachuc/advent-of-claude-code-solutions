# Implementation Plan: Decompression Length Calculator

## Problem Summary
Implement a Python script to calculate the decompressed length of a compressed string without actually decompressing it. The compression format uses markers `(AxB)` to indicate repetition patterns, where A characters following the marker should be repeated B times.

## Key Constraints
1. **Non-recursive processing**: Markers within data sections are treated as literal text
2. **Whitespace handling**: All whitespace should be ignored in the decompressed length calculation. Whitespace is skipped during iteration but still affects character positions for marker data sections.
3. **Efficiency required**: The input is large (~5KB compressed), so we need an efficient O(n) algorithm
4. **Output only length**: We don't need to construct the actual decompressed string
5. **Well-formed input assumption**: We assume all input is well-formed per Advent of Code problem constraints (valid markers, proper formatting)

## Algorithm Design

### Overall Approach: Single-Pass Linear Scan
We'll use a single-pass algorithm that scans the input left to right, maintaining a position pointer and accumulating the total decompressed length.

**Time Complexity**: O(n) where n is the input length
**Space Complexity**: O(1) - only need tracking variables

### Step-by-Step Algorithm

1. **Initialize**
   - `total_length = 0` - accumulates the decompressed length
   - `i = 0` - current position in the input string
   - `n = len(input)` - length of input

2. **Main Loop** - while `i < n`:

   **Case A: Current character is whitespace**
   - Skip it (increment `i`, don't add to length)

   **Case B: Current character is '(' (marker start)**
   - Find the closing ')' by scanning forward from current position
   - Extract marker content between parentheses (e.g., "8x2")
   - Split by 'x' to get A and B as strings, convert to integers
   - Calculate contribution: `A * B` (these A characters will be repeated B times)
   - Add `A * B` to `total_length`
   - Move position pointer: `i = close_paren_position + 1 + A`
     - `close_paren_position + 1` = position right after ')'
     - `+ A` = skip past the A characters that form the data section
   - Note: We skip A characters INCLUDING any whitespace in those positions

   **Case C: Regular character (not whitespace, not '(')**
   - Add 1 to `total_length`
   - Increment `i`

3. **Return** `total_length`

## Implementation Details

### Function Structure

```
main():
    - Read input from file
    - Clean input (remove newlines if necessary)
    - Call calculate_decompressed_length()
    - Print result

calculate_decompressed_length(s):
    - Main algorithm implementation
    - Returns integer length

parse_marker(s, start_pos):
    - Extract and parse marker starting at position
    - Returns (A, B, marker_length)
    - Handle parsing of numbers from the marker string
```

### Parsing Marker Details

When we encounter '(' at position `i`:

```python
# Find closing parenthesis
close_idx = s.find(')', i)

# Extract content between parentheses (e.g., "8x2")
marker_content = s[i+1:close_idx]

# Split by 'x' to get A and B
a_str, b_str = marker_content.split('x')
A = int(a_str)
B = int(b_str)

# Calculate contribution
contribution = A * B
total_length += contribution

# Advance position past marker and data section
i = close_idx + 1 + A
```

**Edge cases to handle**:
- Markers can contain multi-digit numbers (e.g., `(123x456)`)
- The 'x' separator is always lowercase
- No spaces within markers (based on examples)
- We assume all markers are well-formed (valid integers for A and B)

### Whitespace Handling

**Important**: Whitespace affects length calculation but NOT position tracking.

- When scanning and we encounter whitespace, skip it in length calculation
- However, whitespace still occupies positions in the string
- When a marker says "take next A characters", those A characters are counted by position (including any whitespace positions)
- Use `char.isspace()` to detect all types of whitespace (spaces, tabs, newlines, etc.)

**Example**: `(5x1)AB CD`
- Marker says take next 5 characters by position: `AB CD` (including the space)
- Those 5 characters contain 1 space
- Length contribution: 5 characters × 1 repetition = 5 positions
- But when calculating decompressed length, we don't count the space character itself
- So the decompressed length from this marker is 4 (only 'A', 'B', 'C', 'D')

**Clarification**: Based on the problem statement, whitespace should be ignored in the decompressed length. The simplest interpretation is that whitespace characters in data sections are still part of the "next A characters" but don't contribute to the length. However, if the input has been pre-cleaned (whitespace removed), this is a non-issue.

### Why This Works (Non-Recursive Explanation)

When we encounter a marker `(AxB)`:
- We calculate the contribution as `A * B`
- We skip forward by `marker_length + A` positions
- This means we skip over the A characters that would be repeated
- **Crucially**: Those A characters are never examined individually
- Even if those A characters contain '(' characters, we don't process them as markers
- This naturally implements the "no recursive processing" rule

**Example**: `X(8x2)(3x3)ABCY`
- Position 0: 'X' → add 1, move to position 1
- Position 1: '(' → marker `(8x2)` found
  - A=8, B=2, marker_length=5
  - Add 8*2=16 to length
  - Move to position 1+5+8=14 (skip the marker and 8 chars)
- Position 14: 'Y' → add 1
- Total: 1+16+1=18 ✓

## Code Structure

```python
def calculate_decompressed_length(s):
    """
    Calculate decompressed length without building the output.

    Args:
        s: Compressed string

    Returns:
        Integer length of decompressed string
    """
    total_length = 0
    i = 0
    n = len(s)

    while i < n:
        if s[i].isspace():
            # Skip whitespace - don't count in length
            i += 1
        elif s[i] == '(':
            # Parse marker
            close_idx = s.find(')', i)
            marker_content = s[i+1:close_idx]
            a_str, b_str = marker_content.split('x')
            A, B = int(a_str), int(b_str)

            # Add contribution to total length
            total_length += A * B

            # Skip past marker and the A characters in data section
            i = close_idx + 1 + A
        else:
            # Regular character
            total_length += 1
            i += 1

    return total_length

def main():
    # Read input
    with open('input.md', 'r') as f:
        compressed = f.read().strip()

    # Calculate length
    result = calculate_decompressed_length(compressed)

    # Output result
    print(result)

if __name__ == '__main__':
    main()
```

## Performance Considerations

### Input Size Analysis
- The input file is approximately 5KB
- This contains ~5000 characters
- Our O(n) algorithm will process this in milliseconds
- No memory concerns as we only store position and length variables

### Optimization Notes
- We don't build the decompressed string (would be much larger and waste memory)
- Single pass through input - no backtracking needed
- Simple integer arithmetic for length calculation
- String slicing is minimal (only for parsing markers)

## Testing Strategy Preview

The implementation will be tested with:
1. All provided examples from the problem statement
2. Edge cases (empty strings, only whitespace, nested-looking markers)
3. The actual input file
4. Large marker values to ensure integer arithmetic works correctly

## Expected Output Format

The script should output a single integer to stdout representing the decompressed length.

For the given input, we expect a large integer (likely in the tens of thousands based on the compression ratios visible in the input).
