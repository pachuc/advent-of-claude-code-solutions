def count_garbage_characters(stream: str) -> int:
    """
    Count the total number of non-canceled characters within garbage sections.

    Args:
        stream: The input character stream

    Returns:
        Total count of characters inside garbage (excluding delimiters and canceled chars)
    """
    in_garbage = False
    garbage_count = 0
    i = 0

    while i < len(stream):
        char = stream[i]

        # Handle cancellation character (only inside garbage)
        if in_garbage and char == '!':
            i += 2  # Skip both ! and the next character
            continue

        # Handle garbage start (don't count the <)
        if not in_garbage and char == '<':
            in_garbage = True
            i += 1
            continue

        # Handle garbage end (don't count the >)
        if in_garbage and char == '>':
            in_garbage = False
            i += 1
            continue

        # Count all other characters inside garbage
        if in_garbage:
            garbage_count += 1

        i += 1

    return garbage_count


def read_input(filename: str = 'input.md') -> str:
    """
    Read the input stream from a file.

    Args:
        filename: Path to input file

    Returns:
        The character stream as a string
    """
    with open(filename, 'r') as f:
        return f.read().strip()


def run_tests():
    """Run all test cases and report results."""

    # Test suite from the problem specification
    test_cases = [
        # Basic garbage tests
        ('<>', 0, 'empty garbage'),
        ('<random characters>', 17, 'simple content'),
        ('<<<<>', 3, 'special chars inside'),

        # Cancellation tests
        ('<{!>}>', 2, 'cancel closing bracket'),
        ('<!!>', 0, 'cancel exclamation'),
        ('<!!!>>', 0, 'double cancellation'),
        ('<{o"i!a,<{i<a>', 10, 'complex cancellation'),

        # Multiple garbage sections
        ('{<a>,<a>,<a>,<a>}', 4, 'multiple garbage with groups'),
        ('{{<a>},{<a>},{<a>},{<ab>}}', 5, 'nested-looking groups in garbage'),

        # Edge cases
        ('{{{}}}', 0, 'no garbage'),
        ('<abcdef>', 6, 'only garbage'),
        ('', 0, 'empty string'),
        ('<><>', 0, 'consecutive empty garbage'),
        ('<test>{<data>}', 8, 'garbage at start'),
    ]

    passed = 0
    failed = 0

    print("Running tests...")
    print("=" * 60)

    for input_str, expected, description in test_cases:
        result = count_garbage_characters(input_str)
        if result == expected:
            print(f"✓ PASS - {description}: {result}")
            passed += 1
        else:
            print(f"✗ FAIL - {description}: expected {expected}, got {result}")
            failed += 1

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print()

    return failed == 0


if __name__ == '__main__':
    # Run tests first
    if run_tests():
        print("All tests passed! Running on actual input...\n")

        # Read and process actual input
        stream = read_input('input.md')
        result = count_garbage_characters(stream)

        print(f"Total garbage characters: {result}")
    else:
        print("Tests failed. Please fix the issues before running on actual input.")
