# Problem Report: Lumber Collection Area Simulation - Part 2

## Objective
Calculate the total resource value of a lumber collection area after simulating **1,000,000,000 minutes** (one billion minutes) of landscape transformation.

## Context from Part 1
In Part 1, we simulated a magical landscape where acres of land undergo transformations based on cellular automaton rules. The landscape is a 50x50 grid where each position can be:
- `.` = open ground
- `|` = trees (wooded acre)
- `#` = lumberyard

The simulation rules (applied simultaneously to all acres each minute):
1. **Open ground (`.`)**: Becomes trees (`|`) if 3 or more adjacent acres contain trees. Otherwise, remains open.
2. **Trees (`|`)**: Becomes a lumberyard (`#`) if 3 or more adjacent acres are lumberyards. Otherwise, remains trees.
3. **Lumberyard (`#`)**: Remains a lumberyard if adjacent to at least 1 other lumberyard AND at least 1 acre containing trees. Otherwise, becomes open ground (`.`).

Part 1 required simulating 10 minutes and calculated a resource value of 604884.

## Part 2 Challenge
The key challenge is that simulating 1 billion iterations directly would be computationally infeasible. The solution must detect that the system eventually enters a **cycle** (the grid states repeat in a pattern), then use this cycle to calculate what the state would be after 1 billion minutes without actually simulating all iterations.

## Input Description
- A 50x50 grid representing the lumber collection area
- Each cell can be one of three types:
  - `.` = open ground
  - `|` = trees (wooded acre)
  - `#` = lumberyard
- Input format: 50 lines of text, each containing 50 characters

## Algorithm Approach
1. Run the simulation while tracking all seen grid states
2. Detect when a grid state repeats (a cycle has been found)
3. Calculate the cycle length and cycle start point
4. Use modular arithmetic to determine which state in the cycle corresponds to minute 1,000,000,000
5. Calculate the resource value for that state

## Important Implementation Details
- **Adjacent**: Means any of the 8 surrounding acres (diagonal and orthogonal neighbors)
- Edge acres have fewer than 8 neighbors - missing acres are not counted
- **Simultaneous updates**: All changes happen at the same time using the state at the beginning of the minute
- **State tracking**: Need to store grid states to detect cycles. Convert grids to hashable representations (e.g., tuples or strings) for efficient lookup
- **Cycle detection**: When a state is seen again, we've found a cycle

## Expected Output
Calculate the **resource value** after 1,000,000,000 minutes:
- Count the total number of wooded acres (`|`)
- Count the total number of lumberyards (`#`)
- Multiply these two counts together
- Output format: A single integer representing the resource value

## Example Cycle Logic
If the simulation finds that:
- State repeats at minute 500 (this is the same state as minute 480)
- Cycle length = 20 (states from minute 480-499 repeat)
- To find state at minute 1,000,000,000:
  - Calculate: (1,000,000,000 - 480) % 20 = position in cycle
  - Return the resource value for that position
