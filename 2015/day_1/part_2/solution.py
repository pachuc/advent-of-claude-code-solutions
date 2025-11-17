def find_basement_position(instructions: str) -> int:
    """
    Find the 1-indexed position where Santa first enters basement (floor -1).

    Args:
        instructions: String of '(' and ')' characters

    Returns:
        1-indexed position of first basement entry, or None if never reached
    """
    current_floor = 0

    for index, char in enumerate(instructions):
        if char == '(':
            current_floor += 1
        elif char == ')':
            current_floor -= 1

        # Check if we've entered the basement
        if current_floor == -1:
            return index + 1  # Convert to 1-indexed

    return None  # Never reached basement


def main():
    # Read input
    with open('input.md', 'r') as f:
        instructions = f.read().strip()

    # Find and print result
    result = find_basement_position(instructions)
    print(result)


if __name__ == "__main__":
    main()
