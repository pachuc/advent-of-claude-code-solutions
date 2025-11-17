def parse_input(filename):
    """Parse IP ranges from input file"""
    ranges = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    parts = line.split('-')
                    start = int(parts[0])
                    end = int(parts[1])
                    ranges.append((start, end))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []
    return ranges


def merge_ranges(ranges):
    """Sort and merge overlapping/adjacent ranges"""
    if not ranges:
        return []

    # Sort ranges by start value
    sorted_ranges = sorted(ranges)

    # Initialize with first range
    merged = []
    current_start, current_end = sorted_ranges[0]

    # Merge overlapping and adjacent ranges
    for start, end in sorted_ranges[1:]:
        if start <= current_end + 1:
            # Ranges overlap or are adjacent - merge them
            current_end = max(current_end, end)
        else:
            # No overlap - save current range and start new one
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    # Don't forget to add the last range
    merged.append((current_start, current_end))

    return merged


def find_lowest_unblocked(merged_ranges):
    """Find lowest IP not in any range"""
    if not merged_ranges:
        return 0

    candidate = 0

    for start, end in merged_ranges:
        if candidate < start:
            # Found a gap! candidate is not blocked
            return candidate
        else:
            # candidate is blocked, move past this range
            candidate = end + 1

    # If we exit the loop, candidate is beyond all ranges
    return candidate


def main():
    """Main execution"""
    import sys

    # Accept filename as command-line argument, default to input.md
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    ranges = parse_input(filename)
    merged = merge_ranges(ranges)
    result = find_lowest_unblocked(merged)
    print(result)


if __name__ == '__main__':
    main()
