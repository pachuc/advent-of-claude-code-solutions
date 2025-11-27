import re

def parse_input(filename):
    """Parse the input file to extract position and velocity data."""
    points = []
    pattern = r'position=<\s*(-?\d+),\s*(-?\d+)>\s+velocity=<\s*(-?\d+),\s*(-?\d+)>'

    with open(filename, 'r') as f:
        for line in f:
            match = re.match(pattern, line.strip())
            if match:
                px, py, vx, vy = map(int, match.groups())
                points.append((px, py, vx, vy))
    return points

def calculate_positions(points, t):
    """Calculate positions of all points at time t."""
    positions = []
    for px, py, vx, vy in points:
        x = px + t * vx
        y = py + t * vy
        positions.append((x, y))
    return positions

def get_bounding_box_area(positions):
    """Calculate the area of the bounding box."""
    xs = [x for x, y in positions]
    ys = [y for x, y in positions]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max_x - min_x
    height = max_y - min_y
    return width * height

# Test with the alignment time from Part 2
points = parse_input('input.md')
T = 10011

area_before = get_bounding_box_area(calculate_positions(points, T - 1))
area_at = get_bounding_box_area(calculate_positions(points, T))
area_after = get_bounding_box_area(calculate_positions(points, T + 1))

print(f"Area at t={T-1}: {area_before}")
print(f"Area at t={T}: {area_at}")
print(f"Area at t={T+1}: {area_after}")

if area_at <= area_before and area_after > area_at:
    print("\n✓ Boundary test PASSED - t=10011 is the minimum")
else:
    print("\n✗ Boundary test FAILED")
