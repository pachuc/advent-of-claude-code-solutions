# Implementation Plan: Spiral Memory Manhattan Distance

## Problem Analysis

### Understanding the Spiral Pattern
- The spiral starts at position (0, 0) with value 1
- It moves: RIGHT → UP → LEFT → DOWN → RIGHT (repeating with increasing step sizes)
- Pattern forms concentric square "rings" around the center
- Ring 0: contains only value 1
- Ring 1: contains values 2-9 (8 values)
- Ring 2: contains values 10-25 (16 values)
- Ring n: contains 8n values (except ring 0)

### Key Observations
1. **Coordinate System**: Origin (0,0) at square 1, positive X = right/east, positive Y = up/north
2. **Ring Identification**: Each ring k (k ≥ 1) ends at bottom-right corner (k, -k) with value (2k+1)²
3. **Ring Size**: Ring k contains numbers from (2k-1)² + 1 to (2k+1)²
4. **Spiral Direction**: From square 1: RIGHT → UP → LEFT → DOWN, then repeat with longer segments
5. **Manhattan Distance**: For any point (x, y), distance = |x| + |y|
6. **Efficiency**: With input potentially being 289326, we need O(1) or O(√n) solution, not O(n)

### Algorithm Strategy
Use a mathematical approach to avoid simulating the entire spiral:

1. **Determine which ring the number belongs to**
   - Find the smallest odd number whose square is ≥ target number
   - This gives us the side length of the ring
   - Calculate the ring index from the side length

2. **Find position within the ring**
   - Each ring has 4 sides
   - Determine which side the number is on
   - Calculate offset within that side

3. **Calculate coordinates**
   - Based on the side and offset, compute (x, y) coordinates

4. **Compute Manhattan distance**
   - Return |x| + |y|

## Step-by-Step Implementation

### Step 1: Handle Base Case
```python
if n == 1:
    return 0
```

### Step 2: Find the Ring Number
- Calculate the ring index that contains number n
- Find the side length of the square ring (always odd: 3, 5, 7, 9, ...)
- Method: Take ceiling of sqrt(n), round up to nearest odd number

```python
import math

# Find the side length of the ring containing n
side_length = math.ceil(math.sqrt(n))
if side_length % 2 == 0:
    side_length += 1

# Ring index (0 at center, 1 for first ring, etc.)
ring = side_length // 2
```

### Step 3: Find Position Within Ring
- Calculate which number starts the current ring: (2*ring - 1)² + 1
- Calculate the maximum number in the ring: (2*ring + 1)²
- Find position of n within the ring
- Determine which side (right, top, left, bottom) and offset

```python
# Maximum value of the previous ring
max_prev_ring = (2 * ring - 1) ** 2

# Position within current ring (0-indexed)
position_in_ring = n - max_prev_ring - 1

# Each side has '2 * ring' numbers (not side_length - 1)
# Total numbers in ring k = 8k, so each of 4 sides has 2k numbers
side_len = 2 * ring

# Determine which side we're on (0=right, 1=top, 2=left, 3=bottom)
side_index = position_in_ring // side_len
offset = position_in_ring % side_len
```

### Step 4: Calculate Coordinates
Each ring starts to the right of where the previous ring ended, then spirals:

```python
# Each ring k ends at (k, -k) and the next ring starts at (k+1, -k)
# Ring k starts at value (2k-1)² + 1
# The spiral goes: right side (moving up), top (moving left),
#                  left side (moving down), bottom (moving right)
#
# For ring k with side_length = 2k+1:
# - Right side: goes from (k, -k+1) to (k, k), that's 2k values (indices 0 to 2k-1)
# - Top side: goes from (k-1, k) to (-k, k), that's 2k values (indices 2k to 4k-1)
# - Left side: goes from (-k, k-1) to (-k, -k), that's 2k values (indices 4k to 6k-1)
# - Bottom side: goes from (-k+1, -k) to (k, -k), that's 2k values (indices 6k to 8k-1)

side_len = 2 * ring  # Number of steps on each side

if side_index == 0:  # Right side, moving up from (ring, -ring+1)
    x = ring
    y = -ring + 1 + offset
elif side_index == 1:  # Top side, moving left from (ring-1, ring)
    x = ring - 1 - offset
    y = ring
elif side_index == 2:  # Left side, moving down from (-ring, ring-1)
    x = -ring
    y = ring - 1 - offset
else:  # side_index == 3, Bottom side, moving right from (-ring+1, -ring)
    x = -ring + 1 + offset
    y = -ring
```

### Step 5: Calculate Manhattan Distance
```python
manhattan_distance = abs(x) + abs(y)
return manhattan_distance
```

## Complete Function Structure

```python
import math

def spiral_manhattan_distance(n):
    """
    Calculate Manhattan distance from square n to square 1 in spiral grid.

    Coordinate system: (0,0) at square 1, +X right, +Y up
    Spiral direction: RIGHT → UP → LEFT → DOWN (clockwise when viewed with Y-up)

    Args:
        n: Square number in the spiral (positive integer)

    Returns:
        Manhattan distance (positive integer)
    """
    # Base case
    if n == 1:
        return 0

    # Find ring number
    # Each ring k ends with (2k+1)², so we find which ring contains n
    side_length = math.ceil(math.sqrt(n))
    if side_length % 2 == 0:
        side_length += 1
    ring = side_length // 2

    # Find position within ring
    max_prev_ring = (2 * ring - 1) ** 2
    position_in_ring = n - max_prev_ring - 1

    # Each side has 2*ring numbers
    side_len = 2 * ring
    side_index = position_in_ring // side_len
    offset = position_in_ring % side_len

    # Calculate coordinates based on side
    # Ring k: right side (k, -k+1) to (k, k)
    #         top side (k-1, k) to (-k, k)
    #         left side (-k, k-1) to (-k, -k)
    #         bottom side (-k+1, -k) to (k, -k)
    if side_index == 0:  # Right side, moving up
        x, y = ring, -ring + 1 + offset
    elif side_index == 1:  # Top side, moving left
        x, y = ring - 1 - offset, ring
    elif side_index == 2:  # Left side, moving down
        x, y = -ring, ring - 1 - offset
    else:  # Bottom side, moving right
        x, y = -ring + 1 + offset, -ring

    # Return Manhattan distance
    return abs(x) + abs(y)
```

## Main Script Structure

```python
def main():
    # Read input
    with open('input.md', 'r') as f:
        n = int(f.read().strip())

    # Calculate result
    result = spiral_manhattan_distance(n)

    # Output result
    print(result)

if __name__ == "__main__":
    main()
```

## Complexity Analysis

- **Time Complexity**: O(1) - constant time operations (square root, arithmetic)
- **Space Complexity**: O(1) - only storing a few integer variables
- **Scalability**: Can handle very large inputs (millions) instantly

## Edge Cases Handled

1. n = 1 (center square): Returns 0
2. Small values (2-9): First ring
3. Perfect squares: Corner positions
4. Large values (289326): Efficiently computed
5. Values on different sides of the ring
