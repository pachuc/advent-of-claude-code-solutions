# Problem Report: Coprocessor Instruction Counter

## Objective
Count how many times the `mul` (multiply) instruction is invoked during the execution of a coprocessor assembly program.

## Context
We are debugging an experimental coprocessor that is running in debug mode. The coprocessor executes a simple assembly-like language with four instruction types. We need to track execution statistics, specifically counting `mul` instruction invocations.

## Input Format
The input is a sequence of assembly instructions, one per line. Each instruction has an operation and operands.

### Instruction Set
The coprocessor supports four instructions:

1. **`set X Y`** - Sets register `X` to the value of `Y`
2. **`sub X Y`** - Decreases register `X` by the value of `Y` (i.e., `X = X - Y`)
3. **`mul X Y`** - Multiplies the value in register `X` by the value of `Y` and stores the result in `X` (i.e., `X = X * Y`)
4. **`jnz X Y`** - Jumps with an offset of `Y`, but only if the value of `X` is not zero
   - An offset of `2` skips the next instruction
   - An offset of `-1` jumps to the previous instruction
   - An offset of `0` would create an infinite loop on the same instruction

### Operand Types
- **X**: Always a register name (a single letter from `a` to `h`)
- **Y**: Can be either:
  - A register name (single letter `a` to `h`)
  - An integer literal (positive or negative number)

### Initial State
- Eight registers named `a` through `h`
- All registers start at value `0`
- Program execution starts at the first instruction (index 0)
- Program terminates when execution moves outside the instruction range

## Expected Output
A single integer representing the total number of times the `mul` instruction was invoked during program execution.

## Task
Implement a simulator that:
1. Parses the input instructions
2. Executes the program starting from the first instruction
3. Maintains register state
4. Tracks each time a `mul` instruction is executed
5. Handles jumps correctly (relative offsets from current position)
6. Terminates when the instruction pointer goes out of bounds
7. Returns the count of `mul` instruction invocations
