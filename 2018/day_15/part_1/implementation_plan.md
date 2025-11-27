# Implementation Plan: Beverage Bandits Combat Simulation

## Overview
Implement a turn-based combat simulator for Elves vs Goblins on a 2D grid with specific movement and attack rules.

## Updates from Critique
This plan has been updated to address the following key issues from the critique:
1. **Grid as single source of truth**: Clarified that the grid is dynamically updated and is the authoritative source for unit positions
2. **Occupied square detection**: Explicitly specified to check `grid[y][x] in ['E', 'G']` rather than iterating units
3. **BFS implementation details**: Added specifics about using `collections.deque` and data structures
4. **Direction order vs reading order**: Clarified these are different concepts
5. **Function signatures**: Removed unnecessary `units` parameter from functions that only need the grid
6. **Input file reading**: Added explicit code example for reading from `input.md`
7. **Max rounds safety limit**: Added 10000 round limit to prevent infinite loops in edge cases
8. **Adjacency checks**: Specified exact formula: `abs(dx) + abs(dy) == 1`
9. **Mid-round ending**: Added clear example of when rounds don't increment

## Algorithm Efficiency Analysis

**Input Size**: The grid is approximately 32x32 = 1024 cells with ~15-20 units initially.

**Time Complexity Targets**:
- Per turn per unit: O(W×H) for BFS pathfinding where W,H are grid dimensions
- Total rounds: Typically 50-100 rounds (units have 200 HP, 3 damage = ~67 hits to kill)
- Overall: O(rounds × units × W × H) ≈ O(75 × 15 × 1024) ≈ 1.15M operations - highly manageable

**Space Complexity**: O(W×H) for grid and BFS queue - negligible for this problem size.

**Conclusion**: Straightforward BFS approach is sufficient. No need for A* or advanced optimizations.

## Data Structures

### 1. Grid Representation
```python
# 2D list of characters: '#', '.', 'E', 'G'
# The grid is the SINGLE SOURCE OF TRUTH for current unit positions
# It is DYNAMIC - updated whenever units move or die
grid = [list(row) for row in input_lines]
```

### 2. Unit Class
```python
class Unit:
    def __init__(self, x, y, unit_type):
        self.x = x              # Current x position
        self.y = y              # Current y position
        self.type = unit_type   # 'E' or 'G'
        self.hp = 200           # Hit points
        self.attack = 3         # Attack power
        self.alive = True       # Status flag
```

### 3. Units List
```python
# List of all Unit objects
# Re-sorted each round in reading order
units = []
```

## Implementation Steps

### Step 1: Parse Input
**File**: `solution.py`

```python
def parse_input(input_text):
    """
    Parse grid and create Unit objects.

    Returns:
        - grid: 2D list of characters
        - units: list of Unit objects
    """
    # 1. Split input into lines
    # 2. Create 2D grid
    # 3. Scan grid for 'E' and 'G'
    # 4. Create Unit object for each E/G
    # 5. Initially keep E/G on grid (grid will be dynamically updated as units move/die)
    # 6. Return grid and units list
```

**Why**: Separates parsing logic; units list allows easy iteration while grid tracks positions.

### Step 2: Reading Order Sort
**File**: `solution.py`

```python
def reading_order(pos):
    """Sort key for reading order: (y, x)"""
    return (pos[1], pos[0])  # or (pos.y, pos.x) for Unit objects

def sort_units(units):
    """Sort living units in reading order"""
    return sorted([u for u in units if u.alive],
                  key=lambda u: (u.y, u.x))
```

**Why**: Reading order (top-to-bottom, left-to-right) is critical for turn order and tie-breaking.

### Step 3: Find Targets
**File**: `solution.py`

```python
def find_targets(unit, units):
    """
    Find all living enemy units.

    Args:
        unit: Current unit
        units: All units

    Returns:
        List of enemy Unit objects
    """
    # 1. Get enemy type ('E' if unit is 'G', vice versa)
    # 2. Filter units: alive and enemy type
    # 3. Return filtered list
```

**Why**: Needed to check if combat should end and to find in-range squares.

### Step 4: BFS Pathfinding
**File**: `solution.py`

```python
def bfs_distances(grid, start_x, start_y):
    """
    BFS to find distances to all reachable squares.

    Args:
        grid: 2D grid (single source of truth for positions)
        start_x, start_y: Starting position

    Returns:
        Dict of (x, y): distance

    Implementation notes:
        - Use collections.deque for efficient queue operations
        - Check neighbors in direction order: up, left, right, down
        - A square is passable if grid[y][x] == '.'
        - A square is occupied if grid[y][x] in ['E', 'G']
        - The grid is the single source of truth for current positions
        - Starting position should be included in result ONLY if it's '.'
          (when pathfinding from destination, it will be '.')
    """
    from collections import deque

    # 1. Initialize distances dict (empty initially)
    # 2. Only proceed if start position is valid:
    #    - If grid[start_y][start_x] == '.': add to distances as {(start_x, start_y): 0}
    #    - Otherwise return empty dict (starting from a unit or wall position)
    # 3. Create queue: deque([(start_x, start_y)])
    # 4. While queue not empty:
    #    a. Dequeue position (x, y)
    #    b. Get current distance from distances dict
    #    c. Check 4 neighbors in direction order: up, left, right, down
    #    d. For each neighbor at (nx, ny):
    #       - Skip if out of bounds
    #       - Skip if grid[ny][nx] != '.' (wall or occupied by unit)
    #       - Skip if (nx, ny) already in distances
    #       - Add to distances with current_distance + 1
    #       - Enqueue (nx, ny)
    # 5. Return distances dict
```

**Why**: BFS guarantees shortest path. Dictionary allows O(1) distance lookup.

### Step 5: Find In-Range Squares
**File**: `solution.py`

```python
def find_in_range_squares(targets, grid):
    """
    Find all open squares adjacent to any target.

    Args:
        targets: List of enemy units
        grid: 2D grid (single source of truth)

    Returns:
        Set of (x, y) tuples
    """
    # 1. Initialize empty set
    # 2. For each target:
    #    - Check 4 adjacent squares in all directions
    #    - For each adjacent position (ax, ay):
    #      * Skip if out of bounds
    #      * If grid[ay][ax] == '.', add (ax, ay) to set
    # 3. Return set
```

**Why**: These are potential movement destinations.

### Step 6: Choose Destination
**File**: `solution.py`

```python
def choose_destination(unit, targets, grid):
    """
    Choose which in-range square to move toward.

    Returns:
        (x, y) of chosen destination, or None if no valid destination
    """
    # 1. Get in-range squares using find_in_range_squares()
    # 2. If empty, return None (no targets have adjacent open squares)
    # 3. Run BFS from unit's current position
    # 4. Filter in-range squares to only reachable ones (present in BFS distances dict)
    # 5. If none reachable, return None (targets exist but unreachable)
    # 6. Find minimum distance among reachable in-range squares
    # 7. Filter to squares with minimum distance (may be multiple)
    # 8. Sort by reading order (y, x) and return first
```

**Why**: Implements the "nearest in-range square, reading order tie-break" rule.

### Step 7: Choose Next Step
**File**: `solution.py`

```python
def choose_next_step(unit, destination, grid):
    """
    Choose which adjacent square to move to.

    This is tricky: must consider all shortest paths from unit to destination.
    We do this by running BFS from the DESTINATION backward.

    Returns:
        (x, y) of next position
    """
    # 1. Run BFS from DESTINATION backward to find distances from destination
    # 2. Check 4 adjacent squares to unit in DIRECTION ORDER: up, left, right, down
    #    (This corresponds to: (0,-1), (-1,0), (1,0), (0,1) in (dx,dy))
    # 3. For each adjacent square at (ax, ay):
    #    - Must be passable: grid[ay][ax] == '.'
    #    - Must be reachable from destination: (ax, ay) in BFS distances
    # 4. Among valid adjacent squares, find minimum distance to destination
    # 5. Return the FIRST valid square with minimum distance (due to direction order check)
```

**Why**: Moving toward destination requires BFS from destination to ensure we're on a shortest path.

### Step 8: Attack Target Selection
**File**: `solution.py`

```python
def choose_attack_target(unit, targets):
    """
    Choose which adjacent enemy to attack.

    Returns:
        Unit object to attack, or None
    """
    # 1. Filter targets to only adjacent ones
    #    - Adjacent means: abs(target.x - unit.x) + abs(target.y - unit.y) == 1
    # 2. If no adjacent enemies, return None
    # 3. Find minimum HP among adjacent enemies
    # 4. Filter to enemies with minimum HP (may be multiple)
    # 5. Sort by reading order (y, x): sorted(key=lambda t: (t.y, t.x))
    # 6. Return first from sorted list
```

**Why**: Implements "lowest HP, reading order tie-break" rule.

### Step 9: Execute Unit Turn
**File**: `solution.py`

```python
def execute_turn(unit, units, grid):
    """
    Execute one unit's turn: move and attack.

    Returns:
        True if combat continues, False if no targets found
    """
    # 1. Find targets using find_targets()
    # 2. If no targets exist, return False (combat ends immediately)
    #
    # MOVEMENT PHASE:
    # 3. Check if already adjacent to any target:
    #    any(abs(t.x - unit.x) + abs(t.y - unit.y) == 1 for t in targets)
    # 4. If not adjacent:
    #    a. Choose destination using choose_destination()
    #    b. If destination exists (not None):
    #       - Choose next step using choose_next_step()
    #       - Update grid: grid[unit.y][unit.x] = '.'
    #       - Update unit: unit.x, unit.y = next_step
    #       - Update grid: grid[unit.y][unit.x] = unit.type
    #
    # ATTACK PHASE:
    # 5. After movement (or if skipped), choose attack target using choose_attack_target()
    # 6. If attack target exists (not None):
    #    a. Reduce target HP: target.hp -= unit.attack
    #    b. If target.hp <= 0:
    #       - Set target.alive = False
    #       - Update grid: grid[target.y][target.x] = '.'
    # 7. Return True (combat continues)
```

**Why**: Encapsulates full turn logic for one unit.

### Step 10: Execute Round
**File**: `solution.py`

```python
def execute_round(units, grid):
    """
    Execute one full round of combat.

    Returns:
        True if round completed fully, False if ended mid-round
    """
    # 1. Sort units in reading order
    # 2. For each unit:
    #    a. Skip if not alive (may have died earlier this round)
    #    b. Execute unit's turn
    #    c. If turn returns False (no targets), return False
    # 3. Return True (round completed)
```

**Why**: Handles round execution and mid-round ending detection.

### Step 11: Main Combat Loop
**File**: `solution.py`

```python
def simulate_combat(grid, units):
    """
    Run full combat simulation.

    Returns:
        Number of completed rounds

    Example: If Round 68 starts and the first unit finds no targets,
    combat ends immediately. Final round count is 67, NOT 68.
    """
    # 1. Initialize round counter to 0
    # 2. Add optional safety limit: max_rounds = 10000 (prevents infinite loops in edge cases)
    # 3. Loop while rounds < max_rounds:
    #    a. Execute round using execute_round()
    #    b. If round returns False (ended mid-round), break WITHOUT incrementing
    #    c. Otherwise increment round counter
    # 4. Return round counter
```

**Why**: Main simulation loop.

### Step 12: Calculate Outcome
**File**: `solution.py`

```python
def calculate_outcome(rounds, units):
    """
    Calculate final outcome value.

    Returns:
        rounds × sum_of_remaining_hp
    """
    # 1. Filter units to alive ones
    # 2. Sum their HP
    # 3. Multiply by rounds
    # 4. Return result
```

**Why**: Implements outcome formula.

### Step 13: Main Function
**File**: `solution.py`

```python
def main():
    """Main entry point"""
    # 1. Read input from input.md:
    #    with open('input.md', 'r') as f:
    #        input_text = f.read()
    # 2. Parse input: grid, units = parse_input(input_text)
    # 3. Simulate combat: rounds = simulate_combat(grid, units)
    # 4. Calculate outcome: result = calculate_outcome(rounds, units)
    # 5. Print result: print(result)

if __name__ == "__main__":
    main()
```

## Key Implementation Details

### Direction Order
Always use this order for consistency:
```python
# These are (dx, dy) deltas where x is column and y is row
# Up means y-1 (row decreases), Down means y+1 (row increases)
# Left means x-1 (column decreases), Right means x+1 (column increases)
DIRECTIONS = [
    (0, -1),  # Up: same column, row above
    (-1, 0),  # Left: column to left, same row
    (1, 0),   # Right: column to right, same row
    (0, 1)    # Down: same column, row below
]
```
This ensures proper direction checking for movement decisions.

Note: Direction order (up, left, right, down) is DIFFERENT from reading order.
- **Reading order** compares positions as (y, x) for sorting
- **Direction order** is the sequence we check adjacent squares

### Grid Updates
**CRITICAL**: The grid is the single source of truth for current unit positions.

When a unit moves:
1. Set old position to '.': `grid[old_y][old_x] = '.'`
2. Update unit coordinates: `unit.x, unit.y = new_x, new_y`
3. Set new position to unit type: `grid[new_y][new_x] = unit.type`

When a unit dies:
1. Set alive flag: `unit.alive = False`
2. Clear grid position: `grid[unit.y][unit.x] = '.'`

To check if a square is occupied:
- Check `grid[y][x] in ['E', 'G']` (do NOT iterate through units list)

### Unit Death
Set `alive = False` immediately when HP <= 0. Check `alive` flag before executing turn.

### Mid-Round Ending
Critical: If a unit finds no targets at start of turn, combat ends immediately. That round does NOT count as completed.

## Testing Checkpoints

1. **Parsing**: Verify grid and units created correctly
2. **Reading Order**: Verify units sorted correctly
3. **BFS**: Test pathfinding on small grids
4. **Movement**: Verify correct destination and step chosen
5. **Attack**: Verify correct target selected
6. **Full Round**: Test on simple scenarios
7. **Final**: Test on provided example

## Estimated Complexity

- **Time**: O(R × U × W × H) where R=rounds, U=units, W,H=dimensions
  - For this input: ~75 × 15 × 32 × 32 ≈ 1.15M operations
  - Should run in under 1 second
- **Space**: O(W × H + U) ≈ O(1024 + 15) - negligible

## Common Pitfalls to Avoid

1. **Wrong reading order**: (x, y) vs (y, x) - use (y, x) for reading order
2. **Unit acts after death**: Check `alive` flag before turn
3. **Grid not updated**: Update grid immediately after move/death
4. **Off-by-one rounds**: Don't count incomplete final round
5. **Wrong BFS direction**: Must check all 4 directions in reading order
6. **Multiple paths**: When choosing step, must use BFS from destination
7. **Target selection**: Must check HP first, then reading order
