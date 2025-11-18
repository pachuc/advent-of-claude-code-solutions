# Problem Report: Spinlock Algorithm - Part 2 (Scaled Version)

## Objective
Simulate the same spinlock algorithm from Part 1, but now for 50 million insertions instead of 2017. Find the value that appears immediately after `0` (not after the last inserted value) in the circular buffer after all insertions are complete.

## Context from Part 1
In Part 1, we simulated a spinlock algorithm that:
- Starts with a circular buffer containing only `0`
- Repeatedly steps forward by a fixed number of positions (the step size)
- Inserts sequential values (1, 2, 3, ...) into the buffer
- Performed 2017 insertions and found the value after 2017

Part 1 answer: `1912` (the value after 2017 with step size 355)

## Part 2 Changes
The algorithm remains the same, but with two critical differences:
1. **Scale**: Now performing **50,000,000 insertions** (instead of 2017)
2. **Target**: Find the value after **`0`** (instead of after the last inserted value)

## Algorithm Description

### Initial State
- Start with a circular buffer containing only the value `0`
- Mark position 0 as the current position

### Process (repeat 50,000,000 times)
For each iteration i from 1 to 50,000,000:
1. **Step forward**: Move forward through the circular buffer by the step size (given as input)
2. **Insert**: Insert the new value `i` immediately after the position where you stopped
3. **Update current position**: The newly inserted value becomes the current position for the next iteration

### Important Details
- The buffer is circular, meaning after the last element you wrap around to the first
- Each insertion increases the buffer size by 1
- After all 50,000,000 insertions, the buffer will contain 50,000,001 values total (0 through 50,000,000)
- The value `0` always remains at position 0 in the buffer (it never moves)
- We need to track what value is at position 1 (immediately after `0`)

## Performance Consideration
**CRITICAL**: With 50 million insertions, a naive simulation that maintains the entire buffer will be extremely slow and memory-intensive. An optimization is needed:
- Since `0` never moves from position 0, we only need to track what value is at position 1
- We can simulate the position movements without storing the entire buffer
- Only track/update the value after position 0 when an insertion happens at position 1

## Input
A single integer representing the number of steps to move forward in each iteration.

**Given input**: `355`

## Output
A single integer: the value that appears immediately after `0` in the circular buffer after 50,000,000 insertions.

## Expected Output Format
A single integer value (no additional formatting required).
