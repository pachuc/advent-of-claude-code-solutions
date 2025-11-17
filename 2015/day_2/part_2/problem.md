# Problem Report: Gift Ribbon Calculator

## Context
The elves need to order ribbon to wrap presents. They want to calculate the exact amount of ribbon needed for all their presents. Each present is a rectangular box with three dimensions.

## Objective
Calculate the total feet of ribbon needed to wrap all presents and tie bows on them.

## Input Format
- Multiple lines, each containing the dimensions of a present
- Format: `length x width x height` (e.g., `29x13x26`)
- Three integers separated by 'x' character
- Each line represents one present

## Calculation Rules

For each present, calculate two components:

### 1. Wrapping Ribbon
- Find the shortest distance around the sides (smallest perimeter of any face)
- A box has three possible face perimeters:
  - 2*length + 2*width
  - 2*width + 2*height
  - 2*length + 2*height
- Use the **smallest** of these three perimeters

### 2. Bow Ribbon
- Calculate the cubic volume of the present
- Formula: length × width × height

### 3. Total per Present
- Total ribbon = wrapping ribbon + bow ribbon

## Examples

**Example 1:** Present with dimensions `2x3x4`
- Face perimeters: 2+2+3+3=10, 2+2+4+4=12, 3+3+4+4=14
- Smallest perimeter: 10 feet (for wrapping)
- Volume: 2×3×4 = 24 feet (for bow)
- Total: 10 + 24 = **34 feet**

**Example 2:** Present with dimensions `1x1x10`
- Face perimeters: 1+1+1+1=4, 1+1+10+10=22, 1+1+10+10=22
- Smallest perimeter: 4 feet (for wrapping)
- Volume: 1×1×10 = 10 feet (for bow)
- Total: 4 + 10 = **14 feet**

## Expected Output
A single integer representing the total feet of ribbon needed for all presents combined.

## Algorithm Summary
1. Parse each line to extract the three dimensions
2. For each present:
   - Calculate all three possible face perimeters
   - Select the minimum perimeter (this is the wrapping ribbon)
   - Calculate the volume (length × width × height) for the bow
   - Add wrapping ribbon + bow ribbon
3. Sum the ribbon needed for all presents
4. Return the total
