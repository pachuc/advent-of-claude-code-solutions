import json


def sum_numbers(data):
    """
    Recursively traverse a JSON-parsed data structure and sum all numbers.

    Args:
        data: Can be int, float, list, dict, str, bool, or None

    Returns:
        int or float: Sum of all numeric values found

    Note:
        - Booleans are excluded (return 0) even though bool is a subclass of int
        - Both integers and floats are summed
        - The order of type checking matters!
    """
    # CRITICAL: Check bool FIRST before checking int, since bool is a subclass of int in Python
    # Without this check, True would be counted as 1 and False as 0
    if isinstance(data, bool):
        return 0

    # If it's a number (int or float), return it
    if isinstance(data, (int, float)):
        return data

    # If it's a list, recursively sum all elements
    if isinstance(data, list):
        return sum(sum_numbers(item) for item in data)

    # If it's a dict, recursively sum all values (ignore keys)
    if isinstance(data, dict):
        return sum(sum_numbers(value) for value in data.values())

    # For strings, None, or any other type, return 0
    return 0


def main():
    # Read input from input.md
    with open('input.md', 'r') as f:
        json_string = f.read().strip()

    # Parse the JSON string
    data = json.loads(json_string)

    # Calculate the sum
    result = sum_numbers(data)

    # Print the result
    print(result)


if __name__ == "__main__":
    main()
