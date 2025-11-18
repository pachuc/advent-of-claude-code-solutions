# Problem Report: Spinlock Algorithm Simulation

## Objective
Simulate a spinlock algorithm that builds a circular buffer through iterative insertions, then find the value that appears immediately after the final inserted value (2017) in the completed buffer.

## Context
A spinlock uses a circular buffer data structure and repeatedly steps forward by a fixed number of positions before inserting new values. We need to simulate this process to determine the buffer's final state.

## Algorithm Description

### Initial State
- Start with a circular buffer containing only the value `0`
- Mark position 0 as the current position

### Process (repeat 2017 times)
For each iteration i from 1 to 2017:
1. **Step forward**: Move forward through the circular buffer by a fixed number of steps (given as input)
2. **Insert**: Insert the new value `i` immediately after the position where you stopped
3. **Update current position**: The newly inserted value becomes the current position for the next iteration

### Important Details
- The buffer is circular, meaning after the last element you wrap around to the first
- Each insertion increases the buffer size by 1
- After all 2017 insertions, the buffer will contain 2018 values total (0 through 2017)

## Input
A single integer representing the number of steps to move forward in each iteration.

**Given input**: `355`

## Output
A single integer: the value that appears immediately after `2017` in the final circular buffer.

## Example Walkthrough (with step size = 3)

Starting state: `(0)` (parentheses indicate current position)

- Insert 1: Step forward 3 times from position 0 → `0 (1)`
- Insert 2: Step forward 3 times from position at value 1 → `0 (2) 1`
- Insert 3: Step forward 3 times from position at value 2 → `0 2 (3) 1`
- Insert 4: Step forward 3 times from position at value 3 → `0 2 (4) 3 1`
- Insert 5: Step forward 3 times from position at value 4 → `0 (5) 2 4 3 1`
- Insert 6: Step forward 3 times from position at value 5 → `0 5 2 4 3 (6) 1`
- ... continues for 2017 total insertions

After 2017 insertions with step size 3, the buffer near the last insertion looks like:
`1512 1134 151 (2017) 638 1513 851`

The value after 2017 is `638`.

## Expected Output Format
A single integer value (no additional formatting required).
