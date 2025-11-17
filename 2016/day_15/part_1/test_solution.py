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


# Test with simple example
print("Test 1: Simple example from test plan")
print("Expected: 5")
discs = parse_input('test_input.md')
result = find_earliest_time(discs)
print(f"Got: {result}")
print(f"Verified: {is_valid_time(result, discs)}")
print()
