# Problem Report: Assembunny Code Interpreter with Toggle Instruction

## Objective
We need to build an assembunny code interpreter that executes a series of assembly-like instructions and returns the final value in register `a`. This interpreter will simulate a keypad logic circuit that determines what code should be sent to a safe.

## Context
The code uses an assembunny architecture (similar to a previous monorail computer implementation) but with an additional `tgl` (toggle) instruction that can modify other instructions during runtime.

## Input
- **Initial register state**: Register `a` starts with the value `7` (representing "eggs" from the puzzle context). All other registers (`b`, `c`, `d`) start at `0`.
- **Program instructions**: A series of assembunny instructions provided in the input file, including:
  - `cpy x y` - copies value `x` (either an integer or register value) into register `y`
  - `inc x` - increments register `x` by 1
  - `dec x` - decrements register `x` by 1
  - `jnz x y` - jumps `y` instructions forward (positive) or backward (negative) if `x` is not zero
  - `tgl x` - toggles the instruction at offset `x` from the current instruction

## Instruction Set Details

### Standard Instructions
- `cpy x y`: Copy value from `x` to register `y` (`x` can be a number or register)
- `inc x`: Increment register `x`
- `dec x`: Decrement register `x`
- `jnz x y`: Jump `y` instructions if `x` is not zero (`x` can be a number or register, `y` can be a number or register)

### Toggle Instruction (`tgl x`)
The `tgl x` instruction modifies the instruction located `x` positions away from it:
- **For one-argument instructions**:
  - `inc` becomes `dec`
  - Any other one-argument instruction (including `dec`) becomes `inc`
- **For two-argument instructions**:
  - `jnz` becomes `cpy`
  - Any other two-argument instruction (including `cpy`) becomes `jnz`

### Toggle Rules
1. The arguments of toggled instructions remain unchanged
2. If toggle attempts to modify an instruction outside the program bounds, nothing happens
3. If toggling creates an invalid instruction (e.g., `cpy 1 2` where destination is not a register), skip that instruction when execution reaches it
4. If `tgl` toggles itself, the resulting instruction is not executed until the next time it's reached

## Expected Output
A single integer value: the final value in register `a` after all instructions have been executed.

## Example
Given this program with register `a` starting at `2`:
```
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
```

Execution trace:
1. `cpy 2 a`: register `a` = 2
2. First `tgl a`: toggles instruction 2 positions ahead (line 4: `tgl a` → `inc a`)
3. Second `tgl a`: toggles instruction 2 positions ahead (line 5: `cpy 1 a` → `jnz 1 a`)
4. Line 4 is now `inc a`: register `a` = 3
5. Line 5 is now `jnz 1 a`: jumps 3 instructions ahead (exits program)

Final result: `a` = **3**

## Implementation Requirements
1. Initialize registers: `a=7`, `b=0`, `c=0`, `d=0`
2. Parse and execute each instruction sequentially
3. Handle dynamic instruction modification via `tgl`
4. Skip invalid instructions (e.g., `cpy` with non-register destination)
5. Return the final value of register `a`
