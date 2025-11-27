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


def main():
    """Main execution function."""
    polymer = read_input('input.md')
    result = react_polymer(polymer)
    print(result)


if __name__ == '__main__':
    main()
