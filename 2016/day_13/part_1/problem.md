# Problem Report: Maze Pathfinding

## Objective
Find the shortest path from a starting position to a target position in a procedurally-generated maze.

## Context
We are navigating through a maze where each coordinate can be either an open space or a wall. The maze layout is determined algorithmically based on a given "favorite number" input.

## Inputs
- **Favorite number**: An integer (in this case: `1362`)
- **Starting position**: `(1, 1)`
- **Target position**: `(31, 39)`

## Maze Generation Rules

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

## Example Validation
With favorite number = `10`:
- The maze starting at `(0,0)` produces a specific pattern
- The shortest path from `(1,1)` to `(7,4)` is `11` steps

## Expected Output
A single integer representing the **minimum number of steps** required to reach the target position `(31, 39)` from the starting position `(1, 1)`.

## Algorithm Requirements
- Implement maze generation logic based on the rules above
- Implement pathfinding algorithm (e.g., BFS, A*, Dijkstra) to find shortest path
- Handle the constraint that you can only move to open spaces (not walls)
- Only consider valid coordinates (non-negative x and y values)
