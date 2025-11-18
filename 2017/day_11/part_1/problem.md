# Problem: Hexagonal Grid Navigation Distance

## Context
We need to find the shortest distance to a point on a hexagonal grid, given a path of movements from the origin.

## Problem Description
You are given a sequence of moves on a hexagonal grid. The hexagonal grid uses a coordinate system where from any position, you can move in six directions:
- North (n)
- Northeast (ne)
- Southeast (se)
- South (s)
- Southwest (sw)
- Northwest (nw)

The hexagonal grid layout:
```
  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \
```

Starting from the origin (0, 0), a series of moves is performed. Your task is to determine the **fewest number of steps required** to reach the final position from the origin.

## Input
A comma-separated list of directional moves. Each move is one of: `n`, `ne`, `se`, `s`, `sw`, `nw`

Example input formats:
- `ne,ne,ne`
- `ne,ne,sw,sw`
- `ne,ne,s,s`
- `se,sw,se,sw,sw`

## Output
A single integer representing the minimum number of steps needed to reach the final position from the starting position.

## Examples
1. Input: `ne,ne,ne` → Output: `3` (3 steps away from origin)
2. Input: `ne,ne,sw,sw` → Output: `0` (back at the origin)
3. Input: `ne,ne,s,s` → Output: `2` (can be simplified to `se,se`)
4. Input: `se,sw,se,sw,sw` → Output: `3` (can be simplified to `s,s,sw`)

## Key Insights
- Opposite directions cancel each other out (e.g., `n` and `s`, `ne` and `sw`, `nw` and `se`)
- Some combinations of moves can be simplified (e.g., `ne` + `s` = `se`, `ne` + `nw` = `n`)
- You need to calculate the final position after all moves, then determine the shortest path back to the origin
- Hexagonal grids can be represented using cube coordinates or axial coordinates for easier distance calculation
