#!/usr/bin/env python3

from solution import parse_input, find_strongest_nanobot, count_in_range, manhattan_distance

def validate_solution():
    """Perform comprehensive validation of the solution."""
    print("=" * 60)
    print("Validating Solution with Actual Input")
    print("=" * 60)
    
    # Parse input
    nanobots = parse_input('input.md')
    print(f"✓ Total nanobots parsed: {len(nanobots)}")
    
    # Sanity check: should have 1000 nanobots
    assert len(nanobots) == 1000, f"Expected 1000 nanobots, got {len(nanobots)}"
    
    # Find strongest
    strongest = find_strongest_nanobot(nanobots)
    sx, sy, sz, sr = strongest
    print(f"✓ Strongest nanobot: pos=<{sx},{sy},{sz}>, r={sr}")
    
    # Verify this matches what's documented
    assert sr == 99859637, f"Expected strongest radius to be 99859637, got {sr}"
    assert (sx, sy, sz) == (113369857, 1348469, 44315500), f"Unexpected strongest position"
    
    # Count in range
    result = count_in_range(nanobots, strongest)
    print(f"✓ Nanobots in range: {result}")
    
    # Sanity checks
    assert 1 <= result <= 1000, f"Result {result} outside valid range [1, 1000]"
    assert result == 713, f"Expected result to be 713 based on implementation summary, got {result}"
    
    # Verify the strongest nanobot counts itself
    self_dist = manhattan_distance((sx, sy, sz), (sx, sy, sz))
    assert self_dist == 0, f"Distance from nanobot to itself should be 0, got {self_dist}"
    assert self_dist <= sr, "Strongest nanobot should always be in its own range"
    
    print("\n" + "=" * 60)
    print("✓ All validation checks passed!")
    print("=" * 60)
    print(f"\nFinal Answer: {result}")
    
    return result

if __name__ == "__main__":
    validate_solution()
