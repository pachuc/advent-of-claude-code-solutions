# Implementation Plan: Topological Sort with Alphabetical Ordering

## Problem Analysis

This is a classic topological sort problem with an additional constraint: when multiple nodes are available for processing, we must select them in alphabetical order. The input contains 101 dependency relationships among uppercase letters A-Z.

### Key Observations:
- We have at most 26 unique steps (A-Z)
- The input has 101 lines, meaning many duplicate or redundant dependencies
- We need to build a dependency graph and process nodes in topological order
- When multiple nodes are ready, we select alphabetically first

### Algorithm Complexity:
- **Time Complexity**: O(V + E) where V is number of unique steps and E is number of dependencies
  - Building graph: O(E)
  - Processing nodes: O(V²) in worst case with simple implementation, or O(V log V) with priority queue
  - Given V ≤ 26, any reasonable approach will be fast
- **Space Complexity**: O(V + E) for storing the graph

## Step-by-Step Implementation Plan

### Step 1: Parse Input
**Goal**: Extract dependency relationships from input text

**Implementation**:
1. Read the input (from file or string)
2. For each line matching the pattern "Step X must be finished before step Y can begin."
   - Extract the prerequisite step (X)
   - Extract the dependent step (Y)
3. Store these as (prerequisite, dependent) tuples

**Data Structure**: List of tuples `[(prerequisite, dependent), ...]`

**Parsing Strategy**:
```python
# Use string slicing (simplest for fixed format)
# Line format: "Step X must be finished before step Y can begin."
# X is at position 5 (0-indexed)
# Y is at position 36
line = "Step G must be finished before step S can begin."
prerequisite = line[5]
dependent = line[36]
```

**Input Assumptions**:
- Lines follow the exact format shown (Advent of Code guarantees this)
- No need to handle empty lines or malformed input for this script
- Each line contains exactly one dependency relationship

---

### Step 2: Build Dependency Graph
**Goal**: Create data structures to efficiently track dependencies and process order

**Data Structures Needed**:

1. **`dependencies`**: Dictionary mapping each step to its set of prerequisites
   - Type: `dict[str, set[str]]`
   - Example: `{'B': {'A', 'X', 'U'}, 'C': {'B', 'Q', 'X'}, ...}`

2. **`all_steps`**: Set of all unique steps that appear in the input
   - Type: `set[str]`
   - Ensures we process all steps, even those without dependencies

**Implementation**:
1. Initialize empty defaultdict or regular dict
2. Initialize empty set for all_steps
3. For each (prerequisite, dependent) tuple:
   - Add dependent to all_steps
   - Add prerequisite to all_steps
   - Add prerequisite to dependencies[dependent] (initialize with empty set if not exists)
4. **Critical**: Ensure ALL steps have an entry in dependencies dict:
   ```python
   for step in all_steps:
       if step not in dependencies:
           dependencies[step] = set()
   ```
   This ensures steps that only appear as prerequisites get an empty dependency set

**Time Complexity**: O(E) where E is number of dependency lines

---

### Step 3: Identify Initial Available Steps
**Goal**: Find steps with no prerequisites that can be started immediately

**Implementation**:
1. Iterate through all_steps
2. For each step, check if it has zero prerequisites
3. Collect all such steps in a list
4. Sort the list alphabetically

**Data Structure**: Sorted list of available steps

**Time Complexity**: O(V log V) for sorting, where V ≤ 26

---

### Step 4: Process Steps in Topological Order
**Goal**: Repeatedly select and process available steps in alphabetical order

**Algorithm** (Kahn's Algorithm variant with alphabetical selection):
```
result = []
available = [steps with no prerequisites, sorted]
# Deep copy: copy dict AND copy each set
remaining_dependencies = {k: v.copy() for k, v in dependencies.items()}

while available is not empty:
    # Select alphabetically first available step
    current_step = available[0]
    available.remove(current_step)

    # Add to result
    result.append(current_step)

    # Update dependencies for all remaining unprocessed steps
    for step in all_steps:
        if step not in result and current_step in remaining_dependencies[step]:
            remaining_dependencies[step].remove(current_step)

            # If step now has no dependencies, add to available
            if len(remaining_dependencies[step]) == 0:
                available.append(step)

    # Keep available list sorted
    available.sort()

return ''.join(result)
```

**Key Implementation Details**:

1. **Available Steps Management**:
   - Use a list that we keep sorted after each update
   - Alternative: Use a min-heap (heapq) for O(log V) insertion/removal
   - Given V ≤ 26, simple list is fine

2. **Dependency Tracking**:
   - Make a **deep copy** of dependencies to track remaining prerequisites
   - Must copy both the dict AND each set: `{k: v.copy() for k, v in dependencies.items()}`
   - As we complete steps, remove them from prerequisite sets
   - When a step's prerequisite set becomes empty, it becomes available
   - Only check unprocessed steps (not in result list) when updating dependencies

3. **Completion Check**:
   - Continue until available list is empty
   - All steps should be in result at the end

**Time Complexity**:
- O(V²) with list approach (V iterations × V sort operations)
- O(V² log V) worst case, but with V ≤ 26, this is negligible

---

### Step 5: Return Result
**Goal**: Format and return the final answer

**Implementation**:
1. Join the result list into a single string
2. Return or print the string

---

## Complete Code Structure

```python
def parse_input_file(filename):
    """Parse input file and return list of (prerequisite, dependent) tuples."""
    with open(filename) as f:
        return parse_input_text(f.read())

def parse_input_text(text):
    """Parse input text and return list of (prerequisite, dependent) tuples."""
    pass

def build_dependency_graph(dependencies_list):
    """
    Build graph from dependency list.

    Args:
        dependencies_list: List of (prerequisite, dependent) tuples

    Returns:
        tuple: (all_steps: set[str], dependencies: dict[str, set[str]])
            - all_steps: set of all unique step names
            - dependencies: dict mapping each step to set of its prerequisites
                            (includes empty sets for steps with no prerequisites)
    """
    pass

def topological_sort_alphabetical(all_steps, dependencies):
    """
    Perform topological sort with alphabetical tie-breaking.
    Returns: string of steps in execution order
    """
    pass

def solve(input_text=None, input_file='input.md'):
    """
    Main solver function.

    Args:
        input_text: Optional string containing input data. If None, reads from input_file
        input_file: Path to input file (default: 'input.md')

    Returns:
        str: The order in which steps should be completed
    """
    # Parse input
    if input_text is not None:
        deps_list = parse_input_text(input_text)
    else:
        deps_list = parse_input_file(input_file)

    # Build graph
    all_steps, dependencies = build_dependency_graph(deps_list)

    # Solve
    result = topological_sort_alphabetical(all_steps, dependencies)

    return result

if __name__ == '__main__':
    answer = solve()
    print(answer)
```

---

## Optimization Considerations

### Current Approach Efficiency:
- **Input Size**: 101 dependency lines, max 26 unique steps
- **Bottleneck**: None - problem is small enough that any reasonable approach works
- **Chosen Approach**: Simple list-based selection with sorting

### Alternative Optimizations (not necessary for this problem):
1. **Priority Queue/Heap**: Use `heapq` for O(log V) insertion instead of O(V log V) sorting
   - Overkill for V ≤ 26
2. **Sorted Set**: Use `sortedcontainers.SortedSet` for automatic ordering
   - Adds external dependency
3. **In-degree Array**: Track in-degrees instead of prerequisite sets
   - More memory efficient but same time complexity

**Conclusion**: Simple list-based approach is optimal for this problem size.

---

## Edge Cases to Handle

1. **Steps mentioned only as prerequisites**: Steps that are never dependent on others (must have empty dependency set)
2. **Linear chain**: Steps form A→B→C→...→Z
3. **Parallel steps**: Multiple steps with no dependencies between them (choose alphabetically first)
4. **Diamond dependencies**: A→B, A→C, B→D, C→D (D waits for both B and C)
5. **Duplicate dependencies**: Same dependency listed multiple times (use sets to automatically handle)
6. **Complex graphs with multiple branching paths**: Real input has 101 dependencies among ~26 steps

**Assumptions** (guaranteed by Advent of Code):
- Input contains a valid directed acyclic graph (no cycles)
- No need to detect or handle circular dependencies
- All steps will eventually be completable

---

## Testing Strategy Reference

The implementation should be tested against:
1. The provided example in problem.md (expected: CABDFE)
2. The actual input.md file
3. Custom edge cases (see test_plan.md)
