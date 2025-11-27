# Problem Report: Chronal Calibration - Part 2

## Context from Part 1
In Part 1, we calibrated a time-travel device by processing a sequence of frequency changes. Starting from frequency 0, we applied each frequency change in order and calculated the final frequency. The Part 1 solution found that the final frequency was **474** after processing all changes once.

The device receives frequency changes as signed integers (e.g., `+6`, `-3`) from an input file, with one change per line.

## Part 2: Finding the First Repeated Frequency

### New Discovery
The device **repeats the same frequency change list over and over** in a continuous loop. To properly calibrate the device, we need to find the first frequency value that is reached **twice**.

### Objective
Find the first frequency that the device reaches twice as it continuously loops through the frequency changes.

## Input Specification
- **Starting frequency**: 0 (zero)
- **Input format**: A sequence of frequency changes, one per line (same as Part 1)
- **Change format**: Signed integers with explicit signs (`+N` or `-N`)
- **Important**: The list of changes repeats infinitely until a duplicate frequency is found

## Algorithm Requirements
1. Start with frequency = `0`
2. Keep track of all frequencies that have been seen
3. Process each frequency change in order, applying it to the current frequency
4. After each change is applied:
   - Check if the new frequency has been seen before
   - If yes, this is the answer - return it immediately
   - If no, add it to the set of seen frequencies and continue
5. When reaching the end of the input list, loop back to the beginning and continue
6. The duplicate frequency might be found in the middle of processing the list
7. The list may need to be repeated many times before finding a duplicate

## Examples

### Example 1: `+1, -2, +3, +1`
- Start: frequency = `0` (mark as seen)
- Apply `+1`: frequency = `1` (mark as seen)
- Apply `-2`: frequency = `-1` (mark as seen)
- Apply `+3`: frequency = `2` (mark as seen)
- Apply `+1`: frequency = `3` (mark as seen)
- **Loop back to start of list**
- Apply `+1`: frequency = `4` (mark as seen)
- Apply `-2`: frequency = `2` (already seen!)
- **Result**: `2`

### Example 2: `+1, -1`
- Start: frequency = `0` (mark as seen)
- Apply `+1`: frequency = `1` (mark as seen)
- Apply `-1`: frequency = `0` (already seen!)
- **Result**: `0`

### Example 3: `+3, +3, +4, -2, -4`
- Processing through multiple loops...
- **Result**: `10` (first frequency reached twice)

### Example 4: `-6, +3, +8, +5, -6`
- Processing through multiple loops...
- **Result**: `5` (first frequency reached twice)

### Example 5: `+7, +7, -2, -7, -4`
- Processing through multiple loops...
- **Result**: `14` (first frequency reached twice)

## Expected Output
A single integer representing the first frequency that is reached twice during the infinite loop of frequency changes.

## Implementation Notes
- Use a set or hash table to efficiently track which frequencies have been seen
- The starting frequency (0) should be considered as "seen" before processing begins
- The input list will repeat indefinitely - implement proper looping logic
- The duplicate might be found after many iterations through the list
- Once a duplicate is found, immediately return it - no need to continue processing
- Memory consideration: Track seen frequencies efficiently since the list may loop many times
