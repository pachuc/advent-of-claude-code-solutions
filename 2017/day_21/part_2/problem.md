# Problem Report: Fractal Art Pattern Enhancement (Part 2)

## Objective
Count how many pixels are "on" (represented by `#`) after performing **18 iterations** (instead of 5) of the pattern enhancement process on a starting grid.

## Context from Part 1
In Part 1, we implemented a fractal art generation program that repeatedly enhances an image using transformation rules. The program successfully counted pixels after 5 iterations and returned **173** as the answer.

Part 2 uses the exact same algorithm and rules but requires running for **18 iterations** instead of 5, which will produce a much larger grid.

## Initial State
The program always starts with this 3x3 pattern:
```
.#.
..#
###
```

## Algorithm (Same as Part 1)

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
Repeat steps 1-4 for **18 iterations** (this is the change from Part 1).

## Input Format
The input consists of enhancement rules, one per line, in the format:
```
input_pattern => output_pattern
```

Where patterns use slashes (`/`) to separate rows. For example:
- `../.#` represents a 2x2 grid
- `.#./..#/###` represents a 3x3 grid
- `##./#../...` represents a 3x3 grid

## Expected Output
A single integer representing the total count of "on" pixels (`#`) in the grid after exactly **18 iterations**.

## Implementation Notes
1. The algorithm is identical to Part 1
2. The only change is the number of iterations: **18 instead of 5**
3. The grid will be significantly larger after 18 iterations
4. Performance may be a consideration - the grid grows exponentially with each iteration
5. Grid size progression: 3→4→6→9→12→18→27→36→54→81→108→162→243→324→486→729→1094→1641→2187 pixels per side (approximately)

## Reference
- Part 1 solution returned **173** pixels after 5 iterations
- Part 1 solution code can be reused with just changing the iteration count from 5 to 18
