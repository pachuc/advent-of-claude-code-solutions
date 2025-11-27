# Implementation Plan: A Regular Map

## Overview
We need to parse a regex describing routes through a facility, build a graph of rooms and doors, then find the maximum shortest path distance from the starting position.

## Revision Summary (v2)

This plan has been revised based on critique feedback to address:

1. **Clarified Branch Handling Logic**: Added explicit pseudocode and data structures for handling `|` and `)` operators
2. **Added Example Walkthrough**: Included step-by-step table showing stack state and positions for `^N(E|W)S$`
3. **Refined Stack Strategy**: Provided clear recommendation to use stack of tuples `(starting_positions, branch_endpoints)`
4. **Improved Documentation**: Added code examples for adjacency graph building
5. **Coordinate System Clarification**: Explicitly stated using screen coordinates (y increases downward)

## Algorithm Choice

### Graph Representation
- Use a dictionary/set-based graph where nodes are (x, y) coordinates
- Store edges as a set of door positions between adjacent rooms
- This allows O(1) lookup for checking if a door exists between two rooms

### Parsing Strategy
- Use a stack-based recursive approach to handle nested branches
- Track current position(s) as we parse the regex
- When encountering '(', save current positions and push to stack
- When encountering '|', restore positions from the branching point
- When encountering ')', merge all branch endpoint positions

### Shortest Path Algorithm
- Use BFS (Breadth-First Search) from the starting position
- BFS guarantees shortest path in unweighted graphs
- Track the distance (number of doors) to each room
- Return the maximum distance found

## Recommended Approach for Branch Handling

For clearest implementation, use this approach:

**Stack Structure:**
- Single stack storing tuples: `(starting_positions, branch_endpoints_accumulator)`
- `starting_positions`: set of positions where the `(` was encountered
- `branch_endpoints_accumulator`: list of sets, one for each `|` alternative

**Parsing Logic:**
```python
stack = []
current_positions = {(0, 0)}

for char in regex:
    if char == '(':
        stack.append((current_positions, []))
    elif char == '|':
        starting_positions, branch_endpoints = stack[-1]
        branch_endpoints.append(current_positions)
        current_positions = starting_positions.copy()
    elif char == ')':
        starting_positions, branch_endpoints = stack.pop()
        branch_endpoints.append(current_positions)
        # Merge all branch alternatives
        current_positions = set()
        for endpoints in branch_endpoints:
            current_positions.update(endpoints)
```

This approach clearly separates concerns and handles nested branches naturally.

## Step-by-Step Implementation

### Step 1: Input Parsing
- Read the regex string from input
- Strip the leading '^' and trailing '$' characters
- The remaining string contains the actual route directions

### Step 2: Build the Graph via Regex Parsing
**Function: `parse_regex_and_build_graph(regex_string)`**

Data structures needed:
- `doors`: Set of tuples representing door positions (could use frozenset of two adjacent room coords)
- `current_positions`: Set of (x, y) tuples representing current position(s) during parsing
- `stack`: List to save positions at branch points

Algorithm:
1. Initialize starting position at (0, 0)
2. Initialize `current_positions = {(0, 0)}`
3. Initialize empty `doors` set
4. Initialize empty `stack` list

5. Create a `branch_endpoints` list to accumulate position sets from each branch alternative

6. Iterate through each character in the regex:
   - **'N', 'S', 'E', 'W'**: For each position in `current_positions`:
     - Calculate new position based on direction
     - Add door between current and new position to `doors` set
     - Move position to new position

     **Detailed logic:**
     ```python
     new_positions = set()
     for pos in current_positions:
         new_pos = (pos[0] + dx, pos[1] + dy)  # Based on direction
         doors.add(frozenset([pos, new_pos]))
         new_positions.add(new_pos)
     current_positions = new_positions
     ```

   - **'('**: Start of branch
     - Push current `current_positions` to stack
     - Initialize empty `branch_endpoints` list for this branch level

   - **'|'**: Branch alternative separator
     - Append current `current_positions` to `branch_endpoints` (these are endpoints of previous alternative)
     - Restore `current_positions` from stack top (peek, don't pop)
     - Continue parsing next alternative from same starting point

   - **')'**: End of branch
     - Append current `current_positions` to `branch_endpoints` (endpoints of final alternative)
     - Merge all sets in `branch_endpoints` into a single set
     - Set `current_positions` to this merged set
     - Pop the saved positions from stack
     - Clear `branch_endpoints` for next branch

7. Return the `doors` set

**Example Walkthrough: `^N(E|W)S$`**

Using screen coordinates (y increases downward):

| Step | Char | current_positions | stack | branch_endpoints | doors | Notes |
|------|------|------------------|-------|------------------|-------|-------|
| 0 | ^ | {(0,0)} | [] | [] | {} | Start |
| 1 | N | {(0,-1)} | [] | [] | {frozenset([(0,0),(0,-1)])} | Move north |
| 2 | ( | {(0,-1)} | [{(0,-1)}] | [] | - | Push to stack |
| 3 | E | {(1,-1)} | [{(0,-1)}] | [] | {... , frozenset([(0,-1),(1,-1)])} | Move east |
| 4 | \| | {(0,-1)} | [{(0,-1)}] | [{(1,-1)}] | - | Save {(1,-1)}, restore from stack |
| 5 | W | {(-1,-1)} | [{(0,-1)}] | [{(1,-1)}] | {... , frozenset([(0,-1),(-1,-1)])} | Move west |
| 6 | ) | {(1,-1),(-1,-1)} | [] | [] | - | Merge [{(1,-1)}, {(-1,-1)}] |
| 7 | S | {(1,0),(-1,0)} | [] | [] | {... , frozenset([(1,-1),(1,0)]), frozenset([(-1,-1),(-1,0)])} | Move south from both |
| 8 | $ | - | - | - | - | End |

**Note on Nested Branches:**
For nested branches like `^(N(E|W)|S)$`, we need to handle the stack properly:
- When we hit the inner `(`, we push the current positions and start a NEW `branch_endpoints` list
- The outer branch's `branch_endpoints` is preserved on the stack along with positions
- Need to use a stack of tuples: `(starting_positions, accumulated_endpoints)` OR handle endpoints separately with proper scoping

**Implementation details:**
- For movement directions, use a direction map (using screen coordinates where y increases downward):
  - 'N': (0, -1) - decrease y
  - 'S': (0, 1) - increase y
  - 'E': (1, 0) - increase x
  - 'W': (-1, 0) - decrease x

- **Refined Stack Strategy for Nested Branches:**
  To properly handle nested branches, the stack should store tuples of:
  `(starting_positions_for_this_branch, accumulated_endpoints_from_outer_branch)`

  However, a simpler approach is to use a SEPARATE stack for branch endpoints:
  - `position_stack`: stores starting positions for each `(`
  - `endpoints_stack`: stores accumulated branch endpoints for each level

  On `(`: push to both stacks
  On `|`: use current level of endpoints_stack
  On `)`: pop from both stacks

### Step 3: Build Adjacency Graph from Doors
**Function: `build_adjacency_graph(doors)`**

Convert the doors set into an adjacency list for BFS:
1. Create empty defaultdict(set) for adjacency list
2. For each door (represented as a frozenset of two room positions):
   - Extract both positions from the frozenset (convert to list or iterate)
   - Add bidirectional edges: `graph[pos1].add(pos2)` and `graph[pos2].add(pos1)`
3. Return adjacency graph

**Example:**
```python
from collections import defaultdict

def build_adjacency_graph(doors):
    graph = defaultdict(set)
    for door in doors:
        pos1, pos2 = door  # Unpack the two positions from frozenset
        graph[pos1].add(pos2)
        graph[pos2].add(pos1)
    return graph
```

### Step 4: Find Maximum Shortest Path Distance
**Function: `find_max_distance(adjacency_graph, start=(0, 0))`**

Use BFS to find shortest path to all reachable rooms:
1. Initialize queue with starting position and distance 0
2. Initialize visited set
3. Initialize max_distance = 0
4. While queue is not empty:
   - Dequeue position and current distance
   - If already visited, skip
   - Mark as visited
   - Update max_distance if current distance is greater
   - For each neighbor in adjacency graph:
     - If not visited, enqueue with distance + 1
5. Return max_distance

### Step 5: Main Function
**Function: `solve()`**

1. Read input from file
2. Strip whitespace and remove '^' and '$'
3. Call `parse_regex_and_build_graph(regex_string)`
4. Call `build_adjacency_graph(doors)`
5. Call `find_max_distance(adjacency_graph)`
6. Print the result

## Complexity Analysis

### Time Complexity
- Parsing: O(R) where R is the length of the regex
  - Each character processed once
  - Branch handling involves set operations which are typically O(P) where P is number of positions
  - In worst case: O(R * P) but P is bounded by the number of unique rooms

- BFS: O(V + E) where V is number of rooms and E is number of doors
  - Each room visited once
  - Each door (edge) examined once from each direction

- Overall: O(R * P + V + E)
  - For the given input size (~10K characters), this should be very efficient

### Space Complexity
- Doors set: O(D) where D is number of unique doors
- Positions during parsing: O(P) where P can be exponential in worst case with many branches
  - However, positions get merged and duplicate rooms are naturally deduplicated
- Adjacency graph: O(V + E)
- BFS queue and visited set: O(V)

- Overall: O(D + V + E + P)

## Edge Cases to Handle

1. **Empty branches**: `(NEWS|)` - one branch is empty
   - The empty branch means "no movement", so positions stay the same

2. **Multiple consecutive branches**: `(A|B)(C|D)`
   - Need to properly track positions between branches

3. **Deeply nested branches**: `((A|B)|C)`
   - Stack-based approach handles this naturally

4. **Long chains without branches**: `NNNNEEEEESSSS`
   - Simple linear path, no special handling needed

5. **Starting position**: Always (0, 0)
   - Marked as 'X' in map visualization, but we just track as a coordinate

## Data Structure Choices

### Doors Representation
Option 1: Set of tuples `{((x1,y1), (x2,y2)), ...}`
- Use sorted tuple or frozenset to ensure uniqueness regardless of direction

Option 2: Set of normalized door positions
- For horizontal doors: `('H', min_x, max_x, y)`
- For vertical doors: `('V', x, min_y, max_y)`

**Choice**: Option 1 with frozenset for simplicity and clarity
- Example: `doors.add(frozenset([(x1, y1), (x2, y2)]))`

### Adjacency Graph
- `defaultdict(set)` where key is (x, y) and value is set of adjacent (x, y) positions
- Direct and intuitive for BFS

## Complete Pseudocode

Putting it all together:

```python
def solve():
    # Step 1: Read and parse input
    with open('input.txt') as f:
        regex = f.read().strip()
    regex = regex[1:-1]  # Remove ^ and $

    # Step 2: Build doors set
    doors = parse_regex_and_build_graph(regex)

    # Step 3: Build adjacency graph
    graph = build_adjacency_graph(doors)

    # Step 4: Find max distance using BFS
    max_dist = find_max_distance(graph, start=(0, 0))

    # Step 5: Return result
    return max_dist

def parse_regex_and_build_graph(regex):
    doors = set()
    current_positions = {(0, 0)}
    stack = []
    directions = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}

    for char in regex:
        if char in 'NSEW':
            dx, dy = directions[char]
            new_positions = set()
            for x, y in current_positions:
                new_x, new_y = x + dx, y + dy
                doors.add(frozenset([(x, y), (new_x, new_y)]))
                new_positions.add((new_x, new_y))
            current_positions = new_positions

        elif char == '(':
            stack.append((current_positions, []))

        elif char == '|':
            starting_positions, branch_endpoints = stack[-1]
            branch_endpoints.append(current_positions)
            current_positions = starting_positions.copy()

        elif char == ')':
            starting_positions, branch_endpoints = stack.pop()
            branch_endpoints.append(current_positions)
            current_positions = set()
            for endpoints in branch_endpoints:
                current_positions.update(endpoints)

    return doors

def build_adjacency_graph(doors):
    from collections import defaultdict
    graph = defaultdict(set)
    for door in doors:
        pos1, pos2 = door
        graph[pos1].add(pos2)
        graph[pos2].add(pos1)
    return graph

def find_max_distance(graph, start):
    from collections import deque
    queue = deque([(start, 0)])
    visited = {start}
    max_distance = 0

    while queue:
        pos, dist = queue.popleft()
        max_distance = max(max_distance, dist)

        for neighbor in graph[pos]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return max_distance
```

## Implementation Order

1. Write helper function to move in a direction (integrated into parse function)
2. Write the regex parser with graph building
3. Write adjacency graph builder
4. Write BFS for finding max distance
5. Write main function to tie everything together
6. Test with provided examples
7. Run on actual input
