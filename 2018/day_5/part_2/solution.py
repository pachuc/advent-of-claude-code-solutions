def reacts(a, b):
    """
    Check if two characters react with each other.

    Args:
        a: First character
        b: Second character

    Returns:
        True if characters react (same letter, opposite polarity), False otherwise
    """
    return a != b and a.lower() == b.lower()


def react_polymer(polymer, return_polymer=False):
    """
    Simulate polymer reactions until stable.

    Args:
        polymer: String representing the polymer
        return_polymer: If True, return (length, final_polymer_string), else just length

    Returns:
        Integer representing the length of the final polymer, or
        Tuple of (length, final_polymer_string) if return_polymer=True
    """
    stack = []

    for unit in polymer:
        if stack and reacts(stack[-1], unit):
            stack.pop()
        else:
            stack.append(unit)

    if return_polymer:
        return len(stack), ''.join(stack)
    return len(stack)


def read_input(filename='input.md'):
    """
    Read polymer string from input file.

    Handles markdown files by reading all content and stripping whitespace.
    Filters to only alphabetic characters to handle any formatting.

    Args:
        filename: Path to input file

    Returns:
        String containing the polymer (only alphabetic characters)
    """
    with open(filename, 'r') as f:
        content = f.read()
    # Remove all whitespace and non-alphabetic characters
    # This handles markdown formatting, newlines, etc.
    polymer = ''.join(c for c in content if c.isalpha())
    return polymer


def remove_unit_and_react(polymer, unit_to_remove):
    """
    Remove all instances of a unit type and react the polymer.

    Args:
        polymer: String representing the polymer
        unit_to_remove: Lowercase letter representing the unit type to remove

    Returns:
        Integer representing the length of the reacted polymer
    """
    # Filter out the unit type (both uppercase and lowercase)
    filtered_polymer = ''.join(
        c for c in polymer
        if c.lower() != unit_to_remove
    )

    # React the filtered polymer
    return react_polymer(filtered_polymer)


def find_shortest_polymer(polymer):
    """
    Find the shortest polymer by removing one unit type optimally.

    Args:
        polymer: String representing the polymer

    Returns:
        Integer representing the minimum achievable polymer length
    """
    # Handle edge case of empty polymer
    if not polymer:
        return 0

    # Test all 26 possible unit types
    return min(
        remove_unit_and_react(polymer, unit)
        for unit in 'abcdefghijklmnopqrstuvwxyz'
    )


def main():
    """Main execution function."""
    # Read the polymer from input
    polymer = read_input('input.md')

    # Find the shortest polymer achievable
    result = find_shortest_polymer(polymer)

    # Print the result
    print(result)


if __name__ == '__main__':
    main()
