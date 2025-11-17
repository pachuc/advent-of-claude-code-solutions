# Problem Report: Santa's House Delivery Tracker

## Problem Overview
Santa is delivering presents on an infinite 2D grid of houses. We need to track his movements and determine how many unique houses receive at least one present.

## Context
Santa starts at an initial position and delivers a present to that starting house. An elf then provides directions via radio that tell Santa where to move next. After each move, Santa delivers another present to the house at his new location. Due to the elf's impaired state (too much eggnog), some directions cause Santa to revisit houses, meaning some houses receive multiple presents while others receive none.

## What We're Solving
Count the total number of **unique houses** that receive **at least one present** during Santa's journey.

## Input Specification
- A string of directional characters
- Each character represents a move to an adjacent house:
  - `^` = move north (up)
  - `v` = move south (down)
  - `>` = move east (right)
  - `<` = move west (left)
- The input will be a single continuous string with no spaces or delimiters
- Input can be found in `input.md`

## Output Specification
- A single integer representing the count of unique houses that received at least one present
- This count includes the starting house (where Santa begins and delivers the first present)

## Important Rules
1. Santa always starts by delivering a present at his starting location before making any moves
2. After each move, Santa delivers a present to the house at his new location
3. If Santa visits a house multiple times, it still only counts as ONE house in the final count
4. The grid is infinite (no boundary constraints)

## Example Cases

### Example 1: `>`
- Moves: Start at origin, move east once
- Houses visited: Starting house + 1 house to the east
- **Output: 2**

### Example 2: `^>v<`
- Moves: North, East, South, West (forms a square)
- Returns to starting position at the end
- Houses visited: 4 corners of a square, with starting/ending house visited twice
- **Output: 4** (unique houses)

### Example 3: `^v^v^v^v^v`
- Moves: Alternating north and south
- Santa moves back and forth between only 2 houses
- **Output: 2** (only 2 unique houses despite many moves)

## Algorithm Requirements
1. Track Santa's current position (x, y coordinates)
2. Maintain a collection of all unique house positions visited
3. Start by marking the initial position (0, 0) as visited
4. Process each direction character to update position
5. Mark each new position as visited
6. Return the count of unique positions visited
