# Problem Report: Mine Cart Last Survivor Detection

## Context from Part 1
Elves are transporting materials using carts on a track system. The track system uses curves, straight paths, and intersections. Multiple carts move simultaneously on these tracks.

In Part 1, we found the location of the **first collision** at coordinates `58,93`.

The system continues to have multiple carts that will eventually collide with each other.

## Part 2 Objective
Instead of finding the first collision, we now need to predict where the **last remaining cart** will be after all other carts have crashed and been removed from the system.

### New Collision Handling Rule
When any two carts collide:
- **Both carts are instantly removed** from the track system
- The simulation continues with the remaining carts
- This process repeats until only one cart remains

## Objective
Find the location (X,Y coordinates) of the last cart remaining after all collisions have occurred and all other carts have been removed.

## Input Specification

### Track Components
The input is a 2D map where:
- **Straight tracks**: `|` (vertical) and `-` (horizontal)
- **Curves**: `/` and `\` (connect exactly two perpendicular track pieces)
- **Intersections**: `+` (where two perpendicular paths cross)

### Cart Representation
Carts are represented by directional characters:
- `^` - facing up
- `v` - facing down
- `<` - facing left
- `>` - facing right

**Important**: On the initial map, the track under each cart is a straight path matching the cart's direction (the cart character replaces the track character).

## Movement Rules

### Cart Movement
1. Carts move one step at a time in the direction they're facing
2. On straight tracks (`|` or `-`), carts continue straight
3. On curves (`/` or `\`), carts turn 90 degrees following the curve
4. At intersections (`+`), carts follow a specific turning pattern (see below)

### Turn Order
Carts move in a specific order each tick:
- Top row first (left to right)
- Then second row (left to right)
- Continue row by row, top to bottom

### Intersection Behavior
When a cart reaches an intersection (`+`), it follows a repeating pattern:
1. **First intersection**: turn LEFT
2. **Second intersection**: go STRAIGHT
3. **Third intersection**: turn RIGHT
4. **Fourth intersection**: turn LEFT (pattern repeats)

Each cart tracks its own intersection count independently - this is not based on which physical intersection it's at, but on how many intersections this particular cart has encountered.

### Collision Detection and Removal (Part 2 Behavior)
- When two carts occupy the same location during a tick, they collide
- **Both carts involved in the collision are immediately removed** from the system
- Collisions are detected immediately after a cart moves (before other carts in the same tick move)
- **Important**: If a cart is removed due to collision, it doesn't complete any remaining moves in that tick
- The simulation continues with the remaining carts until only one cart is left

## Output Specification

### Format
Return the coordinates as `X,Y` where:
- **X** = column number (leftmost column is 0)
- **Y** = row number (topmost row is 0)

### Example
For the last cart at column 6, row 4, output: `6,4`

## Input Data
The input is provided in `input.md` - the same multi-line text map from Part 1 showing:
- Track layout (using `|`, `-`, `/`, `\`, `+`)
- Initial cart positions and directions (using `^`, `v`, `<`, `>`)

## Algorithm Requirements

1. Parse the input map to extract:
   - Track layout
   - Initial cart positions and directions

2. Simulate cart movement tick by tick:
   - Sort carts by position (top to bottom, left to right)
   - Move each cart one step (skip carts that have been removed)
   - Update cart direction based on track type
   - Check for collisions after each move
   - **Remove both carts** involved in any collision
   - Continue until only one cart remains

3. Return the coordinates of the last remaining cart in `X,Y` format

## Key Differences from Part 1
- **Part 1**: Stop at the first collision and return its location
- **Part 2**: Remove both carts when they collide, continue simulation until only one cart remains, return that cart's location
