import sys

def parse_input(lines):
    """Parse input and return set of clay positions."""
    clay = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Split by comma
        parts = line.split(', ')

        # Parse first part (either x=VALUE or y=VALUE)
        first = parts[0].split('=')
        first_coord = first[0]
        first_val = int(first[1])

        # Parse second part (either y=START..END or x=START..END)
        second = parts[1].split('=')
        second_coord = second[0]
        range_parts = second[1].split('..')
        range_start = int(range_parts[0])
        range_end = int(range_parts[1])

        # Generate all clay positions
        if first_coord == 'x':
            x = first_val
            for y in range(range_start, range_end + 1):
                clay.add((x, y))
        else:  # first_coord == 'y'
            y = first_val
            for x in range(range_start, range_end + 1):
                clay.add((x, y))

    return clay

def get_y_range(clay_set):
    """Get the min and max y coordinates from clay positions."""
    y_coords = [y for x, y in clay_set]
    return min(y_coords), max(y_coords)

def get_x_range(clay_set):
    """Get the min and max x coordinates from clay positions."""
    x_coords = [x for x, y in clay_set]
    return min(x_coords), max(x_coords)

def print_grid(clay_set, flowing, settled, min_x, max_x, min_y, max_y):
    """Print grid visualization for debugging."""
    print("\nGrid visualization:")
    for y in range(min_y - 1, max_y + 2):
        row = f"{y:4d} "
        for x in range(min_x - 1, max_x + 2):
            if x == 500 and y == 0:
                row += '+'
            elif (x, y) in clay_set:
                row += '#'
            elif (x, y) in settled:
                row += '~'
            elif (x, y) in flowing:
                row += '|'
            else:
                row += '.'
        print(row)
    print()

def settle_water(y, left_x, right_x, flowing, settled):
    """Convert flowing water to settled water in the given range."""
    for x in range(left_x, right_x + 1):
        if (x, y) in flowing:
            flowing.remove((x, y))
        settled.add((x, y))

def spread_horizontal(x, y, clay_set, flowing, settled, min_y, max_y):
    """
    Spread water horizontally from position (x, y).
    Returns (is_contained, left_bound, right_bound).

    This function spreads water in both directions, keeping track of:
    - Whether we hit walls or overflow on each side
    - The bounds of the water spread

    Water settles only if contained by walls on both sides.
    """
    left_wall = False
    right_wall = False
    left_bound = x
    right_bound = x
    left_overflow_pos = None
    right_overflow_pos = None

    # Spread left
    curr_x = x - 1
    while (curr_x, y) not in clay_set:
        flowing.add((curr_x, y))

        # Check if there's support below
        below = (curr_x, y + 1)
        has_support = below in clay_set or below in settled

        if not has_support:
            # No immediate support - recursively flow down to fill below
            flow_down(curr_x, y + 1, clay_set, flowing, settled, min_y, max_y)
            # Re-check if we now have settled water below
            has_support = below in settled or below in clay_set

        if not has_support:
            # Still no support after flowing - this is an overflow edge
            left_wall = False
            left_overflow_pos = curr_x
            left_bound = curr_x
            break

        # Has support, continue spreading
        left_bound = curr_x
        curr_x -= 1
    else:
        # Hit clay wall
        left_wall = True
        left_bound = curr_x + 1

    # Spread right
    curr_x = x + 1
    while (curr_x, y) not in clay_set:
        flowing.add((curr_x, y))

        # Check if there's support below
        below = (curr_x, y + 1)
        has_support = below in clay_set or below in settled

        if not has_support:
            # No immediate support - recursively flow down to fill below
            flow_down(curr_x, y + 1, clay_set, flowing, settled, min_y, max_y)
            # Re-check if we now have settled water below
            has_support = below in settled or below in clay_set

        if not has_support:
            # Still no support after flowing - this is an overflow edge
            right_wall = False
            right_overflow_pos = curr_x
            right_bound = curr_x
            break

        # Has support, continue spreading
        right_bound = curr_x
        curr_x += 1
    else:
        # Hit clay wall
        right_wall = True
        right_bound = curr_x - 1

    is_contained = left_wall and right_wall
    return is_contained, left_bound, right_bound

def flow_down(x, y, clay_set, flowing, settled, min_y, max_y):
    """
    Simulate water flowing down from position (x, y).
    Returns True if water settles or has support, False if it flows away.
    """
    # Boundary check - water fell off bottom
    if y > max_y:
        return False

    # Check if already processed
    if (x, y) in clay_set:
        return True  # Clay provides support
    if (x, y) in settled:
        return True  # Settled water provides support
    if (x, y) in flowing:
        return False  # Already processed as flowing

    # Mark as flowing initially
    flowing.add((x, y))

    # Check support below
    below = (x, y + 1)
    if below in clay_set or below in settled:
        has_support_below = True
    else:
        # Recursively flow down
        has_support_below = flow_down(x, y + 1, clay_set, flowing, settled, min_y, max_y)
        if not has_support_below:
            return False  # Water flows away, no support

    # We have support, so spread horizontally
    is_contained, left_bound, right_bound = spread_horizontal(x, y, clay_set, flowing, settled, min_y, max_y)

    # Determine if water settles
    if is_contained:
        # Water is contained by walls on both sides - settle it
        settle_water(y, left_bound, right_bound, flowing, settled)
        return True  # Settled water provides support
    else:
        # Water overflows on at least one side
        return False  # Cannot support water above

def solve(input_text):
    """Main solving function."""
    lines = input_text.strip().split('\n')

    # Parse input
    clay_set = parse_input(lines)

    # Get valid y-range
    min_y, max_y = get_y_range(clay_set)
    min_x, max_x = get_x_range(clay_set)

    # Initialize water sets
    flowing_water = set()
    settled_water = set()

    # Increase recursion limit for deep flows
    sys.setrecursionlimit(10000)

    # Start simulation from spring
    flow_down(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)

    # Optional: Print grid for debugging (comment out for large inputs)
    # print_grid(clay_set, flowing_water, settled_water, min_x, max_x, min_y, max_y)

    # Count water tiles within valid range
    water_in_range = {(x, y) for (x, y) in (flowing_water | settled_water) if min_y <= y <= max_y}

    return len(water_in_range)

if __name__ == '__main__':
    # Read input
    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)
    print(f"Water can reach {result} tiles")
