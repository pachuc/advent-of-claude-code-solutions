# Testing Plan: Four-Dimensional Constellation Grouping

## Testing Strategy

This plan covers verification of correctness through:
1. Provided test cases
2. Edge cases
3. Algorithm correctness verification
4. Performance validation

## Test Categories

### 1. Provided Test Cases (Critical)

These are given in the problem statement and MUST pass.

#### Test Case 1: Two Separate Constellations
```
Input:
0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0

Expected Output: 2
```

**What to verify**:
- First 6 points form one constellation (all within reach through chains)
- Points at x=9 and x=12 form second constellation (distance=3 from each other)
- Distance from (0,0,0,6) to (9,0,0,0) is 9+6=15 > 3 (correctly separated)

**Testing approach**:
1. Run algorithm on this input
2. Assert output == 2
3. Manually trace unions to verify constellation membership

#### Test Case 2: Four Constellations
```
Input:
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0

Expected Output: 4
```

**What to verify**:
- Correctly identifies 4 distinct groups
- Negative coordinates handled properly
- Points with mixed positive/negative values processed correctly

**Testing approach**:
1. Run algorithm on this input
2. Assert output == 4
3. Optionally: manually identify which points belong to which constellation

#### Test Case 3: Three Constellations
```
Input:
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2

Expected Output: 3
```

**Testing approach**:
1. Run algorithm
2. Assert output == 3

#### Test Case 4: Eight Constellations
```
Input:
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2

Expected Output: 8
```

**What to verify**:
- Each point is its own constellation (or almost all are)
- Algorithm correctly identifies when points are too far apart

**Testing approach**:
1. Run algorithm
2. Assert output == 8

### 2. Edge Cases

#### Test Case 5: Single Point
```
Input:
0,0,0,0

Expected Output: 1
```
**Verifies**: Handles minimum input size

#### Test Case 6: Two Points - Connected
```
Input:
0,0,0,0
3,0,0,0

Expected Output: 1
```
**Verifies**:
- Distance = 3 (boundary case)
- Correctly identifies as connected

#### Test Case 7: Two Points - Disconnected
```
Input:
0,0,0,0
4,0,0,0

Expected Output: 2
```
**Verifies**:
- Distance = 4 (just beyond threshold)
- Correctly identifies as separate

#### Test Case 8: All Points Identical
```
Input:
5,5,5,5
5,5,5,5
5,5,5,5

Expected Output: 1
```
**Verifies**:
- Distance = 0 (all same point)
- Forms single constellation

#### Test Case 9: Linear Chain
```
Input:
0,0,0,0
3,0,0,0
6,0,0,0
9,0,0,0

Expected Output: 1
```
**Verifies**:
- Transitive connectivity works
- Each consecutive pair has distance 3
- All should be in same constellation

#### Test Case 10: Almost Connected
```
Input:
0,0,0,0
2,2,0,0

Expected Output: 2
```
**Verifies**:
- Distance = 4 (2+2)
- Should NOT be connected

#### Test Case 11: Maximum Distance Components
```
Input:
0,0,0,0
1,1,1,0
0,0,0,1

Expected Output: 1
```
**Verifies**:
- (0,0,0,0) to (1,1,1,0): distance = 3 ✓
- (0,0,0,0) to (0,0,0,1): distance = 1 ✓
- All connected through (0,0,0,0)

#### Test Case 11b: Negative-to-Positive Boundary
```
Input:
-2,0,0,0
1,0,0,0

Expected Output: 1
```
**Verifies**:
- Distance across zero: |-2-1| + 0 + 0 + 0 = 3
- Exactly at threshold (should connect)
- Negative and positive coordinates interact correctly

#### Test Case 12: Empty Input
```
Input:
(empty or only whitespace)

Expected Output: 0
```
**Verifies**: Handles empty input gracefully
**Rationale**: 0 constellations is the mathematically correct answer for zero points

### 3. Algorithm Correctness Verification

#### Test 13: Manual Trace on Small Input
Take a small input (4-5 points) and:
1. Manually calculate all pairwise distances
2. Manually determine which should be connected
3. Trace through union-find operations step by step
4. Verify algorithm produces same result

Example:
```
Points:
A: 0,0,0,0
B: 1,0,0,0  (dist to A = 1)
C: 2,0,0,0  (dist to A = 2, to B = 1)
D: 10,0,0,0 (dist to A = 10, to B = 9, to C = 8)

Expected unions:
- A-B (distance 1 ≤ 3) ✓
- A-C (distance 2 ≤ 3) ✓
- B-C (distance 1 ≤ 3) ✓
- No connections to D

Expected: 2 constellations {A,B,C} and {D}
```

#### Test 14: Symmetric Distance Verification
```python
def test_symmetric_distance():
    p1 = (1, 2, 3, 4)
    p2 = (5, 6, 7, 8)
    assert manhattan_distance(p1, p2) == manhattan_distance(p2, p1)
```

#### Test 15: Distance Calculation Accuracy
```python
def test_manhattan_distance():
    assert manhattan_distance((0,0,0,0), (1,1,1,1)) == 4
    assert manhattan_distance((0,0,0,0), (3,0,0,0)) == 3
    assert manhattan_distance((1,2,3,4), (1,2,3,4)) == 0
    assert manhattan_distance((-1,-1,-1,-1), (1,1,1,1)) == 8
```

### 4. Union-Find Correctness

#### Test 16: Union-Find Operations
```python
def test_union_find():
    n = 5
    parent = list(range(n))
    rank = [0] * n

    # Test initial state
    assert all(find(i) == i for i in range(n))

    # Test union
    union(0, 1)
    assert find(0) == find(1)

    union(1, 2)
    assert find(0) == find(1) == find(2)

    # Test separate components
    assert find(0) != find(3)
    assert find(0) != find(4)
```

#### Test 17: Path Compression Verification
- After multiple finds, verify parent pointers are compressed
- Ensure find operations are idempotent

### 5. Boundary Conditions

#### Test 18: Maximum Coordinate Values
```
Input:
-8,-8,-8,-8
-5,-5,-5,-5
8,8,8,8

Expected Output: 2
```
**Verifies**:
- Large absolute values handled correctly
- Distance(-8,-8,-8,-8 to -5,-5,-5,-5) = 12 (separate)
- Distance(-5,-5,-5,-5 to 8,8,8,8) = 52 (separate)
- Distance(-8,-8,-8,-8 to 8,8,8,8) = 64 (separate)

#### Test 19: All Dimensions Contribute
```
Input:
0,0,0,0
1,1,1,0
1,1,0,1
1,0,1,1
0,1,1,1

Expected Output: 1
```
**Verifies**:
- Each point differs in exactly 3 dimensions from (0,0,0,0)
- All have distance 3 from origin
- All should connect to origin

### 6. Performance Testing

#### Test 20: Actual Input Performance
1. Run on provided input.md (1037 points)
2. Measure execution time
3. **Expected**: < 1 second
4. **Verify**: No timeout or excessive memory usage

#### Test 21: Worst Case - All Connected
Generate 1000 points all within distance 3 of each other:
```python
# Creates diverse points all within reach (distance ≤ 3)
points = [(i % 4, (i // 4) % 4, 0, 0) for i in range(1000)]
```
- All points should form single constellation (or a few large ones)
- Should still complete quickly
- Tests union-find efficiency with many merge operations

#### Test 22: Worst Case - All Separate
Generate 1000 points all far apart:
```python
points = [(i * 10, 0, 0, 0) for i in range(1000)]
```
- Should produce 1000 separate constellations
- Tests counting efficiency

## Testing Implementation Approach

**Test Automation Strategy**:
- For this one-off Advent of Code problem, tests can be run manually or via simple assert statements
- For more rigorous testing, consider using pytest framework
- Each test case can be a separate function that returns True/False or asserts correctness

### Phase 1: Unit Tests (Run First)
1. Test manhattan_distance function with known inputs
2. Test union-find find() and union() operations
3. Test input parsing with various formats

### Phase 2: Integration Tests (Run Second)
1. Test all 4 provided examples from problem statement
2. Verify exact output matches expected

### Phase 3: Edge Case Tests (Run Third)
1. Run all edge cases (tests 5-12)
2. Verify behavior on boundary conditions

### Phase 4: Correctness Verification (Run Fourth)
1. Manual trace on small inputs
2. Verify union-find correctness properties
3. Check distance calculations

### Phase 5: Performance Tests (Run Last)
1. Run on actual input.md
2. Measure and verify performance (< 1 second expected)
3. Test worst-case scenarios
4. **If slower than expected**: Review implementation for missing optimizations (path compression, union by rank)

## Test Execution Checklist

- [ ] All 4 provided test cases pass
- [ ] Edge case: Single point
- [ ] Edge case: Two points (connected and disconnected)
- [ ] Edge case: Empty input (should return 0)
- [ ] Edge case: All identical points
- [ ] Edge case: Negative-to-positive boundary
- [ ] Linear chain connectivity
- [ ] Manhattan distance calculations verified
- [ ] Union-find operations correct
- [ ] Actual input processes in < 1 second
- [ ] Output format correct (single integer)

## Debugging Strategy

If tests fail:

1. **Wrong constellation count (too high)**:
   - Check if union operation is working correctly
   - Verify find() uses path compression
   - Check if distance threshold is correct (should be ≤ 3, not < 3)

2. **Wrong constellation count (too low)**:
   - Check if all pairs are being compared
   - Verify loop bounds (i < n, j starts at i+1)
   - Check manhattan_distance calculation

3. **Performance issues**:
   - Verify using Union-Find (not building full graph)
   - Check no redundant distance calculations
   - Ensure path compression is implemented

4. **Parsing errors**:
   - Print parsed points to verify format
   - Check for empty lines, whitespace handling
   - Verify coordinate order (x,y,z,w)

## Success Criteria

The implementation is considered correct if:
1. All 4 provided test cases produce exact expected output
2. All edge cases pass
3. Actual input.md completes in < 1 second
4. Output is a single integer (no extra formatting)
5. Manual verification of small examples confirms correctness
