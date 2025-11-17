# Implementation Plan: Recursive Decompression (Part 2)

## Overview
Implement a recursive decompression length calculator that processes nested markers. Unlike Part 1 (non-recursive), Part 2 requires that markers within decompressed data sections be recursively processed.

## Core Algorithm Differences from Part 1

### Part 1 Approach (Non-Recursive)
```
When encountering (AxB):
  - Add A * B to total length
  - Skip past marker and A characters
```

### Part 2 Approach (Recursive)
```
When encountering (AxB):
  - Extract next A characters as a substring
  - Recursively calculate decompressed_length(substring)
  - Add recursive_length * B to total length
  - Skip past marker and A characters
```

## Implementation Steps

### Step 1: Create Recursive Helper Function
**Function**: `calculate_decompressed_length_recursive(s)`

**Purpose**: Recursively calculate the decompressed length of a string that may contain markers.

**Algorithm**:
1. Initialize `total_length = 0` and `i = 0`
2. Iterate through string with index `i`:
   - **If whitespace**: Skip (increment `i`, don't add to length)
   - **If `(`**: This is a marker
     - Find matching `)` to extract marker content
     - Parse `(AxB)` to get integers `A` and `B`
     - Extract substring of next `A` characters after the marker
     - **Recursively call** `calculate_decompressed_length_recursive(substring)`
     - Add `recursive_result * B` to `total_length`
     - Skip past marker and the `A` characters: `i = close_paren_index + 1 + A`
   - **If regular character**:
     - Add 1 to `total_length`
     - Increment `i`
3. Return `total_length`

**Key Implementation Details**:
- String indexing: When at position after `)`, the next `A` characters are `s[i:i+A]` where `i = close_paren_index + 1`
- **Whitespace handling clarification**: When extracting "next A characters", whitespace counts as a character position (e.g., if A=5 and the next 5 positions are "A B C", we extract all 5 positions including spaces). However, when recursively calculating the length of that substring, whitespace is ignored in the length calculation. This is consistent with Part 1 behavior.
- Handle whitespace in the extracted substring - the recursive call will handle it
- No need to actually build the decompressed string, just count length
- **Assumption**: Input markers are well-formed (valid integers, closed parentheses). No error handling needed for this puzzle solution.

### Step 2: Handle Edge Cases
1. **Empty string**: Return 0
2. **No markers**: Each character counts as 1 (base case of recursion)
3. **Whitespace**: Should be ignored at all recursion levels
4. **Nested markers**: Handled automatically by recursion

### Step 3: Main Function
1. Read input from `input.md`
2. Strip whitespace from beginning/end (but preserve internal whitespace for proper parsing)
3. Call `calculate_decompressed_length_recursive(compressed)`
4. Print result

## Code Structure

```python
def calculate_decompressed_length_recursive(s):
    """
    Recursively calculate decompressed length.

    Markers within data sections are processed recursively.

    Args:
        s: Compressed string (or substring)

    Returns:
        Integer length of decompressed string
    """
    total_length = 0
    i = 0
    n = len(s)

    while i < n:
        if s[i].isspace():
            # Skip whitespace
            i += 1
        elif s[i] == '(':
            # Parse marker (AxB)
            close_idx = s.find(')', i)
            marker_content = s[i+1:close_idx]
            a_str, b_str = marker_content.split('x')
            A, B = int(a_str), int(b_str)

            # Extract the next A characters
            start = close_idx + 1
            substring = s[start:start + A]

            # RECURSIVE CALL: Calculate length of substring
            substring_length = calculate_decompressed_length_recursive(substring)

            # Multiply by B repetitions
            total_length += substring_length * B

            # Skip past marker and A characters
            i = start + A
        else:
            # Regular character
            total_length += 1
            i += 1

    return total_length


def main():
    # Read input
    with open('input.md', 'r') as f:
        compressed = f.read().strip()

    # Calculate length using recursive approach
    result = calculate_decompressed_length_recursive(compressed)

    # Output result
    print(result)


if __name__ == '__main__':
    main()
```

## Reusability from Part 1

**Reusable components**:
- File reading logic (exactly the same)
- Overall structure (main function, input handling)
- Whitespace handling logic
- Marker parsing logic (finding `(`, `)`, splitting on `x`)

**Changes needed**:
- Replace simple `A * B` calculation with recursive call
- Extract substring and pass to recursive function
- The function becomes recursive instead of iterative-only

## Time Complexity Analysis

### Best Case
- String with no markers: O(n) where n is length of input
- Each character processed once

### Worst Case
- Deeply nested markers with large repetition factors
- Time complexity: O(n * d) where:
  - n = length of input string
  - d = maximum depth of marker nesting
- Each recursion level processes its substring once
- The recursion depth is bounded by the nesting level

### Space Complexity
- O(d) for recursion stack where d is maximum nesting depth
- O(n) for substring extraction in worst case
- Total: O(n + d)

**Note**: The actual decompressed length could be gigabytes, but we never build it in memory - we only calculate the length mathematically.

## Potential Optimizations (If Needed)

1. **Memoization**: Cache results for identical substrings. While substrings are usually unique in compression data, there's potential for repeated patterns. However, memoization adds complexity and memory overhead. If performance becomes an issue, profile first to identify actual bottlenecks before adding memoization.
2. **Iterative with explicit stack**: Convert recursion to iteration if stack depth becomes an issue (unlikely given problem constraints)
3. **String pre-processing**: Remove all whitespace upfront to simplify parsing (minor optimization, but may complicate character extraction logic)

**Decision**: Start with clean recursive solution. Optimize only if performance issues arise. Profile before optimizing.

## Implementation File
- Filename: `solution.py`
- Will adapt structure from `part_1_solution.py` with recursive modification
