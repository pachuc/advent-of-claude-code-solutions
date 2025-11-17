import re
import sys


def parse_input(filename):
    """
    Parse input file and extract reindeer data.

    Args:
        filename: Path to input file

    Returns:
        List of tuples (name, speed, fly_time, rest_time)
    """
    reindeer = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Pattern: [Name] can fly [speed] km/s for [fly_time] seconds, but then must rest for [rest_time] seconds.
            match = re.search(r'([A-Za-z]+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds', line)
            if match:
                name = match.group(1)
                speed = int(match.group(2))
                fly_time = int(match.group(3))
                rest_time = int(match.group(4))
                reindeer.append((name, speed, fly_time, rest_time))
    return reindeer


def calculate_distance(speed, fly_time, rest_time, total_time):
    """
    Calculate total distance traveled by a reindeer in given time.

    Args:
        speed: Flying speed in km/s
        fly_time: Number of seconds reindeer can fly before resting
        rest_time: Number of seconds reindeer must rest
        total_time: Total race duration in seconds

    Returns:
        Total distance traveled in kilometers
    """
    cycle_length = fly_time + rest_time
    complete_cycles = total_time // cycle_length
    remaining_seconds = total_time % cycle_length

    # Distance from complete cycles
    distance = complete_cycles * fly_time * speed

    # Distance from partial cycle (only the flying portion)
    flying_in_remainder = min(remaining_seconds, fly_time)
    distance += flying_in_remainder * speed

    return distance


def find_winner(reindeer, race_duration=2503):
    """
    Find the maximum distance traveled by any reindeer.

    Args:
        reindeer: List of tuples (name, speed, fly_time, rest_time)
        race_duration: Total race time in seconds

    Returns:
        Maximum distance traveled by winning reindeer
    """
    max_distance = 0

    for name, speed, fly_time, rest_time in reindeer:
        distance = calculate_distance(speed, fly_time, rest_time, race_duration)
        max_distance = max(max_distance, distance)

    return max_distance


def run_tests():
    """Run all test cases and verify correctness."""
    print("Running tests...")

    # Test 2.1: Comet at 1000s
    assert calculate_distance(14, 10, 127, 1000) == 1120, "Test 2.1 failed"
    print("✓ Test 2.1 passed: Comet at 1000s")

    # Test 2.2: Dancer at 1000s
    assert calculate_distance(16, 11, 162, 1000) == 1056, "Test 2.2 failed"
    print("✓ Test 2.2 passed: Dancer at 1000s")

    # Test 2.3: Exact cycle boundary
    assert calculate_distance(10, 5, 5, 100) == 500, "Test 2.3 failed"
    print("✓ Test 2.3 passed: Exact cycle boundary")

    # Test 2.4: Race ends during flying
    assert calculate_distance(10, 10, 5, 12) == 100, "Test 2.4 failed"
    print("✓ Test 2.4 passed: Race ends during flying")

    # Test 2.5: Race ends during resting
    assert calculate_distance(10, 5, 10, 12) == 50, "Test 2.5 failed"
    print("✓ Test 2.5 passed: Race ends during resting")

    # Test 2.6: Single incomplete cycle
    assert calculate_distance(20, 10, 5, 7) == 140, "Test 2.6 failed"
    print("✓ Test 2.6 passed: Single incomplete cycle")

    # Test 2.7: Zero time
    assert calculate_distance(10, 5, 5, 0) == 0, "Test 2.7 failed"
    print("✓ Test 2.7 passed: Zero time")

    print("\nAll unit tests passed!\n")


def main():
    # Get input filename (default to 'input.md')
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    # Parse input
    reindeer = parse_input(filename)

    # Find winner
    max_distance = find_winner(reindeer, race_duration=2503)

    # Output result
    print(max_distance)


if __name__ == '__main__':
    run_tests()
    main()
