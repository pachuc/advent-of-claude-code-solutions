# Problem Report: Spreadsheet Evenly Divisible Values

## Context from Part 1
In Part 1, we calculated a corruption checksum for a spreadsheet by finding the difference between the maximum and minimum values in each row, then summing those differences. The Part 1 solution yielded a checksum of 39126.

The spreadsheet consists of rows of numbers, with each row containing space-separated integers. The same input spreadsheet is used for both parts.

## Part 2 Objective
Calculate a new sum based on finding evenly divisible number pairs in the spreadsheet. Instead of max-min differences, we need to find division results for specific number pairs in each row.

## Problem Description
For the same spreadsheet from Part 1:
1. In each row, find the only two numbers where one evenly divides the other (the division result is a whole number with no remainder)
2. Divide the larger number by the smaller number to get that row's result
3. Sum all the row results to get the final answer

## Key Constraints
- There is exactly ONE pair of numbers in each row where one evenly divides the other
- "Evenly divides" means the division operation produces a whole number (no remainder)
- For numbers a and b where a > b, we check if a % b == 0 (a is divisible by b)

## Input Format
- Same spreadsheet format as Part 1
- Multiple rows of space-separated integers
- Input is located in `input.md`
- Each row may have different numbers of values

## Expected Output
- A single integer representing the sum of all division results across all rows

## Algorithm Steps
1. For each row in the spreadsheet:
   - Check all pairs of numbers in the row
   - Find the pair where one number evenly divides the other
   - Calculate the division result (larger / smaller)
   - Add this result to the running sum
2. Return the final sum

## Worked Example
Given the spreadsheet:
```
5 9 2 8
9 4 7 3
3 8 6 5
```

- Row 1: Numbers are [5, 9, 2, 8]
  - Check pairs: 8 / 2 = 4 (evenly divides!)
  - Result = 4

- Row 2: Numbers are [9, 4, 7, 3]
  - Check pairs: 9 / 3 = 3 (evenly divides!)
  - Result = 3

- Row 3: Numbers are [3, 8, 6, 5]
  - Check pairs: 6 / 3 = 2 (evenly divides!)
  - Result = 2

Final sum = 4 + 3 + 2 = 9

## Implementation Notes
- Need to check all possible pairs in each row
- For each pair (a, b), check both a % b and b % a to find which divides evenly
- The problem guarantees exactly one valid pair per row
- The actual input data is the same 16-row spreadsheet from Part 1 in `input.md`
