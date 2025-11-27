# Implementation Plan: A Regular Map - Part 2

## Overview
Part 2 reuses almost all of the Part 1 solution. The graph construction logic remains identical; only the final calculation changes from finding the maximum distance to counting rooms at distance >= 1000.

## Core Algorithm Understanding

### Part 1 Recap
The Part 1 solution (`part_1_solution.py`) consists of three main components:
1. **Regex Parser**: Parses the regex string to trace all possible routes and build a set of doors
2. **Graph Builder**: Converts the doors set into an adjacency graph
3. **BFS Distance Finder**: Uses breadth-first search to find shortest paths from the starting position to all reachable rooms

### Part 2 Modification
The only change needed is in the BFS function:
- **Part 1**: Track and return the maximum distance encountered
- **Part 2**: Count and return how many rooms have distance >= 1000

## Implementation Steps

### Step 1: Copy and Adapt Part 1 Functions
**Action**: Copy the following functions from `part_1_solution.py` without modification:
- `parse_regex_and_build_graph(regex)` - Parses regex and builds door set
- `build_adjacency_graph(doors)` - Converts doors to adjacency graph

**Rationale**: These functions handle the graph construction, which is identical for Part 2.

### Step 2: Modify the Distance Finding Function
**Action**: Create a new function `count_distant_rooms(graph, start=(0, 0), threshold=1000)`:

**Algorithm**:
```
1. Initialize BFS queue with starting position and distance 0
2. Initialize visited set with starting position
3. Initialize counter for rooms meeting threshold
4. While queue is not empty:
   a. Dequeue current position and distance
   b. If distance >= threshold, increment counter
   c. For each unvisited neighbor:
      - Mark as visited
      - Enqueue with distance + 1
5. Return counter
```

**Key Changes from Part 1**:
- Add a `threshold` parameter (default: 1000)
- Replace `max_distance = max(max_distance, dist)` with conditional counting
- Return count instead of maximum distance

**Complexity**: O(V + E) where V is number of rooms and E is number of doors (same as Part 1)

### Step 3: Update the Main Solve Function
**Action**: Modify the `solve(input_text, threshold=1000)` function:

**Changes**:
1. Keep the regex parsing and graph building steps identical
2. Replace `find_max_distance(graph)` with `count_distant_rooms(graph, start=(0, 0), threshold=threshold)`
3. Update return statement to return the count
4. Accept optional `threshold` parameter (defaults to 1000) to support testing with different thresholds

**Signature**: `solve(input_text, threshold=1000) -> int`

### Step 4: Update Main Execution Block
**Action**: Update the `if __name__ == '__main__'` block:

**Changes**:
1. Keep input reading logic identical
2. Update print statement to reflect counting rooms instead of maximum distance
3. Print the result in a clear format

## Code Structure

```python
from collections import defaultdict, deque

# Step 1: Copy from Part 1 (no changes)
def parse_regex_and_build_graph(regex):
    # ... exact copy from part_1_solution.py ...

# Step 1: Copy from Part 1 (no changes)
def build_adjacency_graph(doors):
    # ... exact copy from part_1_solution.py ...

# Step 2: New function (modified from Part 1)
def count_distant_rooms(graph, start=(0, 0), threshold=1000):
    """
    Count rooms that require passing through at least 'threshold' doors.

    Args:
        graph: Adjacency graph (defaultdict of sets)
        start: Starting position (default: (0, 0))
        threshold: Minimum number of doors (default: 1000)

    Returns:
        Count of rooms with distance >= threshold
    """
    queue = deque([(start, 0)])
    visited = {start}
    count = 0

    while queue:
        pos, dist = queue.popleft()

        # Count rooms at or beyond threshold
        if dist >= threshold:
            count += 1

        for neighbor in graph[pos]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return count

# Step 3: Modified solve function
def solve(input_text, threshold=1000):
    """
    Count rooms requiring at least 'threshold' doors to reach.

    Args:
        input_text: The regex string including ^ and $
        threshold: Minimum number of doors (default: 1000)

    Returns:
        Count of rooms with shortest path >= threshold doors
    """
    # Strip whitespace and remove ^ and $
    regex = input_text.strip()[1:-1]

    # Build the doors set by parsing the regex
    doors = parse_regex_and_build_graph(regex)

    # Build the adjacency graph
    graph = build_adjacency_graph(doors)

    # Count rooms at distance >= threshold
    count = count_distant_rooms(graph, start=(0, 0), threshold=threshold)

    return count

# Step 4: Main execution
if __name__ == '__main__':
    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)
    print(f"Rooms requiring at least 1000 doors: {result}")
```

## Algorithm Efficiency

### Time Complexity
- **Regex Parsing**: O(R) where R is the regex length
- **Graph Building**: O(D) where D is the number of doors
- **BFS Traversal**: O(V + E) where V is rooms and E is doors
- **Overall**: O(R + V + E) - Linear in all components

### Space Complexity
- **Doors Set**: O(D)
- **Adjacency Graph**: O(V + E)
- **BFS Visited Set**: O(V)
- **Overall**: O(V + E)

### Scalability Considerations
The input regex is very large (15000+ characters), which creates a substantial graph:
- From Part 1, we know the furthest room is 3672 doors away
- This suggests thousands of rooms in the facility
- The BFS approach remains efficient even for this scale
- No optimization needed beyond the Part 1 solution

## Edge Cases Handled

1. **Empty branches**: Already handled by Part 1 parser (e.g., `(NEWS|)`)
2. **Nested branches**: Already handled by Part 1 parser
3. **Starting position**: Distance 0, won't be counted when threshold=1000 (0 < 1000)
4. **Threshold boundary**: Use `>=` to include rooms at exactly threshold doors
5. **Unreachable rooms**: Not possible in this problem (regex describes all doors)
6. **Variable threshold**: The `solve()` function accepts an optional threshold parameter, enabling testing with different values while defaulting to 1000 for the actual puzzle

## Validation

The solution can be validated against Part 1:
- Part 1 answer: 3672 (maximum distance)
- Part 2 answer: Should be <= total number of rooms
- Part 2 answer: Should be >= 1 (since max distance is 3672 > 1000)
- Sanity check: If we set threshold=3672, answer should be >= 1
