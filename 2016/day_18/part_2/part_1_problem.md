# Problem Report: Safe Tile Counter

## Objective
Calculate the total number of safe tiles in a room with trap-based floor tiles across multiple rows.

## Context
We have a room with pressure plate traps arranged in rows. The tiles follow a pattern where each row is generated based on the previous row. We need to determine how many safe tiles exist across all rows to navigate the room safely.

## Input
- A single string representing the first row of tiles
- Each character is either:
  - `.` = safe tile
  - `^` = trap tile
- Example input: `.^^^^^.^^.^^^.^...^..^^.^.^..^^^^^^^^^^..^...^^.^..^^^^..^^^^...^.^.^^^^^^^^....^..^^^^^^.^^^.^^^.^^`

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

In all other situations, the new tile is **safe** (`.`).

## Example
Starting with: `..^^.`
- Row 2: `.^^^^`
- Row 3: `^^..^`

## Output Requirements
- Generate a total of **40 rows** (including the starting row)
- Count and return the total number of safe tiles (`.` characters) across all 40 rows
- Output should be a single integer representing the count

## Expected Output Format
A single integer (e.g., `38` for the 10-row example given in the puzzle)
