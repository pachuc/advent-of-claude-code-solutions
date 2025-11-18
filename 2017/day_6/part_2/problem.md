# Problem Report: Memory Reallocation Loop Size Detection

## Objective
Determine the size of the infinite loop in the memory reallocation routine - specifically, how many redistribution cycles occur between the first and second appearance of the repeated configuration.

## Context from Part 1
In Part 1, we solved a memory reallocation problem where we:
- Detected when a configuration repeated for the first time
- Counted how many redistribution cycles it took to reach that first repetition
- Answer for Part 1: **4074 cycles** until a configuration repeated

The redistribution algorithm works as follows:
1. Find the memory bank with the most blocks (ties won by lowest index)
2. Remove all blocks from that bank
3. Redistribute those blocks one at a time to subsequent banks (wrapping around)
4. Track each resulting configuration

## Part 2 Task
Now that we know a repeated configuration occurs, we need to find the **loop size**: starting from the state that was seen for the first time, how many additional cycles does it take before that same state appears again?

### Example Walkthrough
From the Part 1 example with initial state `0 2 7 0`:

- Cycle 1: `2 4 1 2` (first time seeing this)
- Cycle 2: `3 1 2 3`
- Cycle 3: `0 2 3 4`
- Cycle 4: `1 3 4 1`
- Cycle 5: `2 4 1 2` (seen this before - detected at cycle 5)

The configuration `2 4 1 2` first appeared after Cycle 1, and appeared again at Cycle 5.
Loop size = 5 - 1 = **4 cycles**

## Input
- Same input as Part 1: `11 11 13 7 0 15 5 5 4 4 1 1 7 1 15 11`
- A single line containing space-separated integers representing block counts in memory banks

## Algorithm Requirements

1. **Continue from Part 1 logic**: Run the same redistribution algorithm
2. **Track when each configuration first appears**: Store not just which configurations were seen, but also at which cycle number each was first encountered
3. **When a repeat is detected**:
   - Identify which configuration repeated
   - Look up when that configuration was first seen
   - Calculate the difference: current_cycle - first_occurrence_cycle
4. **Return the loop size**: This difference is the size of the infinite loop

## Expected Output
A single integer representing the number of cycles in the infinite loop (the distance between the first and second appearance of the repeated configuration).

## Key Implementation Details
- Modify the tracking mechanism from Part 1 to store cycle numbers, not just a set of seen configurations
- Use a dictionary/map to associate configurations with the cycle number when first seen
- The loop size = (cycle when repeated) - (cycle when first seen)
- The redistribution algorithm itself remains identical to Part 1
