# Problem Report: Spreadsheet Corruption Checksum

## Objective
Calculate a checksum for a spreadsheet to verify data integrity. The checksum helps determine if the recovery process for corrupted data is on the right track.

## Problem Description
Given a spreadsheet consisting of rows of numbers, calculate a checksum value by:
1. For each row, find the difference between the largest value and the smallest value
2. Sum all of these differences to get the final checksum

## Input Format
- The input is a spreadsheet with multiple rows
- Each row contains space-separated integers
- Rows may have different numbers of values

Example input:
```
5 1 9 5
7 5 3
2 4 6 8
```

## Expected Output
- A single integer representing the checksum of the spreadsheet

## Algorithm Steps
1. For each row in the spreadsheet:
   - Identify the maximum value in the row
   - Identify the minimum value in the row
   - Calculate the difference: max - min
2. Sum all the row differences to produce the final checksum

## Worked Example
Given the spreadsheet:
```
5 1 9 5
7 5 3
2 4 6 8
```

- Row 1: max = 9, min = 1, difference = 8
- Row 2: max = 7, min = 3, difference = 4
- Row 3: max = 8, min = 2, difference = 6

Checksum = 8 + 4 + 6 = 18

## Implementation Notes
- The actual input data is located in `input.md`
- Each row should be parsed to extract integer values
- Empty lines or trailing whitespace should be handled appropriately
