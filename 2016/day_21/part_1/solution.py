def swap_position(s, x, y):
    """Swap characters at positions x and y"""
    lst = list(s)
    lst[x], lst[y] = lst[y], lst[x]
    return ''.join(lst)


def swap_letter(s, x, y):
    """Swap all occurrences of letter x with letter y"""
    lst = list(s)
    for i in range(len(lst)):
        if lst[i] == x:
            lst[i] = y
        elif lst[i] == y:
            lst[i] = x
    return ''.join(lst)


def rotate_left(s, steps):
    """Rotate string left by steps positions"""
    if len(s) == 0:
        return s
    steps = steps % len(s)
    return s[steps:] + s[:steps]


def rotate_right(s, steps):
    """Rotate string right by steps positions"""
    if len(s) == 0:
        return s
    steps = steps % len(s)
    if steps == 0:
        return s
    return s[-steps:] + s[:-steps]


def rotate_based_on_letter(s, letter):
    """Rotate right based on position of letter: 1 + index + (1 if index >= 4 else 0)"""
    index = s.index(letter)
    steps = 1 + index + (1 if index >= 4 else 0)
    return rotate_right(s, steps)


def reverse_positions(s, x, y):
    """Reverse substring from position x to y (inclusive)"""
    lst = list(s)
    lst[x:y+1] = lst[x:y+1][::-1]
    return ''.join(lst)


def move_position(s, x, y):
    """Remove character at position x and insert at position y"""
    lst = list(s)
    char = lst.pop(x)
    lst.insert(y, char)
    return ''.join(lst)


def parse_operation(operation):
    """Parse operation string and return (operation_type, parameters)"""
    parts = operation.split()

    if operation.startswith('swap position'):
        # swap position X with position Y
        x = int(parts[2])
        y = int(parts[5])
        return ('swap_position', (x, y))

    elif operation.startswith('swap letter'):
        # swap letter X with letter Y
        x = parts[2]
        y = parts[5]
        return ('swap_letter', (x, y))

    elif operation.startswith('rotate left'):
        # rotate left X steps
        steps = int(parts[2])
        return ('rotate_left', steps)

    elif operation.startswith('rotate right'):
        # rotate right X steps
        steps = int(parts[2])
        return ('rotate_right', steps)

    elif operation.startswith('rotate based'):
        # rotate based on position of letter X
        letter = parts[6]
        return ('rotate_based', letter)

    elif operation.startswith('reverse positions'):
        # reverse positions X through Y
        x = int(parts[2])
        y = int(parts[4])
        return ('reverse', (x, y))

    elif operation.startswith('move position'):
        # move position X to position Y
        x = int(parts[2])
        y = int(parts[5])
        return ('move', (x, y))

    else:
        raise ValueError(f"Unknown operation: {operation}")


def scramble_password(initial, operations):
    """Apply all operations to the initial password and return the final result"""
    password = initial

    for operation in operations:
        op_type, params = parse_operation(operation)

        if op_type == 'swap_position':
            password = swap_position(password, params[0], params[1])
        elif op_type == 'swap_letter':
            password = swap_letter(password, params[0], params[1])
        elif op_type == 'rotate_left':
            password = rotate_left(password, params)
        elif op_type == 'rotate_right':
            password = rotate_right(password, params)
        elif op_type == 'rotate_based':
            password = rotate_based_on_letter(password, params)
        elif op_type == 'reverse':
            password = reverse_positions(password, params[0], params[1])
        elif op_type == 'move':
            password = move_position(password, params[0], params[1])

    return password


def read_operations(filename):
    """Read operations from input file"""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def test_example():
    """Test with the provided example"""
    password = 'abcde'

    # Step by step from example
    password = swap_position(password, 4, 0)
    assert password == 'ebcda', f"Step 1: Expected 'ebcda', got '{password}'"

    password = swap_letter(password, 'd', 'b')
    assert password == 'edcba', f"Step 2: Expected 'edcba', got '{password}'"

    password = reverse_positions(password, 0, 4)
    assert password == 'abcde', f"Step 3: Expected 'abcde', got '{password}'"

    password = rotate_left(password, 1)
    assert password == 'bcdea', f"Step 4: Expected 'bcdea', got '{password}'"

    password = move_position(password, 1, 4)
    assert password == 'bdeac', f"Step 5: Expected 'bdeac', got '{password}'"

    password = move_position(password, 3, 0)
    assert password == 'abdec', f"Step 6: Expected 'abdec', got '{password}'"

    password = rotate_based_on_letter(password, 'b')
    assert password == 'ecabd', f"Step 7: Expected 'ecabd', got '{password}'"

    password = rotate_based_on_letter(password, 'd')
    assert password == 'decab', f"Step 8: Expected 'decab', got '{password}'"

    print("Example test passed!")
    return True


def test_operations():
    """Unit tests for individual operations"""
    # Test swap_position
    assert swap_position('abcdefgh', 0, 7) == 'hbcdefga'
    assert swap_position('abcdefgh', 3, 3) == 'abcdefgh'

    # Test swap_letter
    assert swap_letter('abcdefgh', 'a', 'h') == 'hbcdefga'
    assert swap_letter('abcdefgh', 'e', 'd') == 'abcedfgh'

    # Test rotate_left
    assert rotate_left('abcdefgh', 0) == 'abcdefgh'
    assert rotate_left('abcdefgh', 1) == 'bcdefgha'
    assert rotate_left('abcdefgh', 8) == 'abcdefgh'

    # Test rotate_right
    assert rotate_right('abcdefgh', 0) == 'abcdefgh'
    assert rotate_right('abcdefgh', 1) == 'habcdefg'
    assert rotate_right('abcd', 1) == 'dabc'

    # Test reverse_positions
    assert reverse_positions('abcdefgh', 0, 7) == 'hgfedcba'
    assert reverse_positions('abcdefgh', 2, 5) == 'abfedcgh'

    # Test move_position
    assert move_position('abcdefgh', 0, 7) == 'bcdefgha'
    assert move_position('abcdefgh', 7, 0) == 'habcdefg'
    assert move_position('bcdea', 1, 4) == 'bdeac'

    print("Unit tests passed!")
    return True


def main():
    # Run tests first
    test_operations()
    test_example()

    # Run actual solution
    initial_password = 'abcdefgh'
    operations = read_operations('input.md')
    final_password = scramble_password(initial_password, operations)

    # Verify character set is preserved
    assert sorted(final_password) == sorted(initial_password), "Character set not preserved!"
    assert len(final_password) == 8, f"Result length is {len(final_password)}, expected 8"

    print(f"Final scrambled password: {final_password}")
    return final_password


if __name__ == '__main__':
    main()
