import re
from math import gcd, lcm


def parse_input(filename):
    """Parse disc information from input file"""
    pattern = r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)\.'
    discs = []

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            match = re.match(pattern, line)
            if match:
                disc_num = int(match.group(1))
                positions = int(match.group(2))
                initial = int(match.group(3))
                discs.append((disc_num, positions, initial))

    # Validate disc numbers are sequential starting from 1
    for i, (disc_num, _, _) in enumerate(discs):
        if disc_num != i + 1:
            raise ValueError(f"Disc numbers must be sequential starting from 1")

    return discs


def find_earliest_time(discs):
    """Find earliest time to press button using optimized search"""
    time = 0
    step = 1

    for disc_num, positions, initial in discs:
        # Find next time that works for this disc
        while (initial + time + disc_num) % positions != 0:
            time += step

        # Update step to maintain all previous constraints
        step = lcm(step, positions)

    return time


def is_valid_time(T, discs):
    """Check if time T works for all discs (for verification)"""
    for disc_num, positions, initial in discs:
        capsule_arrival_time = T + disc_num
        disc_position = (initial + capsule_arrival_time) % positions
        if disc_position != 0:
            return False
    return True


def main():
    """Main execution"""
    # Parse input
    discs = parse_input('input.md')

    # Add the 7th disc: disc_num=7, positions=11, initial=0
    discs.append((7, 11, 0))

    # Print parsed disc information for verification
    print("Parsed discs:")
    for disc_num, positions, initial in discs:
        print(f"  Disc #{disc_num}: {positions} positions, initial position {initial}")
    print()

    # Find solution
    result = find_earliest_time(discs)

    # Verify solution
    print(f"Solution: {result}")
    print()

    # Verify the solution is correct
    if is_valid_time(result, discs):
        print("✓ Solution verified: All discs align correctly")
    else:
        print("✗ Solution verification failed!")

    # Check minimality (T-1 should fail)
    if result > 0 and is_valid_time(result - 1, discs):
        print("✗ Warning: T-1 also works, solution may not be minimal")
    else:
        print("✓ Solution is minimal (T-1 does not work)")

    print()
    print(f"Answer: {result}")


if __name__ == '__main__':
    main()
