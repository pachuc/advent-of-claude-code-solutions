# Testing Plan: Maze Reachability Counter (Part 2)

## Testing Strategy Overview
We need to verify that our solution correctly counts all distinct locations reachable within 50 steps from (1,1) in a maze generated with favorite_number = 1362.

## Test Categories

### 1. Unit Tests: is_open_space Function

**Test 1.1: Verify is_open_space matches Part 1**
- **Purpose**: Ensure maze generation logic is identical to Part 1
- **Method**: Test known coordinates with favorite_number = 1362
- **Test Cases**:
  - (1, 1) should be open (Part 1 starts here)
  - (31, 39) should be open (Part 1 target was reachable)
  - Test a few coordinates that should be walls
- **Expected**: Same results as Part 1's is_open_space function

**Test 1.2: Edge cases for is_open_space**
- **Test Cases**:
  - (-1, 0) → False (negative x)
  - (0, -1) → False (negative y)
  - (-5, -5) → False (both negative)
  - (0, 0) → Test with favorite_number = 1362
- **Expected**: Negative coordinates always return False

**Test 1.3: Validate with Part 1 example (multiple coordinates)**
- **Purpose**: Verify maze generation with known example
- **Test Cases with favorite_number = 10**:
  - (1, 1) → should be open (starting position)
  - (7, 4) → should be open (target was reachable)
  - Test several coordinates along a known path to verify consistency
- **Method**: Use the Part 1 example to validate multiple coordinates
- **Expected**: All tested coordinates should match known open/wall status

### 2. Integration Tests: count_reachable_locations Function

**Note on Debug Parameter**: Many tests use `debug=True` to access the visited set for validation. The function should support:
- `count_reachable_locations(start, max_steps, favorite_number)` → returns `int` (count only)
- `count_reachable_locations(start, max_steps, favorite_number, debug=True)` → returns `(int, set)` (count and visited set)

**Test 2.1: Minimal step limits**
- **Purpose**: Verify step limit logic works correctly
- **Test Cases**:
  ```
  max_steps = 0: Should return 1 (only starting position)
  max_steps = 1: Should return 1 + number of adjacent open spaces
  max_steps = 2: Should return count of locations within 2 steps
  ```
- **Method**: Manually verify small step counts
- **Verification**:
  - For max_steps=0: count == 1
  - For max_steps=1: count == 1 + (valid adjacent spaces)
  - Each increment should add new reachable locations

**Test 2.2: Starting position always counted**
- **Test Case**: Run with any max_steps >= 0
- **Expected**: Result should always be >= 1 (start position included)

**Test 2.3: No duplicate counting**
- **Purpose**: Ensure each location counted only once
- **Method**:
  - Add instrumentation to track if any coordinate added to visited twice
  - Verify visited set size matches return value
- **Expected**: No duplicates in visited set

**Test 2.4: Step limit strictly enforced**
- **Purpose**: Verify we don't explore beyond max_steps
- **Method**:
  - Run with max_steps = 50
  - Add debug logging to track maximum steps value in queue
  - Verify no location is explored at step > 50
- **Expected**: Maximum steps in queue should be exactly max_steps (50)

**Test 2.5: Boundary condition - max_steps vs max_steps+1**
- **Purpose**: Verify step limit boundary behavior
- **Method**:
  ```python
  count_50 = count_reachable_locations((1,1), 50, 1362)
  count_51 = count_reachable_locations((1,1), 51, 1362)
  assert count_51 >= count_50, "More steps should reach >= same locations"
  ```
- **Expected**:
  - count_51 >= count_50 (monotonicity)
  - If count_51 > count_50, there are new locations reachable at exactly step 51
- **Rationale**: Catches off-by-one errors in step limit logic

### 3. Consistency Tests

**Test 3.1: Monotonicity of reachable count**
- **Purpose**: Verify count increases or stays same as steps increase
- **Method**:
  ```python
  results = []
  for steps in range(0, 55, 5):  # 0, 5, 10, 15, ..., 50
      count = count_reachable_locations((1,1), steps, 1362)
      results.append(count)
  ```
- **Expected**: results should be non-decreasing: results[i] <= results[i+1]
- **Rationale**: More steps = at least same locations reachable, possibly more

**Test 3.2: Comparison with Part 1 knowledge (Enhanced)**
- **Purpose**: Use Part 1 answer to validate Part 2 step counting
- **Known Fact**: Part 1 found (31, 39) reachable in exactly 82 steps from (1,1)
- **Test Cases**:
  ```python
  # Test with max_steps = 50
  count_50, visited_50 = count_reachable_locations((1,1), 50, 1362, debug=True)
  assert (31, 39) not in visited_50, "(31,39) should NOT be reachable in 50 steps"

  # Test with max_steps = 81
  count_81, visited_81 = count_reachable_locations((1,1), 81, 1362, debug=True)
  assert (31, 39) not in visited_81, "(31,39) should NOT be reachable in 81 steps"

  # Test with max_steps = 82
  count_82, visited_82 = count_reachable_locations((1,1), 82, 1362, debug=True)
  assert (31, 39) in visited_82, "(31,39) SHOULD be reachable in 82 steps"
  ```
- **Method**: Use the `debug=True` parameter to return both count and visited set
- **Expected**:
  - max_steps < 82: (31, 39) NOT reachable
  - max_steps >= 82: (31, 39) IS reachable
- **Rationale**: This validates our step counting is precise and matches Part 1's pathfinding

**Test 3.3: Symmetry in local area**
- **Purpose**: Verify BFS explores evenly in all directions
- **Method**: For small max_steps (e.g., 3-5), manually verify the explored region
- **Expected**: Should roughly form a diamond/circular shape if no walls blocking

### 4. Correctness Verification Tests

**Test 4.1: Manual verification for small steps**
- **Purpose**: Hand-verify correctness with small max_steps
- **Method**:
  1. Set max_steps = 2
  2. Print all coordinates in visited set
  3. Manually verify each coordinate:
     - Is it reachable from (1,1) in ≤2 steps?
     - Is it an open space?
     - Are all open spaces within 2 steps included?
- **Expected**: Exact match between manual calculation and code output

**Test 4.2: Validate maze structure around start**
- **Purpose**: Ensure maze generation creates expected local pattern
- **Method**: Print 10x10 grid around (1,1) showing walls vs open spaces
- **Expected**: Visual inspection should show sensible maze pattern

**Test 4.3: BFS distance property (simplified)**
- **Purpose**: Verify BFS respects distance ordering
- **Method**:
  - For a location at Manhattan distance d from start
  - It should be reachable in at least d steps (Manhattan distance is lower bound)
  - Test: Pick (1+d, 1) which has Manhattan distance d from (1,1)
  - Verify it's not reachable with max_steps < d (if there are no walls blocking)
- **Note**: This is a basic sanity check, not a comprehensive BFS verification
- **Expected**: BFS respects fundamental distance properties

### 5. Final Solution Validation

**Test 5.1: Run with actual input**
- **Input**: favorite_number = 1362, start = (1,1), max_steps = 50
- **Method**: Run solution and capture output
- **Validation Checks**:
  - Result is a positive integer
  - Result >= 1 (at minimum, starting position)
  - Result is reasonable (likely in range 100-300 based on step limit)

**Test 5.2: Sanity check against theoretical bounds**
- **Purpose**: Verify result is within theoretical limits
- **Theoretical Maximum**:
  - Perfect square with no walls and radius 50
  - Area = π * 50² ≈ 7,854 locations
  - Manhattan distance 50: (50+1)² = 2,601 locations
- **Expected**: Result should be significantly less due to walls
- **Validation**: 1 <= result < 2,601

**Test 5.3: Reproducibility**
- **Purpose**: Ensure deterministic results
- **Method**: Run solution 3 times
- **Expected**: Identical output all three times

### 6. Edge Case Tests

**Test 6.1: Start position on boundary**
- **Purpose**: Verify algorithm works if start is at x=0 or y=0
- **Test Cases**:
  - start = (0, 0), max_steps = 10
  - start = (0, 5), max_steps = 10
- **Expected**: Should still count correctly without errors

**Test 6.2: Removed (impractical for this context)**
- This test case (all adjacent spaces are walls) is impractical and low-value
- The actual input has (1,1) as accessible with open neighbors
- Testing contrived scenarios adds little value for puzzle-solving

**Test 6.3: Very small max_steps**
- **Test Cases**:
  - max_steps = 0 → expect 1
  - max_steps = 1 → expect 1 + adjacent open spaces
- **Expected**: Correct counts without errors

### 7. Performance Tests

**Test 7.1: Runtime measurement**
- **Purpose**: Ensure solution runs in reasonable time
- **Method**: Time the execution with actual input
- **Expected**: Runtime < 1 second (should be much faster, typically ~0.1s or less)
- **Rationale**: BFS with 50 steps is very efficient; > 1s suggests an implementation issue

**Test 7.2: Memory usage**
- **Purpose**: Verify memory footprint is reasonable
- **Method**: Monitor visited set size during execution
- **Expected**: visited set size < 10,000 coordinates

## Testing Execution Order

1. **Phase 1**: Unit tests on is_open_space (Tests 1.1-1.3)
2. **Phase 2**: Basic integration tests (Tests 2.1-2.5) - includes new boundary test
3. **Phase 3**: Correctness verification with small inputs (Tests 4.1-4.3)
4. **Phase 4**: Consistency checks (Tests 3.1-3.3) - enhanced Test 3.2 with Part 1 cross-validation
5. **Phase 5**: Final solution validation (Tests 5.1-5.3)
6. **Phase 6**: Edge cases (Tests 6.1, 6.3) - Test 6.2 removed
7. **Phase 7**: Performance validation (Tests 7.1-7.2) - tightened threshold

## Success Criteria

The solution is considered correct if:
- ✅ All unit tests pass (is_open_space works correctly)
- ✅ count_reachable_locations returns >= 1 for any max_steps >= 0
- ✅ Monotonicity test passes (increasing steps → increasing/same count)
- ✅ Boundary test passes (max_steps=50 vs 51 behaves correctly)
- ✅ Manual verification for small max_steps matches code output
- ✅ **Part 1 cross-validation passes**:
  - (31, 39) is NOT reachable in 50 steps
  - (31, 39) is NOT reachable in 81 steps
  - (31, 39) IS reachable in 82 steps
- ✅ Final answer is within theoretical bounds [1, 2601]
- ✅ Result is reproducible across multiple runs
- ✅ Runtime < 1 second

## Debugging Strategies

If tests fail:

1. **Wrong count for small max_steps**:
   - Print visited set and manually verify each coordinate
   - Check step limit logic: `if steps < max_steps`
   - Verify visited set initialization includes start

2. **Count doesn't increase with more steps**:
   - Likely bug in visited set or step limit logic
   - Check that neighbors are being added correctly

3. **Performance issues**:
   - Verify visited set prevents re-exploration
   - Check for infinite loops (should be impossible with visited set)

4. **Off-by-one errors**:
   - Common issue with step limits
   - Verify: `steps < max_steps` vs `steps <= max_steps`
   - Test with max_steps = 0 and 1 to identify
   - Use Part 1 cross-validation: test with max_steps=81 vs 82 for (31,39)

## Expected Final Answer Characteristics

Based on the problem constraints:
- Start: (1, 1)
- Max steps: 50
- Favorite number: 1362
- Expected range: Likely 100-300 locations
- Should be significantly less than theoretical max due to walls
- Should NOT include (31, 39) which requires 82 steps
