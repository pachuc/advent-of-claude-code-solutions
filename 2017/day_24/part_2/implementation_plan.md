# Implementation Plan: Electromagnetic Moat Bridge Builder - Part 2

## Problem Summary
Find the **longest** bridge possible from magnetic components. If multiple bridges have the same maximum length, return the **strength** of the strongest one among them.

## Key Differences from Part 1
- **Part 1**: Maximized strength only
- **Part 2**: Maximize length first, then strength among bridges of that maximum length

## Reusable Components from Part 1 Solution

The Part 1 solution (`part_1_solution.py`) provides excellent foundational code that can be adapted:

1. **`parse_input(filename)`** - Can be reused as-is
2. **`build_port_index(components)`** - Can be reused as-is
3. **DFS backtracking approach** - Core algorithm structure is perfect, just needs modification to track length
4. **Overall structure** - Modular design is well-suited for Part 2

## Implementation Steps

### Step 1: Copy and Adapt Parsing & Indexing Functions
- Copy `parse_input()` function from Part 1 (no changes needed)
- Copy `build_port_index()` function from Part 1 (no changes needed)
- These functions work perfectly for Part 2

### Step 2: Modify the DFS Function to Track Both Length and Strength

**Current Part 1 signature:**
```python
def find_max_strength(components, port_map, current_port, used, current_strength)
```

**New Part 2 signature:**
```python
def find_longest_strongest(components, port_map, current_port, used, current_length, current_strength)
```

**Key changes:**
1. Add `current_length` parameter to track number of components used
2. Return a tuple `(length, strength)` instead of just strength
3. When comparing branches, prioritize by length first, then by strength
4. Increment `current_length` by 1 for each component added

**Algorithm logic:**
```python
def find_longest_strongest(components, port_map, current_port, used, current_length, current_strength):
    # Base case: if no more components can be added, the current bridge
    # is a valid complete bridge. Initialize best with current state,
    # then try to improve by exploring all possible extensions.
    best = (current_length, current_strength)

    # Try all unused components with matching port
    for component_index in port_map.get(current_port, []):
        if component_index in used:
            continue

        port_a, port_b = components[component_index]

        # Determine next port
        next_port = port_b if port_a == current_port else port_a

        # Calculate component strength
        component_strength = port_a + port_b

        # Recurse with this component added
        used.add(component_index)
        result = find_longest_strongest(
            components,
            port_map,
            next_port,
            used,
            current_length + 1,  # Length increases
            current_strength + component_strength
        )
        used.remove(component_index)

        # Compare: prioritize longer, then stronger
        if result[0] > best[0] or (result[0] == best[0] and result[1] > best[1]):
            best = result

    return best
```

### Step 3: Update the Solve Function

**Changes needed:**
```python
def solve(components):
    port_map = build_port_index(components)
    used = set()
    length, strength = find_longest_strongest(
        components,
        port_map,
        current_port=0,
        used=used,
        current_length=0,  # Start with 0 components
        current_strength=0
    )
    # Return only strength - the length was used internally to find
    # the longest bridge, but the answer requires only its strength
    return strength
```

### Step 4: Keep Main Function Structure

The main function can remain largely the same:
```python
def main():
    components = parse_input('input.md')
    result = solve(components)
    print(result)
```

## Algorithm Complexity Analysis

### Time Complexity
- **Worst case**: O(n! * n) where n is the number of components
  - At each step, we may try any unused component
  - With n components, worst case is exploring n! permutations
  - For each path, we do O(n) work
- **Expected case**: Much better due to:
  - Port matching constraints significantly prune the search space
  - Most components won't have matching ports at each step
  - The port_map optimization provides O(1) lookup for candidates

### Space Complexity
- **Recursion stack**: O(n) - maximum depth is number of components
- **Data structures**: O(n) for components list, port_map, and used set
- **Overall**: O(n)

### Input Size Considerations
- Input has 54 components (small enough for exhaustive search)
- Port values range from 0-50, providing good constraint
- DFS with backtracking is appropriate for this input size
- No optimizations needed beyond the port_map indexing already in Part 1

## Code Structure

```
solution.py
├── parse_input(filename)           # Reused from Part 1
├── build_port_index(components)    # Reused from Part 1
├── find_longest_strongest(...)     # Modified from Part 1's find_max_strength
├── solve(components)               # Modified from Part 1
└── main()                          # Similar to Part 1
```

## Algorithm Correctness

The DFS approach guarantees finding the optimal solution because:

1. **Exhaustive Exploration**: The recursive DFS explores every possible valid bridge that can be built
2. **Correct Comparison**: At each step, we compare (length, strength) tuples, which naturally prioritizes length first, then strength
3. **Complete Search Space**: By trying all unused components at each step and backtracking properly, we never miss a potential bridge
4. **Optimal Substructure**: The longest+strongest bridge from any state is built from the longest+strongest bridges of subsequent states

Since we explore all possibilities and always keep the best (longest, then strongest) result, we're guaranteed to find the optimal answer.

## Implementation Notes

1. **Comparison Logic**: The key difference is in how we compare bridges:
   - Part 1: `max_strength = max(max_strength, branch_strength)`
   - Part 2: `if length > best_length or (length == best_length and strength > best_strength)`

2. **Return Values**: Tracking tuples (length, strength) throughout makes comparison clean

3. **Base Case**: An empty bridge (0 components, 0 strength) is valid, which is why we initialize with `current_length=0`

4. **Backtracking**: The used set must still be properly maintained with add/remove for correct backtracking

5. **Port Map Optimization**: The `build_port_index` from Part 1 is crucial for efficiency - it allows O(1) lookup of components with a specific port type, rather than O(n) linear search

6. **Testing**: Should verify with the example from problem statement first before running on actual input
