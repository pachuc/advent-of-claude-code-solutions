def calculate_decompressed_length(s):
    """
    Calculate decompressed length without building the output.

    Args:
        s: Compressed string

    Returns:
        Integer length of decompressed string
    """
    total_length = 0
    i = 0
    n = len(s)

    while i < n:
        if s[i].isspace():
            # Skip whitespace - don't count in length
            i += 1
        elif s[i] == '(':
            # Parse marker
            close_idx = s.find(')', i)
            marker_content = s[i+1:close_idx]
            a_str, b_str = marker_content.split('x')
            A, B = int(a_str), int(b_str)

            # Add contribution to total length
            total_length += A * B

            # Skip past marker and the A characters in data section
            i = close_idx + 1 + A
        else:
            # Regular character
            total_length += 1
            i += 1

    return total_length


def main():
    # Read input
    with open('input.md', 'r') as f:
        compressed = f.read().strip()

    # Calculate length
    result = calculate_decompressed_length(compressed)

    # Output result
    print(result)


if __name__ == '__main__':
    main()
