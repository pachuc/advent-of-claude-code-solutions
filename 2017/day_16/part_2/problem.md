# Problem Report: Permutation Promenade - Part 2

## Background from Part 1
In Part 1, we simulated a dance performed by 16 programs named `a` through `p`. The programs start in alphabetical order (positions 0-15) and execute a sequence of dance moves:

1. **Spin (`sX`)**: Rotates the last `X` programs to the front
2. **Exchange (`xA/B`)**: Swaps programs at positions `A` and `B`
3. **Partner (`pA/B`)**: Swaps programs named `A` and `B`

After executing the full sequence of dance moves once, the programs ended up in the order: **`eojfmbpkldghncia`**

## Part 2 Objective
Determine the final order of programs after they perform the **same dance sequence one billion (1,000,000,000) times**.

## Key Details
- The programs do **not** reset to the starting position (`abcdefghijklmnop`) between dances
- Each subsequent dance begins with the ending position of the previous dance
- The first dance produces the result from Part 1: `eojfmbpkldghncia`
- The second dance would begin with `eojfmbpkldghncia` and execute the same move sequence
- This continues for a total of **1 billion iterations**

## Input Format
The input is the same comma-separated sequence of dance moves used in Part 1. The input consists of thousands of moves in the format:
- `sX` - spin moves
- `xA/B` - exchange moves
- `pA/B` - partner moves

Example: `s11,x10/2,s5,x1/3,pl/d,x2/5,s9,x9/14,pa/i,...`

## Expected Output
A string representing the final order of the 16 programs after executing the dance sequence one billion times.

The output should be exactly 16 characters (the program names in their final positions from left to right).

## Important Considerations
Given the massive number of iterations (1 billion), a naive simulation approach would be computationally infeasible. The solution will likely need to:
- Detect cycles in the permutation sequence
- Use mathematical properties of permutations to avoid simulating all iterations
- Find the period/cycle length and use modulo arithmetic to jump to the final state

## Example Pattern
With a simple 5-program example (`abcde`):
- After dance 1: `baedc`
- After dance 2 (starting from `baedc`): `ceadb`
- The pattern would eventually cycle back to a previously seen state
