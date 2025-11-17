# Problem Report: Password Unscrambler (Part 2)

## Objective
Implement the **reverse** of the password scrambling function from Part 1. Given a scrambled password and the list of scrambling operations, determine the original unscrambled password by reversing the scrambling process.

## Context from Part 1
In Part 1, we implemented a password scrambler that applies a series of operations to transform an initial password string. We successfully scrambled `abcdefgh` into `fdhbcgea` using the operations in the input file.

Now, in Part 2, we discover that we cannot modify the password file on the system. Instead, we need to **un-scramble** an existing password by reversing the scrambling process.

## The Challenge
We need to reverse the scrambling process. This means:
- Apply the operations in **reverse order** (from last to first)
- For each operation, apply its **inverse operation**

## Input
1. **Scrambled password**: `fbgdceah` (the password we need to unscramble)
2. **List of scrambling operations**: The same sequence of operations from Part 1 (100 operations in the input file)

## Required Output
A single string representing the **original unscrambled password** before the scrambling operations were applied.

**Format**: Plain text string (8 characters)

## Operation Inversions

To reverse the scrambling process, we need to invert each operation:

### 1. Swap Position (Self-Inverse)
- **Forward**: `swap position X with position Y`
- **Reverse**: `swap position X with position Y` (same operation)
- Swapping the same positions again undoes the swap

### 2. Swap Letter (Self-Inverse)
- **Forward**: `swap letter X with letter Y`
- **Reverse**: `swap letter X with letter Y` (same operation)
- Swapping the same letters again undoes the swap

### 3. Rotate Left/Right (Inverse with Opposite Direction)
- **Forward**: `rotate left X steps`
- **Reverse**: `rotate right X steps`
- **Forward**: `rotate right X steps`
- **Reverse**: `rotate left X steps`

### 4. Rotate Based on Letter Position (Complex Inverse)
- **Forward**: `rotate based on position of letter X`
  - Find index of letter X (before rotation)
  - Rotate right: 1 + index + (1 if index >= 4 else 0)
- **Reverse**: This is the most complex operation to reverse
  - Given the current position of letter X after rotation, we need to find its original position
  - Then rotate left by the appropriate amount
  - **Challenge**: The mapping is not straightforward because different original positions can result in different rotation amounts
  - **Solution approaches**:
    - Try all possible original positions (brute force for 8 positions)
    - Build a lookup table mapping post-rotation positions to pre-rotation positions
    - For a string of length 8, test which original position would result in the current position after the forward rotation

### 5. Reverse Positions (Self-Inverse)
- **Forward**: `reverse positions X through Y`
- **Reverse**: `reverse positions X through Y` (same operation)
- Reversing the same range again undoes the reversal

### 6. Move Position (Inverse with Swapped Indices)
- **Forward**: `move position X to position Y`
- **Reverse**: `move position Y to position X`
- If forward moved from X to Y, reverse moves from Y back to X

## Algorithm

1. Start with the scrambled password: `fbgdceah`
2. Read all operations from the input file
3. Process operations in **reverse order** (from last to first)
4. For each operation, apply its **inverse operation**:
   - Parse the operation to determine its type
   - Apply the appropriate inverse transformation
   - Update the password string
5. After processing all operations in reverse, the result is the original unscrambled password

## Special Consideration: Rotate Based on Letter Position

The trickiest operation to reverse is "rotate based on position of letter X". For a string of length 8:

**Forward rotation amounts by original position:**
- Position 0: rotate right 1 (1 + 0 + 0)
- Position 1: rotate right 2 (1 + 1 + 0)
- Position 2: rotate right 3 (1 + 2 + 0)
- Position 3: rotate right 4 (1 + 3 + 0)
- Position 4: rotate right 6 (1 + 4 + 1)
- Position 5: rotate right 7 (1 + 5 + 1)
- Position 6: rotate right 8 (1 + 6 + 1)
- Position 7: rotate right 9 (1 + 7 + 1)

**After rotating, the letter ends up at:**
- Was at 0, rotated right 1 → now at 1
- Was at 1, rotated right 2 → now at 3
- Was at 2, rotated right 3 → now at 5
- Was at 3, rotated right 4 → now at 7
- Was at 4, rotated right 6 → now at 2
- Was at 5, rotated right 7 → now at 4
- Was at 6, rotated right 8 → now at 6
- Was at 7, rotated right 9 → now at 0

**Reverse mapping (current position → rotate left amount to undo):**
- Now at 0 → was at 7 → rotate left 1
- Now at 1 → was at 0 → rotate left 1
- Now at 2 → was at 4 → rotate left 2
- Now at 3 → was at 1 → rotate left 2
- Now at 4 → was at 5 → rotate left 3
- Now at 5 → was at 2 → rotate left 3
- Now at 6 → was at 6 → rotate left 4
- Now at 7 → was at 3 → rotate left 4

## Expected Output Format
The final unscrambled password as a plain text string (8 characters).

## Validation
The result should:
- Be 8 characters long
- Contain the letters a through h (each exactly once)
- When passed through the forward scrambling process with the same operations, should produce `fbgdceah`
