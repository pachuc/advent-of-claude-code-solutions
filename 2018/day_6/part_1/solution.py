def parse_coordinates(input_file):
    """
    Parse the input file to extract coordinate pairs.

    Returns: List of tuples [(x1, y1), (x2, y2), ...]
    """
    coordinates = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                x, y = line.split(',')
                coordinates.append((int(x.strip()), int(y.strip())))
            except ValueError:
                continue
    return coordinates


def get_bounding_box(coordinates):
    """
    Find the min/max x and y values to define the search space.

    Returns: (min_x, max_x, min_y, max_y)
    """
    if not coordinates:
        return 0, 0, 0, 0

    xs = [x for x, y in coordinates]
    ys = [y for x, y in coordinates]

    return min(xs), max(xs), min(ys), max(ys)


def manhattan_distance(x1, y1, x2, y2):
    """Calculate Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)


def build_grid(coordinates, min_x, max_x, min_y, max_y):
    """
    For each grid cell, determine which coordinate it's closest to.

    Returns: Dictionary mapping (x, y) -> coordinate_index (or None for ties)
    """
    grid = {}

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            # Calculate distance to all coordinates
            distances = []
            for i, (cx, cy) in enumerate(coordinates):
                dist = manhattan_distance(x, y, cx, cy)
                distances.append((dist, i))

            # Find minimum distance
            distances.sort()
            min_dist = distances[0][0]

            # Check if there's a tie (multiple coordinates with same min distance)
            closest_coords = [idx for dist, idx in distances if dist == min_dist]

            if len(closest_coords) == 1:
                # Single closest coordinate
                grid[(x, y)] = closest_coords[0]
            else:
                # Tie - don't assign to any coordinate
                grid[(x, y)] = None

    return grid


def find_infinite_coordinates(grid, coordinates, min_x, max_x, min_y, max_y):
    """
    Any coordinate that owns cells on the boundary has an infinite area.

    Returns: Set of coordinate indices with infinite areas
    """
    infinite_coords = set()

    # Check all cells on the boundary
    for x in range(min_x, max_x + 1):
        # Top edge
        coord_idx = grid.get((x, min_y))
        if coord_idx is not None:
            infinite_coords.add(coord_idx)

        # Bottom edge
        coord_idx = grid.get((x, max_y))
        if coord_idx is not None:
            infinite_coords.add(coord_idx)

    for y in range(min_y, max_y + 1):
        # Left edge
        coord_idx = grid.get((min_x, y))
        if coord_idx is not None:
            infinite_coords.add(coord_idx)

        # Right edge
        coord_idx = grid.get((max_x, y))
        if coord_idx is not None:
            infinite_coords.add(coord_idx)

    return infinite_coords


def count_areas(grid, infinite_coords, num_coordinates):
    """
    Count the area size for each coordinate that has a finite area.

    Returns: Dictionary mapping coordinate_index -> area_count
    """
    areas = {i: 0 for i in range(num_coordinates)}

    # Count cells for each coordinate
    for coord_idx in grid.values():
        if coord_idx is not None:
            areas[coord_idx] += 1

    # Filter out infinite coordinates
    finite_areas = {idx: count for idx, count in areas.items()
                    if idx not in infinite_coords}

    return finite_areas


def find_largest_finite_area(areas):
    """
    Find the largest area among finite coordinates.

    Returns: Integer representing the largest finite area size
    """
    if not areas:
        return 0
    return max(areas.values())


def solve(input_file):
    """
    Main function that orchestrates the solution.

    Returns: The size of the largest finite area
    """
    # Parse coordinates
    coordinates = parse_coordinates(input_file)

    # Handle edge cases
    if not coordinates:
        return 0

    if len(coordinates) == 1:
        return 0

    # Calculate bounding box
    min_x, max_x, min_y, max_y = get_bounding_box(coordinates)

    # Build grid with assignments
    grid = build_grid(coordinates, min_x, max_x, min_y, max_y)

    # Identify infinite coordinates
    infinite_coords = find_infinite_coordinates(grid, coordinates, min_x, max_x, min_y, max_y)

    # Count areas for finite coordinates
    finite_areas = count_areas(grid, infinite_coords, len(coordinates))

    # Find and return the largest finite area
    return find_largest_finite_area(finite_areas)


if __name__ == '__main__':
    import sys

    # Accept input file as command-line argument, default to 'input.md'
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    try:
        result = solve(input_file)
        print(result)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
