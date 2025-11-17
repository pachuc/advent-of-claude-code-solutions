# Testing Plan: Taxicab Distance Calculator

## Testing Strategy Overview

Test the solution with:
1. Provided examples from problem statement
2. Edge cases for direction handling
3. Edge cases for position tracking
4. Actual puzzle input validation

## Test 1: Provided Examples

### Test 1.1: Simple Path (R2, L3)
**Input:** `R2, L3`

**Expected behavior:**
- Start: (0, 0) facing North
- Turn right → East, move 2 → (2, 0)
- Turn left → North, move 3 → (2, 3)
- Distance: |2| + |3| = 5

**Expected output:** `5`

**Verification method:**
```python
instructions = [('R', 2), ('L', 3)]
x, y = follow_instructions(instructions)
assert (x, y) == (2, 3)
assert calculate_manhattan_distance(x, y) == 5
```

### Test 1.2: Square Path (R2, R2, R2)
**Input:** `R2, R2, R2`

**Expected behavior:**
- Start: (0, 0) facing North
- R2: East → (2, 0)
- R2: South → (2, -2)
- R2: West → (0, -2)
- Distance: |0| + |-2| = 2

**Expected output:** `2`

**Verification method:**
```python
instructions = [('R', 2), ('R', 2), ('R', 2)]
x, y = follow_instructions(instructions)
assert (x, y) == (0, -2)
assert calculate_manhattan_distance(x, y) == 2
```

### Test 1.3: Complex Path (R5, L5, R5, R3)
**Input:** `R5, L5, R5, R3`

**Expected behavior:**
- Start: (0, 0) facing North
- R5: East → (5, 0)
- L5: North → (5, 5)
- R5: East → (10, 5)
- R3: South → (10, 2)
- Distance: |10| + |2| = 12

**Expected output:** `12`

**Verification method:**
```python
instructions = [('R', 5), ('L', 5), ('R', 5), ('R', 3)]
x, y = follow_instructions(instructions)
assert (x, y) == (10, 2)
assert calculate_manhattan_distance(x, y) == 12
```

## Test 2: Edge Cases - Direction Handling

### Test 2.1: Four Right Turns (Full Circle)
**Input:** `R1, R1, R1, R1`

**Purpose:** Verify direction wrapping works correctly

**Expected behavior:**
- Should return to same direction after 4 right turns
- Path: (0,0) → (1,0) → (1,-1) → (0,-1) → (0,0)
- Final position: (0, 0)
- Distance: 0

**Verification method:**
```python
instructions = [('R', 1), ('R', 1), ('R', 1), ('R', 1)]
x, y = follow_instructions(instructions)
assert (x, y) == (0, 0)
assert calculate_manhattan_distance(x, y) == 0
```

### Test 2.2: Four Left Turns (Full Circle)
**Input:** `L1, L1, L1, L1`

**Purpose:** Verify left turn wrapping works correctly

**Expected behavior:**
- Should return to same direction after 4 left turns
- Path: (0,0) → (-1,0) → (-1,-1) → (0,-1) → (0,0)
- Final position: (0, 0)
- Distance: 0

**Verification method:**
```python
instructions = [('L', 1), ('L', 1), ('L', 1), ('L', 1)]
x, y = follow_instructions(instructions)
assert (x, y) == (0, 0)
assert calculate_manhattan_distance(x, y) == 0
```

### Test 2.3: Mixed Turns
**Input:** `R1, L1`

**Purpose:** Verify R then L returns to original direction

**Expected behavior:**
- R1: East → (1, 0)
- L1: North → (1, 1)
- Distance: 2

**Verification method:**
```python
instructions = [('R', 1), ('L', 1)]
x, y = follow_instructions(instructions)
assert (x, y) == (1, 1)
assert calculate_manhattan_distance(x, y) == 2
```

## Test 3: Edge Cases - Position Tracking

### Test 3.1: Large Single Step
**Input:** `R100`

**Purpose:** Verify large step values work correctly

**Expected behavior:**
- Position: (100, 0)
- Distance: 100

**Verification method:**
```python
instructions = [('R', 100)]
x, y = follow_instructions(instructions)
assert (x, y) == (100, 0)
assert calculate_manhattan_distance(x, y) == 100
```

### Test 3.2: Zero Net Displacement
**Input:** `R5, R5, R5, R5`

**Purpose:** Verify path that returns to origin

**Expected behavior:**
- Should return to (0, 0)
- Distance: 0

**Verification method:**
```python
instructions = [('R', 5), ('R', 5), ('R', 5), ('R', 5)]
x, y = follow_instructions(instructions)
assert (x, y) == (0, 0)
assert calculate_manhattan_distance(x, y) == 0
```

### Test 3.3: Negative Coordinates
**Input:** `R1, R1`

**Purpose:** Verify negative coordinates handled correctly

**Expected behavior:**
- R1: East → (1, 0)
- R1: South → (1, -1)
- Distance: |1| + |-1| = 2

**Verification method:**
```python
instructions = [('R', 1), ('R', 1)]
x, y = follow_instructions(instructions)
assert (x, y) == (1, -1)
assert calculate_manhattan_distance(x, y) == 2
```

## Test 4: Input Parsing

### Test 4.1: Parsing Format
**Purpose:** Verify input parsing handles format correctly and various whitespace patterns

**Test cases:**
- Standard format with spaces: `"R5, L3, R2"`
- No spaces after comma: `"R5,L3,R2"`
- Extra whitespace: `"R5 ,  L3 , R2"`
- Large numbers: `"R185"`
- Single instruction: `"R5"`

**Verification method:**
```python
# Create a temporary test function that parses strings directly
def test_parsing():
    # Test standard format
    content = "R5, L3, R2"
    instructions = [inst.strip() for inst in content.split(',')]
    parsed = [(inst[0], int(inst[1:])) for inst in instructions]
    assert parsed == [('R', 5), ('L', 3), ('R', 2)]

    # Test no spaces
    content = "R5,L3,R2"
    instructions = [inst.strip() for inst in content.split(',')]
    parsed = [(inst[0], int(inst[1:])) for inst in instructions]
    assert parsed == [('R', 5), ('L', 3), ('R', 2)]

    # Test extra whitespace
    content = "R5 ,  L3 , R2"
    instructions = [inst.strip() for inst in content.split(',')]
    parsed = [(inst[0], int(inst[1:])) for inst in instructions]
    assert parsed == [('R', 5), ('L', 3), ('R', 2)]

    # Test large number
    content = "R185"
    instructions = [inst.strip() for inst in content.split(',')]
    parsed = [(inst[0], int(inst[1:])) for inst in instructions]
    assert parsed == [('R', 185)]
```

## Test 5: Actual Puzzle Input

### Test 5.1: Run with Actual Input
**Input:** Content from `input.md`

**Purpose:** Verify solution works with real puzzle input

**Verification method:**
1. Run the complete solution with `input.md`
2. Verify output is a positive integer
3. Manually trace first 5 instructions to verify correctness:
   - Start: (0, 0) facing North
   - R3: face East, move 3 → (3, 0)
   - R1: face South, move 1 → (3, -1)
   - R4: face West, move 4 → (-1, -1)
   - L4: face South, move 4 → (-1, -5)
   - R3: face West, move 3 → (-4, -5)
   - Expected position after 5 instructions: (-4, -5)
   - Expected distance after 5 instructions: |-4| + |-5| = 9

4. Perform bounds check:
   - Count total number of instructions (should be ~141 based on input)
   - Calculate sum of all step values
   - Verify result ≤ sum of all steps

**Expected output:** Some positive integer between 0 and sum of all steps

## Test 6: Bounds Checking

### Test 6.1: Sanity Check for Valid Range
**Purpose:** Verify the result is within mathematically valid bounds

**Verification method:**
```python
def test_bounds_check():
    instructions = parse_input('input.md')
    final_x, final_y = follow_instructions(instructions)
    distance = calculate_manhattan_distance(final_x, final_y)

    # Calculate maximum possible distance
    total_steps = sum(steps for _, steps in instructions)

    # Result must be between 0 and total_steps
    assert 0 <= distance <= total_steps, \
        f"Distance {distance} is outside valid range [0, {total_steps}]"

    print(f"Bounds check passed: {distance} ∈ [0, {total_steps}]")
```

**Expected behavior:**
- Minimum distance = 0 (if path returns to origin)
- Maximum distance = sum of all steps (if all in same direction)
- Actual result must fall within this range

## Test 7: Helper Function Tests

### Test 7.1: Turn Functions
**Purpose:** Verify turn logic in isolation

**Verification method:**
```python
# Test turn_right
assert turn_right(0) == 1  # North → East
assert turn_right(1) == 2  # East → South
assert turn_right(2) == 3  # South → West
assert turn_right(3) == 0  # West → North (wrap)

# Test turn_left
assert turn_left(0) == 3  # North → West
assert turn_left(3) == 2  # West → South
assert turn_left(2) == 1  # South → East
assert turn_left(1) == 0  # East → North (wrap)
```

### Test 7.2: Manhattan Distance
**Purpose:** Verify distance calculation in isolation

**Verification method:**
```python
assert calculate_manhattan_distance(0, 0) == 0
assert calculate_manhattan_distance(5, 0) == 5
assert calculate_manhattan_distance(0, 5) == 5
assert calculate_manhattan_distance(3, 4) == 7
assert calculate_manhattan_distance(-3, -4) == 7
assert calculate_manhattan_distance(-3, 4) == 7
assert calculate_manhattan_distance(3, -4) == 7
```

## Testing Execution Plan

### Phase 1: Unit Tests
1. Test helper functions (turn_right, turn_left, calculate_manhattan_distance) - Test 7
2. Test input parsing with sample data - Test 4
3. Verify each function works in isolation

### Phase 2: Integration Tests
1. Test with provided examples (Test 1.1, 1.2, 1.3) - Test 1
2. Test edge cases (Test 2 and Test 3)
3. Verify end-to-end flow

### Phase 3: Validation
1. Run with actual puzzle input - Test 5
2. Spot-check first 5 instructions manually
3. Verify output is within valid bounds - Test 6
4. Verify output is reasonable (positive integer)

## Test File Structure

Create `test_solution.py`:
```python
from solution import *

def test_helper_functions():
    """Test turn and distance functions - Test 7"""
    # Test 7.1: Turn functions
    assert turn_right(0) == 1  # North → East
    assert turn_right(1) == 2  # East → South
    assert turn_right(2) == 3  # South → West
    assert turn_right(3) == 0  # West → North

    assert turn_left(0) == 3   # North → West
    assert turn_left(3) == 2   # West → South
    assert turn_left(2) == 1   # South → East
    assert turn_left(1) == 0   # East → North

    # Test 7.2: Manhattan distance
    assert calculate_manhattan_distance(0, 0) == 0
    assert calculate_manhattan_distance(3, 4) == 7
    assert calculate_manhattan_distance(-3, -4) == 7
    print("✓ Helper functions test passed")

def test_examples():
    """Test provided examples - Test 1"""
    # Test 1.1
    x, y = follow_instructions([('R', 2), ('L', 3)])
    assert (x, y) == (2, 3)
    assert calculate_manhattan_distance(x, y) == 5

    # Test 1.2
    x, y = follow_instructions([('R', 2), ('R', 2), ('R', 2)])
    assert (x, y) == (0, -2)
    assert calculate_manhattan_distance(x, y) == 2

    # Test 1.3
    x, y = follow_instructions([('R', 5), ('L', 5), ('R', 5), ('R', 3)])
    assert (x, y) == (10, 2)
    assert calculate_manhattan_distance(x, y) == 12
    print("✓ Examples test passed")

def test_direction_edge_cases():
    """Test direction wrapping - Test 2"""
    # Test 2.1: Four right turns
    x, y = follow_instructions([('R', 1), ('R', 1), ('R', 1), ('R', 1)])
    assert (x, y) == (0, 0)

    # Test 2.2: Four left turns
    x, y = follow_instructions([('L', 1), ('L', 1), ('L', 1), ('L', 1)])
    assert (x, y) == (0, 0)

    # Test 2.3: Mixed turns
    x, y = follow_instructions([('R', 1), ('L', 1)])
    assert (x, y) == (1, 1)
    print("✓ Direction edge cases test passed")

def test_position_edge_cases():
    """Test position tracking - Test 3"""
    # Test 3.1: Large single step
    x, y = follow_instructions([('R', 100)])
    assert (x, y) == (100, 0)

    # Test 3.2: Return to origin
    x, y = follow_instructions([('R', 5), ('R', 5), ('R', 5), ('R', 5)])
    assert (x, y) == (0, 0)

    # Test 3.3: Negative coordinates
    x, y = follow_instructions([('R', 1), ('R', 1)])
    assert (x, y) == (1, -1)
    print("✓ Position edge cases test passed")

def test_bounds_check():
    """Test bounds checking - Test 6"""
    instructions = parse_input('input.md')
    final_x, final_y = follow_instructions(instructions)
    distance = calculate_manhattan_distance(final_x, final_y)

    total_steps = sum(steps for _, steps in instructions)
    assert 0 <= distance <= total_steps
    print(f"✓ Bounds check passed: {distance} ∈ [0, {total_steps}]")

if __name__ == '__main__':
    test_helper_functions()
    test_examples()
    test_direction_edge_cases()
    test_position_edge_cases()
    test_bounds_check()
    print("\n✓ All tests passed!")
```

## Success Criteria

✓ All helper functions work correctly in isolation
✓ All provided examples produce correct output
✓ Direction wrapping works correctly (both left and right)
✓ Negative coordinates handled properly
✓ Input parsing handles various whitespace formats
✓ Actual puzzle input produces a valid integer result
✓ Result is within valid bounds (0 to sum of all steps)
✓ Manual spot-check of first 5 instructions confirms correctness

## Summary of Changes from Original Plan

Based on the critique, the following improvements were made:

1. **More robust input parsing** - Now handles variations in whitespace
2. **Simplified Test 4.1** - Uses in-memory test data instead of creating separate files
3. **Fixed Test 2.1 description** - Clarified expected path and removed incorrect position
4. **Fixed Test 2.2 description** - Clarified path notation instead of confusing tuple format
5. **Added Test 6** - Bounds checking to verify result is mathematically valid
6. **Enhanced Test 5.1** - Added specific manual verification for first 5 instructions with expected results
7. **Complete test implementation** - Provided fully working test code instead of just signatures
8. **Better test organization** - Renumbered tests logically (Test 6 for bounds, Test 7 for helpers)
