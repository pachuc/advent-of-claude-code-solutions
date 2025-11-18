# Problem Report: Dueling Generators

## Objective
Calculate how many times the lowest 16 bits of two pseudo-random number generators match after generating 40 million pairs of values.

## Context
Two generators (A and B) produce sequences of numbers. A judge compares each pair of generated values by examining only their lowest 16 bits and counts how many times these 16-bit portions match.

## Generator Algorithm
Both generators follow the same algorithm to produce values:

1. Start with an initial "starting value" (given in input)
2. To generate the next value:
   - Take the previous value
   - Multiply it by a generator-specific factor:
     - **Generator A factor**: 16807
     - **Generator B factor**: 48271
   - Calculate: `(previous_value * factor) % 2147483647`
   - The remainder becomes the next value

## Input
Two starting values:
- Generator A starts with: **277**
- Generator B starts with: **349**

## Process
1. Generate 40,000,000 pairs of values (one from each generator)
2. For each pair:
   - Compare the lowest 16 bits of generator A's value with the lowest 16 bits of generator B's value
   - If they match exactly, increment a counter
3. The generators operate in lockstep - the judge waits for both to produce their next value before comparing

## Output
A single integer: the total count of pairs where the lowest 16 bits matched.

## Example Verification
With starting values A=65 and B=8921:
- First 5 pairs generated are:

```
--Gen. A--  --Gen. B--
   1092455   430625591
1181022009  1233683848
 245556042  1431495498
1744312007   137874439
1352636052   285222916
```

- Only the 3rd pair matches in the lowest 16 bits (both end with `1110001101001010` in binary)
- After all 40 million pairs with these example values, the total count would be 588

## Technical Notes
- The modulo value `2147483647` is 2^31 - 1 (a Mersenne prime)
- "Lowest 16 bits" means the rightmost 16 bits in binary representation
- The comparison is for exact equality of these 16 bits (as binary/integer values)
