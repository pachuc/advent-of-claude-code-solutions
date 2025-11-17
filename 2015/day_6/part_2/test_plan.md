# Testing Plan: Light Grid Brightness Control

## Testing Strategy Overview
Verify the solution through a combination of unit tests for individual components and integration tests for complete scenarios. Focus on correctness of operations, boundary conditions, and the provided input.

## Test Categories

### 1. Unit Tests: Instruction Parsing

#### Test 1.1: Parse "turn on" instruction
- **Input**: `"turn on 0,0 through 999,999"`
- **Expected**: `("turn on", 0, 0, 999, 999)`
- **Purpose**: Verify basic parsing of turn on command

#### Test 1.2: Parse "turn off" instruction
- **Input**: `"turn off 499,499 through 500,500"`
- **Expected**: `("turn off", 499, 499, 500, 500)`
- **Purpose**: Verify basic parsing of turn off command

#### Test 1.3: Parse "toggle" instruction
- **Input**: `"toggle 0,0 through 999,0"`
- **Expected**: `("toggle", 0, 0, 999, 0)`
- **Purpose**: Verify basic parsing of toggle command

#### Test 1.4: Handle invalid input
- **Input**: `"invalid instruction format"`
- **Expected**: `None` (function returns None for unparseable input)
- **Verification**: `assert parse_instruction("invalid instruction format") is None`
- **Purpose**: Ensure parser doesn't crash on malformed input

#### Test 1.5: Parse with varied coordinate ranges
- **Input**: `"turn on 887,9 through 959,629"` (from actual input)
- **Expected**: `("turn on", 887, 9, 959, 629)`
- **Purpose**: Verify parsing of real input coordinates

### 2. Unit Tests: Grid Operations

#### Test 2.1: Grid initialization
- **Action**: Create grid with `initialize_grid()`
- **Verification**:
  - Grid is 1000x1000 in size: `len(grid) == 1000 and len(grid[0]) == 1000`
  - All values are 0
  - `grid[0][0] == 0` (top-left)
  - `grid[999][999] == 0` (bottom-right)
  - Grid access pattern: `grid[row][column]` = `grid[y][x]`
- **Purpose**: Ensure grid starts in correct state

#### Test 2.2: Turn on single light
- **Setup**: Initialize grid with all zeros
- **Action**: `process_instruction(grid, "turn on", 0, 0, 0, 0)`
- **Expected**: `grid[0][0] == 1`, all others remain 0
- **Verification**: Total brightness = 1
- **Purpose**: Test basic turn on operation

#### Test 2.3: Turn on multiple times (brightness accumulation)
- **Setup**: Initialize grid with all zeros
- **Actions**:
  1. `process_instruction(grid, "turn on", 0, 0, 0, 0)`
  2. `process_instruction(grid, "turn on", 0, 0, 0, 0)`
  3. `process_instruction(grid, "turn on", 0, 0, 0, 0)`
- **Expected**: `grid[0][0] == 3`
- **Purpose**: Verify brightness increases, not just toggles to 1

#### Test 2.4: Turn off with brightness floor
- **Setup**: Initialize grid, set `grid[0][0] = 2`
- **Actions**:
  1. `process_instruction(grid, "turn off", 0, 0, 0, 0)` → should be 1
  2. `process_instruction(grid, "turn off", 0, 0, 0, 0)` → should be 0
  3. `process_instruction(grid, "turn off", 0, 0, 0, 0)` → should stay 0
- **Expected**: `grid[0][0] == 0` (never goes negative)
- **Purpose**: Verify brightness floor at 0

#### Test 2.5: Toggle operation
- **Setup**: Initialize grid with all zeros
- **Actions**:
  1. `process_instruction(grid, "toggle", 0, 0, 0, 0)`
  2. `process_instruction(grid, "toggle", 0, 0, 0, 0)`
- **Expected**: After first toggle: `grid[0][0] == 2`, after second: `grid[0][0] == 4`
- **Purpose**: Verify toggle adds 2 to brightness

#### Test 2.6: Rectangular region operation
- **Setup**: Initialize grid with all zeros
- **Action**: `process_instruction(grid, "turn on", 0, 0, 2, 2)`
- **Expected**:
  - 3x3 rectangle: (X,Y) from (0,0) to (2,2)
  - Access as grid[y][x]: grid[0][0], grid[0][1], grid[0][2], grid[1][0], grid[1][1], grid[1][2], grid[2][0], grid[2][1], grid[2][2]
  - All 9 positions have brightness 1
  - Total brightness: 9
- **Verification**: `calculate_total_brightness(grid) == 9`
- **Purpose**: Verify rectangular regions are processed correctly

#### Test 2.6b: Asymmetric region (coordinate system validation)
- **Setup**: Initialize grid with all zeros
- **Action**: `process_instruction(grid, "turn on", 0, 0, 3, 1)`
- **Expected**:
  - Rectangle from X=0 to X=3 (4 wide), Y=0 to Y=1 (2 tall)
  - 4 columns × 2 rows = 8 lights affected
  - Affected positions: grid[0][0], grid[0][1], grid[0][2], grid[0][3] (row 0)
                        grid[1][0], grid[1][1], grid[1][2], grid[1][3] (row 1)
  - Total brightness: 8
- **Verification**: `calculate_total_brightness(grid) == 8`
- **Purpose**: **CRITICAL** - Verify coordinate system is correct (X=column, Y=row)

#### Test 2.7: Inclusive boundary verification
- **Setup**: Initialize grid with all zeros
- **Action**: `process_instruction(grid, "turn on", 5, 5, 5, 5)`
- **Expected**: Only `grid[5][5] == 1`, exactly 1 light affected
- **Purpose**: Verify single-point region works (both coords are inclusive)

### 3. Integration Tests: Example Cases

#### Test 3.1: Problem example 1
- **Input**: `"turn on 0,0 through 0,0"`
- **Expected Output**: Total brightness = 1
- **Purpose**: Verify problem statement example

#### Test 3.2: Problem example 2
- **Input**: `"toggle 0,0 through 999,999"`
- **Expected Output**: Total brightness = 2,000,000 (1M lights × 2 brightness each)
- **Purpose**: Verify problem statement example and large region handling

#### Test 3.3: Sequential operations interaction
- **Instructions**:
  1. `"turn on 0,0 through 2,2"` → 3×3 grid, 9 lights at brightness 1 = 9 total
  2. `"toggle 1,1 through 3,3"` → 3×3 grid starting at (1,1)
     - Overlapping region (1,1) to (2,2): 4 lights go from 1→3 (add 8 brightness)
     - New region (3,1), (3,2), (1,3), (2,3), (3,3): 5 lights go from 0→2 (add 10 brightness)
     - Non-overlapping from step 1: 4 lights stay at 1
     - Subtotal after toggle: (4×3) + (5×2) + (4×1) = 12 + 10 + 4 = 26
  3. `"turn off 0,0 through 1,1"` → 2×2 grid
     - (0,0): 1→0 (decrease 1)
     - (1,0): 1→0 (decrease 1)
     - (0,1): 1→0 (decrease 1)
     - (1,1): 3→2 (decrease 1)
     - Total decrease: 4
- **Expected final brightness**: 26 - 4 = 22
- **Purpose**: Verify overlapping regions interact correctly
- **Verification**: `assert calculate_total_brightness(grid) == 22`

#### Test 3.4: Complex sequence with all operations
- **Instructions**:
  1. `"turn on 0,0 through 99,99"` → 100×100 = 10,000 lights at brightness 1 = 10,000 total
  2. `"toggle 50,50 through 149,149"` → 100×100 = 10,000 lights affected
     - Overlapping with step 1: (50,50) to (99,99) = 50×50 = 2,500 lights go from 1→3 (add 5,000)
     - New region: (100,50) to (149,149) and (50,100) to (99,149) = 10,000-2,500 = 7,500 lights go from 0→2 (add 15,000)
     - Non-overlapping from step 1: 10,000-2,500 = 7,500 lights stay at 1
     - Subtotal: (2,500×3) + (7,500×2) + (7,500×1) = 7,500 + 15,000 + 7,500 = 30,000
  3. `"turn off 75,75 through 124,124"` → 50×50 = 2,500 lights affected
     - Overlap with step 1&2: (75,75) to (99,99) = 25×25 = 625 lights go from 3→2 (decrease 625)
     - Overlap with step 2 only: (100,75) to (124,124) and (75,100) to (99,124) = 2,500-625 = 1,875 lights go from 2→1 (decrease 1,875)
     - Total decrease: 625 + 1,875 = 2,500
- **Expected final brightness**: 30,000 - 2,500 = 27,500
- **Purpose**: Test combination of all three operations
- **Verification**: `assert calculate_total_brightness(grid) == 27500`

### 4. Edge Case Tests

#### Test 4.1: Full grid turn on
- **Action**: `"turn on 0,0 through 999,999"`
- **Expected**: All 1,000,000 lights have brightness 1
- **Total brightness**: 1,000,000
- **Purpose**: Test maximum single region size

#### Test 4.2: Multiple operations on same cell
- **Setup**: Start with brightness 0 at (500, 500)
- **Actions**:
  1. Turn on × 5 → brightness = 5
  2. Toggle × 3 → brightness = 11
  3. Turn off × 20 → brightness = 0 (floor)
- **Expected**: Final brightness at (500, 500) = 0
- **Purpose**: Verify floor works with multiple decrements

#### Test 4.3: Corner coordinates
- **Actions**:
  - `"turn on 0,0 through 0,0"` → grid[0][0] = 1 (X=0, Y=0)
  - `"turn on 999,999 through 999,999"` → grid[999][999] = 1 (X=999, Y=999)
  - `"turn on 999,0 through 999,0"` → grid[0][999] = 1 (X=999, Y=0)
  - `"turn on 0,999 through 0,999"` → grid[999][0] = 1 (X=0, Y=999)
- **Expected**: Total brightness = 4
- **Purpose**: Verify all grid corners are accessible

#### Test 4.3b: Maximum coordinate boundary
- **Setup**: Initialize grid with all zeros
- **Action**: `"turn on 998,998 through 999,999"`
- **Expected**:
  - 2×2 rectangle at maximum coordinates
  - grid[998][998] = 1, grid[998][999] = 1, grid[999][998] = 1, grid[999][999] = 1
  - Total brightness: 4
- **Verification**: `assert calculate_total_brightness(grid) == 4`
- **Purpose**: Verify no off-by-one errors at grid boundaries

#### Test 4.4: Single row/column
- **Action**: `"turn on 0,0 through 999,0"` (entire top row)
- **Expected**: 1,000 lights at brightness 1 = 1,000 total
- **Purpose**: Verify row operations work correctly

#### Test 4.5: Order dependency
- **Sequence A**:
  1. Turn on (0,0) through (10,10)
  2. Turn off (0,0) through (10,10)
- **Sequence B**:
  1. Turn off (0,0) through (10,10)
  2. Turn on (0,0) through (10,10)
- **Expected**: Sequence A results in 0 total, Sequence B results in 121 total
- **Purpose**: Verify operations are order-dependent

### 5. Actual Input Test

#### Test 5.1: Full input file processing
- **Input**: Complete `input.md` file (300 instructions)
- **Process**: Run full solution
- **Verification Steps**:
  1. Confirm no parsing errors (all 300 lines processed)
  2. Confirm no runtime errors during execution
  3. Verify output is a positive integer
  4. Check runtime is reasonable (< 10 seconds)
  5. Record final answer for submission

#### Test 5.2: Instruction count verification
- **Check**: Number of successfully parsed instructions = 300
- **Purpose**: Ensure no instructions are silently skipped

#### Test 5.3: Grid state sanity check
- **After processing**: Verify no brightness values are negative
- **Method**: Check `min(min(row) for row in grid) >= 0`
- **Purpose**: Ensure floor constraint is maintained throughout

### 6. Performance Tests

#### Test 6.1: Runtime measurement
- **Action**: Measure time to process full input
- **Expected**: < 10 seconds (ideally < 1 second)
- **Purpose**: Verify solution is efficient enough

#### Test 6.2: Memory usage
- **Check**: Solution doesn't exceed reasonable memory limits
- **Expected**: < 100MB
- **Purpose**: Ensure solution is memory-efficient

### 7. Regression Tests

#### Test 7.1: Known output validation
- **Approach**: If we submit and get correct answer, save it
- **Purpose**: Prevent future code changes from breaking solution
- **Format**: `assert solve(input_file) == KNOWN_CORRECT_ANSWER`

## Test Execution Order

1. **Unit tests first**: Parsing → Grid initialization → Individual operations
2. **Integration tests**: Simple examples → Complex sequences
3. **Edge cases**: Boundaries, floors, extremes
4. **Actual input**: Final validation
5. **Performance**: Timing and resource checks

## Manual Verification Strategy

For the actual input, manually verify a subset of instructions:
1. Pick first 3 instructions
2. Calculate expected brightness changes by hand
3. Add print statements to show brightness after each instruction
4. Compare manual calculation with code output

## Success Criteria

✓ All unit tests pass
✓ All integration tests pass
✓ All edge cases handled correctly
✓ Full input processes without errors
✓ Runtime < 10 seconds
✓ No negative brightness values in final grid
✓ Output is a reasonable positive integer (likely in millions range)

## Debugging Strategy

If tests fail:
1. **Parsing issues**: Print parsed instructions, verify format
2. **Operation issues**: Add logging to show grid state after each operation
3. **Boundary issues**: Test with small 5x5 grid and visualize changes
4. **Performance issues**: Profile code to find bottlenecks
5. **Logic issues**: Step through example with debugger

## Test Implementation

Create a separate `test_solution.py` file with:
```python
import unittest
from solution import (parse_instruction, initialize_grid,
                      process_instruction, calculate_total_brightness)

class TestLightGrid(unittest.TestCase):
    # Implement all test cases above

    def test_coordinate_system(self):
        """Critical test to verify X,Y coordinate mapping"""
        grid = initialize_grid()
        # X=5 (column), Y=3 (row) should map to grid[3][5]
        process_instruction(grid, "turn on", 5, 3, 5, 3)
        self.assertEqual(grid[3][5], 1)
        self.assertEqual(grid[5][3], 0)  # Wrong indexing would set this

if __name__ == '__main__':
    unittest.main()
```

Alternative: Use assertions in main code with a `--test` flag for quick validation.
