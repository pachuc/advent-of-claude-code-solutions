# Implementation Plan: Jump Instruction Maze (Part 2)

## Overview
Modify the Part 1 solution to implement a conditional offset modification rule based on the offset value.

## Algorithm Analysis

### Key Changes from Part 1
- **Part 1 Rule**: Always increment offset by 1 after jumping
- **Part 2 Rule**:
  - If offset >= 3: decrement by 1 (offset -= 1)
  - If offset < 3: increment by 1 (offset += 1)

### Performance Considerations
- **Input size**: 1,038 instructions
- **Expected complexity**: O(n) where n is the number of steps
- **Part 1 result**: 339,351 steps
- **Part 2 behavior**: The conditional decrement for large offsets (>= 3) creates different dynamics than Part 1. The example shows a 2x increase (5 → 10 steps), but actual behavior depends on the input distribution. The result could be higher or lower than Part 1.
- **Memory**: O(1038) - single list modified in place
- **Runtime**: Unknown until execution. Could range from seconds to minutes depending on the loop patterns created by the conditional modification rule.
- **No optimization needed**: Simple simulation with conditional logic is the correct approach

### Algorithm Strategy
Direct simulation approach (same as Part 1):
1. Parse input into list of integers
2. Start at position 0, step counter at 0
3. While position is within bounds:
   - Read offset at current position
   - Apply conditional modification rule to offset
   - Jump to new position
   - Increment step counter
4. Return total steps

## Implementation Steps

### Step 1: Reuse Part 1 Parser
- Copy the `parse_input()` function from `part_1_solution.py`
- No changes needed - same input format

### Step 2: Modify the Solve Function
- Copy the `solve()` function structure from `part_1_solution.py`
- Locate the offset modification line (line 19 in Part 1)
- Replace `instructions[position] += 1` with conditional logic:
  ```python
  if instructions[position] >= 3:
      instructions[position] -= 1
  else:
      instructions[position] += 1
  ```
- Keep all other logic identical (position tracking, bounds checking, step counting)

### Step 3: Create Main Execution Block
- Same structure as Part 1:
  - Read from 'input.md'
  - Call solve function
  - Print result

### Step 4: Code Structure
```python
def parse_input(filename):
    """Parse the input file and return a list of integers."""
    # Reuse from Part 1

def simulate(instructions):
    """Run simulation on a list of instructions (modifies in place)."""
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]

        # PART 2 CHANGE: Conditional modification
        if offset >= 3:
            instructions[position] -= 1
        else:
            instructions[position] += 1

        position += offset
        steps += 1

    return steps

def solve(filename):
    """Solve the jump instruction maze with conditional offset modification."""
    instructions = parse_input(filename)
    return simulate(instructions)

if __name__ == "__main__":
    result = solve('input.md')
    print(result)
```

**Note**: The `simulate()` helper function enables code reuse in test cases and keeps the logic in one place.

## Implementation Details

### Critical Logic Points
1. **Order of operations**:
   - Read offset BEFORE modification
   - Modify offset at current position
   - Jump using the ORIGINAL offset value (not the modified one)

2. **Conditional check**:
   - Use the already-read `offset` variable: `if offset >= 3`
   - Check `>= 3` (not `> 3`)
   - Decrement for large offsets (unlike Part 1)
   - Increment for small offsets (same as Part 1)

3. **Exit condition**:
   - Same as Part 1: `position < 0 or position >= len(instructions)`
   - Loop continues while: `0 <= position < len(instructions)`

### Edge Cases to Handle
- Zero offsets (< 3, so increment to 1)
- Negative offsets (< 3, so increment toward zero)
- Exactly 3 (>= 3, so decrement to 2)
- Large positive offsets (>= 3, so they decrease over time)

## Expected Behavior

### Example Trace
Input: `[0, 3, 0, 1, -3]`
Expected output: **10 steps** (steps 0-9)

| Step | Pos | Offset | Offset >= 3? | Modification | Jump | New List |
|------|-----|--------|--------------|--------------|------|----------|
| 0 | 0 | 0 | No | +1 | +0 | `[1, 3, 0, 1, -3]` |
| 1 | 0 | 1 | No | +1 | +1 | `[2, 3, 0, 1, -3]` |
| 2 | 1 | 3 | Yes | -1 | +3 | `[2, 2, 0, 1, -3]` |
| 3 | 4 | -3 | No | +1 | -3 | `[2, 2, 0, 1, -2]` |
| 4 | 1 | 2 | No | +1 | +2 | `[2, 3, 0, 1, -2]` |
| 5 | 3 | 1 | No | +1 | +1 | `[2, 3, 0, 2, -2]` |
| 6 | 4 | -2 | No | +1 | -2 | `[2, 3, 0, 2, -1]` |
| 7 | 2 | 0 | No | +1 | +0 | `[2, 3, 1, 2, -1]` |
| 8 | 2 | 1 | No | +1 | +1 | `[2, 3, 2, 2, -1]` |
| 9 | 3 | 2 | No | +1 | +2 | `[2, 3, 2, 3, -1]` |
| 10 | 5 | EXIT | - | - | - | - |

Result: 10 steps ✓

## Validation Approach
- Run with example input: should produce 10 steps
- Run with actual input: should produce a positive integer (may be higher or lower than Part 1's 339,351)
- Verify the conditional logic is correct by tracing first few steps manually
- Optionally verify Part 1 logic still produces 339,351 as a regression test
