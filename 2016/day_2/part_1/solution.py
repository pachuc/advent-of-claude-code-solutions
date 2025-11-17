def get_button_at_position(row, col):
    """Convert coordinates to button value on the keypad."""
    keypad = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    return keypad[row][col]


def move(current_row, current_col, direction):
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

    # Validate the new position
    if 0 <= new_row <= 2 and 0 <= new_col <= 2:
        return new_row, new_col
    else:
        # Invalid move, stay at current position
        return current_row, current_col


def find_bathroom_code(instructions):
    """
    Process instruction lines and return the bathroom code.

    Args:
        instructions: List of instruction lines (strings of U/D/L/R commands)

    Returns:
        String representing the bathroom code
    """
    # Start at button 5, which is position (1, 1)
    row, col = 1, 1
    code = ""

    for line in instructions:
        # Process each character in the line
        for char in line:
            row, col = move(row, col, char)

        # After processing the line, record the button value
        button = get_button_at_position(row, col)
        code += str(button)

    return code


def main():
    """Read input and calculate the bathroom code."""
    # Read the input file
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse instructions: strip whitespace and skip empty lines
    instructions = [line.strip() for line in lines if line.strip()]

    # Find the bathroom code
    code = find_bathroom_code(instructions)

    # Print the result
    print(code)


if __name__ == "__main__":
    main()
