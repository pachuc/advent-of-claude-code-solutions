# Problem Report: Assembunny Code Interpreter

## Objective
Implement an interpreter for "assembunny" assembly-like code and execute a program to determine the final value in register `a`.

## Context
We need to execute a password-checking boot sequence for a monorail control system. The code operates on a simple virtual machine with 4 registers and a small instruction set.

## Input Specification
The input is a series of assembunny instructions, one per line. The input file contains approximately 23 lines of instructions.

### Virtual Machine Specifications
- **Registers**: Four registers named `a`, `b`, `c`, and `d`
- **Initial State**: All registers start at `0`
- **Data Type**: Registers can hold any integer value

### Instruction Set
The assembunny code supports four instructions:

1. **`cpy x y`** - Copy instruction
   - Copies value `x` into register `y`
   - `x` can be either an integer literal or a register name
   - `y` must be a register name

2. **`inc x`** - Increment instruction
   - Increases the value of register `x` by 1
   - `x` must be a register name

3. **`dec x`** - Decrement instruction
   - Decreases the value of register `x` by 1
   - `x` must be a register name

4. **`jnz x y`** - Jump if not zero instruction
   - If `x` is not zero, jump `y` instructions relative to the current position
   - `x` can be either an integer literal or a register name
   - `y` can be either an integer literal or a register name
   - Positive `y` values jump forward, negative values jump backward
   - The offset is relative to the current instruction (e.g., offset `-1` goes to the previous instruction, offset `2` skips the next instruction)

### Execution Rules
- Instructions execute sequentially unless a `jnz` instruction causes a jump
- Program terminates when execution moves past the last instruction
- The instruction pointer moves to the next instruction after each non-jumping instruction

## Expected Output
After executing all instructions until the program halts, output the **integer value stored in register `a`**.

## Example
Given the program:
```
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
```

Execution trace:
1. `cpy 41 a` → register `a` = 41
2. `inc a` → register `a` = 42
3. `inc a` → register `a` = 43
4. `dec a` → register `a` = 42
5. `jnz a 2` → register `a` is 42 (not zero), so jump forward 2 instructions (skip the next `dec a`)
6. Program ends

**Result**: Register `a` contains `42`
