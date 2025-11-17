# Implementation Plan: Maze Reachability Counter (Part 2)

## Overview
Part 2 modifies Part 1 by changing from finding a shortest path to a specific target, to counting all distinct locations reachable within a step limit. We can reuse most of the Part 1 code with minor modifications.

## Key Differences from Part 1
- **Part 1**: Find shortest path from (1,1) to (31,39) → Answer: 82 steps
- **Part 2**: Count all distinct locations reachable from (1,1) in ≤50 steps → Answer: TBD

## Reusable Components from Part 1
- `is_open_space(x, y, favorite_number)` function - **No changes needed**
- BFS algorithm structure - **Modify to count instead of find target**
- Input reading logic - **No changes needed**

## Algorithm Analysis

### Approach: Modified BFS
- **Time Complexity**: O(V + E) where V is vertices (reachable locations) and E is edges (connections)
  - In worst case with 50 steps, we could explore up to ~(4^50) paths, but:
  - Visited set prevents revisiting, limiting to unique coordinates
  - Practical bound: at most a circle of radius 50 around start = ~7,854 cells max
  - Actual reachable cells will be much fewer due to walls
- **Space Complexity**: O(V) for visited set and queue
  - Maximum ~7,854 coordinates to track
  - Very manageable memory footprint

### Why BFS is Optimal
- BFS naturally explores by distance/step count
- Guarantees we visit each location at its minimum step count
- Easy to enforce step limit constraint
- No need for priority queue (all edges have weight 1)

## Implementation Steps

### Step 1: Copy and Preserve Part 1 Functions
```python
from collections import deque

def is_open_space(x, y, favorite_number):
    # COPY DIRECTLY FROM PART 1 - No modifications needed
    # This function already works perfectly
```

**Rationale**: The maze generation rules are identical between Part 1 and Part 2.

### Step 2: Create New Reachability Counter Function
```python
def count_reachable_locations(start, max_steps, favorite_number, debug=False):
    """
    Count all distinct locations reachable within max_steps from start.

    Args:
        start: tuple (x, y) starting position
        max_steps: int maximum number of steps allowed
        favorite_number: int used for maze generation
        debug: bool if True, return (count, visited_set) for validation

    Returns:
        int: count of distinct reachable locations (including start)
        OR (int, set): (count, visited_set) if debug=True
    """
```

**Note on Debug Parameter**: The optional `debug` parameter allows returning the visited set for validation purposes (e.g., checking if specific coordinates like (31,39) are reachable). This is useful for cross-validation with Part 1 results.

**Key Modifications from Part 1's find_shortest_path**:
1. **Remove target parameter**: We're not searching for a specific location
2. **Add max_steps parameter**: Enforce step limit
3. **Remove early termination on target found**: Explore all reachable locations
4. **Add step limit check**: Don't add to queue if steps >= max_steps
5. **Return visited set size**: Count of distinct locations

### Step 3: Implement Modified BFS Logic

**Initialization**:
```python
queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
visited = {start}  # Track all visited locations
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Up, down, right, left
```

**Main Loop**:
```python
while queue:
    x, y, steps = queue.popleft()

    # CRITICAL: Only explore further if we haven't reached step limit
    if steps < max_steps:
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check validity and add if not visited
            if (nx >= 0 and ny >= 0 and
                (nx, ny) not in visited and
                is_open_space(nx, ny, favorite_number)):

                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))
```

**Key Implementation Detail - Step Limit Logic**:
- We check `if steps < max_steps` BEFORE exploring neighbors
- This ensures we never go beyond the step limit
- **CRITICAL CLARIFICATION**: With `steps < max_steps` (e.g., `steps < 50`):
  - We explore neighbors FROM locations at steps 0-49
  - We can REACH and COUNT locations at steps 0-50
  - A location reached at exactly step 50 is added to visited and counted
  - But we don't explore further from that location (no step 51)
- This correctly implements "at most 50 steps" (inclusive of 50)

### Step 4: Return Count (with Optional Debug Info)
```python
if debug:
    return len(visited), visited
return len(visited)
```

**Rationale**:
- The visited set contains all unique coordinates reachable within the step limit, including the starting position
- When `debug=True`, also return the visited set for validation purposes
- This allows testing whether specific coordinates (e.g., (31,39) from Part 1) are reachable

### Step 5: Update Main Execution Block
```python
if __name__ == "__main__":
    # Read the favorite number from input
    with open('input.md', 'r') as f:
        FAVORITE_NUMBER = int(f.read().strip())

    # Define start position and step limit
    START = (1, 1)
    MAX_STEPS = 50

    # Count and print reachable locations
    result = count_reachable_locations(START, MAX_STEPS, FAVORITE_NUMBER)
    print(result)
```

**Changes from Part 1**:
- Remove TARGET constant
- Add MAX_STEPS = 50 constant
- Call count_reachable_locations instead of find_shortest_path

## Edge Cases Handled

1. **Starting position counts**: Visited set initialized with start → included in count
2. **Step limit boundary**: Check `steps < max_steps` ensures we don't exceed limit
3. **Negative coordinates**: `nx >= 0 and ny >= 0` check prevents invalid coordinates
4. **Walls**: `is_open_space()` check ensures we only visit valid locations
5. **Duplicate visits**: `(nx, ny) not in visited` prevents counting same location twice

## Expected Behavior

With favorite_number = 1362, start = (1,1), max_steps = 50:
- The algorithm will explore outward from (1,1) in all directions
- It will respect walls (determined by is_open_space function)
- It will stop exploring paths that reach 50 steps
- It will return the count of all unique coordinates visited

## Validation Strategy with Part 1

**Key Cross-Validation Point**: Part 1 found that (31,39) is reachable in exactly 82 steps from (1,1).
- With `max_steps = 50`: (31,39) should NOT be reachable
- With `max_steps = 81`: (31,39) should NOT be reachable
- With `max_steps = 82`: (31,39) SHOULD be reachable

This provides a concrete validation point to ensure our step counting logic is correct.

## Complete File Structure

```python
from collections import deque

# Function 1: is_open_space (copied from Part 1)
# Function 2: count_reachable_locations (new, modified from Part 1's find_shortest_path)
#            - includes optional debug parameter for validation
# Main block: read input, call count_reachable_locations, print result
```

## Example Manual Walkthrough (max_steps = 2)

To illustrate the algorithm behavior, here's a manual trace with max_steps = 2:

**Starting**: (1,1) with favorite_number = 1362

**Step 0**:
- Queue: [(1,1,0)]
- Visited: {(1,1)}
- Count: 1

**Step 1** (exploring from (1,1) at step 0):
- Check (1,2): if open, add to visited → {(1,1), (1,2)}
- Check (1,0): if open, add to visited → {(1,1), (1,2), (1,0)}
- Check (2,1): if open, add to visited → {(1,1), (1,2), (1,0), (2,1)}
- Check (0,1): if open, add to visited → {(1,1), (1,2), (1,0), (2,1), (0,1)}
- Queue now contains all reachable neighbors at step 1

**Step 2** (exploring from step 1 locations):
- For each location at step 1, check their neighbors
- Add any new open spaces not yet visited
- These locations are at step 2

**Result**: len(visited) includes all locations reachable in 0, 1, or 2 steps

This demonstrates how BFS naturally explores by distance and respects the step limit.

## Verification Points

- [ ] is_open_space function copied correctly from Part 1
- [ ] BFS queue initialized with (x, y, steps) tuples
- [ ] Visited set initialized with starting position
- [ ] Step limit check: `if steps < max_steps` before exploring (allows reaching step max_steps)
- [ ] All four directions explored
- [ ] Coordinate bounds checked (x >= 0, y >= 0)
- [ ] Wall checking with is_open_space
- [ ] Duplicate prevention with visited set
- [ ] Return len(visited) for count (or (len(visited), visited) if debug=True)
- [ ] Main block reads from input.md
- [ ] Main block uses MAX_STEPS = 50
- [ ] Main block prints result
- [ ] Optional: Verify (31,39) NOT in visited set with max_steps=50 (cross-check with Part 1)

## Performance Expectations

- **Runtime**: < 1 second for 50 steps limit
- **Memory**: Minimal (few thousand coordinates at most)
- **Correctness**: BFS guarantees we find all reachable locations within step limit
