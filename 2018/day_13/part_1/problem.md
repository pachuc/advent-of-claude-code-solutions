# Problem Report: Mine Cart Collision Detection

## Context
Elves are transporting materials using carts on a track system. The track system uses curves, straight paths, and intersections. Multiple carts move simultaneously on these tracks, and we need to detect when and where the first collision occurs.

## Objective
Find the location (X,Y coordinates) of the first collision between carts moving on a track system.

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

### Collision Detection
- When two carts occupy the same location, they collide
- We need to find the location of the **first** collision
- Collisions are detected immediately after a cart moves (before other carts in the same tick move)

## Output Specification

### Format
Return the coordinates as `X,Y` where:
- **X** = column number (leftmost column is 0)
- **Y** = row number (topmost row is 0)

### Example
For a collision at column 7, row 3, output: `7,3`

## Input Data
The input is provided in `input.md` - a multi-line text map showing:
- Track layout (using `|`, `-`, `/`, `\`, `+`)
- Initial cart positions and directions (using `^`, `v`, `<`, `>`)

## Algorithm Requirements

1. Parse the input map to extract:
   - Track layout
   - Initial cart positions and directions

2. Simulate cart movement tick by tick:
   - Sort carts by position (top to bottom, left to right)
   - Move each cart one step
   - Update cart direction based on track type
   - Check for collisions after each move

3. Return the coordinates of the first collision in `X,Y` format
