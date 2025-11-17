# Problem Report: Taxicab Distance Calculator

## Objective
Calculate the Manhattan distance (taxicab distance) from a starting position to a final position after following a series of directional instructions on a 2D street grid.

## Context
You start at coordinates (0, 0) facing North on a city grid. You need to follow a sequence of turn-and-move instructions to determine where you end up, then calculate how far you are from your starting position using Manhattan distance.

## Input Format
- A comma-separated sequence of instructions
- Each instruction consists of:
  - A direction: `L` (turn left 90 degrees) or `R` (turn right 90 degrees)
  - A number: the number of blocks to walk forward after turning
- Example: `R2, L3` means "turn right, walk 2 blocks, then turn left, walk 3 blocks"

## Rules and Constraints
1. Starting position: (0, 0)
2. Starting orientation: North
3. Turns are always 90 degrees (left or right)
4. After each turn, walk forward the specified number of blocks
5. Movement is constrained to a grid (only North, South, East, West directions)

## Expected Output
A single integer representing the Manhattan distance from the starting position to the final position.

Manhattan distance = |final_x - start_x| + |final_y - start_y| = |final_x| + |final_y|

## Examples

**Example 1:** `R2, L3`
- Start at (0, 0) facing North
- Turn right (now facing East), walk 2 blocks → position (2, 0)
- Turn left (now facing North), walk 3 blocks → position (2, 3)
- Distance: |2| + |3| = 5 blocks

**Example 2:** `R2, R2, R2`
- Start at (0, 0) facing North
- Turn right (East), walk 2 → (2, 0)
- Turn right (South), walk 2 → (2, -2)
- Turn right (West), walk 2 → (0, -2)
- Distance: |0| + |-2| = 2 blocks

**Example 3:** `R5, L5, R5, R3`
- Final distance: 12 blocks

## Input Data Location
The actual input sequence is provided in `input.md`
