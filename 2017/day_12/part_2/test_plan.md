# Test Plan: Digital Plumber - Part 2

## Testing Objectives
1. Verify correct counting of all connected components
2. Ensure all nodes are assigned to exactly one group
3. Validate performance on the actual input (2000 programs)
4. Confirm edge cases are handled properly

## Test Cases

### Test Case 1: Example from Problem Statement
**Purpose**: Verify basic correctness with known output

**Input**:
```
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
```

**Expected Output**: `2`

**Explanation**:
- Group 1: {0, 2, 3, 4, 5, 6} - size 6
- Group 2: {1} - size 1
- Total groups: 2

**Validation Steps**:
1. Create a file `test_example.md` with the example input above
2. Temporarily modify `main()` to read from `test_example.md` instead of `input.md`:
   ```python
   with open('test_example.md', 'r') as f:  # Change filename here
   ```
3. Run the solution: `python solution.py`
4. Verify output is exactly `2`
5. Restore `main()` to read from `input.md` before continuing to other tests

---

### Test Case 2: Multiple Small Isolated Groups
**Purpose**: Test detection of many small components

**Input**:
```
0 <-> 0
1 <-> 1
2 <-> 2
3 <-> 3
```

**Expected Output**: `4`

**Explanation**: 4 isolated nodes = 4 groups of size 1 each

**Validation**: Each node only connects to itself, so each is its own group

---

### Test Case 3: Single Large Group
**Purpose**: Ensure single component is counted correctly

**Input**:
```
0 <-> 1
1 <-> 0, 2
2 <-> 1, 3
3 <-> 2
```

**Expected Output**: `1`

**Explanation**: All nodes are connected in one chain

**Validation**: BFS from any node should reach all others

---

### Test Case 4: Three Distinct Groups
**Purpose**: Test intermediate complexity

**Input**:
```
0 <-> 1
1 <-> 0
2 <-> 3
3 <-> 2
4 <-> 5, 6
5 <-> 4
6 <-> 4
```

**Expected Output**: `3`

**Explanation**:
- Group 1: {0, 1}
- Group 2: {2, 3}
- Group 3: {4, 5, 6}

---

### Test Case 5: Actual Puzzle Input
**Purpose**: Solve the actual problem

**Input**: Use the provided `input.md` file (2000 lines)

**Expected Output**: Unknown (to be determined)

**Validation Steps**:
1. Ensure `main()` reads from `input.md`
2. Run the solution: `python solution.py`
3. Record the output
4. Verify the answer is reasonable (should be much less than 2000)
5. Confirm it's greater than 1 (since Part 1 found only 239 programs in group 0, there must be other groups)
6. Check that the execution completes quickly (should be < 1 second)

**Sanity Checks**:
- If group count is 1: All 2000 programs are connected (unlikely given Part 1 result)
- If group count is 2000: Every program is isolated (contradicts the input showing connections)
- Reasonable range: Should be much less than 2000, likely between 2 and several hundred groups

---

## Verification Strategy

### 1. Manual Verification of Example
- Trace through the algorithm by hand for the example
- Ensure we visit nodes in the expected order
- Confirm visited_global set grows correctly

### 2. Cross-Reference with Part 1
- Part 1 answer: 239 programs in group containing 0
- Part 2 should identify that same group as one component
- The remaining (2000 - 239 = 1761) programs must be in other groups

### 3. Conservation Check

**Mathematical Foundation**:
In a partition of a set into disjoint subsets (connected components):
- Every node belongs to exactly one component
- Therefore: Σ(size of each component) = Total nodes
- For our input: Σ(group sizes) must equal 2000
- If this fails, we either:
  - Missed some nodes (sum < 2000)
  - Counted some nodes twice (sum > 2000)

For the actual input, verify:
```
Sum of all group sizes = Total number of nodes (2000)
```

**Optional Debugging Code** (add to a separate debug script, NOT the main solution):

Create a file `debug_solution.py` with the following:
```python
from solution import parse_input, find_connected_group

def count_all_groups_with_sizes(graph):
    """Debug version that prints detailed group information."""
    visited_global = set()
    group_sizes = []

    for node in graph:
        if node not in visited_global:
            group_nodes = find_connected_group(graph, node)
            visited_global.update(group_nodes)
            group_sizes.append(len(group_nodes))

    print(f"Group sizes: {sorted(group_sizes, reverse=True)}")
    print(f"Total nodes covered: {sum(group_sizes)}")
    print(f"Total nodes in graph: {len(graph)}")
    print(f"One group has size 239: {239 in group_sizes}")

    return len(group_sizes)

# Read and test
with open('input.md', 'r') as f:
    lines = f.readlines()
graph = parse_input(lines)
total = count_all_groups_with_sizes(graph)
print(f"\nTotal groups: {total}")
```

This helps verify:
- One group should have size 239 (from Part 1)
- All groups together should cover all 2000 nodes
- No node is counted twice

**When to use this**: Run after getting your answer to validate correctness, not as part of the main solution.

---

## Edge Cases to Verify

### Edge Case 1: Self-Loops
**Input**: `4 <-> 4, 1473` (from actual input)
- Verify this doesn't cause infinite loops
- Confirm node 4 is in the same group as node 1473

### Edge Case 2: Bidirectional Connections
**Input**: If `2 <-> 0, 3, 4` and `0 <-> 2`, both connections exist
- Verify we don't double-count edges
- The set-based visited tracking should prevent revisiting

### Edge Case 3: Empty Lines
- Parser should skip empty lines gracefully (already tested in Part 1)

---

## Performance Validation

### Time Complexity Check
- **Expected**: O(V + E) where V ≈ 2000, E ≈ 6000 (estimated from input)
- **Measurement**: Time the execution
- **Acceptance Criteria**: Should complete in under 1 second

### Space Complexity Check
- **Expected**: O(V) for visited set and graph storage
- **Measurement**: Should use minimal memory (< 1 MB)

---

## How to Run Tests

### Option 1: Manual Testing (Recommended for simplicity)
1. Create test input files as needed (e.g., `test_example.md`, `test_simple.md`)
2. Temporarily modify the `main()` function to read from the test file:
   ```python
   with open('test_example.md', 'r') as f:  # Change filename for each test
       lines = f.readlines()
   ```
3. Run: `python solution.py`
4. Verify output matches expected result
5. Change filename back to `input.md` for the actual puzzle

### Option 2: Parameterized Main (Better for multiple tests)
Modify `main()` to accept a filename parameter:
```python
def main(filename='input.md'):
    with open(filename, 'r') as f:
        lines = f.readlines()
    # ... rest of code
```

Then test with: `python -c "from solution import main; main('test_example.md')"`

### Option 3: Automated Testing (Most thorough)
Create a separate `test_solution.py` file:
```python
from solution import parse_input, count_all_groups

def test_example():
    input_text = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
    lines = input_text.split('\n')
    graph = parse_input(lines)
    result = count_all_groups(graph)
    assert result == 2, f"Expected 2, got {result}"
    print("✓ Example test passed")

# Add more test functions...
if __name__ == "__main__":
    test_example()
    # Call other tests...
```

## Test Execution Order

1. **Start with simple cases** (Test Cases 2, 3, 4) to verify basic logic
2. **Run example** (Test Case 1) to confirm expected behavior
3. **Run actual input** (Test Case 5) to get the solution
4. **Optional**: Run conservation check (using `debug_solution.py`) to validate correctness

---

## Success Criteria

- [ ] All small test cases pass with correct outputs
- [ ] Example test case outputs exactly `2`
- [ ] Actual input produces a reasonable answer (2 ≤ answer ≤ 100 estimated)
- [ ] Conservation check: sum of group sizes = 2000
- [ ] One group has size 239 (matching Part 1 answer)
- [ ] Execution time < 1 second
- [ ] No crashes or infinite loops

---

## Debugging Strategies

If tests fail:

### 1. Wrong Count
**Symptoms**: Output doesn't match expected value

**Debug steps**:
- Add print statements to show group_sizes:
  ```python
  print(f"Group sizes: {sorted(group_sizes, reverse=True)}")
  ```
- Verify no groups are being merged incorrectly
- Check: Is `visited_global` being updated correctly?
- Confirm: Are we starting BFS from unvisited nodes only?

### 2. Infinite Loop
**Symptoms**: Program hangs and never completes

**Debug steps**:
- Add a max iterations counter to detect loops:
  ```python
  max_groups = len(graph)  # Can't have more groups than nodes
  if group_count > max_groups:
      raise Exception("Infinite loop detected")
  ```
- Print the current node being processed:
  ```python
  for node in graph:
      print(f"Processing node {node}, groups so far: {group_count}")
  ```
- Verify BFS marks nodes as visited BEFORE adding neighbors to queue
- Check: Does the visited set contain the current node before exploring neighbors?

### 3. Missing Nodes
**Symptoms**: Sum of group sizes < 2000

**Debug steps**:
- Print total nodes parsed:
  ```python
  print(f"Total nodes in graph: {len(graph)}")
  ```
- Check if any node IDs are referenced in connections but not defined as keys
- Verify parser handles all lines correctly (no skipped lines except empty ones)

### 4. Double Counting
**Symptoms**: Sum of group sizes > 2000

**Debug steps**:
- Print `visited_global` after each group discovery:
  ```python
  print(f"After group {group_count}, visited: {len(visited_global)} nodes")
  ```
- Verify no overlap between groups
- Check: Is `visited_global.update(group_nodes)` called BEFORE incrementing group_count?
- Ensure we skip nodes already in `visited_global`

### 5. Performance Issues
**Symptoms**: Takes longer than 1 second

**Debug steps**:
- Profile which part is slow (parsing vs. BFS)
- Check for redundant operations in loops
- Verify we're using sets (O(1) lookup) not lists (O(n) lookup) for visited tracking
