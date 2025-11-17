# Implementation Plan: Safe Tile Counter

## Problem Analysis

This is a cellular automaton problem similar to Conway's Game of Life but with simpler rules. We need to:
1. Start with an initial row configuration
2. Generate 39 more rows based on trap generation rules
3. Count all safe tiles (`.`) across all 40 rows

### Key Observations

**Rule Pattern Recognition:**
The four trap conditions can be simplified using XOR logic:
- A tile becomes a trap when the left and right tiles differ (one is trap, one is safe)
- This is equivalent to: `left XOR right` when center doesn't matter in the pattern

The four conditions are:
1. `^^ .` → trap (left and center traps, right safe)
2. `. ^^` → trap (center and right traps, left safe)
3. `^. .` → trap (only left trap)
4. `. .^` → trap (only right trap)

Pattern: trap if `left != right` (XOR relationship)

**Algorithm Complexity:**
- Time: O(n × m) where n = number of rows (40), m = row length (~100)
- Space: O(m) - we only need to keep the current row in memory
- Total operations: ~4,000 - very efficient

## Solution Overview

**Approach**:
1. Read the initial row pattern from input.md
2. Generate each subsequent row by applying trap rules to the previous row
3. Count safe tiles (`.`) across all 40 rows
4. Output the total count

**Key Design Decisions**:
- **Input Method**: Read directly from `input.md` (hardcoded) with 40 rows (hardcoded)
- **Algorithm**: Simple XOR-based rule (`left != right`) for trap detection
- **Memory**: Only store current row, not all rows (O(m) space)
- **No CLI Arguments**: This is a single-purpose script for solving one AoC problem

## Implementation Steps

### Step 1: Input Parsing
```python
def parse_input(filename='input.md'):
    """
    Read the first row from input file.

    The input file contains the puzzle input as the first line.
    Since the file is named input.md, it may have markdown formatting,
    but the actual input is just the raw tile string on the first line.

    Args:
        filename: path to input file (default: 'input.md')

    Returns:
        str: first row of tiles (stripped of whitespace)

    Implementation:
    - Open the file and read the first line
    - Strip whitespace and newlines using .strip()
    - Return the cleaned string
    - Note: If file doesn't exist, let Python raise FileNotFoundError naturally
    """
```

### Step 2: Trap Detection Logic
```python
def is_trap(left, center, right):
    """
    Determine if a tile should be a trap based on the three tiles above it.

    The four trap conditions can be simplified using XOR logic.
    Truth table showing the pattern:

    Left | Right | Trap?
    -----|-------|------
      ^  |   ^   | False (both traps)
      ^  |   .   | True  (differ)
      .  |   ^   | True  (differ)
      .  |   .   | False (both safe)

    Pattern: A tile is a trap if and only if left != right (XOR relationship)
    Note: The center tile is actually irrelevant to the outcome!

    Args:
        left: character for left tile ('^' or '.')
        center: character for center tile ('^' or '.')
        right: character for right tile ('^' or '.')

    Returns:
        bool: True if new tile is a trap, False if safe

    Implementation:
    - Simply return: left != right
    - This elegant solution covers all four conditions
    """
```

### Step 3: Row Generation
```python
def generate_next_row(current_row):
    """
    Generate the next row based on current row using trap rules.

    Args:
        current_row: string representing current row

    Returns:
        str: next row as string
    """
    - Initialize empty result list
    - For each position i in range(len(current_row)):
        - Get left tile: current_row[i-1] if i > 0, else '.'
        - Get center tile: current_row[i]
        - Get right tile: current_row[i+1] if i < len-1, else '.'
        - Determine if position is trap using is_trap()
        - Append '^' or '.' to result
    - Join and return result string
```

### Step 4: Main Counting Logic
```python
def count_safe_tiles(first_row, total_rows):
    """
    Count total safe tiles across all rows.

    Args:
        first_row: initial row configuration
        total_rows: number of rows to generate (including first)

    Returns:
        int: total count of safe tiles
    """
    - Initialize safe_count = 0
    - Set current_row = first_row
    - For row_num in range(total_rows):
        - Count '.' characters in current_row
        - Add to safe_count
        - If not last row:
            - Generate next row using generate_next_row()
            - Set current_row to new row
    - Return safe_count
```

### Step 5: Main Execution
```python
def main():
    """
    Main entry point for the solution.

    This script is designed to solve the specific Advent of Code problem:
    - Reads from 'input.md' (hardcoded)
    - Generates exactly 40 rows (as specified in problem)
    - Outputs a single integer result
    """
    - Call parse_input() to read from 'input.md'
    - Call count_safe_tiles(first_row, 40)
    - Print the result as a single integer

# Script entry point
if __name__ == '__main__':
    main()
```

## Optimization Considerations

### Space Efficiency
- We only need to keep one row in memory at a time
- No need to store all 40 rows
- Current approach: O(m) space where m is row length

### Time Efficiency
- Each row generation is O(m) where m is row length
- Total time: O(n × m) = O(40 × 100) = O(4000) operations
- This is highly efficient for the problem size

### Alternative Optimizations (Not Needed)
- Could use bit manipulation for faster operations
- Could parallelize row generation (overkill for 40 rows)
- Could memoize patterns (unlikely to repeat significantly)

## Implementation Details

### Edge Case Handling
1. **Boundary conditions**: Treat out-of-bounds as safe tiles ('.')
2. **Empty input**: Should handle gracefully (though not expected)
3. **Single character row**: Should work with boundary rules

### Data Structures
- Use strings for rows (immutable, simple to work with)
- Could use lists for faster character access, but strings are fine for this size

### Code Structure
```
solution.py
├── parse_input()
├── is_trap()
├── generate_next_row()
├── count_safe_tiles()
└── main()
```

## Expected Behavior

For the example `..^^.` over 3 rows:
```
Row 1: ..^^.  (3 safe tiles)
Row 2: .^^^^  (1 safe tile)
Row 3: ^^..^  (2 safe tiles)
Total: 6 safe tiles
```

For 10 rows with pattern `.^^.^.^^^^`, expected output is 38 safe tiles.

For actual input (40 rows with the provided pattern), we expect the output to be between 0 and 4000 (the maximum possible safe tiles for 40 rows of ~100 tiles each). The exact value will be determined by running the solution.
