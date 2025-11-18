# Implementation Plan: Digital Plumber

## Problem Summary
Find all programs that are connected to program ID 0 either directly or indirectly through a network of bidirectional pipe connections. This is a graph connectivity/reachability problem.

## Algorithm Analysis

### Problem Type
- **Graph Connectivity Problem**: Finding all nodes reachable from a starting node
- **Graph Type**: Undirected graph (bidirectional connections)
- **Task**: Count all nodes in the connected component containing node 0

### Algorithm Choice: BFS (Breadth-First Search)
**Rationale:**
- Both BFS and DFS have O(V + E) time complexity for this problem
- BFS is slightly more intuitive for "reachability" problems
- BFS uses iteration (more Pythonic), DFS typically uses recursion which could hit Python's recursion limit with deep graphs
- For this input size (~2000 nodes), both are equally efficient

**Alternative:** DFS would work equally well with similar complexity

### Complexity Analysis
- **Input Size**: 2000 programs (nodes), approximately 3000-6000 connections (edges)
- **Time Complexity**: O(V + E) where V = number of vertices, E = number of edges
  - For this input: O(2000 + ~4000) ≈ O(6000) - very efficient
- **Space Complexity**: O(V) for the visited set and adjacency list
  - For this input: O(2000) - minimal memory usage

## Implementation Steps

### Step 1: Parse Input
**Goal**: Convert the text input into a usable graph data structure

**Approach:**
1. Read the input file line by line
2. For each line, parse the format: `<program_id> <-> <connected_id_1>, <connected_id_2>, ...`
3. Store as an adjacency list (dictionary mapping program_id to list of connected programs)

**Data Structure Choice:**
- Use `dict[int, list[int]]` for the adjacency list
- Dictionary provides O(1) lookup time
- Lists store the neighbors for each node

**Implementation Details:**
```python
# Pseudocode
graph = {}
for line in input_lines:
    # Skip empty lines
    if not line.strip():
        continue
    # Split by '<->'
    parts = line.split('<->')
    program_id = int(parts[0].strip())
    # Split connections by comma
    connections = [int(x.strip()) for x in parts[1].split(',')]
    graph[program_id] = connections
```

**Important Input Format Assumption:**
- The input file already represents bidirectional edges explicitly
- If program A connects to B, both "A <-> ... B ..." and "B <-> ... A ..." appear in the input
- This has been verified by examining the input: line 1 shows "0 <-> 122, 874, 1940" and checking lines for 122, 874, and 1940 confirms they list 0 as a connection
- Therefore, we do NOT need to manually add reverse edges during parsing

**Edge Cases to Handle:**
- Self-connections (e.g., "4 <-> 4, 1473") - should be included but won't affect BFS
- Single connections vs. multiple connections
- Whitespace variations in input (handled by strip())
- Empty lines (handled by skip check)

### Step 2: Implement BFS Traversal
**Goal**: Find all programs reachable from program 0

**Approach:**
1. Initialize a queue with program 0
2. Initialize a set to track visited programs
3. While queue is not empty:
   - Dequeue a program
   - If already visited, skip
   - Mark as visited
   - Add all its neighbors to the queue
4. Return the count of visited programs

**Implementation Details:**
```python
# Pseudocode
from collections import deque

def find_connected_group(graph, start_node):
    queue = deque([start_node])
    visited = set()

    while queue:
        current = queue.popleft()

        # Skip if already visited (happens when same node added to queue multiple times)
        if current in visited:
            continue

        visited.add(current)

        # Add all unvisited neighbors to queue
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append(neighbor)

    return len(visited)
```

**BFS Strategy Explanation:**
- We check if a node is visited BOTH when dequeuing (line 8) AND before enqueueing (line 15)
- The dequeue check prevents processing the same node twice
- The enqueue check reduces queue size (optimization)
- Both checks are necessary: dequeue check for correctness, enqueue check for efficiency

**Why BFS over DFS:**
- Iterative (no recursion depth issues with Python's default recursion limit)
- Natural FIFO queue behavior matches the "spread out from node 0" mental model
- Easier to debug and visualize

**Optimization Notes:**
- Using set for O(1) visited checks instead of list with O(n) checks
- Checking before enqueueing reduces memory usage (smaller queue)

### Step 3: Main Program Flow
**Goal**: Orchestrate the solution

**Steps:**
1. Read input from file
2. Parse input into graph
3. Run BFS from node 0
4. Output the count

**Implementation Details:**
```python
# Pseudocode
def main():
    # Read input
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse graph
    graph = parse_input(lines)

    # Find connected group
    count = find_connected_group(graph, 0)

    # Output result
    print(count)
```

### Step 4: Code Organization
**File Structure:**
- Single Python file: `solution.py`
- Functions:
  - `parse_input(lines)` -> `dict[int, list[int]]`
  - `find_connected_group(graph, start_node)` -> `int`
  - `main()` -> None

**No Need For:**
- Error handling for malformed input (problem guarantees valid input)
- Logging/debugging output (simple script)
- Type hints (helpful but not required for this simple script)
- Classes or complex abstractions (overkill for this problem)

## Performance Considerations

### Expected Runtime
- Parsing: O(V + E) ≈ 6000 operations
- BFS: O(V + E) ≈ 6000 operations
- Total: ~12000 operations - **near instantaneous** (< 1ms)

### Memory Usage
- Memory usage is **negligible** for this input size (~2000 nodes)
- All data structures fit comfortably in memory
- No special memory optimizations needed

### Scalability
- Current approach scales to **millions of nodes** efficiently
- No optimization needed for this input size
- If input were 10x larger (20K nodes), same algorithm would work fine

## Alternative Approaches Considered

### 1. DFS (Depth-First Search)
- **Pros**: Same time complexity, slightly less memory (no queue)
- **Cons**: Recursion depth issues in Python, less intuitive
- **Verdict**: BFS is better for this use case

### 2. Union-Find (Disjoint Set Union)
- **Pros**: Can find all connected components efficiently
- **Cons**: More complex to implement, overkill for single-source reachability
- **Verdict**: Unnecessary for this problem

### 3. Connected Components Algorithm
- **Pros**: Can find all groups in one pass
- **Cons**: We only need one group (containing node 0)
- **Verdict**: More than needed

## Implementation Checklist
- [ ] Create `parse_input()` function
- [ ] Create `find_connected_group()` function with BFS
- [ ] Create `main()` function
- [ ] Test with example input
- [ ] Test with actual input
- [ ] Verify output format (single integer)
