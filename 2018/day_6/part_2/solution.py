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


def count_safe_region(coordinates, threshold, min_x, max_x, min_y, max_y):
    """
    Count locations where total Manhattan distance to all coordinates is less than threshold.

    Args:
        coordinates: List of (x, y) tuples
        threshold: Maximum total distance
        min_x, max_x, min_y, max_y: Search space bounds

    Returns: Count of locations in safe region
    """
    count = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            total_distance = 0
            for cx, cy in coordinates:
                total_distance += manhattan_distance(x, y, cx, cy)
                # Early termination optimization
                if total_distance >= threshold:
                    break
            if total_distance < threshold:
                count += 1
    return count


def validate_search_space(coordinates, threshold, min_x, max_x, min_y, max_y):
    """
    Check if any boundary points are in the safe region.

    Returns: True if search space is adequate, False if it needs to be expanded
    """
    # Sample boundary points to avoid checking every single one
    # Check top and bottom edges
    step_x = max(1, (max_x - min_x) // 10)
    for x in range(min_x, max_x + 1, step_x):
        for y in [min_y, max_y]:
            total_dist = sum(manhattan_distance(x, y, cx, cy)
                           for cx, cy in coordinates)
            if total_dist < threshold:
                return False  # Boundary point in safe region - need larger space

    # Check left and right edges
    step_y = max(1, (max_y - min_y) // 10)
    for y in range(min_y, max_y + 1, step_y):
        for x in [min_x, max_x]:
            total_dist = sum(manhattan_distance(x, y, cx, cy)
                           for cx, cy in coordinates)
            if total_dist < threshold:
                return False

    return True  # No boundary points in safe region - space is adequate


def solve(input_file, threshold=10000):
    """
    Main function that finds the size of the safe region.

    Args:
        input_file: Path to input file with coordinates
        threshold: Maximum total Manhattan distance (default 10000)

    Returns:
        Integer count of locations in the safe region
    """
    # Parse coordinates
    coordinates = parse_coordinates(input_file)

    # Handle edge cases
    if not coordinates:
        return 0

    if len(coordinates) == 1:
        # Special case: single coordinate creates diamond shape
        # Number of points at Manhattan distance < threshold from one point
        cx, cy = coordinates[0]
        count = 0
        # Use threshold as radius since distance to single point is the total
        for x in range(cx - threshold + 1, cx + threshold):
            for y in range(cy - threshold + 1, cy + threshold):
                if manhattan_distance(x, y, cx, cy) < threshold:
                    count += 1
        return count

    # Determine search space using bounding box + buffer
    min_x, max_x, min_y, max_y = get_bounding_box(coordinates)

    # Calculate generous buffer (conservative estimate)
    buffer = (threshold // len(coordinates)) * 2

    search_min_x = min_x - buffer
    search_max_x = max_x + buffer
    search_min_y = min_y - buffer
    search_max_y = max_y + buffer

    # Validate search space adequacy
    if not validate_search_space(coordinates, threshold,
                                  search_min_x, search_max_x,
                                  search_min_y, search_max_y):
        # If validation fails, increase buffer and try again
        buffer = buffer * 2
        search_min_x = min_x - buffer
        search_max_x = max_x + buffer
        search_min_y = min_y - buffer
        search_max_y = max_y + buffer

    # Count safe region
    count = count_safe_region(coordinates, threshold,
                              search_min_x, search_max_x,
                              search_min_y, search_max_y)

    return count


if __name__ == '__main__':
    import sys

    # Accept input file as first command-line argument, default to 'input.md'
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    # Accept threshold as second command-line argument, default to 10000
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 10000

    try:
        result = solve(input_file, threshold)
        print(result)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
