# Problem Report: Coprocessor Optimization - Part 2

## Objective
Determine the final value left in register `h` after the coprocessor program completes execution with register `a` starting at `1` instead of `0`.

## Context from Part 1
In Part 1, we built a simulator for an experimental coprocessor that executes a simple assembly language with four instruction types:
- `set X Y` - Sets register `X` to the value of `Y`
- `sub X Y` - Decreases register `X` by the value of `Y`
- `mul X Y` - Multiplies register `X` by the value of `Y`
- `jnz X Y` - Jumps with offset `Y` if value of `X` is not zero

The coprocessor has 8 registers (`a` through `h`), all starting at `0`. When run in debug mode (Part 1), the program executed and we counted 4225 `mul` instruction invocations.

## What Changed in Part 2
The **debug mode switch** is wired to register `a`. When we flip the switch:
- Register `a` now starts at `1` (instead of `0`)
- All other registers still start at `0`
- The program becomes extremely slow/inefficient when run with this change

## The Challenge
The program is computationally expensive and won't complete in a reasonable time with direct simulation. The puzzle hints that:
1. The program is inefficiently implemented
2. We need to **optimize** or **understand what the program is computing** rather than just simulating it
3. The goal is to find what value ends up in register `h` without necessarily running every instruction

## Input Format
Same assembly program as Part 1 - a sequence of instructions using the four operations listed above.

The input program has 32 instructions total.

## Expected Output
A single integer representing the final value in register `h` after the program completes execution (with `a=1` initially).

## Task Approach
Since direct simulation is too slow, you will likely need to:
1. **Analyze the assembly code** to understand what algorithm it implements
2. **Reverse-engineer** the logic to understand what it's computing
3. **Optimize** or rewrite the algorithm in a more efficient way
4. **Calculate** the final value of register `h` directly

Common patterns to look for in these optimization puzzles:
- Nested loops that could be replaced with mathematical formulas
- Primality testing or factorization algorithms
- Counting operations that can be computed directly
- Inefficient implementations of well-known algorithms

## Notes
- The program must run to completion (until instruction pointer goes out of bounds)
- You need the value in register `h` at that point
- Simply running the Part 1 simulator with `a=1` will likely take too long
- Focus on understanding WHAT the program computes, not just HOW it computes it
