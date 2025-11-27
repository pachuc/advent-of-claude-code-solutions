# Problem Report: Water Flow Simulation

## Objective
Simulate water flowing through a 2D cross-section of ground containing sand and clay veins. Calculate how many tiles can be reached by water within the valid y-coordinate range.

## Context
The simulation models water flowing from a spring at coordinates (x=500, y=0). Water flows through sand but is blocked by clay. The goal is to determine the total number of tiles that water can reach, either as settled water or flowing water.

## Input Format
The input consists of lines defining clay vein positions using one of two formats:
- `x=VALUE, y=START..END` - vertical clay vein at x-coordinate VALUE from y=START to y=END
- `y=VALUE, x=START..END` - horizontal clay vein at y-coordinate VALUE from x=START to x=END

Example:
```
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
```

## Water Flow Rules
1. **Starting point**: Water originates from a spring at x=500, y=0
2. **Movement priority**: Water always moves DOWN when possible
3. **Horizontal spreading**: When water cannot move down (blocked by clay or settled water), it spreads LEFT and RIGHT
4. **Settling conditions**: Water settles (becomes `~`) when contained by clay walls on both left and right sides
5. **Overflow**: Water that reaches a clay wall on only one side will overflow and fall down
6. **No pressure**: Water pressure does not apply - water on one side of a barrier doesn't affect the other side

## Valid Counting Range
- **Minimum y**: The smallest y-coordinate in the clay vein input data
- **Maximum y**: The largest y-coordinate in the clay vein input data
- Only count water tiles within this range (inclusive)
- Ignore the spring at y=0 if it's outside this range
- Ignore water that falls beyond the maximum y value

## Output Format
A single integer representing the total count of tiles that water can reach.

## Water States to Count
- `~` (settled water): Water that has come to rest in a container formed by clay
- `|` (flowing water): Sand through which water has passed or is passing

Both states should be counted toward the final answer.

## Example
For the given example in the puzzle:
- Clay veins define valid y-range of 1 to 13
- Water flows from the spring, settles in containers, and overflows when full
- Total tiles reached by water: **57**

## Implementation Notes
1. Parse input to identify all clay tile positions
2. Determine the valid y-range (min and max y from clay positions)
3. Simulate water flow starting from (500, 0):
   - Track flowing water (`|`) and settled water (`~`)
   - Handle downward flow, horizontal spreading, settling, and overflow
4. Count all tiles marked as either `~` or `|` within the valid y-range
5. Return the count
