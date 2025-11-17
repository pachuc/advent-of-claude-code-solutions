# Problem Report: First Location Visited Twice

## Objective
Find the Manhattan distance from the starting position to the **first location you visit twice** while following a series of directional instructions on a 2D street grid.

## Context from Part 1
In Part 1, we calculated the Manhattan distance to the final destination after following all instructions. We started at coordinates (0, 0) facing North on a city grid and followed a sequence of turn-and-move instructions. The Part 1 solution found that the final destination was 300 blocks away.

## Part 2 - The New Challenge
The instructions continue on the back of the document revealing that Easter Bunny HQ is **not** at the final destination, but rather at the **first location you visit twice** (the first location where your path crosses itself).

**Key Difference from Part 1:** Instead of tracking just the final position, we must now track **every position we visit** and detect when we visit a location for the second time.

## Important Detail: Track Every Block, Not Just Intersections
When moving forward by N blocks, you must track **each individual block** along the path, not just the final position after the move. For example, if you move 5 blocks north from (0, 0), you visit positions (0, 1), (0, 2), (0, 3), (0, 4), and (0, 5) - all of these must be checked for revisits.

## Input Format
- A comma-separated sequence of instructions (same as Part 1)
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
6. **Track each individual position visited along the path (not just intersections after completing each instruction)**
7. Stop as soon as you visit any location for the second time

## Expected Output
A single integer representing the Manhattan distance from the starting position (0, 0) to the first location visited twice.

Manhattan distance = |x| + |y|

## Example

**Example:** `R8, R4, R4, R8`
- Start at (0, 0) facing North
- Turn right (now facing East), walk 8 blocks → visits (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)
- Turn right (now facing South), walk 4 blocks → visits (8, -1), (8, -2), (8, -3), (8, -4)
- Turn right (now facing West), walk 4 blocks → visits (7, -4), (6, -4), (5, -4), (4, -4)
- Turn right (now facing North), walk 8 blocks → visits (4, -3), (4, -2), (4, -1), (4, 0) ← **STOP!**
  - (4, 0) was already visited during the first instruction
  - This is the first location visited twice
- Distance: |4| + |0| = 4 blocks

## Algorithm Requirements
1. Parse the input instructions (same as Part 1)
2. Start at (0, 0) facing North
3. Maintain a set of all visited positions
4. For each instruction:
   - Apply the turn (left or right)
   - Move forward one block at a time for the specified number of steps
   - For each individual block moved:
     - Check if the current position has been visited before
     - If yes, this is the answer - calculate and return the Manhattan distance
     - If no, add the position to the visited set and continue
5. Return the Manhattan distance to the first revisited location

## Input Data Location
The actual input sequence is provided in `input.md`
