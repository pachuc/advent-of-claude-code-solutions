# Problem Report: Fractal Art Pattern Enhancement

## Objective
Count how many pixels are "on" (represented by `#`) after performing 5 iterations of a pattern enhancement process on a starting grid.

## Context
We're simulating an art generation program that repeatedly enhances an image using a set of transformation rules. The image is a 2D square grid where pixels can be either on (`#`) or off (`.`). The grid grows larger with each iteration as smaller squares are replaced by bigger ones.

## Initial State
The program always starts with this 3x3 pattern:
```
.#.
..#
###
```

## Algorithm

### Step 1: Determine Grid Division
At each iteration, check if the current grid size is:
- **Divisible by 2**: Break the grid into 2x2 squares, and convert each 2x2 square into a 3x3 square
- **Divisible by 3**: Break the grid into 3x3 squares, and convert each 3x3 square into a 4x4 square

### Step 2: Pattern Matching with Transformations
For each sub-square extracted from the grid:
- Look up the matching enhancement rule from the input
- **Important**: The input pattern may need to be rotated or flipped to find a match in the rules
- All 8 possible orientations should be considered (original, 3 rotations, flip, and 3 rotations of the flip)
- **Never** rotate or flip the output pattern, only the input

### Step 3: Apply Enhancement Rule
Replace each sub-square with its corresponding enhanced square based on the matched rule.

### Step 4: Reassemble Grid
Combine all the enhanced squares back into a single larger grid.

### Step 5: Repeat
Repeat steps 1-4 for the specified number of iterations (5 iterations for this problem).

## Input Format
The input consists of enhancement rules, one per line, in the format:
```
input_pattern => output_pattern
```

Where patterns use slashes (`/`) to separate rows. For example:
- `../.#` represents a 2x2 grid
- `.#./..#/###` represents a 3x3 grid
- `##./#../...` represents a 3x3 grid

Examples:
```
../.# => ##./#../...
```
This means the 2x2 pattern:
```
..
.#
```
should be replaced with the 3x3 pattern:
```
##.
#..
...
```

## Expected Output
A single integer representing the total count of "on" pixels (`#`) in the grid after exactly 5 iterations.

## Example
With simplified rules:
```
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
```

After 2 iterations starting from the initial pattern, the result is:
```
##.##.
#..#..
......
##.##.
#..#..
......
```
Which contains **12** pixels that are on.

## Implementation Notes
1. The input pattern must be matched against rules by trying all possible rotations and flips
2. Only the input pattern is transformed for matching - the output pattern is always used as-is
3. Grid size will grow with each iteration (3→4→6→9→12→18 for the first 5 iterations)
4. The grid must be evenly divisible into squares at each step
