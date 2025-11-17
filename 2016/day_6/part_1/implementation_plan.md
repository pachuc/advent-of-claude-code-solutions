# Implementation Plan: Signal Error Correction

## Problem Summary
Decode an error-corrected message from corrupted transmissions by finding the most frequent character at each position across all transmissions.

## Input Analysis
- **Size**: 598 lines of 8-character strings
- **Format**: Each line is a corrupted transmission of the same message
- **Constraints**: All lines have equal length (8 characters)
- **Character set**: Lowercase letters (a-z)

## Algorithm Strategy

### Approach: Column-wise Frequency Analysis
**Time Complexity**: O(n × m) where n = number of lines (598), m = message length (8)
**Space Complexity**: O(m × k) where k = unique characters per position (max 26)

This is optimal for the problem since we must examine every character in the input.

### Step-by-Step Algorithm

1. **Parse Input**
   - Read all lines from input file
   - Strip whitespace/newlines from each line
   - Store in a list of strings
   - Validate: All lines should have same length

2. **Determine Message Length**
   - Get length from first line (all lines are equal length)
   - This will be used to iterate over positions

3. **For Each Position (Column)**
   - Iterate from position 0 to message_length - 1
   - For each position:
     - Extract character at that position from each line
     - Count frequency of each character at this position
     - Identify the character with maximum frequency

4. **Build Result Message**
   - Concatenate the most frequent character from each position
   - Return the decoded message

## Implementation Details

### Data Structures
- **Input storage**: `List[str]` - stores all transmission lines
- **Frequency counting**: `collections.Counter` - efficient frequency counting for each position
- **Result**: `str` - the decoded message

### Key Functions

#### Main Function: `decode_message(lines: List[str]) -> str`
```
Purpose: Main decoder that orchestrates the error correction
Input: List of corrupted transmission strings
Output: Decoded message string
Process:
  1. Validate input (not empty, all lines same length)
  2. Determine message length
  3. For each position in range(message_length):
     - Extract all characters at this position
     - Use Counter to find most common character
     - Append to result
  4. Return result string
```

#### I/O Function: `read_input(filepath: str) -> List[str]`
```
Purpose: Read and parse input file with error handling
Input: Path to input file
Output: List of transmission strings
Process:
  1. Try to open file (handle FileNotFoundError)
  2. Read all lines
  3. Strip whitespace from each line
  4. Filter out empty lines
  5. Return list of cleaned strings
Error Handling:
  - FileNotFoundError: Print clear error message and exit
  - Other IOErrors: Print error and exit
```

### Implementation Steps

1. **Import Required Modules**
   - `collections.Counter` for frequency counting
   - Standard file I/O operations

2. **Implement Input Reading**
   - Function to read input file
   - Clean each line (strip whitespace)
   - Return list of transmission strings

3. **Implement Core Decoding Logic**
   - Validate input is not empty
   - Get message length from first line
   - Validate all lines have the same length
   - Loop through each position (0 to length-1)
   - For each position:
     - Collect all characters at that position using list comprehension
     - Use Counter to find most common character
     - Append to result string

4. **Implement Main Entry Point**
   - Read input from file
   - Call decode function
   - Print result

## Efficiency Considerations

### Why This Approach is Optimal
1. **Single Pass**: We read the input once and process each character once
2. **Counter Efficiency**: Python's Counter uses a hash table (O(1) average insert/lookup)
3. **Memory Efficient**: We only store frequency counts for one position at a time
4. **No Sorting Needed**: Counter.most_common() uses heapq for finding top element (O(n) for single element)

### Alternative Approaches Considered
- **Sorting each column**: O(n × m × n log n) - much slower
- **Manual frequency counting with dict**: Same complexity, but Counter is optimized C code
- **NumPy arrays**: Overkill for this problem size, adds dependency

### Performance Expectations
- **Input size**: 598 lines × 8 chars = 4,784 characters
- **Expected runtime**: < 1ms (trivial for this size)
- **Memory usage**: < 1MB (minimal)

## Code Structure

```python
from collections import Counter
import sys

def read_input(filepath):
    """Read and parse input file with error handling."""
    try:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"Error: Input file '{filepath}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{filepath}': {e}")
        sys.exit(1)

def decode_message(lines):
    """Decode message by finding most frequent char at each position."""
    if not lines:
        return ""

    # Validate all lines have the same length
    message_length = len(lines[0])
    for i, line in enumerate(lines):
        if len(line) != message_length:
            raise ValueError(f"Line {i} has length {len(line)}, expected {message_length}")

    decoded = []

    for pos in range(message_length):
        # Get all characters at this position
        chars_at_pos = [line[pos] for line in lines]
        # Find most frequent character
        most_frequent = Counter(chars_at_pos).most_common(1)[0][0]
        decoded.append(most_frequent)

    return ''.join(decoded)

def main():
    lines = read_input('input.md')
    result = decode_message(lines)
    print(result)

if __name__ == '__main__':
    main()
```

## Edge Cases Handled
1. **Empty input**: Return empty string
2. **Single line**: Each character is most frequent (100% frequency)
3. **Ties in frequency**: Counter.most_common() tie-breaking is deterministic but implementation-dependent (based on Python's dict ordering)
4. **Unequal line lengths**: Raise ValueError with clear error message
5. **File not found**: Print error message and exit gracefully

## Validation
- Verify all lines have same length (explicit validation with error message)
- Ensure input file exists and is readable (with try-except handling)
- Handle empty input gracefully
- Result should be lowercase letters only
