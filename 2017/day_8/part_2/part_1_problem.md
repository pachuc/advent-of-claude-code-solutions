# Problem Report: Register Instruction Processor

## Objective
Process a series of CPU register instructions and determine the largest value in any register after all instructions have been executed.

## Context
We are assisting the CPU by computing the result of unusual register instructions. Each instruction conditionally modifies register values based on comparison conditions.

## Input Format
The input is a series of instructions, one per line, with the following format:
```
<register> <operation> <amount> if <condition_register> <comparator> <condition_value>
```

Where:
- `<register>`: the name of the register to modify (string, e.g., "a", "b", "pq", "cfa")
- `<operation>`: either "inc" (increase) or "dec" (decrease)
- `<amount>`: an integer amount to increase or decrease by (can be negative)
- `if`: keyword separator
- `<condition_register>`: the register to check in the condition
- `<comparator>`: one of: `>`, `<`, `>=`, `<=`, `==`, `!=`
- `<condition_value>`: an integer value to compare against

## Processing Rules
1. All registers start at value `0`
2. Registers are created/initialized automatically when first referenced
3. For each instruction:
   - Evaluate the condition (compare `condition_register` value with `condition_value` using the `comparator`)
   - If the condition is **true**, apply the operation to the target register
   - If the condition is **false**, skip the instruction (do not modify the register)
4. Process all instructions sequentially in the order given

## Example Walkthrough
Given these instructions:
```
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
```

Processing:
1. `b inc 5 if a > 1`: a=0, which is NOT > 1, so skip (b remains 0)
2. `a inc 1 if b < 5`: b=0, which IS < 5, so a becomes 1
3. `c dec -10 if a >= 1`: a=1, which IS >= 1, so c decreases by -10 (increases by 10), c becomes 10
4. `c inc -20 if c == 10`: c=10, which IS == 10, so c increases by -20 (decreases by 20), c becomes -10

After processing, register values are: a=1, b=0, c=-10
The largest value is **1**.

## Expected Output
A single integer representing the **largest value in any register** after completing all instructions.

## Implementation Notes
- Register names are arbitrary strings determined from the input
- The `dec` operation with a negative amount results in an increase (e.g., `dec -10` increases by 10)
- The `inc` operation with a negative amount results in a decrease (e.g., `inc -20` decreases by 20)
- Only registers that pass their condition check are modified
- The final answer is the maximum value across all registers after all instructions complete
