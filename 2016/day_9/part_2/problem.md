# Problem Report: Recursive Decompression Algorithm (Version 2)

## Context
This is Part 2 of a decompression problem. In Part 1, we calculated the decompressed length of a file using a non-recursive compression format where markers within data sections were treated as literal text. Part 1 produced an answer of **98135**.

In Part 2, the format has been upgraded to **version 2**, which supports **recursive decompression**. This provides much more substantial compression capabilities, allowing many-gigabyte files to be stored in only a few kilobytes.

## Key Difference from Part 1
**Part 1 (Non-Recursive)**: Markers within decompressed data were treated as literal text and NOT processed as markers.

**Part 2 (Recursive)**: Markers within decompressed data ARE decompressed recursively. This means when you decompress a section referenced by a marker, you must scan that section for additional markers and process them as well.

## Objective
Calculate the **decompressed length** of a compressed string using the recursive version 2 format. Due to the potentially enormous size of the decompressed output (possibly many gigabytes), you CANNOT actually build the decompressed string - you must calculate the length mathematically.

## Input Format
- A single string containing compressed data
- The string may contain:
  - Regular characters (A-Z)
  - Compression markers in the format `(AxB)` where:
    - `A` = number of characters to take after the marker
    - `B` = number of times to repeat those characters
  - Whitespace (which should be ignored)

## Decompression Rules (Version 2)

### Recursive Marker Processing
1. When encountering a marker `(AxB)`:
   - Take the next `A` characters immediately following the marker
   - These `A` characters should be repeated `B` times in the output
   - **RECURSIVELY** process any markers within those `A` characters
   - The marker itself is NOT included in the decompressed output
   - After processing, continue reading from after the `A` characters

### Whitespace Handling
2. Whitespace should be ignored and not counted in the decompressed length.

## Examples

### Example 1: No nested markers
**Input**: `(3x3)XYZ`
- Take 3 characters: `XYZ` (no markers inside)
- Repeat 3 times: `XYZXYZXYZ`
- **Length**: 9

### Example 2: Nested markers
**Input**: `X(8x2)(3x3)ABCY`
- Start with `X` (length 1)
- Marker `(8x2)` takes 8 characters: `(3x3)ABC`
- Repeat those 8 characters 2 times, but NOW process recursively:
  - The segment `(3x3)ABC` contains a marker `(3x3)` that takes `ABC`
  - This expands to `ABCABCABC` (length 9)
  - Since we repeat this segment 2 times: 9 × 2 = 18
- Continue with `Y` (length 1)
- **Total length**: 1 + 18 + 1 = 20

### Example 3: Deeply nested markers
**Input**: `(27x12)(20x12)(13x14)(7x10)(1x12)A`
- The outer marker repeats 12 times
- Each repetition expands recursively through multiple levels
- **Final length**: 241920

### Example 4: Multiple nested markers
**Input**: `(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN`
- The outer marker takes 25 characters and repeats 3 times
- Within those 25 characters are multiple nested markers that must be recursively processed
- **Final length**: 445

## Algorithm Requirements

### Must Calculate Length Without Building String
- The decompressed output could be gigabytes in size
- You CANNOT build the actual decompressed string in memory
- You must calculate the length recursively/mathematically

### Recursive Processing Strategy
1. Parse the compressed string from left to right
2. For regular characters: add 1 to length
3. For markers `(AxB)`:
   - Extract the next `A` characters after the marker
   - **Recursively calculate the decompressed length of those A characters**
   - Multiply that recursive length by `B`
   - Add the result to the total length
4. Skip whitespace entirely

### Key Insight
When you encounter a marker `(AxB)`:
- Don't just add `A * B` to the length (that was Part 1)
- Instead, recursively calculate: `decompressed_length(next_A_characters) * B`

## Expected Output
A single integer representing the total length of the decompressed string using version 2 format, excluding whitespace.

## Comparison with Part 1
Part 1 used a simple non-recursive approach and got **98135**. Part 2's recursive processing will produce a significantly larger number due to the exponential expansion that occurs with nested markers.
