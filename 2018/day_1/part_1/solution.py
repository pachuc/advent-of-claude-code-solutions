def solve():
    """
    Calculate the final frequency after applying all frequency changes.
    Returns the final frequency as an integer.
    """
    try:
        # Read input file
        with open('input.md', 'r') as f:
            changes = [int(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: input.md file not found")
        return None

    # Calculate final frequency (starting from 0)
    final_frequency = sum(changes)

    return final_frequency

if __name__ == '__main__':
    result = solve()
    if result is not None:
        print(result)
