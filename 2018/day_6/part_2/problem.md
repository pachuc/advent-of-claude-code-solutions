# Problem Report: Safe Region Based on Total Manhattan Distance

## Context from Part 1
In Part 1, we had a set of coordinate points on a 2D grid and found the largest finite area around a single coordinate using Manhattan distance. The answer was 4233.

Now in Part 2, we're shifting our approach: instead of finding areas closest to individual coordinates, we need to find a **safe region** where locations are close to **many** coordinates simultaneously.

## Part 2 Objective
Find the size of the region containing all locations where the **total Manhattan distance to all given coordinates is less than 10000**.

## Input Format
- Same as Part 1: A list of coordinates in the format `x, y` (one per line)
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

2. **Total Distance**: For any grid location, calculate the Manhattan distance to **ALL** given coordinates and sum them up

3. **Safe Region**: A location is in the safe region if its total distance to all coordinates is **less than 10000**

4. **Region Size**: Count how many integer grid locations satisfy the total distance condition

### Algorithm Steps
1. Parse all input coordinates (same as Part 1)
2. Determine a search space (bounding box with appropriate buffer)
   - The safe region will be somewhere near the center of all coordinates
   - Need to search a large enough area to capture all qualifying locations
3. For each integer location in the search space:
   - Calculate Manhattan distance to **each** coordinate
   - Sum all these distances
   - If the total is less than 10000, this location is in the safe region
4. Count the total number of locations in the safe region

## Expected Output
- A single integer representing the size of the safe region
- For the example in the puzzle with threshold 32, the answer is `16`
- For the actual puzzle with threshold 10000, output that count

## Example Walkthrough
Given the same coordinates from Part 1:
```
1, 1  (A)
1, 6  (B)
8, 3  (C)
3, 4  (D)
5, 5  (E)
8, 9  (F)
```

With threshold **less than 32**:

Example location (4, 3):
- Distance to A: |4-1| + |3-1| = 5
- Distance to B: |4-1| + |3-6| = 6
- Distance to C: |4-8| + |3-3| = 4
- Distance to D: |4-3| + |3-4| = 2
- Distance to E: |4-5| + |3-5| = 3
- Distance to F: |4-8| + |3-9| = 10
- **Total: 30** (which is < 32, so this location is in the region)

The total region size with threshold 32 is **16**.

For the actual puzzle, use threshold **10000**.

## Implementation Notes
- Unlike Part 1, we don't care about which coordinate is closest
- We need to sum distances to **all** coordinates for each location
- The safe region will typically be concentrated near the centroid of all coordinates
- The search space should be large enough but doesn't need to extend infinitely
- A reasonable search space would be the bounding box of all coordinates plus some buffer
- Any location too far from the cluster of coordinates will have a total distance exceeding 10000
