# Implementation Plan: Reindeer Race Simulation

## Problem Analysis

### Core Requirements
- Simulate a reindeer race lasting exactly 2503 seconds
- Each reindeer alternates between flying (at constant speed) and resting (0 speed)
- Track total distance traveled by each reindeer
- Return the maximum distance traveled by any reindeer

### Input Characteristics
- 9 reindeer in the input
- Each has: speed (km/s), fly_time (seconds), rest_time (seconds)
- Input format: `[Name] can fly [speed] km/s for [fly_time] seconds, but then must rest for [rest_time] seconds.`

### Algorithm Complexity Considerations
- Total time: 2503 seconds (fixed)
- Number of reindeer: 9 (small)
- Time complexity: O(n * t) where n = number of reindeer, t = race duration
- With n=9 and t=2503, this is ~22,500 operations - very manageable
- Space complexity: O(n) to store reindeer data

### Optimization Strategy
Since the race duration is only 2503 seconds and we have few reindeer, we can use either:
1. **Simulation approach**: Iterate through each second (simple, clear)
2. **Mathematical approach**: Calculate complete cycles + remainder (more efficient)

**Chosen approach**: Mathematical calculation for O(n) instead of O(n*t)
- Calculate how many complete cycles fit in 2503 seconds
- Calculate distance for complete cycles
- Handle the partial cycle remainder
- This is more efficient and scales better

## Step-by-Step Implementation Plan

### Step 1: Input Parsing
**Objective**: Parse input file and extract reindeer data

**Details**:
- Read input file line by line
- Use regex or string splitting to extract:
  - Name (not strictly needed for final answer, but useful for debugging)
  - Speed (integer, km/s)
  - Fly time (integer, seconds)
  - Rest time (integer, seconds)
- Store each reindeer's data in a data structure (list of tuples/dicts)

**Implementation approach**:
```python
import re

def parse_input(filename):
    """
    Parse input file and extract reindeer data.

    Args:
        filename: Path to input file

    Returns:
        List of tuples (name, speed, fly_time, rest_time)
    """
    reindeer = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Pattern: [Name] can fly [speed] km/s for [fly_time] seconds, but then must rest for [rest_time] seconds.
            match = re.search(r'([A-Za-z]+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds', line)
            if match:
                name = match.group(1)
                speed = int(match.group(2))
                fly_time = int(match.group(3))
                rest_time = int(match.group(4))
                reindeer.append((name, speed, fly_time, rest_time))
    return reindeer
```

**Improvements**:
- Changed `\w+` to `[A-Za-z]+` for more precise name matching
- Added empty line check to skip blank lines
- Added docstring for clarity

### Step 2: Distance Calculation Function
**Objective**: Calculate distance traveled by a single reindeer after T seconds

**Mathematical approach**:
For a reindeer with parameters (speed, fly_time, rest_time):
1. Cycle length = fly_time + rest_time
2. Number of complete cycles = T // cycle_length
3. Remaining seconds = T % cycle_length
4. Distance from complete cycles = complete_cycles × fly_time × speed
5. Distance from remainder = min(remaining_seconds, fly_time) × speed
6. Total distance = distance_from_cycles + distance_from_remainder

**Implementation approach**:
```python
def calculate_distance(speed: int, fly_time: int, rest_time: int, total_time: int) -> int:
    """
    Calculate total distance traveled by a reindeer in given time.

    Args:
        speed: Flying speed in km/s
        fly_time: Number of seconds reindeer can fly before resting
        rest_time: Number of seconds reindeer must rest
        total_time: Total race duration in seconds

    Returns:
        Total distance traveled in kilometers
    """
    cycle_length = fly_time + rest_time
    complete_cycles = total_time // cycle_length
    remaining_seconds = total_time % cycle_length

    # Distance from complete cycles
    distance = complete_cycles * fly_time * speed

    # Distance from partial cycle (only the flying portion)
    flying_in_remainder = min(remaining_seconds, fly_time)
    distance += flying_in_remainder * speed

    return distance
```

**Improvements**:
- Added type hints for better code clarity
- Added detailed docstring

**Why this works**:
- Each complete cycle contributes exactly (fly_time × speed) km
- The remainder is handled by checking if the reindeer is still in its flying phase
- If remainder > fly_time, the reindeer is resting, so we only count fly_time
- If remainder ≤ fly_time, the reindeer is still flying, so we count all remaining seconds

### Step 3: Find Maximum Distance
**Objective**: Calculate distances for all reindeer and find the maximum

**Implementation approach**:
```python
def find_winner(reindeer: list, race_duration: int = 2503) -> int:
    """
    Find the maximum distance traveled by any reindeer.

    Args:
        reindeer: List of tuples (name, speed, fly_time, rest_time)
        race_duration: Total race time in seconds

    Returns:
        Maximum distance traveled by winning reindeer
    """
    max_distance = 0

    for name, speed, fly_time, rest_time in reindeer:
        distance = calculate_distance(speed, fly_time, rest_time, race_duration)
        max_distance = max(max_distance, distance)

    return max_distance
```

**Improvements**:
- Added type hints
- Added docstring

### Step 4: Main Program
**Objective**: Tie everything together

**Implementation approach**:
```python
import sys

def main():
    # Get input filename (default to 'input.md')
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    # Parse input
    reindeer = parse_input(filename)

    # Find winner
    max_distance = find_winner(reindeer, race_duration=2503)

    # Output result
    print(max_distance)

if __name__ == '__main__':
    main()
```

**Improvements**:
- Added support for command-line argument to specify input file
- Falls back to 'input.md' if no argument provided
- More flexible for testing with different inputs

## Complete Implementation Structure

```
solution.py
├── parse_input(filename) -> list of tuples
├── calculate_distance(speed, fly_time, rest_time, total_time) -> int
├── find_winner(reindeer, race_duration) -> int
└── main()
```

## Improvements Based on Review

This implementation plan has been refined with the following enhancements:

1. **Type Hints**: Added type annotations to all functions for better clarity and IDE support
2. **Docstrings**: Added comprehensive docstrings explaining parameters and return values
3. **Flexible Input**: Support for command-line arguments to specify input file (defaults to 'input.md')
4. **Robust Parsing**:
   - More precise regex pattern using `[A-Za-z]+` for reindeer names
   - Skip empty lines in input
   - Strip whitespace from lines
5. **Code Documentation**: Inline comments explain key logic steps

## Edge Cases Handled

1. **Partial cycles**: The remainder calculation handles cases where race ends mid-cycle
2. **Race ending during rest**: min(remaining_seconds, fly_time) ensures we don't count rest time
3. **Exact cycle boundaries**: Works correctly when total_time is exact multiple of cycle_length
4. **Single cycle**: Works when race_duration < cycle_length
5. **Empty lines**: Parser skips blank lines gracefully

## Time and Space Complexity

- **Time Complexity**: O(n) where n is number of reindeer
  - Parsing: O(n)
  - Distance calculation: O(1) per reindeer × n reindeer = O(n)
  - Finding max: O(n)
  - Total: O(n)

- **Space Complexity**: O(n)
  - Storing reindeer data: O(n)
  - No additional data structures needed

## Verification Against Example

The problem provides an example:
- After 1000 seconds:
  - Comet (14 km/s, 10s fly, 127s rest) → 1120 km
  - Dancer (16 km/s, 11s fly, 162s rest) → 1056 km

We can verify our algorithm:
- Comet: cycle=137s, complete_cycles=7, remainder=41s
  - Distance = 7×10×14 + min(41,10)×14 = 980 + 140 = 1120 ✓
- Dancer: cycle=173s, complete_cycles=5, remainder=135s
  - Distance = 5×11×16 + min(135,11)×16 = 880 + 176 = 1056 ✓
