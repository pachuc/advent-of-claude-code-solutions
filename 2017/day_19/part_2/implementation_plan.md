# Implementation Plan: Network Packet Routing - Step Count (Part 2)

## Overview
Part 2 requires counting the total number of steps taken while following the same path from Part 1. We can reuse almost all of the Part 1 solution, with a simple modification to count steps instead of collecting letters.

## Summary of Changes from Part 1

**What stays the same (95% of code)**:
- All helper functions: `parse_input()`, `find_start()`, `get_perpendicular()`, `is_valid_position()`, `is_path_char()`, `get_next_position()`
- All direction constants and logic
- The `main()` function structure
- Path-following algorithm and termination logic

**What changes (only in `follow_path()` function)**:
- Replace `letters = []` with `steps = 0`
- Remove letter collection logic (`if current_char.isalpha()...`)
- Add `steps += 1` to count each position
- Return `steps` instead of `''.join(letters)`

**Critical detail**: The step counter MUST increment BEFORE checking for the next move to avoid off-by-one errors.

## Algorithm Analysis

### Reusable Components from Part 1
The entire path-following algorithm from `part_1_solution.py` can be reused:
- **Grid parsing**: `parse_input()` - unchanged
- **Starting position finder**: `find_start()` - unchanged
- **Direction handling**: `get_perpendicular()` - unchanged
- **Position validation**: `is_valid_position()` - unchanged
- **Path character detection**: `is_path_char()` - unchanged
- **Path traversal logic**: `get_next_position()` - unchanged

### Required Modification
Only the `follow_path()` function needs modification:
- **Remove**: Letter collection logic
- **Add**: Step counter that increments for each position visited
- **Keep**: Same traversal loop and termination condition

### Complexity Analysis
- **Time Complexity**: O(n) where n is the number of cells in the path
  - We visit each cell in the path exactly once
  - Each position check is O(1)
  - The input size is fixed (the routing diagram dimensions)
- **Space Complexity**: O(w × h) where w and h are the grid dimensions
  - Store the entire grid in memory
  - A few variables for current position, direction, and step count

### Performance Considerations
Based on the input size (~200 lines × variable width):
- The grid has at most ~40,000 characters
- The actual path is much shorter (a single continuous line)
- Expected runtime: milliseconds (very efficient)
- No optimization needed for this input size

## Step-by-Step Implementation Plan

### Step 1: Copy Part 1 Solution Structure
- Copy the entire `part_1_solution.py` as the starting point
- This includes all imports, constants, and helper functions
- **Rationale**: 95% of the code is identical; start with working code

### Step 2: Modify the `follow_path()` Function
**Current behavior** (Part 1):
```python
def follow_path(grid, start_row, start_col):
    letters = []
    row, col = start_row, start_col
    direction = DOWN

    while True:
        current_char = grid[row][col]
        if current_char.isalpha() and current_char.isupper():
            letters.append(current_char)

        next_move = get_next_position(grid, row, col, direction)
        if next_move is None:
            break
        row, col, direction = next_move

    return ''.join(letters)
```

**New behavior** (Part 2):
```python
def follow_path(grid, start_row, start_col):
    steps = 0
    row, col = start_row, start_col
    direction = DOWN

    while True:
        steps += 1  # Count current position

        next_move = get_next_position(grid, row, col, direction)
        if next_move is None:
            break
        row, col, direction = next_move

    return steps
```

**Key changes**:
- Replace `letters = []` with `steps = 0`
- Remove letter collection logic (the `if current_char.isalpha()` block)
- Add `steps += 1` to count each position visited
- Return `steps` instead of `''.join(letters)`

**CRITICAL: Step Counter Placement**

The placement of `steps += 1` BEFORE checking for the next move is essential to avoid off-by-one errors:

**Why this is correct**:
1. **First iteration**: We enter the loop at the starting position
   - Increment `steps` from 0 to 1 ✓ (starting position counted)
   - Check for next move and continue

2. **Intermediate iterations**: We're at a valid path position
   - Increment `steps` ✓ (current position counted)
   - Move to next position

3. **Final iteration**: We're at the last path position
   - Increment `steps` ✓ (final position counted)
   - `get_next_position()` returns `None`
   - Break from loop

**What would go wrong if we counted AFTER the move**:
- The final position would NOT be counted (we'd break before counting it)
- Result would be off by one (e.g., 37 instead of 38 for the example)

**Verification trace for minimal path `| A |`**:
- Iteration 1: At first `|`, steps=1, move to A
- Iteration 2: At A, steps=2, move to last `|`
- Iteration 3: At last `|`, steps=3, no next move, break
- Result: 3 ✓

### Step 3: Update the `main()` Function
Minimal change needed:
```python
def main():
    """Main function to solve the problem."""
    grid = parse_input('input.md')
    start = find_start(grid)

    if start is None:
        print("No starting position found")
        return

    result = follow_path(grid, start[0], start[1])
    print(result)  # Will now print an integer instead of letters
```

The only change: `result` will be an integer instead of a string, but `print()` handles both.

### Step 4: Update Documentation
- Update the module docstring to reflect Part 2's purpose
- Update the `follow_path()` docstring to describe step counting
- Update any comments that reference letter collection

### Step 5: Verify Input File Reference
- Ensure the script reads from 'input.md' (same as Part 1)
- No changes needed since both parts use the same input

## Implementation Checklist

1. [ ] Copy all constants and direction definitions from Part 1
2. [ ] Copy all helper functions unchanged:
   - `parse_input()`
   - `find_start()`
   - `get_perpendicular()`
   - `is_valid_position()`
   - `is_path_char()`
   - `get_next_position()`
3. [ ] Modify `follow_path()` to count steps instead of collecting letters
4. [ ] Ensure `steps += 1` is placed BEFORE the next move check
5. [ ] Keep `main()` function (works for both integer and string output)
6. [ ] Update docstrings and comments to reflect Part 2 purpose
7. [ ] Run example test immediately after implementation to verify 38 steps
8. [ ] Run on actual input to get the solution

## Expected Code Structure

```
solution.py
├── Shebang and module docstring
├── Direction constants (UP, DOWN, LEFT, RIGHT, DIRECTIONS)
├── parse_input(filename) - unchanged
├── find_start(grid) - unchanged
├── get_perpendicular(direction) - unchanged
├── is_valid_position(grid, row, col) - unchanged
├── is_path_char(char) - unchanged
├── get_next_position(grid, row, col, direction) - unchanged
├── follow_path(grid, start_row, start_col) - MODIFIED to count steps
└── main() - unchanged
```

## Example Validation

Using the example from the problem:
```
     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
```

Expected path breakdown:
- 6 steps down (including the first line at the top)
- 3 steps right
- 4 steps up
- 3 steps right
- 4 steps down
- 3 steps right
- 2 steps up
- 13 steps left (including F where it stops)

**Total: 38 steps**

The modified `follow_path()` should return 38 for this example.

## Edge Cases Analysis

### Inherited from Part 1 (Already Handled)
Since we're reusing the Part 1 algorithm, these are already handled:
- ✓ Grid parsing with variable line lengths
- ✓ Finding the unique starting position
- ✓ Following corners and junctions correctly
- ✓ Stopping at the end of the path
- ✓ Handling line crossings (continue straight)
- ✓ Letters on the path (now just counted as regular steps)

### New Edge Case Specific to Part 2
**Single-position path**: What if the path consists of only the starting position with no valid next move?

**Example**:
```
|
```
(A single vertical bar with nowhere to go)

**Expected behavior**: Should return 1 (count the starting position)

**Verification**:
- Enter loop at the starting `|`
- Increment steps to 1
- `get_next_position()` returns `None` (no valid continuation)
- Break from loop
- Return 1 ✓

**Conclusion**: The current algorithm handles this correctly due to counting BEFORE checking for next move.

## Final Notes

This is a minimal modification problem. The algorithmic complexity remains the same, and we're simply changing what we track (steps instead of letters). The Part 1 solution is already efficient and handles all edge cases correctly, so Part 2 is straightforward.
