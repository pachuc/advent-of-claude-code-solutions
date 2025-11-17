import re


def parse_input(input_text):
    """
    Extract row and column from input text.

    Input format: "Enter the code at row [ROW], column [COLUMN]."

    Returns: (row, column) as integers
    """
    pattern = r'row (\d+), column (\d+)'
    match = re.search(pattern, input_text)
    if match:
        row = int(match.group(1))
        col = int(match.group(2))
        return row, col
    raise ValueError(f"Could not parse input: {input_text}")


def calculate_position(row, col):
    """
    Calculate the sequential position in the generation order
    for a given (row, col) coordinate.

    Formula: position = (row + col - 1) * (row + col - 2) // 2 + col

    Args:
        row: 1-indexed row number
        col: 1-indexed column number

    Returns: Sequential position (1-indexed)

    Example:
        calculate_position(1, 1) -> 1
        calculate_position(2978, 3083) -> 18361853
    """
    diagonal = row + col - 1
    # Last position of previous diagonal
    prev_diagonal_end = (diagonal - 1) * diagonal // 2
    # Position within current diagonal (column number)
    position_in_diagonal = col
    # Total position
    return prev_diagonal_end + position_in_diagonal


def generate_code(position):
    """
    Generate the code at the given sequential position.

    Starting code: 20151125
    Formula: next = (prev * 252533) % 33554393

    Args:
        position: Sequential position (1-indexed)

    Returns: The code at that position
    """
    code = 20151125
    for i in range(1, position):
        code = (code * 252533) % 33554393
    return code


def solve(input_text):
    """
    Main solution function that ties everything together.

    Args:
        input_text: Raw input string with row and column

    Returns: The code at the specified position
    """
    row, col = parse_input(input_text)
    position = calculate_position(row, col)
    code = generate_code(position)
    return code


if __name__ == "__main__":
    # Read input from file
    with open('input.md', 'r') as f:
        input_text = f.read().strip()

    # Solve and print result
    result = solve(input_text)
    print(result)
