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


def count_allowed_ips(merged_ranges):
    """Count total allowed IPs in the 32-bit address space"""
    TOTAL_IP_SPACE = 2**32  # 4,294,967,296

    # Calculate total blocked IPs
    blocked_count = 0
    for start, end in merged_ranges:
        blocked_count += (end - start + 1)

    # Allowed IPs = Total - Blocked
    allowed_count = TOTAL_IP_SPACE - blocked_count

    # Verification assertion to catch arithmetic errors
    assert blocked_count + allowed_count == TOTAL_IP_SPACE, "Count mismatch!"

    return allowed_count


def main():
    """Main execution"""
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    debug = '--debug' in sys.argv

    ranges = parse_input(filename)
    merged = merge_ranges(ranges)

    # Optional debug output
    if debug:
        print(f"Parsed {len(ranges)} ranges")
        print(f"Merged to {len(merged)} ranges")
        if merged:
            print(f"First merged range: {merged[0]}")
            print(f"Last merged range: {merged[-1]}")
            # Calculate blocked count for debug
            blocked_count = sum(end - start + 1 for start, end in merged)
            print(f"Total blocked IPs: {blocked_count}")
            print(f"Total IP space: {2**32}")

    result = count_allowed_ips(merged)
    print(result)


if __name__ == '__main__':
    main()
