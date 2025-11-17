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
    shift_amount = shift_amount % width  # Handle shifts larger than width
    # Rotate right: take last N elements and move to front
    screen[row_index] = row[-shift_amount:] + row[:-shift_amount]


def rotate_column(screen, col_index, shift_amount):
    """Rotate a column DOWNWARD with wrapping"""
    height = len(screen)
    # Extract column
    column = [screen[row][col_index] for row in range(height)]
    shift_amount = shift_amount % height  # Handle shifts larger than height
    # Rotate down: take last N elements and move to top
    rotated = column[-shift_amount:] + column[:-shift_amount]
    # Put back into screen
    for row in range(height):
        screen[row][col_index] = rotated[row]


def parse_and_execute_instruction(screen, instruction):
    """Parse an instruction and execute it on the screen"""
    # Define regex patterns
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


def display_screen(screen):
    """Display screen visually with # for ON and . for OFF"""
    for row in screen:
        print(''.join('#' if pixel else '.' for pixel in row))


# Create screen and process instructions
screen = initialize_screen(50, 6)

with open('input.md', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            parse_and_execute_instruction(screen, line)

# Display with column guides
print("Column:  ", end="")
for i in range(0, 50, 5):
    print(f"{i:<5}", end="")
print("\n         " + "|    " * 10)

for row_idx, row in enumerate(screen):
    print(f"Row {row_idx}:   ", end="")
    print(''.join('#' if pixel else '.' for pixel in row))

print("         " + "|    " * 10)

# Count pixels
pixel_count = sum(sum(row) for row in screen)
print(f"\nTotal lit pixels: {pixel_count}")
print(f"Expected from Part 1: 119")
