# Problem Report: Elf Present Delivery (Part 2)

## Context
This is Part 2 of an Advent of Code puzzle about elves delivering presents to houses. In this variation, the elves have updated delivery rules.

## What We Are Trying to Solve
We need to find the lowest house number that receives at least a target number of presents, given new delivery constraints where each elf has limited delivery capacity.

## Input
- A single integer representing the minimum number of presents required: `34000000`

## Algorithm Requirements

### Delivery Rules
1. **Elf Numbering**: Elves are numbered starting from 1, 2, 3, etc.
2. **House Visits**: Each elf visits houses whose numbers are multiples of their elf number
   - Elf 1 visits houses 1, 2, 3, 4, 5, ...
   - Elf 2 visits houses 2, 4, 6, 8, 10, ...
   - Elf 3 visits houses 3, 6, 9, 12, 15, ...
   - And so on...
3. **Delivery Limit**: Each elf stops after delivering to exactly **50 houses** (NEW CONSTRAINT)
4. **Presents per Visit**: Each elf delivers presents equal to **11 times their elf number** at each house they visit
   - Elf 1 delivers 11 presents per house
   - Elf 2 delivers 22 presents per house
   - Elf 3 delivers 33 presents per house
   - And so on...

### Key Differences from Part 1
- Elves now have a maximum delivery limit of 50 houses each
- Present multiplier increased from 10 to 11

### Calculation Example
For a given house number N, the total presents it receives is:
- Sum of (11 × elf_number) for all elves that visit house N
- Where an elf visits house N if:
  - N is divisible by elf_number, AND
  - N / elf_number ≤ 50 (the elf hasn't exceeded their 50-house limit)

## Expected Output
A single integer: the lowest house number that receives at least `34000000` presents.

## Output Format
Just the integer house number (no additional formatting required).
