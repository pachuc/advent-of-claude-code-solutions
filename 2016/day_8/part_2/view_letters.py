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


def display_screen_with_separators(screen):
    """Display screen with column separators every 5 pixels"""
    for row in screen:
        line = ''
        for i, pixel in enumerate(row):
            if i > 0 and i % 5 == 0:
                line += '|'
            line += '#' if pixel else '.'
        print(line)


def extract_letter(screen, letter_index):
    """Extract a single 5x6 letter from the screen"""
    start_col = letter_index * 5
    end_col = start_col + 5

    letter_pattern = []
    for row in screen:
        row_segment = row[start_col:end_col]
        row_str = ''.join('#' if pixel else '.' for pixel in row_segment)
        letter_pattern.append(row_str)

    return tuple(letter_pattern)


# Build the final screen
screen = initialize_screen(50, 6)
with open('input.md', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            parse_and_execute_instruction(screen, line)

print("Screen with column separators (every 5 pixels):")
display_screen_with_separators(screen)

print("\n\nIndividual letters:")
for i in range(10):
    pattern = extract_letter(screen, i)
    print(f"\nLetter {i}:")
    for row in pattern:
        print(f"  {row}")
