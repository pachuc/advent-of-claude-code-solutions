# Implementation Plan: Hexagonal Grid Navigation Distance

## Problem Analysis

We need to find the minimum number of steps to reach a final position on a hexagonal grid after executing a series of moves. The hexagonal grid has 6 directions: n, ne, se, s, sw, nw.

### Key Insights

1. **Coordinate System**: Use cube coordinates (x, y, z) for hexagonal grids where x + y + z = 0
2. **Distance Calculation**: Manhattan distance in cube coordinates divided by 2 gives the shortest path
3. **Move Tracking**: Each direction modifies the cube coordinates in a specific way
4. **Input Size**: The input contains ~7000+ moves, so efficiency matters but O(n) is acceptable

### Algorithm Complexity

- **Time Complexity**: O(n) where n is the number of moves (single pass through input)
- **Space Complexity**: O(1) - only storing coordinate values
- This is optimal since we must process each move at least once

## Implementation Steps

### Step 1: Parse Input

```python
def parse_input(filename='input.md'):
    """
    Read the input file and parse comma-separated moves.

    Returns:
        List[str]: List of direction strings
    """
    with open(filename, 'r') as f:
        content = f.read().strip()
    # Handle empty input: empty string split returns [''], not []
    if not content:
        return []
    # Strip whitespace from each move for robustness
    return [move.strip() for move in content.split(',') if move.strip()]
```

**Details**:
- Read file content and strip whitespace
- Handle empty input explicitly (returns empty list)
- Split by comma and strip whitespace from each move
- Filter out any empty strings from the split
- Return list of move strings

### Step 2: Define Cube Coordinate System

```python
# Cube coordinate deltas for each direction
DIRECTION_DELTAS = {
    'n':  (0, 1, -1),   # North: y increases, z decreases
    'ne': (1, 0, -1),   # Northeast: x increases, z decreases
    'se': (1, -1, 0),   # Southeast: x increases, y decreases
    's':  (0, -1, 1),   # South: y decreases, z increases
    'sw': (-1, 0, 1),   # Southwest: x decreases, z increases
    'nw': (-1, 1, 0)    # Northwest: x decreases, y increases
}
```

**Details**:
- Cube coordinates maintain invariant: x + y + z = 0
- Each direction maps to a delta tuple (dx, dy, dz)
- These deltas ensure the invariant is preserved after each move

### Step 3: Process Moves and Track Position

```python
def calculate_final_position(moves):
    """
    Process all moves and calculate final cube coordinates.

    Args:
        moves: List of direction strings

    Returns:
        Tuple[int, int, int]: Final (x, y, z) cube coordinates
    """
    x, y, z = 0, 0, 0  # Start at origin

    for move in moves:
        # Input validation (optional but recommended for robustness)
        if move not in DIRECTION_DELTAS:
            raise ValueError(f"Invalid direction: '{move}'. Valid directions: n, ne, se, s, sw, nw")

        dx, dy, dz = DIRECTION_DELTAS[move]
        x += dx
        y += dy
        z += dz

    return (x, y, z)
```

**Details**:
- Initialize position at origin (0, 0, 0)
- Validate each move is a valid direction (prevents KeyError)
- For each move, add the corresponding delta to current position
- Return final coordinates
- No need to track path history, only final position matters

### Step 4: Calculate Manhattan Distance in Cube Coordinates

```python
def calculate_distance(x, y, z):
    """
    Calculate shortest distance from origin to (x, y, z) in hexagonal grid.

    The distance formula for cube coordinates is:
    distance = (|x| + |y| + |z|) / 2

    This works because in cube coordinates with x + y + z = 0,
    the Manhattan distance divided by 2 gives the actual hex distance.

    Args:
        x, y, z: Cube coordinates

    Returns:
        int: Minimum number of steps to reach position from origin
    """
    return (abs(x) + abs(y) + abs(z)) // 2
```

**Details**:
- Use Manhattan distance formula for cube coordinates
- Divide by 2 because in cube coordinates, each hex step affects 2 coordinates
- Use integer division (//) since result is always an integer
- This formula is mathematically proven for hexagonal grids with cube coordinates

**Mathematical Proof**:
- In cube coordinates: x + y + z = 0 (always)
- At origin: x = y = z = 0
- After moves: some coordinates are positive, some negative
- The sum |x| + |y| + |z| counts each step twice (one coordinate increases, another decreases)
- Therefore, distance = (|x| + |y| + |z|) / 2

### Step 5: Main Solution Function

```python
def solve():
    """
    Main solution function.

    Returns:
        int: Minimum number of steps to reach final position from origin
    """
    # Parse input
    moves = parse_input('input.md')

    # Calculate final position
    x, y, z = calculate_final_position(moves)

    # Calculate distance from origin
    distance = calculate_distance(x, y, z)

    return distance
```

**Details**:
- Orchestrate the solution steps
- Parse input → process moves → calculate distance
- Return the final answer

### Step 6: Script Entry Point

```python
if __name__ == '__main__':
    result = solve()
    print(result)
```

**Details**:
- Execute solve() when script is run directly
- Print result to stdout
- Keep output clean (just the number)

## Complete File Structure

```
solution.py
├── Constants: DIRECTION_DELTAS
├── Functions:
│   ├── parse_input()
│   ├── calculate_final_position()
│   ├── calculate_distance()
│   └── solve()
└── Main execution block
```

## Efficiency Considerations

1. **Single Pass**: Process moves in O(n) time with one iteration
2. **Constant Space**: Only store 3 coordinate values regardless of input size
3. **No Optimization Needed**: Don't need to simplify moves (e.g., n+s=cancel) because we only care about final position
4. **Direct Calculation**: Distance formula is O(1) after processing moves

## Edge Cases Handled

1. **Empty path**: Returns 0 (stay at origin) - handled by returning empty list from parse_input
2. **Return to origin**: Returns 0 (all moves cancel out)
3. **Single direction**: Returns number of moves in that direction
4. **Large input**: Efficiently handles 7000+ moves with O(n) complexity
5. **All directions**: Correctly handles any combination of the 6 directions
6. **Whitespace in input**: Strips whitespace from moves during parsing
7. **Invalid directions**: Raises ValueError with helpful message (prevents silent errors)
