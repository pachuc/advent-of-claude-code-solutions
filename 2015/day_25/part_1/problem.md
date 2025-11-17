# Problem Report: Code Generation for Weather Machine

## Objective
Calculate a specific code from an infinite grid of codes that are generated using a mathematical formula and filled in a diagonal pattern.

## Context
Santa's weather machine requires a code from a manual to operate. The codes are arranged on an infinite grid and generated using a specific algorithm. We need to find the code at a specific position in this grid.

## Grid Filling Pattern
The codes are filled in the grid by diagonals, starting from the top-left corner and proceeding diagonally up and to the right.

The order codes are filled:
```
   | 1   2   3   4   5   6
---+---+---+---+---+---+---+
 1 |  1   3   6  10  15  21
 2 |  2   5   9  14  20
 3 |  4   8  13  19
 4 |  7  12  18
 5 | 11  17
 6 | 16
```

- The 1st code goes to position (row=1, col=1)
- The 2nd code goes to position (row=2, col=1)
- The 3rd code goes to position (row=1, col=2)
- The 12th code goes to position (row=4, col=2)
- The 15th code goes to position (row=1, col=5)

## Code Generation Algorithm
1. The first code is: **20151125**
2. Each subsequent code is generated from the previous code using:
   - Multiply the previous code by **252533**
   - Take the remainder when dividing by **33554393**
   - This remainder is the next code

Formula: `next_code = (previous_code * 252533) % 33554393`

### Example
- Code 1: 20151125
- Code 2: (20151125 * 252533) % 33554393 = 31916031

### Sample Grid Values (for validation)
```
   |    1         2         3         4         5         6
---+---------+---------+---------+---------+---------+---------+
 1 | 20151125  18749137  17289845  30943339  10071777  33511524
 2 | 31916031  21629792  16929656   7726640  15514188   4041754
 3 | 16080970   8057251   1601130   7981243  11661866  16474243
 4 | 24592653  32451966  21345942   9380097  10600672  31527494
 5 |    77061  17552253  28094349   6899651   9250759  31663883
 6 | 33071741   6796745  25397450  24659492   1534922  27995004
```

## Input
The target position is provided in the format:
"Enter the code at row [ROW], column [COLUMN]."

For this puzzle: **row 2978, column 3083**

## Expected Output
A single integer representing the code at the specified row and column position.

## Algorithm Requirements
1. Determine which sequential position in the generation order corresponds to the given (row, column)
2. Generate codes sequentially from the first code until reaching that position
3. Return the code at the target position

## Notes
- The grid is infinite, so any valid positive integer row and column can be requested
- The diagonal filling pattern means we need to calculate which iteration number corresponds to a given (row, col) coordinate
- Each diagonal has a specific number of elements, and we fill from bottom-left to top-right within each diagonal
