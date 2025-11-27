# Problem Report: Fuel Requirement Calculator

## Objective
Calculate the **total fuel requirement** for all spacecraft modules.

## Problem Description
Given a list of module masses, compute the fuel needed for each module and sum them all together to get the total fuel requirement.

## Fuel Calculation Formula
For each module mass:
1. Divide the mass by 3
2. Round down to the nearest integer (floor division)
3. Subtract 2

**Formula:** `fuel = floor(mass / 3) - 2`

## Examples
| Mass   | Calculation           | Fuel Required |
|--------|----------------------|---------------|
| 12     | floor(12/3) - 2 = 4 - 2 | 2           |
| 14     | floor(14/3) - 2 = 4 - 2 | 2           |
| 1969   | floor(1969/3) - 2     | 654          |
| 100756 | floor(100756/3) - 2   | 33583        |

## Input Format
- A text file containing one integer per line
- Each integer represents the mass of a single module
- The input contains 100 module masses

## Expected Output
- A single integer representing the **sum of all fuel requirements** for every module in the input

## Algorithm Steps
1. Read all module masses from the input file
2. For each mass, apply the fuel formula: `floor(mass / 3) - 2`
3. Sum all the individual fuel values
4. Output the total sum
