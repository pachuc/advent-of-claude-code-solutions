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


# Test Edge Case 1: Single disc
print("Test: Single disc")
print("Expected: 3")
with open('test_single.md', 'w') as f:
    f.write("Disc #1 has 7 positions; at time=0, it is at position 3.\n")
discs = parse_input('test_single.md')
result = find_earliest_time(discs)
print(f"Got: {result}")
print(f"Verified: {is_valid_time(result, discs)}")
print()

# Test Edge Case 2: T=0 answer
print("Test: Answer is T=0")
print("Expected: 0")
with open('test_zero.md', 'w') as f:
    f.write("Disc #1 has 3 positions; at time=0, it is at position 2.\n")
    f.write("Disc #2 has 5 positions; at time=0, it is at position 3.\n")
discs = parse_input('test_zero.md')
result = find_earliest_time(discs)
print(f"Got: {result}")
print(f"Verified: {is_valid_time(result, discs)}")
print()

# Test Edge Case 3: All discs start at position 0
print("Test: All discs start at position 0")
print("Expected: 4")
with open('test_zero_start.md', 'w') as f:
    f.write("Disc #1 has 5 positions; at time=0, it is at position 0.\n")
    f.write("Disc #2 has 3 positions; at time=0, it is at position 0.\n")
discs = parse_input('test_zero_start.md')
result = find_earliest_time(discs)
print(f"Got: {result}")
print(f"Verified: {is_valid_time(result, discs)}")
print()

# Manually verify Test 3:
# Disc 1: (0 + T + 1) % 5 == 0 -> T ≡ 4 (mod 5)
# Disc 2: (0 + T + 2) % 3 == 0 -> T ≡ 1 (mod 3)
# T must be 4 mod 5: {4, 9, 14, 19, 24, ...}
# T must be 1 mod 3: {1, 4, 7, 10, 13, 16, 19, ...}
# First match: T = 4
print("Manual verification of Test 3:")
T = 4
print(f"  Disc 1 at time {T+1}: (0 + {T+1}) % 5 = {(0 + T + 1) % 5}")
print(f"  Disc 2 at time {T+2}: (0 + {T+2}) % 3 = {(0 + T + 2) % 3}")
print()

# Test Edge Case 4: From test plan - 3 discs with specific values
print("Test: 3 discs (from test plan)")
print("Expected: 157")
with open('test_three.md', 'w') as f:
    f.write("Disc #1 has 3 positions; at time=0, it is at position 1.\n")
    f.write("Disc #2 has 7 positions; at time=0, it is at position 2.\n")
    f.write("Disc #3 has 11 positions; at time=0, it is at position 5.\n")
discs = parse_input('test_three.md')
result = find_earliest_time(discs)
print(f"Got: {result}")
print(f"Verified: {is_valid_time(result, discs)}")
print()

# Manual verification
print("Manual verification of Test 4:")
T = result
for disc_num, positions, initial in discs:
    arrival_time = T + disc_num
    disc_position = (initial + arrival_time) % positions
    print(f"  Disc {disc_num} at time {arrival_time}: ({initial} + {arrival_time}) % {positions} = {disc_position}")
