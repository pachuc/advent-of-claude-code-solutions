# Problem Report: Chronal Calibration

## Context
A time-travel device needs to be calibrated before use. The device has detected frequency drift and cannot maintain a destination lock. To calibrate it, we need to process a sequence of frequency changes.

## Objective
Calculate the resulting frequency after applying all frequency changes to an initial starting frequency.

## Input Specification
- **Starting frequency**: 0 (zero)
- **Input format**: A sequence of frequency changes, one per line
- **Change format**: Each change is represented as a signed integer with an explicit sign:
  - `+N` means increase the current frequency by N
  - `-N` means decrease the current frequency by N
  - Example: `+6`, `-3`, `+17`, `-2`

## Algorithm
1. Start with a frequency of `0`
2. Process each frequency change in order
3. For each change, apply it to the current frequency:
   - If the change is `+N`, add N to the current frequency
   - If the change is `-N`, subtract N from the current frequency
4. After processing all changes, return the final frequency value

## Examples

### Example 1: `+1, -2, +3, +1`
- Start: frequency = `0`
- Apply `+1`: frequency = `1`
- Apply `-2`: frequency = `-1`
- Apply `+3`: frequency = `2`
- Apply `+1`: frequency = `3`
- **Result**: `3`

### Example 2: `+1, +1, +1`
- Start: frequency = `0`
- Apply `+1`: frequency = `1`
- Apply `+1`: frequency = `2`
- Apply `+1`: frequency = `3`
- **Result**: `3`

### Example 3: `+1, +1, -2`
- Start: frequency = `0`
- Apply `+1`: frequency = `1`
- Apply `+1`: frequency = `2`
- Apply `-2`: frequency = `0`
- **Result**: `0`

### Example 4: `-1, -2, -3`
- Start: frequency = `0`
- Apply `-1`: frequency = `-1`
- Apply `-2`: frequency = `-3`
- Apply `-3`: frequency = `-6`
- **Result**: `-6`

## Expected Output
A single integer representing the final frequency after all changes have been applied.

## Implementation Notes
- The input will be provided in a file where each line contains one frequency change
- Each change is a signed integer (positive or negative)
- The result can be positive, negative, or zero
- This is essentially computing the sum of all frequency changes starting from 0
