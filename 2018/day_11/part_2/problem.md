# Problem Report: Fuel Cell Power Grid Optimization - Part 2

## Objective
Find the square of **any size** (from 1x1 to 300x300) with the largest total power in a 300x300 grid, and identify it including its size.

## Context from Part 1
In Part 1, we found the optimal 3x3 square of fuel cells in a 300x300 grid. Each fuel cell has a power level calculated based on its coordinates and a grid serial number. For our input (serial number `2568`), the best 3x3 square had its top-left corner at `21,68`.

## Part 2 Extension
We've now discovered that the device supports selecting squares of **any size** from 1x1 up to 300x300, not just 3x3. We need to find the square of any size that has the maximum total power across the entire grid.

## Input
- A single integer: the **grid serial number** (puzzle input: `2568`)

## Grid Specifications
- Grid size: 300x300 cells
- Coordinate system: Uses `X,Y` notation where:
  - X ranges from 1 to 300 (horizontal)
  - Y ranges from 1 to 300 (vertical)
  - Top-left cell is `1,1`
  - Top-right cell is `300,1`

## Power Level Calculation Algorithm
For each fuel cell at coordinate `X,Y` (same as Part 1):

1. Calculate **rack ID** = X + 10
2. Start with power level = rack ID × Y
3. Add the grid serial number to power level
4. Multiply power level by rack ID
5. Extract only the **hundreds digit** of the power level (e.g., `12345` → `3`, `45` → `0`)
6. Subtract 5 from the result

### Example Calculation
For cell at `3,5` with serial number `8`:
- Rack ID = 3 + 10 = 13
- Power level = 13 × 5 = 65
- Add serial: 65 + 8 = 73
- Multiply by rack ID: 73 × 13 = 949
- Hundreds digit: 9
- Subtract 5: 9 - 5 = **4**

## Task Requirements
1. Calculate power levels for all cells in the 300x300 grid (same as Part 1)
2. For **every possible square size** (1x1, 2x2, 3x3, ..., up to 300x300):
   - For every valid position where a square of that size fits entirely within the grid
   - Calculate the sum of all power levels in that square
3. Find the square (of any size) with the maximum total power
4. Identify this square by its top-left coordinate AND its size

## Output Format
Return the `X,Y,size` identifier of the square with the largest total power.

Format: `X,Y,size` (e.g., `90,269,16` for a 16x16 square with top-left at 90,269)

### Expected Output Examples
- For serial number `18`: Answer is `90,269,16` (16x16 square, total power: 113)
- For serial number `42`: Answer is `232,251,12` (12x12 square, total power: 119)

## Constraints
- Square sizes range from 1 to 300
- For a square of size `S`, valid top-left coordinates range from `1,1` to `(301-S, 301-S)`
- The entire square must fit within the 300x300 grid

## Performance Considerations
- This is a computationally intensive problem (potentially checking 300 × 298 × 298 ≈ 26.6 million squares)
- Consider optimization techniques like:
  - Summed-area tables (integral images) for O(1) square sum calculations
  - Dynamic programming to reuse calculations from smaller squares
  - Early termination strategies if possible
