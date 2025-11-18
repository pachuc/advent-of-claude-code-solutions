# Implementation Plan: Fractal Art Pattern Enhancement

## Overview
Implement a Python script to solve the fractal art enhancement problem by applying transformation rules iteratively to a grid, counting the number of "on" pixels after 5 iterations.

## Algorithm Complexity Analysis
- **Grid Growth**: 3 → 4 → 6 → 9 → 12 → 18 pixels per side after 5 iterations
- **Final Grid Size**: 18×18 = 324 cells (manageable for brute force)
- **Pattern Matching**: With ~108 rules and up to 8 orientations to check per pattern, this is O(rules × orientations) per sub-square
- **Overall Complexity**: O(iterations × (grid_size/sub_size)² × rules × 8) - acceptable for the given constraints

## Data Structures

### 1. Grid Representation
- Use a list of strings (each string is a row) for easy manipulation and pattern matching
- Example: `['.#.', '..#', '###']` for the initial 3×3 grid

### 2. Rule Storage
- Dictionary mapping pattern strings to output patterns
- Key: normalized pattern string (e.g., "../.#")
- Value: output pattern string (e.g., "##./#../...")
- Store ALL 8 orientations as separate keys for O(1) lookup instead of generating them on the fly

## Implementation Steps

### Step 1: Input Parsing
**Function**: `parse_rules(input_text)`
- Read the input line by line
- Split each line on " => " to separate input and output patterns
- For each rule, generate all 8 orientations of the input pattern
- Store all orientations in a dictionary mapping to the same output pattern
- Return the complete rule dictionary

**Why generate all orientations upfront?**
- Avoids repeated computation during iteration
- Trades memory (8× storage) for speed (O(1) lookup vs O(8) generation+comparison)
- With ~108 rules, this means ~864 dictionary entries - still very manageable

### Step 2: Pattern Transformation Functions
**Function**: `pattern_to_grid(pattern_str)`
- Convert slash-separated pattern string to list of strings
- Example: "../.#" → [".", ".#"]
- Return grid representation

**Function**: `grid_to_pattern(grid)`
- Convert list of strings back to slash-separated pattern
- Algorithm: `'/'.join(grid)`
- Example: ["..", ".#"] → "../.#"
- Return pattern string

**Function**: `rotate_grid(grid)`
- Rotate a grid 90 degrees clockwise
- Algorithm: new[i][j] = old[n-1-j][i] where n is grid size
- Return rotated grid

**Function**: `flip_grid(grid)`
- Flip a grid horizontally (reverse each row)
- Algorithm: new[i] = old[i][::-1]
- Return flipped grid

**Function**: `generate_all_orientations(pattern_str)`
- Convert pattern to grid
- Generate 4 rotations (0°, 90°, 180°, 270°)
- Flip the grid and generate 4 more rotations
- Convert each back to pattern string
- Return set of all unique pattern strings (use set to deduplicate symmetric patterns)

### Step 3: Grid Division and Enhancement
**Function**: `divide_grid(grid, block_size)`
- Determine how many blocks fit in each dimension: `num_blocks = len(grid) // block_size`
- Create a 2D list to store sub-grids
- Extract each block_size × block_size sub-grid
- Algorithm (for grid as list of strings):
  ```
  for block_row in range(num_blocks):
      for block_col in range(num_blocks):
          block = []
          for r in range(block_row * block_size, (block_row + 1) * block_size):
              # Extract the substring for this block's columns
              row_section = grid[r][block_col * block_size:(block_col + 1) * block_size]
              block.append(row_section)
          blocks[block_row][block_col] = block
  ```
- Return list of lists of sub-grids

**Function**: `enhance_block(block, rules)`
- Convert block (list of strings) to pattern string using `grid_to_pattern()`
- Look up pattern in rules dictionary
- **Error handling**: If pattern not found, raise an error with helpful message:
  ```python
  if pattern not in rules:
      raise KeyError(f"Pattern not found in rules: {pattern}")
  ```
- Convert output pattern to grid using `pattern_to_grid()`
- Return enhanced grid

**Function**: `reassemble_grid(enhanced_blocks)`
- Given a 2D list of enhanced blocks, combine them into a single grid
- Algorithm:
  ```
  for each row of blocks:
      for each row within the blocks:
          concatenate corresponding rows from all blocks in that block-row
  ```
- Return combined grid as list of strings

### Step 4: Main Iteration Loop
**Function**: `perform_iterations(initial_grid, rules, num_iterations)`
- Start with initial grid
- For each iteration (1 to num_iterations):
  1. Determine block size:
     - If len(grid) % 2 == 0: block_size = 2
     - Else: block_size = 3
  2. Divide grid into blocks
  3. Enhance each block using rules
  4. Reassemble into new grid
- Return final grid

### Step 5: Count On Pixels
**Function**: `count_on_pixels(grid)`
- Iterate through each row in grid
- Count '#' characters in each row
- Sum all counts
- Return total

### Step 6: Main Execution
**Function**: `main()`
1. Read input from file (`input.md`)
   - Read all lines from the file
   - Skip empty lines if any
   - Each line contains a rule in format: `input_pattern => output_pattern`
2. Parse rules and generate all orientations
3. Initialize starting grid: `['.#.', '..#', '###']`
4. Perform 5 iterations
5. Count on pixels in final grid
6. Print result as a single integer

## Implementation Order
1. Implement helper functions (pattern_to_grid, grid_to_pattern)
2. Implement transformation functions (rotate_grid, flip_grid, generate_all_orientations)
3. Implement rule parsing with orientation generation
4. Implement grid division and reassembly
5. Implement enhancement logic
6. Implement main iteration loop
7. Implement counting function
8. Tie everything together in main()

## Edge Cases to Handle in Code
1. **Grid size divisibility**: Always check grid size and use correct block size
2. **Pattern matching**: Ensure all 8 orientations are pre-generated to guarantee matches
3. **Grid boundaries**: Ensure division and reassembly maintain correct grid dimensions
4. **Empty patterns**: Not expected in valid input, but could validate rules exist

## Optimization Considerations
1. **Pre-generate all orientations**: Done during rule parsing (one-time cost)
2. **Use dictionary for O(1) lookup**: Instead of checking orientations during matching
3. **String operations**: Keep grids as lists of strings for efficient slicing and concatenation
4. **Avoid deep copying**: Work with references where possible, only create new objects when necessary

## File Structure
```
solution.py         # Main implementation file
input.md           # Input rules (provided)
```

## Expected Output Format
Single integer representing the count of '#' pixels after 5 iterations.
