# Implementation Plan: Electromagnetic Moat Bridge Builder

## Problem Analysis

This is a **graph traversal problem** with backtracking. We need to:
- Find all possible valid bridges starting from port 0
- Track used components (each can only be used once)
- Calculate strength for each bridge
- Return the maximum strength

### Key Observations:
1. Input size: ~54 components - small enough for exhaustive search with backtracking
2. Components are bidirectional (0/3 can connect via 0 or 3)
3. This is essentially finding the maximum-weight path in a graph where nodes can only be visited once
4. Brute force with pruning is feasible given the input size

## Algorithm Choice: Depth-First Search with Backtracking

**Rationale:**
- Input size (~54 components) allows exhaustive search
- Need to explore all possible bridge combinations
- DFS with backtracking naturally handles "use once" constraint
- Can track maximum strength during exploration

**Time Complexity:** O(n! * n) worst case, but pruned significantly in practice
**Space Complexity:** O(n) for recursion stack and used component tracking

## Implementation Steps

### Step 1: Parse Input and Build Index
**Goal:** Convert input into usable data structures with efficient lookup

**Details:**
- Read input file line by line
- Parse each line in format "A/B" into tuple (A, B)
- Store as list of tuples: `[(48, 5), (25, 10), ...]`
- Convert strings to integers for calculations
- Build port-to-component index for efficient lookup
- Add basic error handling for malformed input

**Code Structure:**
```python
def parse_input(filename):
    components = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                a, b = line.split('/')
                components.append((int(a), int(b)))
            except (ValueError, AttributeError):
                # Skip malformed lines
                continue
    return components

def build_port_index(components):
    """Build a mapping from port number to list of component indices."""
    port_map = {}
    for i, (a, b) in enumerate(components):
        port_map.setdefault(a, []).append(i)
        if a != b:  # Avoid duplicates for same-port components
            port_map.setdefault(b, []).append(i)
    return port_map
```

### Step 2: Build DFS Recursive Function with Port Index
**Goal:** Explore all possible bridges using backtracking with optimized lookup

**Function Signature:**
```python
def find_max_strength(components, port_map, current_port, used, current_strength):
    """
    Args:
        components: List of all available components (tuples)
        port_map: Dictionary mapping port number to list of component indices
        current_port: The port type we need to match next
        used: Set of indices of components already used
        current_strength: Accumulated strength so far

    Returns:
        Maximum strength achievable from this state
    """
```

**Algorithm Logic:**
1. **Base case**: Current strength is a valid bridge (even if no further connections)
2. **Recursive case**: Try all unused components that can connect to current_port
3. For each compatible component (using port_map for efficient lookup):
   - Determine which port connects (matches current_port)
   - Calculate new current_port (the other port of the component)
   - Add component to used set
   - Add component strength to current_strength
   - Recurse
   - Backtrack (remove from used set)
4. Return maximum strength found across all branches

**Optimized Pseudocode:**
```
max_strength = current_strength  # Current bridge is valid (handles no components with port 0)

# Only check components that have the current_port (optimization)
for component_index in port_map.get(current_port, []):
    if component_index in used:
        continue

    port_a, port_b = components[component_index]

    # Determine which end connects and which is free
    if port_a == current_port:
        next_port = port_b
    else:  # port_b == current_port
        next_port = port_a

    # Calculate strength of this component
    component_strength = port_a + port_b

    # Explore this branch
    used.add(component_index)
    branch_strength = find_max_strength(
        components,
        port_map,
        next_port,
        used,
        current_strength + component_strength
    )
    used.remove(component_index)

    # Track maximum
    max_strength = max(max_strength, branch_strength)

return max_strength
```

**Key Optimization:**
- Instead of checking all 54 components at each level, we only check components that have the required port
- This significantly reduces the number of iterations per recursive level
- The port_map lookup is O(1), and we iterate only over matching components

### Step 3: Initialize and Start Search
**Goal:** Set up initial conditions and begin DFS

**Details:**
- Build the port index for efficient lookup
- Starting port is always 0 (given in problem)
- Initial used set is empty
- Initial strength is 0
- Call the recursive function

**Code Structure:**
```python
def solve(components):
    port_map = build_port_index(components)
    used = set()
    return find_max_strength(components, port_map, current_port=0, used=used, current_strength=0)
```

**Edge Case Handling:**
- If no components have port 0, `port_map.get(0, [])` returns empty list
- The DFS function returns `current_strength` (which is 0)
- This correctly handles the "no valid bridge" case

### Step 4: Main Entry Point
**Goal:** Orchestrate parsing, solving, and output

**Code Structure:**
```python
def main():
    components = parse_input('input.md')
    max_strength = solve(components)
    print(max_strength)

if __name__ == '__main__':
    main()
```

## Optimization Strategy

### Optimizations Included:
1. **Pre-indexing (port_map)**: Build dictionary of port → list of component indices
   - **Benefits**: Only check components that can actually connect (O(matches) instead of O(n) per level)
   - **Cost**: Minimal - ~10 lines of setup code, negligible memory (~few KB)
   - **Decision**: Include from the start - simple to implement and provides significant speedup

### Why This is Sufficient:
1. **Small Input Size**: ~54 components means even unoptimized approach would work
2. **Natural Pruning**: Port map ensures we only explore valid branches
3. **Early Termination**: Dead ends naturally return current strength

### Optimizations NOT Needed:
1. **Memoization**: Caching (current_port, frozenset(used)) → max_strength
   - Would require expensive frozenset conversions
   - Unlikely to have many repeated states in this problem
   - Adds significant complexity for minimal gain with 54 components

### Performance Expectations:
- With port_map optimization: Should complete in < 1 second for 54 components
- Without optimization: Would still complete in < 5 seconds

## Data Structures Summary

| Structure | Purpose | Type |
|-----------|---------|------|
| `components` | Store all components | `List[Tuple[int, int]]` |
| `port_map` | Map port numbers to component indices | `Dict[int, List[int]]` |
| `used` | Track used component indices | `Set[int]` |
| `current_port` | Port type to match next | `int` |
| `current_strength` | Accumulated strength | `int` |

## Edge Cases to Handle in Code

1. **Empty input file**: Returns empty list, algorithm returns 0 (no bridge possible)
2. **No components with port 0**: port_map.get(0, []) returns [], algorithm returns 0
3. **Only one component with port 0**: Recursion tries it and returns its strength
4. **Component with matching ports** (e.g., 5/5 or 13/13): Works normally, both ports are the same value
5. **Component 0/0**: Can connect at start (port 0) and leaves port 0 free - handled correctly
6. **Dead ends**: Bridge cannot continue - naturally returns current_strength
7. **All components used**: Natural termination when port_map lookup finds no unused components
8. **Malformed input lines**: Skipped during parsing (try/except block)

## Complete File Structure

```
solution.py:
    - parse_input(filename) -> List[Tuple[int, int]]
    - build_port_index(components) -> Dict[int, List[int]]
    - find_max_strength(components, port_map, current_port, used, current_strength) -> int
    - solve(components) -> int
    - main()
```

## Execution Flow

```
1. main() called
2. Parse input into components list (with error handling for malformed lines)
3. Call solve(components)
4. solve() builds port_map index
5. solve() initializes empty used set and calls find_max_strength with port=0
6. find_max_strength explores all paths via DFS/backtracking:
   - Uses port_map to efficiently find matching components
   - Tracks used components to avoid reuse
   - Recursively explores all valid bridges
   - Returns maximum strength across all branches
7. Print result
```
