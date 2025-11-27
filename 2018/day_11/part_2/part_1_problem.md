# Problem Report: Fuel Cell Power Grid Optimization

## Objective
Find the 3x3 square of fuel cells with the largest total power in a 300x300 grid.

## Context
We have a 300x300 grid of fuel cells. Each cell has a power level that is calculated based on its coordinates and a grid serial number. We need to find the optimal 3x3 square region to maximize power.

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
For each fuel cell at coordinate `X,Y`:

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

### Verification Examples
- Cell `122,79` with serial `57`: power level = `-5`
- Cell `217,196` with serial `39`: power level = `0`
- Cell `101,153` with serial `71`: power level = `4`

## Task Requirements
1. Calculate power levels for all cells in the 300x300 grid
2. For every possible 3x3 square (that fits entirely within the grid), calculate the sum of the 9 power levels
3. Find the 3x3 square with the maximum total power

## Output Format
Return the `X,Y` coordinate of the **top-left fuel cell** of the 3x3 square with the largest total power.

Format: `X,Y` (e.g., `33,45`)

### Expected Output Examples
- For serial number `18`: Answer is `33,45` (total power: 29)
- For serial number `42`: Answer is `21,61` (total power: 30)

## Constraints
- The 3x3 square must be entirely within the 300x300 grid
- Valid top-left coordinates range from `1,1` to `298,298` (to ensure the 3x3 square fits)
