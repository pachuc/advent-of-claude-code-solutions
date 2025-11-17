# Problem Report: Computer Instruction Simulator

## Context
We need to simulate a simple computer with two registers and six basic instructions. The computer will execute a program (a list of instructions) and we need to determine the final state of the registers after execution completes.

## Objective
Find the value in register `b` after the program finishes executing.

## System Specifications

### Registers
- Two registers: `a` and `b`
- Both hold non-negative integers
- Both start with an initial value of `0`

### Instruction Set
The computer supports six instructions:

1. **`hlf r`** - Halves register `r` (integer division by 2), then moves to next instruction
2. **`tpl r`** - Triples register `r` (multiplies by 3), then moves to next instruction
3. **`inc r`** - Increments register `r` by 1, then moves to next instruction
4. **`jmp offset`** - Unconditional jump; moves to instruction at position `current_position + offset`
5. **`jie r, offset`** - Conditional jump if register `r` is even; moves to instruction at `current_position + offset` if `r` is even, otherwise moves to next instruction
6. **`jio r, offset`** - Conditional jump if register `r` equals 1; moves to instruction at `current_position + offset` if `r == 1`, otherwise moves to next instruction

### Jump Offset Format
- Offsets are always prefixed with `+` or `-` to indicate direction
- Offsets are relative to the current instruction
- Example: `jmp +1` moves to the next instruction
- Example: `jmp +0` would loop forever on the same instruction
- Example: `jmp -2` moves back 2 instructions

### Program Execution
- Instructions are executed sequentially starting from the first instruction (index 0)
- The program **exits** when it attempts to execute an instruction beyond the defined program bounds (either before the first instruction or after the last instruction)

## Input Format
The input is a list of instructions, one per line. Each instruction follows one of these patterns:
- `hlf a` or `hlf b`
- `tpl a` or `tpl b`
- `inc a` or `inc b`
- `jmp [+/-]offset` (e.g., `jmp +19`, `jmp -7`)
- `jie a, [+/-]offset` or `jie b, [+/-]offset` (e.g., `jie a, +4`)
- `jio a, [+/-]offset` or `jio b, [+/-]offset` (e.g., `jio a, +22`)

## Expected Output
A single integer: **the value in register `b`** when the program finishes executing.

## Example
Given this simple program:
```
inc a
jio a, +2
tpl a
inc a
```

Execution trace:
1. Line 0: `inc a` → register `a` becomes 1
2. Line 1: `jio a, +2` → register `a` is 1, so jump forward 2 instructions (to line 3)
3. Line 3: `inc a` → register `a` becomes 2
4. Program tries to execute line 4 (doesn't exist) → program exits

Final result: register `a` = 2

## Implementation Requirements
1. Parse the input instructions
2. Initialize registers `a` and `b` to 0
3. Maintain an instruction pointer starting at 0
4. Execute instructions sequentially, updating the instruction pointer appropriately
5. Handle jumps by modifying the instruction pointer
6. Detect program termination (instruction pointer out of bounds)
7. Return the final value of register `b`
