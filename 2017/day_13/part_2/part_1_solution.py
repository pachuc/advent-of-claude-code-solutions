def parse_input(filename):
    """Parse input file and return list of (depth, range) tuples."""
    layers = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                depth, range_val = line.split(':')
                layers.append((int(depth.strip()), int(range_val.strip())))
    return layers


def is_caught(depth, range_val):
    """
    Determine if packet is caught at given layer.

    Scanner is at position 0 when time % period == 0.
    Period = 2 * (range - 1) for scanner oscillation.

    Edge case: range=1 means scanner never moves (always at position 0).
    """
    # Critical edge case: range=1 means scanner always at position 0
    if range_val == 1:
        return True

    # Calculate period of scanner oscillation
    period = 2 * (range_val - 1)

    # Check if scanner is at position 0 when packet enters at time=depth
    return depth % period == 0


def calculate_severity(layers):
    """Calculate total severity of getting caught by scanners."""
    total_severity = 0

    for depth, range_val in layers:
        if is_caught(depth, range_val):
            severity = depth * range_val
            total_severity += severity

    return total_severity


def main():
    # Parse input
    layers = parse_input('input.md')

    # Calculate severity
    severity = calculate_severity(layers)

    # Output result
    print(severity)


if __name__ == '__main__':
    main()
