def parse_input(filename):
    """Parse the input file and return a dictionary of Sue data."""
    sues = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Split on the first colon to separate "Sue N" from compounds
            parts = line.split(':', 1)
            sue_part = parts[0].strip()  # "Sue N"
            compounds_part = parts[1].strip()  # "compound1: value1, compound2: value2, ..."

            # Extract Sue number
            sue_number = int(sue_part.split()[1])

            # Parse compounds
            compounds = {}
            compound_pairs = compounds_part.split(', ')
            for pair in compound_pairs:
                compound_name, value = pair.split(': ')
                compounds[compound_name] = int(value)

            sues[sue_number] = compounds

    return sues


def matches_target(sue_compounds, target, greater_than_compounds, less_than_compounds):
    """
    Check if a Sue's compounds match the target according to Part 2 rules.

    Args:
        sue_compounds: dict of {compound: value} for this Sue
        target: dict of target MFCSAM values
        greater_than_compounds: set of compounds that need > comparison
        less_than_compounds: set of compounds that need < comparison

    Returns:
        bool: True if all of Sue's compounds match, False otherwise
    """
    for compound, value in sue_compounds.items():
        target_value = target[compound]

        if compound in greater_than_compounds:
            # For cats and trees, actual value must be GREATER THAN target
            if not (value > target_value):
                return False
        elif compound in less_than_compounds:
            # For pomeranians and goldfish, actual value must be LESS THAN target
            if not (value < target_value):
                return False
        else:
            # Exact match required for all other compounds
            if value != target_value:
                return False

    return True


def find_matching_sue(sues, target, greater_than_compounds, less_than_compounds):
    """Find the Sue that matches the MFCSAM reading."""
    for sue_number, compounds in sues.items():
        if matches_target(compounds, target, greater_than_compounds, less_than_compounds):
            return sue_number
    return None


def main():
    # Define target MFCSAM values
    target = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }

    # Define which compounds use which comparison rules
    greater_than_compounds = {'cats', 'trees'}
    less_than_compounds = {'pomeranians', 'goldfish'}

    # Parse input
    sues = parse_input('input.md')

    # Find matching Sue
    matching_sue = find_matching_sue(sues, target, greater_than_compounds, less_than_compounds)

    # Output result
    print(matching_sue)


if __name__ == '__main__':
    main()
