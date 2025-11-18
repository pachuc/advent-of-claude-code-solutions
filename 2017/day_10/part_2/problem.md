# Problem Report: Knot Hash Algorithm - Full Implementation (Part 2)

## Objective
Implement the complete Knot Hash algorithm, which extends Part 1's circular list reversal algorithm to create a cryptographic-style hash function. The goal is to compute the final 32-character hexadecimal Knot Hash of the input string.

## Context from Part 1
Part 1 implemented a single round of the Knot Hash algorithm:
- Started with a list of numbers 0-255
- Processed a sequence of length values, reversing circular sections of the list
- Maintained a current position and skip size that incremented with each operation
- Part 1's answer was 38628 (the product of the first two elements after one round)

## Part 2 Extensions
Part 2 transforms the algorithm from a single round into a full hash function with multiple rounds and additional processing steps.

## Input

### Input Format Change
**IMPORTANT**: The input is no longer parsed as comma-separated integers. Instead:
- Treat the input as a **string of ASCII characters**
- Convert each character to its ASCII code value
- Ignore any leading or trailing whitespace

Example:
- Input string: `1,2,3`
- ASCII codes: `49,44,50,44,51` (ASCII for '1', ',', '2', ',', '3')

### Input from input.md
The actual input string is: `130,126,1,11,140,2,255,207,18,254,246,164,29,104,0,224`

### Standard Length Suffix
After converting the input string to ASCII codes, **append these fixed values** to the sequence:
`17, 31, 73, 47, 23`

Example for input `1,2,3`:
- ASCII codes: `49,44,50,44,51`
- Final sequence: `49,44,50,44,51,17,31,73,47,23`

## Algorithm

### Step 1: Prepare Length Sequence
1. Read the input string and strip leading/trailing whitespace
2. Convert each character to its ASCII code
3. Append the standard suffix: `17, 31, 73, 47, 23`

### Step 2: Run 64 Rounds of Knot Hash
Using the same algorithm from Part 1, but with critical changes:

**Initial State (before round 1):**
- List: Numbers from 0 to 255 (256 elements)
- Current Position: 0
- Skip Size: 0

**For each of 64 rounds:**
1. Process each length in the sequence (including the suffix):
   - Reverse the circular section starting at current position with the given length
   - Move current position forward by `length + skip_size` (with wrapping)
   - Increment skip size by 1

**CRITICAL**: The current position and skip size are **preserved across rounds**. Do NOT reset them between rounds.

### Step 3: Create Dense Hash from Sparse Hash
After all 64 rounds, the list contains the "sparse hash" (256 numbers).

Convert to "dense hash" (16 numbers):
1. Divide the 256-element sparse hash into 16 blocks of 16 elements each
2. For each block, XOR all 16 numbers together to get one output number
3. The result is 16 numbers (each between 0-255)

Example:
- Block 1: elements[0:16] → XOR them all together → dense[0]
- Block 2: elements[16:32] → XOR them all together → dense[1]
- ...
- Block 16: elements[240:256] → XOR them all together → dense[15]

### Step 4: Convert to Hexadecimal String
1. Take each of the 16 numbers in the dense hash
2. Convert each to a 2-digit hexadecimal string (lowercase)
3. Use leading zeros if necessary (e.g., 7 becomes "07")
4. Concatenate all 16 hex strings together

Result: A 32-character hexadecimal string (0-9, a-f)

## Expected Output

A single 32-character hexadecimal string representing the Knot Hash.

## Examples

### Example Hashes
- Empty string `""` → `a2582a3a0e66e6e86e3812dcb672a272`
- `AoC 2017` → `33efeb34ea91902bb2f59c9920caa6cd`
- `1,2,3` → `3efbe78a8d82f29979031a4aa0b16a9d`
- `1,2,4` → `63960835bcdc130f0b66d7ff4f6a5a8e`

### XOR Example
If the first 16 elements of sparse hash are:
`65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22`

Then: `65 ^ 27 ^ 9 ^ 1 ^ 4 ^ 3 ^ 40 ^ 50 ^ 91 ^ 7 ^ 6 ^ 0 ^ 2 ^ 5 ^ 68 ^ 22 = 64`

The first element of the dense hash would be 64, which converts to hexadecimal as "40".

## Output Format

A single lowercase hexadecimal string of exactly 32 characters (0-9, a-f).

## Key Differences from Part 1

1. **Input parsing**: ASCII codes instead of comma-separated integers
2. **Length suffix**: Always append `17, 31, 73, 47, 23` to the sequence
3. **Multiple rounds**: 64 rounds instead of 1
4. **State persistence**: current_position and skip_size carry across rounds
5. **Dense hash**: XOR every 16 elements to reduce 256 → 16 numbers
6. **Output format**: 32-character hexadecimal string instead of integer product
