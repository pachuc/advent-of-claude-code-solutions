def parse_input(filename):
    """
    Parse input file to extract replacement rules and medicine molecule.

    Returns:
        tuple: (rules, medicine) where rules is list of (source, replacement) tuples
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    # Find blank line separator dynamically
    blank_index = lines.index('')

    # Parse rules (all lines before blank line)
    rules = []
    for line in lines[:blank_index]:
        if line:  # Skip any empty lines
            source, replacement = line.split(' => ')
            rules.append((source, replacement))

    # Get medicine molecule (line after blank)
    medicine = lines[blank_index + 1]

    return rules, medicine


def find_all_occurrences(text, pattern):
    """
    Find all starting positions where pattern occurs in text (including overlaps).

    Args:
        text: String to search in
        pattern: String pattern to find

    Returns:
        list: List of starting indices where pattern occurs
    """
    positions = []
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i+len(pattern)] == pattern:
            positions.append(i)
    return positions


def solve(input_file):
    """
    Main solution function. Counts distinct molecules from single replacements.

    Args:
        input_file: Path to input file

    Returns:
        int: Count of distinct molecules
    """
    # Parse input
    rules, medicine = parse_input(input_file)

    # Generate all possible molecules
    distinct_molecules = set()

    for source, replacement in rules:
        # Find all occurrences of source pattern
        positions = find_all_occurrences(medicine, source)

        # Generate new molecule for each position
        for pos in positions:
            new_molecule = (
                medicine[:pos] +
                replacement +
                medicine[pos+len(source):]
            )
            distinct_molecules.add(new_molecule)

    return len(distinct_molecules)


if __name__ == "__main__":
    result = solve("input.md")
    print(result)
