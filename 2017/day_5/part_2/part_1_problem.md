# Problem Report: Escape the Jump Instruction Maze

## Objective
Calculate how many steps it takes to escape from a maze of jump instructions by following the offsets until we jump outside the bounds of the instruction list.

## Context
A CPU is trapped in a maze of jump instructions and needs assistance finding the exit. The maze consists of a list of relative jump offsets that determine how to navigate through the instructions.

## Input
- A list of integers representing jump offsets (one per line)
- Each integer represents a relative jump offset:
  - Positive values jump forward (toward the end of the list)
  - Negative values jump backward (toward the beginning of the list)
  - Zero means stay at the current position
- The input file contains 1038 offset values

## Algorithm Requirements

### Starting Condition
- Begin at the first instruction (index 0)
- Step counter starts at 0

### Execution Rules
1. Read the offset value at the current position
2. Jump to a new position by adding the offset to the current position
3. **After reading the offset but before jumping**, increment the offset value at the current position by 1
4. Increment the step counter
5. Repeat until the position goes outside the list bounds (either negative or >= list length)

### Key Details
- Jump offsets are **relative** to the current position
  - Offset of -1 means move to the previous instruction
  - Offset of 2 means skip the next instruction
  - Offset of 0 means stay at the current instruction (which then becomes 1 after incrementing)
- After each jump, the offset at the **source position** increases by 1
- This modification persists for subsequent visits to that instruction
- Exit occurs when the calculated next position falls outside the list (position < 0 or position >= list length)

## Example Walkthrough
Given the list: `[0, 3, 0, 1, -3]`

| Step | Position | Offset | Action | List State After |
|------|----------|--------|--------|------------------|
| 0 | 0 | 0 | Jump 0 positions, increment offset to 1 | `[1, 3, 0, 1, -3]` |
| 1 | 0 | 1 | Jump 1 position, increment offset to 2 | `[2, 3, 0, 1, -3]` |
| 2 | 1 | 3 | Jump 3 positions, increment offset to 4 | `[2, 4, 0, 1, -3]` |
| 3 | 4 | -3 | Jump -3 positions, increment offset to -2 | `[2, 4, 0, 1, -2]` |
| 4 | 1 | 4 | Jump 4 positions, increment offset to 5 | `[2, 5, 0, 1, -2]` |
| 5 | 5 | - | Position 5 is outside the list (length 5) - **EXIT** | - |

Result: **5 steps**

## Expected Output
A single integer representing the total number of steps taken to exit the maze.

## Output Format
Just the integer value, no additional formatting required.
