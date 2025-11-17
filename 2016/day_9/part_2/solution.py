def calculate_decompressed_length_recursive(s):
    """
    Recursively calculate decompressed length.

    Markers within data sections are processed recursively.

    Args:
        s: Compressed string (or substring)

    Returns:
        Integer length of decompressed string
    """
    total_length = 0
    i = 0
    n = len(s)

    while i < n:
        if s[i].isspace():
            # Skip whitespace
            i += 1
        elif s[i] == '(':
            # Parse marker (AxB)
            close_idx = s.find(')', i)
            marker_content = s[i+1:close_idx]
            a_str, b_str = marker_content.split('x')
            A, B = int(a_str), int(b_str)

            # Extract the next A characters
            start = close_idx + 1
            substring = s[start:start + A]

            # RECURSIVE CALL: Calculate length of substring
            substring_length = calculate_decompressed_length_recursive(substring)

            # Multiply by B repetitions
            total_length += substring_length * B

            # Skip past marker and A characters
            i = start + A
        else:
            # Regular character
            total_length += 1
            i += 1

    return total_length


def main():
    # Read input
    with open('input.md', 'r') as f:
        compressed = f.read().strip()

    # Calculate length using recursive approach
    result = calculate_decompressed_length_recursive(compressed)

    # Output result
    print(result)


if __name__ == '__main__':
    main()
