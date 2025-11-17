# Problem Report: Elf Gift Exchange Circle

## Context
We are simulating a circular gift exchange game where elves steal presents from each other in a specific pattern until only one elf remains with all the presents.

## Objective
Determine which elf (by their starting position number) ends up with all the presents after the game completes.

## Problem Description

### Setup
- N elves are arranged in a circle, numbered from 1 to N (starting at position 1)
- Each elf initially has one present
- The game proceeds in turns, starting with Elf 1

### Rules
1. On each turn, the current elf steals all presents from the elf immediately to their left (the next elf in numerical order, wrapping around the circle)
2. When an elf has no presents, they are removed from the circle and skipped in future turns
3. The game continues until only one elf remains with all the presents

### Turn Order
- Turns proceed sequentially through the circle
- After an elf takes their turn, the next elf still in the circle (who has presents) takes their turn
- The circle wraps around (after the highest numbered elf, it goes back to the lowest numbered elf still in the game)

## Example Walkthrough (N = 5)

Initial circle: Elves 1, 2, 3, 4, 5 (each with 1 present)

- Turn 1: Elf 1 takes from Elf 2 → Elf 1 has 2 presents, Elf 2 is out
- Turn 2: Elf 3 takes from Elf 4 → Elf 3 has 2 presents, Elf 4 is out
- Turn 3: Elf 5 takes from Elf 1 → Elf 5 has 3 presents, Elf 1 is out
- Turn 4: Elf 3 takes from Elf 5 → Elf 3 has 5 presents, Elf 5 is out

Result: **Elf 3** wins

## Input
- A single integer N representing the total number of elves
- The input file contains: `3017957`

## Expected Output
- A single integer representing the position number (1 to N) of the elf who ends up with all the presents

## Notes
- This is a variant of the Josephus problem with k=2 (every second person is eliminated)
- The solution requires simulating the circular elimination process or using a mathematical formula to determine the winner
