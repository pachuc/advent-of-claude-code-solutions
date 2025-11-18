def calculate_checksum(filename):
    """Calculate spreadsheet checksum from file.

    For each row, calculate the difference between max and min values,
    then sum all differences to get the checksum.
    """
    rows = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                values = [int(x) for x in line.split()]
                rows.append(values)

    checksum = 0
    for row in rows:
        max_val = max(row)
        min_val = min(row)
        checksum += (max_val - min_val)

    return checksum


if __name__ == "__main__":
    import sys

    # Use command line argument if provided, otherwise default to input.md
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    result = calculate_checksum(filename)
    print(result)
