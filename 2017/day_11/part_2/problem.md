# Problem: Maximum Distance Reached During Hexagonal Grid Navigation

## Context from Part 1
In Part 1, we navigated on a hexagonal grid following a series of directional moves and calculated the **final distance** from the origin to the ending position.

The hexagonal grid uses six possible directions:
- North (n)
- Northeast (ne)
- Southeast (se)
- South (s)
- Southwest (sw)
- Northwest (nw)

We used cube coordinates (x, y, z) where x + y + z = 0 to represent positions, with direction deltas:
- `n`:  (0, 1, -1)
- `ne`: (1, 0, -1)
- `se`: (1, -1, 0)
- `s`:  (0, -1, 1)
- `sw`: (-1, 0, 1)
- `nw`: (-1, 1, 0)

The distance from origin to any point (x, y, z) is calculated as: `(|x| + |y| + |z|) / 2`

Part 1 answer was **687 steps** - the shortest distance from origin to the final position after all moves.

## Part 2 Problem Description
Instead of finding the distance to the **final** position, we now need to find the **maximum distance** the child process ever reached from the starting position **during the entire journey**.

In other words, we need to track the distance from the origin after **each step** and return the furthest distance achieved at any point during the path traversal.

## Input
Same as Part 1: A comma-separated list of directional moves.
- Each move is one of: `n`, `ne`, `se`, `s`, `sw`, `nw`
- The input file contains a long sequence of moves

## Output
A single integer representing the **maximum number of steps away** from the origin that was reached at any point during the journey.

## Algorithm Approach
1. Start at origin (0, 0, 0)
2. For each move in the sequence:
   - Apply the direction delta to current position
   - Calculate distance from origin to new position
   - Track the maximum distance seen so far
3. Return the maximum distance

## Key Difference from Part 1
- **Part 1**: Distance from origin to final position only
- **Part 2**: Maximum distance from origin reached at ANY point during the journey (including intermediate positions)
