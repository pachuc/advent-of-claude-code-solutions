# Implementation Plan: String Literal Character Count

## Problem Summary
Calculate the difference between the number of characters in the code representation of string literals versus their in-memory representation after parsing escape sequences.

## Algorithm Analysis

### Runtime Complexity
- **Time Complexity**: O(n × m) where n is the number of lines and m is the average line length
- **Space Complexity**: O(1) - we only need counters, no additional data structures
- **Efficiency**: The algorithm is highly efficient as it requires only a single pass through each line

### Input Size Considerations
- The input has 300 lines with average line length of ~30-40 characters
- Total input size: ~10,000-12,000 characters
- This is a small input, so even O(n²) would be acceptable, but our O(n) solution per line is optimal

## Step-by-Step Implementation Plan

### Step 1: Set Up File Reading
**Task**: Create the basic structure to read the input file
- Open and read the input file (input.md)
- Strip whitespace from each line
- Filter out empty lines

**Implementation Details**:
```python
def read_input(filename='input.md'):
    """Read input file and return list of non-empty lines.

    The input file is named input.md (markdown extension) but contains
    plain text string literals, one per line.
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines
```

### Step 2: Implement Code Character Counter
**Task**: Count the raw string literal characters
- For each line, simply use `len(line)` to get the total character count
- This includes the surrounding quotes and all escape sequences in their raw form

**Implementation Details**:
```python
def count_code_chars(line):
    return len(line)
```

### Step 3: Implement Memory Character Counter
**Task**: Parse escape sequences and count actual in-memory characters
- Remove surrounding double quotes (first and last character)
- Iterate through the string character by character
- Handle three types of escape sequences:
  - `\\` → single backslash (counts as 1)
  - `\"` → single quote (counts as 1)
  - `\x##` → single character from hex code (counts as 1)
- All other characters count as 1

**Algorithm**:
1. Start with the string without outer quotes
2. Use an index pointer to traverse the string
3. When encountering a backslash:
   - Check next character to determine escape type
   - If next char is `\` or `"`: increment counter by 1, advance index by 2
   - If next char is `x`: this is hex escape, increment counter by 1, advance index by 4 (`\x##`)
   - Otherwise: treat as regular character (edge case, shouldn't happen in valid input)
4. For non-backslash characters: increment counter by 1, advance index by 1

**Implementation Details**:
```python
def count_memory_chars(line):
    # Remove surrounding quotes
    content = line[1:-1]

    memory_count = 0
    i = 0

    while i < len(content):
        if content[i] == '\\':
            # Check what follows the backslash
            if i + 1 < len(content):
                next_char = content[i + 1]
                if next_char == '\\' or next_char == '"':
                    # \\ or \" - counts as 1 character
                    memory_count += 1
                    i += 2
                elif next_char == 'x':
                    # \x## - hex escape, counts as 1 character
                    memory_count += 1
                    i += 4  # Skip \x and two hex digits
                else:
                    # Invalid escape (shouldn't happen in valid input)
                    # Treat backslash as regular char, next char will be processed normally
                    memory_count += 1
                    i += 1
            else:
                # Backslash at end (shouldn't happen in valid input)
                memory_count += 1
                i += 1
        else:
            # Regular character
            memory_count += 1
            i += 1

    return memory_count
```

**Note on Edge Case Handling**: For invalid escape sequences (e.g., `\a`), the code treats the backslash as a regular character and advances by 1, allowing the next character to be processed in the next iteration. Since the problem guarantees valid input, this case won't occur, but the handling prevents double-counting if it did.

### Step 4: Implement Main Calculation Logic
**Task**: Process all lines and calculate the total difference
- Iterate through all lines
- For each line:
  - Count code characters
  - Count memory characters
  - Add the difference to running total
- Return the final sum

**Implementation Details**:
```python
def calculate_difference(lines):
    total_code = 0
    total_memory = 0

    for line in lines:
        code_count = count_code_chars(line)
        memory_count = count_memory_chars(line)

        total_code += code_count
        total_memory += memory_count

    return total_code - total_memory
```

### Step 5: Create Main Entry Point
**Task**: Tie everything together with a main function
- Read the input
- Calculate the difference
- Print the result

**Implementation Details**:
```python
def main():
    lines = read_input('input.md')
    result = calculate_difference(lines)
    print(result)

if __name__ == '__main__':
    main()
```

## Edge Cases to Handle

1. **Empty string `""`**: Code chars = 2, Memory chars = 0
2. **String with only escaped characters**: e.g., `"\\\\"`
3. **Hex escape at end of string**: e.g., `"\x27"` or `"abc\x27"`
4. **Multiple consecutive escapes**: e.g., `"\\\\\\\\"`
5. **Multiple consecutive hex escapes**: e.g., `"\x27\x27\x27"`
6. **Mixed escape types in one string**: e.g., `"a\\b\"c\x27d"`
7. **Escape immediately after escape**: e.g., `"\\\x27"` (backslash followed by hex)

**Note**: The problem guarantees valid input, so we don't need to handle:
- Malformed hex escapes (e.g., `\xZZ` or `\x1`)
- Lines that don't start/end with quotes
- Invalid escape sequences

## Optimization Considerations

### Current Approach (Optimal)
- Single pass through each line
- O(1) space complexity
- No string concatenation or rebuilding
- Direct character counting

### Why This Is Optimal
- We don't need to actually decode the strings, just count characters
- Each character is examined at most once
- No additional data structures needed
- For the given input size (~300 lines), this will execute in milliseconds

### Alternative Approaches Considered
1. **Using Python's string literal evaluation**: Could use `ast.literal_eval()` to decode strings
   - **Potential advantage**: Uses Python's built-in parser, guaranteed correct for valid Python strings
   - **Disadvantages**:
     - Would need to count characters in the result afterward (not more efficient)
     - Slower due to AST parsing overhead
     - The problem is about understanding the encoding, not actually decoding the strings
     - Manual parsing gives us more control and insight into the process
   - **Verdict**: Manual parsing is simpler and more direct for this use case

2. **Regex-based parsing**: Could use regex to find and replace escape sequences:
   - More complex to implement correctly (especially for hex escapes)
   - Similar performance to manual parsing
   - Harder to debug when issues arise
   - No significant advantage over clear iterative approach
   - **Verdict**: Not recommended for this problem

## File Structure
```
solution.py          # Main implementation file
input.md            # Input data (300 string literals)
implementation_plan.md  # This file
test_plan.md        # Testing plan
```

## Conclusion
The implementation uses a straightforward single-pass algorithm that is both optimal in time complexity and easy to understand and verify. Given the small input size, performance is not a concern, but the algorithm scales linearly with input size.
