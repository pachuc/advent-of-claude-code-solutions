# Problem Report: Santa's Basement Entry Position

## Objective
Find the **position** of the first character in a sequence of instructions that causes Santa to enter the basement (floor -1).

## Context
Santa is following instructions to navigate between floors in a building:
- An opening parenthesis `(` means go up one floor
- A closing parenthesis `)` means go down one floor
- Santa starts at floor 0 (ground floor)
- The basement is floor -1

We need to determine at which character position Santa first reaches floor -1.

## Input
A single string consisting of parentheses characters `(` and `)`.

The input can be found in `input.md` and consists of a long sequence of these characters.

## Output
A single integer representing the **position** of the first character that causes Santa to enter the basement (floor -1).

**Important:** Character positions are 1-indexed (the first character is at position 1, not 0).

## Examples
1. Input: `)`
   - Output: `1`
   - Explanation: The first character immediately takes Santa from floor 0 to floor -1

2. Input: `()())`
   - Output: `5`
   - Explanation:
     - Position 1: `(` → floor 1
     - Position 2: `)` → floor 0
     - Position 3: `(` → floor 1
     - Position 4: `)` → floor 0
     - Position 5: `)` → floor -1 (first time in basement)

## Algorithm Requirements
1. Start at floor 0
2. Process each character sequentially from left to right
3. For each character:
   - If `(`: increment floor by 1
   - If `)`: decrement floor by 1
   - Check if floor == -1
4. Return the 1-indexed position of the first character that results in floor -1
