# Implementation Plan - Part 2: First Location Visited Twice

## Overview
This solution builds on Part 1's code by adding position tracking to detect the first location visited twice. The key difference is that we must track **every individual block** visited during movement, not just final positions after each instruction.

## Key Differences from Part 1
- **Part 1**: Calculate final position after all instructions
- **Part 2**: Detect the first position visited twice and stop immediately
- **Critical Detail**: Track each block moved, not just positions after completing instructions

## Algorithm Analysis

### Time Complexity
- **O(n × m)** where:
  - n = number of instructions
  - m = average steps per instruction
- Set lookups and insertions are O(1) on average
- Total positions visited is bounded by sum of all steps

### Space Complexity
- **O(n × m)** for the visited set
- In worst case (no revisits), we store every position visited

### Input Size Analysis
Looking at the input in `input.md`, there are approximately 145 instructions. The maximum step count appears to be 185. In the absolute worst case:
- Total steps = sum of all step values (likely < 10,000)
- Memory needed: < 10,000 positions × (2 integers + set overhead) = negligible
- This is very manageable even with a basic Python set

## Implementation Steps

### Step 1: Reuse Core Components from Part 1
**Files to reference**: `part_1_solution.py`

Reuse these existing functions (no changes needed):
- `parse_input(filename)` - Parse instructions into (turn, steps) tuples
- `turn_right(current_dir)` - Rotate direction index right
- `turn_left(current_dir)` - Rotate direction index left
- `calculate_manhattan_distance(x, y)` - Calculate distance from origin
- `DIRECTIONS` constant - Direction vectors array

**Rationale**: The input parsing and direction handling logic is identical between parts.

### Step 2: Implement Position Tracking During Movement
**New function**: `find_first_revisited_position(instructions) -> tuple[int, int]`

**Coordinate System Note**: Uses (x, y) where x increases going East and y increases going North.

This replaces Part 1's `follow_instructions()` function with a modified version that:

1. **Initialize state**:
   ```python
   x, y = 0, 0
   direction = 0  # North
   visited = set()
   visited.add((0, 0))  # IMPORTANT: Mark starting position as visited BEFORE processing instructions
   ```

2. **For each instruction**:
   - Apply turn (L or R) to update direction
   - Get direction vector (dx, dy) from DIRECTIONS array
   - **Move one block at a time** (this is the critical part):
     ```python
     for step in range(steps):
         x += dx
         y += dy
         if (x, y) in visited:
             return x, y  # Found first revisit!
         visited.add((x, y))
     ```

3. **Return value**:
   - Return (x, y) tuple of first revisited position
   - If no revisit found after all instructions (unexpected), raise an exception:
     ```python
     raise ValueError("No position visited twice - unexpected!")
     ```
   - This helps catch bugs if the algorithm or input is incorrect

**Why step-by-step movement matters**:
- Example: Moving from (0,0) to (5,0) visits (1,0), (2,0), (3,0), (4,0), (5,0)
- If we only checked (5,0), we'd miss any revisits along the path
- The example in problem.md demonstrates this: R8, R4, R4, R8 revisits (4,0) which was visited during the first R8, not at its endpoint

### Step 3: Implement Main Solution Logic
**New function**: `solve_part2(filename)`

```python
def solve_part2(filename):
    instructions = parse_input(filename)
    revisited_x, revisited_y = find_first_revisited_position(instructions)
    distance = calculate_manhattan_distance(revisited_x, revisited_y)
    return distance, (revisited_x, revisited_y)
```

### Step 4: Update Main Function
Modify `main()` to:
1. Run verification with the provided example (R8, R4, R4, R8 → distance 4)
2. Process actual input from `input.md`
3. Print the first revisited position and its Manhattan distance
4. Perform sanity check (distance should be ≤ total steps)

### Step 5: Add Example Verification
**New function**: `verify_part2_example()`

Verify the example from problem.md:
- Input: R8, R4, R4, R8
- Expected first revisit: (4, 0)
- Expected distance: 4

Path trace for verification (coordinate system: x increases East, y increases North):
1. R8: Visit (1,0) through (8,0) facing East
2. R4: Visit (8,-1) through (8,-4) facing South
3. R4: Visit (7,-4) through (4,-4) facing West
4. R8 (North): Visit (4,-3), (4,-2), (4,-1), then (4,0) ← STOP (already visited in step 1)

## Code Structure

```
part_2_solution.py
│
├── DIRECTIONS (reused from Part 1)
├── parse_input() (reused from Part 1)
├── turn_right() (reused from Part 1)
├── turn_left() (reused from Part 1)
├── calculate_manhattan_distance() (reused from Part 1)
│
├── find_first_revisited_position() [NEW - core algorithm]
├── verify_part2_example() [NEW - example validation]
├── solve_part2() [NEW - main solver]
└── main() [MODIFIED - orchestrates Part 2 flow]
```

## Edge Cases to Handle

1. **Starting position**: Add (0,0) to visited set BEFORE processing any instructions
2. **Immediate revisit**: First instruction could return to (0,0)
3. **No revisit found**: Raise `ValueError("No position visited twice - unexpected!")` for debugging
4. **Single step movements**: Ensure loop handles steps=1 correctly
5. **Zero step movements**: Parse "R0" as 0 steps (though unlikely in input)
6. **Multiple revisits in one move**: If a single instruction crosses multiple visited positions, return immediately at the FIRST revisit encountered

## Optimization Considerations

Given the input size analysis:
- **No optimization needed** - basic set-based solution is sufficient
- Set operations (add, lookup) are O(1) average case
- Total positions < 10,000, which is trivial for modern hardware
- **Avoid premature optimization** - clarity over cleverness

## Testing Integration Points

The implementation should expose:
- `find_first_revisited_position(instructions)` - testable with custom instruction lists
- `verify_part2_example()` - validates against known example
- Clear output showing: position found, distance calculated

## Common Pitfalls to Avoid

1. **Don't skip intermediate positions**: Must check every block, not just endpoints
2. **Don't forget to mark starting position**: (0,0) is already visited
3. **Don't continue after finding revisit**: Return immediately on first match
4. **Don't confuse coordinate systems**: Maintain consistent (x,y) interpretation throughout
