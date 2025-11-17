#!/usr/bin/env python3
"""
Aunt Sue Identification Solution
Identifies which Aunt Sue sent a gift by matching MFCSAM analysis with remembered characteristics.
"""

import sys


def parse_line(line):
    """
    Parse a line to extract Sue ID and characteristics.
    Returns (sue_id, characteristics_dict) or (None, {}) for invalid lines.
    """
    try:
        # Skip empty lines
        if not line.strip() or 'Sue' not in line:
            return None, {}

        # Split on first colon to separate "Sue N" from characteristics
        parts = line.split(':', 1)
        sue_id = int(parts[0].replace('Sue', '').strip())

        # Parse characteristics
        characteristics = {}
        compounds = parts[1].split(',')
        for compound in compounds:
            name, count = compound.split(':')
            characteristics[name.strip()] = int(count.strip())

        return sue_id, characteristics

    except (ValueError, IndexError, AttributeError):
        # Skip malformed lines
        return None, {}


def matches_target(aunt_characteristics, target_signature):
    """
    Check if all remembered characteristics match the target signature.
    Returns True if all match, False otherwise.
    """
    for compound, count in aunt_characteristics.items():
        if target_signature.get(compound) != count:
            return False
    return True


def find_matching_sue(aunts_data, target_signature):
    """
    Find the Sue whose remembered characteristics all match the target.
    Returns Sue ID or None if no match found.
    """
    for sue_id, characteristics in aunts_data.items():
        if matches_target(characteristics, target_signature):
            return sue_id
    return None


def verify_uniqueness(aunts, target):
    """
    Verify exactly one Sue matches the target.
    Returns (matching_sue_id, other_matches_list)
    """
    matches = []
    for sue_id, characteristics in aunts.items():
        if matches_target(characteristics, target):
            matches.append(sue_id)

    if len(matches) == 0:
        print("# WARNING: No Sue matches!", file=sys.stderr)
        return None, []
    elif len(matches) == 1:
        print(f"# SUCCESS: Exactly one Sue matches: {matches[0]}", file=sys.stderr)
        return matches[0], []
    else:
        print(f"# WARNING: Multiple Sues match: {matches}", file=sys.stderr)
        return matches[0], matches[1:]


def validate_data(aunts, target):
    """
    Validate parsed data for integrity and correctness.
    Prints diagnostics and returns True if valid.
    """
    print(f"# Validation Results:", file=sys.stderr)

    # Verify Target Signature Completeness
    expected_compounds = {'children', 'cats', 'samoyeds', 'pomeranians', 'akitas',
                         'vizslas', 'goldfish', 'trees', 'cars', 'perfumes'}
    if set(target.keys()) != expected_compounds:
        print(f"#   ERROR: Target missing compounds: {expected_compounds - set(target.keys())}",
              file=sys.stderr)
        return False
    print(f"#   ✓ Target has all 10 compounds", file=sys.stderr)

    # Verify Input Parsing Completeness
    if len(aunts) != 500:
        print(f"#   WARNING: Expected 500 Sues, got {len(aunts)}", file=sys.stderr)
    else:
        print(f"#   ✓ Parsed exactly 500 Sues", file=sys.stderr)

    # Verify Each Sue Has Exactly 3 Characteristics
    invalid_sues = [sid for sid, chars in aunts.items() if len(chars) != 3]
    if invalid_sues:
        print(f"#   ERROR: Sues with != 3 characteristics: {invalid_sues[:5]}...",
              file=sys.stderr)
        return False
    print(f"#   ✓ All Sues have exactly 3 characteristics", file=sys.stderr)

    # Verify Compound Name Consistency
    all_compounds = set()
    for chars in aunts.values():
        all_compounds.update(chars.keys())
    invalid_compounds = all_compounds - expected_compounds
    if invalid_compounds:
        print(f"#   ERROR: Unknown compounds found: {invalid_compounds}", file=sys.stderr)
        return False
    print(f"#   ✓ All compound names are valid", file=sys.stderr)

    # Verify Value Ranges
    invalid_values = []
    for sue_id, chars in aunts.items():
        for compound, count in chars.items():
            if not isinstance(count, int) or count < 0:
                invalid_values.append((sue_id, compound, count))
    if invalid_values:
        print(f"#   ERROR: Invalid values found: {invalid_values[:5]}...", file=sys.stderr)
        return False
    print(f"#   ✓ All values are non-negative integers", file=sys.stderr)

    return True


def verify_result(sue_id, aunts, target):
    """
    Verify the found Sue matches the target and print diagnostic info.
    Returns True if valid match, False otherwise.
    """
    if sue_id is None:
        print("ERROR: No matching Sue found!", file=sys.stderr)
        return False

    print(f"# Found Sue {sue_id}", file=sys.stderr)
    print("# Verification:", file=sys.stderr)

    characteristics = aunts[sue_id]
    all_match = True

    for compound, count in characteristics.items():
        target_val = target[compound]
        match = count == target_val
        all_match = all_match and match
        status = "✓" if match else "✗"
        print(f"#   {compound}: {count} (target: {target_val}) {status}", file=sys.stderr)

    if all_match:
        print(f"# All characteristics match!", file=sys.stderr)

    return all_match


def main(filename='input.md'):
    # 1. Define target signature
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

    # 2. Read and parse input file
    aunts = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                sue_id, characteristics = parse_line(line)
                if sue_id is not None:  # Skip invalid lines
                    aunts[sue_id] = characteristics
    except FileNotFoundError:
        print("ERROR: input.md not found!", file=sys.stderr)
        sys.exit(1)

    # 3. Validate parsed data
    print(f"# Parsed {len(aunts)} Sues", file=sys.stderr)
    if len(aunts) == 0:
        print("ERROR: No valid Sue data found!", file=sys.stderr)
        sys.exit(1)

    if not validate_data(aunts, target):
        print("ERROR: Data validation failed!", file=sys.stderr)
        sys.exit(1)

    # 4. Find matching Sue and verify uniqueness
    result, other_matches = verify_uniqueness(aunts, target)

    if other_matches:
        print(f"# ERROR: Multiple matches found: {[result] + other_matches}", file=sys.stderr)
        sys.exit(1)

    # 5. Verify and output result
    if verify_result(result, aunts, target):
        print(result)  # Only output to stdout for the answer
    else:
        print("ERROR: Verification failed!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    main(filename)
