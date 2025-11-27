# Problem Report: Fabric Claim Overlap

## Context
The Elves are trying to cut fabric for Santa's suit from a large square piece of fabric (at least 1000x1000 inches). Each Elf has made a claim about which rectangular area of the fabric they want to use. Many claims overlap, causing conflicts about who gets which part of the fabric.

## Objective
Calculate how many square inches of fabric are claimed by two or more Elves (i.e., count the number of square inches where claims overlap).

## Input Format
The input consists of multiple lines, each containing a claim in the following format:

```
#<ID> @ <left>,<top>: <width>x<height>
```

Where:
- `<ID>` - A unique identifier for the claim (integer)
- `<left>` - Number of inches from the left edge of the fabric to the left edge of the rectangle (integer)
- `<top>` - Number of inches from the top edge of the fabric to the top edge of the rectangle (integer)
- `<width>` - Width of the claimed rectangle in inches (integer)
- `<height>` - Height of the claimed rectangle in inches (integer)

**Example:**
```
#123 @ 3,2: 5x4
```
This means claim ID 123 specifies a rectangle that starts 3 inches from the left edge, 2 inches from the top edge, is 5 inches wide, and 4 inches tall.

## Expected Output
A single integer representing the total number of square inches of fabric that are within two or more claims.

## Algorithm Requirements
1. Parse each claim to extract its position (left, top) and dimensions (width, height)
2. Track which square inches of fabric are claimed by each claim
3. Count how many square inches are claimed by 2 or more different claims
4. Return the count as an integer

## Example
Given these claims:
```
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
```

Visual representation (numbers show which claim covers each square):
```
........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
```

The squares marked with `X` are claimed by both claim 1 and claim 2. There are **4 square inches** that overlap, so the answer would be `4`.
