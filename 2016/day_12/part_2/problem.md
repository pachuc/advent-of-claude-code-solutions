# Problem Report: Assembunny Code Interpreter - Part 2

## Objective
Execute the same assembunny program from Part 1, but with **register `c` initialized to `1`** instead of `0`, and determine the final value in register `a`.

## Context from Part 1
In Part 1, we implemented an interpreter for "assembunny" assembly-like code to execute a password-checking boot sequence for a monorail control system. The program operated on a virtual machine with 4 registers (a, b, c, d) all initialized to `0`, and we found that register `a` contained `318077` after execution.

## Part 2 Change
The monorail didn't start because **register `c` needs to be initialized to the position of the ignition key**. We need to re-run the same program with register `c` initialized to `1` instead of `0`.

## Input Specification
The input is the same set of assembunny instructions from Part 1 (23 lines of assembly code).

### Virtual Machine Specifications
- **Registers**: Four registers named `a`, `b`, `c`, and `d`
- **Initial State**:
  - Register `c` starts at `1` (CHANGED FROM PART 1)
  - Registers `a`, `b`, and `d` start at `0`
- **Data Type**: Registers can hold any integer value

### Instruction Set
The assembunny code supports four instructions (unchanged from Part 1):

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
   - The offset is relative to the current instruction

### Execution Rules
- Instructions execute sequentially unless a `jnz` instruction causes a jump
- Program terminates when execution moves past the last instruction
- The instruction pointer moves to the next instruction after each non-jumping instruction

## Expected Output
After executing all instructions until the program halts, output the **integer value stored in register `a`**.

## Implementation Note
The solution from Part 1 can be reused with a simple modification: change the initial value of register `c` from `0` to `1` in the registers dictionary initialization.
