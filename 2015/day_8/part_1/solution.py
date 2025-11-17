def read_input(filename='input.md'):
    """Read input file and return list of non-empty lines."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def count_code_chars(line):
    """Count the number of characters in the code representation."""
    return len(line)


def count_memory_chars(line):
    """Count the number of characters in the memory representation.

    Parse escape sequences:
    - double backslash -> single backslash (1 char)
    - backslash quote -> single quote (1 char)
    - backslash x hex hex -> single character from hex code (1 char)
    """
    # Remove surrounding quotes
    content = line[1:-1]

    memory_count = 0
    i = 0

    while i < len(content):
        if content[i] == '\\':
            # Check what follows the backslash
            if i + 1 < len(content):
                next_char = content[i + 1]
                if next_char == '\\' or next_char == '"':
                    # \\ or \" - counts as 1 character
                    memory_count += 1
                    i += 2
                elif next_char == 'x':
                    # \x## - hex escape, counts as 1 character
                    memory_count += 1
                    i += 4  # Skip \x and two hex digits
                else:
                    # Invalid escape (shouldn't happen in valid input)
                    memory_count += 1
                    i += 1
            else:
                # Backslash at end (shouldn't happen in valid input)
                memory_count += 1
                i += 1
        else:
            # Regular character
            memory_count += 1
            i += 1

    return memory_count


def calculate_difference(lines):
    """Calculate the difference between code and memory characters."""
    total_code = 0
    total_memory = 0

    for line in lines:
        code_count = count_code_chars(line)
        memory_count = count_memory_chars(line)

        total_code += code_count
        total_memory += memory_count

    return total_code - total_memory


def main():
    lines = read_input('input.md')
    result = calculate_difference(lines)
    print(result)


if __name__ == '__main__':
    main()
