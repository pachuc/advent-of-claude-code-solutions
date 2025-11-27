# Problem Report: Water Retention After Spring Dries Up (Part 2)

## Context from Part 1
In Part 1, we simulated water flowing from a spring at (x=500, y=0) through a 2D cross-section of ground containing sand and clay veins. Water flows down when possible and spreads horizontally when blocked. The Part 1 answer of **41027** represented the total number of tiles that water could reach, including both:
- `~` (settled water): Water at rest in containers formed by clay
- `|` (flowing water): Sand through which water has passed or is passing

## Part 2 Objective
After the water spring runs dry, only the settled water (`~`) will remain. All flowing water (`|`) will eventually drain away. Calculate how many tiles still contain water after all the flowing water has drained.

## Key Difference from Part 1
- **Part 1**: Count both settled water (`~`) AND flowing water (`|`)
- **Part 2**: Count ONLY settled water (`~`)

## Input Format
Same as Part 1. The input consists of lines defining clay vein positions:
- `x=VALUE, y=START..END` - vertical clay vein
- `y=VALUE, x=START..END` - horizontal clay vein

## Water Flow Rules (Same as Part 1)
1. **Starting point**: Water originates from a spring at x=500, y=0
2. **Movement priority**: Water always moves DOWN when possible
3. **Horizontal spreading**: When water cannot move down, it spreads LEFT and RIGHT
4. **Settling conditions**: Water settles (becomes `~`) when contained by clay walls on both left and right sides
5. **Overflow**: Water that reaches a clay wall on only one side will overflow and fall down (remains as `|`)

## Valid Counting Range
- **Minimum y**: The smallest y-coordinate in the clay vein input data
- **Maximum y**: The largest y-coordinate in the clay vein input data
- Only count water tiles within this range (inclusive)

## Output Format
A single integer representing the total count of tiles containing **settled water only** (`~`).

## Example
From the Part 1 puzzle description:
- Total tiles water can reach (Part 1): **57** (both `~` and `|`)
- Tiles with settled water only (Part 2): **29** (only `~`)

## Implementation Strategy
The Part 1 solution already tracks settled water and flowing water separately in two different sets:
- `settled_water` - contains all positions with settled water (`~`)
- `flowing_water` - contains all positions with flowing water (`|`)

For Part 2, simply count only the `settled_water` tiles within the valid y-range, ignoring the `flowing_water` tiles.

## Expected Modification
Modify the counting logic at the end of the Part 1 solution:
- **Part 1** counted: `flowing_water | settled_water` (union of both sets)
- **Part 2** should count: `settled_water` only (ignore flowing_water)

Both counts should respect the valid y-range (min_y to max_y).
