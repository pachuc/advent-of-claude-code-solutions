# Implementation Plan: Password Scrambler

## Overview
Implement a password scrambling system that applies 6 different types of operations sequentially to transform an initial password string (`abcdefgh`) according to 100 operations specified in the input file.

## Algorithm Analysis

### Time Complexity
- Total operations: 100
- String length: 8 characters (constant)
- Each operation: O(n) where n = 8
- Overall: O(100 × 8) = O(1) since both values are constants
- **Conclusion**: No efficiency concerns; straightforward sequential processing is optimal

### Space Complexity
- O(n) for storing the string (n = 8)
- O(1) additional space for parsing and operations
- **Conclusion**: Minimal memory usage

## Implementation Steps

### Step 1: Project Structure Setup
**Goal**: Create the basic file structure and imports

**Actions**:
- Create main Python script (e.g., `solution.py`)
- Import necessary modules:
  - `re` for parsing operation strings
  - No other special libraries needed

### Step 2: Input Parsing Module
**Goal**: Read and parse the input file containing operations

**Actions**:
- Create function `read_operations(filename)`:
  - Read the input file line by line
  - Strip whitespace from each line
  - Filter out empty lines
  - Return list of operation strings

**Implementation details**:
```python
def read_operations(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]
```

### Step 3: Operation Parser
**Goal**: Parse each operation string and extract parameters

**Actions**:
- Create function `parse_operation(operation_str)`:
  - Use regex or string splitting to identify operation type
  - Extract relevant parameters (positions, letters, steps)
  - Return tuple: (operation_type, parameters)

**Operation patterns to match**:
1. `swap position X with position Y` → extract X, Y as integers
2. `swap letter X with letter Y` → extract X, Y as characters
3. `rotate left X steps` / `rotate right X steps` → extract direction and X as integer
4. `rotate based on position of letter X` → extract X as character
5. `reverse positions X through Y` → extract X, Y as integers
6. `move position X to position Y` → extract X, Y as integers

**Implementation approach**:
- Use conditional checks with `startswith()` or regex patterns
- Example: `if operation.startswith('swap position'):`

### Step 4: Core Operation Functions
**Goal**: Implement each of the 6 operation types

#### 4.1: Swap Position
```python
def swap_position(s, x, y):
    # Convert string to list for mutability
    # Swap characters at indices x and y
    # Return as string
```
**Logic**: Direct index swap using list conversion

#### 4.2: Swap Letter
```python
def swap_letter(s, x, y):
    # Convert string to list for mutability
    # Iterate through list, swap x with y and y with x
    # Return as string
    # Alternative: use replace with '\x00' as placeholder (null character)
```
**Logic**: Convert to list and swap character-by-character to avoid placeholder conflicts. This ensures correctness even if x or y don't exist in the string (no-op behavior).

#### 4.3: Rotate Left/Right
```python
def rotate_left(s, steps):
    # Normalize steps to be within string length (steps % len(s))
    # Handle empty string or steps = 0
    # Slice string: s[steps:] + s[:steps]

def rotate_right(s, steps):
    # Normalize steps (steps % len(s))
    # Handle edge case: if steps = 0, return s unchanged
    # Use rotate_left with (len(s) - steps) to avoid s[:-0] issue
    # Alternative: if steps == 0: return s; else: s[-steps:] + s[:-steps]
```
**Logic**: String slicing with proper wraparound handling. Important: `s[:-0]` returns empty string, so normalize steps first or use rotate_left approach.

#### 4.4: Rotate Based on Position
```python
def rotate_based_on_letter(s, letter):
    # Find index of letter in current string using s.index(letter)
    # Calculate rotation: 1 + index + (1 if index >= 4 else 0)
    # Call rotate_right with calculated steps
```
**Logic**: Find index using `s.index(letter)`, apply rotation formula. The index is found in the **current** string state before rotation, not the original password.

**Example**: For string `ecabd` with letter `d`:
- Find `d` at index 4
- Calculate: 1 + 4 + 1 = 6 steps (since 4 >= 4)
- Rotate right 6 steps: 6 % 5 = 1, so `ecabd` → `decab`

#### 4.5: Reverse Positions
```python
def reverse_positions(s, x, y):
    # Convert to list
    # Reverse slice from x to y+1 (inclusive)
    # s[x:y+1] = s[x:y+1][::-1]
    # Return as string
```
**Logic**: Slice reversal using Python's slice notation

#### 4.6: Move Position
```python
def move_position(s, x, y):
    # Convert to list
    # Remove character at index x: char = lst.pop(x)
    # Insert at index y: lst.insert(y, char)
    # Return as string
```
**Logic**: List pop and insert operations

### Step 5: Main Execution Engine
**Goal**: Orchestrate the entire scrambling process

**Actions**:
- Create function `scramble_password(initial, operations)`:
  - Initialize current password = initial
  - For each operation in operations:
    - Parse the operation
    - Dispatch to appropriate operation function
    - Update current password with result
  - Return final password

**Implementation structure**:
```python
def scramble_password(initial, operations):
    password = initial
    for operation in operations:
        op_type, params = parse_operation(operation)

        if op_type == 'swap_position':
            password = swap_position(password, params[0], params[1])
        elif op_type == 'swap_letter':
            password = swap_letter(password, params[0], params[1])
        # ... handle all 6 operation types

    return password
```

### Step 6: Main Entry Point
**Goal**: Wire everything together and execute

**Actions**:
- Create main function or script entry point:
  - Define initial password: `abcdefgh`
  - Read operations from input file
  - Call scramble function
  - Print final result

**Implementation**:
```python
def main():
    initial_password = 'abcdefgh'
    operations = read_operations('input.md')
    final_password = scramble_password(initial_password, operations)
    print(final_password)

if __name__ == '__main__':
    main()
```

## Implementation Considerations

### String Immutability Handling
- Python strings are immutable
- Convert to list for operations that modify in place
- Convert back to string after modification
- Alternative: use string slicing and concatenation (slower but cleaner for some operations)

### Index Validation
- All indices should be valid based on input assumptions
- Input is assumed to be well-formed (no need for extensive error handling)
- String length remains constant at 8 characters throughout
- For `swap_letter`: if a letter doesn't exist, operation acts as no-op (graceful handling)

### Rotation Edge Cases
- Handle steps > string length using modulo operator: `steps % len(s)`
- Handle steps = 0 (no-op): check explicitly or use modulo normalization
- **Critical**: For rotate_right, avoid `s[:-0]` which returns empty string
  - Solution 1: `if steps == 0: return s`
  - Solution 2: Use `rotate_left(s, len(s) - steps)` after normalization

### Parsing Strategy
- **Recommended approach**: Use simple string methods (startswith, split) for clarity
- Extract numbers using `split()` and conversion to int
- Extract letters directly from known positions after split
- Regex alternative available but not necessary for well-formed input

**Example parsing returns**:
- `"swap position 7 with position 1"` → `('swap_position', (7, 1))`
- `"swap letter e with letter d"` → `('swap_letter', ('e', 'd'))`
- `"rotate left 2 steps"` → `('rotate_left', 2)`
- `"rotate based on position of letter a"` → `('rotate_based', 'a')`

## Code Organization

```
solution.py
├── read_operations()           # Input parsing
├── parse_operation()           # Operation string parsing
├── swap_position()             # Operation 1
├── swap_letter()               # Operation 2
├── rotate_left()               # Operation 3a
├── rotate_right()              # Operation 3b
├── rotate_based_on_letter()    # Operation 4
├── reverse_positions()         # Operation 5
├── move_position()             # Operation 6
├── scramble_password()         # Main orchestrator
└── main()                      # Entry point
```

## Expected Development Time
- Estimated implementation: 30-45 minutes
- Testing and debugging: 15-30 minutes
- Total: ~1 hour

## Final Output
- Single line containing the scrambled password (8 characters)
- No additional formatting, newlines, or debug output in production run
