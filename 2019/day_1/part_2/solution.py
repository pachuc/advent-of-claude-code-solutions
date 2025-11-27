def calculate_fuel(mass):
    """Calculate fuel required for a given mass.

    Formula: floor(mass / 3) - 2
    Uses integer division for floor behavior.
    """
    return mass // 3 - 2


def calculate_recursive_fuel(mass):
    """Calculate total fuel for a module including fuel for the fuel.

    For a given module mass, repeatedly calculate fuel needed and add it
    to the total. The fuel itself has mass, so we calculate fuel for the
    fuel, and so on until the calculated fuel is zero or negative.

    Args:
        mass: The module mass (non-negative integer)

    Returns:
        Total fuel needed including recursive fuel requirements (always >= 0)
    """
    total_fuel = 0
    fuel = calculate_fuel(mass)

    while fuel > 0:
        total_fuel += fuel
        fuel = calculate_fuel(fuel)

    return total_fuel


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
    """Calculate total fuel for all masses including recursive fuel."""
    return sum(calculate_recursive_fuel(mass) for mass in masses)


def main():
    # Read input
    masses = read_masses('input.md')

    # Calculate total fuel
    total_fuel = calculate_total_fuel(masses)

    # Output result
    print(total_fuel)


if __name__ == '__main__':
    main()
