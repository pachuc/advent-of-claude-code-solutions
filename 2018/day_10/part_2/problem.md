# Problem Report: The Stars Align - Part 2

## Background from Part 1

Points of light in the sky are moving with constant velocities. These points eventually align to form a readable message, but the alignment is brief - lasting only a second before the points continue moving and disperse.

In Part 1, we determined that the message formed by the aligned points is **"LRGPBHEZ"**.

The Part 1 solution:
1. Parsed position and velocity data for all points
2. Simulated the movement of points over time
3. Detected when points were most aligned by finding the time when the bounding box area was minimized
4. Visualized the points at that moment to read the message

## Part 2 Objective

**Determine exactly how many seconds it takes for the message to appear.**

In the example from Part 1, the message "HI" appeared after 3 seconds. The actual message "LRGPBHEZ" takes much longer to appear.

## Input Format

Same as Part 1. The input consists of multiple lines, where each line represents one point of light:
- A **position** given as `<X, Y>` coordinates
- A **velocity** given as `<X, Y>` velocity components

Format: `position=<X, Y> velocity=<X, Y>`

Where:
- **X**: Positive values mean right, negative values mean left
- **Y**: Positive values mean down, negative values mean up
- Velocities represent the change in position per second

## Physics Rules

Same as Part 1:
1. At time `t=0`, each point starts at its given position
2. Each second, each point's velocity is added to its position
3. For a point with position `(px, py)` and velocity `(vx, vy)`:
   - Position at time `t` = `(px + t*vx, py + t*vy)`

## Expected Output

A single integer representing **the number of seconds that must elapse for the message to appear**.

## Solution Approach

The Part 1 solution already contains the answer! The `find_alignment_time()` function returns the exact time when the points are most aligned (minimum bounding box area), which is when the message appears.

Simply return this time value as the answer, rather than the decoded message.

## Notes

- The message appears when the bounding box area is at its minimum
- This occurs at the exact moment before the bounding box area starts increasing again
- The Part 1 code already calculates this value - we just need to output it as the answer for Part 2
