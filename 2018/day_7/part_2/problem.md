# Problem Report: Parallel Task Execution with Multiple Workers

## Context from Part 1
In Part 1, we needed to determine the correct order to assemble a sleigh by completing a series of steps that have dependencies (certain steps must be completed before others can begin). We solved this using a topological sort with alphabetical tie-breaking.

**Part 1 Answer**: `GRTAHKLQVYWXMUBCZPIJFEDNSO`

This was the sequential order when one worker completes steps one at a time.

## Part 2 Objective
Now we need to calculate **how long it takes** to complete all steps when **multiple workers can work in parallel**. Instead of finding the order, we need to find the total time duration.

## Key Changes from Part 1
1. **Multiple workers**: 5 workers can work simultaneously (instead of 1 sequential worker)
2. **Steps take time**: Each step has a duration based on its letter
3. **Parallel execution**: Workers can begin multiple available steps at the same time
4. **Output changes**: Instead of a string showing order, we need the total time in seconds

## Input Format
Same as Part 1 - multiple lines describing dependencies:
```
Step X must be finished before step Y can begin.
```

Where:
- `X` is a prerequisite step (single letter)
- `Y` is a dependent step (single letter)

## Time Calculation Rules

### Step Duration
Each step takes **60 seconds plus an amount corresponding to its letter**:
- A = 60 + 1 = 61 seconds
- B = 60 + 2 = 62 seconds
- C = 60 + 3 = 63 seconds
- ...
- Z = 60 + 26 = 86 seconds

Formula: `duration = 60 + (letter_position_in_alphabet)`

### Worker Rules
- **5 workers** are available
- Workers can work on different steps simultaneously
- When multiple steps are available, workers should begin them in **alphabetical order**
- A step is only "available" when ALL of its prerequisites have been **completed** (not just started)
- No time is required between steps
- Workers become idle (`.`) when they finish their current task and no steps are available

## Example (Simplified Version)

The puzzle provides a simplified example with:
- **2 workers** (instead of 5)
- **Base time of 0** (instead of 60), so A=1 second, B=2 seconds, etc.

Using the same dependencies from Part 1 example:
```
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
```

Execution timeline:
```
Second   Worker 1   Worker 2   Done
   0        C          .
   1        C          .
   2        C          .
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE
```

In this simplified example, the answer is **15 seconds**.

## Output Format
A single integer representing the total time in seconds to complete all steps.

## Algorithm Requirements

The solution should simulate the parallel execution:

1. **Track worker state**: Each worker can be idle or working on a specific step with a remaining time
2. **Track available steps**: Steps whose prerequisites are all completed
3. **Assign work**: When workers are idle and steps are available, assign steps in alphabetical order
4. **Advance time**: Move forward second by second (or jump to next event)
5. **Mark completion**: When a step finishes, mark it complete and update which steps become available
6. **Continue until done**: Repeat until all steps are completed

Key considerations:
- A step becomes available only when all prerequisites are **completed** (fully finished)
- When assigning work at the same moment, prioritize alphabetically
- Track the current second/time throughout execution
- Return the time when the last step completes

## Actual Problem Parameters
- **5 workers** (not 2)
- **60 + letter_value** seconds per step (not 0 + letter_value)
