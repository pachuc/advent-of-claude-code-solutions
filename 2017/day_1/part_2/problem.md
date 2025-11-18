# Problem Report: Circular Digit Sum - Halfway Around (Inverse Captcha Part 2)

## Context from Part 1

In Part 1, we solved a captcha by finding the sum of all digits that match the *next* digit in a circular sequence. We successfully solved it with an answer of 1341.

The captcha algorithm from Part 1:
- Compared each digit with the very next digit in the sequence
- The sequence was circular (last digit wraps to first)
- Summed all digits that matched their immediate neighbor

## Part 2 Objective

The captcha requirements have changed. Now we must calculate the sum of all digits that match the digit **halfway around** the circular list, not the immediate next digit.

## Input Specification

- **Format**: A single string of digits (0-9)
- **Length**: The input has an even number of elements (guaranteed by the puzzle)
- **Location**: The input can be found in `input.md`
- **Same Input**: We use the same input sequence as Part 1, but apply different matching logic

## Algorithm Requirements

1. Calculate the step size: `step = len(sequence) / 2`
2. For each digit at position `i`, compare it with the digit at position `(i + step) % len(sequence)`
3. If the digits match, add the digit's value to the running sum
4. Return the total sum

**Key Change from Part 1**: Instead of comparing position `i` with `(i + 1)`, we now compare position `i` with `(i + len/2)`

## Output Specification

- **Format**: A single integer representing the sum
- **Example outputs**:
  - Input: `1212` (length 4, step = 2)
    - Position 0 (`1`) compared with position 2 (`1`) → match, add 1
    - Position 1 (`2`) compared with position 3 (`2`) → match, add 2
    - Position 2 (`1`) compared with position 0 (`1`) → match, add 1
    - Position 3 (`2`) compared with position 1 (`2`) → match, add 2
    - Output: `6` (1 + 2 + 1 + 2 = 6)

  - Input: `1221` (length 4, step = 2)
    - Position 0 (`1`) compared with position 2 (`2`) → no match
    - Position 1 (`2`) compared with position 3 (`1`) → no match
    - Position 2 (`2`) compared with position 0 (`1`) → no match
    - Position 3 (`1`) compared with position 1 (`2`) → no match
    - Output: `0`

  - Input: `123425` (length 6, step = 3)
    - Position 0 (`1`) compared with position 3 (`4`) → no match
    - Position 1 (`2`) compared with position 4 (`2`) → match, add 2
    - Position 2 (`3`) compared with position 5 (`5`) → no match
    - Position 3 (`4`) compared with position 0 (`1`) → no match
    - Position 4 (`2`) compared with position 1 (`2`) → match, add 2
    - Position 5 (`5`) compared with position 2 (`3`) → no match
    - Output: `4`

  - Input: `123123` (length 6, step = 3) → Output: `12`

  - Input: `12131415` (length 8, step = 4) → Output: `4`

## Key Implementation Notes

- The input is **guaranteed to have an even number of elements**, so the halfway point is always an integer
- The sequence is still **circular**: positions wrap around using modulo arithmetic
- Only sum the digit when it **matches the digit halfway around**
- Each digit is checked exactly once (we don't double-count when iterating through all positions, though note that if position `i` matches position `i+step`, then position `i+step` will also match position `i` when we get to it in the iteration)
