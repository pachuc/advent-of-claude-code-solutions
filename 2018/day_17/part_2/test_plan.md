# Test Plan: Water Retention After Spring Dries Up (Part 2)

## Testing Strategy
Verify that the Part 2 solution correctly counts only settled water by testing edge cases, comparing with Part 1 results, and validating the simulation logic.

## Test Implementation Approach
Tests can be implemented as:
- **Manual verification steps** for initial testing (run solution and check output)
- **Assertions in solution code** for automated validation during development
- **Separate test script** for comprehensive automated testing (optional)

For this script-based problem, manual verification with strategic assertions is recommended.

## Test 1: Example Verification
**Objective**: Verify the solution works on the known example

**Test Data**: Use the example from the problem description
```
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=10..13
x=506, y=1..2
x=498, y=13..13
y=13, x=498..504
```

**Expected Results**:
- Part 1 total water: 57 tiles
- Part 2 settled water: 29 tiles

**Validation**:
1. Run the Part 2 solution on the example
2. Verify output is exactly 29
3. Confirm it's less than the Part 1 result (57)
4. **STRONGLY RECOMMENDED**: Enable grid visualization to visually verify settled vs flowing water

**Test Method**:
```python
example_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=10..13
x=506, y=1..2
x=498, y=13..13
y=13, x=498..504"""

result = solve(example_input)
assert result == 29, f"Expected 29, got {result}"

# HIGHLY RECOMMENDED: Uncomment to visualize and manually count 29 settled tiles
# print_grid(clay_set, flowing_water, settled_water, min_x, max_x, min_y, max_y)
```

## Test 2: Comparison with Part 1 Answer
**Objective**: Verify Part 2 result is less than Part 1 result

**Test Data**: Use the actual input.md file

**Expected Results**:
- Part 1 answer: 41027 (from part_1_answer.txt)
- Part 2 answer: Should be < 41027
- Difference should be positive and substantial (representing flowing water)

**Validation**:
1. Run Part 2 solution on actual input
2. Verify: `result < 41027`
3. Verify: `result > 0`
4. Verify: `41027 - result` is a reasonable amount (e.g., > 5000)

**Test Method**:
```python
with open('input.md', 'r') as f:
    actual_input = f.read()

part2_result = solve(actual_input)
part1_result = 41027

assert part2_result < part1_result, f"Part 2 ({part2_result}) should be less than Part 1 ({part1_result})"
assert part2_result > 0, f"Part 2 result should be positive, got {part2_result}"
assert (part1_result - part2_result) > 1000, f"Difference should be substantial: {part1_result - part2_result}"
```

## Test 3: Edge Case - Single Container
**Objective**: Test a simple single container scenario

**Test Data**:
```
x=495, y=1..5
x=505, y=1..5
y=5, x=495..505
```
This creates a simple U-shaped container.

**Expected Results**:
- Water should settle in the container
- Container geometry: 11 tiles wide (x=495 to x=505), walls from y=1 to y=5, bottom at y=5
- Interior space: x=496 to x=504 (9 tiles wide), y=1 to y=4 (4 levels high)
- **Exact expected settled water**: 9 × 4 = **36 tiles**
- All water inside should be settled (no flowing water in a closed container)
- Should count tiles from y=1 to y=5 (respecting the y-range)

**Validation**:
1. Run the test and verify result is exactly 36
2. Verify no flowing water exists within the container
3. Use grid visualization to manually count tiles

## Test 4: Edge Case - Waterfall (No Container)
**Objective**: Test scenario with only flowing water, no settling

**Test Data**:
```
x=499, y=1..5
x=501, y=1..5
```
This creates two walls with a gap - water falls through without settling.

**Expected Results**:
- Walls at x=499 and x=501 from y=1 to y=5
- Water from spring at x=500 flows down between the walls
- No bottom, so water falls through without any container to settle in
- All water at x=500, y=1-5 will be flowing water (`|`), not settled water (`~`)
- **Expected Part 2 result**: **0** (no settled water)

**Validation**:
```python
waterfall_input = """x=499, y=1..5
x=501, y=1..5"""

result = solve(waterfall_input)
assert result == 0, f"Expected 0 settled water for waterfall, got {result}"
```

## Test 5: Edge Case - Stacked Containers
**Objective**: Test multiple containers stacked vertically

**Test Data**:
```
x=495, y=1..10
x=505, y=1..10
y=5, x=495..505
y=10, x=495..505
```
Creates two containers, one on top of the other.

**Expected Results**:
- Two containers separated by floor at y=5, with bottom at y=10
- Container geometry: 11 tiles wide (x=495 to x=505), interior 9 tiles wide (x=496 to x=504)
- Upper container: y=1 to y=4 (4 levels), settled water = 9 × 4 = 36 tiles
- Lower container: y=6 to y=9 (4 levels), settled water = 9 × 4 = 36 tiles
- **Expected total settled water**: 36 + 36 = **72 tiles**
- Both containers should fill with settled water

**Validation**:
1. Run test and verify result is exactly 72
2. Verify both containers have settled water (use grid visualization)
3. Verify water settles in both levels correctly

## Test 6: Edge Case - Overflow Scenario
**Objective**: Test container that allows water to overflow

**Test Data** (Revised for clarity):
```
x=495, y=5..10
x=505, y=5..10
y=10, x=495..500
```
Creates a container with walls but bottom only covers half, allowing overflow on the right.

**Expected Results**:
- Left wall at x=495 from y=5 to y=10
- Right wall at x=505 from y=5 to y=10
- Bottom only from x=495 to x=500 (partial bottom)
- Water fills the left side and is contained: x=496 to x=500, y=6 to y=9
- Interior: 5 tiles wide × 4 levels = **20 tiles** of settled water
- Water at x=501 to x=504 cannot settle (no support on right side), flows as `|`
- **Expected Part 2 result**: **20 tiles** (only the settled portion on the left)

**Validation**:
1. Verify settled water exists only in the contained left portion
2. Verify the result matches the expected 20 tiles
3. Check that overflow positions (x=501-504) are NOT in settled_water set (use grid visualization)

## Test 7: Y-Range Boundary Testing
**Objective**: Verify that only water within the valid y-range is counted

**Test Data**: Create scenario where water exists outside the clay y-range
```
x=495, y=5..10
x=505, y=5..10
y=10, x=495..505
```

**Expected Results**:
- Valid y-range: 5 to 10
- Water above y=5 (like at y=0 from spring) should NOT be counted
- Water at y=5 to y=10 should be counted

**Validation**:
1. Manually verify the y-range calculation
2. Ensure spring water at y=0 is excluded
3. Count only includes water where `min_y <= y <= max_y`

## Test 8: Data Integrity Check
**Objective**: Ensure the simulation doesn't modify Part 1's logic

**Test Data**: Use actual input.md

**Expected Results**:
- Running Part 1 code should still give 41027
- The sets `flowing_water` and `settled_water` should be populated correctly
- `len(settled_water)` = Part 2 result
- `len(flowing_water | settled_water)` = 41027 (Part 1 result)

**Validation**:
```python
# Run simulation
clay_set = parse_input(lines)
min_y, max_y = get_y_range(clay_set)
flowing_water = set()
settled_water = set()
flow_down(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)

# Count both ways
part1_count = len({(x,y) for (x,y) in (flowing_water | settled_water) if min_y <= y <= max_y})
part2_count = len({(x,y) for (x,y) in settled_water if min_y <= y <= max_y})

assert part1_count == 41027, f"Part 1 logic broken: expected 41027, got {part1_count}"
assert part2_count < part1_count, f"Part 2 should be less than Part 1"
```

## Test 9: Set Disjointness
**Objective**: Verify that flowing_water and settled_water sets don't overlap

**Test Data**: Use actual input.md

**Expected Results**:
- A tile cannot be both flowing and settled simultaneously
- `flowing_water & settled_water` should be empty set
- This verifies the simulation logic is sound

**Validation**:
```python
intersection = flowing_water & settled_water
assert len(intersection) == 0, f"Found {len(intersection)} tiles in both sets: {intersection}"
```

## Test 10: Reasonableness Check
**Objective**: Verify the answer is in a reasonable range

**Test Data**: Use actual input.md

**Expected Results**:
- Part 2 result should be positive
- Part 2 result should be at least 30% of Part 1 result (some water settles)
- Part 2 result should be at most 80% of Part 1 result (some water flows)
- Typical ratio is 40-70% settled (though this is a heuristic, not a hard requirement)

**Validation** (Heuristic check with warning):
```python
part2_result = solve(actual_input)
part1_result = 41027
ratio = part2_result / part1_result

# Heuristic check - actual ratio depends on input structure
# Most inputs have 40-70% settled water, but this can vary
if not (0.3 <= ratio <= 0.8):
    print(f"Warning: Ratio {ratio:.1%} outside typical range (30%-80%)")
    print("This may be normal depending on input structure - verify manually")
else:
    print(f"Settled water is {ratio:.1%} of total water (within expected range)")
```

## Test 11: Part 1 Regression Test
**Objective**: Verify that the original Part 1 solution still works correctly

**Test Data**: Use actual input.md

**Expected Results**:
- Running `part_1_solution.py` should still produce **41027**
- This ensures we haven't accidentally modified the Part 1 file

**Validation**:
```bash
# Run the original Part 1 solution
cd /app/agent_workspace/2018/day_17/part_1
python part_1_solution.py
# Verify output is 41027
```

Or programmatically:
```python
# Import and run Part 1 solution
import sys
sys.path.insert(0, '../part_1')
from part_1_solution import solve as solve_part1

part1_result = solve_part1(actual_input)
assert part1_result == 41027, f"Part 1 regression: expected 41027, got {part1_result}"
```

## Testing Execution Order
1. **Test 11**: Part 1 regression (ensure Part 1 still works)
2. **Test 1**: Example verification (builds confidence with known answer)
3. **Test 4**: Waterfall edge case (validates no-settling scenario)
4. **Test 3**: Single container (validates settling scenario)
5. **Test 8**: Data integrity (ensures Part 1 logic intact)
6. **Test 9**: Set disjointness (validates simulation correctness)
7. **Test 2**: Part 1 comparison (validates actual answer is less than Part 1)
8. **Test 10**: Reasonableness check (heuristic sanity check)
9. **Tests 5-7**: Additional edge cases (thorough validation)

## Success Criteria
- ✅ Part 1 regression test passes (Part 1 still produces 41027)
- ✅ Example test produces exactly 29
- ✅ Actual result is less than 41027 and greater than 0
- ✅ All edge cases pass with expected exact values
- ✅ Sets are disjoint (no overlap between flowing and settled)
- ✅ Y-range filtering works correctly
- ✅ Result is in reasonable range (typically 30-80% of Part 1, though may vary)

## Debugging Tools
If tests fail, use these debugging techniques:

1. **Grid Visualization**: Uncomment the `print_grid()` call to see water distribution
2. **Set Inspection**: Print sizes of `flowing_water` and `settled_water` sets
3. **Manual Verification**: For small examples, manually count tiles on printed grid
4. **Difference Analysis**: Compare `flowing_water` and `settled_water` to understand the difference
5. **Y-Range Check**: Print `min_y` and `max_y` to verify range calculation

## Expected Performance
- Example input: < 1 second
- Actual input: < 30 seconds (typically much faster, performance depends on system)
- Memory usage: < 100 MB
- No stack overflow (recursion limit set to 10,000)
