# Problem Report: Register Instruction Processor - Part 2

## Part 1 Context
In Part 1, we processed a series of CPU register instructions and found the largest value in any register **after all instructions completed**. The answer was 5221.

Each instruction has the format:
```
<register> <operation> <amount> if <condition_register> <comparator> <condition_value>
```

All registers start at 0, and instructions are processed sequentially. Each instruction only modifies its target register if its condition evaluates to true.

## Part 2 Objective
Find the **highest value held in any register at any point during the entire execution process** (not just the final state).

## Key Difference from Part 1
- **Part 1**: Track only the final maximum value after all instructions complete
- **Part 2**: Track the maximum value ever reached during execution (across all intermediate states)

## Example
Given the same instructions from Part 1:
```
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
```

Processing step-by-step:
1. `b inc 5 if a > 1`: Condition false, b stays 0. Max so far: 0
2. `a inc 1 if b < 5`: Condition true, a becomes 1. Max so far: 1
3. `c dec -10 if a >= 1`: Condition true, c becomes 10. **Max so far: 10**
4. `c inc -20 if c == 10`: Condition true, c becomes -10. Max so far: still 10

Final register values: a=1, b=0, c=-10
**Highest value ever held during execution: 10** (in register c after instruction 3)

Note: The final maximum is 1, but the highest value *during* execution was 10.

## Input Format
Same as Part 1: A series of instructions, one per line, with format:
```
<register> <operation> <amount> if <condition_register> <comparator> <condition_value>
```

## Processing Rules
1. All registers start at value `0`
2. Process instructions sequentially in order
3. For each instruction:
   - Evaluate the condition
   - If true, apply the operation to the target register
   - **After each modification, track if this creates a new maximum value**
4. Return the highest value observed across all register states throughout execution

## Expected Output
A single integer representing the **highest value ever held in any register during the entire execution process**.

## Implementation Notes
- This requires tracking the maximum value continuously during execution, not just checking the final state
- After each register modification (when a condition is true), check if the new value exceeds the current maximum
- The algorithm from Part 1 can be adapted by adding a running maximum tracker that updates after each successful instruction
