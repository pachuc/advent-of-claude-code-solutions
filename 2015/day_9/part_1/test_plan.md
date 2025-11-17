# Test Plan: Traveling Salesman Problem - Shortest Route

## Testing Strategy Overview

Since this is a script to solve a specific problem instance, testing focuses on:
1. **Correctness verification** - Ensure the algorithm produces correct results
2. **Edge case handling** - Test with simple cases we can verify manually
3. **Input parsing validation** - Ensure distances are read correctly
4. **Algorithm logic verification** - Confirm route distance calculations are accurate

## Test Case 1: Example from Problem Statement

**Purpose:** Verify solution matches the given example

**Input:**
```
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
```

**Expected Behavior:**
- Locations identified: London, Dublin, Belfast (3 locations)
- Total permutations: 3! = 6 (or 3 unique paths)
- Minimum distance: 605

**Verification Steps:**
1. Create a test file with the example input
2. Run the solution on this test file
3. Verify output is exactly `605`

**Manual Calculation:**
- London → Dublin → Belfast: 464 + 141 = 605 ✓ (shortest)
- London → Belfast → Dublin: 518 + 141 = 659
- Dublin → London → Belfast: 464 + 518 = 982
- Dublin → Belfast → London: 141 + 518 = 659
- Belfast → London → Dublin: 518 + 464 = 982
- Belfast → Dublin → London: 141 + 464 = 605 ✓ (shortest)

## Test Case 2: Minimal Graph (2 Locations)

**Purpose:** Test simplest possible case

**Input:**
```
A to B = 100
```

**Expected Behavior:**
- Locations: A, B
- Only one possible route: A → B or B → A
- Minimum distance: 100

**Verification:**
- Ensure solution handles this minimal case without errors
- Confirm output is `100`

## Test Case 3: Complete Triangle (3 Locations, All Equal)

**Purpose:** Test symmetry and tie-breaking

**Input:**
```
X to Y = 10
Y to Z = 10
X to Z = 10
```

**Expected Behavior:**
- All routes have same total distance: 20
- Minimum distance: 20
- Verifies solution handles ties correctly (all permutations yield same result)

**Verification:**
- Any route: X→Y→Z = 10+10 = 20
- Solution should return `20` consistently
- All 6 permutations should calculate to 20, confirming minimum detection works even with ties

## Test Case 4: Star Pattern (Optimal Route Uses Center)

**Purpose:** Test a graph where structure matters

**Input:**
```
Center to A = 1
Center to B = 1
Center to C = 1
A to B = 100
B to C = 100
A to C = 100
```

**Expected Behavior:**
- 4 locations total: Center, A, B, C
- Outer nodes are far apart (distance 100), but all close to Center (distance 1)
- Optimal routes minimize use of expensive outer edges

**Manual Calculation of Routes:**
- A → B → C → Center: 100 + 100 + 1 = 201
- A → B → Center → C: 100 + 1 + 1 = 102
- A → Center → B → C: 1 + 1 + 100 = 102 ✓ (shortest)
- A → Center → C → B: 1 + 1 + 100 = 102 ✓ (shortest)
- A → C → B → Center: 100 + 100 + 1 = 201
- A → C → Center → B: 100 + 1 + 1 = 102 ✓ (shortest)
- (Plus 18 more permutations starting from other locations)

**Expected Output:** 102

**Note:** This test reveals if the algorithm properly explores all routes and finds optimal paths in non-uniform graphs

## Test Case 5: Actual Input Validation

**Purpose:** Verify the real input is processed correctly

**Verification Steps:**

### 5.1: Location Count
- Parse the input file
- Count unique locations
- **Expected:** Exactly 8 locations
- **Actual locations:** Faerun, Norrath, Tristram, AlphaCentauri, Arbre, Snowdin, Tambi, Straylight

### 5.2: Distance Count
- Count number of distance specifications
- **Expected:** 28 lines (8 choose 2 = 28 for complete graph)
- Verify this matches a complete graph: n(n-1)/2 = 8×7/2 = 28 ✓

### 5.3: Bidirectionality Check
- Pick a random pair, e.g., "Faerun to Norrath = 129"
- Verify `distances['Faerun']['Norrath'] == 129`
- Verify `distances['Norrath']['Faerun'] == 129`
- Both should be equal and accessible

### 5.4: Sample Distance Verification
- Manually verify a few distances from input:
  - Faerun to Norrath = 129
  - AlphaCentauri to Snowdin = 12
  - Tambi to Straylight = 70
- Ensure these are correctly stored in the distance dictionary

## Test Case 6: Route Calculation Logic

**Purpose:** Verify distance calculation for a specific route is correct

**Test Approach:**
- Manually construct a route: `['Faerun', 'AlphaCentauri', 'Snowdin', 'Tambi', ...]`
- Calculate expected distance by hand using input data:
  - Faerun → AlphaCentauri: 13
  - AlphaCentauri → Snowdin: 12
  - Snowdin → Tambi: 15
  - (Continue for all 7 edges in route)
- Run the `calculate_route_distance` function
- Verify the result matches manual calculation

**Example Manual Calculation:**
Route: Faerun → AlphaCentauri → Snowdin → Tambi → Arbre → Straylight → Norrath → Tristram
- Faerun → AlphaCentauri = 13
- AlphaCentauri → Snowdin = 12
- Snowdin → Tambi = 15
- Tambi → Arbre = 53
- Arbre → Straylight = 40
- Straylight → Norrath = 54
- Norrath → Tristram = 142
- **Total = 329**

## Test Case 7: Permutation Count Verification

**Purpose:** Ensure all routes are being explored

**Verification:**
- For 8 locations, expect 8! = 40,320 permutations
- Add a counter in the code to track permutations checked
- Verify counter reaches 40,320
- This confirms we're not missing any routes

**Implementation:**
```python
count = 0
for route in permutations(locations):
    count += 1
    # ... calculate distance ...
print(f"Checked {count} permutations")
# Should print: Checked 40320 permutations
```

## Test Case 8: Minimum Detection Logic

**Purpose:** Verify minimum is correctly identified

**Test Approach:**
- Use a small dataset where we know the answer
- Add debug output showing all route distances
- Verify the minimum is correctly identified
- Use Test Case 1 (3 locations) for this:
  - Should see 6 distances printed
  - Minimum should be 605

## Edge Cases and Boundary Conditions

### Edge Case 1: All Distances Equal
- What if all edges have the same weight?
- Answer should be: (n-1) × distance
- For 8 locations with distance 10 each: 7 × 10 = 70

### Edge Case 2: One Very Short Edge
- What if one edge is much shorter than others?
- Optimal route should include this edge
- Verify the algorithm finds it

### Edge Case 3: Triangle Inequality Violation
- The problem doesn't guarantee triangle inequality
- Example: A-B=5, B-C=5, but A-C=100
- Going through B is better: verify this is found

## Regression Testing

**Final Verification on Actual Input:**

1. **Run the solution on the actual input**
2. **Record the output** (the minimum distance found)
3. **Verify properties:**
   - Output is a positive integer
   - Output is reasonable (greater than longest single edge, less than sum of all edges)
   - Output is consistent across multiple runs

4. **Sanity Checks:**
   - Minimum distance should be ≥ the maximum single edge distance (since we travel multiple edges)
   - Maximum single edge from input: 142 (Norrath to Tristram)
   - So answer must be > 142
   - Minimum distance should be << sum of all edges
   - Rough heuristic: 7 edges needed, smallest edges are 12, 13, 15, 15, 18, 24, 40...
   - Sum of 7 smallest ≈ 137 (note: this is a heuristic only, not a guaranteed lower bound, as these edges may not form a connected path)
   - Realistic expected range: 200-500 based on input values

## Test Execution Checklist

**Execution Strategy:** Create test input files and run the solution script on each, verifying output manually.

**Setup:**
- Create `test_inputs/` directory
- Create separate `.txt` files for each test case (test1.txt, test2.txt, etc.)
- Modify the script temporarily to read from these test files, or use command-line arguments

**Tests to Run:**
- [ ] Run Test Case 1 (example input) - verify output is 605
- [ ] Run Test Case 2 (2 locations) - verify output is 100
- [ ] Run Test Case 3 (equal triangle) - verify output is 20
- [ ] Run Test Case 4 (star pattern) - verify output is 102
- [ ] Verify actual input has 8 locations and 28 distances
- [ ] Verify bidirectional distances are stored correctly
- [ ] Manually verify one complete route calculation
- [ ] Verify permutation count is 40,320 (add debug print if needed)
- [ ] Run solution on actual input and verify output is reasonable (200-500 range)
- [ ] Run solution multiple times to ensure deterministic output

## Debugging Strategy

If tests fail:

1. **Wrong output on example:** Check parsing logic and distance calculation
2. **Crashes or errors:** Check dictionary access, ensure all location pairs exist
3. **Output seems too high/low:** Print intermediate routes and distances to debug
4. **Inconsistent results:** Check for any randomness or uninitialized variables

## Performance Verification

**Expected Runtime:**
- With 40,320 permutations and simple operations
- Expected runtime: < 1 second on modern hardware
- If runtime > 5 seconds, investigate performance issues

**Performance Test:**
- Time the execution
- Verify it completes in reasonable time
- No optimization needed for n=8, but good to verify

## Success Criteria

The solution is correct if:
1. ✓ Passes the example test (output = 605 for 3-city example)
2. ✓ Correctly parses all 28 distances from actual input
3. ✓ Identifies all 8 locations
4. ✓ Generates 40,320 permutations
5. ✓ Produces a consistent, reasonable output for actual input
6. ✓ Completes in under 5 seconds
