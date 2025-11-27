# Problem Report: Finding the Non-Overlapping Fabric Claim

## Context from Part 1
The Elves are trying to cut fabric for Santa's suit from a large square piece of fabric (at least 1000x1000 inches). Each Elf has made a claim about which rectangular area of the fabric they want to use. In Part 1, we found that many claims overlap - specifically, there were **107,820 square inches** of fabric that were claimed by two or more Elves.

## Part 2 Objective
Find the ID of the single claim that doesn't overlap with any other claim. According to the puzzle, exactly one claim exists that is completely intact - it doesn't share even a single square inch with any other claim.

## Input Format
The input format is identical to Part 1. Each line contains a claim in the following format:

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

## Expected Output
A single integer: the ID of the only claim that doesn't overlap with any other claim.

## Algorithm Requirements
1. Parse each claim to extract its ID, position (left, top) and dimensions (width, height)
2. Build a representation of the fabric that tracks which claims cover each square inch
3. For each claim, check if ALL of its square inches are covered ONLY by that claim (not shared with any other claim)
4. Return the ID of the claim that has no overlaps with any other claims

## Example
Given these claims from Part 1:
```
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
```

Visual representation:
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

- Claim #1 overlaps with claim #2 (the `X` squares)
- Claim #2 overlaps with claim #1 (the `X` squares)
- Claim #3 doesn't overlap with any other claim (all its squares are only claimed by #3)

**Answer: 3**

## Key Insight
You can reuse the grid approach from Part 1:
- Create a grid where each cell tracks the count of how many claims cover it
- After marking all claims, a non-overlapping claim is one where every square inch it covers has a count of exactly 1
- There is guaranteed to be exactly one such claim in the input
