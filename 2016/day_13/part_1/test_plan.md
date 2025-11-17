# Test Plan: Maze Pathfinding

## Testing Strategy Overview

The testing approach focuses on verifying:
1. **Correctness** of maze generation logic
2. **Correctness** of pathfinding algorithm
3. **Edge cases** specific to the problem constraints
4. **Validation** against provided example

## Test Categories

### 1. Maze Generation Testing

#### Test 1.1: Verify Example from Problem Statement
**Purpose**: Validate the `is_open_space` function against known example

**Setup**:
- Use favorite_number = 10 (from problem example)
- Test specific coordinates mentioned or implied in the example

**Test Cases**:
```
Favorite = 10, (0, 0): Calculate and verify
Favorite = 10, (1, 1): Should be open (starting position in example)
Favorite = 10, (7, 4): Should be open (ending position in example)
```

**Method**:
1. For coordinate (1, 1) with favorite = 10:
   - Calculate: 1*1 + 3*1 + 2*1*1 + 1 + 1*1 = 1 + 3 + 2 + 1 + 1 = 8
   - Add favorite: 8 + 10 = 18
   - Binary: 18 = 0b10010
   - Count 1s: 2 (even)
   - Expected: open space ✓

2. For coordinate (0, 0) with favorite = 10:
   - Calculate: 0 + 0 + 0 + 0 + 0 = 0
   - Add favorite: 0 + 10 = 10
   - Binary: 10 = 0b1010
   - Count 1s: 2 (even)
   - Expected: open space ✓

3. For coordinate (7, 4) with favorite = 10:
   - Calculate: 7*7 + 3*7 + 2*7*4 + 4 + 4*4 = 49 + 21 + 56 + 4 + 16 = 146
   - Add favorite: 146 + 10 = 156
   - Binary: 156 = 0b10011100
   - Count 1s: 4 (even)
   - Expected: open space ✓

**Verification**: Manually calculate expected results and compare with function output

#### Test 1.2: Known Wall and Open Space Examples
**Purpose**: Verify wall/open space determination with hand-calculated examples

**Test Cases**:
```
Test various coordinates with favorite = 1362:
- Calculate expected values manually
- Verify function returns correct boolean
```

**Sample Manual Calculation**:
- (1, 0): 1 + 3 + 0 + 0 + 0 = 4, + 1362 = 1366 = 0b10101010110 (6 ones, even) → open
- (0, 1): 0 + 0 + 0 + 1 + 1 = 2, + 1362 = 1364 = 0b10101010100 (5 ones, odd) → wall

#### Test 1.3: Boundary Conditions for Maze Generation
**Purpose**: Ensure no errors at coordinate boundaries

**Test Cases**:
- (0, 0): Minimum valid coordinate
- Large coordinates: (100, 100), (1000, 1000) - should not error
- Verify negative coordinates are properly rejected/handled (x < 0 or y < 0)

### 2. Pathfinding Algorithm Testing

#### Test 2.1: Validate Against Problem Example
**Purpose**: Verify BFS finds correct shortest path length using the example

**Setup**:
- Favorite number = 10
- Start = (1, 1)
- Target = (7, 4)
- Expected result = 11 steps

**Method**:
1. Run pathfinding algorithm with example parameters
2. Verify result equals 11
3. This is the PRIMARY validation test

**Success Criteria**: Output must be exactly 11

#### Test 2.2: Actual Problem Input
**Purpose**: Solve the actual problem and verify reasonable output

**Setup**:
- Favorite number = 1362
- Start = (1, 1)
- Target = (31, 39)

**Sanity Checks**:
- Result should be >= Manhattan distance: |31-1| + |39-1| = 30 + 38 = 68
- Result should be < 1000 (if much higher, likely a bug)
- Result should be < explored area (if we explore 2500 cells, path should be much shorter)

**Method**:
1. Run the algorithm
2. Verify result is a positive integer
3. Verify result is >= 68 (Manhattan distance lower bound)
4. Check that result seems reasonable (not obviously wrong)

#### Test 2.3: Simple Path Cases
**Purpose**: Test algorithm on trivial cases

**Test Cases**:

**Case A - Start is Target**:
- Start = (1, 1), Target = (1, 1)
- Expected: 0 steps
- Note: Modify code to handle this edge case if needed

**Case B - Adjacent Cells**:
- Find two adjacent open spaces in the maze
- Verify path length is 1

**Case C - Verify Movement Restrictions**:
- Ensure algorithm doesn't move diagonally
- Ensure algorithm doesn't move to negative coordinates
- Ensure algorithm doesn't move to walls

### 3. Edge Cases and Special Scenarios

#### Test 3.1: Starting Position Validation
**Purpose**: Ensure starting position (1, 1) is actually an open space

**Method**:
- Call `is_open_space(1, 1, 1362)`
- Verify it returns True
- If False, problem is unsolvable as stated

**Expected for (1, 1) with favorite = 1362**:
- Calculate: 1 + 3 + 2 + 1 + 1 = 8
- Add: 8 + 1362 = 1370 = 0b10101011010 (6 ones, even) → open ✓

#### Test 3.2: Target Position Validation
**Purpose**: Ensure target position (31, 39) is actually an open space

**Method**:
- Call `is_open_space(31, 39, 1362)`
- Verify it returns True
- If False, problem is unsolvable as stated

**Expected for (31, 39) with favorite = 1362**:
- Calculate: 31*31 + 3*31 + 2*31*39 + 39 + 39*39
- = 961 + 93 + 2418 + 39 + 1521 = 5032
- Add: 5032 + 1362 = 6394 = 0b1100011111010 (8 ones, even) → open ✓

#### Test 3.3: Visited Set Functionality
**Purpose**: Ensure we don't revisit cells (infinite loop prevention)

**Method**:
- Add debug logging to count cells visited
- Verify visited count is reasonable
  - For target (31, 39), expect roughly 1000-3000 cells visited
  - Should be well under 10,000
- Verify visited set prevents revisiting

**Success Criteria**: Algorithm terminates in reasonable time (< 1 second)

#### Test 3.4: Queue Operations
**Purpose**: Verify BFS explores in correct order (layer by layer)

**Method**:
- Optionally add debug output showing steps count for first few dequeued items
- Verify steps increase monotonically or stay same (BFS property)
- Steps should go: 0, 1, 1, 1, ..., 2, 2, 2, ... (all distance-1 nodes before distance-2)

### 4. Algorithm Correctness Verification

#### Test 4.1: Shortest Path Guarantee
**Purpose**: Verify BFS properties hold

**Method**:
- BFS guarantees shortest path in unweighted graphs
- Verify we process all nodes at distance D before distance D+1
- This is inherent to BFS if implemented correctly with a queue

**Verification**:
- Code review: Ensure using `deque` from `collections` module
- Code review: Verify using `popleft()` NOT `pop()` to ensure FIFO behavior (critical!)
- Code review: Ensure incrementing steps by 1 for each neighbor
- Code review: Verify nodes are added to visited set when enqueueing (prevents duplicates in queue)
- No additional runtime test needed if implementation follows BFS pattern correctly

#### Test 4.2: Four-Directional Movement
**Purpose**: Ensure only 4 directions are used (no diagonal)

**Method**:
- Code review: Verify direction list is exactly `[(0,1), (0,-1), (1,0), (-1,0)]` or equivalent
- No additional runtime test needed

#### Test 4.3: Non-Negative Coordinate Constraint
**Purpose**: Ensure we never explore negative coordinates

**Method**:
- Code review: Verify condition `nx >= 0 and ny >= 0` before exploring
- Optional: Add assertion in loop to verify this

### 5. Integration Testing

#### Test 5.1: End-to-End with Example Input
**Purpose**: Full system test with known answer

**Steps**:
1. Create test input file with "10"
2. Run script with modified constants: START=(1,1), TARGET=(7,4)
3. Verify output is 11

#### Test 5.2: End-to-End with Actual Input
**Purpose**: Solve the actual problem

**Steps**:
1. Use input file with "1362"
2. Use START=(1,1), TARGET=(31,39)
3. Run script and capture output
4. Verify output is a reasonable integer (>= 68, < 1000)

### 6. Test Execution Plan

#### Phase 0: Quick Smoke Test
1. Before running full test suite, verify that (1,1) is open with favorite=1362
2. If this fails, something is fundamentally wrong with the maze generation
3. Expected: `is_open_space(1, 1, 1362)` returns `True`

#### Phase 1: Unit Tests (Manual Verification)
1. Test maze generation function with hand-calculated examples (Tests 1.1, 1.2)
2. Verify starting and target positions are open (Tests 3.1, 3.2)

#### Phase 2: Algorithm Validation
1. Run with example input (favorite=10, target=(7,4)) → must get 11 (Test 2.1)
2. This is the CRITICAL validation step

#### Phase 3: Actual Problem Solution
1. Run with actual input (favorite=1362, target=(31,39)) (Test 2.2)
2. Verify output is reasonable

#### Phase 4: Code Review
1. Verify BFS implementation correctness (Test 4.1, 4.2, 4.3)
2. Check data structures are correct (deque, set)
3. Verify all constraints are enforced

## Test Success Criteria

### Minimum Required Tests:
1. ✅ **Example validation**: favorite=10, (1,1)→(7,4) must return 11
2. ✅ **Actual solution**: favorite=1362, (1,1)→(31,39) returns reasonable value (>= 68)
3. ✅ **Code review**: BFS implemented correctly with proper data structures

### Additional Validation:
- Manual calculation of several maze cells matches function output
- Starting and target positions are verified as open spaces
- Algorithm terminates in reasonable time (< 1 second)

## Expected Challenges and Mitigations

### Challenge 1: Off-by-One Errors
- **Risk**: Incorrect step counting or coordinate calculation
- **Mitigation**: Validate with example where answer is known (11 steps)

### Challenge 2: Formula Implementation Error
- **Risk**: Wrong formula for maze generation
- **Mitigation**: Hand-calculate several examples and compare

### Challenge 3: BFS Implementation Bugs
- **Risk**: Using stack instead of queue, or incorrect visited tracking
- **Mitigation**: Code review, verify with example

## Test Output Format

For a simple script, use straightforward assertions or print comparisons:
```python
# Example for maze generation test
assert is_open_space(1, 1, 10) == True, "Expected (1,1) to be open with favorite=10"
print(f"✓ Test 1.1: (1,1) with favorite=10 is open")

# Example for pathfinding test
result = find_shortest_path((1,1), (7,4), 10)
assert result == 11, f"Expected 11 steps, got {result}"
print(f"✓ Test 2.1: Example validation passed (11 steps)")
```

For more formal reporting (optional):
```
Test X.Y: [Test Name]
Status: PASS/FAIL
Expected: [expected value]
Actual: [actual value]
Notes: [any relevant observations]
```

## Summary

The test plan focuses on:
1. **Validating the example** (favorite=10, 11 steps) - CRITICAL TEST
2. **Solving the actual problem** with reasonable output
3. **Code review** to ensure correct BFS implementation
4. **Spot checks** of maze generation with manual calculations

This approach balances thoroughness with practicality for a one-time problem solution script.
