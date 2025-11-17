# Problem Report: Light Grid Brightness Control

## Context
We are controlling a grid of lights with individual brightness controls. Each light can have a brightness level of zero or more, and all lights start at brightness zero. We need to follow a series of instructions to adjust the brightness levels and calculate the total brightness at the end.

## Objective
Calculate the **total brightness** of all lights combined after following all instructions.

## Input Format
The input consists of multiple lines, each containing an instruction in one of three formats:
- `turn on X1,Y1 through X2,Y2`
- `turn off X1,Y1 through X2,Y2`
- `toggle X1,Y1 through X2,Y2`

Where:
- `X1,Y1` represents the top-left corner coordinate
- `X2,Y2` represents the bottom-right corner coordinate
- Coordinates define a rectangular region (inclusive on all boundaries)

## Command Interpretations
- **`turn on`**: Increase the brightness of all lights in the specified region by **1**
- **`turn off`**: Decrease the brightness of all lights in the specified region by **1** (minimum brightness is 0, cannot go below zero)
- **`toggle`**: Increase the brightness of all lights in the specified region by **2**

## Expected Output
A single integer representing the total brightness of all lights after executing all instructions in order.

## Examples
- `turn on 0,0 through 0,0` would increase the total brightness by 1 (one light from 0 to 1)
- `toggle 0,0 through 999,999` would increase the total brightness by 2,000,000 (1,000,000 lights each increasing by 2)

## Notes
- The grid coordinates appear to range from 0 to 999 (a 1000x1000 grid)
- Instructions must be processed sequentially in the order given
- Brightness cannot go below zero (floor at 0)
- Each coordinate pair represents a rectangular region inclusive of both endpoints
