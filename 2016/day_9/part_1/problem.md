# Problem Report: Decompression Algorithm

## Context
This problem involves decompressing a file that has been compressed using an experimental compression format. The format uses markers to indicate sequences of characters that should be repeated.

## Objective
Calculate the **decompressed length** of a compressed string without actually constructing the full decompressed output.

## Input Format
- A single string containing compressed data
- The string may contain:
  - Regular characters (A-Z)
  - Compression markers in the format `(AxB)` where:
    - `A` = number of characters to take after the marker
    - `B` = number of times to repeat those characters
  - Whitespace (which should be ignored)

## Decompression Rules

### Basic Marker Processing
1. When encountering a marker `(AxB)`:
   - Take the next `A` characters immediately following the marker
   - These `A` characters should be repeated `B` times in the output
   - The marker itself is NOT included in the decompressed output
   - After processing, continue reading from after the repeated data

### Important Constraint
2. **No Recursive Processing**: Characters within a data section referenced by a marker are treated as literal data, NOT as markers, even if they look like markers (e.g., contain parentheses).

### Whitespace Handling
3. Whitespace should be ignored and not counted in the decompressed length.

## Examples

| Input | Decompressed Output | Decompressed Length |
|-------|---------------------|---------------------|
| `ADVENT` | `ADVENT` | 6 |
| `A(1x5)BC` | `ABBBBBC` | 7 |
| `(3x3)XYZ` | `XYZXYZXYZ` | 9 |
| `A(2x2)BCD(2x2)EFG` | `ABCBCDEFEFG` | 11 |
| `(6x1)(1x3)A` | `(1x3)A` | 6 |
| `X(8x2)(3x3)ABCY` | `X(3x3)ABC(3x3)ABCY` | 18 |

### Example Explanations

**Example 5**: `(6x1)(1x3)A`
- The marker `(6x1)` means "take the next 6 characters and repeat 1 time"
- The next 6 characters are `(1x3)A`
- Even though `(1x3)` looks like a marker, it's within the data section, so it's treated as literal text
- Result: `(1x3)A` with length 6

**Example 6**: `X(8x2)(3x3)ABCY`
- Start with `X`
- The marker `(8x2)` means "take the next 8 characters and repeat 2 times"
- The next 8 characters are `(3x3)ABC`
- Repeat them twice: `(3x3)ABC(3x3)ABC`
- Then continue with `Y`
- Result: `X(3x3)ABC(3x3)ABCY` with length 18
- Note: The `(3x3)` markers in the output are NOT processed because they were part of a data section

## Expected Output
A single integer representing the total length of the decompressed string, excluding whitespace.

## Algorithm Requirements
- Parse the compressed string from left to right
- When a marker is found, extract the parameters and calculate the contribution to the total length
- Skip over the specified number of characters after processing each marker
- Do NOT recursively process markers within data sections
- Ignore all whitespace in length calculations
