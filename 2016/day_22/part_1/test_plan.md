# Testing Plan: Grid Computing Viable Pairs Count

## Testing Strategy

Since this is a script to solve a specific problem (not production code), our testing should focus on:
1. Correctness of the algorithm logic
2. Proper handling of the actual input data
3. Key edge cases that could affect the result
4. Verification against expected behavior

We do NOT need extensive unit tests, mocks, or comprehensive edge case coverage beyond what's necessary to ensure correctness.

## Test Categories

### 1. Unit Testing: Parsing Function

#### Test 1.1: Basic Parsing
**Purpose**: Verify parsing extracts correct values

**Test Data**:
```
root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0     89T   65T    24T   73%
/dev/grid/node-x0-y1     92T   64T    28T   69%
/dev/grid/node-x1-y0     90T    0T    90T    0%
```

**Expected Result**:
```python
[(65, 24), (64, 28), (0, 90)]
```

**Verification**:
- Check list length is 3
- Check first tuple is (65, 24)
- Check last tuple is (0, 90)

#### Test 1.2: Large Numbers
**Purpose**: Verify parsing handles large capacity nodes

**Test Data**:
```
root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0    501T  495T     6T   98%
```

**Expected Result**:
```python
[(495, 6)]
```

**Verification**:
- Check tuple is (495, 6)
- Ensure no integer overflow issues

#### Test 1.3: Actual Input File
**Purpose**: Verify parsing works on real input

**Test Data**: Use actual `input.md` file

**Expected Behavior**:
- Should return list of ~1,015 tuples
- No exceptions or errors
- All tuples should have positive integers (or 0 for used)

**Verification**:
```python
nodes = parse_input(open('input.md').read())
assert len(nodes) == 1015  # or actual count
assert all(isinstance(u, int) and isinstance(a, int) for u, a in nodes)
assert all(u >= 0 and a >= 0 for u, a in nodes)
```

### 2. Unit Testing: Viable Pairs Counting

#### Test 2.1: Simple Case - All Pairs Viable
**Purpose**: Verify basic counting logic

**Test Data**:
```python
nodes = [(10, 50), (20, 60), (30, 70)]
```
- Node 0: used=10, avail=50
- Node 1: used=20, avail=60
- Node 2: used=30, avail=70

**Analysis**:
- Node 0→Node 0: SKIP (same node)
- Node 0→Node 1: used=10 ≤ avail=60 ✓ → Count
- Node 0→Node 2: used=10 ≤ avail=70 ✓ → Count
- Node 1→Node 0: used=20 ≤ avail=50 ✓ → Count
- Node 1→Node 1: SKIP (same node)
- Node 1→Node 2: used=20 ≤ avail=70 ✓ → Count
- Node 2→Node 0: used=30 ≤ avail=50 ✓ → Count
- Node 2→Node 1: used=30 ≤ avail=60 ✓ → Count
- Node 2→Node 2: SKIP (same node)

**Expected Result**: 6 pairs

#### Test 2.2: Empty Node (used = 0)
**Purpose**: Verify empty nodes are excluded as source

**Test Data**:
```python
nodes = [(0, 50), (20, 60), (30, 70)]
```

**Analysis**:
- Node 0: used=0, SKIP (empty nodes don't count) → 0 pairs
- Node 1: used=20, can fit in node 0 (avail=50) and node 2 (avail=70) → 2 pairs
- Node 2: used=30, can fit in node 0 (avail=50) and node 2 (avail=70) → 2 pairs

**Expected Result**: 4 pairs

#### Test 2.3: No Available Space
**Purpose**: Verify pairs where data doesn't fit are excluded

**Test Data**:
```python
nodes = [(50, 10), (60, 20), (70, 30)]
```

**Analysis**:
- Node 0: used=50, too large for all other nodes → 0 pairs
- Node 1: used=60, too large for all other nodes → 0 pairs
- Node 2: used=70, too large for all other nodes → 0 pairs

**Expected Result**: 0 pairs

#### Test 2.4: Exact Fit
**Purpose**: Verify edge case where used exactly equals available

**Test Data**:
```python
nodes = [(50, 50), (50, 60)]
```
- Node 0: used=50, avail=50
- Node 1: used=50, avail=60

**Analysis**:
- Node 0→Node 0: SKIP (same node)
- Node 0→Node 1: used=50 ≤ avail=60 ✓ → Count
- Node 1→Node 0: used=50 ≤ avail=50 ✓ → Count (exact fit)
- Node 1→Node 1: SKIP (same node)

**Expected Result**: 2 pairs

**Note**: The condition is `used_a <= avail_b`, so exact fit counts as viable. Each node cannot pair with itself.

#### Test 2.5: Single Node
**Purpose**: Edge case with only one node

**Test Data**:
```python
nodes = [(50, 50)]
```

**Analysis**:
- Node 0: can't pair with itself → 0 pairs

**Expected Result**: 0 pairs

#### Test 2.6: Two Nodes
**Purpose**: Minimal viable case

**Test Data**:
```python
nodes = [(10, 50), (20, 60)]
```

**Analysis**:
- Node 0: used=10, fits in node 1 (avail=60) → 1 pair
- Node 1: used=20, fits in node 0 (avail=50) → 1 pair

**Expected Result**: 2 pairs

### 3. Integration Testing

#### Test 3.1: End-to-End with Small Example
**Purpose**: Verify complete flow from input to output

**Test Input File** (create `test_input.txt`):
```
root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0     10T    8T     2T   80%
/dev/grid/node-x0-y1     10T    5T     5T   50%
/dev/grid/node-x1-y0     10T    0T    10T    0%
```

**Manual Calculation**:
- Node 0 (8, 2): used=8, fits in node 1 (avail=5)? NO, fits in node 2 (avail=10)? YES → 1 pair
- Node 1 (5, 5): used=5, fits in node 0 (avail=2)? NO, fits in node 2 (avail=10)? YES → 1 pair
- Node 2 (0, 10): SKIP (empty) → 0 pairs

**Expected Output**: 2

**Verification**:
- Run script with this test input
- Compare output to expected value

#### Test 3.2: End-to-End with Actual Input
**Purpose**: Verify script solves the actual problem

**Test Input**: Use `input.md`

**Verification Method**:
Since we don't know the expected answer beforehand:
1. Run the script and record the output
2. Manually verify the logic is correct using spot checks
3. Verify the number is reasonable (should be > 0 and ≤ n×(n-1))
4. For ~1,015 nodes, maximum possible pairs is ~1,029,210

**Sanity Checks**:
```python
result = <actual output>
n = 1015  # approximate node count
assert 0 < result <= n * (n - 1)  # Must be in valid range
```

### 4. Algorithm Correctness Verification

#### Test 4.1: Order Matters Verification
**Purpose**: Confirm (A,B) and (B,A) are counted separately

**Test Data**:
```python
nodes = [(10, 20), (5, 100)]
```

**Analysis**:
- (Node 0 → Node 1): used=10, avail=100, 10 ≤ 100 ✓ → Count
- (Node 0 → Node 0): Skip (same node)
- (Node 1 → Node 0): used=5, avail=20, 5 ≤ 20 ✓ → Count
- (Node 1 → Node 1): Skip (same node)

**Expected Result**: 2 pairs

**Confirms**: Both directions are counted when viable

#### Test 4.2: Non-Adjacent Nodes
**Purpose**: Confirm adjacency doesn't matter (problem says ignore it)

**Test Data**:
```python
nodes = [(10, 50), (20, 60), (30, 70)]
```

**Expected Behavior**:
All pairs should be considered regardless of position in list

**Expected Result**: Should count all viable pairs without regard to index distance

### 5. Edge Case Testing

#### Test 5.1: All Empty Nodes
**Purpose**: Extreme edge case

**Test Data**:
```python
nodes = [(0, 100), (0, 100), (0, 100)]
```

**Expected Result**: 0 pairs (no non-empty source nodes)

#### Test 5.2: All Full Nodes (no available space)
**Purpose**: Verify no false positives

**Test Data**:
```python
nodes = [(100, 0), (100, 0), (100, 0)]
```

**Expected Result**: 0 pairs (no available space anywhere)

#### Test 5.3: One Large Node
**Purpose**: Simulate the 501T node in actual input

**Test Data**:
```python
nodes = [(495, 6), (65, 24), (70, 20)]
```

**Analysis**:
- Node 0 (495, 6): used=495, can't fit anywhere → 0 pairs
- Node 1 (65, 24): fits in node 2 (avail=20)? NO, fits in node 0 (avail=6)? NO → 0 pairs
- Node 2 (70, 20): fits in node 0 (avail=6)? NO, fits in node 1 (avail=24)? NO → 0 pairs

**Expected Result**: 0 pairs

**Verification**: Large nodes with little available space don't cause issues

## Testing Implementation Approach

### Recommended Test Structure

Create a `test_solution.py` file:

```python
from solution import parse_input, count_viable_pairs

def test_parsing():
    # Test 1.1, 1.2, 1.3
    pass

def test_counting():
    # Test 2.1 through 2.6
    pass

def test_edge_cases():
    # Test 5.1, 5.2, 5.3
    pass

def test_actual_input():
    # Test 3.2
    pass

if __name__ == "__main__":
    test_parsing()
    test_counting()
    test_edge_cases()
    test_actual_input()
    print("All tests passed!")
```

### Manual Verification Steps

1. **Run on small examples**: Create 2-3 small test inputs and manually calculate expected output
2. **Spot check actual input**: Manually verify a few nodes from the actual input
3. **Sanity check result**: Ensure output is in reasonable range for ~1,015 nodes
4. **Performance check**: Verify script completes in < 1 second

### Acceptance Criteria

The solution is correct if:
1. All unit tests pass
2. Integration test with actual input produces a result
3. Result is in valid range: 0 < result < n × (n-1)
4. Spot checks of logic are correct
5. Script runs without errors in reasonable time (< 1 second)

## Test Execution Order

1. Run unit tests for parsing first (ensure data is read correctly)
2. Run unit tests for counting with known examples
3. Run edge case tests
4. Run integration test with actual input
5. Perform manual sanity checks on the result

## Expected Issues and Validation

### Common Pitfalls to Check

1. **Off-by-one errors**: Ensure we're not double-counting or missing pairs
2. **Self-pairing**: Ensure nodes don't pair with themselves
3. **Empty node handling**: Ensure used=0 nodes are skipped as sources
4. **Comparison operator**: Ensure we use `<=` not `<` (exact fit is valid)
5. **Order independence**: Ensure (A,B) and (B,A) are both counted when valid

### Final Validation

After getting a result from actual input:
- Number should be reasonable (likely in thousands range)
- Re-run to ensure deterministic output
- Verify no runtime errors or warnings
