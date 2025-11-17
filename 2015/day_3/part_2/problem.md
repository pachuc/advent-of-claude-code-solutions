# Problem Report: Santa and Robo-Santa Gift Delivery

## Context
Santa has created a robot version of himself (Robo-Santa) to help deliver presents. Both Santa and Robo-Santa start at the same location and take turns following movement instructions from a sequence of directional commands.

## Objective
Determine how many houses receive at least one present after Santa and Robo-Santa have both completed their deliveries.

## Input Specification
- A string of directional characters where each character represents a move on a 2D grid:
  - `^` = move north (up)
  - `v` = move south (down)
  - `>` = move east (right)
  - `<` = move west (left)
- Santa and Robo-Santa alternate reading from this instruction sequence:
  - Character at index 0: Santa's move
  - Character at index 1: Robo-Santa's move
  - Character at index 2: Santa's move
  - Character at index 3: Robo-Santa's move
  - And so on...

## Rules
1. Both Santa and Robo-Santa start at the same initial location
2. The starting house receives 2 presents (one from each)
3. They take turns following the instructions:
   - Santa follows instructions at even indices (0, 2, 4, ...)
   - Robo-Santa follows instructions at odd indices (1, 3, 5, ...)
4. Each position they visit receives at least one present
5. If both visit the same house, that house still counts as only one house that received "at least one present"

## Output Specification
A single integer representing the total number of unique houses that receive at least one present.

## Examples

### Example 1: `^v`
- Santa: starts at origin, moves north to position (0,1)
- Robo-Santa: starts at origin, moves south to position (0,-1)
- Houses visited: (0,0), (0,1), (0,-1) = **3 houses**

### Example 2: `^>v<`
- Santa: origin → north (0,1) → south back to (0,0)
- Robo-Santa: origin → east (1,0) → west back to (0,0)
- Houses visited: (0,0), (0,1), (1,0) = **3 houses**

### Example 3: `^v^v^v^v^v`
- Santa: repeatedly moves north: (0,0) → (0,1) → (0,2) → (0,3) → (0,4) → (0,5)
- Robo-Santa: repeatedly moves south: (0,0) → (0,-1) → (0,-2) → (0,-3) → (0,-4)
- Houses visited: (0,-4), (0,-3), (0,-2), (0,-1), (0,0), (0,1), (0,2), (0,3), (0,4), (0,5) = **11 houses**

## Algorithm Approach
1. Track positions for both Santa and Robo-Santa, both starting at origin (0,0)
2. Use a set to store all unique positions visited
3. Add the starting position to the set
4. Iterate through the instruction string:
   - Even indices: update Santa's position and add to set
   - Odd indices: update Robo-Santa's position and add to set
5. Return the size of the set
