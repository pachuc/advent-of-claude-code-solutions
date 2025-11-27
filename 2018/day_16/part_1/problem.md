# Problem Report: Chronal Classification - Part 1

## Context
We're analyzing a device with a CPU that has 4 registers (numbered 0-3) and 16 different opcodes. The device's manual lists the opcode names but doesn't specify which opcode number (0-15) corresponds to which operation. We need to analyze sample observations of CPU execution to determine how many samples could match multiple opcodes.

## What We Are Trying to Solve
Count how many sample observations in the input behave like **three or more** different opcodes.

## Input Format
The input consists of sample observations. Each sample has three lines followed by a blank line:

```
Before: [r0, r1, r2, r3]
opcode A B C
After:  [r0, r1, r2, r3]
```

Where:
- **Before**: The state of the 4 registers before instruction execution (array of 4 integers)
- **Instruction**: Four integers representing:
  - `opcode`: The opcode number (0-15, but we don't know which operation it represents)
  - `A`: First input parameter
  - `B`: Second input parameter
  - `C`: Output register (0-3)
- **After**: The state of the 4 registers after instruction execution (array of 4 integers)

## The 16 Opcodes

### Addition
- **addr**: register[C] = register[A] + register[B]
- **addi**: register[C] = register[A] + value B

### Multiplication
- **mulr**: register[C] = register[A] * register[B]
- **muli**: register[C] = register[A] * value B

### Bitwise AND
- **banr**: register[C] = register[A] & register[B]
- **bani**: register[C] = register[A] & value B

### Bitwise OR
- **borr**: register[C] = register[A] | register[B]
- **bori**: register[C] = register[A] | value B

### Assignment
- **setr**: register[C] = register[A] (B is ignored)
- **seti**: register[C] = value A (B is ignored)

### Greater-than Testing
- **gtir**: register[C] = 1 if value A > register[B], else 0
- **gtri**: register[C] = 1 if register[A] > value B, else 0
- **gtrr**: register[C] = 1 if register[A] > register[B], else 0

### Equality Testing
- **eqir**: register[C] = 1 if value A == register[B], else 0
- **eqri**: register[C] = 1 if register[A] == value B, else 0
- **eqrr**: register[C] = 1 if register[A] == register[B], else 0

## Task Details

For each sample observation:
1. Take the "Before" register state
2. For each of the 16 opcodes, simulate applying it with parameters A, B, C
3. Check if the result matches the "After" register state
4. Count how many opcodes produce a matching result

A sample "behaves like" an opcode if applying that opcode with the given parameters transforms the "Before" state into the "After" state.

## Expected Output
A single integer: the count of samples that behave like **three or more** opcodes.

## Example
Given this sample:
```
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
```

The instruction is `9 2 1 2` (opcode=9, A=2, B=1, C=2).

This sample matches 3 opcodes:
- **mulr**: register[2] (=1) * register[1] (=2) = 2 → stored in register[2] ✓
- **addi**: register[2] (=1) + value 1 = 2 → stored in register[2] ✓
- **seti**: value 2 → stored in register[2] ✓

Since this sample behaves like 3 opcodes, it would be counted toward the answer.
