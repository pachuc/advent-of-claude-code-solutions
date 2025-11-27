# Implementation Plan: Chronal Calibration - Part 2

## Problem Summary
Find the first frequency that is reached twice while continuously looping through the frequency changes list. Start from frequency 0, apply changes in order, and loop back to the beginning when reaching the end of the list.

## Key Differences from Part 1
- Part 1: Single pass through the list, simple summation
- Part 2: Potentially multiple passes (cycles) through the list, requires duplicate detection
- Part 2 requires maintaining state (seen frequencies) across cycles
- Part 2 keeps the same input parsing and error handling from Part 1

## Algorithm Design

### Approach: Cycle Detection with Hash Set
**Time Complexity**: O(n × k) where n = number of frequency changes, k = number of cycles needed
**Space Complexity**: O(n × k) for storing all seen frequencies
**Justification**: Hash set provides O(1) average-case lookup and insertion, optimal for duplicate detection.

### Algorithm Steps
1. **Initialize State**
   - Create a set to track seen frequencies: `seen = {0}`
   - Start with current frequency: `frequency = 0`
   - The initial frequency (0) is already "seen" before processing begins

2. **Parse Input** (Reuse from Part 1)
   - Read input file (default `input.md`)
   - Parse each line as an integer (handles both `+N` and `-N` formats)
   - Include error handling from Part 1 (`try-except` for FileNotFoundError)
   - Store in a list for repeated iteration

3. **Infinite Loop with Cycle Detection**
   - Use `itertools.cycle()` to continuously iterate through changes
   - For each frequency change:
     - Apply the change to current frequency
     - Check if new frequency exists in `seen` set
     - If yes: return immediately (this is the answer)
     - If no: add to `seen` set and continue

4. **Implementation Considerations**
   - Use `itertools.cycle()` for clean infinite iteration over the list
   - Early termination: return as soon as duplicate is found
   - The problem guarantees a solution exists, so no infinite loop risk

## Code Structure

```python
from itertools import cycle

def solve(filename='input.md'):
    """
    Find the first frequency reached twice during continuous looping.

    Args:
        filename: Input file path (default: 'input.md')

    Returns:
        The first duplicate frequency as an integer.
    """
    # Step 1: Read and parse input (copied from Part 1 with error handling)
    try:
        with open(filename, 'r') as f:
            changes = [int(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} file not found")
        return None

    # Step 2: Initialize tracking structures
    seen = {0}  # Start frequency is already "seen"
    frequency = 0

    # Step 3: Infinite loop with cycle detection
    for change in cycle(changes):
        frequency += change
        if frequency in seen:
            return frequency  # Found duplicate!
        seen.add(frequency)
```

## Reusable Components from Part 1
- **File reading logic**: Exact same input file parsing with `try-except`
- **Integer parsing**: Same format handling (strips whitespace, converts to int)
- **Error handling**: FileNotFoundError handling
- **Main structure**: Keep same `if __name__ == '__main__'` pattern

## Implementation Steps (Sequential)
1. Start with Part 1's `solve()` function structure
2. Add `filename` parameter with default value `'input.md'` for testability
3. Copy error handling from Part 1 (`try-except FileNotFoundError`)
4. Import `itertools.cycle` at top of file
5. Initialize `seen = {0}` and `frequency = 0`
6. Replace summation logic with cycle detection loop
7. Test with provided examples
8. Run on actual input

## Expected Behavior
- Function returns single integer (first duplicate frequency)
- Should complete quickly (within seconds)
- The problem guarantees a solution exists
