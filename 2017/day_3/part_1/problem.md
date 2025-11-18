# Problem Report: Spiral Memory Manhattan Distance

## Objective
Calculate the Manhattan Distance from a given square number in a spiral memory grid to the center square (square 1).

## Context
We have an infinite 2D grid where squares are numbered starting from 1 at the center, spiraling outward in a specific pattern. Data stored in any square must be carried back to square 1 (the access port) using only up/down/left/right movements. We need to find the shortest path distance (Manhattan Distance) from a given square to square 1.

## Spiral Pattern
The grid is numbered in a spiral pattern starting from the center:

```
17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
```

Square 1 is at the center, and numbers increase while spiraling outward (right, up, left, down, then repeat with larger steps).

## Input
- A single integer representing a square number in the spiral grid
- Example input: `289326`

## Output
- A single integer representing the Manhattan Distance (number of steps) from the given square to square 1
- Manhattan Distance is calculated as: |x1 - x2| + |y1 - y2| where square 1 is at coordinates (0, 0)

## Examples
- Square `1` → Distance: `0` (already at the access port)
- Square `12` → Distance: `3` (e.g., down, left, left)
- Square `23` → Distance: `2` (e.g., up, up)
- Square `1024` → Distance: `31`

## Algorithm Requirements
1. Determine the position (x, y coordinates) of the given square number in the spiral
2. Calculate the Manhattan Distance from that position to the center (0, 0)
3. Return the distance as an integer
