# Problem Report: JSON Number Summation

## Objective
Calculate the sum of all numbers found within a JSON document.

## Context
Santa's Accounting-Elves are balancing the books after a recent order. Their accounting software uses JSON format to store data, and we need to find all numbers in the document and sum them together.

## Input
- A JSON document containing various data types:
  - Arrays (e.g., `[1,2,3]`)
  - Objects (e.g., `{"a":1, "b":2}`)
  - Numbers (integers, both positive and negative)
  - Strings

- The input will be provided in the file `input.md`

## Task Requirements
1. Parse through the entire JSON document
2. Identify all numeric values (integers) regardless of their location within:
   - Arrays
   - Objects (as values)
   - Nested structures (deeply nested arrays and objects)
3. Add all identified numbers together
4. Return the sum

## Important Constraints
- You will NOT encounter any strings containing numbers (so no need to parse strings for numeric content)
- Numbers can be positive or negative
- Empty arrays `[]` and empty objects `{}` contribute 0 to the sum
- Numbers can be deeply nested within multiple levels of arrays and objects

## Examples
- `[1,2,3]` has a sum of `6`
- `{"a":2,"b":4}` has a sum of `6`
- `[[[3]]]` has a sum of `3`
- `{"a":{"b":4},"c":-1}` has a sum of `3`
- `{"a":[-1,1]}` has a sum of `0`
- `[-1,{"a":1}]` has a sum of `0`
- `[]` has a sum of `0`
- `{}` has a sum of `0`

## Expected Output
A single integer representing the sum of all numbers in the JSON document.

## Output Format
The answer should be output as a single integer (no additional formatting required).
