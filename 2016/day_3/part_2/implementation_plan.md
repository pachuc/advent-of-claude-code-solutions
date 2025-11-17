# Implementation Plan - Triangle Validation (Part 2)

## Overview
Adapt the Part 1 solution to read triangles vertically (by columns) instead of horizontally (by rows). The input is processed in groups of 3 consecutive rows, where each column within a group represents one triangle.

## Key Changes from Part 1
- **Part 1**: Each row → 1 triangle (horizontal reading)
- **Part 2**: Every 3 rows → 3 triangles (vertical reading by columns)

## Algorithm Design

### Time Complexity
- **O(n)** where n is the number of lines
- Each line is read once and processed in constant time
- No nested loops or complex operations

### Space Complexity
- **O(1)** constant space
- Only need to store 3 rows at a time
- Counter variables use constant space

## Implementation Steps

### 1. Reuse Core Validation Logic from Part 1
The `is_valid_triangle(a, b, c)` function from Part 1 remains identical:
- Check triangle inequality theorem
- Return True if `(a + b > c) and (a + c > b) and (b + c > a)`
- **No changes needed** - copy from `part_1_solution.py`

### 2. Modify Input Reading Strategy
Instead of processing line-by-line, process in groups of 3 rows:

**Algorithm**:
```python
def count_valid_triangles_vertical(filename):
    lines = read_input(filename)
    count = 0

    # Process lines in groups of 3
    # Use len(lines) - 2 to ensure we have at least 3 lines remaining
    for i in range(0, len(lines) - 2, 3):
        # Parse the 3 rows
        row1 = parse_line(lines[i])
        row2 = parse_line(lines[i + 1])
        row3 = parse_line(lines[i + 2])

        # Skip if any row is invalid
        if None in (row1, row2, row3):
            continue

        # Extract triangles from columns
        triangle1 = (row1[0], row2[0], row3[0])  # Column 1
        triangle2 = (row1[1], row2[1], row3[1])  # Column 2
        triangle3 = (row1[2], row2[2], row3[2])  # Column 3

        # Validate each triangle
        for triangle in [triangle1, triangle2, triangle3]:
            if is_valid_triangle(*triangle):
                count += 1

    return count
```

**Note**: Using `range(0, len(lines) - 2, 3)` ensures we only iterate when we have at least 3 complete lines, eliminating the need for an explicit boundary check inside the loop. This is cleaner and more efficient than checking `if i + 2 >= len(lines)` inside the loop.

### 3. Reuse Parsing Functions from Part 1
- `read_input(filename)`: Read all lines - **no changes needed**
- `parse_line(line)`: Parse 3 integers from a line - **no changes needed**
- Both functions work exactly as in Part 1

### 4. Create Main Function
Update the main entry point to use the new vertical counting function:
```python
def main():
    result = count_valid_triangles_vertical('input.md')
    print(result)
```

## Code Structure

```
part_2_solution.py
├── read_input(filename)              [Copy from Part 1]
├── parse_line(line)                  [Copy from Part 1]
├── is_valid_triangle(a, b, c)        [Copy from Part 1]
├── count_valid_triangles_vertical()  [NEW - Main logic change]
└── main()                            [Modified to call new function]
```

## Edge Cases to Handle

1. **Incomplete groups**: If total lines is not divisible by 3
   - Use `range(0, len(lines) - 2, 3)` to automatically handle this
   - Only iterates when we have at least 3 lines remaining
   - Incomplete groups at the end are automatically skipped

2. **Invalid rows**: Any row that can't be parsed
   - Check if any of `row1`, `row2`, `row3` is `None`
   - Skip the entire group if any row is invalid

3. **Empty input**: No lines in file
   - `range(0, -2, 3)` produces empty range (no iterations)
   - Returns count of 0

4. **1 or 2 lines**: Input with fewer than 3 lines
   - `range(0, len(lines) - 2, 3)` produces empty range when `len(lines) < 3`
   - Returns count of 0

## Example Walkthrough

Given input:
```
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
```

**Processing**:
- **Group 1 (rows 0-2)**:
  - Triangle 1: (101, 102, 103) from column 1
  - Triangle 2: (301, 302, 303) from column 2
  - Triangle 3: (501, 502, 503) from column 3

- **Group 2 (rows 3-5)**:
  - Triangle 4: (201, 202, 203) from column 1
  - Triangle 5: (401, 402, 403) from column 2
  - Triangle 6: (601, 602, 603) from column 3

Each triangle is validated using the triangle inequality theorem.

## Performance Considerations

- **Input size**: 1993 lines in input.md = 664 groups of 3 = 1992 triangles analyzed
- **Operations per triangle**: 3 comparisons (constant time)
- **Total operations**: ~6000 comparisons
- **Expected runtime**: < 1ms (very efficient)

## Implementation Order

1. Copy `read_input()`, `parse_line()`, and `is_valid_triangle()` from Part 1
2. Implement `count_valid_triangles_vertical()` with the new column-based logic
3. Update `main()` to call the new function
4. Test with the example from problem.md
5. Run on full input.md
