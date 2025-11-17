# Test Plan: Longest Route TSP Variant

## Testing Strategy Overview

**Testing Approach**: Manual verification with known test cases
**Focus Areas**:
1. Input parsing correctness
2. Graph construction accuracy
3. Distance calculation logic
4. Maximum finding correctness
5. Edge cases and special scenarios

## Test Case Categories

### 1. Simple Test Cases (Manual Verification)

#### Test 1.1: Minimal Graph (3 locations)
**Purpose**: Verify basic functionality with smallest non-trivial input

**Input**:
```
Dublin to London = 464
London to Belfast = 518
Dublin to Belfast = 141
```

**Expected Behavior**:
- Locations: {Dublin, London, Belfast}
- Permutations: 3! = 6, but only 3 unique paths (ignoring reverses)
- Possible routes:
  1. Dublin → London → Belfast = 464 + 518 = 982
  2. Dublin → Belfast → London = 141 + 518 = 659
  3. London → Dublin → Belfast = 464 + 141 = 605
  4. London → Belfast → Dublin = 518 + 141 = 659
  5. Belfast → Dublin → London = 141 + 464 = 605
  6. Belfast → London → Dublin = 518 + 464 = 982

**Expected Output**: `982`

**Verification Method**:
- Create a test file with this input
- Run the solution
- Manually verify the output matches 982

#### Test 1.2: Four Locations (Square Graph)
**Purpose**: Test with simple geometric pattern

**Input**:
```
A to B = 10
B to C = 10
C to D = 10
D to A = 10
A to C = 5
B to D = 5
```

**Expected Behavior**:
- Forms a square with diagonals
- Longest path should avoid short diagonals (A-C=5, B-D=5)
- Best route uses three edges of length 10
- Example: A → B → C → D = 10 + 10 + 10 = 30
- Alternative: A → D → C → B = 10 + 10 + 10 = 30

**Expected Output**: `30`

**Note**: Multiple routes achieve this maximum by using only the perimeter edges and avoiding the short diagonals.

**Verification Method**:
- Create test file
- Calculate manually
- Verify output

### 2. Actual Problem Input Test

#### Test 2.1: Full Input Verification
**Purpose**: Verify solution works on actual problem input

**Input**: The provided `input.md` file with 8 locations

**Expected Behavior**:
- Parse all 28 edges correctly
- Generate 40,320 permutations
- Calculate distances correctly
- Find the maximum

**Verification Strategy**:
Since manual calculation is impractical, use these checks:

1. **Location Count Check**:
   - Should identify exactly 8 unique locations
   - Locations: {Faerun, Norrath, Tristram, AlphaCentauri, Arbre, Snowdin, Tambi, Straylight}

2. **Edge Count Check**:
   - Should have 28 unique bidirectional edges
   - Complete graph: n(n-1)/2 = 8×7/2 = 28 ✓

3. **Sanity Check on Output**:
   - Theoretical maximum: Sum of 7 largest edges
   - Calculate: 142 + 135 + 129 + 129 + 122 + 118 + 116 = 891
   - Actual output should be ≤ 891 (this is an upper bound)
   - **Why not achievable**: A path must form a connected route through all nodes; you can't arbitrarily combine any 7 edges
   - More realistic range based on input analysis: 650-850

4. **Comparison with Minimum**:
   - Run a similar algorithm for shortest path
   - Maximum should be significantly larger than minimum
   - This validates we're actually finding max, not min

**Verification Method**:
```python
# Add debug output to solution
print(f"Locations found: {len(locations)}")
print(f"Edges found: {len(distances) // 2}")
print(f"Max distance: {max_distance}")
```

### 3. Edge Cases and Special Scenarios

#### Test 3.1: Two Locations Only
**Purpose**: Test minimal valid input

**Input**:
```
A to B = 100
```

**Expected Output**: `100`
**Reasoning**: Only one possible path: A → B

#### Test 3.2: Uniform Distances
**Purpose**: Test when all edges have same weight

**Input**:
```
A to B = 10
B to C = 10
C to A = 10
```

**Expected Output**: `20`
**Reasoning**: All routes have same length (2 edges × 10)

#### Test 3.3: Star Graph Pattern
**Purpose**: Test hub-and-spoke topology

**Input**:
```
Hub to A = 100
Hub to B = 100
Hub to C = 100
A to B = 1
B to C = 1
C to A = 1
```

**Expected Behavior**:
- Best path uses two of the long hub edges (100 each) and one short peripheral edge (1)
- Example paths achieving maximum:
  - A → Hub → B → C = 100 + 100 + 1 = 201
  - A → Hub → C → B = 100 + 100 + 1 = 201
  - B → Hub → C → A = 100 + 100 + 1 = 201
- Multiple routes achieve this maximum

**Expected Output**: `201`

#### Test 3.4: Single Large Edge
**Purpose**: Verify solution finds and uses the largest edge

**Input**:
```
A to B = 1
B to C = 1
C to D = 1000
D to A = 1
A to C = 1
B to D = 1
```

**Expected Behavior**:
- Graph has 4 nodes, 6 edges (complete graph)
- Longest path must include the C-D edge (1000)
- Best routes use C-D plus two edges of length 1
- Examples:
  - A → B → C → D = 1 + 1 + 1000 = 1002
  - A → C → D → B = 1 + 1000 + 1 = 1002
  - B → C → D → A = 1 + 1000 + 1 = 1002

**Expected Output**: `1002`

### 4. Parsing Tests

#### Test 4.1: Whitespace Handling
**Purpose**: Ensure parser handles extra spaces

**Input**:
```
  London   to   Dublin   =   500
Manchester to London = 100
```

**Expected Behavior**: Should parse correctly, ignoring extra whitespace

#### Test 4.2: Order Independence
**Purpose**: Verify bidirectional edges work correctly

**Input**:
```
A to B = 50
C to A = 30
B to C = 40
```

**Expected Behavior**:
- Can traverse A→B or B→A with same distance (50)
- Order in input file shouldn't matter

### 5. Algorithm Correctness Tests

#### Test 5.1: Verify Maximum, Not Minimum
**Purpose**: Ensure we're actually finding maximum, not minimum

**Method**:
1. Modify code to track both max and min
2. Verify max > min for any non-trivial input
3. For the 3-location example: max=982, min=605

#### Test 5.2: Complete Permutation Coverage
**Purpose**: Verify all permutations are checked

**Method**:
```python
# Add counter
routes_checked = 0
for route in permutations(locations):
    routes_checked += 1
    # ... rest of logic

assert routes_checked == factorial(len(locations))
```

For 8 locations: should check exactly 40,320 routes

**Note**: This includes reverse duplicates (e.g., [A,B,C] and [C,B,A]), which both have the same distance since edges are bidirectional. The algorithm checks all permutations (not just unique paths), which is simpler and still efficient for n=8.

#### Test 5.3: Distance Calculation Accuracy
**Purpose**: Verify distance calculation for a known route

**Method**:
1. Pick a specific route manually
2. Calculate expected distance by hand
3. Force code to calculate that specific route
4. Compare results

**Example**:
```python
# Test route: [A, B, C]
# Expected: distance[A,B] + distance[B,C]
test_route = ('A', 'B', 'C')
expected = distances[('A','B')] + distances[('B','C')]
actual = calculate_route_distance(test_route, distances)
assert actual == expected
```

## Test Execution Plan

### Phase 1: Unit Testing (Component-Level)
1. Test `parse_input()` function:
   - Verify correct location extraction
   - Verify correct distance extraction
   - Verify bidirectional storage

2. Test `calculate_route_distance()` function:
   - Test with known routes
   - Verify correct summation

3. Test `find_longest_route()` function:
   - Use simple 3-location example
   - Verify returns maximum

### Phase 2: Integration Testing
1. Run on simple test case (3 locations)
2. Verify end-to-end correctness
3. Run on 4-location test case
4. Verify correct output

### Phase 3: Full Problem Testing
1. Run on actual input.md
2. Verify:
   - Correct number of locations parsed
   - Correct number of edges parsed
   - Output is within reasonable range
   - Completes in reasonable time (< 1 second)

### Phase 4: Edge Case Testing
1. Test all edge cases listed above
2. Verify correct behavior for each

## Validation Checklist

- [ ] Parses all 8 locations from input.md
- [ ] Parses all 28 edges from input.md
- [ ] Creates bidirectional distances (56 entries in dict)
- [ ] Generates correct number of permutations (40,320)
- [ ] Calculates distance correctly for sample routes
- [ ] Returns maximum, not minimum
- [ ] Completes in under 1 second
- [ ] Output is a positive integer
- [ ] Output is in reasonable range (650-850 for this input)
- [ ] Simple 3-location test case returns 982
- [ ] Two-location test case works correctly
- [ ] Four-location square test case returns 30
- [ ] Single large edge test case returns 1002

## Debugging Strategy

If tests fail, check in this order:

**Step 0: File Reading**:
   - Verify input file exists and is readable
   - Check file path is correct ('input.md')
   - Confirm file has content

1. **Parsing Issues**:
   - Print parsed locations and count
   - Print parsed distances and count
   - Verify bidirectional entries exist

2. **Distance Calculation Issues**:
   - Print a few sample routes and their distances
   - Manually verify one route calculation
   - Check for KeyError in distance lookup

3. **Maximum Finding Issues**:
   - Print both max and min distances found
   - Verify max > min
   - Print the route that achieves maximum

4. **Performance Issues**:
   - Add timer around main computation
   - Verify permutation count matches expected
   - Check for infinite loops

## Expected Output for Main Problem

Based on the input provided (8 locations, 28 edges):

**Rough Estimate**:
- Theoretical upper bound: ~891 (sum of 7 largest edges, not achievable as a connected path)
- **Realistic range: 650-850**
- The actual answer will be a specific value in this range

**Verification**:
- Compare with Part 1 (shortest route) if available
- Should be significantly larger than shortest route (likely 3-4x larger)
- Should be less than theoretical upper bound of 891
- Should represent a valid connected path through all 8 locations

## Test Success Criteria

The solution is considered correct if:

1. ✅ All simple test cases pass with correct output
2. ✅ Actual input produces output in expected range
3. ✅ Parsing extracts correct number of locations and edges
4. ✅ Algorithm completes in reasonable time (< 1 second)
5. ✅ Maximum distance > Minimum distance (if we calculate both)
6. ✅ No runtime errors or exceptions
7. ✅ Output is a single integer value

## Performance Benchmarks

- **Target Runtime**: < 100ms for 8 locations
- **Acceptable Runtime**: < 1 second for 8 locations
- **Memory Usage**: < 10MB
- **Scalability**: Should handle up to 10 locations comfortably

## Manual Verification Steps

1. Create simple test file with 3 locations
2. Run solution on test file
3. Verify output is 982
4. Run solution on actual input.md
5. Verify output is reasonable (600-900 range)
6. Verify no errors during execution
7. Check execution completes quickly

## Notes

- Since this is a script (not production code), exhaustive testing isn't necessary
- Focus on correctness verification with a few key test cases
- Primary validation is that actual input produces a reasonable answer
- Manual verification of simple cases builds confidence in algorithm correctness
