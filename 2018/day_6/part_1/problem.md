# Problem Report: Largest Finite Area Using Manhattan Distance

## Context
We have a set of coordinate points on an infinite 2D grid. We need to determine which coordinate has the largest "area of influence" - that is, the region of points closest to it using Manhattan distance - but only among coordinates whose areas are finite (not extending to infinity).

## Objective
Find the size of the largest finite area where each location in that area is closest to one specific coordinate (and not tied in distance to any other coordinate).

## Input Format
- A list of coordinates in the format `x, y` (one per line)
- Each coordinate is a pair of integers separated by a comma and space
- Example:
  ```
  181, 47
  337, 53
  331, 40
  ```

## Problem Requirements

### Key Concepts
1. **Manhattan Distance**: The distance between two points (x1, y1) and (x2, y2) is `|x1 - x2| + |y1 - y2|`

2. **Area of a Coordinate**: The count of all integer grid locations that are closest to that specific coordinate compared to all other coordinates

3. **Ties**: If a location is equidistant from two or more coordinates, it doesn't belong to any coordinate's area

4. **Infinite vs Finite Areas**:
   - If a coordinate's closest locations extend to the edges of the bounding box containing all coordinates, its area is considered infinite
   - Only coordinates whose areas are fully contained within the bounding region have finite areas

### Algorithm Steps
1. Parse all input coordinates
2. Determine the bounding box that contains all coordinates
3. For each integer location in a sufficient grid area (including some buffer beyond the bounding box):
   - Calculate Manhattan distance to all coordinates
   - Determine which coordinate(s) it's closest to
   - If tied (equidistant to multiple), mark as neutral
   - Otherwise, assign to the closest coordinate
4. Identify which coordinates have infinite areas (those that reach the edges of the grid)
5. Among coordinates with finite areas, find the one with the largest area count

## Expected Output
- A single integer representing the size of the largest finite area
- For the example in the puzzle (coordinates A-F), the answer is `17`

## Example Walkthrough
Given coordinates:
```
1, 1  (A)
1, 6  (B)
8, 3  (C)
3, 4  (D)
5, 5  (E)
8, 9  (F)
```

Results:
- Coordinates A, B, C, F have infinite areas (extend beyond visible bounds)
- Coordinate D has area of 9 locations
- Coordinate E has area of 17 locations (the largest finite area)
- **Answer: 17**

## Implementation Notes
- The grid extends infinitely, but practically we only need to check within and slightly beyond the bounding box
- Coordinates whose areas touch the boundary of our search grid are infinite
- Need to handle ties properly - locations equidistant from multiple coordinates belong to none
