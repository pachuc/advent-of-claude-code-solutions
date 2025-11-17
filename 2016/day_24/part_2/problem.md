# Problem Report: Air Duct Robot Pathfinding - Part 2 (Round Trip)

## Context from Part 1
A cleaning robot navigates through air ducts to reach multiple control locations to bypass security controls. The robot is slow, so we need to find the most efficient path possible.

In Part 1, we found that the minimum number of steps to start at location `0` and visit all other numbered locations was **428 steps**. The robot did not need to return to the starting position.

## Part 2 Change: Return to Start Required
The key difference in Part 2 is that **the robot must return to location `0` after visiting all other locations**. This is to avoid leaving the cleaning robot in a weird location where someone might notice it.

## Objective
Find the **minimum number of steps** required for the robot to:
- Start at location `0`
- Visit every other numbered location at least once
- **Return to location `0`** (NEW requirement for Part 2)
- The order of visiting locations (other than starting at `0` and ending at `0`) can be optimized

This is now a classic Traveling Salesman Problem (TSP) where we need to find the shortest **round trip** that visits all numbered waypoints.

## Input Format
The input remains the same as Part 1:
- A 2D grid/map representing air ducts
- `#` represents walls (impassable)
- `.` represents open passages (passable)
- `0` represents the starting location (and ending location for Part 2)
- `1-9` represent locations that must be visited (these also behave as open passages)
- The robot can only move horizontally or vertically (no diagonal movement)
- Each step moves one grid cell

## Expected Output
A single integer representing the **fewest number of steps** required to:
1. Start at location `0`
2. Visit every other numbered location at least once
3. Return to location `0`

## Algorithm Approach
The approach is very similar to Part 1, with one key modification:

1. Parse the grid to find all numbered locations (0-N)
2. Use BFS (Breadth-First Search) to calculate shortest distances between all pairs of numbered locations (this step is identical to Part 1)
3. Solve the TSP variant: starting from location `0`, find the shortest path that visits all other locations at least once **and returns to `0`**
4. Return the minimum total distance

### Key Difference from Part 1
In Part 1, the final answer was:
```
min(dp[full_mask][i]) for all ending positions i
```

In Part 2, the final answer must be:
```
min(dp[full_mask][i] + distance[i][0]) for all ending positions i
```

This adds the distance from each possible final location back to location `0`.

## Notes
- The robot must visit all locations "at least once" - revisiting is allowed but not required for the optimal solution
- The robot **must return to `0`** after visiting all other locations
- Movement is restricted to 4 directions (up, down, left, right)
- The Part 1 solution code can be reused with a small modification to the final calculation
