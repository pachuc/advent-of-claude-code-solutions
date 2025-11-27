# Implementation Plan: Part 2 - Optimal Teleportation Position

## Problem Analysis

### Core Challenge
Find a coordinate (x, y, z) in 3D space that is:
1. **Primary Goal**: In range of the maximum number of nanobots
2. **Tiebreaker**: Among coordinates with max nanobot count, choose the one closest to origin (0,0,0)

### Key Differences from Part 1
- Part 1: Fixed position (strongest nanobot), count reachable nanobots
- Part 2: Variable position (any coordinate), find position that maximizes coverage

### Algorithm Complexity Considerations
With ~1000 nanobots and potentially infinite search space, we need an efficient approach:
- **Brute force**: Infeasible (infinite/astronomical search space)
- **Smart search**: Use spatial decomposition and pruning
- **Geometric insight**: Leverage the properties of Manhattan distance spheres (octahedra)

## Proposed Solution: Octree-Based Binary Search

### Approach Overview
Use a 3D octree structure to recursively subdivide space, focusing on regions with high nanobot density.

### Algorithm Steps

#### 1. **Input Parsing** (Reuse from Part 1)
- Parse nanobot positions and radii from input
- Function: `parse_input(filename)` → List[(x, y, z, r)]
- **Reuse** the existing parser from `part_1_solution.py`

#### 2. **Determine Search Space Bounds**
```python
def get_search_bounds(nanobots):
    """
    Calculate initial bounding box for search.
    Consider: min/max of (nanobot_position ± radius) for each dimension
    """
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    min_z, max_z = float('inf'), float('-inf')

    for x, y, z, r in nanobots:
        # Each nanobot can affect space from (pos - r) to (pos + r)
        min_x = min(min_x, x - r)
        max_x = max(max_x, x + r)
        min_y = min(min_y, y - r)
        max_y = max(max_y, y + r)
        min_z = min(min_z, z - r)
        max_z = max(max_z, z + r)

    return (min_x, max_x), (min_y, max_y), (min_z, max_z)
```

#### 3. **Count Nanobots in Range of a Position**
```python
def count_bots_in_range(position, nanobots):
    """
    For a given position, count how many nanobots can reach it.
    A nanobot at (bx, by, bz) with radius r can reach position p if:
    manhattan_distance(p, (bx, by, bz)) <= r
    """
    count = 0
    px, py, pz = position
    for bx, by, bz, r in nanobots:
        if manhattan_distance((px, py, pz), (bx, by, bz)) <= r:
            count += 1
    return count
```
**Reuse** `manhattan_distance()` from Part 1.

#### 4. **Estimate Max Nanobots for a Region (Box)**
```python
def max_bots_for_box(box, nanobots):
    """
    Upper bound estimate: Count nanobots that could possibly reach
    ANY point in the box.

    For a nanobot to potentially reach the box, the minimum distance
    from the nanobot to the box must be <= nanobot radius.
    """
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box
    count = 0

    for bx, by, bz, r in nanobots:
        # Calculate minimum Manhattan distance from nanobot to box
        min_dist = 0

        # X dimension
        if bx < x_min:
            min_dist += x_min - bx
        elif bx > x_max:
            min_dist += bx - x_max
        # else: bx is within [x_min, x_max], contributes 0

        # Y dimension
        if by < y_min:
            min_dist += y_min - by
        elif by > y_max:
            min_dist += by - y_max

        # Z dimension
        if bz < z_min:
            min_dist += z_min - bz
        elif bz > z_max:
            min_dist += bz - z_max

        if min_dist <= r:
            count += 1

    return count
```

#### 5. **Octree Search with Priority Queue**
```python
import heapq

def find_optimal_position(nanobots):
    """
    Use octree subdivision with priority queue to find optimal position.

    Strategy:
    - Start with bounding box of entire search space
    - Use priority queue to explore most promising regions first
    - Subdivide boxes into 8 octants
    - Track best single-point solution found so far
    - Prune boxes that can't beat current best
    """

    # Get initial bounds
    bounds_x, bounds_y, bounds_z = get_search_bounds(nanobots)
    initial_box = (bounds_x, bounds_y, bounds_z)

    # Validate bounds are reasonable
    assert bounds_x[0] <= bounds_x[1], "Invalid x bounds"
    assert bounds_y[0] <= bounds_y[1], "Invalid y bounds"
    assert bounds_z[0] <= bounds_z[1], "Invalid z bounds"

    # Priority queue: (-max_bots, box_size, box)
    # Negative for max-heap behavior (higher bot count = higher priority)
    # box_size as tiebreaker (smaller boxes = higher priority)
    pq = []

    initial_max = max_bots_for_box(initial_box, nanobots)
    box_size = get_box_size(initial_box)
    heapq.heappush(pq, (-initial_max, box_size, initial_box))

    best_count = 0
    best_distance = float('inf')
    best_position = None

    while pq:
        neg_max_bots, size, box = heapq.heappop(pq)
        max_bots = -neg_max_bots

        # Pruning: If this box can't beat our best, skip it
        if max_bots < best_count:
            continue
        if max_bots == best_count:
            # Even if equal count, check if box is too far from origin
            # This handles the tiebreaker: prefer positions closer to origin
            min_dist_to_origin = min_distance_box_to_origin(box)
            if min_dist_to_origin >= best_distance:
                continue

        # If box is a single point, evaluate it
        if is_single_point(box):
            point = box_to_point(box)
            count = count_bots_in_range(point, nanobots)
            dist = manhattan_distance(point, (0, 0, 0))

            if count > best_count or (count == best_count and dist < best_distance):
                best_count = count
                best_distance = dist
                best_position = point
        else:
            # Subdivide box into 8 octants
            octants = subdivide_box(box)
            for octant in octants:
                octant_max = max_bots_for_box(octant, nanobots)
                octant_size = get_box_size(octant)
                heapq.heappush(pq, (-octant_max, octant_size, octant))

    return best_position, best_count, best_distance
```

#### 6. **Helper Functions for Box Operations**
```python
def get_box_size(box):
    """Calculate total size of box (sum of dimensions)."""
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box
    return (x_max - x_min) + (y_max - y_min) + (z_max - z_min)

def is_single_point(box):
    """Check if box has collapsed to a single point."""
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box
    return x_min == x_max and y_min == y_max and z_min == z_max

def box_to_point(box):
    """Convert single-point box to coordinate tuple."""
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box
    return (x_min, y_min, z_min)

def min_distance_box_to_origin(box):
    """Calculate minimum Manhattan distance from any point in box to origin."""
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box

    # For each dimension, pick the value closest to 0
    x = 0 if x_min <= 0 <= x_max else min(abs(x_min), abs(x_max))
    y = 0 if y_min <= 0 <= y_max else min(abs(y_min), abs(y_max))
    z = 0 if z_min <= 0 <= z_max else min(abs(z_min), abs(z_max))

    # x, y, z are already non-negative distances, no need for abs()
    return x + y + z

def subdivide_box(box):
    """
    Divide box into up to 8 octants.
    Split each dimension at midpoint.
    Handles degenerate boxes (already collapsed in one or more dimensions).
    """
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box

    x_mid = (x_min + x_max) // 2
    y_mid = (y_min + y_max) // 2
    z_mid = (z_min + z_max) // 2

    # Generate ranges for each dimension
    # If dimension already collapsed (min == max), keep it as single range
    x_ranges = [(x_min, x_mid), (x_mid + 1, x_max)] if x_min < x_max else [(x_min, x_max)]
    y_ranges = [(y_min, y_mid), (y_mid + 1, y_max)] if y_min < y_max else [(y_min, y_max)]
    z_ranges = [(z_min, z_mid), (z_mid + 1, z_max)] if z_min < z_max else [(z_min, z_max)]

    # Generate all combinations (cartesian product)
    octants = []
    for x_range in x_ranges:
        for y_range in y_ranges:
            for z_range in z_ranges:
                octants.append((x_range, y_range, z_range))

    return octants
```

#### 7. **Main Function**
```python
def main():
    """Main execution function."""
    # Reuse parser from Part 1
    nanobots = parse_input('input.md')

    if len(nanobots) == 0:
        print("Error: No nanobots found")
        return 0

    # Find optimal position
    position, count, distance = find_optimal_position(nanobots)

    # Final answer is the distance from origin
    print(distance)
    return distance
```

## Alternative Approach: Z3 SMT Solver (Backup Plan)

If the octree approach is too slow or complex, we can use Z3 theorem prover:

```python
from z3 import *

def solve_with_z3(nanobots):
    """
    Use Z3 SMT solver to find optimal position.
    Formulate as optimization problem.
    """
    x, y, z = Int('x'), Int('y'), Int('z')

    # Helper for absolute value in Z3
    def z3_abs(val):
        return If(val >= 0, val, -val)

    # For each nanobot, create boolean: is position in range?
    in_range = []
    for bx, by, bz, r in nanobots:
        dist = z3_abs(x - bx) + z3_abs(y - by) + z3_abs(z - bz)
        in_range.append(If(dist <= r, 1, 0))

    # Maximize count of nanobots in range
    range_count = Sum(in_range)

    # Distance from origin
    dist_origin = z3_abs(x) + z3_abs(y) + z3_abs(z)

    # Optimize
    opt = Optimize()
    opt.maximize(range_count)
    opt.minimize(dist_origin)

    opt.check()
    model = opt.model()

    return (model[x].as_long(), model[y].as_long(), model[z].as_long())
```

## Implementation Strategy

1. **Start with octree approach** (more educational, better understanding)
2. **If octree is too slow**, fall back to Z3 solver
3. **Reuse** functions from Part 1:
   - `parse_input()`
   - `manhattan_distance()`

## Performance Considerations

- **Octree depth**: Bounded by coordinate range (roughly log2 of range)
- **Priority queue**: Ensures we explore most promising regions first
- **Pruning**: Critical for performance - skip boxes that can't improve solution
- **Expected runtime**: O(n × log(range)) where n = number of nanobots

## Edge Cases to Handle

1. Multiple coordinates with same max count → pick closest to origin
2. Origin itself might be optimal
3. Very large coordinate values (millions)
4. All nanobots have small radii → optimal position might be at a nanobot position
5. Single nanobot edge case
