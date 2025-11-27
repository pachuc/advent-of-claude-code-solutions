def calculate_fuel(mass):
    """Calculate fuel required for a given mass.

    Formula: floor(mass / 3) - 2
    Uses integer division for floor behavior.
    """
    return mass // 3 - 2


def read_masses(filename):
    """Read module masses from input file.

    Args:
        filename: Path to input file with one mass per line

    Returns:
        List of integer masses
    """
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]


def calculate_total_fuel(masses):
    """Calculate total fuel for all masses."""
    return sum(calculate_fuel(mass) for mass in masses)


def main():
    # Read input
    masses = read_masses('input.md')

    # Calculate total fuel
    total_fuel = calculate_total_fuel(masses)

    # Output result
    print(total_fuel)


if __name__ == '__main__':
    main()
