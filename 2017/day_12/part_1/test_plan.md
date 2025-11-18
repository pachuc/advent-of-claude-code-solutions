# Testing Plan: Digital Plumber

## Testing Strategy Overview
We need to verify that our solution correctly finds all programs connected to program 0 in a bidirectional graph. Testing will focus on correctness across different graph structures and edge cases.

## Test Cases

### Test 1: Example Input (Provided in Problem)
**Purpose**: Verify solution matches expected output from problem statement

**Input:**
```
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
```

**Expected Output:** `6`

**Rationale:**
- Programs 0, 2, 3, 4, 5, 6 are connected
- Program 1 only connects to itself (isolated)
- This tests basic connectivity and isolated nodes

**Verification Method:**
1. Create test file with this input
2. Run solution
3. Assert output equals 6

**Manual Trace:**
- Start at 0
- Visit 0 → neighbors: [2]
- Visit 2 → neighbors: [0, 3, 4] → add 3, 4
- Visit 3 → neighbors: [2, 4] → add 4 (already in queue)
- Visit 4 → neighbors: [2, 3, 6] → add 6
- Visit 6 → neighbors: [4, 5] → add 5
- Visit 5 → neighbors: [6]
- Total visited: {0, 2, 3, 4, 5, 6} = 6 programs ✓

### Test 2: Actual Problem Input
**Purpose**: Solve the actual problem

**Input:** The full 2000-line input from `input.md`

**Expected Output:** Unknown (to be determined)

**Verification Method:**
1. Run solution on actual input
2. Verify output is a reasonable number (between 1 and 2000)
3. Verify parsing correctness by checking graph[0] == [122, 874, 1940]
4. Verify bidirectional consistency (if 0→122, then 122 should list 0)
5. Re-run to ensure deterministic output (same result each time)
6. Optional: Implement alternative DFS solution and compare results

**Sanity Checks:**
- Output should be ≥ 1 (at minimum, program 0 itself)
- Output should be ≤ 2000 (can't exceed total programs)
- Parsing validation: `assert graph[0] == [122, 874, 1940]`
- Bidirectional validation: `assert 0 in graph[122] and 0 in graph[874] and 0 in graph[1940]`

### Test 3: Minimal Graph (Single Node)
**Purpose**: Test edge case of smallest possible graph

**Input:**
```
0 <-> 0
```

**Expected Output:** `1`

**Rationale:**
- Program 0 only connects to itself
- Should return 1 (just program 0)
- Tests self-loop handling

### Test 4: Fully Connected Graph
**Purpose**: Test case where all nodes are connected

**Input:**
```
0 <-> 1, 2
1 <-> 0, 2
2 <-> 0, 1
```

**Expected Output:** `3`

**Rationale:**
- All programs connect to each other
- Should return total count
- Tests complete connectivity

### Test 5: Linear Chain
**Purpose**: Test linear connectivity (worst case for BFS depth)

**Input:**
```
0 <-> 1
1 <-> 0, 2
2 <-> 1, 3
3 <-> 2, 4
4 <-> 3
```

**Expected Output:** `5`

**Rationale:**
- Programs form a chain: 0-1-2-3-4
- All should be reachable from 0
- Tests path traversal through intermediate nodes

### Test 6: Multiple Disconnected Components
**Purpose**: Verify only programs connected to 0 are counted

**Input:**
```
0 <-> 1
1 <-> 0
2 <-> 3
3 <-> 2
4 <-> 4
```

**Expected Output:** `2`

**Rationale:**
- Group 1: {0, 1} - connected to 0 ✓
- Group 2: {2, 3} - not connected to 0 ✗
- Group 3: {4} - not connected to 0 ✗
- Should only count group 1

### Test 7: Complex Graph with Cycles
**Purpose**: Test that cycles don't cause infinite loops or duplicate counting

**Input:**
```
0 <-> 1, 2
1 <-> 0, 2, 3
2 <-> 0, 1, 3
3 <-> 1, 2
```

**Expected Output:** `4`

**Rationale:**
- Graph has multiple cycles (0-1-2-0, 1-2-3-1, etc.)
- All 4 nodes are reachable from 0
- Tests visited tracking prevents re-counting

### Test 8: Whitespace Variations
**Purpose**: Ensure parsing handles different whitespace patterns

**Input:**
```
0<->1
1 <-> 0,2
2  <->  1, 3
3 <-> 2
```

**Expected Output:** `4`

**Rationale:**
- Tests parsing with minimal whitespace (`0<->1`)
- Tests parsing with no space after comma (`0,2`)
- Tests parsing with extra whitespace (`2  <->  1, 3`)
- All variations should parse correctly due to `strip()` calls

## Edge Cases to Verify

### Edge Case 1: Self-Loops
**Example:** `4 <-> 4, 1473` (from actual input)
**Expected Behavior:** Node 4 should be counted once, not twice
**Test:** Verify visited set prevents duplicate additions

### Edge Case 2: Bidirectional Consistency
**Example:** If `0 <-> 2`, then `2 <-> 0` should also appear
**Expected Behavior:** Both directions should be represented in input
**Test:** Implement bidirectional validation:
```python
# Verify all edges are bidirectional
for node, neighbors in graph.items():
    for neighbor in neighbors:
        if neighbor == node:  # Skip self-loops
            continue
        assert node in graph[neighbor], \
            f"Missing reverse edge: {neighbor} -> {node}"
```
This validation should be run on the actual input to confirm the assumption

### Edge Case 3: Input Parsing with Variable Whitespace
**Example:** `0<->2` vs `0 <-> 2` vs `0  <->  2`
**Expected Behavior:** All should parse correctly
**Test:** See Test 8 above - dedicated test case for whitespace variations

### Edge Case 4: Programs with Many Connections
**Example:** Some programs may connect to 10+ others
**Expected Behavior:** All connections should be parsed and traversed
**Test:** Verify programs with many connections are fully processed

## Verification Methods

### Method 1: Manual Tracing (Small Inputs)
For small test cases (< 10 nodes):
1. Draw the graph on paper
2. Manually perform BFS from node 0
3. Compare manual result with program output

### Method 2: Output Validation (All Inputs)
For all test cases:
1. Verify output is a single integer
2. Verify output is in valid range [1, total_nodes]
3. Verify output is deterministic (same result on multiple runs)

### Method 3: Parsing Validation (Actual Input)
For the actual input:
1. Print first few parsed adjacency list entries
2. Manually compare with input file
3. Verify bidirectional relationships

**Example Validation:**
```python
# From input: 0 <-> 122, 874, 1940
assert graph[0] == [122, 874, 1940]
# Check reverse connections exist
assert 0 in graph[122]
assert 0 in graph[874]
assert 0 in graph[1940]
```

### Method 4: Reachability Spot-Check (Actual Input)
For the actual input:
1. Pick a program that should be reachable (e.g., 122, direct neighbor of 0)
2. Verify it's in the visited set
3. Pick a program multiple hops away
4. Trace the path manually and verify it's included

## Test Execution Plan

### Phase 1: Development Testing
1. ✓ Test with example input first
2. ✓ Verify output matches expected (6)
3. ✓ If fails, debug with print statements showing BFS traversal

### Phase 2: Edge Case Testing
1. Run tests 3-8 (minimal, fully connected, linear, disconnected, cycles, whitespace)
2. Verify each produces expected output
3. If any fail, examine the specific graph structure

### Phase 3: Actual Input Testing
1. Run on actual input
2. Verify output is in range [1, 2000]
3. Perform parsing validation: `assert graph[0] == [122, 874, 1940]`
4. Perform bidirectional validation (see Edge Case 2 code snippet)
5. Perform reachability spot-check (verify 122, 874, 1940 are in visited set)
6. Re-run multiple times to ensure determinism

### Phase 4: Performance Testing
1. Time the execution on actual input using Python's `time` module or shell `time` command:
   ```python
   import time
   start = time.time()
   # run solution
   elapsed = time.time() - start
   print(f"Execution time: {elapsed:.3f} seconds")
   ```
2. Verify runs in < 1 second (should be milliseconds)
3. If slow, profile to identify bottleneck

## Success Criteria

### Correctness
- [ ] Example input produces output of 6
- [ ] All edge case tests produce expected outputs
- [ ] Actual input produces a valid integer in range [1, 2000]
- [ ] Bidirectional validation passes
- [ ] Multiple runs produce identical results

### Code Quality
- [ ] Code is readable and well-structured
- [ ] No obvious bugs or logical errors
- [ ] Handles all input format variations

### Performance
- [ ] Completes in under 1 second for actual input
- [ ] No memory issues or crashes

## Debugging Checklist (If Tests Fail)

### If Output Too Low
- [ ] Check if parsing is missing connections (comma splitting issue?)
- [ ] Check if BFS is terminating early
- [ ] Print visited set to see which programs were reached
- [ ] Verify queue is being populated correctly

### If Output Too High
- [ ] Check if nodes are being counted multiple times
- [ ] Verify visited set is preventing re-addition
- [ ] Check if parsing is creating duplicate entries

### If Output is Wrong by Small Amount
- [ ] Off-by-one error (counting starting node twice?)
- [ ] Missing or extra self-loop handling
- [ ] Bidirectional edge counted as two separate edges?

### If Program Crashes
- [ ] Check input file format
- [ ] Verify all program IDs are integers
- [ ] Check for empty lines in input
- [ ] Verify file path is correct

## Test Data Preparation

### Create Test Files
1. `test_example.txt` - The example from problem statement
2. `test_minimal.txt` - Single node test
3. `test_chain.txt` - Linear chain test
4. `test_disconnected.txt` - Multiple components test
5. `test_cycles.txt` - Graph with cycles test

### Test Runner Script (Recommended)
Creating a simple test runner is recommended to automate testing:
```python
test_cases = [
    ("test_example.txt", 6),
    ("test_minimal.txt", 1),
    ("test_chain.txt", 5),
    ("test_disconnected.txt", 2),
    ("test_cycles.txt", 4),
    ("test_whitespace.txt", 4),
]

for input_file, expected in test_cases:
    result = run_solution(input_file)
    assert result == expected, f"Failed on {input_file}: got {result}, expected {expected}"
    print(f"✓ {input_file} passed")
```

This makes it easy to verify all test cases quickly and systematically.
