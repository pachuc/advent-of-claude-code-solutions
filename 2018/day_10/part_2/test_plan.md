# Testing Plan - Part 2: The Stars Align

## Testing Objectives
1. Verify that the alignment time calculation is correct
2. Ensure the output matches the expected format
3. Validate that we're finding the same time that produced "LRGPBHEZ" in Part 1
4. Test edge cases and boundary conditions

## Test Strategy Overview
Since Part 2 reuses the core logic from Part 1, and Part 1 already works correctly (it found the message "LRGPBHEZ"), our main goal is to verify that:
- We're outputting the time value instead of the message
- The time value is correct and consistent with Part 1

## Test 1: Consistency Check with Part 1

### Purpose
Verify that Part 2 returns the same alignment time that Part 1 used to generate "LRGPBHEZ".

### Test Procedure
1. Run Part 2 solution with `input.md`
2. Record the output time `T`
3. Manually verify by running Part 1 solution and checking that:
   - Part 1 reports: `Message appears at t=T`
   - Part 1 shows the message "LRGPBHEZ" at this time
   - The two times match exactly

### Expected Result
- Part 2 outputs a single integer
- Part 1's reported alignment time matches Part 2's output
- Part 1 shows "LRGPBHEZ" at time T

### Validation Method
```bash
# Run Part 2
python solution.py input.md > part2_output.txt

# Run Part 1
python ../part_1/part_1_solution.py input.md > part1_output.txt

# Compare the time values
# Part 2 should output just the number
# Part 1 should show "Message appears at t=<number>"
```

## Test 2: Visual Verification (Optional - Redundant with Test 1)

### Purpose
Confirm that at the calculated time, the points actually form "LRGPBHEZ".

**Note:** This test is optional since Test 1 already verifies consistency with Part 1, which demonstrates the message at time T.

### Test Procedure
1. Get the alignment time `T` from Part 2 output
2. Modify Part 1 solution to visualize at time `T` explicitly
3. Verify the visual output shows "LRGPBHEZ" clearly

### Expected Result
- At time `T`, points form readable letters
- Letters spell "LRGPBHEZ"
- Bounding box is minimal (compact arrangement)

### Validation Method
Use Part 1's visualization functionality:
```python
# In Part 1 solution
alignment_time = <output from Part 2>
aligned_positions = calculate_positions(points, alignment_time)
message_visual = visualize_points(aligned_positions)
print(message_visual)
# Should show clear "LRGPBHEZ"
```

## Test 3: Boundary Time Testing

### Purpose
Verify that times before and after the alignment time have larger bounding box areas.

### Test Procedure
1. Get alignment time `T` from Part 2
2. Calculate bounding box area at times: `T-1`, `T`, `T+1`
3. Verify: `area(T-1) >= area(T)` and `area(T+1) > area(T)`

### Expected Result
- Area at `T-1` is greater than or equal to area at `T`
- Area at `T+1` is strictly greater than area at `T`
- This confirms `T` is the minimum

### Validation Method
```python
# Add test code
points = parse_input('input.md')
T = find_alignment_time(points)

area_before = get_bounding_box_area(calculate_positions(points, T - 1))
area_at = get_bounding_box_area(calculate_positions(points, T))
area_after = get_bounding_box_area(calculate_positions(points, T + 1))

print(f"Area at t={T-1}: {area_before}")
print(f"Area at t={T}: {area_at}")
print(f"Area at t={T+1}: {area_after}")

assert area_at <= area_before, "Area at T should be <= area before"
assert area_after > area_at, "Area after T should be > area at T"
print("✓ Boundary test passed")
```

## Test 4: Output Format Validation

### Purpose
Ensure the output is exactly as expected - a single integer with no extra formatting.

### Test Procedure
1. Run the solution
2. Check output format
3. Verify it's a valid positive integer

### Expected Result
- Output is a single line
- Contains only digits (and possibly a newline)
- No extra text, labels, or formatting

### Validation Method
```bash
# Run and capture output
output=$(python solution.py input.md)

# Check it's a valid integer
if [[ "$output" =~ ^[0-9]+$ ]]; then
    echo "✓ Output format is correct: $output"
else
    echo "✗ Output format is invalid: $output"
    exit 1
fi
```

## Test 5: Small Example Test

### Purpose
Test with the small example from Part 1 problem description (points form "HI" after 3 seconds).

### Test Data
Create a test file `example.txt` with the example data:
```
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
```

### Expected Result
- Output should be `3`

### Validation Method
```bash
python solution.py example.txt
# Should output: 3
```

## Test 6: Performance Test

### Purpose
Ensure the solution runs in reasonable time for the actual input.

### Test Procedure
1. Time the execution with the actual input
2. Verify it completes in under 5 seconds

### Expected Result
- Execution time < 5 seconds (likely < 1 second)
- No memory issues
- Correct output

### Validation Method
```bash
time python solution.py input.md
# Should complete quickly
```

## Test 7: Input Parsing Validation

### Purpose
Verify that all input lines are parsed correctly.

### Test Procedure
1. Count lines in `input.md`
2. Check that parser returns same number of points
3. Spot-check a few parsed values

### Expected Result
- 356 points parsed (based on manual count of input file)
- First point: `position=(-39892, -9859), velocity=(4, 1)` (from line 1 of input)
- Last point: `position=(-9860, -9862), velocity=(1, 1)` (from line 356 of input)

**Note:** These expected values are from manual inspection of input.md. Verify before running tests.

### Validation Method
```python
points = parse_input('input.md')
print(f"Parsed {len(points)} points")
print(f"First point: {points[0]}")
print(f"Last point: {points[-1]}")

assert len(points) == 356, "Should parse 356 points"
assert points[0] == (-39892, -9859, 4, 1), "First point mismatch"
assert points[-1] == (-9860, -9862, 1, 1), "Last point mismatch"
print("✓ Parsing test passed")
```

## Test 8: Edge Case - Monotonic Area Check

### Purpose
Verify that the bounding box area is strictly decreasing until the minimum, then strictly increasing.

### Test Procedure
1. Calculate areas for times 0 to T+10
2. Verify monotonic decrease until T
3. Verify monotonic increase after T

### Expected Result
- Areas decrease: 0, 1, 2, ..., T-1, T
- Areas increase: T, T+1, T+2, ...

### Validation Method
```python
points = parse_input('input.md')
T = find_alignment_time(points)

areas = []
for t in range(max(0, T-10), T+11):
    pos = calculate_positions(points, t)
    area = get_bounding_box_area(pos)
    areas.append((t, area))
    print(f"t={t}: area={area}")

# Check decreasing before T and increasing after T
for i in range(len(areas) - 1):
    if areas[i][0] < T:
        assert areas[i][1] >= areas[i+1][1], f"Area should decrease before T"
    elif areas[i][0] > T:  # Fixed: use > instead of >= to avoid checking T itself
        assert areas[i][1] < areas[i+1][1], f"Area should increase after T"

print("✓ Monotonic area test passed")
```

## Testing Summary Checklist

### Critical Tests (Must Pass)
- [ ] Test 1: Part 1 and Part 2 report same alignment time
- [ ] Test 3: Bounding box area is minimal at calculated time
- [ ] Test 5: Small example returns 3

### Important Tests (Should Pass)
- [ ] Test 4: Output format is a single integer
- [ ] Test 7: Input parsing is correct (356 points)

### Optional Tests (Nice to Have)
- [ ] Test 2: Visual verification shows "LRGPBHEZ" at calculated time (redundant with Test 1)
- [ ] Test 6: Performance is acceptable (< 5 seconds)
- [ ] Test 8: Area monotonically decreases then increases

## Success Criteria

The solution is correct if:
1. ✓ Output is a single integer
2. ✓ The value matches Part 1's alignment time
3. ✓ At this time, Part 1 would show "LRGPBHEZ"
4. ✓ The bounding box area is minimal at this time
5. ✓ Example input returns 3

## Known Limitations

Since this is a puzzle solution (not production code):
- No need for extensive input validation
- No need for handling malformed input gracefully
- No need for testing with random/fuzzy inputs
- No need for stress testing with millions of points
- Focus on correctness for the given input

## Final Verification

Once all tests pass, the final check:
```bash
# Run the solution
python solution.py input.md
# Take the output and verify it makes sense (likely 10000-20000 range)
# Cross-reference with Part 1 to ensure consistency
```
