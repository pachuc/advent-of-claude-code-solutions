# Problem Report: Triangle Validation

## Objective
Determine how many of the listed triangles are geometrically **possible** (valid).

## Context
We are analyzing a list of triangle specifications from a design document. Each specification provides three side lengths for a triangle. However, not all of these specifications represent valid triangles - some are geometrically impossible.

## Validation Rule
For a triangle to be valid, it must satisfy the **triangle inequality theorem**: the sum of any two sides must be larger than the remaining side.

More specifically, for a triangle with sides `a`, `b`, and `c`, ALL of the following conditions must be true:
- `a + b > c`
- `a + c > b`
- `b + c > a`

If any of these conditions fail, the triangle is impossible.

### Example
The specification `5 10 25` is **invalid** because:
- `5 + 10 = 15`, which is NOT larger than `25`

## Input Format
- The input consists of multiple lines
- Each line contains three space-separated integers representing the three side lengths of a potential triangle
- Example lines:
  ```
  566  477  376
  575  488  365
   50   18  156
  ```

## Expected Output
A single integer representing the count of valid (possible) triangles in the input.

## Algorithm Requirements
For each line in the input:
1. Parse the three side lengths
2. Check if all three triangle inequality conditions are satisfied
3. If all conditions pass, count it as a valid triangle
4. Return the total count of valid triangles
