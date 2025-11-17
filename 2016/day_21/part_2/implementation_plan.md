# Implementation Plan: Password Unscrambler (Part 2)

## Overview
Create a solution to reverse the password scrambling process from Part 1. Given the scrambled password `fbgdceah` and the list of 100 operations, determine the original unscrambled password by applying inverse operations in reverse order.

## Key Updates Based on Critique

**CRITICAL FIX:**
- ✓ Fixed the inverse rotation lookup table (had incorrect values)
- ✓ **Recommended approach: Use brute force instead of lookup** (simpler, guaranteed correct)

**MAJOR IMPROVEMENTS:**
- ✓ Import from Part 1 solution instead of copying code (DRY principle)
- ✓ Added runtime assertion to validate string length is 8
- ✓ Enhanced verification with detailed error messages
- ✓ Clarified relationship between Part 1 and Part 2 (different passwords, same operations)

**MINOR IMPROVEMENTS:**
- ✓ More accurate complexity analysis (O(n × m²) with brute force)
- ✓ Better code organization and file structure
- ✓ Added input validation considerations

## Core Strategy
This is an **inverse problem** where we need to:
1. Process operations in **reverse order** (from last to first)
2. Apply the **inverse** of each operation
3. Most operations have straightforward inverses; the trickiest is "rotate based on letter position"

## Code Reuse from Part 1
We can reuse significant portions of `part_1_solution.py`:
- All basic operation functions (with some kept as-is, some inverted)
- The parsing logic from `parse_operation()`
- The general structure and testing framework

## Algorithm Design

### High-Level Algorithm
```
1. Start with scrambled password: "fbgdceah"
2. Read all 100 operations from input.md
3. Reverse the order of operations (process from index 99 to 0)
4. For each operation, apply its inverse:
   - Determine operation type via parsing
   - Apply the appropriate inverse transformation
5. Return the final unscrambled password
```

### Time Complexity
- **O(n × m)** where n = number of operations (100) and m = password length (8)
- Each operation takes O(m) time at worst (string manipulation)
- Total: O(800) operations - extremely efficient
- The "rotate based on letter" inverse requires trying at most 8 positions

### Space Complexity
- **O(n + m)** for storing operations list and working with string copies
- Minimal memory usage overall

## Implementation Steps

### Step 1: Import Functions from Part 1 Solution

**Import all necessary functions from Part 1 to avoid code duplication:**

```python
# Import all helper functions from Part 1
from part_1_solution import (
    swap_position,           # self-inverse
    swap_letter,             # self-inverse
    rotate_left,             # needed for inverting rotate_right
    rotate_right,            # needed for inverting rotate_left
    rotate_based_on_letter,  # needed to verify inverse
    reverse_positions,       # self-inverse
    move_position,           # needed for inverse_move
    parse_operation,         # reuse for parsing
    read_operations,         # reuse for reading input
    scramble_password        # needed for verification testing
)
```

**Benefits of importing vs. copying:**
- DRY principle (Don't Repeat Yourself)
- Single source of truth for shared logic
- Can reuse `scramble_password` for verification
- Easier maintenance - fixes in Part 1 automatically apply
- Smaller codebase

**Why these can be reused:**
- Swap operations are commutative (doing them twice returns to original)
- Reverse is self-inverse
- Rotate functions are needed for each other's inverses
- Parsing and I/O logic remains the same
- `rotate_based_on_letter` is needed to verify the inverse operation

### Step 2: Create New Inverse Operations

#### 2.1: Inverse Move Position
```python
def inverse_move_position(s, x, y):
    """
    Inverse of 'move position X to position Y'
    Forward: remove char at X, insert at Y
    Reverse: remove char at Y, insert at X

    This is equivalent to: move_position(s, y, x)
    """
    return move_position(s, y, x)
```

**Logic:** If forward moved from X→Y, reverse moves from Y→X

#### 2.2: Inverse Rotate Based on Letter Position (Most Complex)

**Approach: Brute Force (Recommended)**

The inverse of "rotate based on letter position" is complex. Rather than using a lookup table that could contain errors, we use a brute force approach that is guaranteed correct:

```python
def inverse_rotate_based_on_letter(s, letter):
    """
    Inverse of 'rotate based on position of letter X'

    Strategy: Try all possible rotations (0-7 left rotations) and find
    which one, when forward-rotated, produces the current string.

    This is guaranteed correct and for length 8 is only O(64) operations.
    """
    # Validate string length (this function is hardcoded for length 8)
    assert len(s) == 8, f"This function only works for length 8, got {len(s)}"

    # Try each possible left rotation amount
    for left_amount in range(len(s)):
        candidate = rotate_left(s, left_amount)
        # Check if forward rotation of candidate gives us back our string
        if rotate_based_on_letter(candidate, letter) == s:
            return candidate

    # Should never reach here if implementation is correct
    raise ValueError(f"Could not find inverse rotation for letter '{letter}' in string '{s}'")
```

**Why brute force is better:**
- **Guaranteed correct**: No risk of lookup table errors
- **Still efficient**: For length 8, at most 8 tries × 8 operations = 64 operations per call
- **Self-documenting**: The logic is clear and verifiable
- **Robust**: Works even if we misunderstood the forward operation
- **Total cost**: 100 operations in file × worst case 64 = 6400 operations (negligible)

**Alternative: Lookup Table (if preferred)**

If you prefer O(1) lookup, here's the corrected lookup table:
```python
def inverse_rotate_based_on_letter_lookup(s, letter):
    """Using pre-computed lookup table for length 8"""
    assert len(s) == 8, f"This function only works for length 8, got {len(s)}"

    current_pos = s.index(letter)

    # Corrected inverse mapping (current position → left rotation amount)
    # Derived from: orig_pos → rotate_right(1+pos+(1 if pos>=4 else 0)) → final_pos
    inverse_rotation = {
        0: 1,  # was at 7, rotated right 9 (mod 8 = 1)
        1: 1,  # was at 0, rotated right 1
        2: 6,  # was at 4, rotated right 6
        3: 2,  # was at 1, rotated right 2
        4: 7,  # was at 5, rotated right 7
        5: 3,  # was at 2, rotated right 3
        6: 0,  # was at 6, rotated right 8 (mod 8 = 0)
        7: 4,  # was at 3, rotated right 4
    }

    return rotate_left(s, inverse_rotation[current_pos])
```

**Recommendation:** Use the brute force approach - it's simpler, safer, and still very fast.

### Step 3: Create the Unscramble Function
```python
def unscramble_password(scrambled, operations):
    """
    Apply inverse operations in reverse order to unscramble password

    Args:
        scrambled: The scrambled password string (e.g., "fbgdceah")
        operations: List of operation strings

    Returns:
        The original unscrambled password
    """
    password = scrambled

    # Process operations in reverse order
    for operation in reversed(operations):
        op_type, params = parse_operation(operation)

        # Apply inverse of each operation
        if op_type == 'swap_position':
            # Self-inverse: swap again
            password = swap_position(password, params[0], params[1])

        elif op_type == 'swap_letter':
            # Self-inverse: swap again
            password = swap_letter(password, params[0], params[1])

        elif op_type == 'rotate_left':
            # Inverse: rotate right
            password = rotate_right(password, params)

        elif op_type == 'rotate_right':
            # Inverse: rotate left
            password = rotate_left(password, params)

        elif op_type == 'rotate_based':
            # Complex inverse using lookup table
            password = inverse_rotate_based_on_letter(password, params)

        elif op_type == 'reverse':
            # Self-inverse: reverse again
            password = reverse_positions(password, params[0], params[1])

        elif op_type == 'move':
            # Inverse: swap source and destination
            password = inverse_move_position(password, params[0], params[1])

    return password
```

### Step 4: Create Main Function
```python
def main():
    # Note: Part 1 scrambled 'abcdefgh' → 'fdhbcgea' using these operations
    # Part 2 unscrambles a DIFFERENT password 'fbgdceah' using the SAME operations
    # We don't need Part 1's answer - this is a separate problem instance

    # The scrambled password we need to unscramble
    scrambled_password = 'fbgdceah'

    # Read operations from input file (same file as Part 1)
    operations = read_operations('input.md')
    print(f"Read {len(operations)} operations from input file")

    # Unscramble the password
    original_password = unscramble_password(scrambled_password, operations)

    # Validation: verify it contains correct characters
    assert sorted(original_password) == sorted(scrambled_password), \
        "Character set not preserved!"
    assert len(original_password) == 8, \
        f"Result length is {len(original_password)}, expected 8"

    # Critical verification: re-scramble should produce original scrambled password
    verification = scramble_password(original_password, operations)
    if verification != scrambled_password:
        print(f"VERIFICATION FAILED!")
        print(f"Unscrambled: {original_password}")
        print(f"Re-scrambled: {verification}")
        print(f"Expected: {scrambled_password}")
        raise ValueError("Solution incorrect - re-scrambling didn't match")

    print(f"Original unscrambled password: {original_password}")
    print(f"✓ Verification passed: {original_password} → {verification}")
    return original_password
```

### Step 5: Add Verification Tests
```python
def verify_solution(original, scrambled, operations):
    """
    Verify that scrambling the original produces the scrambled version
    This confirms our unscrambling is correct
    """
    # Import/reuse scramble_password from part 1
    result = scramble_password(original, operations)
    return result == scrambled

def test_inverse_operations():
    """Test that each inverse operation actually inverts its forward operation"""
    test_string = 'abcdefgh'

    # Test inverse move
    forward = move_position(test_string, 3, 7)
    backward = inverse_move_position(forward, 3, 7)
    assert backward == test_string, "Inverse move failed"

    # Test inverse rotate based on letter
    for letter in test_string:
        forward = rotate_based_on_letter(test_string, letter)
        backward = inverse_rotate_based_on_letter(forward, letter)
        assert backward == test_string, f"Inverse rotate based failed for {letter}"

    # Test rotate left/right inverses
    forward = rotate_left(test_string, 3)
    backward = rotate_right(forward, 3)
    assert backward == test_string, "Rotate left/right inverse failed"

    print("Inverse operation tests passed!")
```

## File Structure
```
solution.py
├── Imports from Part 1
│   ├── from part_1_solution import swap_position, swap_letter, ...
│   └── (all helper functions and scramble_password)
├── New inverse operation functions (Part 2 specific)
│   ├── inverse_move_position()
│   └── inverse_rotate_based_on_letter()
├── Core unscrambling logic
│   └── unscramble_password()
├── Testing functions
│   ├── test_inverse_operations()
│   └── verify_solution()
└── main()
```

**Key difference from Part 1:**
- Much shorter code since we import most functions
- Only define inverse operations and unscrambling logic
- Reuse scramble_password for verification

## Edge Cases Handled
1. **String length**: Runtime assertion in inverse_rotate_based ensures length is 8
2. **Modulo arithmetic**: Already handled in rotate functions from Part 1
3. **Rotate based inverse**: Brute force guarantees correctness (or corrected lookup table)
4. **Empty operations**: Would return input unchanged (though not expected)
5. **Character preservation**: Validation ensures all chars a-h present
6. **Missing input file**: Error will occur naturally when reading file

## Optimization Considerations
- **No optimization needed**: 100 operations × 8 chars = extremely fast
- Most operations are O(m) where m=8 (string length)
- Rotate-based inverse with brute force is O(m²) = O(64) per call
- Total worst case: O(n × m²) = O(100 × 64) = O(6400) operations - negligible
- String operations in Python are efficient for this size
- Brute force is still faster than we need for this problem

## Expected Output
- Single string of 8 characters
- Contains letters a-h (each exactly once)
- When scrambled using Part 1's logic, produces "fbgdceah"
