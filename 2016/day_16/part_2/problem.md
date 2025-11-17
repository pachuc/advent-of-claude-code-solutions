# Problem Report: Dragon Curve Checksum - Part 2

## Objective
Generate data using a modified dragon curve algorithm to fill a **much larger disk** of specified length, then compute a checksum of that data.

## Context from Part 1
In Part 1, we successfully generated data for a disk of length 272 using a modified dragon curve algorithm and computed its checksum. The answer for Part 1 was `00000100100001100`.

**Part 2 scales up the problem significantly**: Instead of filling a disk of length 272, we now need to fill a disk of length **35651584** (over 131,000 times larger).

## Input
- **Initial state**: `11011110011011101` (same binary string as Part 1, from input.md)
- **Disk length**: **35651584** (the key change from Part 1)

## Algorithm

### Part 1: Data Generation (Modified Dragon Curve)
Repeat the following steps until the generated data is at least as long as the disk length:

1. Let "a" be the current data
2. Create a copy of "a" and call it "b"
3. Reverse the order of characters in "b"
4. Flip all bits in "b" (replace `0` with `1` and `1` with `0`)
5. The new data becomes: `a + "0" + b`

**Examples of single iterations:**
- `1` → `100`
- `0` → `001`
- `11111` → `11111000000`
- `111100001010` → `1111000010100101011110000`

**Important**: Once the generated data meets or exceeds the disk length, truncate it to exactly the disk length before proceeding to checksum calculation.

### Part 2: Checksum Calculation
Calculate the checksum for the data that fits on the disk:

1. Process the data in non-overlapping pairs of characters
2. For each pair:
   - If both characters match (`00` or `11`), output `1`
   - If characters differ (`01` or `10`), output `0`
3. This produces a new string exactly half the length of the input
4. If the resulting checksum has **even** length, repeat the checksum process on the checksum itself
5. Stop when the checksum has **odd** length

**Example (disk length 12, data `110010110100`):**
- Pairs: `11`, `00`, `10`, `11`, `01`, `00`
- Results: same, same, different, same, different, same → `110101` (length 6, even)
- Continue with `110101`: pairs `11`, `01`, `01`
- Results: same, different, different → `100` (length 3, odd)
- Final checksum: `100`

## Performance Considerations for Part 2
Given the massive disk size (35651584 characters), the solution needs to be efficient:
- The dragon curve generation will need approximately 25 iterations (since 2^25 = 33,554,432 and we start with length 17)
- String concatenation should be handled efficiently
- Memory usage could be significant (35+ MB for the data string)
- The checksum calculation will iterate multiple times until reaching odd length

## Expected Output
A binary string representing the checksum with odd length.

For the given input (`11011110011011101`) and disk length (35651584), output the final checksum as a string of `0`s and `1`s.
