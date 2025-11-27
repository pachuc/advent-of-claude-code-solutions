# Testing Plan: A Regular Map - Part 2

## Testing Strategy Overview

The testing approach focuses on:
1. Verifying the modified counting logic works correctly
2. Ensuring graph construction remains consistent with Part 1
3. Validating threshold boundary conditions
4. Testing with the actual puzzle input

Since Part 2 reuses Part 1's graph construction, we don't need to extensively test the parser and graph builder again. Instead, we focus on the new counting logic.

## Test Categories

### 1. Threshold Counting Logic Tests

#### Test 1.1: Small Graph with Known Distances
**Objective**: Verify counting logic with a manually traceable example

**Test Case**: `^EEENNN$`
- Creates a simple path: start -> E -> E -> E -> N -> N -> N
- Room distances:
  - (0,0): 0 doors
  - (1,0): 1 door
  - (2,0): 2 doors
  - (3,0): 3 doors
  - (3,-1): 4 doors
  - (3,-2): 5 doors
  - (3,-3): 6 doors

**Expected Results**:
- Threshold = 0: count = 7 (all rooms)
- Threshold = 1: count = 6 (exclude start)
- Threshold = 3: count = 4 (rooms at 3, 4, 5, 6)
- Threshold = 6: count = 1 (only furthest room)
- Threshold = 7: count = 0 (no rooms this far)

**Implementation**:
```python
def test_threshold_counting():
    regex = '^EEENNN$'
    result_0 = solve(regex, threshold=0)
    result_1 = solve(regex, threshold=1)
    result_3 = solve(regex, threshold=3)
    result_6 = solve(regex, threshold=6)
    result_7 = solve(regex, threshold=7)

    assert result_0 == 7, f"Expected 7, got {result_0}"
    assert result_1 == 6, f"Expected 6, got {result_1}"
    assert result_3 == 4, f"Expected 4, got {result_3}"
    assert result_6 == 1, f"Expected 1, got {result_6}"
    assert result_7 == 0, f"Expected 0, got {result_7}"
```

**Note**: The `solve()` function accepts an optional `threshold` parameter (defaults to 1000) to support testing with different thresholds.

#### Test 1.2: Graph with Branches
**Objective**: Verify counting with multiple paths to same room

**Test Case**: `^N(E|W)N$`
- Creates a diamond pattern where multiple paths converge
- Tests that each room is only counted once

**Expected Behavior**:
- Each room counted exactly once, regardless of number of paths to it
- BFS ensures we find shortest path to each room

**Validation Method**:
- Manually trace the graph structure
- Verify room count matches expected unique positions
- Check that distances represent shortest paths

#### Test 1.3: Empty Branch Handling
**Objective**: Ensure empty branches don't affect counting

**Test Case**: `^NNNN(EE|)NNNN$`
- One path goes NNNNNNNN (8 north)
- Other path goes NNNNEENNNN (4N, 2E, 4N)

**Expected Behavior**:
- All rooms reachable via shortest path
- Empty branch option correctly processed
- No duplicate counting

### 2. Boundary Condition Tests

#### Test 2.1: Threshold at Exactly 1000
**Objective**: Verify >= comparison includes rooms at exactly 1000 doors

**Approach**:
- Use actual puzzle input (we know max distance is 3672)
- Count with threshold 1000: `solve(input_text, threshold=1000)` (call it C1000)
- Count with threshold 1001: `solve(input_text, threshold=1001)` (call it C1001)
- Verify C1000 >= C1001 (could be equal if no rooms at exactly 1000)

#### Test 2.2: Threshold Beyond Maximum Distance
**Objective**: Verify count is 0 when threshold exceeds all distances

**Test Case**: Using actual input with threshold 4000 (> 3672)
```python
result = solve(input_text, threshold=4000)
assert result == 0, f"Expected 0 for threshold beyond max, got {result}"
```

**Expected Result**: count = 0

#### Test 2.3: Threshold at 0
**Objective**: Verify all rooms counted when threshold is 0

**Test**:
```python
# Build graph to get total room count
regex = input_text.strip()[1:-1]
doors = parse_regex_and_build_graph(regex)
graph = build_adjacency_graph(doors)
total_rooms = len(graph)

# Count with threshold 0
result = solve(input_text, threshold=0)
assert result == total_rooms, f"Expected {total_rooms}, got {result}"
```

**Expected Result**: count = total number of unique rooms in the graph

### 3. Consistency Tests with Part 1

#### Test 3.1: Graph Construction Consistency
**Objective**: Verify Part 2 builds identical graph to Part 1

**Method**:
1. Run Part 1 solution on puzzle input, capture doors set and graph
2. Run Part 2 solution on puzzle input, capture doors set and graph
3. Compare:
   - Number of doors (should be identical)
   - Number of rooms (should be identical)
   - Graph structure (should be identical)

**Implementation**:
```python
def test_graph_consistency():
    # Read input
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Extract regex
    regex = input_text.strip()[1:-1]

    # Build graph (same method in both parts)
    doors = parse_regex_and_build_graph(regex)
    graph = build_adjacency_graph(doors)

    # Verify graph properties
    total_rooms = len(graph)
    total_doors = len(doors)

    print(f"Total rooms: {total_rooms}")
    print(f"Total doors: {total_doors}")

    # These should be large numbers for the puzzle input
    assert total_rooms > 1000, "Graph should have many rooms"
    assert total_doors > 1000, "Graph should have many doors"
```

#### Test 3.2: Maximum Distance Verification
**Objective**: Verify Part 2's BFS finds the same maximum distance as Part 1

**Method**:
1. Modify count_distant_rooms to also track maximum distance seen
2. Verify it equals 3672 (Part 1's answer)
3. This confirms BFS traversal is complete and correct

**Implementation**:
```python
def count_and_find_max(graph, start=(0, 0), threshold=1000):
    queue = deque([(start, 0)])
    visited = {start}
    count = 0
    max_dist = 0

    while queue:
        pos, dist = queue.popleft()
        max_dist = max(max_dist, dist)

        if dist >= threshold:
            count += 1

        for neighbor in graph[pos]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return count, max_dist

# Test
count, max_dist = count_and_find_max(graph, (0, 0), 1000)
assert max_dist == 3672, f"Expected max distance 3672, got {max_dist}"
```

### 4. Actual Puzzle Input Test

#### Test 4.1: Run on Actual Input
**Objective**: Solve the actual puzzle and verify answer is reasonable

**Execution**:
```python
def test_actual_puzzle():
    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)

    # Sanity checks
    assert result > 0, "Should have at least one room beyond 1000 doors"
    assert result < 10000, "Shouldn't have an unreasonably large count"

    # More specific check: Part 1 found max distance 3672
    # So we definitely have rooms at 1000+ doors
    # Count should be substantial but less than total rooms

    print(f"Rooms requiring at least 1000 doors: {result}")

    return result
```

**Expected Characteristics of Answer**:
- Greater than 0 (since max distance is 3672 > 1000)
- Less than total number of rooms
- Should be a reasonable proportion of total rooms
- Exact value will be the answer, but we can verify it's in a sensible range

#### Test 4.2: Relationship Between Different Thresholds
**Objective**: Verify monotonic decrease as threshold increases

**Test**:
```python
def test_threshold_monotonicity():
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Test multiple thresholds using solve() function
    count_500 = solve(input_text, threshold=500)
    count_1000 = solve(input_text, threshold=1000)
    count_2000 = solve(input_text, threshold=2000)
    count_3000 = solve(input_text, threshold=3000)

    # Verify monotonic decrease
    assert count_500 >= count_1000, "Higher threshold should not increase count"
    assert count_1000 >= count_2000, "Higher threshold should not increase count"
    assert count_2000 >= count_3000, "Higher threshold should not increase count"

    print(f"Distance >= 500:  {count_500}")
    print(f"Distance >= 1000: {count_1000}")
    print(f"Distance >= 2000: {count_2000}")
    print(f"Distance >= 3000: {count_3000}")
```

## Testing Execution Order

1. **First**: Test 1.1 (Simple threshold counting) - validates core logic
2. **Second**: Test 3.1 (Graph consistency) - ensures graph is correct
3. **Third**: Test 3.2 (Max distance verification) - confirms BFS is correct
4. **Fourth**: Test 2.2 and 2.3 (Boundary conditions) - edge case validation
5. **Fifth**: Test 4.2 (Threshold monotonicity) - relationship validation
6. **Finally**: Test 4.1 (Actual puzzle) - get the answer

## Success Criteria

The solution is correct if:
1. ✓ Simple test cases produce expected counts
2. ✓ Graph construction matches Part 1 (same doors, same rooms)
3. ✓ BFS finds maximum distance of 3672 (matches Part 1)
4. ✓ Threshold boundaries work correctly (>= comparison)
5. ✓ Monotonic decrease as threshold increases
6. ✓ Actual puzzle answer is in reasonable range (0 < answer < total_rooms)

## Manual Verification Approach

If automated tests are unclear, manually verify by:
1. Print total number of rooms in graph
2. Print distribution of distances (histogram):
   - How many rooms at distance 0? (should be 1 - the start)
   - How many rooms at distance 1-100?
   - How many rooms at distance 100-500?
   - How many rooms at distance 500-1000?
   - How many rooms at distance 1000-2000?
   - How many rooms at distance 2000-3672?
3. Sum rooms at 1000+ and verify it matches our answer

## Debugging Strategy

If answer seems incorrect:
1. Add logging to count_distant_rooms to track:
   - Total rooms visited
   - Distribution of distances
   - Rooms at exactly threshold
2. Verify BFS is traversing entire graph (visited.size == total rooms)
3. Check threshold comparison (should be `>=`, not `>`)
4. Ensure starting position (0,0) is not counted if distance is 0
