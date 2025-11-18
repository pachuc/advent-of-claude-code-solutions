def parse_input(input_string):
    """Parse space-separated integers into a list of bank values."""
    return [int(x) for x in input_string.strip().split()]


def find_max_bank(banks):
    """
    Find the index of the bank with the most blocks.
    If there's a tie, return the lowest index.
    """
    max_value = banks[0]
    max_index = 0

    for i, value in enumerate(banks):
        if value > max_value:
            max_value = value
            max_index = i

    return max_index


def redistribute(banks):
    """
    Perform one redistribution cycle.
    Modifies banks in-place and returns the new configuration.
    """
    # Find the bank with most blocks
    max_idx = find_max_bank(banks)

    # Get the number of blocks to redistribute
    blocks_to_distribute = banks[max_idx]

    # Set that bank to 0
    banks[max_idx] = 0

    # Distribute blocks one at a time starting from next bank
    for i in range(blocks_to_distribute):
        current_idx = (max_idx + 1 + i) % len(banks)
        banks[current_idx] += 1

    return banks


def find_loop_size(banks):
    """
    Run redistribution cycles until a repeated configuration is found.
    Returns the size of the loop (cycles between first and second occurrence).

    Note: The initial state (before any redistributions) is considered cycle 0.
    The loop size is the number of cycles between the first and second
    occurrence of the repeated configuration.
    """
    seen_at = {}  # Maps configuration tuple to cycle number when first seen
    seen_at[tuple(banks)] = 0  # Initial state is at cycle 0

    cycle_count = 0

    while True:
        redistribute(banks)
        cycle_count += 1

        config = tuple(banks)
        if config in seen_at:
            # Found a repeat - calculate loop size
            loop_size = cycle_count - seen_at[config]
            return loop_size

        seen_at[config] = cycle_count


def main():
    """Main entry point for the solution."""
    with open('input.md', 'r') as f:
        input_data = f.read()

    banks = parse_input(input_data)
    result = find_loop_size(banks)
    print(result)


if __name__ == "__main__":
    main()
