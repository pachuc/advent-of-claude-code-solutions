# Problem Report: Maze Reachability Analysis

## Objective
Count the total number of distinct locations that can be reached within a limited number of steps from a starting position in a procedurally-generated maze.

## Context from Part 1
In Part 1, we navigated through a maze where each coordinate can be either an open space or a wall. The maze layout is determined algorithmically based on a given "favorite number" input. We found the shortest path from `(1, 1)` to `(31, 39)`, which was `82` steps.

## Part 2 Objective
Instead of finding a path to a specific target, we now need to explore the maze and count how many unique locations (including the starting position) can be reached within a step limit.

## Inputs
- **Favorite number**: An integer (in this case: `1362`)
- **Starting position**: `(1, 1)`
- **Step limit**: `50` steps maximum

## Maze Generation Rules (Same as Part 1)

The maze is infinite and uses a coordinate system of non-negative integers `(x, y)` where:
- Only non-negative values are valid (x >= 0, y >= 0)
- Movement is restricted to 4 directions (no diagonal movement)

To determine if a coordinate `(x, y)` is a wall or open space:

1. Calculate: `x*x + 3*x + 2*x*y + y + y*y`
2. Add the favorite number to this result
3. Convert the sum to binary representation
4. Count the number of `1` bits in the binary representation:
   - If the count is **even**: the coordinate is an **open space**
   - If the count is **odd**: the coordinate is a **wall**

## Expected Output
A single integer representing the **total number of distinct locations** (x, y coordinates) that can be reached from the starting position `(1, 1)` in **at most 50 steps**.

**Important**: The count should include:
- The starting location `(1, 1)` itself (0 steps)
- All locations reachable in 1 step
- All locations reachable in 2 steps
- ... up to all locations reachable in exactly 50 steps

Each unique coordinate should only be counted once, even if it can be reached via multiple paths or in different numbers of steps.

## Algorithm Requirements
- Reuse the maze generation logic from Part 1
- Implement a breadth-first search (BFS) or similar exploration algorithm
- Track all visited locations within the step limit
- Count distinct coordinates (not paths)
- Return the total count of reachable locations
