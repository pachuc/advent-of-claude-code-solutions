# Problem Report: LCD Screen Pixel Display Simulation

## Context
We need to simulate an LCD screen that displays a code for a two-factor authentication system. The screen has been smashed, so we need to determine what it *would* have displayed by processing the instructions encoded on a magnetic strip.

## Objective
Calculate how many pixels should be lit (turned on) after processing all the display instructions.

## Screen Specifications
- **Dimensions**: 50 pixels wide × 6 pixels tall
- **Initial State**: All pixels start in the OFF state
- **Pixel States**: ON (#) or OFF (.)

## Input Format
A series of instructions, one per line, in the following formats:

1. **`rect AxB`** - Creates a rectangle of lit pixels
   - Turns ON all pixels in a rectangle at the top-left corner
   - `A` = width (number of columns)
   - `B` = height (number of rows)

2. **`rotate row y=A by B`** - Rotates a row to the right
   - Shifts all pixels in row `A` to the right by `B` positions
   - Row indexing: 0 is the top row
   - Pixels that fall off the right edge wrap around to the left edge

3. **`rotate column x=A by B`** - Rotates a column downward
   - Shifts all pixels in column `A` down by `B` positions
   - Column indexing: 0 is the left column
   - Pixels that fall off the bottom wrap around to the top

## Example Walkthrough
On a smaller 7×3 screen:

**Initial state**: All pixels OFF
```
.......
.......
.......
```

**`rect 3x2`**: Turn on 3×2 rectangle at top-left
```
###....
###....
.......
```

**`rotate column x=1 by 1`**: Shift column 1 down by 1
```
#.#....
###....
.#.....
```

**`rotate row y=0 by 4`**: Shift row 0 right by 4
```
....#.#
###....
.#.....
```

**`rotate column x=1 by 1`**: Shift column 1 down by 1 (with wrapping)
```
.#..#.#
#.#....
.#.....
```

## Expected Output
A single integer representing the total number of pixels that are lit (ON) after executing all instructions.

## Implementation Notes
- Process instructions sequentially in the order they appear
- Rotation operations wrap pixels around (circular shift)
- The screen maintains state between operations
- Count all ON pixels after all instructions are processed
