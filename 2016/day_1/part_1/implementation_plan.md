# Implementation Plan: Taxicab Distance Calculator

## Overview
Implement a Python script to calculate Manhattan distance from origin after following turn-and-move instructions on a 2D grid.

## Algorithm Design

### Time Complexity: O(n)
- n = number of instructions
- Each instruction requires constant time processing

### Space Complexity: O(1)
- Only need to track current position and direction
- No need to store the path or history

## Step-by-Step Implementation

### Step 1: Input Parsing
**File:** `solution.py`

1. Read the input from `input.md`
2. Strip whitespace and split by comma
3. Handle variations in whitespace (e.g., `R2,L3` vs `R2, L3`)
4. Parse each instruction into:
   - Turn direction: 'L' or 'R' (first character)
   - Steps: integer (remaining characters)
5. Store as list of tuples: `[(turn, steps), ...]`

**Implementation details:**
```python
def parse_input(filename):
    with open(filename, 'r') as f:
        content = f.read().strip()
    # Split by comma and strip whitespace from each instruction
    instructions = [inst.strip() for inst in content.split(',')]
    parsed = [(inst[0], int(inst[1:])) for inst in instructions]
    return parsed
```

### Step 2: Direction Management
**File:** `solution.py`

1. Represent 4 cardinal directions using indices 0-3:
   - 0: North (0, 1)
   - 1: East (1, 0)
   - 2: South (0, -1)
   - 3: West (-1, 0)

2. Store direction vectors in a list for easy lookup

3. Track current direction as index (0-3)

4. Implement turn logic:
   - Right turn: `direction = (direction + 1) % 4`
   - Left turn: `direction = (direction - 1) % 4` or `(direction + 3) % 4`

**Implementation details:**
```python
# Direction vectors: [North, East, South, West]
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def turn_right(current_dir):
    return (current_dir + 1) % 4

def turn_left(current_dir):
    return (current_dir - 1) % 4  # Python handles negative modulo correctly
```

### Step 3: Position Tracking
**File:** `solution.py`

1. Initialize position at origin: `x = 0, y = 0`
2. Initialize facing direction: `direction = 0` (North)

3. For each instruction:
   - Apply turn (update direction index)
   - Get direction vector from DIRECTIONS list
   - Update position: `x += dx * steps`, `y += dy * steps`

**Implementation details:**
```python
def follow_instructions(instructions):
    x, y = 0, 0
    direction = 0  # Start facing North

    for turn, steps in instructions:
        # Apply turn
        if turn == 'R':
            direction = turn_right(direction)
        else:  # turn == 'L'
            direction = turn_left(direction)

        # Move forward
        dx, dy = DIRECTIONS[direction]
        x += dx * steps
        y += dy * steps

    return x, y
```

### Step 4: Manhattan Distance Calculation
**File:** `solution.py`

1. Calculate Manhattan distance from origin:
   - `distance = abs(x) + abs(y)`
2. Return the result

**Implementation details:**
```python
def calculate_manhattan_distance(x, y):
    return abs(x) + abs(y)
```

### Step 5: Verification Helper
**File:** `solution.py`

1. Create a helper function to verify solution against examples
2. Run before processing actual input to catch implementation errors

**Implementation details:**
```python
def verify_with_examples():
    """Verify implementation with provided examples"""
    # Example 1: R2, L3 → distance 5
    test1 = [('R', 2), ('L', 3)]
    x, y = follow_instructions(test1)
    assert (x, y) == (2, 3), f"Example 1 failed: got {(x, y)}, expected (2, 3)"
    assert calculate_manhattan_distance(x, y) == 5

    # Example 2: R2, R2, R2 → distance 2
    test2 = [('R', 2), ('R', 2), ('R', 2)]
    x, y = follow_instructions(test2)
    assert (x, y) == (0, -2), f"Example 2 failed: got {(x, y)}, expected (0, -2)"
    assert calculate_manhattan_distance(x, y) == 2

    # Example 3: R5, L5, R5, R3 → distance 12
    test3 = [('R', 5), ('L', 5), ('R', 5), ('R', 3)]
    x, y = follow_instructions(test3)
    assert (x, y) == (10, 2), f"Example 3 failed: got {(x, y)}, expected (10, 2)"
    assert calculate_manhattan_distance(x, y) == 12

    print("All examples verified successfully!")
```

### Step 6: Sanity Check Helper
**File:** `solution.py`

1. Calculate bounds for the answer to verify reasonableness
2. Maximum distance = sum of all steps (if all in same direction)
3. Minimum distance = 0 (if path returns to origin)

**Implementation details:**
```python
def sanity_check(instructions, result):
    """Verify the result is within reasonable bounds"""
    total_steps = sum(steps for _, steps in instructions)
    max_distance = total_steps
    min_distance = 0

    assert min_distance <= result <= max_distance, \
        f"Result {result} is outside valid range [{min_distance}, {max_distance}]"

    print(f"Sanity check passed: {result} is within bounds [0, {max_distance}]")
```

### Step 7: Main Function
**File:** `solution.py`

1. Orchestrate the entire solution:
   - Verify implementation with examples first
   - Parse input from `input.md`
   - Follow instructions to get final position
   - Calculate Manhattan distance
   - Run sanity check
   - Print the result

**Implementation details:**
```python
def main():
    # Verify implementation with examples
    verify_with_examples()

    # Process actual input
    instructions = parse_input('input.md')
    final_x, final_y = follow_instructions(instructions)
    distance = calculate_manhattan_distance(final_x, final_y)

    # Sanity check the result
    sanity_check(instructions, distance)

    print(f"Manhattan distance: {distance}")

if __name__ == '__main__':
    main()
```

## Complete Solution Structure

```
solution.py
├── DIRECTIONS (constant)
├── parse_input(filename) -> list of tuples
├── turn_right(direction) -> int
├── turn_left(direction) -> int
├── follow_instructions(instructions) -> (x, y)
├── calculate_manhattan_distance(x, y) -> int
├── verify_with_examples() -> None
├── sanity_check(instructions, result) -> None
└── main()
```

## Implementation Notes

1. **Robust parsing**: Handle variations in whitespace (comma with/without spaces)
2. **Built-in verification**: Run examples before processing actual input
3. **Sanity checking**: Verify result is within valid bounds
4. **No error handling needed**: Per requirements, we assume valid input format
5. **No logging**: Keep it simple for script purposes
6. **Direct calculation**: No need to store path history
7. **Efficient**: O(n) time complexity is optimal for this problem
8. **Clean code**: Use functions for modularity and testability

## Expected Behavior

1. Verify implementation with provided examples (catches bugs early)
2. Read instructions from `input.md`
3. Process each turn-and-move instruction sequentially
4. Track position changes in 2D space
5. Perform sanity check on result
6. Output final Manhattan distance as single integer

## Summary of Changes from Original Plan

Based on the critique, the following improvements were made:

1. **More robust input parsing** - Added `.strip()` to handle variations in whitespace (e.g., `R2,L3` vs `R2, L3`)
2. **Added verification step** - `verify_with_examples()` runs all provided examples before processing actual input
3. **Added sanity check** - `sanity_check()` verifies result is within valid bounds [0, sum of all steps]
4. **Updated solution structure** - Added two new helper functions for verification and validation
5. **Enhanced main function** - Now includes verification and sanity checking steps
6. **Better implementation notes** - Clarified the importance of verification and bounds checking
