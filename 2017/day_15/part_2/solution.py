def parse_input(filename):
    """
    Parse input file to extract starting values for generators A and B.

    Args:
        filename: Path to input file

    Returns:
        Tuple of (start_a, start_b)
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Extract numbers from lines like "Generator A starts with 277"
    start_a = int(lines[0].split()[-1])
    start_b = int(lines[1].split()[-1])

    return start_a, start_b


def generate_values_filtered(start, factor, modulo, filter_divisor):
    """
    Generator function that yields filtered sequence of pseudo-random values.
    Only yields values that are divisible by filter_divisor.

    Args:
        start: Initial value
        factor: Multiplication factor (16807 for A, 48271 for B)
        modulo: Modulo value (2147483647)
        filter_divisor: Only yield values divisible by this (4 for A, 8 for B)

    Yields:
        Next value in sequence that passes the filter
    """
    current = start
    while True:
        current = (current * factor) % modulo
        if current % filter_divisor == 0:
            yield current


def count_matches(start_a, start_b, pairs=5_000_000):
    """
    Count how many pairs match in their lowest 16 bits.

    Args:
        start_a: Starting value for generator A
        start_b: Starting value for generator B
        pairs: Number of pairs to generate (default 5 million)

    Returns:
        Count of matching pairs
    """
    FACTOR_A = 16807
    FACTOR_B = 48271
    MODULO = 2147483647
    MASK_16_BIT = 0xFFFF
    FILTER_A = 4  # Generator A keeps multiples of 4
    FILTER_B = 8  # Generator B keeps multiples of 8

    gen_a = generate_values_filtered(start_a, FACTOR_A, MODULO, FILTER_A)
    gen_b = generate_values_filtered(start_b, FACTOR_B, MODULO, FILTER_B)

    count = 0
    for _ in range(pairs):
        value_a = next(gen_a)
        value_b = next(gen_b)
        if (value_a & MASK_16_BIT) == (value_b & MASK_16_BIT):
            count += 1

    return count


def main():
    """
    Main entry point for the solution.
    """
    # Read input from input.txt
    start_a, start_b = parse_input('input.txt')

    # Count matches
    result = count_matches(start_a, start_b, 5_000_000)

    # Print result
    print(result)


if __name__ == "__main__":
    main()
