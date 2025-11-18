def find_divisible_pair(row):
    """Find the pair of numbers where one evenly divides the other.

    Returns the division result (larger / smaller).
    Problem guarantees exactly one valid pair per row.
    """
    # Nested loop to check all pairs
    for i in range(len(row)):
        for j in range(i + 1, len(row)):
            # Check if row[i] divides by row[j]
            if row[i] % row[j] == 0:
                return row[i] // row[j]
            # Check if row[j] divides by row[i]
            if row[j] % row[i] == 0:
                return row[j] // row[i]

    # Should never reach here per problem guarantees
    raise ValueError(f"No evenly divisible pair found in row: {row}")


def calculate_divisible_sum(filename):
    """Calculate sum of division results from file.

    For each row, find the pair where one evenly divides the other,
    then sum all division results.
    """
    # Parse file (adapted from Part 1)
    rows = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                values = [int(x) for x in line.split()]
                rows.append(values)

    # Calculate sum
    total = 0
    for row in rows:
        total += find_divisible_pair(row)

    return total


if __name__ == "__main__":
    import sys

    # Use command line argument if provided, otherwise default to input.md
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    result = calculate_divisible_sum(filename)
    print(result)
