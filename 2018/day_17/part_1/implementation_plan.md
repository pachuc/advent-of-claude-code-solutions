# Implementation Plan: Water Flow Simulation

## Overview
Simulate water flowing from a spring at (500, 0) through a 2D grid containing clay veins, tracking both settled and flowing water.

## Algorithm Strategy
Use a **recursive flood-fill simulation** with backtracking to model water behavior:
- Water flows down until blocked
- Water spreads horizontally when downward flow is blocked
- Water settles when contained by clay on both sides
- Water overflows when only one side is blocked

**Time Complexity**: O(W × H) where W is width and H is height of the region
**Space Complexity**: O(W × H) for grid storage + O(H) for recursion stack

## Step-by-Step Implementation

### 1. Parse Input and Build Clay Map
**Function**: `parse_input(lines) -> set[tuple[int, int]]`

- Read each line from input
- Parse format: "x=VALUE, y=START..END" or "y=VALUE, x=START..END"
- For each line:
  - Split on comma to get two parts
  - Extract coordinate type (x or y) and value
  - Extract range start and end
  - Generate all clay positions in the range
- Return set of (x, y) tuples representing clay positions

**Edge cases**:
- Single position ranges (START == END)
- Handle whitespace properly

### 2. Determine Valid Y-Range
**Function**: `get_y_range(clay_set) -> tuple[int, int]`

- Find minimum y-coordinate in clay set: `min_y`
- Find maximum y-coordinate in clay set: `max_y`
- Return (min_y, max_y)
- Only water within this range counts toward final answer

### 3. Initialize Grid State
**Data structures**:
- `clay_set`: Set of (x, y) positions containing clay (from step 1)
- `flowing_water`: Set of (x, y) positions with flowing water `|`
- `settled_water`: Set of (x, y) positions with settled water `~`

### 4. Implement Water Flow Simulation
**Main function**: `simulate_water(start_pos, clay_set, min_y, max_y) -> tuple[set, set]`

This is the core algorithm using recursive depth-first simulation.

#### 4.1 Flow Down Function
**Function**: `flow_down(x, y, clay_set, flowing, settled, min_y, max_y) -> bool`

**Return Value Semantics**:
- Returns True if water at this level has settled or there's support (clay/settled water) - meaning the level can support water above
- Returns False if water flows away (fell off bottom or overflowed) - meaning this level cannot support water above

**Algorithm**:
1. **Boundary check**: If y > max_y: return False (water fell off bottom)

2. **Memoization check**: If (x, y) already visited:
   - If (x, y) in settled: return True (provides support)
   - If (x, y) in flowing: return False (already processed as flowing path)

3. **Mark as flowing**: Add (x, y) to flowing set (initially mark as flowing)

4. **Check support below** at position (x, y+1):
   - If (x+1, y) is clay OR settled water: has_support_below = True
   - Else:
     - Recursively call flow_down(x, y+1, ...)
     - has_support_below = return value from recursive call
     - If has_support_below is False: water flows away, return False immediately

5. **Horizontal spreading** (only when has_support_below is True):
   - Call `spread_horizontal(x, y, clay_set, flowing, settled, min_y, max_y)`
   - This returns (is_contained, left_bound, right_bound)

6. **Determine if water settles**:
   - If is_contained is True (walls on both sides):
     - Call `settle_water(y, left_bound, right_bound, flowing, settled)`
     - Return True (this level provides support)
   - Else (water overflows on at least one side):
     - Water remains flowing at this level
     - Return False (this level cannot support water above)

**Key insight**: The return value tells the caller whether this level can support water. If water settles, it provides support. If it overflows, it doesn't.

#### 4.2 Horizontal Spread Function
**Function**: `spread_horizontal(x, y, clay_set, flowing, settled, min_y, max_y) -> tuple[bool, int, int]`

Returns (is_contained, left_bound, right_bound).

**Algorithm**:
1. **Initialize**:
   - left_wall = False
   - right_wall = False
   - left_bound = x
   - right_bound = x

2. **Spread left**:
   - Start from x-1, move left (x-2, x-3, ...)
   - For each position (curr_x, y):
     - **Check for wall**: If (curr_x, y) is clay:
       - left_wall = True
       - left_bound = curr_x + 1 (first non-clay position)
       - Break from loop

     - **Mark as flowing**: Add (curr_x, y) to flowing set

     - **Check support below** at (curr_x, y+1):
       - If (curr_x, y+1) is NOT clay AND NOT settled water:
         - **Overflow found**: No support, water will fall
         - Recursively call flow_down(curr_x, y+1, ...)
         - left_wall = False (no wall, water overflows here)
         - left_bound = curr_x
         - Break from loop

     - **Continue spreading**: If has support, continue left

3. **Spread right**:
   - Start from x+1, move right (x+2, x+3, ...)
   - Same logic as spreading left:
     - Check for clay wall → right_wall = True, break
     - Mark as flowing
     - Check support below → if no support, overflow, right_wall = False, break
     - Continue if has support

4. **Check if contained**:
   - is_contained = (left_wall AND right_wall)

5. Return (is_contained, left_bound, right_bound)

**Critical Detail**: When spreading finds an unsupported edge, it calls flow_down() recursively to simulate water falling from that overflow point. This creates the proper cascading behavior.

#### 4.3 Settle Water Function
**Function**: `settle_water(y, left_x, right_x, flowing, settled)`

When water is contained by walls on both sides:
1. For each x in range [left_x, right_x] (inclusive):
   - Remove (x, y) from flowing set (if present)
   - Add (x, y) to settled set
2. This simulates water coming to rest

**State Transition**: Positions can transition from flowing → settled when a container fills up. The sets must be updated to reflect this.

### 5. Grid Visualization Function (REQUIRED)
**Function**: `print_grid(clay_set, flowing, settled, min_x, max_x, min_y, max_y)`

**Purpose**: Essential for debugging - implement this FIRST before core algorithm.

**Algorithm**:
1. For each y in range(min_y-1, max_y+2):
   - Build row string
   - For each x in range(min_x-1, max_x+2):
     - If (x, y) in clay_set: append '#'
     - Elif (x, y) in settled: append '~'
     - Elif (x, y) in flowing: append '|'
     - Elif x == 500 and y == 0: append '+' (spring)
     - Else: append '.' (empty)
   - Print row with y-coordinate label
2. Print x-axis labels

**Usage**: Call this after simulation to visualize results and debug issues.

### 6. Main Simulation Loop
**Function**: `main()`

1. **Parse input** to get clay positions
2. **Get valid y-range** (min_y, max_y)
3. **Get x-range** for visualization: (min_x, max_x) from clay positions
4. **Initialize sets**: clay_set, flowing_water = set(), settled_water = set()
5. **Increase recursion limit**: `sys.setrecursionlimit(10000)` (for deep flows)
6. **Start simulation** from spring: `flow_down(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)`
7. **Optional: Print grid** for debugging: `print_grid(clay_set, flowing_water, settled_water, min_x, max_x, min_y, max_y)`
8. **Count water tiles** within valid range:
   - Use set comprehension for clarity:
   - `water_in_range = {(x, y) for (x, y) in flowing_water | settled_water if min_y <= y <= max_y}`
   - Return len(water_in_range)

**Note**: Start from y=0 even if outside range; the simulation will mark positions, and counting filters by range.

### 7. Implementation Details

**Key considerations**:
- **Memoization Strategy**: The `flowing_water` and `settled_water` sets serve as memoization:
  - If (x, y) in settled: already processed and settled, return True
  - If (x, y) in flowing: already processed as flowing path, return False
  - This prevents infinite loops and redundant processing

- **Recursion depth**: Python's default recursion limit (1000) is insufficient
  - Call `sys.setrecursionlimit(10000)` in main()
  - With input max_y ~1700, we need higher limit

- **State transitions**: Positions can change state:
  - Initially marked as flowing when first visited
  - Can transition to settled when container fills
  - Use set operations: remove from flowing, add to settled

- **Boundary conditions**:
  - Count only water in range [min_y, max_y]
  - Water flowing beyond max_y returns False (fell away)
  - Spring at y=0 may be outside range but simulation starts there

**Water behavior rules** (critical for correctness):
1. Water ALWAYS tries to flow down first
2. Water only spreads horizontally when it has support below (clay or settled water)
3. Water settles ONLY when contained on BOTH sides by clay walls
4. If contained on one side or neither side → water overflows and remains flowing
5. Overflow points recursively flow down, cascading the flow
6. Water can spread on top of previously settled water (settled provides support)

### 7. Algorithm Flow Example

For a simple container:
```
    #   #     (clay walls)
    # ~ #     (water settles)
    #~~~#     (water settles)
    #####     (clay floor)
```

**Detailed recursive flow**:

1. **Initial call**: flow_down(500, 0)
   - Marks (500, 0) as flowing
   - No support below at (500, 1), recursively calls flow_down(500, 1)

2. **flow_down(500, 1)**:
   - Marks (500, 1) as flowing
   - Continues down until hitting clay floor at (500, 5)

3. **flow_down(500, 4)** (one level above floor):
   - Marks (500, 4) as flowing
   - Finds clay support at (500, 5)
   - Calls spread_horizontal(500, 4, ...)
   - Spread finds walls on both sides (left at x=498, right at x=502)
   - Returns (is_contained=True, left_bound=499, right_bound=501)
   - Calls settle_water(4, 499, 501, ...) → settles row y=4
   - Returns True (provides support)

4. **Back to flow_down(500, 3)**:
   - Marks (500, 3) as flowing
   - Finds settled water support at (500, 4)
   - Calls spread_horizontal(500, 3, ...)
   - Spread finds walls on both sides
   - Settles row y=3
   - Returns True

5. **Process continues upward** through recursion until:
   - Water reaches a level with no walls (overflows), OR
   - Water reaches the spring level

**Key insight**: Containers fill from bottom to top through the natural recursion. Each call to flow_down() processes one level, and the return values propagate support information upward.

### 8. Optimization Notes

For the given input size (~1800 lines of clay definitions):
- Grid will be roughly 200-600 units wide, 1700 units tall
- Expected positions: ~30,000-50,000 tiles
- Recursive depth: up to max_y (~1700)
- Must increase recursion limit: `sys.setrecursionlimit(10000)`

**Performance**: O(W × H) time is acceptable for these dimensions, should complete in 1-3 seconds.

## Implementation Order (CRITICAL)

Follow this order to minimize debugging:

1. **Implement `parse_input()` and `get_y_range()`** - test with small input
2. **Implement `print_grid()`** - REQUIRED for debugging, do this early
3. **Implement `flow_down()` skeleton** - just downward flow, no spreading yet
4. **Test downward flow** - water should flow straight down
5. **Implement `spread_horizontal()`** - add horizontal spreading logic
6. **Test simple container** - water should settle in a U-shape
7. **Add overflow handling** - recursive flow_down from overflow points
8. **Test overflow cases** - water should overflow and continue falling
9. **Implement `settle_water()`** - convert flowing to settled
10. **Test complete example** - should produce 57 tiles
11. **Run on full input** - verify reasonable answer

## Testing Strategy Reference
- Test with example: should produce 57 tiles
- Verify settled vs flowing water distinction
- Test overflow behavior at container rim
- Test nested containers and vertical filling
- Ensure positions can transition from flowing → settled
