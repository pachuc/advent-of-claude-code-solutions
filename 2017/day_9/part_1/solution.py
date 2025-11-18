def calculate_stream_score(stream: str) -> int:
    """
    Calculate the total score for all groups in a character stream.

    Args:
        stream: The input character stream

    Returns:
        Total score of all groups
    """
    in_garbage = False
    depth = 0
    total_score = 0
    i = 0

    while i < len(stream):
        char = stream[i]

        # Handle cancellation character (only inside garbage)
        if in_garbage and char == '!':
            i += 2  # Skip the next character
            continue

        # Handle garbage start
        if not in_garbage and char == '<':
            in_garbage = True
            i += 1
            continue

        # Handle garbage end
        if in_garbage and char == '>':
            in_garbage = False
            i += 1
            continue

        # Handle group start (only outside garbage)
        if not in_garbage and char == '{':
            depth += 1
            total_score += depth
            i += 1
            continue

        # Handle group end (only outside garbage)
        if not in_garbage and char == '}':
            depth -= 1
            i += 1
            continue

        # All other characters are ignored
        i += 1

    return total_score


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

    # Test suite from the problem statement
    test_cases = [
        # Basic tests
        ('{}', 1, 'single group'),
        ('{{{}}}', 6, 'nested groups'),
        ('{{},{}}', 5, 'sibling groups'),
        ('{{{},{},{{}}}}', 16, 'complex nesting'),

        # Garbage tests
        ('{<a>,<a>,<a>,<a>}', 1, 'multiple garbage'),
        ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9, 'garbage in nested groups'),
        ('{<{},{},{{}}>}', 1, 'garbage with group chars'),

        # Cancellation tests
        ('{<{!>}>}', 1, 'canceled >'),
        ('{<!!>}', 1, 'canceled !'),
        ('{<!!!>>}', 1, 'double canceled'),
        ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9, 'multiple !!'),
        ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3, 'multiple canceled >'),

        # Edge cases
        ('', 0, 'empty string'),
        ('<>', 0, 'only garbage'),
    ]

    passed = 0
    failed = 0

    print("Running tests...")
    print("=" * 60)

    for input_str, expected, description in test_cases:
        result = calculate_stream_score(input_str)
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
        result = calculate_stream_score(stream)

        print(f"Total score: {result}")
    else:
        print("Tests failed. Please fix the issues before running on actual input.")
