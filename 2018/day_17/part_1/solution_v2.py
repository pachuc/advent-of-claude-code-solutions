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

def fill_horizontal(x, y, clay_set, water, min_y, max_y):
    """
    Fill water horizontally from position (x, y).
    Returns (left_bound, right_bound, contained)
    where contained is True if water is blocked by walls on both sides.
    """
    # Find left extent
    left_x = x
    while True:
        if (left_x - 1, y) in clay_set:
            # Hit wall on left
            left_wall = True
            break
        if (left_x - 1, y + 1) not in clay_set and (left_x - 1, y + 1) not in water:
            # No support on left, water falls
            left_wall = False
            break
        left_x -= 1

    # Find right extent
    right_x = x
    while True:
        if (right_x + 1, y) in clay_set:
            # Hit wall on right
            right_wall = True
            break
        if (right_x + 1, y + 1) not in clay_set and (right_x + 1, y + 1) not in water:
            # No support on right, water falls
            right_wall = False
            break
        right_x += 1

    # Fill the range
    for fill_x in range(left_x, right_x + 1):
        water.add((fill_x, y))

    contained = left_wall and right_wall
    return (left_x, right_x, contained)

def flow(x, y, clay_set, water, settled, min_y, max_y):
    """
    Simulate water flowing from position (x, y).
    """
    # Check if out of bounds or already processed
    if y > max_y:
        return
    if (x, y) in water or (x, y) in clay_set:
        return

    # Flow down as far as possible
    while y <= max_y and (x, y) not in clay_set and (x, y + 1) not in clay_set and (x, y + 1) not in water:
        water.add((x, y))
        y += 1

    if y > max_y:
        return

    water.add((x, y))

    # Now we're at a position where we can't go down further
    # Try to spread horizontally and settle
    while True:
        left_x, right_x, contained = fill_horizontal(x, y, clay_set, water, min_y, max_y)

        if contained:
            # Water is contained, mark as settled
            for settle_x in range(left_x, right_x + 1):
                water.discard((settle_x, y))
                settled.add((settle_x, y))
                water.add((settle_x, y))  # Keep in water for support checks
            # Move up one level and try again
            y -= 1
            if y < 0:
                break
        else:
            # Water overflows, flow down from overflow points
            # Left overflow
            if not (left_x - 1, y) in clay_set:
                flow(left_x, y + 1, clay_set, water, settled, min_y, max_y)
            # Right overflow
            if not (right_x + 1, y) in clay_set:
                flow(right_x, y + 1, clay_set, water, settled, min_y, max_y)
            break

def solve(input_text):
    """Main solving function."""
    lines = input_text.strip().split('\n')

    # Parse input
    clay_set = parse_input(lines)

    # Get valid y-range
    min_y, max_y = get_y_range(clay_set)
    min_x, max_x = get_x_range(clay_set)

    # Initialize water sets
    water = set()  # All water (flowing + settled)
    settled = set()  # Only settled water

    # Increase recursion limit for deep flows
    sys.setrecursionlimit(10000)

    # Start simulation from spring
    flow(500, 0, clay_set, water, settled, min_y, max_y)

    # Count water tiles within valid range
    water_in_range = {(x, y) for (x, y) in water if min_y <= y <= max_y}

    return len(water_in_range)

if __name__ == '__main__':
    # Read input
    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)
    print(f"Water can reach {result} tiles")
