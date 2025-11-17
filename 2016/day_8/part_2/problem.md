# Problem Report: LCD Screen Character Recognition (Part 2)

## Context from Part 1
In Part 1, we simulated a two-factor authentication LCD screen that processes instructions to manipulate pixels. The screen is **50 pixels wide × 6 pixels tall** and supports three operations:

1. **`rect AxB`** - Turns ON all pixels in an AxB rectangle at the top-left corner
2. **`rotate row y=A by B`** - Shifts all pixels in row A to the RIGHT by B positions (with wrapping)
3. **`rotate column x=A by B`** - Shifts all pixels in column A DOWNWARD by B positions (with wrapping)

In Part 1, we determined that **119 pixels** are lit after processing all instructions.

## Part 2 Objective
Instead of counting the lit pixels, we now need to **read the actual text message** displayed on the screen. The screen displays capital letters using a specific font format.

## Letter Format Specifications
- Each capital letter is **5 pixels wide**
- Each letter is **6 pixels tall** (the full height of the screen)
- The 50-pixel wide screen can theoretically display **up to 10 letters** (50 ÷ 5 = 10)
- Letters are formed by the pattern of lit (#) and unlit (.) pixels
- Not all positions may contain letters; some may be blank space

## What We're Solving
After processing all the same instructions from Part 1, we need to:
1. Generate the final screen state (50×6 grid of pixels)
2. Visually interpret the pattern of lit pixels as capital letters
3. Read the code that appears on the screen (likely 8-10 characters)

## Input Format
The input is **identical to Part 1**: a series of instructions that manipulate the screen pixels. The same input file is used.

## Expected Output
An **uppercase string** representing the code displayed on the screen.

The output should be the actual letters that can be read when viewing the final screen display, where:
- `#` represents a lit (ON) pixel
- `.` represents an unlit (OFF) pixel

## Implementation Approach
1. **Reuse Part 1 logic** to process all instructions and generate the final 50×6 screen state
2. **Display the screen visually** to see the pixel pattern
3. **Perform OCR (Optical Character Recognition)** by:
   - Dividing the 50-pixel width into 10 sections of 5 pixels each
   - Analyzing each 5×6 block as a single letter
   - Matching the pixel patterns to capital letters A-Z
4. **Return the decoded message** as a string

## Example of Letter Recognition
If the screen shows a pattern like this in a 5×6 block:
```
.##..
#..#.
#..#.
####.
#..#.
#..#.
```
This would be recognized as the letter 'A'.

## Notes
- The solution requires visual pattern recognition or a lookup table of letter patterns
- Each letter occupies exactly 5 columns of the 50-pixel width
- All 6 rows of the screen height are used for each letter
- The answer is a string of capital letters, not a number
