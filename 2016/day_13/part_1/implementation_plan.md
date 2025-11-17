# Implementation Plan: Maze Pathfinding

## Problem Summary
Find the shortest path from (1, 1) to (31, 39) in a procedurally-generated maze where walls/open spaces are determined by counting 1-bits in a binary representation of a formula based on coordinates and a favorite number (1362).

## Algorithm Selection

**Chosen Algorithm: Breadth-First Search (BFS)**

**Rationale:**
- BFS guarantees finding the shortest path in an unweighted graph
- Time complexity: O(V + E) where V is vertices visited and E is edges
- For this problem, we explore coordinates layer by layer, ensuring minimal steps
- Simple to implement and efficient for this use case
- Alternative A* could be used with Manhattan distance heuristic, but BFS is sufficient given the problem size (target at 31, 39 is relatively close)

## Implementation Steps

### Step 1: Input Parsing
- Read the favorite number from input file
  - Use `open('input.md').read().strip()` to handle potential whitespace
  - Convert to integer
- Define constants:
  - `START = (1, 1)`
  - `TARGET = (31, 39)`
  - `FAVORITE_NUMBER = <parsed_value>`

### Step 2: Implement Maze Cell Determination Function
```
Function: is_open_space(x, y, favorite_number)
```
- **Input**: coordinates (x, y) and favorite_number
- **Process**:
  1. Validate that x >= 0 and y >= 0
  2. Calculate: `value = x*x + 3*x + 2*x*y + y + y*y`
     - This matches exactly the formula from the problem statement
     - Use explicit parentheses for clarity: `value = (x*x) + (3*x) + (2*x*y) + y + (y*y)`
  3. Add favorite_number: `value += favorite_number`
  4. Count 1-bits in binary representation using `bin(value).count('1')`
  5. Return True if count is even (open space), False if odd (wall)
- **Output**: Boolean indicating if the position is traversable

**Efficiency Note**: This is O(1) operation with at most ~20-30 bits for reasonable coordinate values.

### Step 3: Implement BFS Pathfinding
```
Function: find_shortest_path(start, target, favorite_number)
```

**Data Structures:**
- **Queue**: Use `collections.deque` for O(1) append and popleft operations
  - Elements: tuples of (x, y, steps)
- **Visited Set**: Use `set()` to track visited coordinates
  - Elements: tuples of (x, y)
  - Prevents revisiting same cell (O(1) lookup)

**Algorithm Flow:**
1. Initialize queue with starting position: `queue = deque([(1, 1, 0)])`
2. Initialize visited set: `visited = {(1, 1)}`
3. Define possible moves: `[(0, 1), (0, -1), (1, 0), (-1, 0)]` (up, down, right, left)
4. While queue is not empty:
   a. Dequeue current position: `(x, y, steps) = queue.popleft()` (use `popleft()` for FIFO behavior)
   b. Check if current position is target:
      - If yes, return steps
   c. For each of 4 directions:
      - Calculate new position: `(nx, ny) = (x + dx, y + dy)`
      - Validate new position:
        * `nx >= 0` and `ny >= 0` (non-negative coordinates)
        * `(nx, ny) not in visited` (not already explored)
        * `is_open_space(nx, ny, favorite_number)` (not a wall)
      - If valid:
        * Add to visited set: `visited.add((nx, ny))` (mark as visited when enqueueing to prevent duplicates)
        * Enqueue: `queue.append((nx, ny, steps + 1))`
5. If queue exhausted without finding target, raise an informative error:
   - `raise ValueError(f"No path found from {start} to {target}")`
   - For this problem, a path should always exist, so this catches implementation bugs

**Complexity Analysis:**
- **Time**: O(W × H) where W and H are the maximum width and height explored
  - In worst case, we might explore up to ~50×50 = 2500 cells (reasonable given target at 31, 39)
- **Space**: O(W × H) for visited set and queue
  - Expected to be well under 10,000 cells

### Step 4: Main Execution Flow
1. Read input file and parse favorite number
2. Call `find_shortest_path((1, 1), (31, 39), favorite_number)`
3. Print the result (number of steps)

### Step 5: Code Structure
```
# Constants and input parsing
FAVORITE_NUMBER = int(open('input.md').read().strip())
START = (1, 1)
TARGET = (31, 39)

# Helper function
def is_open_space(x, y, favorite_number):
    # Implementation here
    pass

# Main algorithm
def find_shortest_path(start, target, favorite_number):
    # BFS implementation here
    pass

# Execution
if __name__ == "__main__":
    result = find_shortest_path(START, TARGET, FAVORITE_NUMBER)
    print(result)
```

## Optimization Considerations

### Why BFS is Sufficient:
- Target is relatively close (31, 39 from 1, 1)
- Expected exploration area is small (~2000-3000 cells maximum)
- Each cell check is O(1)
- Total runtime: O(1) per cell × ~2500 cells = very fast

### Potential Optimizations (NOT necessary for this problem):
- **A* with Manhattan distance**: Would reduce cells explored but adds heuristic overhead
- **Bidirectional BFS**: Search from both start and target simultaneously
- **Memoization of cell types**: Cache results of `is_open_space` (minimal benefit as it's already O(1))

### Why These Are Unnecessary:
- Problem size is small (target at 31, 39)
- BFS will solve in milliseconds
- No need to optimize further for a one-time script

## Expected Runtime
- **Best case**: O(Manhattan distance) ≈ 68 cells if direct path exists
- **Worst case**: O(50 × 50) ≈ 2500 cells if significant detours needed
- **Actual runtime**: < 100ms on modern hardware

## Summary
Use BFS with a queue and visited set to find the shortest path in the procedurally-generated maze. The algorithm is simple, correct, and efficient enough for the given problem constraints.
