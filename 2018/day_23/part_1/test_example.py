#!/usr/bin/env python3

from solution import parse_input, find_strongest_nanobot, count_in_range

def test_example():
    """Test with the example from the problem statement."""
    nanobots = parse_input('test_example.txt')

    # Verify parsing
    assert len(nanobots) == 9, f"Expected 9 nanobots, got {len(nanobots)}"

    # Find strongest
    strongest = find_strongest_nanobot(nanobots)
    print(f"Strongest nanobot: pos=<{strongest[0]},{strongest[1]},{strongest[2]}>, r={strongest[3]}")

    # Verify strongest is correct
    assert strongest == (0, 0, 0, 4), f"Expected strongest at (0,0,0) with r=4, got {strongest}"

    # Count in range
    result = count_in_range(nanobots, strongest)
    print(f"Nanobots in range: {result}")

    # Verify result
    assert result == 7, f"Expected 7 nanobots in range, got {result}"

    print("✓ Example test passed!")
    return True

if __name__ == "__main__":
    test_example()
