# Implementation Plan: Santa and Robo-Santa Gift Delivery

## Overview
Implement a Python script to calculate the number of unique houses visited by Santa and Robo-Santa as they alternate following directional commands.

## Algorithm Analysis

### Time Complexity
- **O(n)** where n is the length of the input string
- Single pass through the input string
- Set operations (add, contains) are O(1) average case

### Space Complexity
- **O(n)** worst case if all positions are unique
- Expected to be much lower in practice due to overlapping paths

### Efficiency Considerations
- Using a set for O(1) lookup and insertion of coordinates
- Tuples (x, y) for immutable coordinate representation (hashable for set)
- No unnecessary data structure conversions
- Single iteration through input

## Implementation Steps

### Step 1: Read Input
- Read the directional command string from `input.md`
- Strip any trailing whitespace/newlines
- Validate input exists (basic check)
- Note: Assume input contains only valid characters (^, v, <, >) per problem specification

### Step 2: Initialize Data Structures
- Create a set to store unique house positions (coordinates as tuples)
- Initialize Santa's position: `santa_pos = [0, 0]`
- Initialize Robo-Santa's position: `robo_pos = [0, 0]`
- Add starting position (0, 0) to the visited set BEFORE processing any commands

### Step 3: Define Direction Mapping
- Create a dictionary mapping direction characters to coordinate changes:
  - `'^'`: (0, 1) - north/up
  - `'v'`: (0, -1) - south/down
  - `'>'`: (1, 0) - east/right
  - `'<'`: (-1, 0) - west/left

### Step 4: Process Commands
- Iterate through the input string with enumeration to get index and character
- For each character at index `i`:
  - If `i % 2 == 0` (even): Santa's turn
    - Update Santa's position based on direction
    - Add new position to visited set
  - If `i % 2 == 1` (odd): Robo-Santa's turn
    - Update Robo-Santa's position based on direction
    - Add new position to visited set

### Step 5: Position Update Logic
- Get the direction change (dx, dy) from the direction mapping
- Update position: `position[0] += dx`, `position[1] += dy`
- Convert to tuple and add to set: `visited.add((position[0], position[1]))`

### Step 6: Return Result
- Return the length of the visited set (number of unique houses)
- Print the result

## Code Structure

```python
def solve_santa_delivery(input_string: str) -> int:
    """
    Calculate unique houses visited by Santa and Robo-Santa.

    Args:
        input_string: String of directional commands (^, v, <, >)

    Returns:
        int: Number of unique houses that received at least one present
    """
    # Initialize data structures
    # Define direction mapping
    # Add starting position to visited set BEFORE loop
    # Iterate through commands with enumeration
    # Update positions alternately (even=Santa, odd=Robo-Santa)
    # Return count of unique positions

def main():
    # Read input file
    # Call solve function
    # Print result in clear format: "Houses visited: {count}"
```

## Edge Cases Handled
1. Empty input string: Only starting house visited (count = 1)
2. Single character: Santa moves once, Robo-Santa remains at starting position, resulting in 2 unique houses visited
3. Both visiting same houses: Set automatically handles duplicates
4. Large input: O(n) time complexity handles large inputs efficiently

## File Organization
- Main solution in `solution.py`
- Input reading from `input.md`
- Clean, readable code with appropriate comments
