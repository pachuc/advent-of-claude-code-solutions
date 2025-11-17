def has_abba(sequence):
    """
    Check if a sequence contains an ABBA pattern.
    An ABBA is a 4-character palindrome with two different characters.
    Example: 'abba', 'xyyx', 'oxxo' are valid ABBAs
    'aaaa' is NOT valid (must have 2 different characters)
    """
    if len(sequence) < 4:
        return False

    # Sliding window of size 4
    for i in range(len(sequence) - 3):
        window = sequence[i:i+4]
        # Check if it's a palindrome with different chars
        if (window[0] == window[3] and
            window[1] == window[2] and
            window[0] != window[1]):
            return True

    return False


def parse_address(address):
    """
    Parse an IPv7 address into supernet and hypernet sequences.
    Returns: (supernet_sequences, hypernet_sequences)

    Supernet sequences are outside brackets.
    Hypernet sequences are inside brackets [].
    """
    supernets = []
    hypernets = []
    current_sequence = ""
    inside_brackets = False

    for char in address:
        if char == '[':
            # Save current supernet sequence if non-empty
            if current_sequence:
                supernets.append(current_sequence)
            current_sequence = ""
            inside_brackets = True
        elif char == ']':
            # Save current hypernet sequence if non-empty
            if current_sequence:
                hypernets.append(current_sequence)
            current_sequence = ""
            inside_brackets = False
        else:
            current_sequence += char

    # Don't forget the last sequence if it exists
    if current_sequence:
        if inside_brackets:
            hypernets.append(current_sequence)
        else:
            supernets.append(current_sequence)

    return supernets, hypernets


def supports_tls(address):
    """
    Check if an IPv7 address supports TLS.

    TLS is supported if:
    1. At least one ABBA exists in supernet sequences (outside brackets)
    2. No ABBA exists in hypernet sequences (inside brackets)
    """
    supernets, hypernets = parse_address(address)

    # Check hypernets first (fail fast)
    for hypernet in hypernets:
        if has_abba(hypernet):
            return False

    # Check supernets
    for supernet in supernets:
        if has_abba(supernet):
            return True

    return False


def main():
    """
    Main function to process input and count TLS-supporting addresses.
    """
    count = 0

    with open('input.md', 'r') as f:
        for line in f:
            address = line.strip()
            if address and supports_tls(address):
                count += 1

    print(count)


if __name__ == "__main__":
    main()
