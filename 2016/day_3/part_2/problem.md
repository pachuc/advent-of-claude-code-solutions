# Problem Report: Triangle Validation (Part 2 - Column-Based Reading)

## Context from Part 1
In Part 1, we validated triangles by reading the input file **horizontally** (row by row). Each row contained three space-separated integers representing the three side lengths of a single triangle. We used the triangle inequality theorem to determine if each triangle was valid, and counted 1050 valid triangles.

## Part 2 Changes: Vertical Reading
We now realize that the triangles are actually specified **vertically** in groups of three. The input should be read **by columns**, not by rows.

## How Column-Based Reading Works
- The input is arranged in a grid format with 3 columns
- Every 3 consecutive rows form a "group"
- Within each group, each **column** represents one triangle
- The three numbers in a column (across the 3 rows) are the three side lengths of that triangle

### Example
Given this input:
```
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
```

This represents **6 triangles** (not 6):
- **First group (rows 1-3):**
  - Triangle 1: sides 101, 102, 103 (from column 1)
  - Triangle 2: sides 301, 302, 303 (from column 2)
  - Triangle 3: sides 501, 502, 503 (from column 3)
- **Second group (rows 4-6):**
  - Triangle 4: sides 201, 202, 203 (from column 1)
  - Triangle 5: sides 401, 402, 403 (from column 2)
  - Triangle 6: sides 601, 602, 603 (from column 3)

## Validation Rule (Same as Part 1)
For a triangle to be valid, it must satisfy the **triangle inequality theorem**: the sum of any two sides must be larger than the remaining side.

For sides `a`, `b`, and `c`, ALL of the following must be true:
- `a + b > c`
- `a + c > b`
- `b + c > a`

## Input Format
- Multiple lines of input
- Each line contains three space-separated integers
- Lines should be processed in groups of 3
- Each group of 3 lines contains data for 3 triangles (one per column)

## Expected Output
A single integer representing the count of valid (possible) triangles when reading the input **by columns**.

## Algorithm Requirements
1. Read the input in groups of 3 consecutive rows
2. For each group:
   - Extract the three numbers from column 1 (positions [0] from each of the 3 rows) → Triangle 1
   - Extract the three numbers from column 2 (positions [1] from each of the 3 rows) → Triangle 2
   - Extract the three numbers from column 3 (positions [2] from each of the 3 rows) → Triangle 3
3. For each triangle, validate using the triangle inequality theorem
4. Count all valid triangles
5. Return the total count
