# Problem Report: Password Scrambler

## Objective
Implement a password scrambling function that applies a series of operations to transform an initial password string. The goal is to determine the final scrambled result after applying all operations in sequence.

## Context
We are breaking into a computer system that uses a scrambling function to store passwords. We need to generate our own scrambled password by implementing the scrambler so we can add it to the system.

## Input
1. **Initial password string**: `abcdefgh` (8 characters)
2. **List of scrambling operations**: A sequence of operations provided in the input file, each operation on a separate line

## Operations

The scrambler supports six types of operations that modify the string:

### 1. Swap Position
- **Format**: `swap position X with position Y`
- **Behavior**: Swap the characters at index X and index Y (0-indexed)

### 2. Swap Letter
- **Format**: `swap letter X with letter Y`
- **Behavior**: Swap all occurrences of character X with character Y (regardless of position)

### 3. Rotate Left/Right
- **Format**: `rotate left X steps` or `rotate right X steps`
- **Behavior**: Rotate the entire string X positions in the specified direction
  - Right rotation: characters move right, rightmost wraps to leftmost
  - Left rotation: characters move left, leftmost wraps to rightmost
  - Example: `abcd` rotated right 1 step → `dabc`

### 4. Rotate Based on Letter Position
- **Format**: `rotate based on position of letter X`
- **Behavior**: Rotate the string to the right based on the index of letter X
  - Find the index of letter X in the current string (before rotation)
  - Rotate right: 1 + index + (1 additional if index ≥ 4)
  - Example: If letter is at index 1, rotate right 2 times (1 + 1 + 0)
  - Example: If letter is at index 4, rotate right 6 times (1 + 4 + 1)

### 5. Reverse Positions
- **Format**: `reverse positions X through Y`
- **Behavior**: Reverse the substring from index X to index Y (inclusive)

### 6. Move Position
- **Format**: `move position X to position Y`
- **Behavior**: Remove the character at index X, then insert it at index Y
  - The character is removed first, then inserted at the new position

## Processing Algorithm
1. Start with the initial password string: `abcdefgh`
2. Read each operation from the input file in order
3. Apply each operation sequentially to the string
4. Each operation modifies the string, which becomes the input for the next operation

## Expected Output
A single string representing the final scrambled password after all operations have been applied.

**Format**: Plain text string (8 characters, no newline or special formatting required)

## Example
Starting with `abcde`, applying these operations:
1. `swap position 4 with position 0` → `ebcda`
2. `swap letter d with letter b` → `edcba`
3. `reverse positions 0 through 4` → `abcde`
4. `rotate left 1 step` → `bcdea`
5. `move position 1 to position 4` → `bdeac`
6. `move position 3 to position 0` → `abdec`
7. `rotate based on position of letter b` → `ecabd` (b at index 1: rotate right 1+1=2)
8. `rotate based on position of letter d` → `decab` (d at index 4: rotate right 1+4+1=6)

Final result: `decab`
