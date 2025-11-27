# Implementation Plan - Part 2: The Stars Align

## Problem Summary
We need to determine exactly how many seconds it takes for the message to appear when points of light align in the sky. This is a modification of Part 1, which found the actual message ("LRGPBHEZ"). The alignment occurs at the moment when the bounding box area of all points is minimized.

## Key Insight
The Part 1 solution (`part_1_solution.py`) already calculates the alignment time! The `find_alignment_time()` function returns the exact time `t` when the points are most aligned (minimum bounding box area). We simply need to output this value as the answer instead of the visual message.

## Algorithm Approach

### Core Logic (Reused from Part 1)
The algorithm works by:
1. Starting at `t = 0`
2. Calculating the bounding box area at each time step
3. Continuing until the area starts increasing (indicating we've passed the minimum)
4. Returning `t - 1` as the alignment time

### Why This Works
- Points move linearly with constant velocity
- The bounding box area forms a convex function over time
- There is exactly one global minimum where points are most tightly clustered
- This minimum is where the message is readable

### Time Complexity
- **O(T × N)** where:
  - `T` = alignment time (number of seconds until alignment)
  - `N` = number of points (~356 in our input)
- Expected `T` is likely in the range of 10,000-20,000 seconds based on the input coordinates

### Space Complexity
- **O(N)** to store points and their positions
- Very memory efficient

## Implementation Steps

### Step 1: Reuse Parsing Logic from Part 1
- Copy or import the `parse_input()` function
- Uses regex pattern: `position=<X, Y> velocity=<X, Y>`
- Returns list of tuples: `[(px, py, vx, vy), ...]`

### Step 2: Reuse Physics Simulation from Part 1
- Copy the `calculate_positions(points, t)` function
- For each point `(px, py, vx, vy)`, calculate position at time `t`:
  - `x = px + t * vx`
  - `y = py + t * vy`

### Step 3: Reuse Bounding Box Calculation from Part 1
- Copy the `get_bounding_box_area(positions)` function
- Finds min/max x and y coordinates
- Returns `width × height`

### Step 4: Reuse the Alignment Time Finder from Part 1
- Copy the `find_alignment_time(points)` function
- This is the core algorithm that:
  1. Iterates through time steps
  2. Tracks bounding box area
  3. Detects when area starts increasing
  4. Returns the time of minimum area

### Step 5: Simplify Main Function
Unlike Part 1, we don't need to:
- Visualize the points
- Extract individual letters
- Recognize letter patterns
- Read the message

We only need to:
1. Parse input
2. Find alignment time
3. Output the time value

### Step 6: Output the Result
Simply print the alignment time as an integer.

## Code Structure

```python
import re

def parse_input(filename):
    # [REUSE FROM PART 1 - no changes needed]
    pass

def calculate_positions(points, t):
    # [REUSE FROM PART 1 - no changes needed]
    pass

def get_bounding_box(positions):
    # [REUSE FROM PART 1 - no changes needed]
    pass

def get_bounding_box_area(positions):
    # [REUSE FROM PART 1 - no changes needed]
    pass

def find_alignment_time(points):
    # [REUSE FROM PART 1 - no changes needed]
    pass

def main(input_file='input.md'):
    # Parse input
    points = parse_input(input_file)

    # Find alignment time
    alignment_time = find_alignment_time(points)

    # Output result
    print(alignment_time)

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    main(input_file)
```

## Optimization Considerations

### Current Implementation is Sufficient
The Part 1 implementation is already quite efficient:
- Linear search through time is appropriate
- No need for binary search since we don't know the range beforehand
- Each iteration is O(N) which is minimal

### Potential Optimizations (Not Needed for This Problem)
1. **Early termination**: Already implemented - stops when area increases
2. **Skip steps**: Could increment by larger steps initially, but adds complexity
3. **Parallel computation**: Overkill for ~356 points
4. **Analytical solution**: Would require solving for when velocity vectors converge, which is complex

### Why Current Approach is Optimal
- Simple and correct
- Runs in reasonable time (< 1 second for expected input)
- Code reuse from Part 1 minimizes bugs

## Edge Cases to Handle

1. **Empty input**: Should handle gracefully (already handled in Part 1)
2. **Single point**: Minimum area is 0 at t=0
3. **Points never converge**: MAX_ITERATIONS limit prevents infinite loop
4. **Multiple local minima**: Won't occur with linear motion and constant velocity

## Files to Reference
- `part_1_solution.py`: Source for all core functions
- `input.md`: The actual input data
- `part_1_answer.txt`: Contains "LRGPBHEZ" (for verification that we're finding the same time)

## Expected Output Format
A single integer representing the number of seconds, e.g.:
```
10304
```

## Implementation Notes
- Remove all visualization code from Part 1
- Remove letter recognition code from Part 1
- Keep only the time-finding logic
- Much simpler than Part 1!

## Code Reuse Strategy
For this puzzle solution, directly **copy** the required functions from Part 1 rather than importing:
- Simpler approach with no import path issues
- Self-contained solution file
- Easier to run standalone

## Verification Step
After implementing the solution:
1. Run the Part 2 solution to get the alignment time `T`
2. Run the Part 1 solution and verify it reports the same time `T`
3. Confirm that Part 1 shows "LRGPBHEZ" at time `T`
4. This cross-validation ensures both solutions are consistent

## Expected Time Range
Based on input coordinates ranging from approximately -50,000 to +50,000:
- The convergence time is likely in the range of 10,000-20,000 seconds
- This estimate comes from the ratio of coordinate ranges to velocity magnitudes (1-5)
- Rough calculation: 50,000 / 5 = 10,000 seconds order of magnitude
