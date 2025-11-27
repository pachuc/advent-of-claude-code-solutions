# Implementation Summary: Fuel Cell Power Grid Optimization

## Problem Overview
Find the 3x3 square of fuel cells with the largest total power in a 300x300 grid, where each cell's power level is calculated using a specific algorithm based on its coordinates and a grid serial number (2568).

## Solution Approach
Implemented a brute-force approach with precomputed grid:
1. Calculate power levels for all 90,000 cells (300x300 grid)
2. Check all 88,804 possible 3x3 windows (298x298 valid positions)
3. Track and return the position with maximum total power

## Files Created
- `solution.py` - Complete implementation with the following functions:
  - `read_input()` - Reads grid serial number from input.md
  - `calculate_power_level(x, y, serial_number)` - Calculates power for a single cell
  - `build_power_grid(serial_number, grid_size)` - Builds the complete 300x300 power grid
  - `calculate_square_power(grid, top_left_x, top_left_y, size)` - Calculates total power of a square region
  - `find_max_power_square(grid, grid_size, square_size)` - Finds the 3x3 square with maximum power
  - `format_output(coord)` - Formats the result as "X,Y"
  - `main()` - Orchestrates the entire solution

## Implementation Details

### Power Level Calculation Algorithm
For each cell at coordinates (X, Y):
1. Calculate rack_id = X + 10
2. Initialize power_level = rack_id × Y
3. Add serial_number to power_level
4. Multiply power_level by rack_id
5. Extract hundreds digit: (power_level // 100) % 10
6. Subtract 5 from the result

### Grid Indexing Convention
Used grid[y][x] convention where:
- First index (y) represents the row (y-coordinate)
- Second index (x) represents the column (x-coordinate)
- Grid size: 301x301 (indices 0-300, with index 0 unused for cleaner 1-based indexing)

### Performance Characteristics
- Time Complexity: O(N²) for grid computation + O((N-2)² × 9) for window scanning ≈ O(890,000) operations
- Space Complexity: O(N²) = O(90,000) integers
- Actual runtime: < 1 second on modern hardware

## Testing Process

### Unit Tests
1. **Power Level Calculation Tests** - All PASSED
   - Test 1: calculate_power_level(3, 5, 8) = 4 ✓
   - Test 2: calculate_power_level(122, 79, 57) = -5 ✓
   - Test 3: calculate_power_level(217, 196, 39) = 0 ✓
   - Test 4: calculate_power_level(101, 153, 71) = 4 ✓

### Integration Tests
2. **Complete Solution with Known Examples** - All PASSED
   - Serial number 18: Result = 33,45, Power = 29 ✓ (Expected: 33,45 with power 29)
   - Serial number 42: Result = 21,61, Power = 30 ✓ (Expected: 21,61 with power 30)

### Acceptance Test
3. **Actual Input (Serial 2568)** - PASSED
   - **Result: 21,68**
   - Total power: 29

   Individual cell powers in the 3x3 square:
   ```
   4  3  2
   4  3  3
   3  3  4
   ```
   Sum: 29

### Manual Verification
- Calculated individual power levels for all 9 cells in the winning square
- Verified sum equals 29
- Checked 8 adjacent 3x3 squares - all had lower power levels:
  - Square at (20,67): power = 11
  - Square at (21,67): power = 27
  - Square at (22,67): power = 16
  - Square at (20,68): power = 8
  - Square at (22,68): power = 14
  - Square at (20,69): power = 14
  - Square at (21,69): power = 21
  - Square at (22,69): power = 1

## Final Answer
**21,68**

The 3x3 square with the top-left corner at coordinates (21, 68) has the maximum total power of 29 for grid serial number 2568.

## Testing Outcome
All tests passed successfully:
- ✓ Power level calculation accuracy verified with 4 test cases
- ✓ Grid construction and coordinate indexing verified
- ✓ Complete solution validated against 2 known examples
- ✓ Final answer verified through manual calculation
- ✓ Neighboring squares confirmed to have lower power

The solution is correct and efficient, completing in well under 1 second.
