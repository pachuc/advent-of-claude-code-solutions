# Problem Report: Disc Timing Puzzle

## Overview
We need to find the earliest time to press a button that will allow a capsule to fall through a series of rotating discs with aligned slots.

## Problem Description
A kinetic sculpture contains rotating discs stacked vertically. When a button is pressed, a capsule drops and must pass through slot openings in each disc. Each disc:
- Has a fixed number of positions (rotating through positions 0, 1, 2, ..., n-1)
- Has only one slot at position 0
- Rotates by 1 position each second
- Pauses at each position (discrete movement, not continuous)

## Timing Mechanics
When the button is pressed at time T:
- The capsule reaches disc #1 at time T+1
- The capsule reaches disc #2 at time T+2
- The capsule reaches disc #N at time T+N
- Each disc's position at any time T is: (initial_position + T) % total_positions

For the capsule to successfully fall through, **each disc must be at position 0** when the capsule reaches it.

## Success Conditions
For the button pressed at time T, the capsule succeeds if and only if:
- Disc #1 is at position 0 at time T+1: `(disc1_initial + T + 1) % disc1_positions == 0`
- Disc #2 is at position 0 at time T+2: `(disc2_initial + T + 2) % disc2_positions == 0`
- Disc #N is at position 0 at time T+N: `(discN_initial + T + N) % discN_positions == 0`

## Input Format
Each line describes one disc in the format:
```
Disc #<number> has <positions> positions; at time=0, it is at position <initial_position>.
```

Where:
- `<number>`: The disc number (1-indexed, sequential)
- `<positions>`: Total number of positions for this disc
- `<initial_position>`: The position of the disc at time=0

Example:
```
Disc #1 has 13 positions; at time=0, it is at position 10.
Disc #2 has 17 positions; at time=0, it is at position 15.
```

## Expected Output
A single integer representing the **first time** (earliest non-negative integer) at which the button can be pressed to allow the capsule to successfully fall through all discs.

## Algorithm Approach
This is essentially a system of modular congruences. For each disc i (1-indexed):
- We need: `(initial_position[i] + T + i) % positions[i] == 0`
- Which means: `T ≡ -(initial_position[i] + i) (mod positions[i])`

The solution can be found by:
1. Testing successive time values starting from T=0
2. For each T, check if all discs will be at position 0 when the capsule reaches them
3. Return the first T that satisfies all conditions

Alternatively, this can be solved using the Chinese Remainder Theorem for a more efficient solution.
