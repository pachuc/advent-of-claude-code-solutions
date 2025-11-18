# Problem Report: Turing Machine Simulator

## Context
We need to simulate a Turing machine to compute a diagnostic checksum. The Turing machine operates on an infinite tape of binary values and follows state-based rules to determine what to write, where to move, and which state to transition to next.

## Goal
Calculate the diagnostic checksum by simulating a Turing machine for a specified number of steps, then counting how many times the value `1` appears on the tape.

## Input Format
The input is a blueprint that specifies:

1. **Initial state**: The state the machine begins in (e.g., "state A")
2. **Number of steps**: How many steps to execute before taking the diagnostic checksum
3. **State definitions**: For each state, rules for what to do based on the current tape value:
   - If the current value is 0:
     - What value to write (0 or 1)
     - Which direction to move the cursor (left or right)
     - Which state to continue with next
   - If the current value is 1:
     - What value to write (0 or 1)
     - Which direction to move the cursor (left or right)
     - Which state to continue with next

### Input Example Structure
```
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  ...
```

## Turing Machine Components

1. **Tape**: An infinite tape containing binary values (0 or 1). Initially, all slots contain 0.
2. **Cursor**: A pointer that can move left or right along the tape and read/write values at its current position. Starts at position 0.
3. **States**: A set of states, each containing conditional rules based on the current value under the cursor.

## Algorithm Requirements

For each step:
1. Read the current value at the cursor position on the tape
2. Based on the current state and current value, perform the following actions (as defined in that state's rules):
   - Write a new value (0 or 1) at the cursor position
   - Move the cursor one slot left or right
   - Transition to a new state

After completing the specified number of steps:
1. Stop the machine
2. Count the total number of `1` values on the entire tape

## Expected Output
A single integer representing the diagnostic checksum: the count of how many times `1` appears on the tape after executing the specified number of steps.

For the example provided in the puzzle (6 steps with 2 states), the expected output is `3`.

## Implementation Notes
- The tape is conceptually infinite, but only a finite portion will contain non-zero values
- The cursor position can be tracked with positive and negative indices or using a data structure that allows both left and right expansion
- States should be parsed from the input and stored in a way that allows quick lookup of the rules based on current state and current value
