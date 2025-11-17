# Problem Report: Bathroom Keypad Code

## Objective
Calculate a bathroom door code by following a sequence of directional instructions on a 3x3 numeric keypad.

## Context
You need to determine the code for a keypad lock. Each line of instructions corresponds to one digit of the final code. Starting from a specific position, you follow the directional commands and record the button you end up on after each line.

## Keypad Layout
```
1 2 3
4 5 6
7 8 9
```

## Input Format
The input consists of multiple lines, where each line contains a sequence of directional commands:
- `U` = move up
- `D` = move down
- `L` = move left
- `R` = move right

## Rules
1. **Starting position**: Begin at the "5" button (center of keypad)
2. **Processing instructions**:
   - Each line of instructions produces one digit of the code
   - For each subsequent line, start from where the previous line ended
3. **Movement constraints**:
   - If a move would take you off the keypad (no button exists in that direction), ignore that move and stay on the current button
4. **Output digit**: After processing all commands in a line, the button you're on becomes the next digit of the code

## Example Walkthrough
Given instructions:
```
ULL
RRDDD
LURDL
UUUUD
```

Step-by-step execution:
1. **Line 1 (ULL)**: Start at 5 → U goes to 2 → L goes to 1 → L would go off grid, stay at 1 → **Digit: 1**
2. **Line 2 (RRDDD)**: Start at 1 → R goes to 2 → R goes to 3 → D goes to 6 → D goes to 9 → D would go off grid, stay at 9 → **Digit: 9**
3. **Line 3 (LURDL)**: Start at 9 → L goes to 8 → U goes to 5 → R goes to 6 → D goes to 9 → L goes to 8 → **Digit: 8**
4. **Line 4 (UUUUD)**: Start at 8 → U goes to 5 → U goes to 2 → U would go off grid, stay at 2 → U would go off grid, stay at 2 → D goes to 5 → **Digit: 5**

**Expected output**: 1985

## Expected Output Format
The output should be a string of digits representing the bathroom code, with one digit per line of input instructions.
