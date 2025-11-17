# Testing Plan: Air Duct Robot Pathfinding - Part 2 (Round Trip)

## Testing Objectives
1. Verify the solution correctly computes round-trip distances
2. Ensure the modification from Part 1 is correctly implemented
3. Validate correctness on known examples
4. Confirm the solution works on the actual input

## Test Strategy Overview
Since Part 2 reuses most of Part 1's code, we focus testing on:
1. The modified TSP calculation (round-trip logic)
2. Integration between Part 1 components and the new round-trip requirement
3. Validation that the answer is strictly greater than Part 1 (round trip costs more)

## Test Cases

### Test 1: Simple Example from Part 1 Problem
**Input Grid**:
```
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
```

**Expected Behavior**:
- Locations: 0, 1, 2, 3, 4 (5 total)
- Part 1 optimal path: 0→4→1→2→3 = 14 steps
- Part 2 must add: 3→0 distance

**Manual Calculation**:

Positions in grid:
- 0: (1,1)
- 1: (1,3)
- 2: (1,9)
- 3: (3,9)
- 4: (3,1)

Path option 1: 0→4→1→2→3→0
- 0→4: 2 steps (down 2)
- 4→1: 4 steps (up 2, right 2)
- 1→2: 6 steps (right 6)
- 2→3: 2 steps (down 2)
- 3→0: 10 steps (up 2, left 8)
- Total: 2 + 4 + 6 + 2 + 10 = 24 steps

Path option 2: 0→1→2→3→4→0
- 0→1: 2 steps (right 2)
- 1→2: 6 steps (right 6)
- 2→3: 2 steps (down 2)
- 3→4: 8 steps (left 8)
- 4→0: 2 steps (up 2)
- **Total: 2 + 6 + 2 + 8 + 2 = 20 steps** (optimal)

**Test Execution**:
```bash
# Create test file with simple grid
python solution.py  # Using test input
```

**Success Criteria**: Output should be 20

### Test 2: Actual Input Validation
**Input**: The provided `input.md` with full grid

**Validation Steps**:
1. Identify all numbered locations in the grid (should be 0-7, total 8 locations)
2. Verify all locations are found by parse_grid
3. Verify distance matrix is symmetric (BFS should give same distance both ways)
4. Verify no infinite distances (all locations reachable)
5. Run TSP solver and get result

**Expected Behavior**:
- Should complete in < 5 seconds
- Answer should be > 428 (Part 1 answer)
- Answer should be reasonable (428 < answer < 1000 estimated)

**Success Criteria**:
- No errors or infinite distances
- Result is an integer > 428

### Test 3: Part 1 vs Part 2 Comparison
**Purpose**: Verify round-trip logic adds positive distance

**Test**:
```python
# Temporarily add debug output to compare Part 1 vs Part 2
# This is for verification only - not permanent code
full_mask = (1 << N) - 1
part1_answer = min(dp[full_mask][i] for i in range(N))
part2_answer = min(dp[full_mask][i] + distances[i][start_idx] for i in range(N))
print(f"Part 1 answer: {part1_answer}")
print(f"Part 2 answer: {part2_answer}")
print(f"Return distance adds: {part2_answer - part1_answer}")
```

**Note**: This is temporary debug code to verify the round-trip modification is working correctly.

**Success Criteria**:
- Part 2 answer > Part 1 answer
- Difference represents the minimum return distance to start
- For actual input: Part 1 = 428 (verified in part_1_answer.txt), Part 2 should be > 428
- Note: Part 2 optimal path may visit locations in different order than Part 1

### Test 4: Round-Trip Distance Verification
**Purpose**: Manually verify the return distance calculation

**Test Process**:
1. Run solution and note which ending location gives minimum in Part 2
2. Manually check: `dp[full_mask][best_end] + distances[best_end][0]`
3. Verify this equals the final answer

**Implementation**:
```python
# Add temporary debug output in solve_tsp or main() for testing
# This is debug code only - remove for final submission
full_mask = (1 << N) - 1
for i in range(N):
    round_trip = dp[full_mask][i] + distances[i][start_idx]
    print(f"Ending at location {sorted_locs[i]}: {dp[full_mask][i]} + {distances[i][start_idx]} = {round_trip}")
```

**Note**: This is temporary debug code for verification purposes only.

**Success Criteria**:
- The minimum printed value matches the final answer
- Return distances are all > 0 (except if ending at start, which shouldn't be optimal)

### Test 5: Edge Case - Two Locations (0 and 1 only)
**Input**: Simple grid with only locations 0 and 1
```
#####
#0.1#
#####
```

**Expected**:
- Distance 0→1: 2 steps
- Distance 1→0: 2 steps
- Part 2 answer: 2 + 2 = 4 steps

**Success Criteria**: Answer is 4

### Test 6: Edge Case - All Locations in a Line
**Input**: Grid where all locations are in a straight line
```
#########
#0123456#
#########
```

**Expected**:
- Optimal Part 1: 0→6 = 6 steps (visit all in order)
- Optimal Part 2: 0→6→0 = 6 + 6 = 12 steps
- OR: Visit in order then return: similar

**Success Criteria**: Answer is 12

### Test 7: Distance Matrix Symmetry Check
**Purpose**: Verify BFS produces symmetric distances (distance A→B = B→A)

**Test**:
```python
for i in range(N):
    for j in range(i+1, N):
        assert distances[i][j] == distances[j][i], \
            f"Asymmetric distance: {i}→{j}={distances[i][j]}, {j}→{i}={distances[j][i]}"
```

**Success Criteria**: No assertion failures

### Test 8: DP State Validation
**Purpose**: Ensure DP correctly computes minimum distances

**Test**:
```python
# After DP completes, verify:
# 1. dp[1 << start_idx][start_idx] == 0 (starting state)
# 2. All reachable states have finite values
# 3. full_mask state is reachable for at least one ending location

# Check initial state
assert dp[1 << start_idx][start_idx] == 0, "Starting state should have 0 distance!"

# Check final state is reachable
full_mask = (1 << N) - 1
reachable = any(dp[full_mask][i] != float('inf') for i in range(N))
assert reachable, "No valid path visiting all locations!"
```

**Success Criteria**: All assertions pass, confirming DP correctness

## Testing Execution Plan

### Phase 1: Unit Testing (Optional - Part 1 code already tested)
- Test `parse_grid()` with simple grids
- Test `calculate_distances()` with small grids
- Test `solve_tsp()` with manual distance matrices

**Rationale**: Since we're reusing Part 1's well-tested functions with minimal modification, extensive unit testing is not critical. Focus on integration and round-trip logic validation instead.

### Phase 2: Integration Testing
1. Run Test 5 (simple 2-location case)
2. Run Test 6 (linear case)
3. Run Test 1 (example from problem)
4. Run Test 7 (symmetry check)
5. Run Test 8 (DP validation)

### Phase 3: Final Validation
1. Run Test 2 (actual input)
2. Run Test 3 (Part 1 vs Part 2 comparison)
3. Run Test 4 (verify return distance calculation)

### Phase 4: Output Verification
1. Ensure output is a single integer
2. Verify output > 428 (Part 1 answer)
3. Check reasonableness (not absurdly large)

## Debug Output Recommendations

During development, include these debug prints:
```python
print(f"Found {len(locations)} locations: {sorted(locations.keys())}")
print(f"Distance matrix computed")
print(f"Starting TSP solver...")
print(f"Part 1 answer would be: {part1_answer}")
print(f"Part 2 answer (round trip): {part2_answer}")
print(f"Return distance adds: {part2_answer - part1_answer}")
```

For final submission, can reduce to just:
```python
print(f"Minimum steps required: {min_steps}")
```

## Success Criteria Summary

The solution is considered correct if:
1. ✅ Runs without errors on actual input
2. ✅ Answer is an integer > 428
3. ✅ Distance matrix is symmetric
4. ✅ All locations are reachable
5. ✅ Part 2 answer > Part 1 answer
6. ✅ Simple test cases produce expected results
7. ✅ Completes in < 5 seconds

## Known Constraints

Based on the input:
- Grid size: 43 rows × 173 columns
- Number of locations: 8 (0 through 7, visible in input.md)
- Maximum possible steps: ~43 + 173 = 216 per segment, ~1500 total (very loose upper bound)
- Expected range: 428 < answer < 1000

## Regression Testing

Compare against Part 1:
- Same grid should give Part 1 answer of 428
- Part 2 should add the minimum return distance
- The difference tells us the optimal return path distance

## Error Handling Validation

Verify the solution handles:
- ✅ Location 0 not found (Part 1 code has assertion)
- ✅ Unreachable locations (Part 1 code warns)
- ✅ Invalid grid format (Part 1 code strips markdown)
- ✅ Empty grid (would fail location check)

These are already handled by Part 1 code, no new handling needed.
