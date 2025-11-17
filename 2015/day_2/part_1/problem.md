# Problem Report: Wrapping Paper Calculator

## Context
We need to calculate the total amount of wrapping paper required for a list of box-shaped presents. Each present is a perfect rectangular box with dimensions: length (l), width (w), and height (h).

## Objective
Calculate the total square feet of wrapping paper needed for all presents in the input list.

## Calculation Requirements

For each present, calculate the required wrapping paper using the following formula:

**Wrapping paper needed = Surface area + Slack**

Where:
- **Surface area** = `2*l*w + 2*w*h + 2*h*l`
- **Slack** = area of the smallest side

The smallest side is the minimum of:
- `l*w`
- `w*h`
- `h*l`

## Input Format
- Each line contains the dimensions of one present in the format: `LxWxH`
- Dimensions are separated by the character 'x'
- All measurements are in feet
- Example: `2x3x4` means length=2, width=3, height=4

## Output Format
- A single integer representing the total square feet of wrapping paper needed for all presents

## Examples

**Example 1:** `2x3x4`
- Surface area: `2*6 + 2*12 + 2*8 = 52` square feet
- Smallest side: `min(2*3, 3*4, 2*4) = min(6, 12, 8) = 6` square feet
- Total: `52 + 6 = 58` square feet

**Example 2:** `1x1x10`
- Surface area: `2*1 + 2*10 + 2*10 = 42` square feet
- Smallest side: `min(1*1, 1*10, 1*10) = min(1, 10, 10) = 1` square foot
- Total: `42 + 1 = 43` square feet

## Algorithm Steps
1. Parse each line to extract the three dimensions (l, w, h)
2. For each present:
   - Calculate the three side areas: `l*w`, `w*h`, `h*l`
   - Calculate surface area: `2*(l*w + w*h + h*l)`
   - Find the minimum side area
   - Add surface area + minimum side area to the running total
3. Return the total sum
