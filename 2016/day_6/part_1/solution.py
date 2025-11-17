from collections import Counter
import sys


def read_input(filepath):
    """Read and parse input file with error handling."""
    try:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"Error: Input file '{filepath}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{filepath}': {e}")
        sys.exit(1)


def decode_message(lines):
    """Decode message by finding most frequent char at each position."""
    if not lines:
        return ""

    # Validate all lines have the same length
    message_length = len(lines[0])
    for i, line in enumerate(lines):
        if len(line) != message_length:
            raise ValueError(f"Line {i} has length {len(line)}, expected {message_length}")

    decoded = []

    for pos in range(message_length):
        # Get all characters at this position
        chars_at_pos = [line[pos] for line in lines]
        # Find most frequent character
        most_frequent = Counter(chars_at_pos).most_common(1)[0][0]
        decoded.append(most_frequent)

    return ''.join(decoded)


def main():
    lines = read_input('input.md')
    result = decode_message(lines)
    print(result)


if __name__ == '__main__':
    main()
