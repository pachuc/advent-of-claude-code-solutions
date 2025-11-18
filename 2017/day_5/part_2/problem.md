# Problem Report: Escape the Jump Instruction Maze (Part 2)

## Objective
Calculate how many steps it takes to escape from a maze of jump instructions using a **modified increment rule** based on the offset value.

## Context from Part 1
In Part 1, we had a CPU trapped in a maze of jump instructions where:
- We start at position 0
- Each instruction contains a jump offset (relative movement)
- After reading an offset, we jump by that amount and increment the offset by 1
- We continue until we jump outside the list bounds
- Part 1 answer was **339351 steps**

## Part 2 Change: Modified Increment Rule
The jump instructions now behave differently when modifying offsets:

**NEW RULE:**
- If the offset value is **3 or more**: **decrease** it by 1
- If the offset value is **less than 3**: **increase** it by 1 (same as Part 1)

This change significantly affects the exit time as large offsets now decrease instead of increase.

## Input
- Same input as Part 1: A list of 1038 integers representing jump offsets (one per line)
- Each integer represents a relative jump offset:
  - Positive values jump forward (toward the end of the list)
  - Negative values jump backward (toward the beginning of the list)
  - Zero means stay at the current position

## Algorithm Requirements

### Starting Condition
- Begin at the first instruction (index 0)
- Step counter starts at 0

### Execution Rules
1. Read the offset value at the current position
2. Jump to a new position by adding the offset to the current position
3. **After reading the offset but before jumping**, modify the offset at the current position:
   - If offset >= 3: decrease by 1 (offset -= 1)
   - If offset < 3: increase by 1 (offset += 1)
4. Increment the step counter
5. Repeat until the position goes outside the list bounds (position < 0 or position >= list length)

### Key Details
- Jump offsets are **relative** to the current position
- The modification rule now depends on the offset value
- Offsets >= 3 are decremented (making them less likely to grow unbounded)
- Offsets < 3 are incremented (same as Part 1)
- Exit occurs when the calculated next position falls outside the list bounds

## Example Walkthrough
Given the same list from Part 1: `[0, 3, 0, 1, -3]`

With the **new rule**, this now takes **10 steps** instead of 5:

| Step | Position | Offset | Offset >= 3? | Action | List State After |
|------|----------|--------|--------------|--------|------------------|
| 0 | 0 | 0 | No | Jump 0, increment to 1 | `[1, 3, 0, 1, -3]` |
| 1 | 0 | 1 | No | Jump 1, increment to 2 | `[2, 3, 0, 1, -3]` |
| 2 | 1 | 3 | Yes | Jump 3, **decrement** to 2 | `[2, 2, 0, 1, -3]` |
| 3 | 4 | -3 | No | Jump -3, increment to -2 | `[2, 2, 0, 1, -2]` |
| 4 | 1 | 2 | No | Jump 2, increment to 3 | `[2, 3, 0, 1, -2]` |
| 5 | 3 | 1 | No | Jump 1, increment to 2 | `[2, 3, 0, 2, -2]` |
| 6 | 4 | -2 | No | Jump -2, increment to -1 | `[2, 3, 0, 2, -1]` |
| 7 | 2 | 0 | No | Jump 0, increment to 1 | `[2, 3, 1, 2, -1]` |
| 8 | 2 | 1 | No | Jump 1, increment to 2 | `[2, 3, 2, 2, -1]` |
| 9 | 3 | 2 | No | Jump 2, increment to 3 | `[2, 3, 2, 3, -1]` |
| 10 | 5 | - | - | Position 5 is outside the list - **EXIT** | - |

Final list state: `[2, 3, 2, 3, -1]`
Result: **10 steps**

## Expected Output
A single integer representing the total number of steps taken to exit the maze using the new offset modification rule.

## Output Format
Just the integer value, no additional formatting required.
