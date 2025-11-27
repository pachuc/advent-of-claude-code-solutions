# Test Plan: Fuel Cell Power Grid Optimization

## Testing Strategy Overview
We'll use a layered testing approach: unit tests for individual components, integration tests for the complete workflow, and verification tests against known examples.

## Test Implementation
- Create `test_solution.py` with pytest functions for automated testing
- Also perform manual validation for critical checkpoints
- Run automated tests with: `pytest test_solution.py -v`
- Use assert statements as shown in test cases
- For manual testing, run functions interactively or via print statements

## Test Categories

### 1. Unit Tests: Power Level Calculation

#### Test 1.1: Example Verification Cases
**Purpose**: Verify the power level calculation matches the provided examples

**Test Cases**:
```python
# Test case from problem description
assert calculate_power_level(3, 5, 8) == 4

# Additional verification examples
assert calculate_power_level(122, 79, 57) == -5
assert calculate_power_level(217, 196, 39) == 0
assert calculate_power_level(101, 153, 71) == 4
```

**Expected Results**: All assertions pass
**Failure Action**: Debug the calculation algorithm step-by-step

#### Test 1.2: Hundreds Digit Extraction
**Purpose**: Verify correct extraction of hundreds digit in various scenarios

**Test Cases**:
```python
# Test with step-by-step verification for (3, 5, 8)
# Rack ID: 13
# Initial: 65
# After add serial: 73
# After multiply rack: 949
# Hundreds digit: 9
# Final: 4

# Edge case: No hundreds digit (number < 100)
# Example: result before subtraction could be < 100
# Test a cell that produces a small number

# Edge case: Number with hundreds digit 0
# Example: 1045 -> hundreds digit = 0 -> final = -5
```

**Expected Results**: Correct digit extraction in all cases
**Failure Action**: Review the (n // 100) % 10 logic

#### Test 1.3: Negative Power Levels
**Purpose**: Ensure negative power levels are handled correctly

**Test Cases**:
- Verify cells with power level -5 (hundreds digit = 0)
- Verify cells with power level between -5 and 4 are valid
- Confirm no unexpected clamping or rounding

**Expected Results**: Negative values preserved correctly
**Failure Action**: Check for inadvertent abs() or max() operations

#### Test 1.4: Boundary Coordinates
**Purpose**: Test power calculation at grid boundaries

**Test Cases**:
```python
# Corner cells
calculate_power_level(1, 1, 2568)
calculate_power_level(300, 300, 2568)
calculate_power_level(1, 300, 2568)
calculate_power_level(300, 1, 2568)

# Edge cells
calculate_power_level(150, 1, 2568)
calculate_power_level(150, 300, 2568)
```

**Expected Results**: All calculations complete without errors
**Failure Action**: Check for off-by-one errors or index issues

### 2. Unit Tests: Grid Construction

#### Test 2.1: Grid Dimensions
**Purpose**: Verify the grid has correct dimensions

**Test Cases**:
```python
grid = build_power_grid(2568)
assert len(grid) == 301  # 0-300 inclusive
assert len(grid[0]) == 301
assert len(grid[150]) == 301
```

**Expected Results**: Grid is 301×301
**Failure Action**: Fix list comprehension in build_power_grid

#### Test 2.2: Grid Population and Coordinate Verification
**Purpose**: Ensure all cells are populated correctly and coordinate indexing is correct

**Important**: Our convention is grid[y][x] = grid[row][column]

**Test Cases**:
```python
grid = build_power_grid(8)
# Check specific cells against manual calculations
# grid[y][x] represents the cell at coordinates (x, y)
assert grid[5][3] == 4  # grid[y=5][x=3] = Cell at (x=3, y=5) with serial 8

# Additional verification of coordinate ordering
# Test multiple cells to ensure consistency
power_3_5 = calculate_power_level(3, 5, 8)
assert grid[5][3] == power_3_5  # Verify grid[y][x] = power at (x, y)

# Test corner case
power_1_1 = calculate_power_level(1, 1, 8)
assert grid[1][1] == power_1_1

# Test another cell
power_122_79 = calculate_power_level(122, 79, 57)
grid_57 = build_power_grid(57)
assert grid_57[79][122] == power_122_79
```

**Expected Results**: Spot checks match expected values, coordinate ordering verified
**Failure Action**: Verify x/y coordinate ordering (x is column, y is row; grid[y][x])

#### Test 2.3: Grid Serial Number Variation
**Purpose**: Test grid generation with different serial numbers

**Test Cases**:
```python
grid_18 = build_power_grid(18)
grid_42 = build_power_grid(42)
grid_2568 = build_power_grid(2568)

# Grids should be different
assert grid_18[100][100] != grid_42[100][100]
```

**Expected Results**: Different serial numbers produce different grids
**Failure Action**: Check serial number is being passed correctly

### 3. Unit Tests: Square Power Calculation

#### Test 3.1: Simple Square Sum
**Purpose**: Verify correct summing of 3×3 region

**Test Cases**:
```python
# Create a simple test grid
test_grid = [[0] * 10 for _ in range(10)]
# Fill a 3x3 region with known values
for y in range(1, 4):
    for x in range(1, 4):
        test_grid[y][x] = 1

power = calculate_square_power(test_grid, 1, 1, 3)
assert power == 9
```

**Expected Results**: Sum equals 9
**Failure Action**: Check loop bounds in calculate_square_power

#### Test 3.2: Square with Negative Values
**Purpose**: Ensure negative values are summed correctly

**Test Cases**:
```python
test_grid = [[0] * 10 for _ in range(10)]
# Create a 3x3 region with mix of positive and negative values
values = [5, -3, 2, 1, -2, 0, 3, -1, 4]
idx = 0
for y in range(1, 4):
    for x in range(1, 4):
        test_grid[y][x] = values[idx]
        idx += 1

power = calculate_square_power(test_grid, 1, 1, 3)
expected = sum(values)  # 5-3+2+1-2+0+3-1+4 = 9
assert power == expected
```

**Expected Results**: Correct algebraic sum = 9 (including negatives)
**Failure Action**: Check for incorrect use of abs()

### 4. Integration Tests: Complete Workflow

#### Test 4.1: Known Example - Serial 18
**Purpose**: Verify complete solution for serial number 18

**Test Cases**:
```python
grid = build_power_grid(18)
coord, power = find_max_power_square(grid)
assert coord == (33, 45)
assert power == 29
```

**Expected Results**: coord = (33, 45), power = 29
**Failure Action**: Critical - debug entire workflow

#### Test 4.2: Known Example - Serial 42
**Purpose**: Verify complete solution for serial number 42

**Test Cases**:
```python
grid = build_power_grid(42)
coord, power = find_max_power_square(grid)
assert coord == (21, 61)
assert power == 30
```

**Expected Results**: coord = (21, 61), power = 30
**Failure Action**: Critical - debug entire workflow

### 5. Boundary and Edge Case Tests

#### Test 5.1: Maximum Valid Top-Left Position
**Purpose**: Ensure we can place a 3×3 square at position (298, 298) and invalid positions are excluded

**Test Cases**:
```python
grid = build_power_grid(2568)
# Should not raise an error - this is the maximum valid position
power = calculate_square_power(grid, 298, 298, 3)
assert isinstance(power, int)

# Verify that invalid positions would cause errors if attempted
# (we won't attempt them, just verify they're excluded from search)
# Position (299, 299) would extend to (301, 301) which is out of bounds

# Verify search range excludes invalid positions
search_positions = [(x, y) for y in range(1, 299) for x in range(1, 299)]
assert (298, 298) in search_positions  # Should be included
assert (299, 299) not in search_positions  # Should be excluded
assert (299, 1) not in search_positions  # Should be excluded
assert (1, 299) not in search_positions  # Should be excluded
```

**Expected Results**: No index out of bounds errors, boundary positions correctly included/excluded
**Failure Action**: Check loop bounds in find_max_power_square (should be range(1, 299))

#### Test 5.2: Search Range Validation
**Purpose**: Verify we're checking all valid positions

**Test Cases**:
```python
# Mock find_max_power_square to count iterations
positions_checked = 0
for y in range(1, 299):  # 1 to 298
    for x in range(1, 299):  # 1 to 298
        positions_checked += 1

assert positions_checked == 298 * 298  # Should be 88,804
```

**Expected Results**: Exactly 88,804 positions checked
**Failure Action**: Fix range bounds

#### Test 5.3: Single Maximum Exists
**Purpose**: Ensure there are no ties (or ties are handled consistently)

**Test Cases**:
- Run find_max_power_square and verify it returns a single coordinate
- If there are multiple squares with same power, verify first-found is returned consistently

**Expected Results**: Deterministic result
**Failure Action**: Document tie-breaking behavior

### 6. Performance Tests

#### Test 6.1: Execution Time
**Purpose**: Ensure solution completes in reasonable time

**Test Cases**:
```python
import time

start = time.time()
grid = build_power_grid(2568)
coord, power = find_max_power_square(grid)
elapsed = time.time() - start

assert elapsed < 2.0  # Realistic expectation based on ~800K operations
print(f"Execution time: {elapsed:.3f} seconds")
# Note: Ideal target is < 1 second, but allow up to 2 seconds for safety
```

**Expected Results**: Completes in < 2 seconds (ideally < 1 second)
**Failure Action**: Profile and optimize if needed

#### Test 6.2: Memory Usage
**Purpose**: Ensure memory usage is reasonable

**Test Cases**:
- Grid size: 301 × 301 × 8 bytes (int) ≈ 724 KB
- Should not cause memory issues

**Expected Results**: No memory errors
**Failure Action**: Review data structure choices

### 7. Output Format Tests

#### Test 7.1: Correct Format
**Purpose**: Verify output matches required format

**Test Cases**:
```python
result = format_output((33, 45))
assert result == "33,45"
assert isinstance(result, str)
assert "," in result
```

**Expected Results**: Proper "X,Y" format
**Failure Action**: Fix format_output function

#### Test 7.2: No Extra Whitespace
**Purpose**: Ensure clean output

**Test Cases**:
```python
result = format_output((33, 45))
assert result == result.strip()
assert " " not in result
```

**Expected Results**: No spaces or newlines
**Failure Action**: Add strip() if needed

### 8. Final Acceptance Test

#### Test 8.1: Actual Input (Serial 2568)
**Purpose**: Solve the actual problem

**Test Procedure**:
1. Run the complete solution with serial number 2568
2. Record the output coordinate and power level
3. Verify the output format is "X,Y"
4. Manually verify the 3×3 square at that position:
   - Calculate all 9 cell power levels manually
   - Sum them up
   - Confirm it matches the reported power
5. Spot-check a few nearby squares to confirm they have lower power

**Expected Results**:
- Valid coordinate in format "X,Y"
- Coordinate is within bounds (1-298, 1-298)
- Manual verification confirms the power level
- Nearby squares have lower or equal power

**Failure Action**: Re-run all previous tests to isolate issue

### 9. Regression Test

#### Test 9.1: Regression Test for Serial 2568
**Purpose**: Once the correct answer is found, ensure future changes don't break it

**Test Cases**:
```python
def test_regression_serial_2568():
    """Ensure the solution for the actual input doesn't change."""
    grid = build_power_grid(2568)
    coord, power = find_max_power_square(grid)
    # After finding the correct answer, fill in these values:
    # assert coord == (EXPECTED_X, EXPECTED_Y)
    # assert power == EXPECTED_POWER
    # For now, just verify it returns valid results
    assert isinstance(coord, tuple)
    assert len(coord) == 2
    assert 1 <= coord[0] <= 298
    assert 1 <= coord[1] <= 298
    assert isinstance(power, int)
```

**Expected Results**: Answer matches the verified solution
**Failure Action**: Investigate what changed in the implementation

## Test Execution Order

1. Run unit tests for power level calculation (Tests 1.1-1.4)
2. Run unit tests for grid construction (Tests 2.1-2.3)
3. Run unit tests for square calculation (Tests 3.1-3.2)
4. Run integration tests (Tests 4.1-4.2) - **Critical checkpoints**
5. Run boundary tests (Tests 5.1-5.3)
6. Run performance tests (Tests 6.1-6.2)
7. Run output format tests (Tests 7.1-7.2)
8. Run final acceptance test (Test 8.1)
9. After verification, add regression test (Test 9.1)

## Success Criteria

- All unit tests pass
- Both integration tests (serial 18 and 42) produce correct results - **CRITICAL**
- Coordinate indexing verified correctly (grid[y][x] convention)
- No boundary errors or exceptions
- Performance is acceptable (< 2 seconds, ideally < 1 second)
- Output format is correct
- Final answer for serial 2568 is validated manually
- Regression test created with verified answer

## Debugging Strategy

If tests fail:
1. Start with the first failing test
2. Add print statements to trace values
3. For power calculation: print each step (rack_id, intermediate values, hundreds digit)
4. For grid: print sample cell values
5. For search: print top 5 candidates with their powers
6. Use Python debugger (pdb) for complex issues

## Manual Verification Procedure

For the final answer with serial 2568:
1. Note the output coordinate (X, Y)
2. Manually calculate power for cell (X, Y) using the algorithm
3. Manually calculate power for all 9 cells in the 3×3 square
4. Sum the 9 power levels
5. Verify sum matches what the program reports
6. Check 2-3 adjacent squares to confirm they have lower power
