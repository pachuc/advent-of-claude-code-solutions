# Problem Report: Assembly Code Interpreter

## Objective
We need to implement an interpreter for a simple assembly language called "Duet" and execute a program to find **the value of the recovered frequency the first time a `rcv` instruction is executed with a non-zero value**.

## Context
The assembly code operates on a set of registers (single-letter names) that each hold a single integer. All registers start with a value of 0.

## Input
The input is a series of assembly instructions, one per line. Each instruction consists of an operation code and operands. The operands can be either:
- A register (single letter like `a`, `b`, `p`, etc.)
- A literal integer value (positive or negative)

## Instruction Set

1. **`snd X`** - Plays a sound with frequency equal to the value of X
2. **`set X Y`** - Sets register X to the value of Y
3. **`add X Y`** - Increases register X by the value of Y
4. **`mul X Y`** - Multiplies register X by the value of Y (stores result in X)
5. **`mod X Y`** - Sets register X to X modulo Y (remainder after division)
6. **`rcv X`** - Recovers the frequency of the last sound played, but **only when the value of X is not zero**. If X is zero, this instruction does nothing.
7. **`jgz X Y`** - Jumps with an offset of Y, but only if the value of X is greater than zero. An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, etc.

## Execution Rules

- After a jump instruction, continue with the instruction at the jump target
- After any other instruction, continue with the next instruction
- Jumping or continuing off either end of the program terminates it
- The value of a register is the integer it contains
- The value of a number operand is that number itself

## Expected Output
A single integer representing **the frequency of the last sound played** at the time the first `rcv` instruction is executed with a non-zero value.

## Example Walkthrough

Given this program:
```
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
```

Execution:
1. Set `a` to 1
2. Add 2 to `a` (a = 3)
3. Multiply `a` by itself (a = 9)
4. Set `a` to 9 mod 5 (a = 4)
5. Play sound with frequency 4
6. Set `a` to 0
7. `rcv a` does nothing because a is 0
8. `jgz a -1` does nothing because a is not > 0
9. Set `a` to 1
10. `jgz a -2` jumps back 2 instructions (to `jgz a -1`)
11. `jgz a -1` jumps back 1 instruction (to `rcv a`)
12. `rcv a` executes with a = 1 (non-zero), recovering the last played frequency

The answer is **4** (the frequency of the last sound played).

## Implementation Requirements

The solution should:
1. Parse the input instructions
2. Maintain a dictionary/map of registers (initialized to 0)
3. Track the most recently played sound frequency
4. Execute instructions sequentially (with jumps as specified)
5. Stop execution when `rcv` is called with a non-zero value
6. Return the frequency of the last sound played at that moment
