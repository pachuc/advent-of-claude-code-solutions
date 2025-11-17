# Problem Report: Safe Tile Counter (Part 2)

## Objective
Calculate the total number of safe tiles in a room with trap-based floor tiles across **400,000 rows** (scaled up from Part 1's 40 rows).

## Context from Part 1
This is a continuation of Part 1, where we successfully counted safe tiles across 40 rows and found the answer to be **1989**. The algorithm and rules remain exactly the same - only the number of rows to generate has increased dramatically.

We have a room with pressure plate traps arranged in rows. The tiles follow a pattern where each row is generated based on the previous row. We need to determine how many safe tiles exist across all rows to navigate the room safely.

## Input
- A single string representing the first row of tiles
- Each character is either:
  - `.` = safe tile
  - `^` = trap tile
- Actual input: `.^^^^^.^^.^^^.^...^..^^.^.^..^^^^^^^^^^..^...^^.^..^^^^..^^^^...^.^.^^^^^^^^....^..^^^^^^.^^^.^^^.^^`

## Row Generation Rules
Each subsequent row is generated from the previous row using these rules:

For each position in the new row, examine three tiles from the previous row:
- **Left**: tile at position-1 (or "safe" if out of bounds)
- **Center**: tile at position
- **Right**: tile at position+1 (or "safe" if out of bounds)

A new tile is a **trap** (`^`) if and only if one of these conditions is true:
1. Left and center are traps, but right is not
2. Center and right are traps, but left is not
3. Only left is a trap (center and right are safe)
4. Only right is a trap (left and center are safe)

**Simplified rule**: A tile is a trap if and only if `left != right`

In all other situations, the new tile is **safe** (`.`).

## Output Requirements
- Generate a total of **400,000 rows** (including the starting row)
- Count and return the total number of safe tiles (`.` characters) across all 400,000 rows
- Output should be a single integer representing the count

## Expected Output Format
A single integer representing the total count of safe tiles

## Notes
- Part 1 algorithm can be reused directly - just change the row count from 40 to 400,000
- With 400,000 rows, efficiency may become a consideration, but the algorithm is already O(n*m) where n is the number of rows and m is the row width, which should be acceptable
- No need to store all rows in memory - can count safe tiles row by row
