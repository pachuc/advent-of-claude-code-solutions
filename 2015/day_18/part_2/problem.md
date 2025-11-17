# Problem Report: Conway's Game of Life with Stuck Corner Lights

## Context
This is an implementation of Conway's Game of Life applied to a grid of lights. However, there's a special constraint: the four corner lights are stuck in the "on" state and cannot be turned off throughout the simulation.

## Objective
Determine how many lights are in the "on" state after running 100 steps of the simulation on a 100x100 grid with the special corner constraint.

## Input Specification
- Input is a 100x100 grid of lights
- Each character represents a light:
  - `#` = light is ON
  - `.` = light is OFF
- The input file contains 100 lines, each with 100 characters

## Rules of the Simulation

### Standard Conway's Game of Life Rules:
1. A light that is **ON** stays on if it has **2 or 3 neighbors** that are on; otherwise, it turns off
2. A light that is **OFF** turns on if it has **exactly 3 neighbors** that are on; otherwise, it stays off
3. Neighbors are the 8 adjacent lights (horizontal, vertical, and diagonal)

### Special Constraint:
**The four corner lights are always ON**, regardless of what the standard rules would dictate:
- Top-left corner: position (0, 0)
- Top-right corner: position (0, 99)
- Bottom-left corner: position (99, 0)
- Bottom-right corner: position (99, 99)

These corner lights must be forced to ON state:
- Before starting the simulation (in the initial state)
- After each step of the simulation

## Simulation Process
1. Set all four corner lights to ON in the initial configuration
2. For each of 100 steps:
   - Apply Conway's Game of Life rules to all lights simultaneously
   - Force all four corner lights back to ON (in case the rules turned them off)

## Expected Output
A single integer representing the total count of lights that are ON after completing 100 steps.

## Example
Using a 6x6 grid with the same corner constraint:
- Initial state has corners forced ON
- After 5 steps: **17 lights are on**

The pattern shows how corner lights remain on throughout all steps regardless of their neighbor count.
