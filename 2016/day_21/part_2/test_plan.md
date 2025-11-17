# Testing Plan: Password Unscrambler (Part 2)

## Key Updates Based on Critique

**CRITICAL CHANGES:**
- ✓ **Reordered tests for fail-fast approach** - run critical tests FIRST
- ✓ Enhanced Test 1.2 with detailed output and validation
- ✓ Added Part 1 vs Part 2 clarification to Test 2.3

**MAJOR IMPROVEMENTS:**
- ✓ New `run_minimal_tests()` function for fast puzzle solving
- ✓ Clear prioritization: Must Pass vs Should Pass vs Nice to Have
- ✓ Optimized test execution order (critical tests in <2 seconds)
- ✓ Better debugging strategy focused on most likely failures

**TESTING PHILOSOPHY:**
- Focus on the two critical tests (1.2 and 2.3) that catch 99% of bugs
- Optional comprehensive testing available but not required
- Optimized for puzzle-solving context (not production software)

## Testing Objectives
1. **PRIMARY**: Verify inverse_rotate_based_on_letter works correctly (highest risk)
2. **PRIMARY**: Validate the actual solution produces correct answer
3. Verify other inverse operations work correctly
4. Ensure the unscrambling process produces a valid password
5. Validate that re-scrambling the result produces the original scrambled password

## Test Strategy

### Level 1: Unit Tests for Inverse Operations
Test each inverse operation individually to ensure correctness.

#### Test 1.1: Inverse Move Position
```python
def test_inverse_move():
    """Test that inverse_move_position correctly undoes move_position"""
    test_cases = [
        ('abcdefgh', 0, 7),  # Move first to last
        ('abcdefgh', 7, 0),  # Move last to first
        ('abcdefgh', 3, 5),  # Move middle positions
        ('abcdefgh', 2, 2),  # Move to same position (no-op)
    ]

    for string, x, y in test_cases:
        forward = move_position(string, x, y)
        backward = inverse_move_position(forward, x, y)
        assert backward == string, \
            f"Failed for move {x} to {y}: {string} -> {forward} -> {backward}"
```

**Expected Results:**
- All test cases should return to original string
- Moving to same position should be idempotent

#### Test 1.2: Inverse Rotate Based on Letter Position (CRITICAL TEST)
```python
def test_inverse_rotate_based():
    """
    Test the complex inverse rotation for all possible letter positions
    This is THE MOST CRITICAL test as this operation is the trickiest
    and was identified in the critique as having a potentially incorrect lookup table.

    The brute force approach guarantees correctness, so this test validates
    that the implementation works correctly.
    """
    test_string = 'abcdefgh'

    print("Testing inverse rotate based on letter...")

    # Test for each letter (representing each possible position 0-7)
    for letter in test_string:
        original = test_string

        # Apply forward rotation
        after_forward = rotate_based_on_letter(original, letter)

        # Apply inverse rotation
        after_inverse = inverse_rotate_based_on_letter(after_forward, letter)

        # Should return to original
        assert after_inverse == original, \
            f"Failed for letter '{letter}' at position {original.index(letter)}: " \
            f"{original} -> {after_forward} -> {after_inverse}"

        print(f"  ✓ Letter '{letter}' at pos {original.index(letter)}: " +
              f"{original} -> {after_forward} -> {after_inverse}")

    # Also test with different string configurations
    alternate_strings = [
        'hgfedcba',  # Reversed
        'bcdaefgh',  # Rotated
        'abefcdgh',  # Some swaps
        'fbgdceah',  # The actual scrambled password from Part 2
    ]

    for test_str in alternate_strings:
        for letter in test_str:
            forward = rotate_based_on_letter(test_str, letter)
            backward = inverse_rotate_based_on_letter(forward, letter)
            assert backward == test_str, \
                f"Failed for '{letter}' in '{test_str}': {test_str} -> {forward} -> {backward}"

    print("  ✓ All alternate string configurations passed")
```

**Expected Results:**
- All 8 letter positions should correctly invert
- Should work regardless of string configuration
- Validates the brute force approach (or corrected lookup table) is correct
- This test MUST pass before attempting the actual solution

#### Test 1.3: Rotate Left/Right Inverses
```python
def test_rotate_inverses():
    """Test that rotate left and right are inverses of each other"""
    test_string = 'abcdefgh'

    for steps in range(9):  # Test 0-8 steps
        # Test rotate_left inverted by rotate_right
        forward = rotate_left(test_string, steps)
        backward = rotate_right(forward, steps)
        assert backward == test_string, f"Failed for {steps} steps"

        # Test rotate_right inverted by rotate_left
        forward = rotate_right(test_string, steps)
        backward = rotate_left(forward, steps)
        assert backward == test_string, f"Failed for {steps} steps"
```

**Expected Results:**
- All rotation amounts should correctly invert
- Including edge cases: 0 steps and full rotation (8 steps)

#### Test 1.4: Self-Inverse Operations
```python
def test_self_inverse_operations():
    """Test that self-inverse operations return to original when applied twice"""
    test_string = 'abcdefgh'

    # Test swap_position
    result = swap_position(test_string, 2, 5)
    result = swap_position(result, 2, 5)
    assert result == test_string, "swap_position not self-inverse"

    # Test swap_letter
    result = swap_letter(test_string, 'a', 'h')
    result = swap_letter(result, 'a', 'h')
    assert result == test_string, "swap_letter not self-inverse"

    # Test reverse_positions
    result = reverse_positions(test_string, 1, 6)
    result = reverse_positions(result, 1, 6)
    assert result == test_string, "reverse_positions not self-inverse"
```

**Expected Results:**
- Each operation applied twice should return to original
- Validates that using same operation as inverse is correct

### Level 2: Integration Tests

#### Test 2.1: Simple Sequence Test
```python
def test_simple_sequence():
    """Test unscrambling a simple sequence of operations"""
    initial = 'abcdefgh'

    # Apply a few operations
    operations = [
        'swap position 0 with position 7',
        'rotate right 3 steps',
        'reverse positions 2 through 5',
        'move position 1 to position 4',
    ]

    # Scramble
    scrambled = scramble_password(initial, operations)

    # Unscramble
    unscrambled = unscramble_password(scrambled, operations)

    # Should get back to initial
    assert unscrambled == initial, \
        f"Failed: {initial} -> {scrambled} -> {unscrambled}"
```

**Expected Results:**
- Should perfectly reconstruct the original password
- Validates the overall inverse logic

#### Test 2.2: All Operation Types Test
```python
def test_all_operation_types():
    """Test a sequence that includes every type of operation"""
    initial = 'abcdefgh'

    operations = [
        'swap position 0 with position 3',
        'swap letter a with letter e',
        'rotate left 2 steps',
        'rotate right 1 step',
        'rotate based on position of letter d',
        'reverse positions 1 through 5',
        'move position 3 to position 6',
    ]

    # Scramble then unscramble
    scrambled = scramble_password(initial, operations)
    unscrambled = unscramble_password(scrambled, operations)

    assert unscrambled == initial
```

**Expected Results:**
- All 6 operation types should work correctly in combination
- Order of operations should be properly reversed

#### Test 2.3: Actual Problem Verification (ULTIMATE TEST)
```python
def test_actual_solution():
    """
    THE ULTIMATE TEST: verify that unscrambling 'fbgdceah'
    and then re-scrambling produces 'fbgdceah'

    NOTE: Part 1 scrambled 'abcdefgh' → 'fdhbcgea' using these operations
          Part 2 must unscramble 'fbgdceah' → ??? (different password)
          Same operations, different starting point - Part 1 answer not needed
    """
    scrambled = 'fbgdceah'
    operations = read_operations('input.md')

    print(f"Loaded {len(operations)} operations from input.md")
    print(f"Target scrambled password: {scrambled}")
    print(f"Note: This is DIFFERENT from Part 1's result 'fdhbcgea'")

    # Unscramble
    original = unscramble_password(scrambled, operations)
    print(f"Unscrambled password: {original}")

    # Verify it's a valid password
    assert len(original) == 8, f"Wrong length: {len(original)}"
    assert sorted(original) == list('abcdefgh'), \
        f"Wrong characters: {sorted(original)}"

    # Re-scramble and verify we get back to scrambled
    re_scrambled = scramble_password(original, operations)
    assert re_scrambled == scrambled, \
        f"Re-scrambling failed: {original} -> {re_scrambled}, expected {scrambled}"

    print(f"✓ Successfully unscrambled: {scrambled} -> {original}")
    print(f"✓ Verified by re-scrambling: {original} -> {re_scrambled}")
    print(f"✓ SOLUTION IS CORRECT!")
```

**Expected Results:**
- Unscrambled password contains all 8 unique letters a-h
- Re-scrambling the result produces exactly 'fbgdceah'
- This is the definitive proof of correctness
- Should print clear success message with the answer

### Level 3: Edge Case Tests

#### Test 3.1: Boundary Positions
```python
def test_boundary_positions():
    """Test operations at string boundaries"""
    test_string = 'abcdefgh'

    # Swap at boundaries
    result = swap_position(test_string, 0, 7)
    assert result[0] == 'h' and result[7] == 'a'

    # Reverse entire string
    result = reverse_positions(test_string, 0, 7)
    assert result == 'hgfedcba'

    # Reverse single character (no-op)
    result = reverse_positions(test_string, 3, 3)
    assert result == test_string

    # Move from boundaries
    result = move_position(test_string, 0, 7)
    assert result == 'bcdefgha'
```

**Expected Results:**
- Operations at string edges should work correctly
- Single-character operations should behave as expected

#### Test 3.2: Rotation Edge Cases
```python
def test_rotation_edge_cases():
    """Test rotation with edge case step counts"""
    test_string = 'abcdefgh'

    # Zero rotation (no-op)
    assert rotate_left(test_string, 0) == test_string
    assert rotate_right(test_string, 0) == test_string

    # Full rotation (back to original)
    assert rotate_left(test_string, 8) == test_string
    assert rotate_right(test_string, 8) == test_string

    # Over-rotation (should use modulo)
    assert rotate_left(test_string, 9) == rotate_left(test_string, 1)
    assert rotate_right(test_string, 10) == rotate_right(test_string, 2)
```

**Expected Results:**
- Zero and full rotations should return original
- Over-rotations should wrap correctly

#### Test 3.3: Character Preservation
```python
def test_character_preservation():
    """Ensure all operations preserve the character set"""
    initial = 'abcdefgh'
    operations = read_operations('input.md')

    # After unscrambling
    result = unscramble_password('fbgdceah', operations)

    # Should have exact same characters
    assert sorted(result) == sorted(initial)
    assert set(result) == set(initial)
    assert len(result) == len(initial)
```

**Expected Results:**
- No characters lost or gained
- All letters a-h present exactly once

### Level 4: Stress Tests

#### Test 4.1: Repeated Scramble/Unscramble Cycles
```python
def test_repeated_cycles():
    """Test that scrambling and unscrambling can be done multiple times"""
    initial = 'abcdefgh'
    operations = read_operations('input.md')

    current = initial

    # Do 5 scramble/unscramble cycles
    for i in range(5):
        scrambled = scramble_password(current, operations)
        unscrambled = unscramble_password(scrambled, operations)
        assert unscrambled == current, f"Failed at cycle {i}"
        current = scrambled
```

**Expected Results:**
- Multiple cycles should work consistently
- No accumulation of errors

#### Test 4.2: Large Rotation Values
```python
def test_large_rotations():
    """Test that modulo arithmetic works for large rotation values"""
    test_string = 'abcdefgh'

    # Very large rotation values
    large_values = [100, 256, 1000]

    for value in large_values:
        forward = rotate_right(test_string, value)
        backward = rotate_left(forward, value)
        assert backward == test_string
```

**Expected Results:**
- Large rotation values should be handled via modulo
- No integer overflow or incorrect results

## Test Execution Order (OPTIMIZED FOR FAIL-FAST)

**Goal: Detect issues as quickly as possible, prioritize critical tests**

1. **Critical unit test FIRST** (Test 1.2 only)
   - Test inverse_rotate_based_on_letter immediately
   - This was identified as the most error-prone operation
   - If this fails, stop and fix before continuing
   - Takes <1 second, catches the most likely bug

2. **Actual solution verification** (Test 2.3) - SECOND
   - Run the real problem immediately after critical unit test
   - If solution works, we're done with must-haves
   - Fail fast: know within seconds if solution is correct
   - Most practical for puzzle-solving context

3. **Other unit tests** (Tests 1.1, 1.3, 1.4) - If time permits
   - Verify other inverse operations
   - Good for thoroughness but less critical
   - These operations are simpler and less error-prone

4. **Integration tests** (Level 2) - Optional
   - More confidence building
   - Good practice but not strictly necessary if Test 2.3 passes

5. **Edge cases** (Level 3) - Optional
   - For completeness
   - Skip if time-constrained

6. **Stress tests** (Level 4) - Skip for puzzle solving
   - Not necessary for this context

**Rationale:**
- We're solving a puzzle, not building production software
- Test 1.2 (rotate inverse) is the highest-risk component
- Test 2.3 (actual solution) is the ultimate validation
- Everything else is optional verification
- This order minimizes time to answer

## Success Criteria

### Must Pass (Non-negotiable):
1. ✓ **Test 1.2**: inverse_rotate_based_on_letter correctly undoes rotate_based_on_letter
2. ✓ **Test 2.3**: Unscrambling 'fbgdceah' produces a valid 8-character password
3. ✓ **Test 2.3**: Re-scrambling the unscrambled password produces 'fbgdceah'
4. ✓ **Test 2.3**: Character set is preserved (letters a-h exactly once)

**If these 4 pass, the solution is CORRECT and ready to submit.**

### Should Pass (Verification):
5. ✓ Other inverse operations (move, rotate left/right, swap, reverse) work correctly
6. ✓ Self-inverse operations return to original when applied twice

### Nice to Have (Optional):
7. ✓ All edge cases handle gracefully
8. ✓ Boundary conditions work correctly
9. ✓ Integration tests with operation sequences
10. ✓ Stress tests demonstrate robustness

## Testing Implementation

```python
def run_minimal_tests():
    """
    Run ONLY the critical tests needed to validate the solution
    Use this for fast puzzle solving
    """
    print("=" * 60)
    print("CRITICAL TEST 1: Inverse Rotate Based on Letter")
    print("=" * 60)
    test_inverse_rotate_based()
    print("✓ CRITICAL TEST 1 PASSED\n")

    print("=" * 60)
    print("CRITICAL TEST 2: Actual Solution Verification")
    print("=" * 60)
    test_actual_solution()
    print("✓ CRITICAL TEST 2 PASSED\n")

    print("=" * 60)
    print("ALL CRITICAL TESTS PASSED - SOLUTION IS CORRECT!")
    print("=" * 60)

def run_all_tests():
    """
    Run complete test suite (more thorough, takes longer)
    Use this if you want extra confidence or are debugging
    """
    print("Running CRITICAL tests first...")
    print("\n1. Testing inverse_rotate_based_on_letter...")
    test_inverse_rotate_based()
    print("✓ Passed\n")

    print("2. Testing actual solution...")
    test_actual_solution()
    print("✓ Passed - SOLUTION IS CORRECT!\n")

    print("Running additional unit tests...")
    test_inverse_move()
    test_rotate_inverses()
    test_self_inverse_operations()
    print("✓ All unit tests passed\n")

    print("Running integration tests...")
    test_simple_sequence()
    test_all_operation_types()
    print("✓ All integration tests passed\n")

    print("Running edge case tests...")
    test_boundary_positions()
    test_rotation_edge_cases()
    test_character_preservation()
    print("✓ All edge case tests passed\n")

    print("=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)

if __name__ == '__main__':
    # For puzzle solving, use minimal tests
    run_minimal_tests()

    # Uncomment below for thorough testing
    # run_all_tests()
```

## Debugging Strategy

If tests fail:

1. **For inverse_rotate_based_on_letter failures (Test 1.2):**
   - **Most likely cause**: Lookup table error (if using lookup approach)
   - **Solution**: Switch to brute force approach (guaranteed correct)
   - Print before/after states for each letter position
   - Manually verify a few cases with pen and paper
   - Check that string length validation is working (must be 8)

2. **For actual solution failure (Test 2.3):**
   - First check: Did Test 1.2 pass? If not, fix that first
   - Verify input file is read correctly (should have 100 operations)
   - Check that 'fbgdceah' is the correct scrambled password
   - Add debug logging to print state after each operation
   - Verify operation parsing is correct
   - Try running forward scramble on some test passwords to verify operations work

3. **For other inverse operation failures:**
   - These are simpler operations, unlikely to fail
   - Print before/after states
   - Verify parameter ordering (especially for move: X→Y vs Y→X)
   - Check modulo arithmetic for rotations

4. **General debugging tips:**
   - Add `print(f"After op {i}: {password}")` in unscramble loop
   - Compare intermediate states with manual calculation
   - Use Python debugger (pdb) to step through operations
   - Test individual operations in isolation

## Expected Final Output

When running the solution:
```
Original unscrambled password: ????????
```

Where `????????` is an 8-character string containing letters a-h that, when scrambled using the 100 operations, produces `fbgdceah`.
