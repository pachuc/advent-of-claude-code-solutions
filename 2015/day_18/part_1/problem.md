# Problem Report: Conway's Game of Life Variant - Light Animation

## Objective
Calculate how many lights are "on" after simulating 100 steps of a cellular automaton on a 100x100 grid.

## Context
This is a variant of Conway's Game of Life. We have a grid of lights that can be either "on" or "off", and we need to simulate their state changes over time based on rules that depend on neighboring lights.

## Input Specification
- A 100x100 grid representing the initial configuration of lights
- Each character represents one light:
  - `#` = light is ON
  - `.` = light is OFF
- The input is provided in `input.md` as 100 lines, each containing 100 characters

## Rules for State Transitions
Each light's next state depends on:
1. Its current state (on or off)
2. The number of adjacent lights that are currently on

**Neighbor Definition:**
- Each light has up to 8 neighbors (including diagonals)
- Edge and corner lights have fewer neighbors
- Missing neighbors (outside the grid) are always treated as "off"

**Transition Rules:**
- **A light that is ON**: stays on if exactly 2 or 3 neighbors are on; otherwise turns off
- **A light that is OFF**: turns on if exactly 3 neighbors are on; otherwise stays off

**Important:** All lights update simultaneously. Each light considers the same current state of all lights before any updates occur (not sequential updates).

## Algorithm Requirements
1. Parse the initial 100x100 grid configuration
2. For each of 100 steps:
   - For every light in the grid, count how many of its neighbors are currently on
   - Apply the transition rules based on the light's current state and neighbor count
   - Update all lights simultaneously to their new states
3. After 100 steps, count the total number of lights that are on

## Expected Output
A single integer representing the total number of lights that are "on" after 100 steps.

## Example (6x6 grid for illustration)
```
Initial state:
.#.#.#
...##.
#....#
..#...
#.#..#
####..

After 4 steps:
......
......
..##..
..##..
......
......
```
After 4 steps on this 6x6 example, there are 4 lights on.

For the actual puzzle: **Run 100 steps on the 100x100 grid and report the count of lights that are on.**
