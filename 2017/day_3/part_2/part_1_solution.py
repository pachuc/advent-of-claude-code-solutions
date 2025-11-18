import math

def spiral_manhattan_distance(n):
    """
    Calculate Manhattan distance from square n to square 1 in spiral grid.

    Coordinate system: (0,0) at square 1, +X right, +Y up
    Spiral direction: RIGHT → UP → LEFT → DOWN (clockwise when viewed with Y-up)

    Args:
        n: Square number in the spiral (positive integer)

    Returns:
        Manhattan distance (positive integer)
    """
    # Base case
    if n == 1:
        return 0

    # Find ring number
    # Each ring k ends with (2k+1)², so we find which ring contains n
    side_length = math.ceil(math.sqrt(n))
    if side_length % 2 == 0:
        side_length += 1
    ring = side_length // 2

    # Find position within ring
    max_prev_ring = (2 * ring - 1) ** 2
    position_in_ring = n - max_prev_ring - 1

    # Each side has 2*ring numbers
    side_len = 2 * ring
    side_index = position_in_ring // side_len
    offset = position_in_ring % side_len

    # Calculate coordinates based on side
    # Ring k: right side (k, -k+1) to (k, k)
    #         top side (k-1, k) to (-k, k)
    #         left side (-k, k-1) to (-k, -k)
    #         bottom side (-k+1, -k) to (k, -k)
    if side_index == 0:  # Right side, moving up
        x, y = ring, -ring + 1 + offset
    elif side_index == 1:  # Top side, moving left
        x, y = ring - 1 - offset, ring
    elif side_index == 2:  # Left side, moving down
        x, y = -ring, ring - 1 - offset
    else:  # Bottom side, moving right
        x, y = -ring + 1 + offset, -ring

    # Return Manhattan distance
    return abs(x) + abs(y)


def main():
    # Read input
    with open('input.md', 'r') as f:
        n = int(f.read().strip())

    # Calculate result
    result = spiral_manhattan_distance(n)

    # Output result
    print(result)


if __name__ == "__main__":
    main()
