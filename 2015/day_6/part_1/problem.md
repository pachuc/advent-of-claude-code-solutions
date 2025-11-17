# Problem Report: Light Grid Control System

## Context
You need to configure a 1000x1000 grid of lights (1 million total lights) based on a series of instructions. The goal is to determine how many lights end up being lit after processing all instructions.

## Problem Statement
Calculate the total number of lights that are turned on after executing a sequence of light control instructions on a 1000x1000 grid.

## Initial State
- Grid dimensions: 1000x1000 (coordinates from 0 to 999 in each direction)
- All lights start in the OFF state
- Corner coordinates are at: (0,0), (0,999), (999,999), and (999,0)

## Input Format
The input consists of multiple instruction lines, each with one of three command types:

1. `turn on X1,Y1 through X2,Y2` - Turn on all lights in the rectangle
2. `turn off X1,Y1 through X2,Y2` - Turn off all lights in the rectangle
3. `toggle X1,Y1 through X2,Y2` - Toggle all lights in the rectangle (on→off, off→on)

Where:
- `X1,Y1` and `X2,Y2` represent opposite corners of a rectangle
- Ranges are **inclusive** (e.g., "0,0 through 2,2" affects 9 lights in a 3x3 square)
- Instructions must be processed **in the order given**

## Command Behavior
- **turn on**: Set lights to ON (if already on, remain on)
- **turn off**: Set lights to OFF (if already off, remain off)
- **toggle**: Flip the state (on becomes off, off becomes on)

## Examples
- `turn on 0,0 through 999,999` → turns on all 1,000,000 lights
- `toggle 0,0 through 999,0` → toggles the first row of 1000 lights
- `turn off 499,499 through 500,500` → turns off the middle 4 lights (2x2 square)

## Expected Output
A single integer representing the total count of lights that are turned ON after all instructions have been executed.

## Algorithm Requirements
1. Initialize a 1000x1000 grid with all lights OFF
2. Parse each instruction line to extract:
   - Command type (turn on, turn off, or toggle)
   - Starting coordinate (X1, Y1)
   - Ending coordinate (X2, Y2)
3. For each instruction, apply the command to all lights in the inclusive rectangular range
4. After processing all instructions, count and return the total number of lights in the ON state
