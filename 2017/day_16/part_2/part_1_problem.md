# Problem Report: Permutation Promenade

## Objective
Simulate a dance of 16 programs and determine their final positions after executing a sequence of dance moves.

## Context
There are 16 programs named `a` through `p` that start in a line in alphabetical order:
- Position 0: `a`
- Position 1: `b`
- Position 2: `c`
- ...
- Position 15: `p`

The programs perform a dance consisting of a sequence of moves that rearrange their positions.

## Dance Move Types

There are three types of dance moves:

1. **Spin (`sX`)**: Takes `X` programs from the end of the line and moves them to the front, maintaining their relative order.
   - Example: `s3` on `abcde` → `cdeab` (the last 3 programs `cde` move to the front)

2. **Exchange (`xA/B`)**: Swaps the programs at positions `A` and `B`.
   - Example: `x3/4` on `eabcd` → `eabdc` (programs at positions 3 and 4 swap)

3. **Partner (`pA/B`)**: Swaps the programs named `A` and `B`, regardless of their positions.
   - Example: `pe/b` on `eabdc` → `baedc` (programs named `e` and `b` swap)

## Input Format
The input is a comma-separated sequence of dance moves. Each move is one of:
- `sX` where X is a number indicating how many programs to spin
- `xA/B` where A and B are position indices to exchange
- `pA/B` where A and B are program names (letters) to swap

Example input format: `s11,x10/2,s5,x1/3,pl/d,x2/5,...`

## Expected Output
A string representing the final order of programs after all dance moves have been executed.

The output should be the 16 characters representing the programs in their final positions from left to right (position 0 to position 15).

## Example Walkthrough
Starting with 5 programs `abcde`:
1. `s1` (spin 1): `eabcd`
2. `x3/4` (exchange positions 3 and 4): `eabdc`
3. `pe/b` (swap programs e and b): `baedc`

Final result: `baedc`
