import json


def sum_numbers(data):
    """
    Recursively sum all numbers in a JSON structure.

    Filter rule: Ignore any object (dict) that has ANY property with the value "red".
    Note: "red" in arrays has no effect - only objects are filtered.

    Args:
        data: Parsed JSON data (dict, list, int, float, str, None, or bool)

    Returns:
        float: Sum of all numbers (not filtered out)
    """
    # Case 1: Number (but not boolean, since bool is subclass of int in Python)
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return data

    # Case 2: Dictionary (JSON object)
    elif isinstance(data, dict):
        # Check if any value is exactly the string "red"
        # Only string "red" triggers filtering, not other types
        if "red" in data.values():
            return 0  # Ignore entire object and all its children

        # No "red" found, sum all values recursively
        return sum(sum_numbers(value) for value in data.values())

    # Case 3: List (JSON array)
    elif isinstance(data, list):
        # No filtering for arrays, sum all elements recursively
        return sum(sum_numbers(item) for item in data)

    # Case 4: Other types (string, None, bool)
    else:
        return 0


def main():
    """Main entry point - read input, process, and output result."""
    try:
        # Read input file
        with open('input.md', 'r') as f:
            json_text = f.read().strip()

        # Parse JSON
        data = json.loads(json_text)

        # Calculate sum
        result = sum_numbers(data)

        # Output result (convert to int if it's a whole number)
        output = int(result) if result == int(result) else result
        print(output)

        return output

    except FileNotFoundError:
        print("Error: input.md file not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        return None


if __name__ == "__main__":
    main()
