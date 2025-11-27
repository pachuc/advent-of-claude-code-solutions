# Problem Report: Four-Dimensional Constellation Grouping

## Context
We need to align a device to constellations of fixed points in spacetime to open a portal and retrieve magical energy (hot chocolate) for a sick reindeer. The device requires identifying how many distinct constellations exist in a list of four-dimensional coordinates.

## Objective
Count the number of constellations formed by a set of four-dimensional points.

## Input
- A list of four-dimensional coordinates (4D points in spacetime)
- Each coordinate is represented as four comma-separated integers: `x,y,z,w`
- Example format:
  ```
  0,0,0,0
  3,0,0,0
  0,3,0,0
  ```

## Constellation Definition
Two points belong to the same constellation if either:
1. **Direct connection**: Their Manhattan distance is ≤ 3
2. **Indirect connection**: They can be connected through a chain of points where each consecutive pair has Manhattan distance ≤ 3

### Manhattan Distance in 4D
For two points `(x1,y1,z1,w1)` and `(x2,y2,z2,w2)`:
```
distance = |x1-x2| + |y1-y2| + |z1-z2| + |w1-w2|
```

## Algorithm Requirements
1. Parse each line as a four-dimensional coordinate
2. Determine which points can be grouped into the same constellation based on the connectivity rule
3. Count the total number of distinct constellations

## Output
- A single integer representing the number of constellations
- No special formatting required

## Test Cases

### Example 1
Input:
```
0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0
```
Expected Output: `2`

Explanation: The first six points form one constellation (connected through chains with distance ≤ 3). Points `9,0,0,0` and `12,0,0,0` form a separate constellation (distance 3 from each other, but too far from the first group).

### Example 2
Input:
```
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
```
Expected Output: `4`

### Example 3
Input:
```
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
```
Expected Output: `3`

### Example 4
Input:
```
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
```
Expected Output: `8`

## Implementation Notes
- This is essentially a graph connectivity problem where edges exist between points with Manhattan distance ≤ 3
- Union-Find (Disjoint Set Union) or Depth-First Search (DFS) can be used to group connected components
- Each connected component represents one constellation
