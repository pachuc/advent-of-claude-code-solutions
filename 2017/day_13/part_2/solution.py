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


def is_caught(depth, range_val, delay):
    """
    Determine if packet is caught at given layer with a specific delay.

    Args:
        depth: Layer depth (0-indexed position)
        range_val: Height of the layer (scanner range)
        delay: Number of picoseconds to wait before starting

    Returns:
        True if caught, False if safe
    """
    # Edge case: range=1 means scanner always at position 0
    if range_val == 1:
        return True  # Always caught regardless of delay

    # Calculate period of scanner oscillation
    period = 2 * (range_val - 1)

    # Packet enters this layer at time = delay + depth
    # Scanner is at position 0 if (delay + depth) % period == 0
    time_at_layer = delay + depth
    return time_at_layer % period == 0


def find_minimum_delay(layers):
    """
    Find the minimum delay needed to pass through firewall without being caught.

    Args:
        layers: List of (depth, range) tuples

    Returns:
        Integer representing minimum delay in picoseconds
    """
    delay = 0

    while True:
        # Check if this delay allows safe passage through all layers
        caught = False

        for depth, range_val in layers:
            if is_caught(depth, range_val, delay):
                caught = True
                break  # Early termination: skip to next delay

        if not caught:
            # Found a safe delay!
            return delay

        delay += 1

        # Progress monitoring for long-running searches
        if delay % 10000 == 0:
            print(f"Checking delay {delay}...")


def verify_delay(layers, delay):
    """
    Verify if a delay allows safe passage through all layers.

    Args:
        layers: List of (depth, range) tuples
        delay: Delay to verify

    Returns:
        True if delay allows safe passage, False otherwise
    """
    for depth, range_val in layers:
        if is_caught(depth, range_val, delay):
            return False
    return True


def main():
    # Parse input
    layers = parse_input('input.md')

    # Find minimum delay
    min_delay = find_minimum_delay(layers)

    # Output result
    print(min_delay)


if __name__ == '__main__':
    main()
