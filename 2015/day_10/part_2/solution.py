import itertools


def look_and_say(s):
    """Apply one iteration of look-and-say transformation.

    Args:
        s: A string of digits

    Returns:
        The transformed string
    """
    result = []
    for digit, group in itertools.groupby(s):
        count = sum(1 for _ in group)
        result.append(str(count) + digit)
    return ''.join(result)


def main():
    # Read input from file
    with open('input.md', 'r') as f:
        current = f.read().strip()

    # Validate input
    if not current or not current.isdigit():
        print("Error: Input must be non-empty and contain only digits")
        return

    print(f"Starting with: {current}")
    print(f"Initial length: {len(current)}")
    print()

    # Apply transformation 50 times
    for i in range(1, 51):
        current = look_and_say(current)
        if i % 10 == 0:
            print(f"Iteration {i}: length = {len(current)}")

    # Print final result
    print()
    print(f"Final length after 50 iterations: {len(current)}")
    print(len(current))


if __name__ == "__main__":
    main()
