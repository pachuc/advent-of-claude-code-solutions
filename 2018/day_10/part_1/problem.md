# Problem Report: The Stars Align

## Context
Points of light in the sky are moving with constant velocities. These points will eventually align to form a readable message. The message appears briefly when the points are closest together and aligned properly, then the points continue moving and disperse.

## Objective
Determine what message will appear in the sky when the moving points align.

## Input Format
The input consists of multiple lines, where each line represents one point of light with:
- A **position** given as `<X, Y>` coordinates
- A **velocity** given as `<X, Y>` velocity components

Format: `position=<X, Y> velocity=<X, Y>`

Where:
- **X**: Positive values mean right, negative values mean left
- **Y**: Positive values mean down, negative values mean up (standard screen coordinates)
- Velocities represent the change in position per second

Example input line:
```
position=< 9,  1> velocity=< 0,  2>
```

## Physics Rules
1. At time `t=0`, each point starts at its given position
2. Each second, each point's velocity is added to its position
3. For a point with position `(px, py)` and velocity `(vx, vy)`:
   - Position at time `t` = `(px + t*vx, py + t*vy)`

## Expected Output
The output should be the **message** that appears when the points align.

The message will be:
- Formed by the points of light when they are arranged in a pattern
- Readable as letters/text (capital letters based on the example)
- Visible only briefly at a specific moment in time

## Solution Approach
1. Parse all point positions and velocities from the input
2. Simulate the movement of points over time
3. Detect when the points form a cohesive, readable message
   - This likely occurs when the points are closest together (minimum bounding box area)
4. Visualize the points at that moment to read the message
5. Return the message as a string

## Notes
- The example shows points forming "HI" after 3 seconds
- The actual message will be much longer and take many more seconds to appear
- Points should be displayed as `#` characters when visualizing
- The challenge is determining the exact time when the message appears (when points are most aligned)
