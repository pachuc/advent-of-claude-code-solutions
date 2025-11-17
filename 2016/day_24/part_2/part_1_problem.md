# Problem Report: Air Duct Robot Pathfinding

## Context
A cleaning robot needs to navigate through air ducts to reach multiple control locations in order to bypass security controls. The robot is slow, so we need to find the most efficient path possible.

## Objective
Find the **minimum number of steps** required for the robot to:
- Start at location `0`
- Visit every other numbered location at least once
- The order of visiting locations (other than starting at `0`) can be optimized

This is a variant of the Traveling Salesman Problem (TSP) where we need to find the shortest route that visits all numbered waypoints.

## Input Format
The input is a 2D grid/map representing air ducts where:
- `#` represents walls (impassable)
- `.` represents open passages (passable)
- `0` represents the starting location
- `1-9` represent locations that must be visited (these also behave as open passages)
- The robot can only move horizontally or vertically (no diagonal movement)
- Each step moves one grid cell

## Expected Output
A single integer representing the **fewest number of steps** required to start at location `0` and visit every other numbered location at least once.

## Example
Given this map:
```
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
```

The optimal path is:
- `0` to `4`: 2 steps
- `4` to `1`: 4 steps
- `1` to `2`: 6 steps
- `2` to `3`: 2 steps
- **Total: 14 steps**

## Algorithm Approach
1. Parse the grid to find all numbered locations (0-N)
2. Use BFS (Breadth-First Search) to calculate shortest distances between all pairs of numbered locations
3. Solve the TSP variant: starting from location `0`, find the shortest path that visits all other locations at least once (order matters, but doesn't need to return to start)
4. Return the minimum total distance

## Notes
- The locations must be visited "at least once" - revisiting is allowed but not required for the optimal solution
- The robot starts at `0` and does not need to return to `0` after visiting all locations
- Movement is restricted to 4 directions (up, down, left, right)
