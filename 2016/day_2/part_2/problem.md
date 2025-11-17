# Problem Report: Bathroom Keypad Code (Part 2)

## Context from Part 1
In Part 1, we navigated a standard 3x3 numeric keypad to determine a bathroom code:
```
1 2 3
4 5 6
7 8 9
```
We followed directional instructions (U/D/L/R), starting at button "5", and recorded the button we landed on after each line of instructions. Part 1's answer was: 19636

## Part 2 Change: New Keypad Layout
The actual bathroom keypad has a **diamond-shaped layout** instead of a simple 3x3 grid:

```
    1
  2 3 4
5 6 7 8 9
  A B C
    D
```

This keypad has several important characteristics:
- It is NOT a rectangular grid
- Valid buttons form a diamond shape
- Many positions are "empty" (no button exists there)
- Buttons can be digits (1-9) or letters (A-D)

## Objective
Calculate the bathroom code using the same directional instructions as Part 1, but with the new diamond-shaped keypad layout.

## Input Format
The input is the same as Part 1: multiple lines of directional commands
- `U` = move up
- `D` = move down
- `L` = move left
- `R` = move right

## Rules
1. **Starting position**: Begin at the "5" button (center of the diamond)
2. **Processing instructions**:
   - Each line of instructions produces one character of the code
   - For each subsequent line, start from where the previous line ended
3. **Movement constraints**:
   - If a move would take you to an empty position (no button exists), **ignore that move** and stay on the current button
   - If a move would take you off the edge of the diamond, **ignore that move** and stay on the current button
4. **Output character**: After processing all commands in a line, the button you're on becomes the next character of the code

## Example Walkthrough
Given the same instructions as Part 1:
```
ULL
RRDDD
LURDL
UUUUD
```

With the diamond keypad, the execution is:
1. **Line 1 (ULL)**: Start at 5 → U is edge, stay at 5 → L is edge, stay at 5 → L is edge, stay at 5 → **Character: 5**
2. **Line 2 (RRDDD)**: Start at 5 → R goes to 6 → R goes to 7 → D goes to B → D goes to D → D is edge, stay at D → **Character: D**
3. **Line 3 (LURDL)**: Start at D → L is edge, stay at D → U goes to B → R goes to C → D is edge, stay at C → L goes to B → **Character: B**
4. **Line 4 (UUUUD)**: Start at B → U goes to 7 → U goes to 3 → U is edge, stay at 3 → U is edge, stay at 3 → D goes to 7... wait, that doesn't match. Let me recalculate: Start at B → U goes to 7 → U goes to 3 → U is edge, stay at 3 → U is edge, stay at 3 → D goes to 7... Actually, the puzzle says the answer is 3, so: Start at B → U goes to 7 → U goes to 3 → U is edge → U is edge → D goes to 7...

Looking at the puzzle description again: "Finally, after five more moves, you end at `3`."

So starting from B: the five moves in UUUUD must end at 3.

**Expected output for example**: 5DB3

## Expected Output Format
The output should be a string of characters (digits 1-9 and letters A-D) representing the bathroom code, with one character per line of input instructions.

## Implementation Notes
The key difference from Part 1 is implementing the diamond-shaped keypad layout correctly. You'll need to:
1. Map each valid button to coordinates
2. Validate that a move destination corresponds to a valid button (not an empty space)
3. Handle hexadecimal-style button labels (A, B, C, D)
