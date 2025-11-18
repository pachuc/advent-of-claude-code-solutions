# Problem Report: Disk Defragmentation Grid Analysis

## Objective
Calculate the total number of "used" squares in a 128x128 grid representing disk usage.

## Context
We are simulating a disk defragmentation process where the disk is represented as a 128x128 grid. Each square in the grid is either "free" (0) or "used" (1). The state of the grid is determined by computing knot hashes for each row.

## Input
- A key string (puzzle input): `jxqlasbh`

## Algorithm Requirements

### Step 1: Generate Hash Inputs
For each of the 128 rows (indexed 0 to 127):
- Create an input string by concatenating: `{key}-{row_number}`
- Example: For key `flqrgnkx`, row 0 uses `flqrgnkx-0`, row 1 uses `flqrgnkx-1`, etc.

### Step 2: Compute Knot Hashes
For each row's input string:
- Calculate the knot hash (reference: Day 10 algorithm)
- The knot hash produces a 32-character hexadecimal string

### Step 3: Convert Hexadecimal to Binary
For each hexadecimal hash:
- Convert each hexadecimal digit to its 4-bit binary equivalent (high-bit first)
- Conversion examples:
  - `0` → `0000`
  - `1` → `0001`
  - `e` → `1110`
  - `f` → `1111`
  - `a` → `1010`
  - `c` → `1100`
- Example: `a0c2017...` becomes `10100000110000100000000101110000...`
- Each hash produces exactly 128 bits (32 hex digits × 4 bits each)

### Step 4: Build the Grid
- Each row's 128 bits represents one row in the 128x128 grid
- `1` bits represent "used" squares
- `0` bits represent "free" squares

### Step 5: Count Used Squares
- Count all `1` bits across the entire 128x128 grid

## Expected Output
- A single integer representing the total number of used squares in the grid

## Validation Example
For the test key `flqrgnkx`:
- Expected result: `8108` used squares

## Notes
- The knot hash algorithm is from a previous puzzle (Day 10)
- The grid is 128×128 because each knot hash produces 128 bits, and we compute 128 hashes (one per row)
- The actual puzzle input is: `jxqlasbh`
