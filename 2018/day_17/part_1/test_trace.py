import sys

# Copy the solution code but add debug prints
def parse_input(lines):
    clay = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(', ')
        first = parts[0].split('=')
        first_coord = first[0]
        first_val = int(first[1])
        second = parts[1].split('=')
        second_coord = second[0]
        range_parts = second[1].split('..')
        range_start = int(range_parts[0])
        range_end = int(range_parts[1])
        if first_coord == 'x':
            x = first_val
            for y in range(range_start, range_end + 1):
                clay.add((x, y))
        else:
            y = first_val
            for x in range(range_start, range_end + 1):
                clay.add((x, y))
    return clay

def settle_water(y, left_x, right_x, flowing, settled):
    print(f"      SETTLE y={y}, x={left_x} to {right_x}")
    for x in range(left_x, right_x + 1):
        if (x, y) in flowing:
            flowing.remove((x, y))
        settled.add((x, y))

def spread_horizontal(x, y, clay_set, flowing, settled, min_y, max_y, depth):
    indent = "  " * depth
    print(f"{indent}spread_horizontal({x}, {y})")

    left_wall = False
    right_wall = False
    left_bound = x
    right_bound = x

    # Spread left (simplified for debugging)
    curr_x = x - 1
    while (curr_x, y) not in clay_set:
        flowing.add((curr_x, y))
        left_bound = curr_x
        below = (curr_x, y + 1)
        has_support = below in clay_set or below in settled
        if not has_support:
            print(f"{indent}  Left {curr_x}: no support, flow_down({curr_x}, {y+1})")
            flow_down(curr_x, y + 1, clay_set, flowing, settled, min_y, max_y, depth + 1)
            has_support = below in settled or below in clay_set
        if not has_support:
            print(f"{indent}  Left overflow at {curr_x}")
            left_wall = False
            break
        curr_x -= 1
    else:
        left_wall = True
        left_bound = curr_x + 1

    # Spread right
    curr_x = x + 1
    while (curr_x, y) not in clay_set:
        flowing.add((curr_x, y))
        right_bound = curr_x
        below = (curr_x, y + 1)
        has_support = below in clay_set or below in settled
        if not has_support:
            print(f"{indent}  Right {curr_x}: no support, flow_down({curr_x}, {y+1})")
            flow_down(curr_x, y + 1, clay_set, flowing, settled, min_y, max_y, depth + 1)
            has_support = below in settled or below in clay_set
        if not has_support:
            print(f"{indent}  Right overflow at {curr_x}")
            right_wall = False
            break
        curr_x += 1
    else:
        right_wall = True
        right_bound = curr_x - 1

    print(f"{indent}  left_wall={left_wall}, right_wall={right_wall}, bounds=[{left_bound},{right_bound}]")
    is_contained = left_wall and right_wall
    return is_contained, left_bound, right_bound

def flow_down(x, y, clay_set, flowing, settled, min_y, max_y, depth=0):
    indent = "  " * depth
    if depth < 3 or y < 5:  # Only print first few levels
        print(f"{indent}flow_down({x}, {y})")

    if y > max_y:
        return False
    if (x, y) in clay_set:
        return True
    if (x, y) in settled:
        return True
    if (x, y) in flowing:
        return False

    flowing.add((x, y))

    below = (x, y + 1)
    if below in clay_set or below in settled:
        has_support_below = True
    else:
        has_support_below = flow_down(x, y + 1, clay_set, flowing, settled, min_y, max_y, depth + 1)
        if not has_support_below:
            return False

    is_contained, left_bound, right_bound = spread_horizontal(x, y, clay_set, flowing, settled, min_y, max_y, depth)

    if is_contained:
        settle_water(y, left_bound, right_bound, flowing, settled)
        return True
    else:
        return False

# Test
example_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7"""

lines = example_input.strip().split('\n')
clay_set = parse_input(lines)
min_y, max_y = 2, 7

flowing_water = set()
settled_water = set()

sys.setrecursionlimit(1000)
flow_down(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)
