# Problem Report: Dragon Curve Checksum

## Objective
Generate data using a modified dragon curve algorithm to fill a disk of specified length, then compute a checksum of that data.

## Context
We need to generate pseudo-random data that follows a specific pattern (modified dragon curve) and then validate it with a checksum. The data must have certain properties to avoid detection.

## Input
- **Initial state**: A binary string (puzzle input: `11011110011011101`)
- **Disk length**: 272 characters

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

## Complete Example
**Initial state**: `10000`, **Disk length**: 20

1. **Generation**:
   - Round 1: `10000` → `10000011110` (11 chars, too short)
   - Round 2: `10000011110` → `10000011110010000111110` (23 chars, sufficient)
   - Truncate to 20: `10000011110010000111`

2. **Checksum**:
   - Round 1: `10000011110010000111` → `0111110101` (10 chars, even)
   - Round 2: `0111110101` → `01100` (5 chars, odd)
   - Final checksum: `01100`

## Expected Output
A binary string representing the checksum with odd length.

For the given input (`11011110011011101`) and disk length (272), output the final checksum as a string of `0`s and `1`s.
