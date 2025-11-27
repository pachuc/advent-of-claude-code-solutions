import re
import sys


def parse_input(filename):
    """Parse the input file to extract position and velocity data."""
    points = []
    pattern = r'position=<\s*(-?\d+),\s*(-?\d+)>\s+velocity=<\s*(-?\d+),\s*(-?\d+)>'

    try:
        with open(filename, 'r') as f:
            for line in f:
                match = re.match(pattern, line.strip())
                if match:
                    px, py, vx, vy = map(int, match.groups())
                    points.append((px, py, vx, vy))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []

    return points


def calculate_positions(points, t):
    """Calculate positions of all points at time t."""
    positions = []
    for px, py, vx, vy in points:
        x = px + t * vx
        y = py + t * vy
        positions.append((x, y))
    return positions


def get_bounding_box(positions):
    """Get bounding box coordinates (min_x, min_y, max_x, max_y)."""
    if not positions:
        return (0, 0, 0, 0)

    xs = [x for x, y in positions]
    ys = [y for x, y in positions]

    return (min(xs), min(ys), max(xs), max(ys))


def get_bounding_box_area(positions):
    """Calculate the area of the bounding box."""
    min_x, min_y, max_x, max_y = get_bounding_box(positions)
    width = max_x - min_x
    height = max_y - min_y
    return width * height


def find_alignment_time(points):
    """Find the time when points are most aligned (minimum bounding box area)."""
    t = 0
    prev_area = float('inf')
    MAX_ITERATIONS = 100000

    while t < MAX_ITERATIONS:
        positions = calculate_positions(points, t)
        current_area = get_bounding_box_area(positions)

        if current_area > prev_area:
            # Area is increasing, previous t was the minimum
            return max(0, t - 1)

        prev_area = current_area
        t += 1

    raise RuntimeError("Failed to find alignment within iteration limit")


def main(input_file='input.md'):
    """Main function to solve Part 2."""
    # Parse input
    points = parse_input(input_file)
    if not points:
        print("Error: No valid points parsed from input")
        return

    # Find alignment time
    alignment_time = find_alignment_time(points)

    # Output result (just the time value)
    print(alignment_time)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    main(input_file)
