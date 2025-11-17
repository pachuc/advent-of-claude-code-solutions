# Import all necessary functions from Part 1
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


def inverse_move_position(s, x, y):
    """
    Inverse of 'move position X to position Y'
    Forward: remove char at X, insert at Y
    Reverse: remove char at Y, insert at X

    This is equivalent to: move_position(s, y, x)
    """
    return move_position(s, y, x)


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
            # Complex inverse using brute force
            password = inverse_rotate_based_on_letter(password, params)

        elif op_type == 'reverse':
            # Self-inverse: reverse again
            password = reverse_positions(password, params[0], params[1])

        elif op_type == 'move':
            # Inverse: swap source and destination
            password = inverse_move_position(password, params[0], params[1])

    return password


def test_inverse_operations():
    """Test that each inverse operation actually inverts its forward operation"""
    test_string = 'abcdefgh'

    print("Testing inverse operations...")

    # Test inverse move
    forward = move_position(test_string, 3, 7)
    backward = inverse_move_position(forward, 3, 7)
    assert backward == test_string, "Inverse move failed"
    print("  ✓ Inverse move passed")

    # Test inverse rotate based on letter for all letters
    for letter in test_string:
        forward = rotate_based_on_letter(test_string, letter)
        backward = inverse_rotate_based_on_letter(forward, letter)
        assert backward == test_string, f"Inverse rotate based failed for {letter}"
    print("  ✓ Inverse rotate based passed for all letters")

    # Test rotate left/right inverses
    forward = rotate_left(test_string, 3)
    backward = rotate_right(forward, 3)
    assert backward == test_string, "Rotate left/right inverse failed"
    print("  ✓ Rotate left/right inverses passed")

    print("✓ All inverse operation tests passed!\n")


def test_inverse_rotate_based():
    """
    Test the complex inverse rotation for all possible letter positions
    This is THE MOST CRITICAL test as this operation is the trickiest
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
    print("✓ CRITICAL TEST PASSED\n")


def test_actual_solution():
    """
    THE ULTIMATE TEST: verify that unscrambling 'fbgdceah'
    and then re-scrambling produces 'fbgdceah'
    """
    scrambled = 'fbgdceah'
    operations = read_operations('input.md')

    print(f"Loaded {len(operations)} operations from input.md")
    print(f"Target scrambled password: {scrambled}")

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
    print(f"✓ SOLUTION IS CORRECT!\n")

    return original


def run_minimal_tests():
    """
    Run ONLY the critical tests needed to validate the solution
    Use this for fast puzzle solving
    """
    print("=" * 60)
    print("CRITICAL TEST 1: Inverse Rotate Based on Letter")
    print("=" * 60)
    test_inverse_rotate_based()

    print("=" * 60)
    print("CRITICAL TEST 2: Actual Solution Verification")
    print("=" * 60)
    result = test_actual_solution()

    print("=" * 60)
    print("ALL CRITICAL TESTS PASSED - SOLUTION IS CORRECT!")
    print("=" * 60)

    return result


def main():
    # Note: Part 1 scrambled 'abcdefgh' → 'fdhbcgea' using these operations
    # Part 2 unscrambles a DIFFERENT password 'fbgdceah' using the SAME operations
    # We don't need Part 1's answer - this is a separate problem instance

    # The scrambled password we need to unscramble
    scrambled_password = 'fbgdceah'

    # Read operations from input file (same file as Part 1)
    operations = read_operations('input.md')
    print(f"Read {len(operations)} operations from input file\n")

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
    print(f"✓ Verification passed: {original_password} -> {verification}")
    return original_password


if __name__ == '__main__':
    # Run with minimal testing for quick results
    result = run_minimal_tests()
    print(f"\nFINAL ANSWER: {result}")
