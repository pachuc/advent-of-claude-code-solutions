# Implementation Plan: Santa's House Delivery Tracker

## Problem Summary
Track Santa's movement on an infinite 2D grid and count the number of unique houses that receive at least one present. Santa starts at origin (0,0), delivers a present, then follows directional commands (^, v, <, >) to move and deliver presents at each new location.

## Algorithm Design

### Approach: Set-based Position Tracking
Use a hash set to track unique coordinate positions visited during Santa's journey.

**Time Complexity**: O(n) where n is the length of the input string
**Space Complexity**: O(n) in worst case (all positions unique)

### Why This Approach?
- **Efficient lookups**: Set provides O(1) average-case insertion
- **Automatic uniqueness**: Set naturally handles duplicate positions
- **Simple to implement**: Straightforward coordinate tracking
- **Optimal for large inputs**: Linear time complexity, no redundant work
- **Memory efficient**: Only stores unique positions, not all visits

## Step-by-Step Implementation

### Step 1: Read and Parse Input
```python
# Read the input file
- Open and read 'input.md'
- Extract the direction string (strip whitespace/newlines)
- Store in a variable for processing
```

**Considerations**:
- Input file contains single line of directions
- May have trailing whitespace to strip
- No need for complex parsing or validation

### Step 2: Initialize Data Structures
```python
# Set up tracking variables
- Create a set to store visited positions (tuples of (x, y))
- Initialize current position: x = 0, y = 0
- Add starting position (0, 0) to the visited set
```

**Why tuples for positions?**:
- Tuples are immutable and hashable (required for sets)
- Natural representation of 2D coordinates
- Memory efficient

### Step 3: Create Direction Mapping
```python
# Map characters to coordinate deltas
- '^': (0, 1)   # North: y increases
- 'v': (0, -1)  # South: y decreases
- '>': (1, 0)   # East: x increases
- '<': (-1, 0)  # West: x decreases
```

**Implementation options**:
- Dictionary for O(1) lookup
- Could use if/elif but dictionary is cleaner
- Delta values represent change in (x, y)

**Coordinate System Note**:
- Using mathematical coordinates (y-up) rather than screen coordinates (y-down)
- Since the grid is relative and infinite, the convention doesn't affect correctness
- Only relative positions matter, not absolute orientation

### Step 4: Process Each Direction
```python
# Iterate through each character in the input string
for each direction character:
    1. Look up the (dx, dy) delta from the direction map
    2. Update current position: x += dx, y += dy
    3. Add new position (x, y) to the visited set
```

**Key points**:
- Process characters sequentially (order matters)
- Set automatically handles duplicate positions
- No need to check if position already visited before adding

### Step 5: Calculate and Output Result
```python
# Count unique houses
- Get the size of the visited set using len()
- Print the result as a single integer
```

**Output format**:
- Simple integer count
- No additional formatting needed

## Detailed Implementation Structure

```python
def solve():
    # Step 1: Read input
    with open('input.md', 'r') as f:
        directions = f.read().strip()

    # Step 2: Initialize
    visited = set()
    x, y = 0, 0
    visited.add((x, y))  # Starting position

    # Step 3: Direction mapping
    direction_map = {
        '^': (0, 1),
        'v': (0, -1),
        '>': (1, 0),
        '<': (-1, 0)
    }

    # Step 4: Process directions
    for direction in directions:
        dx, dy = direction_map[direction]
        x += dx
        y += dy
        visited.add((x, y))

    # Step 5: Output result
    print(len(visited))

if __name__ == "__main__":
    solve()
```

## Edge Cases Handled

1. **Empty input**: Would only count starting position (result: 1)
2. **Single direction**: Start + 1 move = 2 houses
3. **Returning to start**: Set handles duplicates automatically
4. **Long input**: O(n) complexity remains efficient
5. **All same direction**: Linear path, all unique positions

## Efficiency Analysis

### For Large Inputs
Given the actual input is ~8000+ characters:
- **Time**: ~8000 iterations, each O(1) → O(n) total
- **Space**: Worst case ~8000 unique positions stored
- **Expected runtime**: < 1 second for inputs of this size

### Why No Optimization Needed
- Already optimal time complexity (must process each character)
- Set operations are O(1) average case
- No redundant computations
- Memory usage proportional to unique positions (necessary)

## Alternative Approaches Considered

1. **Dictionary with counts**:
   - Tracks visit frequency per house
   - Unnecessary overhead since we only need unique count
   - Rejected: More complex, same time/space complexity

2. **List with deduplication**:
   - Store all positions, deduplicate at end
   - Worse space complexity O(n) always
   - Rejected: Inefficient, no benefit

3. **Complex coordinate compression**:
   - Not needed for this problem
   - Grid is sparse, no benefit
   - Rejected: Over-engineering

## Implementation Notes

- **No error handling needed**: Input guaranteed to be valid directional characters
  - Note: If an invalid character is encountered, the script will fail loudly with a KeyError, which is acceptable for this context
- **File I/O assumption**: Assumes input.md exists and is readable
  - For an AoC script, failing on missing input is acceptable behavior
- **No logging needed**: Simple script, not production code
- **No input validation**: Problem guarantees valid format
- **Code style**: Clear, readable, straightforward Python
