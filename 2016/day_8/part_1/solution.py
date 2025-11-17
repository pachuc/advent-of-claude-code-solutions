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


def count_lit_pixels(screen):
    """Count total number of ON pixels"""
    return sum(sum(row) for row in screen)


def display_screen(screen):
    """Display screen visually with # for ON and . for OFF"""
    for row in screen:
        print(''.join('#' if pixel else '.' for pixel in row))


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


def solve(input_file, width=50, height=6):
    """Main solving function"""
    # Initialize screen
    screen = initialize_screen(width, height)

    # Read and process instructions
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                parse_and_execute_instruction(screen, line)

    return screen, count_lit_pixels(screen)


if __name__ == "__main__":
    # Test with the 7x3 example first
    print("Testing with 7x3 example:")
    test_screen = initialize_screen(7, 3)
    instructions = [
        "rect 3x2",
        "rotate column x=1 by 1",
        "rotate row y=0 by 4",
        "rotate column x=1 by 1"
    ]

    for instruction in instructions:
        parse_and_execute_instruction(test_screen, instruction)
        print(f"\nAfter: {instruction}")
        display_screen(test_screen)

    test_count = count_lit_pixels(test_screen)
    print(f"\nTest pixel count: {test_count}")
    print(f"Expected: 6")
    print(f"Test {'PASSED' if test_count == 6 else 'FAILED'}!")

    # Now solve the actual problem
    print("\n" + "="*50)
    print("Solving actual problem:")
    print("="*50 + "\n")

    screen, pixel_count = solve('input.md')

    print("Final screen:")
    display_screen(screen)
    print(f"\nAnswer: {pixel_count}")
