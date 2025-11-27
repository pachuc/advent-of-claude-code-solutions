# Testing Issues

## Issue Found: Example Test Case Fails

### Problem
The solution produces **45 tiles** for the example test case, but the expected answer is **57 tiles**.
This represents a discrepancy of **12 tiles** (21% error).

### Example Input
```
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=10..13
x=506, y=1..2
y=13, x=498..504
```

### Current Output
```
Water can reach 45 tiles
Flowing: 25
Settled: 20
```

### Grid Visualization
```
   0 ......+.......
   1 ......|.....#.
   2 .#|||||||...#.
   3 .#~~~~~#|.....
   4 .#~~~~~#|.....
   5 .#~~~~~#|.....
   6 .#~~~~~#|.....
   7 .#######|.....
   8 ........|.....
   9 ........|.....
  10 ....#...|.....
  11 ....#...|.....
  12 ....#|||||||..
  13 ....#######|..
```

### Analysis
Looking at the grid, the water flow pattern appears to be:
1. Water flows down from (500, 0) to (500, 1)
2. At y=2, it spreads left and right, contained by clay walls at x=495 and x=506
3. Inside the first container (x=495-501, y=3-7), water settles correctly
4. Water overflows and continues down the right side
5. In the second container (y=12-13 around x=498-504), water spreads

### Missing Water
The 12 missing tiles suggest that water is not spreading as far as it should in certain areas. Potential issues:

1. **Horizontal spreading may stop prematurely**: When water encounters a position without immediate support below, it may not be exploring all possible flow paths.

2. **Multi-level filling issue**: Water may not be correctly handling scenarios where it needs to fill multiple levels with complex overflow patterns.

3. **State transition problem**: The transition between flowing and settled water might not be handling all edge cases correctly.

### Impact on Main Answer
The solution reports **41,027 tiles** for the actual puzzle input. If the same bug affects the main input with a similar error rate (~21%), the actual answer could be different.

### Recommendation
The algorithm has a bug in the horizontal spreading or settling logic. The solution should NOT be trusted as correct until the example test case passes. The reported answer of 41,027 is likely **incorrect**.

## Verification Status: FAILURE

The solution fails the example test case and therefore cannot be verified as correct.
