# Test Plan: Fuel Cell Power Grid - Part 2

## Testing Objectives
1. Verify correctness of summed-area table implementation
2. Confirm that the algorithm finds the correct maximum across all sizes
3. Validate against known examples and Part 1 results
4. Ensure edge cases are handled properly
5. Verify acceptable runtime performance

## Test Strategy
Since this is a script to solve a specific puzzle (not production code), we focus on:
- Correctness verification using provided examples
- Edge case validation for algorithm robustness
- Cross-validation with Part 1 results
- Basic performance checks

---

## Unit Tests

### Test 1: Power Level Calculation (Reuse from Part 1)
**Purpose**: Verify the fundamental power calculation is correct

**Test Cases**:
```python
assert calculate_power_level(3, 5, 8) == 4
assert calculate_power_level(122, 79, 57) == -5
assert calculate_power_level(217, 196, 39) == 0
assert calculate_power_level(101, 153, 71) == 4
```

**Expected**: All assertions pass
**Rationale**: These are the examples from the problem statement

---

### Test 2: Summed-Area Table Construction
**Purpose**: Verify SAT is built correctly

**Test Case - Small Grid**:
```python
# Create a simple 3x3 grid for manual verification
test_grid = [
    [0, 0, 0, 0],  # padding row
    [0, 1, 2, 3],  # row 1
    [0, 4, 5, 6],  # row 2
    [0, 7, 8, 9]   # row 3
]

sat = build_summed_area_table(test_grid, 3)

# Verify SAT values (cumulative sums from (1,1))
assert sat[1][1] == 1              # just cell (1,1)
assert sat[1][3] == 1+2+3 == 6     # top row
assert sat[2][2] == 1+2+4+5 == 12  # 2x2 square
assert sat[3][3] == 1+2+3+4+5+6+7+8+9 == 45  # entire 3x3
```

**Expected**: All assertions pass
**Rationale**: Validates the core SAT building logic with manually calculated values

---

### Test 3: Square Sum Retrieval Using SAT
**Purpose**: Verify that square sums are calculated correctly from SAT

**Test Cases Using Test Grid from Test 2**:
```python
# Using the same 3x3 test grid and SAT from above

# 1x1 squares
assert get_square_sum(sat, 1, 1, 1) == 1
assert get_square_sum(sat, 3, 3, 1) == 9

# 2x2 squares
assert get_square_sum(sat, 1, 1, 2) == 1+2+4+5 == 12
assert get_square_sum(sat, 2, 2, 2) == 5+6+8+9 == 28

# 3x3 square
assert get_square_sum(sat, 1, 1, 3) == 45

# Additional test: uniform grid to validate overlap correction
# This test catches if the +SAT[y-1][x-1] term is missing
uniform_grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
]
uniform_sat = build_summed_area_table(uniform_grid, 4)

# For uniform grid of 1s, a KxK square should sum to K*K
assert get_square_sum(uniform_sat, 1, 1, 4) == 16  # 4x4 = 16
assert get_square_sum(uniform_sat, 2, 2, 3) == 9   # 3x3 = 9
assert get_square_sum(uniform_sat, 2, 2, 2) == 4   # 2x2 = 4
assert get_square_sum(uniform_sat, 3, 3, 2) == 4   # 2x2 = 4
```

**Expected**: All assertions pass
**Rationale**: Validates the SAT lookup formula works for various positions and sizes, including the critical overlap correction term

---

### Test 4: Boundary Conditions
**Purpose**: Ensure algorithm handles grid boundaries correctly

**Test Cases**:
```python
# With actual grid (300x300)
grid = build_power_grid(2568)
sat = build_summed_area_table(grid)

# Size 1 at corner positions
power_1_1 = get_square_sum(sat, 1, 1, 1)
power_300_300 = get_square_sum(sat, 300, 300, 1)
assert power_1_1 == grid[1][1]
assert power_300_300 == grid[300][300]

# Size 300 (entire grid) - only valid position is (1,1)
entire_grid_sum = get_square_sum(sat, 1, 1, 300)
assert entire_grid_sum == sat[300][300]

# Large square near edge - should fit exactly
power_bottom_right = get_square_sum(sat, 299, 299, 2)  # 2x2 at position (299,299)
# Should not crash and should return valid value
assert isinstance(power_bottom_right, int)
```

**Expected**: All assertions pass, no index errors
**Rationale**: Validates edge positions don't cause crashes or incorrect calculations

---

## Integration Tests

### Test 5: Validate Against Provided Examples
**Purpose**: Verify complete algorithm against known correct answers

**Test Case 1: Serial Number 18**
```python
serial = 18
grid = build_power_grid(serial)
sat = build_summed_area_table(grid)
coord, power = find_max_power_square_any_size(sat)

assert coord == (90, 269, 16)
assert power == 113  # Total power as stated in problem
assert format_output(coord) == "90,269,16"
```

**Test Case 2: Serial Number 42**
```python
serial = 42
grid = build_power_grid(serial)
sat = build_summed_area_table(grid)
coord, power = find_max_power_square_any_size(sat)

assert coord == (232, 251, 12)
assert power == 119  # Total power as stated in problem
assert format_output(coord) == "232,251,12"
```

**Expected**: All assertions pass
**Rationale**: These are the exact examples from the problem statement

---

### Test 6: Cross-Validation with Part 1 Answer
**Purpose**: Ensure Part 2 algorithm is backward compatible and finds Part 1's answer when checking size 3

**Test Case**:
```python
serial = 2568  # Our actual input
grid = build_power_grid(serial)
sat = build_summed_area_table(grid)

# Find best 3x3 square specifically
max_power_3x3 = float('-inf')
best_coord_3x3 = None

for y in range(1, 299):  # 1 to 298
    for x in range(1, 299):
        power = get_square_sum(sat, x, y, 3)
        if power > max_power_3x3:
            max_power_3x3 = power
            best_coord_3x3 = (x, y)

# Should match Part 1 answer
assert best_coord_3x3 == (21, 68)
```

**Expected**: Assertion passes
**Rationale**: Part 1 found that (21,68) is the best 3x3 square. Our Part 2 algorithm should agree when checking size=3. This is a strong validation that our SAT implementation is correct.

---

### Test 7: Monotonicity Check (Sanity)
**Purpose**: Verify that maximum power for size S+1 can be less than or equal to size S (not always greater)

**Test Case**:
```python
serial = 2568
grid = build_power_grid(serial)
sat = build_summed_area_table(grid)

# Find max power for different sizes
max_powers_by_size = {}
for size in [1, 3, 10, 50, 100, 200, 300]:
    max_p = float('-inf')
    for y in range(1, 302 - size):
        for x in range(1, 302 - size):
            power = get_square_sum(sat, x, y, size)
            max_p = max(max_p, power)
    max_powers_by_size[size] = max_p

# Power doesn't always increase with size (cells can be negative)
# This is expected behavior - just verify we get reasonable values
for size, power in max_powers_by_size.items():
    assert isinstance(power, int)
    assert power != float('-inf')  # We found something
```

**Expected**: All sizes return valid integer powers
**Rationale**: Since power levels can be negative, larger squares don't always have more power. This verifies we're searching correctly and getting reasonable results.

---

## Edge Cases

### Test 8: Minimum and Maximum Sizes
**Purpose**: Verify algorithm handles extreme sizes correctly

**Test Case 1: Size 1 (Individual Cells)**
```python
grid = build_power_grid(2568)
sat = build_summed_area_table(grid)

# Find best 1x1 "square"
max_power_1x1 = float('-inf')
best_1x1 = None

for y in range(1, 301):
    for x in range(1, 301):
        power = get_square_sum(sat, x, y, 1)
        if power > max_power_1x1:
            max_power_1x1 = power
            best_1x1 = (x, y)

# Should equal max value in grid (power level is -5 to 4)
assert max_power_1x1 <= 4  # Maximum possible power level
assert max_power_1x1 >= -5  # Minimum possible power level
```

**Test Case 2: Size 300 (Entire Grid)**
```python
# Only one 300x300 square exists: starting at (1,1)
power_entire = get_square_sum(sat, 1, 1, 300)

# Should equal the sum of all cells
assert power_entire == sat[300][300]

# This is unlikely to be the maximum (too many negative cells)
# Just verify it's a valid value
assert isinstance(power_entire, int)
```

**Expected**: Both edge sizes work without errors
**Rationale**: Size 1 and 300 are the extremes of the range

---

### Test 9: Verify All Sizes Are Checked
**Purpose**: Ensure the search doesn't skip any sizes

**Test Case**:
```python
# Run the full search and capture which size wins
serial = 2568
grid = build_power_grid(serial)
sat = build_summed_area_table(grid)
coord, power = find_max_power_square_any_size(sat)

# The winning size should be in valid range
x, y, size = coord
assert 1 <= size <= 300
assert 1 <= x <= 301 - size
assert 1 <= y <= 301 - size

# Verify this is actually the maximum by spot-checking nearby sizes
# (not exhaustive, but catches major bugs)
test_sizes = [size - 1, size, size + 1]
test_sizes = [s for s in test_sizes if 1 <= s <= 300]

for test_size in test_sizes:
    test_power = get_square_sum(sat, x, y, test_size)
    if test_size == size:
        assert test_power == power
    # Note: Adjacent sizes might have higher power at different locations
    # We're just checking the value at the winning location
```

**Expected**: Winning square has valid size and coordinates
**Rationale**: Basic sanity check on output

---

## Performance Tests

### Test 10: Runtime Performance
**Purpose**: Verify solution completes in reasonable time

**Test Case**:
```python
import time

serial = 2568
start_time = time.time()

grid = build_power_grid(serial)
sat = build_summed_area_table(grid)
coord, power = find_max_power_square_any_size(sat)

elapsed = time.time() - start_time

# Should complete in under 15 seconds (with SAT, should be 2-5s on modern hardware)
assert elapsed < 15, f"Runtime {elapsed:.2f}s exceeds 15s limit"

# Performance feedback
if elapsed < 5:
    print(f"✓ Excellent performance: {elapsed:.2f}s")
elif elapsed < 10:
    print(f"✓ Good performance: {elapsed:.2f}s")
else:
    print(f"⚠ Acceptable but slow: {elapsed:.2f}s")
```

**Expected**: Completes in under 15 seconds (ideally under 5)
**Rationale**: The O(n³) algorithm with SAT should be very fast (2-5s on modern hardware). A 15s limit catches major performance bugs while allowing for slower machines.

---

### Test 11: Memory Usage (Informal)
**Purpose**: Verify memory usage is reasonable

**Test Case**:
```python
import sys

grid = build_power_grid(2568)
sat = build_summed_area_table(grid)

# Check sizes are reasonable
grid_size = sys.getsizeof(grid) + sum(sys.getsizeof(row) for row in grid)
sat_size = sys.getsizeof(sat) + sum(sys.getsizeof(row) for row in sat)

# Both should be under 5 MB (actually ~360 KB each)
assert grid_size < 5 * 1024 * 1024
assert sat_size < 5 * 1024 * 1024

print(f"Grid size: {grid_size / 1024:.1f} KB")
print(f"SAT size: {sat_size / 1024:.1f} KB")
```

**Expected**: Both structures under 5 MB
**Rationale**: Ensures we're not using excessive memory

---

## Final Validation Test

### Test 12: Complete End-to-End Test with Actual Input
**Purpose**: Run the complete solution on actual input and verify format

**Test Case**:
```python
# Run main() with actual input
result = main()

# Verify format: "X,Y,size"
parts = result.split(',')
assert len(parts) == 3

x, y, size = map(int, parts)
assert 1 <= x <= 300
assert 1 <= y <= 300
assert 1 <= size <= 300
assert x + size - 1 <= 300  # Square fits horizontally
assert y + size - 1 <= 300  # Square fits vertically

print(f"✓ Solution for serial 2568: {result}")
```

**Expected**: Valid output in correct format
**Rationale**: Final check that everything works together

---

## Test Execution Plan

### Phase 1: Unit Tests (Run First)
1. Test 1: Power level calculation
2. Test 2: SAT construction
3. Test 3: Square sum retrieval
4. Test 4: Boundary conditions

**Purpose**: Catch basic implementation errors early

### Phase 2: Integration Tests (Run Second)
1. Test 5: Validate against examples (serial 18 and 42)
2. Test 6: Cross-validate with Part 1 answer
3. Test 7: Monotonicity sanity check

**Purpose**: Verify algorithm correctness

### Phase 3: Edge Cases (Run Third)
1. Test 8: Min/max sizes
2. Test 9: Verify all sizes checked

**Purpose**: Ensure robustness

### Phase 4: Performance & Final (Run Last)
1. Test 10: Runtime performance
2. Test 11: Memory usage
3. Test 12: End-to-end with actual input

**Purpose**: Confirm solution is ready for submission

---

## Success Criteria

### Must Pass (Critical)
- ✓ Test 5: Both provided examples (serial 18 and 42) produce correct answers
- ✓ Test 6: Finds same 3x3 square as Part 1 for size=3
- ✓ Test 12: Produces valid output for actual input (serial 2568)

### Should Pass (Important)
- ✓ Tests 1-4: All unit tests pass
- ✓ Test 10: Completes in under 30 seconds

### Nice to Have (Optional)
- ✓ Test 10: Completes in under 10 seconds
- ✓ Test 11: Memory usage is minimal

---

## Debugging Strategy (If Tests Fail)

### If SAT tests fail (Tests 2-3):
1. Print SAT values for small grid and compare manually
2. Check boundary conditions (y-1, x-1 when y=1 or x=1)
3. Verify grid indexing matches expected coordinate system

### If example tests fail (Test 5):
1. Print the actual best square found for each size
2. Check if the expected square has the claimed power value
3. Verify the SAT formula is correct (check signs)

### If Part 1 cross-validation fails (Test 6):
1. Print top 10 best 3x3 squares
2. Manually calculate power at (21,68) for size 3
3. Verify grid building is identical to Part 1

### If performance is too slow (Test 10):
1. Profile the code to find bottleneck
2. Verify using SAT (O(1) lookup), not recalculating sums
3. Check for unnecessary operations in inner loop

---

## Manual Verification Steps

After all automated tests pass:

1. **Visual inspection**: Print the winning square's details
   ```
   X: <x>, Y: <y>, Size: <size>, Power: <power>
   ```

2. **Reasonableness check**:
   - Size is typically in range 10-20 for these problems
   - Power should be positive and substantial (> 50)
   - Coordinates should not be at extreme edges

3. **Rerun with fresh script**: Execute from command line to ensure reproducibility
   ```bash
   python part_2_solution.py
   ```

4. **Compare with community** (if available): Check if answer is in expected range
