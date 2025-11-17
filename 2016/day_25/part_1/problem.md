# Problem Report: Clock Signal Generator

## Objective
Find the lowest positive integer that, when used to initialize register `a`, causes an assembunny program to output an alternating clock signal pattern of `0, 1, 0, 1, 0, 1...` repeating forever.

## Context
We need to generate a clock signal - a timing pattern that alternates indefinitely between 0 and 1. The signal must start with 0 and continue the alternating pattern without deviation.

## Input
The input is an assembunny assembly-like program with the following instruction set:

### Standard Instructions
- `cpy x y` - copies value `x` (integer or register value) into register `y`
- `inc x` - increments register `x` by 1
- `dec x` - decrements register `x` by 1
- `jnz x y` - jumps `y` instructions forward/backward if `x` is not zero (can use integer or register for both parameters)

### Special Instruction
- `out x` - transmits value `x` (integer or register value) as the next output value for the clock signal

### Program Input
The assembunny program is provided in the input file (30 lines of instructions). The program takes an initial value via register `a` at startup. All other registers (`b`, `c`, `d`) start at 0.

## Expected Output
A single integer representing the lowest positive integer that should be placed in register `a` to cause the program to output the repeating pattern: `0, 1, 0, 1, 0, 1, 0, 1...` indefinitely.

## Output Format
Just the integer value, no additional formatting required.

## Constraints
- The answer must be a positive integer (> 0)
- The output pattern must alternate perfectly between 0 and 1
- The pattern must start with 0
- The pattern must repeat forever (or for a sufficiently long sequence to verify correctness)
- We need the LOWEST such integer that produces this pattern

## Implementation Notes
- The program will execute instructions sequentially unless a `jnz` instruction causes a jump
- Registers can hold integer values
- The `out` instruction produces values that form the clock signal
- We need to find the minimum input value that makes the program generate the correct alternating pattern
