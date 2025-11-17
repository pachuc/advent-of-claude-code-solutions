def parse_input(input_text):
    """
    Parse df output to extract node data.

    Returns:
        List of tuples: [(used, avail), (used, avail), ...]
    """
    nodes = []
    lines = input_text.strip().split('\n')

    # Skip first two header lines
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) >= 4:
            # Extract Used (index 2) and Avail (index 3)
            used = int(parts[2][:-1])  # Remove 'T' suffix
            avail = int(parts[3][:-1])  # Remove 'T' suffix
            nodes.append((used, avail))

    return nodes


def count_viable_pairs(nodes):
    """
    Count viable pairs where A's used data fits in B's available space.

    Args:
        nodes: List of (used, avail) tuples

    Returns:
        int: Count of viable pairs
    """
    count = 0

    for i in range(len(nodes)):
        used_a, avail_a = nodes[i]

        # Skip if node A is empty
        if used_a == 0:
            continue

        for j in range(len(nodes)):
            # Skip if same node
            if i == j:
                continue

            used_b, avail_b = nodes[j]

            # Check if A's data fits in B's available space
            if used_a <= avail_b:
                count += 1

    return count


def main():
    # Read input file
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse nodes
    nodes = parse_input(input_text)

    # Count viable pairs
    result = count_viable_pairs(nodes)

    # Print result
    print(result)


if __name__ == "__main__":
    main()
