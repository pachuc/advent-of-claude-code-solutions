# Implementation Plan: The Stars Align

## Overview
Create a Python script to simulate moving points of light and detect when they align to form a readable message.

## Step-by-Step Implementation

### Step 1: Input Parsing
**Goal**: Parse the input file to extract position and velocity data for each point.

**Details**:
- Read input line by line
- Use regex to extract four integers from each line: `position=<X, Y> velocity=<X, Y>`
- Pattern: `position=<\s*(-?\d+),\s*(-?\d+)>\s+velocity=<\s*(-?\d+),\s*(-?\d+)>`
  - `\s+` requires at least one whitespace character between position and velocity
- Store as list of tuples: `[(px, py, vx, vy), ...]`
- Handle potential whitespace variations in the format
- Skip any lines that don't match the pattern (with warning)
- Verify file exists before attempting to read

**Data Structure**: List of tuples or a NumPy array (if using NumPy for performance)

### Step 2: Position Calculation Function
**Goal**: Create a function to calculate positions at any given time `t`.

**Details**:
- Input: List of points (position, velocity), time `t`
- Output: List of current positions at time `t`
- Formula: `position_t = (px + t*vx, py + t*vy)` for each point
- Should be efficient as it will be called many times

**Function Signature**: `def calculate_positions(points, t) -> List[Tuple[int, int]]`

### Step 3: Bounding Box Calculation
**Goal**: Calculate the bounding box dimensions for a set of positions.

**Details**:
- Find min/max X and Y coordinates
- Return bounding box coordinates for use in visualization and area calculation
- This metric helps identify when points are most compact

**Function Signature**: `def get_bounding_box(positions) -> Tuple[int, int, int, int]`
**Returns**: (min_x, min_y, max_x, max_y)

**Additional Function**: `def get_bounding_box_area(positions) -> int`
**Details**:
- Calls get_bounding_box to get coordinates
- Calculate width = max_x - min_x
- Calculate height = max_y - min_y
- Return area = width * height
**Returns**: Integer area of the bounding box

### Step 4: Find Alignment Time
**Goal**: Determine the time `t` when the message appears (minimum bounding box area).

**Details**:
- Strategy: The bounding box area will decrease as points converge, reach a minimum when aligned, then increase as they diverge
- Algorithm:
  1. Start at t=0
  2. Calculate bounding box area for consecutive time steps
  3. Track when area starts increasing after decreasing
  4. The time just before area starts increasing is when points are most aligned
- Termination: Stop as soon as area increases (single increase is sufficient - no local minima expected in this physics simulation)
- Edge Case: If area increases at t=1 (diverging from start), return t=0 as the minimum
- Safety: Add maximum iteration limit (e.g., 100000) to prevent infinite loops
- Expected time range: Based on input velocities (±1 to ±5) and positions (~±50000), rough estimate: 50000 / 5 ≈ 10000 seconds

**Pseudo-code**:
```python
t = 0
prev_area = float('inf')
MAX_ITERATIONS = 100000

while t < MAX_ITERATIONS:
    positions = calculate_positions(points, t)
    current_area = get_bounding_box_area(positions)

    if current_area > prev_area:
        # Area is increasing, previous t was the minimum
        # Special case: if t=1, minimum is at t=0
        return max(0, t - 1)

    prev_area = current_area
    t += 1

raise RuntimeError("Failed to find alignment within iteration limit")
```

### Step 5: Visualization Function
**Goal**: Render the points as a grid of characters to display the message.

**Details**:
- Input: List of positions at alignment time
- Get bounding box to determine grid dimensions
- Normalize coordinates to start at (0, 0) by subtracting min_x and min_y
- Create 2D grid initialized with spaces (not dots)
- Mark positions where points exist with '#'
- Convert grid to string representation with newlines
- Return multi-line string

**Function Signature**: `def visualize_points(positions) -> str`

**Implementation**:
```python
min_x, min_y, max_x, max_y = get_bounding_box(positions)
# Normalize to origin
point_set = {(x - min_x, y - min_y) for (x, y) in positions}

lines = []
for y in range(max_y - min_y + 1):
    row = ""
    for x in range(max_x - min_x + 1):
        row += '#' if (x, y) in point_set else ' '
    lines.append(row)

return '\n'.join(lines)
```

### Step 6: Message Extraction
**Goal**: Read the message from the visualization.

**Details**:
- The visualization will show capital letters made of '#' characters
- For this problem, we need to manually read the output
- Return the visualization string for the user to read
- Note: Automated OCR for ASCII art is complex and unnecessary for this puzzle

### Step 7: Main Function
**Goal**: Orchestrate the entire solution.

**Details**:
```python
def main(input_file='input.md'):
    # Parse input with error handling
    try:
        points = parse_input(input_file)
        if not points:
            print("Error: No valid points parsed from input")
            return
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        return

    # Find alignment time
    alignment_time = find_alignment_time(points)

    # Get positions at alignment time
    aligned_positions = calculate_positions(points, alignment_time)

    # Visualize
    message_visual = visualize_points(aligned_positions)

    # Output
    print(f"Message appears at t={alignment_time}")
    print(message_visual)

# Allow command-line argument for input file
if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    main(input_file)
```

## Algorithm Complexity Analysis

**Time Complexity**:
- Parsing: O(n) where n = number of points (~356)
- Finding alignment: O(t * n) where t = time to alignment (~10000-15000)
- Overall: O(t * n) ≈ O(10000 * 356) ≈ 3.56M operations - very feasible

**Space Complexity**: O(n) for storing points and positions

## Optimization Considerations

1. **NumPy**: Could use NumPy for vectorized operations, but with only 356 points, pure Python is sufficient
2. **Binary Search**: Could use ternary search on time, but linear search is simple and fast enough
3. **Early Termination**: Stop when area increases (already included)

## File Structure

```
solution.py          # Main implementation
input.md            # Input data (already exists)
implementation_plan.md  # This file
test_plan.md        # Testing plan
```

## Expected Output Format

```
Message appears at t=XXXXX
######  #    #  #    #  ######  ######
#       #    #  #    #  #            #
#       #    #  #    #  #            #
#       #    #  #    #  #           #
#####   ######  ######  #####      #
#       #    #  #    #  #         #
#       #    #  #    #  #        #
#       #    #  #    #  #       #
#       #    #  #    #  #       #
######  #    #  #    #  #       ######
```

(The actual message will be different and likely 8-10 lines tall with capital letters)

**Note**: Uses spaces (not dots) for empty positions. Advent of Code messages are typically 8 lines tall.

## Edge Cases to Handle

1. **Negative coordinates**: Input contains negative positions and velocities - handle in visualization normalization
2. **Large initial spread**: Points start very far apart (~±50000) - algorithm handles this naturally
3. **No local minima expected**: Physics simulation produces smooth convergence, so single increase detection is sufficient
4. **Diverging from start**: If area increases at t=1, return t=0 as minimum
5. **Grid size**: Ensure visualization handles the correct bounding box and normalizes to (0,0)
6. **Missing/malformed input**: Check file exists and skip unparseable lines
7. **Iteration limit**: Prevent infinite loops with MAX_ITERATIONS check

## Implementation Notes

- Use regular expressions for robust parsing
- Integer arithmetic throughout (no floating point)
- Keep code clean and readable since it's a one-time solution
- Add minimal comments for clarity
- This is Advent of Code 2018 Day 10 Part 1
- Message format is typically 8 lines tall with capital letters
- Use spaces (not dots) for empty positions in visualization
- Basic error handling for file I/O and parsing
- Support command-line argument for input file path (defaults to 'input.md')
