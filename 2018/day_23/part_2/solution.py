import re
import heapq


def parse_input(filename):
    """
    Parse nanobot data from input file.

    Returns:
        List of tuples: [(x, y, z, radius), ...]
    """
    nanobots = []
    pattern = r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)'

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = re.match(pattern, line)
            if match:
                x, y, z, r = map(int, match.groups())
                nanobots.append((x, y, z, r))

    return nanobots


def manhattan_distance(pos1, pos2):
    """
    Calculate Manhattan distance between two 3D points.

    Args:
        pos1: tuple (x1, y1, z1)
        pos2: tuple (x2, y2, z2)

    Returns:
        int: Manhattan distance
    """
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def get_search_bounds(nanobots):
    """
    Calculate initial bounding box for search.
    Consider: min/max of (nanobot_position ± radius) for each dimension
    """
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    min_z, max_z = float('inf'), float('-inf')

    for x, y, z, r in nanobots:
        # Each nanobot can affect space from (pos - r) to (pos + r)
        min_x = min(min_x, x - r)
        max_x = max(max_x, x + r)
        min_y = min(min_y, y - r)
        max_y = max(max_y, y + r)
        min_z = min(min_z, z - r)
        max_z = max(max_z, z + r)

    return (min_x, max_x), (min_y, max_y), (min_z, max_z)


def count_bots_in_range(position, nanobots):
    """
    For a given position, count how many nanobots can reach it.
    A nanobot at (bx, by, bz) with radius r can reach position p if:
    manhattan_distance(p, (bx, by, bz)) <= r
    """
    count = 0
    px, py, pz = position
    for bx, by, bz, r in nanobots:
        if manhattan_distance((px, py, pz), (bx, by, bz)) <= r:
            count += 1
    return count


def max_bots_for_box(box, nanobots):
    """
    Upper bound estimate: Count nanobots that could possibly reach
    ANY point in the box.

    For a nanobot to potentially reach the box, the minimum distance
    from the nanobot to the box must be <= nanobot radius.
    """
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box
    count = 0

    for bx, by, bz, r in nanobots:
        # Calculate minimum Manhattan distance from nanobot to box
        min_dist = 0

        # X dimension
        if bx < x_min:
            min_dist += x_min - bx
        elif bx > x_max:
            min_dist += bx - x_max
        # else: bx is within [x_min, x_max], contributes 0

        # Y dimension
        if by < y_min:
            min_dist += y_min - by
        elif by > y_max:
            min_dist += by - y_max

        # Z dimension
        if bz < z_min:
            min_dist += z_min - bz
        elif bz > z_max:
            min_dist += bz - z_max

        if min_dist <= r:
            count += 1

    return count


def get_box_size(box):
    """Calculate total size of box (sum of dimensions)."""
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box
    return (x_max - x_min) + (y_max - y_min) + (z_max - z_min)


def is_single_point(box):
    """Check if box has collapsed to a single point."""
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box
    return x_min == x_max and y_min == y_max and z_min == z_max


def box_to_point(box):
    """Convert single-point box to coordinate tuple."""
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box
    return (x_min, y_min, z_min)


def min_distance_box_to_origin(box):
    """Calculate minimum Manhattan distance from any point in box to origin."""
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box

    # For each dimension, pick the value closest to 0
    if x_min <= 0 <= x_max:
        x = 0
    else:
        x = min(abs(x_min), abs(x_max))

    if y_min <= 0 <= y_max:
        y = 0
    else:
        y = min(abs(y_min), abs(y_max))

    if z_min <= 0 <= z_max:
        z = 0
    else:
        z = min(abs(z_min), abs(z_max))

    return x + y + z


def subdivide_box(box):
    """
    Divide box into up to 8 octants.
    Split each dimension at midpoint.
    Handles degenerate boxes (already collapsed in one or more dimensions).
    """
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = box

    x_mid = (x_min + x_max) // 2
    y_mid = (y_min + y_max) // 2
    z_mid = (z_min + z_max) // 2

    # Generate ranges for each dimension
    # If dimension already collapsed (min == max), keep it as single range
    x_ranges = [(x_min, x_mid), (x_mid + 1, x_max)] if x_min < x_max else [(x_min, x_max)]
    y_ranges = [(y_min, y_mid), (y_mid + 1, y_max)] if y_min < y_max else [(y_min, y_max)]
    z_ranges = [(z_min, z_mid), (z_mid + 1, z_max)] if z_min < z_max else [(z_min, z_max)]

    # Generate all combinations (cartesian product)
    octants = []
    for x_range in x_ranges:
        for y_range in y_ranges:
            for z_range in z_ranges:
                octants.append((x_range, y_range, z_range))

    return octants


def find_optimal_position(nanobots):
    """
    Use octree subdivision with priority queue to find optimal position.

    Strategy:
    - Start with bounding box of entire search space
    - Use priority queue to explore most promising regions first
    - Subdivide boxes into 8 octants
    - Track best single-point solution found so far
    - Prune boxes that can't beat current best
    """

    # Get initial bounds
    bounds_x, bounds_y, bounds_z = get_search_bounds(nanobots)
    initial_box = (bounds_x, bounds_y, bounds_z)

    # Priority queue: (-max_bots, dist_to_origin, box_size, box)
    # Negative for max-heap behavior (higher bot count = higher priority)
    # dist_to_origin as tiebreaker (closer to origin = higher priority)
    # box_size as tiebreaker (smaller boxes = higher priority)
    pq = []

    initial_max = max_bots_for_box(initial_box, nanobots)
    box_size = get_box_size(initial_box)
    min_dist = min_distance_box_to_origin(initial_box)
    heapq.heappush(pq, (-initial_max, min_dist, box_size, initial_box))

    best_count = 0
    best_distance = float('inf')
    best_position = None

    while pq:
        neg_max_bots, min_dist, size, box = heapq.heappop(pq)
        max_bots = -neg_max_bots

        # Pruning: If this box can't beat our best, skip it
        if max_bots < best_count:
            continue
        if max_bots == best_count:
            # Even if equal count, check if box is too far from origin
            # This handles the tiebreaker: prefer positions closer to origin
            min_dist_to_origin = min_distance_box_to_origin(box)
            if min_dist_to_origin >= best_distance:
                continue

        # If box is a single point, evaluate it
        if is_single_point(box):
            point = box_to_point(box)
            count = count_bots_in_range(point, nanobots)
            dist = manhattan_distance(point, (0, 0, 0))

            if count > best_count or (count == best_count and dist < best_distance):
                best_count = count
                best_distance = dist
                best_position = point
        else:
            # Subdivide box into 8 octants
            octants = subdivide_box(box)
            for octant in octants:
                octant_max = max_bots_for_box(octant, nanobots)
                octant_size = get_box_size(octant)
                octant_min_dist = min_distance_box_to_origin(octant)
                heapq.heappush(pq, (-octant_max, octant_min_dist, octant_size, octant))

    return best_position, best_count, best_distance


def main():
    """Main execution function."""
    # Parse input
    nanobots = parse_input('input.md')

    if len(nanobots) == 0:
        print("Error: No nanobots found")
        return 0

    # Find optimal position
    position, count, distance = find_optimal_position(nanobots)

    # Final answer is the distance from origin
    print(distance)
    return distance


if __name__ == "__main__":
    main()
