# Implementation Plan: Triangle Validation

## Overview
Implement a Python script to count the number of valid triangles from a list of triangle specifications using the triangle inequality theorem.

## Plan Status
**Status**: Approved (based on critique feedback)
**Last Updated**: After incorporating critique recommendations

This plan has been reviewed and approved. The algorithm is optimal (O(n) is the best possible), the code structure is modular and testable, and the approach is appropriately scoped for a script-based solution.

## Algorithm Selection

**Chosen Approach**: Linear scan with validation
- **Time Complexity**: O(n) where n is the number of triangles
- **Space Complexity**: O(1) - only storing counter
- **Rationale**: The problem requires checking each triangle exactly once. No optimization beyond O(n) is possible since we must examine each input.

## Step-by-Step Implementation

### Step 1: Input Reading
**File**: `solution.py`

**Implementation**:
```python
def read_input(filename='input.md'):
    """Read triangle specifications from input file."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines
```

**Details**:
- Read all lines from the input file
- No preprocessing needed - will parse line by line
- Handle file I/O with context manager for proper resource cleanup

### Step 2: Triangle Validation Function
**Function**: `is_valid_triangle(a, b, c)`

**Implementation**:
```python
def is_valid_triangle(a, b, c):
    """
    Check if three sides can form a valid triangle.

    Triangle inequality theorem: sum of any two sides must be
    greater than the third side.

    Args:
        a, b, c: Integer side lengths

    Returns:
        bool: True if valid triangle, False otherwise
    """
    return (a + b > c) and (a + c > b) and (b + c > a)
```

**Logic**:
- Check all three conditions of triangle inequality
- Return True only if ALL conditions are satisfied
- Simple boolean logic with short-circuit evaluation for efficiency

**Important Note**:
- ALL three inequalities must be strictly greater than (>), not greater than or equal to (>=)
- Example: sides (5, 5, 10) is INVALID because 5 + 5 = 10, which is NOT > 10
- Example: sides (910, 265, 611) is INVALID because 265 + 611 = 876, which is NOT > 910

**Why this approach**:
- Direct implementation of mathematical definition
- Clear and readable
- All three checks are necessary - no optimization possible
- Short-circuit evaluation stops checking as soon as one condition fails

### Step 3: Line Parsing
**Function**: `parse_line(line)`

**Implementation**:
```python
def parse_line(line):
    """
    Parse a line containing three space-separated integers.

    Args:
        line: String with three integers

    Returns:
        tuple: (a, b, c) as integers, or None if invalid
    """
    parts = line.strip().split()
    if len(parts) != 3:
        return None
    try:
        a, b, c = int(parts[0]), int(parts[1]), int(parts[2])
        return (a, b, c)
    except ValueError:
        return None
```

**Details**:
- Strip whitespace and split on spaces
- Validate exactly 3 values present
- Convert to integers with error handling
- Return None for invalid lines (skip them)

### Step 4: Main Counting Logic
**Function**: `count_valid_triangles(filename='input.md')`

**Implementation**:
```python
def count_valid_triangles(filename='input.md'):
    """
    Count valid triangles from input file.

    Args:
        filename: Path to input file

    Returns:
        int: Number of valid triangles
    """
    count = 0
    lines = read_input(filename)

    for line in lines:
        sides = parse_line(line)
        if sides is None:
            continue  # Skip invalid lines

        a, b, c = sides
        if is_valid_triangle(a, b, c):
            count += 1

    return count
```

**Logic**:
1. Initialize counter to 0
2. Read all lines from input
3. For each line:
   - Parse the three side lengths
   - Skip if parsing fails
   - Check triangle validity
   - Increment counter if valid
4. Return total count

### Step 5: Main Entry Point
**Implementation**:
```python
def main():
    """Main entry point."""
    result = count_valid_triangles('input.md')
    print(result)

if __name__ == '__main__':
    main()
```

**Details**:
- Call counting function
- Print result to stdout
- Standard Python entry point pattern

## Complete File Structure

**File**: `solution.py`

**Organization**:
1. Import statements (if needed - none required for this problem)
2. Helper functions:
   - `read_input()`
   - `parse_line()`
   - `is_valid_triangle()`
3. Main function:
   - `count_valid_triangles()`
4. Entry point:
   - `main()`
   - `if __name__ == '__main__'` block

## Error Handling Strategy

**Minimal error handling** - as specified, we're writing a script, not production code:
- Parse errors: Skip invalid lines silently
- File not found: Let Python raise exception (acceptable for script)
- Invalid data types: Catch in parse_line, return None

## Performance Considerations

**Current input size**: ~2000 triangles

**Performance analysis**:
- Reading file: O(n) - unavoidable
- Parsing each line: O(1) per line - simple split and int conversion
- Validation: O(1) per triangle - three comparisons
- Total: O(n) where n = number of lines

**Optimization notes**:
- No optimization needed - algorithm is already optimal
- Could use generators to reduce memory, but 2000 lines is trivial
- Short-circuit evaluation in validation already optimizes false cases

## Testing Approach
- Verify with example from problem: `5 10 25` should be invalid (5+10=15 NOT > 25)
- Test with known valid triangles: `3 4 5`, `5 5 5`, `5 5 8`
- Test boundary cases: `5 5 10` (invalid - equality doesn't count)
- Test pattern of large side with two medium sides: `910 265 611` (invalid - 265+611=876 NOT > 910)
- Test with actual input file
- Comprehensive edge cases documented in separate test plan

## Expected Output Format
Single integer printed to stdout representing the count of valid triangles.
