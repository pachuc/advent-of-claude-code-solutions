"""Test to verify the alignment time produces minimum bounding box area."""
import sys
sys.path.insert(0, '.')

from solution import parse_input, calculate_positions, get_bounding_box_area

# Parse input
points = parse_input('input.md')
T = 10011  # Expected alignment time

# Calculate areas at T-1, T, T+1
area_before = get_bounding_box_area(calculate_positions(points, T - 1))
area_at = get_bounding_box_area(calculate_positions(points, T))
area_after = get_bounding_box_area(calculate_positions(points, T + 1))

print(f"Area at t={T-1}: {area_before}")
print(f"Area at t={T}: {area_at}")
print(f"Area at t={T+1}: {area_after}")

# Verify boundaries
assert area_at <= area_before, f"Area at T ({area_at}) should be <= area before ({area_before})"
assert area_after > area_at, f"Area after T ({area_after}) should be > area at T ({area_at})"

print("\n✓ Boundary test passed - t=10011 produces minimum bounding box area")
