# Implementation Plan: Mine Cart Collision Detection

## Overview
Implement a simulation of carts moving on a track system to detect the first collision location.

## Algorithm Analysis

### Time Complexity
- **Best case**: O(k) where k is the number of moves until first collision
- **Worst case**: O(n * m * c²) where n×m is the grid size and c is the number of carts
  - Each tick requires sorting carts: O(c log c)
  - Each cart movement requires collision check: O(c) per cart
  - Maximum ticks until collision is bounded by grid size
- **Expected**: The collision should occur relatively quickly given the track layout

### Space Complexity
- O(n * m) for the track grid
- O(c) for cart storage
- Total: O(n * m + c)

### Efficiency Considerations
- The input appears to be ~150 lines × ~150 columns with a small number of carts
- Direct simulation is feasible and efficient enough
- No need for complex optimization like spatial hashing

## Implementation Steps

### Step 1: Parse Input
**Objective**: Convert the text map into data structures for simulation

**Actions**:
1. Read the input file line by line
2. Create a 2D grid to store the track layout
3. Identify and extract cart positions and directions:
   - `^`, `v`, `<`, `>` characters are carts
   - Replace cart characters with underlying track:
     - `^` or `v` → `|` (vertical track)
     - `<` or `>` → `-` (horizontal track)
4. Create a Cart class/data structure with:
   - `x, y`: current position
   - `direction`: current facing direction (N/S/E/W or similar)
   - `intersection_count`: number of intersections encountered (starts at 0)

**Data Structures**:
- `track`: 2D list of characters representing the track
- `carts`: list of cart objects

### Step 2: Implement Direction and Movement Logic
**Objective**: Handle cart movement and direction changes

**Actions**:
1. Define direction representations (e.g., using tuples or enums):
   - UP: (0, -1)
   - DOWN: (0, 1)
   - LEFT: (-1, 0)
   - RIGHT: (1, 0)

2. Implement movement function:
   - Update cart position: `(x, y) = (x + dx, y + dy)`
   - Get track type at new position
   - Update direction based on track type

3. Implement curve logic:
   - `/` curve:
     - UP → RIGHT
     - RIGHT → UP
     - DOWN → LEFT
     - LEFT → DOWN
   - `\` curve:
     - UP → LEFT
     - LEFT → UP
     - DOWN → RIGHT
     - RIGHT → DOWN

4. Implement intersection logic:
   - Track intersection count modulo 3:
     - 0: turn LEFT
     - 1: go STRAIGHT
     - 2: turn RIGHT
   - Increment intersection count after each intersection

**Helper Functions**:
- `turn_left(direction)`: return new direction after left turn
- `turn_right(direction)`: return new direction after right turn
- `apply_curve(direction, curve_char)`: return new direction after curve
- `apply_intersection(cart)`: update cart direction and intersection count

### Step 3: Implement Simulation Loop
**Objective**: Run the simulation tick by tick until collision

**Actions**:
1. Create main simulation loop:
   ```python
   while True:
       # Sort carts by position (top-to-bottom, left-to-right)
       # Move each cart in order
       # Check for collision after each move
       # If collision found, return location
   ```

2. Implement cart sorting:
   - Sort by y-coordinate first (row)
   - Then by x-coordinate (column)
   - Use: `carts.sort(key=lambda c: (c.y, c.x))`

3. Implement move sequence for each cart:
   - Calculate new position
   - Update position
   - Get track type at new position
   - Update direction based on track type
   - Check for collision

4. Implement collision detection:
   - After moving each cart, check if any other cart is at same position
   - Use a set or dictionary for O(1) lookup
   - Return immediately when first collision found

### Step 4: Collision Detection and Output
**Objective**: Detect collision and format output correctly

**Actions**:
1. After each cart move, check for collision IMMEDIATELY:
   - Maintain a set of positions of carts that have already moved this tick
   - After moving each cart, check if its new position is already in this set
   - If collision found, return immediately with collision position
   - If no collision, add the cart's new position to the set
   - Important: Check after EACH cart moves, not at end of tick

   ```python
   moved_positions = set()
   for cart in sorted_carts:
       cart.move(track)
       if (cart.x, cart.y) in moved_positions:
           return (cart.x, cart.y)  # Collision detected!
       moved_positions.add((cart.x, cart.y))
   ```

2. Format output:
   - Return as `"X,Y"` format
   - X = column (horizontal position, 0-indexed from left)
   - Y = row (vertical position, 0-indexed from top)

   Example coordinate system:
   ```
     0123  (X coordinates / columns)
   0 >--<
   1 |  |
   2 v  ^
   (Y coordinates / rows)

   Collision at column 1, row 0 would be: "1,0"
   ```

### Step 5: Main Function Integration
**Objective**: Tie everything together

**Actions**:
1. Create main function:
   ```python
   def solve():
       # Parse input
       track, carts = parse_input()

       # Run simulation
       collision_x, collision_y = simulate(track, carts)

       # Format and return result
       return f"{collision_x},{collision_y}"
   ```

2. Add input/output handling:
   - Read from `input.md`
   - Print result to stdout

## Implementation Notes

### Critical Details
1. **Cart ordering**: Carts must move in top-to-bottom, left-to-right order each tick
2. **Collision timing**: Check for collision after each individual cart move, not at end of tick
3. **Track restoration**: When parsing, restore the track character under each cart
4. **Intersection state**: Each cart maintains its own intersection counter (0, 1, 2, cycling)

### Edge Cases to Handle
1. Multiple carts on same row (ensure left-to-right ordering)
2. Carts starting adjacent to each other (next to but not overlapping):
   - Adjacent means neighboring cells, not same position
   - They might collide on first tick if moving toward each other
   - Carts cannot start on the same position (would be immediate collision)
3. Curves at edges of track
4. Multiple intersections in sequence

### Potential Pitfalls
1. **Wrong coordinate system**: Ensure X=column, Y=row (not row, column)
2. **Off-by-one errors**: Ensure 0-indexed coordinates
3. **Direction logic errors**: Test curve transformations carefully
4. **Sorting issues**: Ensure stable sorting maintains proper order

## Code Structure

```
main.py
├── parse_input() → (track, carts)
├── Cart class
│   ├── __init__(x, y, direction)
│   ├── move(track)
│   └── intersection_count
├── Direction handling (standalone functions for testability)
│   ├── turn_left(direction)
│   ├── turn_right(direction)
│   └── apply_curve(direction, curve)
├── simulate(track, carts) → (x, y)
└── main()
```

## Testing Strategy Reference
See `test_plan.md` for detailed testing approach including:
- Unit tests for direction transformations
- Small track examples
- Edge cases and validation
