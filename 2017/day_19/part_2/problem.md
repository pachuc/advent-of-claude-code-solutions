# Problem Report: Network Packet Routing - Step Count (Part 2)

## Context from Part 1
In Part 1, we traced a network packet through an ASCII art routing diagram. The packet followed a path marked by `|`, `-`, and `+` characters, collecting letters (A-Z) along the way. The Part 1 solution successfully found the sequence of letters: **LOHMDQATP**.

The path-following algorithm from Part 1:
- Starts at the only `|` character in the top row, moving DOWN
- Follows the continuous path by prioritizing straight movement
- Turns only at `+` characters or when forced to (dead end with one perpendicular option)
- Stops when no valid continuation exists

## Part 2 Objective
Count the **total number of steps** the packet takes while following the same path.

## What Counts as a Step
Every position the packet moves to counts as one step, including:
- The starting position (first `|` at the top)
- Every path character (`|`, `-`, `+`) encountered
- Every letter (A-Z) encountered
- The final stopping position

## Input Description
Same as Part 1: An ASCII art routing diagram provided in `input.md` consisting of:
- `|` - vertical path segments
- `-` - horizontal path segments
- `+` - corner/junction points
- `A-Z` - letter markers on the path
- Spaces - empty areas (not part of path)

## Path Following Rules
**Identical to Part 1** - follow the same continuous path using the same movement algorithm. The only difference is we're counting steps instead of collecting letters.

## Expected Output
A single integer representing the total number of steps taken from start to finish.

**Format**: Plain integer (e.g., `38`)

## Example
Using the example diagram from the puzzle:
```
     |
     |  +--+
     A  |  C
 F---|--|-E---+
     |  |  |  D
     +B-+  +--+
```

The packet's journey broken down by steps:
- 6 steps down (including the first line at the top)
- 3 steps right
- 4 steps up
- 3 steps right
- 4 steps down
- 3 steps right
- 2 steps up
- 13 steps left (including the `F` it stops on)

**Total: 38 steps**

## Implementation Notes
- Reuse the path-following algorithm from Part 1
- Instead of collecting letters, maintain a step counter
- Increment the counter for every position visited (including the starting position)
- Return the final count when the path ends
