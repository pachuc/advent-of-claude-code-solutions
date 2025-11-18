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


def find_cycle_count(banks):
    """
    Run redistribution cycles until a repeated configuration is found.
    Returns the number of cycles completed.
    """
    seen = set()
    seen.add(tuple(banks))

    cycle_count = 0

    while True:
        redistribute(banks)
        cycle_count += 1

        config = tuple(banks)
        if config in seen:
            return cycle_count

        seen.add(config)


def main():
    """Main entry point for the solution."""
    with open('input.md', 'r') as f:
        input_data = f.read()

    banks = parse_input(input_data)
    result = find_cycle_count(banks)
    print(result)


if __name__ == "__main__":
    main()
