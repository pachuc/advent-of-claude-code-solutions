# Implementation Plan: Digital Plumber - Part 2

## Problem Summary
Count the total number of distinct connected components (groups) in a graph of program connections. Each group represents a set of programs that can communicate with each other directly or indirectly, but cannot communicate with programs in other groups.

## Algorithm Overview
This is a standard **connected components** problem in graph theory. We'll use the same BFS approach from Part 1, but apply it iteratively to find all components.

**Time Complexity**: O(V + E) where V = number of programs, E = number of edges
**Space Complexity**: O(V) for tracking visited nodes and the graph structure

## Detailed Implementation Steps

### Step 1: Reuse Parser from Part 1
- **File**: `part_1_solution.py` already has `parse_input()` function at lines 4-28
- **Action**: Copy this function as-is - it correctly parses the input into an adjacency list
- **No changes needed**: The parsing logic is identical for both parts

### Step 2: Modify the BFS Function
- **From Part 1**: `find_connected_group(graph, start_node)` at lines 31-58
- **Modification needed**: Return the set of visited nodes instead of the count
- **Rationale**: We need to track which nodes have been assigned to groups to avoid counting them multiple times
- **Specific change**: Modify line 58 in `part_1_solution.py`:
  ```python
  # OLD - Part 1 version:
  return len(visited)

  # NEW - Part 2 version:
  return visited
  ```
- **New signature**: `find_connected_group(graph, start_node)` → returns `set` of visited nodes (instead of `int`)

### Step 3: Implement Main Algorithm - Count All Groups
Create a new function `count_all_groups(graph)`:

```python
def count_all_groups(graph):
    """Count total number of connected components in the graph.

    Args:
        graph: Adjacency list representation

    Returns:
        Integer count of distinct groups
    """
    visited_global = set()  # Track all visited nodes across all groups
    group_count = 0

    # Iterate through all nodes in the graph
    for node in graph:
        # If node hasn't been assigned to a group yet
        if node not in visited_global:
            # Find all nodes in this component
            group_nodes = find_connected_group(graph, node)

            # Mark all nodes in this group as visited
            visited_global.update(group_nodes)

            # Increment group counter
            group_count += 1

    return group_count
```

**Why this works**:
- We iterate through every node in the graph
- For each unvisited node, we perform BFS to find its entire connected component
- We mark all nodes in that component as visited
- Each BFS traversal discovers exactly one new group
- The count equals the number of BFS traversals needed to cover all nodes

### Step 4: Update Main Function
Modify the `main()` function:

```python
def main():
    """Main function to solve the problem."""
    # Read input
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse graph
    graph = parse_input(lines)

    # Count all groups (CHANGED from Part 1)
    total_groups = count_all_groups(graph)

    # Output result
    print(total_groups)
```

### Step 5: Verify Edge Cases and Validation
Ensure the implementation handles:
1. **Self-loops**: Programs connected to themselves (e.g., `4 <-> 4, 1473`)
   - Already handled by the adjacency list representation
2. **Isolated nodes**: Nodes only connected to themselves
   - Will be counted as groups of size 1
3. **Large components**: The main group with 239 programs
   - BFS handles efficiently
4. **Empty lines**: In input parsing
   - Already handled by Part 1 parser (lines 16-18)

**Important Validation**: When testing on the actual input, verify that:
- One of the discovered groups contains exactly 239 programs (matching Part 1 answer)
- This group should contain node 0
- This serves as a critical sanity check that the algorithm is working correctly

## Implementation Checklist
- [ ] Copy `parse_input()` function from Part 1 (no changes needed)
- [ ] Modify `find_connected_group()` return statement: change `return len(visited)` to `return visited`
- [ ] Implement `count_all_groups()` function with global visited tracking
- [ ] Update `main()` to call `count_all_groups()` instead of `find_connected_group(graph, 0)`
- [ ] Keep the same input reading and output printing logic
- [ ] Test with the example from problem statement (expected output: 2)
- [ ] Validate that one group has size 239 when testing on actual input

## Expected Input/Output
- **Input**: Same format as Part 1 (2000 programs with connections from `input.md`)
- **Output**: Single integer (total number of groups)
- **Example**: For the sample input, output should be `2` (one group of 6 programs {0,2,3,4,5,6} and one isolated program {1})

## Key Differences from Part 1
1. **Part 1**: Find size of ONE specific component (containing node 0)
2. **Part 2**: Count the NUMBER of all components in the entire graph
3. **Code reuse**: ~80% of Part 1 code can be reused with minor modifications

## Notes on Implementation Approach

### Why BFS?
- BFS (used in Part 1) is appropriate and efficient with O(V + E) time complexity
- DFS would also work with the same complexity - BFS is chosen for consistency with Part 1
- Union-Find is an alternative algorithm for connected components, but BFS is simpler for this problem size

### Defensive Programming
- The input file is assumed to be well-formed (all referenced nodes are defined)
- For Advent of Code inputs, this is a safe assumption
- In production code, you might add error handling for missing node definitions
