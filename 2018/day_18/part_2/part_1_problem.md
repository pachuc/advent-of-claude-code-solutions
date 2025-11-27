# Problem Report: Lumber Collection Area Simulation

## Objective
Calculate the total resource value of a lumber collection area after simulating 10 minutes of landscape transformation.

## Context
We're simulating a magical landscape where acres of land undergo transformations each minute based on their current state and the state of adjacent acres. The landscape consists of a grid where each position can be open ground, trees, or a lumberyard.

## Input Description
- A 50x50 grid representing the lumber collection area
- Each cell can be one of three types:
  - `.` = open ground
  - `|` = trees (wooded acre)
  - `#` = lumberyard
- Input format: 50 lines of text, each containing 50 characters

## Transformation Rules
The landscape changes every minute based on these rules (applied simultaneously to all acres):

1. **Open ground (`.`)**: Becomes trees (`|`) if 3 or more adjacent acres contain trees. Otherwise, remains open.

2. **Trees (`|`)**: Becomes a lumberyard (`#`) if 3 or more adjacent acres are lumberyards. Otherwise, remains trees.

3. **Lumberyard (`#`)**: Remains a lumberyard if adjacent to at least 1 other lumberyard AND at least 1 acre containing trees. Otherwise, becomes open ground (`.`).

## Important Implementation Details
- **Adjacent**: Means any of the 8 surrounding acres (diagonal and orthogonal neighbors)
- Edge acres have fewer than 8 neighbors - missing acres are not counted
- **Simultaneous updates**: All changes happen at the same time using the state at the beginning of the minute. Changes during a minute don't affect each other (requires using the previous state for all calculations)

## Simulation Duration
Run the simulation for exactly **10 minutes** (10 iterations).

## Expected Output
Calculate the **resource value** after 10 minutes:
- Count the total number of wooded acres (`|`)
- Count the total number of lumberyards (`#`)
- Multiply these two counts together
- Output format: A single integer representing the resource value

Example: If there are 37 wooded acres and 31 lumberyards after 10 minutes, the resource value would be 37 × 31 = 1147.
