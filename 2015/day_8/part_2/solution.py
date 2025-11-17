def calculate_encoded_difference(line):
    """
    Calculate the difference between encoded and original length for a single line.

    Args:
        line: A string literal (including quotes)

    Returns:
        The difference (encoded_length - original_length)
    """
    # Original length is just the length of the line
    original_length = len(line)

    # Encoded length starts with 2 for the outer quotes
    encoded_length = 2

    # Count each character, escaping " and \
    for char in line:
        if char == '"' or char == '\\':
            encoded_length += 2  # Need backslash + character
        else:
            encoded_length += 1  # Regular character

    return encoded_length - original_length


def solve(input_file):
    """
    Calculate total additional characters when encoding string literals.

    Args:
        input_file: Path to input file containing string literals

    Returns:
        Integer representing total difference between encoded and original lengths
    """
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')

    total_difference = 0

    for line in lines:
        if not line:
            continue

        difference = calculate_encoded_difference(line)
        total_difference += difference

    return total_difference


if __name__ == "__main__":
    result = solve('input.md')
    print(result)
