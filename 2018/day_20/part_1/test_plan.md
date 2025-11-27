# Testing Plan: A Regular Map

## Overview
This testing plan covers verification of the regex parsing, graph building, and shortest path calculation for the facility navigation problem.

## Revision Summary (v2)

This plan has been revised based on critique feedback to address:

1. **Added Missing Edge Cases**:
   - Test 2.3: Empty branch alternative at start `^N(|EW)S$`
   - Test 2.5: Branch mid-path `^NNE(N|S)EE$`

2. **Fixed Incorrect Test Cases**:
   - Test 8.1: Replaced incorrect example with valid `^EE(SS|WSSEE)$` that properly tests BFS shortest path

3. **Clarified Existing Tests**:
   - Test 5.3: Added clearer explanation of expected behavior for paths returning to origin

4. **Improved Test Structure**:
   - Category 6: Converted to validation checks rather than standalone tests
   - Test 7.1: Added specific output validation criteria
   - Test 7.2: Relaxed memory limit from 100MB to 500MB with justification

5. **Enhanced Success Criteria**: Made clearer distinction between must-pass and should-pass tests

## Test Strategy

### Unit Testing Approach
Test individual components in isolation before integration testing:
1. Direction movement logic
2. Regex parsing and graph building
3. BFS shortest path algorithm
4. End-to-end with provided examples

### Integration Testing
Verify the complete solution works correctly with:
1. All provided examples from problem statement
2. Custom edge cases
3. The actual puzzle input

## Test Cases

### Test Category 1: Simple Linear Paths

**Test 1.1: Single Direction**
- Input: `^N$`
- Expected doors: 1
- Expected max distance: 1
- Purpose: Verify basic movement works

**Test 1.2: Multiple Same Direction**
- Input: `^NNN$`
- Expected doors: 3
- Expected max distance: 3
- Purpose: Verify consecutive movements in same direction

**Test 1.3: Multiple Different Directions**
- Input: `^WNE$`
- Expected max distance: 3
- Purpose: Example from problem statement
- Verify: Creates path from (0,0) → (-1,0) → (-1,-1) → (0,-1)

**Test 1.4: Path That Returns to Origin**
- Input: `^NESWW$`
- Expected max distance: Should find furthest point even if path returns
- Purpose: Verify we track maximum distance, not final distance

### Test Category 2: Simple Branches

**Test 2.1: Two-Way Branch**
- Input: `^N(E|W)N$`
- Expected behavior: Creates two paths from north position
  - One going NEN
  - One going NWN
- Purpose: Verify basic branch splitting and merging

**Test 2.2: Empty Branch Alternative (at end)**
- Input: `^N(EW|)S$`
- Expected behavior: Two alternatives:
  - N, then EW, then S
  - N, then nothing, then S
- Purpose: Verify empty branches are handled (positions don't move)

**Test 2.3: Empty Branch Alternative (at start)**
- Input: `^N(|EW)S$`
- Expected behavior: Same as Test 2.2
- Purpose: Verify empty branch handling regardless of position in alternatives list

**Test 2.4: Multiple Alternatives**
- Input: `^(N|S|E|W)$`
- Expected max distance: 1
- Expected doors: 4 different doors
- Purpose: Verify multiple branch options from same point

**Test 2.5: Branch Mid-Path**
- Input: `^NNE(N|S)EE$`
- Expected: Creates paths NNEENEE and NNEESEE
- Verify both branches start from position (1, -2) and continue from there
- Purpose: Ensure branches correctly use positions from before the `(`

### Test Category 3: Nested Branches

**Test 3.1: Two-Level Nesting**
- Input: `^N(E(N|S)|W)$`
- Expected paths:
  - NEN
  - NES
  - NW
- Purpose: Verify nested branch parsing

**Test 3.2: Deep Nesting**
- Input: `^(((N|S)|E)|W)$`
- Expected: All four directions explored
- Purpose: Verify deeply nested branches work correctly

### Test Category 4: Provided Examples

**Test 4.1: Example 1**
- Input: `^WNE$`
- Expected output: 3
- Status: Should pass (baseline)

**Test 4.2: Example 2**
- Input: `^ENWWW(NEEE|SSE(EE|N))$`
- Expected output: 10
- Purpose: Verify nested branches with different path lengths

**Test 4.3: Example 3**
- Input: `^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$`
- Expected output: 18
- Purpose: Verify multiple empty branches

**Test 4.4: Example 4**
- Input: `^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$`
- Expected output: 23
- Purpose: Verify complex nested structure

**Test 4.5: Example 5**
- Input: `^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$`
- Expected output: 31
- Purpose: Verify deeply nested branches with multiple levels

### Test Category 5: Edge Cases

**Test 5.1: Empty Regex**
- Input: `^$`
- Expected output: 0
- Purpose: Verify handling of no movement

**Test 5.2: All Empty Branches**
- Input: `^N(|)(|)$`
- Expected: Same as `^N$`
- Purpose: Verify multiple empty branches don't cause issues

**Test 5.3: Branch Immediately Returning to Same Position**
- Input: `^(NS|EW)$`
- Expected: Both branches end at (0, 0)
- Max distance: 1 because (0,-1) and (1,0) are both 1 door from origin
- Note: Even though both paths return to origin, we track the maximum distance reached during traversal
- Purpose: Verify we track max distance during traversal, not just final position

**Test 5.4: Overlapping Paths**
- Input: `^(NNE|NEE)$`
- Expected: Both paths create different routes but may share rooms
- Purpose: Verify doors are tracked correctly and not duplicated

**Test 5.5: Very Long Linear Path**
- Create a path with 1000 N's
- Expected output: 1000
- Purpose: Verify no stack overflow or performance issues

**Test 5.6: Wide Branching**
- Input: `^(N|S|E|W|NN|SS|EE|WW|NE|NW|SE|SW)$`
- Many alternatives from one branch point
- Purpose: Verify handling of many alternatives

### Test Category 6: Graph Structure Verification

These are validation checks to apply to any test that passes, not standalone test cases.

**Check 6.1: Door Bidirectionality**
- Implementation: For each room A in adjacency graph, for each neighbor B, verify A is in graph[B]
- For any path, verify doors work in both directions
- Purpose: Verify adjacency graph is bidirectional

**Check 6.2: Room Uniqueness**
- For paths that visit same room multiple times
- Verify room is only counted once in graph
- Rooms are represented as (x, y) coordinates in a set/dict, so uniqueness is automatic
- Purpose: Verify no duplicate rooms in graph

**Check 6.3: Connected Components**
- For complex regex, verify all rooms in the graph are reachable from origin via BFS
- Implementation: The BFS traversal should visit every node in the adjacency graph
- Purpose: Ensure graph building doesn't create isolated components (though based on problem structure, this shouldn't happen)

### Test Category 7: Performance Testing

**Test 7.1: Actual Puzzle Input**
- Input: The large regex from input.md (~10K characters)
- Expected:
  - Should complete in under 1 second
  - Output should be a positive integer
  - Output should be >= 0 and <= length of regex (sanity bounds)
  - After getting the answer, can verify against Advent of Code submission
- Purpose: Verify solution handles real input efficiently and produces valid output

**Test 7.2: Memory Usage**
- Monitor memory during parsing of large input
- Expected: Should not exhibit memory growth issues or leaks
- Memory usage should be reasonable (< 500MB) for the given input size
- Note: Python's memory overhead makes exact measurement difficult
- Purpose: Verify no memory leaks or excessive memory usage

### Test Category 8: Algorithm Correctness

**Test 8.1: BFS Shortest Path Property**
- Create a test case where multiple paths reach same room
- Verify BFS finds the shortest one
- Example: `^EE(SS|WSSEE)$`
  - Room (2, 2) is reachable via:
    - Path 1: EESS: 4 doors from origin
    - Path 2: EEWSSEE: 6 doors from origin (goes west then back east)
  - BFS should record distance 4 for (2, 2), not 6
- Purpose: Verify BFS correctly finds shortest paths when multiple routes exist to the same room

**Test 8.2: Maximum Distance Correctness**
- For a known graph, manually calculate expected max distance
- Verify algorithm returns correct maximum
- Purpose: Ensure we're finding the actual maximum, not just any large value

## Test Execution Order

### Phase 1: Unit Tests (Run First)
1. Test simple linear paths (Category 1)
2. Test simple branches (Category 2)
3. Verify graph structure (Category 6.1, 6.2)

### Phase 2: Integration Tests
4. Test nested branches (Category 3)
5. Test provided examples (Category 4) - MUST ALL PASS
6. Test edge cases (Category 5)

### Phase 3: Validation
7. Test BFS correctness (Category 8)
8. Run performance tests (Category 7)

### Phase 4: Final Verification
9. Run on actual puzzle input
10. Verify output is reasonable (should be a positive integer)

## Verification Methods

### Method 1: Manual Calculation
For small examples, manually trace the regex and calculate expected result
- Draw out the map on paper
- Count doors on shortest path to each room
- Verify against code output

### Method 2: Comparison with Examples
- All 5 provided examples MUST produce correct output
- This is the primary verification method

### Method 3: Sanity Checks
- Output should be positive integer
- Output should be ≤ length of regex (can't need more doors than movements)
- Output should be ≥ 0

### Method 4: Graph Properties
- Number of doors should match number of unique movements in regex (accounting for branches)
- Number of rooms should be reasonable given the regex
- All rooms should be reachable from origin

## Test Implementation

### Create Test File Structure
```python
def test_simple_path():
    # Test Category 1
    pass

def test_simple_branches():
    # Test Category 2
    pass

def test_nested_branches():
    # Test Category 3
    pass

def test_provided_examples():
    # Test Category 4 - CRITICAL
    pass

def test_edge_cases():
    # Test Category 5
    pass

def test_actual_input():
    # Test Category 7.1
    pass
```

### Running Tests
1. Run each test function individually
2. Print input, expected output, actual output for each test
3. Mark PASS/FAIL clearly
4. If any test fails, debug before proceeding

## Success Criteria

### Must Pass
- All 5 provided examples (Test Category 4)
- Basic linear paths (Test 1.3)
- Simple branches (Test 2.1)
- Empty branches (Test 2.2)
- Actual puzzle input produces a reasonable answer

### Should Pass
- All other edge cases
- Performance requirements
- All algorithm correctness tests

## Debugging Strategy

If tests fail:

1. **Parsing Issues**
   - Add debug prints to show positions after each character
   - Print stack state at each '(', '|', ')'
   - Verify doors being added correctly

2. **BFS Issues**
   - Print the adjacency graph
   - Print visited rooms and distances
   - Manually verify BFS traversal order

3. **Example Failures**
   - Build a map visualization
   - Manually trace the regex
   - Compare expected vs actual graph structure

4. **Performance Issues**
   - Profile the code to find bottlenecks
   - Check for infinite loops
   - Verify data structure efficiency

## Expected Outcomes

After running all tests:
- All provided examples should pass
- Edge cases should be handled gracefully
- Actual input should produce answer in < 1 second
- Solution should be ready for submission
