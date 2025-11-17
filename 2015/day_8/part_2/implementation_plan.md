# Implementation Plan: String Encoding

## Problem Summary
Given string literals (already containing escape sequences), encode them by re-escaping to create a new string literal representation. Calculate the total additional characters needed when encoding all strings.

## Key Observations

1. **Input Format**: Each line is a string literal enclosed in double quotes containing:
   - Regular ASCII characters
   - Escaped quotes `\"`
   - Escaped backslashes `\\`
   - Hex escape sequences `\xNN`

2. **Encoding Rules**:
   - Wrap entire string in new quotes
   - Escape every `"` by adding `\` before it (becomes `\"`)
   - Escape every `\` by adding `\` before it (becomes `\\`)
   - Result is a new string literal representing the original

3. **Character-by-Character Analysis**:
   - Original: `"abc"` (5 chars)
   - Encoded: `"\"abc\""` (9 chars)
   - The opening `"` becomes `\"`
   - The closing `"` becomes `\"`
   - Add outer quotes
   - Difference: +4

   - Original: `"a\"b"` (6 chars)
   - Contains: `"`, `a`, `\`, `"`, `b`, `"`
   - Encoded: Each `"` → `\"`, each `\` → `\\`
   - `"\"a\\\"b\""` (12 chars)
   - Difference: +6

## Algorithm Design

### Approach
Process each line character-by-character and count:
1. Original length: length of the raw string (as written in file)
2. Encoded length: 2 (for outer quotes) + count of escaped characters

### Step-by-Step Implementation

#### Step 1: File I/O Setup
```python
def solve(input_file):
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')
```

#### Step 2: Character Counting Function
Create a function to calculate encoded length for a single string:

```python
def calculate_encoded_length(line):
    # Original length is just len(line)
    original_length = len(line)

    # For encoded length, count characters that need escaping
    encoded_length = 2  # Start with outer quotes

    for char in line:
        if char == '"' or char == '\\':
            encoded_length += 2  # Backslash + character
        else:
            encoded_length += 1  # Regular character

    return encoded_length, original_length
```

#### Step 3: Main Processing Loop
```python
total_difference = 0

for line in lines:
    if not line:  # Skip empty lines
        continue

    encoded_len, original_len = calculate_encoded_length(line)
    difference = encoded_len - original_len
    total_difference += difference

return total_difference
```

#### Step 4: Complete Solution Structure
```python
def solve(input_file):
    """
    Calculate total additional characters when encoding string literals.

    Args:
        input_file: Path to input file containing string literals

    Returns:
        Integer representing total difference between encoded and original lengths
    """
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')

    total_difference = 0

    for line in lines:
        if not line:
            continue

        # Count original length
        original_length = len(line)

        # Count encoded length
        encoded_length = 2  # Outer quotes
        for char in line:
            if char == '"' or char == '\\':
                encoded_length += 2
            else:
                encoded_length += 1

        total_difference += (encoded_length - original_length)

    return total_difference

if __name__ == "__main__":
    result = solve('input.md')
    print(result)
```

## Complexity Analysis

### Time Complexity: O(n)
- n = total number of characters across all input lines
- Single pass through input file
- Single pass through each line's characters
- Very efficient for large inputs

### Space Complexity: O(m)
- m = number of lines in input
- Store lines in memory (could be optimized to O(1) by processing line-by-line)
- No additional data structures needed

## Edge Cases Handled

1. **Empty lines**: Skip with `if not line: continue`
2. **Single quotes**: No special handling needed (they count as 1 character)
3. **Consecutive backslashes**: Each `\` is escaped individually
4. **Hex sequences**: Characters in `\x27` are processed individually:
   - `\` → `\\` (2 chars in encoded)
   - `x` → `x` (1 char)
   - `2` → `2` (1 char)
   - `7` → `7` (1 char)

## Optimization Notes

For very large files, we could optimize memory by processing line-by-line without storing all lines:

```python
total_difference = 0
with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Process line...
```

However, for this problem size (300 lines), the difference is negligible.

## Why This Approach is Correct

1. **Direct character counting**: We don't need to actually build the encoded string, just count its length
2. **Simple escaping rules**: Only two characters need escaping (`"` and `\`)
3. **Efficient**: Single pass through data with minimal operations
4. **Clear logic**: Easy to verify correctness by hand for small examples

## Input Assumptions

1. **File Encoding**: UTF-8 encoding (Python 3 default)
2. **Line Endings**: Handles Unix (`\n`), Windows (`\r\n`), and Mac (`\r`) line endings via `.strip()`
3. **File Format**: Each line contains a well-formed string literal enclosed in double quotes
4. **Trailing Content**: The `.strip().split('\n')` approach handles trailing newlines correctly

## Optional Debugging Enhancement

For troubleshooting, a verbose mode could be added to show per-line differences:

```python
def solve(input_file, verbose=False):
    # ... existing code ...

    for line in lines:
        if not line:
            continue

        original_length = len(line)
        encoded_length = 2
        for char in line:
            if char == '"' or char == '\\':
                encoded_length += 2
            else:
                encoded_length += 1

        difference = encoded_length - original_length

        if verbose:
            print(f"Line: {line[:50]}... | Original: {original_length} | Encoded: {encoded_length} | Diff: {difference}")

        total_difference += difference

    return total_difference
```

This is **not required** for solving the problem but can be useful for verification.

## Updates Based on Critique

The following enhancements have been incorporated based on feedback:

1. **Input Assumptions Section Added**: Explicitly documents file encoding (UTF-8), line ending handling, and format expectations
2. **Optional Debugging Enhancement**: Added verbose mode example for troubleshooting and verification
3. **Clarity Improvements**: Made explicit what was implicit about trailing newline handling and Python's default behaviors

The critique confirmed that the core algorithm is correct and efficient. These additions provide better documentation without over-engineering the solution. The implementation remains appropriately scoped for an Advent of Code scripting task.
