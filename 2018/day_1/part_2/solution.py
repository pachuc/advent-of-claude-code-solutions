from itertools import cycle

def solve(filename='input.md'):
    """
    Find the first frequency reached twice during continuous looping.

    Args:
        filename: Input file path (default: 'input.md')

    Returns:
        The first duplicate frequency as an integer.
    """
    try:
        # Read and parse input (same as Part 1)
        with open(filename, 'r') as f:
            changes = [int(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} file not found")
        return None

    # Initialize tracking structures
    seen = {0}  # Start frequency is already "seen"
    frequency = 0

    # Infinite loop with cycle detection
    for change in cycle(changes):
        frequency += change
        if frequency in seen:
            return frequency  # Found duplicate!
        seen.add(frequency)

def solve_with_list(changes):
    """Helper function for testing with inline lists"""
    seen = {0}
    frequency = 0
    for change in cycle(changes):
        frequency += change
        if frequency in seen:
            return frequency
        seen.add(frequency)

def run_tests():
    """Run all example tests from the problem statement"""
    print("Running example tests...")

    # Test 1.1: +1, -2, +3, +1 -> 2
    result = solve_with_list([1, -2, 3, 1])
    assert result == 2, f"Test 1.1 failed: expected 2, got {result}"
    print("✓ Test 1.1 passed: [1, -2, 3, 1] -> 2")

    # Test 1.2: +1, -1 -> 0
    result = solve_with_list([1, -1])
    assert result == 0, f"Test 1.2 failed: expected 0, got {result}"
    print("✓ Test 1.2 passed: [1, -1] -> 0")

    # Test 1.3: +3, +3, +4, -2, -4 -> 10
    result = solve_with_list([3, 3, 4, -2, -4])
    assert result == 10, f"Test 1.3 failed: expected 10, got {result}"
    print("✓ Test 1.3 passed: [3, 3, 4, -2, -4] -> 10")

    # Test 1.4: -6, +3, +8, +5, -6 -> 5
    result = solve_with_list([-6, 3, 8, 5, -6])
    assert result == 5, f"Test 1.4 failed: expected 5, got {result}"
    print("✓ Test 1.4 passed: [-6, 3, 8, 5, -6] -> 5")

    # Test 1.5: +7, +7, -2, -7, -4 -> 14
    result = solve_with_list([7, 7, -2, -7, -4])
    assert result == 14, f"Test 1.5 failed: expected 14, got {result}"
    print("✓ Test 1.5 passed: [7, 7, -2, -7, -4] -> 14")

    print("\n✅ All example tests passed!\n")

if __name__ == '__main__':
    # Run tests first
    run_tests()

    # Validate that input parsing matches Part 1
    print("Validating input parsing...")
    with open('input.md', 'r') as f:
        changes = [int(line.strip()) for line in f if line.strip()]
    part1_sum = sum(changes)
    print(f"Sum of all changes: {part1_sum}")
    assert part1_sum == 474, f"Input parsing doesn't match Part 1: expected 474, got {part1_sum}"
    print("✓ Input validation passed: matches Part 1\n")

    # Run on actual input
    print("Running on actual input...")
    result = solve()
    if result is not None:
        print(f"\n🎯 Part 2 answer: {result}")
