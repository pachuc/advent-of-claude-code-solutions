# Problem Report: Spiral Memory Stress Test - Adjacent Sum Values

## Part 1 Context
In Part 1, we worked with a spiral memory grid where squares are numbered starting from 1 at the center, spiraling outward:

```
17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
```

The spiral pattern moves: RIGHT → UP → LEFT → DOWN, with each ring growing larger.
Square 1 is at coordinates (0, 0), and we calculated Manhattan distances from any square to the center.

**Part 1 Answer:** For input `289326`, the Manhattan distance was `419`.

## Part 2 Objective
Instead of using sequential numbering, we now need to fill the spiral grid with values based on a different rule: each square's value is the **sum of all adjacent squares' values** (including diagonals) that have already been filled.

Find the **first value written** that is **larger** than the puzzle input.

## The New Value Assignment Rule

Starting fresh with the same spiral pattern:
1. Square 1 gets value `1` (initial value)
2. Each subsequent square (in spiral order) gets the sum of all adjacent filled squares (8 neighbors: up, down, left, right, and all 4 diagonals)

This produces the following grid:

```
147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...
```

### Example Trace:
- Square 1: value = `1` (starting value)
- Square 2: only adjacent to square 1 (value 1), so value = `1`
- Square 3: adjacent to squares 1 and 2 (values 1, 1), so value = `2`
- Square 4: adjacent to squares 1, 2, 3 (values 1, 1, 2), so value = `4`
- Square 5: adjacent to squares 1 and 4 (values 1, 4), so value = `5`
- ...and so on in spiral order

Once a value is written to a square, it never changes.

## Input
- A single integer: `289326` (the threshold value to exceed)

## Output
- A single integer: the first value written in the spiral that is larger than the input

## Algorithm Requirements

1. **Navigate the spiral pattern** in the same order as Part 1 (RIGHT → UP → LEFT → DOWN)
2. **Track coordinates** for each position in the spiral to know which squares are adjacent
3. **Store values** in a grid/dictionary as squares are filled
4. **For each new square** (in spiral order):
   - Calculate the sum of all adjacent squares that have already been filled (check all 8 neighbors)
   - Store this sum as the square's value
5. **Stop and return** the first value that exceeds the input threshold (`289326`)

## Key Considerations
- Adjacent means all 8 neighbors (horizontally, vertically, and diagonally)
- Only sum neighbors that have already been filled (earlier in the spiral)
- The spiral traversal order is critical - must process squares in the correct sequence
- Need to efficiently store and look up values by coordinates (e.g., using a dictionary with (x, y) as keys)
