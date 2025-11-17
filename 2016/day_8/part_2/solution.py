import re


def initialize_screen(width, height):
    """Initialize a screen with all pixels OFF (False)"""
    return [[False for _ in range(width)] for _ in range(height)]


def rect(screen, width, height):
    """Turn on pixels in a rectangle at top-left corner"""
    for row in range(height):
        for col in range(width):
            screen[row][col] = True


def rotate_row(screen, row_index, shift_amount):
    """Rotate a row to the RIGHT with wrapping"""
    row = screen[row_index]
    width = len(row)
    shift_amount = shift_amount % width
    screen[row_index] = row[-shift_amount:] + row[:-shift_amount]


def rotate_column(screen, col_index, shift_amount):
    """Rotate a column DOWNWARD with wrapping"""
    height = len(screen)
    column = [screen[row][col_index] for row in range(height)]
    shift_amount = shift_amount % height
    rotated = column[-shift_amount:] + column[:-shift_amount]
    for row in range(height):
        screen[row][col_index] = rotated[row]


def count_lit_pixels(screen):
    """Count total number of ON pixels"""
    return sum(sum(row) for row in screen)


def display_screen(screen):
    """Display screen visually with # for ON and . for OFF"""
    for row in screen:
        print(''.join('#' if pixel else '.' for pixel in row))


def parse_and_execute_instruction(screen, instruction):
    """Parse an instruction and execute it on the screen"""
    rect_pattern = re.compile(r"rect (\d+)x(\d+)")
    row_pattern = re.compile(r"rotate row y=(\d+) by (\d+)")
    col_pattern = re.compile(r"rotate column x=(\d+) by (\d+)")

    instruction = instruction.strip()

    if match := rect_pattern.match(instruction):
        width, height = int(match.group(1)), int(match.group(2))
        rect(screen, width, height)
    elif match := row_pattern.match(instruction):
        row_idx, shift = int(match.group(1)), int(match.group(2))
        rotate_row(screen, row_idx, shift)
    elif match := col_pattern.match(instruction):
        col_idx, shift = int(match.group(1)), int(match.group(2))
        rotate_column(screen, col_idx, shift)


def get_letter_patterns():
    """
    Returns a dictionary mapping 5x6 pixel patterns to letters.
    Each pattern is a tuple of 6 strings (rows), 5 chars wide each.
    '#' = lit pixel, '.' = unlit pixel
    """
    patterns = {}

    patterns['Z'] = (
        '####.',
        '...#.',
        '..#..',
        '.#...',
        '#....',
        '####.'
    )

    patterns['F'] = (
        '####.',
        '#....',
        '###..',
        '#....',
        '#....',
        '#....'
    )

    patterns['H'] = (
        '#..#.',
        '#..#.',
        '####.',
        '#..#.',
        '#..#.',
        '#..#.'
    )

    patterns['E'] = (
        '####.',
        '#....',
        '###..',
        '#....',
        '#....',
        '####.'
    )

    patterns['C'] = (
        '.###.',
        '#....',
        '#....',
        '#....',
        '#....',
        '.###.'
    )

    patterns['S'] = (
        '.###.',
        '#....',
        '#....',
        '.##..',
        '...#.',
        '###..'
    )

    patterns['O'] = (
        '.##..',
        '#..#.',
        '#..#.',
        '#..#.',
        '#..#.',
        '.##..'
    )

    patterns['G'] = (
        '.##..',
        '#..#.',
        '#....',
        '#.##.',
        '#..#.',
        '.###.'
    )

    patterns['P'] = (
        '###..',
        '#..#.',
        '#..#.',
        '###..',
        '#....',
        '#....'
    )

    return patterns


def extract_letter(screen, letter_index):
    """
    Extract a single 5x6 letter from the screen.

    Args:
        screen: 6×50 pixel array
        letter_index: Which letter to extract (0-9)

    Returns:
        Tuple of 6 strings representing the 5×6 letter pattern
    """
    start_col = letter_index * 5
    end_col = start_col + 5

    letter_pattern = []
    for row in screen:
        row_segment = row[start_col:end_col]
        row_str = ''.join('#' if pixel else '.' for pixel in row_segment)
        letter_pattern.append(row_str)

    return tuple(letter_pattern)


def recognize_letter(pattern, letter_patterns):
    """
    Match a 5x6 pattern to a known letter.

    Args:
        pattern: Tuple of 6 strings (5 chars each)
        letter_patterns: Dictionary mapping patterns to letters

    Returns:
        The recognized letter, or '?' if not found
    """
    for letter, known_pattern in letter_patterns.items():
        if pattern == known_pattern:
            return letter

    return '?'


def decode_screen(screen):
    """
    Decode the entire 50x6 screen into letters.

    Args:
        screen: 6×50 pixel array

    Returns:
        String containing the decoded message
    """
    letter_patterns = get_letter_patterns()
    message = []

    # Screen can hold 10 letters (50 / 5 = 10)
    for i in range(10):
        pattern = extract_letter(screen, i)

        # Check if the pattern is blank (all dots)
        if all(c == '.' for row in pattern for c in row):
            continue  # Skip blank sections

        # Try to recognize the pattern
        letter = recognize_letter(pattern, letter_patterns)

        if letter == '?':
            print(f"WARNING: Unrecognized pattern at position {i}:")
            for row in pattern:
                print(f"  {row}")
            message.append(letter)
        else:
            message.append(letter)

    return ''.join(message)


def solve_part2(input_file):
    """
    Main solving function for Part 2.

    Args:
        input_file: Path to instruction file

    Returns:
        The decoded message (string of capital letters)
    """
    # Initialize screen and process instructions (reuse Part 1 logic)
    screen = initialize_screen(50, 6)

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parse_and_execute_instruction(screen, line)

    # Display for debugging
    print("Final screen state:")
    display_screen(screen)
    print()

    # Verify Part 1 answer still matches
    pixel_count = count_lit_pixels(screen)
    print(f"Pixel count: {pixel_count} (Part 1 answer: 119)")
    if pixel_count != 119:
        print("WARNING: Pixel count differs from Part 1 answer!")
    print()

    # Decode the message
    message = decode_screen(screen)

    # Validate output
    print(f"Decoded {len(message)} letters from screen")

    if '?' in message:
        print(f"WARNING: Unrecognized patterns found in message: '{message}'")

    return message


if __name__ == "__main__":
    answer = solve_part2('input.md')
    print(f"Part 2 Answer: {answer}")
