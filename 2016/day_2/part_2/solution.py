def get_button_at_position(row, col, keypad):
    """Return button value at coordinates."""
    return keypad[(row, col)]


def move(current_row, current_col, direction, keypad):
    """
    Move from current position in the given direction.
    Returns new position if valid, otherwise returns current position.
    """
    new_row, new_col = current_row, current_col

    if direction == 'U':
        new_row -= 1
    elif direction == 'D':
        new_row += 1
    elif direction == 'L':
        new_col -= 1
    elif direction == 'R':
        new_col += 1

    # Check if the new position exists in the diamond keypad
    if (new_row, new_col) in keypad:
        return new_row, new_col
    else:
        # Invalid move, stay at current position
        return current_row, current_col


def find_bathroom_code(instructions, keypad):
    """
    Process instruction lines and return the bathroom code.

    Args:
        instructions: List of instruction lines (strings of U/D/L/R commands)
        keypad: Dictionary mapping (row, col) to button values

    Returns:
        String representing the bathroom code
    """
    # Start at button 5, which is position (2, 0) in the diamond layout
    row, col = 2, 0
    code = ""

    for line in instructions:
        # Process each character in the line
        for char in line:
            row, col = move(row, col, char, keypad)

        # After processing the line, record the button value
        button = get_button_at_position(row, col, keypad)
        code += button

    return code


def main():
    """Read input and calculate the bathroom code."""
    # Define the diamond-shaped keypad
    #     1
    #   2 3 4
    # 5 6 7 8 9
    #   A B C
    #     D
    keypad = {
        (0, 2): '1',
        (1, 1): '2', (1, 2): '3', (1, 3): '4',
        (2, 0): '5', (2, 1): '6', (2, 2): '7', (2, 3): '8', (2, 4): '9',
        (3, 1): 'A', (3, 2): 'B', (3, 3): 'C',
        (4, 2): 'D'
    }

    # Read the input file
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse instructions: strip whitespace and skip empty lines
    instructions = [line.strip() for line in lines if line.strip()]

    # Find the bathroom code
    code = find_bathroom_code(instructions, keypad)

    # Print the result
    print(code)


if __name__ == "__main__":
    main()
