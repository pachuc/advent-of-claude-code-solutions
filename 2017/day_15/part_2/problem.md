# Problem Report: Dueling Generators (Part 2 - With Filtering)

## Objective
Calculate how many times the lowest 16 bits of two pseudo-random number generators match after generating 5 million pairs of **filtered** values.

## Context from Part 1
In Part 1, two generators (A and B) produced sequences of numbers that a judge compared. The judge examined only the lowest 16 bits of each pair and counted matches. The generators produced values in lockstep - both generated their next value, then the judge compared them.

**Part 1 Result**: With starting values A=277 and B=349, after 40 million unfiltered pairs, there were 592 matches.

## Key Changes in Part 2
The generators now filter their output before giving values to the judge:
- **Generator A**: Only provides values that are multiples of 4
- **Generator B**: Only provides values that are multiples of 8

The generators still produce the same internal sequence of values using the same algorithm, but they **skip values** that don't meet their criteria and only hand acceptable values to the judge.

**Important**: The generators work independently. Generator A might generate 10 internal values before finding one that's a multiple of 4, while Generator B might find a multiple of 8 on its first try. The judge then compares the first acceptable value from A with the first acceptable value from B, the second with the second, etc.

## Generator Algorithm (Same as Part 1)
Both generators follow the same internal algorithm:

1. Start with an initial "starting value" (given in input)
2. To generate the next value:
   - Take the previous value
   - Multiply it by a generator-specific factor:
     - **Generator A factor**: 16807
     - **Generator B factor**: 48271
   - Calculate: `(previous_value * factor) % 2147483647`
   - The remainder becomes the next value
3. **NEW**: Only provide the value to the judge if it meets the criteria:
   - Generator A: value % 4 == 0
   - Generator B: value % 8 == 0

## Input
Two starting values:
- Generator A starts with: **277**
- Generator B starts with: **349**

## Process
1. Each generator independently produces values using the algorithm above
2. Each generator filters its values:
   - Generator A keeps only multiples of 4
   - Generator B keeps only multiples of 8
3. The judge compares 5,000,000 pairs of filtered values:
   - For each pair: compare the lowest 16 bits
   - If they match exactly, increment a counter
4. The generators operate independently - they only synchronize when handing values to the judge

## Output
A single integer: the total count of pairs where the lowest 16 bits matched.

## Example Verification
With starting values A=65 and B=8921 (from original example):
- First 5 **filtered** pairs are:

```
--Gen. A--  --Gen. B--
1352636452  1233683848
1992081072   862516352
 530830436  1159784568
1980017072  1616057672
 740335192   412269392
```

- None of these first 5 pairs match in the lowest 16 bits
- The first match occurs at the 1056th pair
- After 5 million filtered pairs with these example values, the total count would be 309

## Technical Notes
- The modulo value `2147483647` is 2^31 - 1 (a Mersenne prime)
- "Lowest 16 bits" means the rightmost 16 bits in binary representation
- The comparison is for exact equality of these 16 bits (as binary/integer values)
- To check if a value is a multiple of 4: `value % 4 == 0`
- To check if a value is a multiple of 8: `value % 8 == 0`
- Each generator must continue generating until it finds a value meeting its criteria
- The number of pairs to compare is now **5 million** (reduced from 40 million in Part 1)
