from solution import parse_input, get_y_range, get_x_range, print_grid
import sys

# Smaller test - just the first container
example_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7"""

lines = example_input.strip().split('\n')
clay_set = parse_input(lines)

min_y, max_y = get_y_range(clay_set)
min_x, max_x = get_x_range(clay_set)

flowing_water = set()
settled_water = set()

sys.setrecursionlimit(10000)

# Manual flow simulation with debug
def flow_down_debug(x, y, clay_set, flowing, settled, min_y, max_y, depth=0):
    indent = "  " * depth
    print(f"{indent}flow_down({x}, {y})")

    if y > max_y:
        print(f"{indent}  -> fell off bottom")
        return False

    if (x, y) in clay_set:
        print(f"{indent}  -> clay, support=True")
        return True
    if (x, y) in settled:
        print(f"{indent}  -> settled water, support=True")
        return True
    if (x, y) in flowing:
        print(f"{indent}  -> already flowing, support=False")
        return False

    flowing.add((x, y))
    print(f"{indent}  marked as flowing")

    below = (x, y + 1)
    if below in clay_set or below in settled:
        has_support_below = True
        print(f"{indent}  support below (clay or settled)")
    else:
        print(f"{indent}  no immediate support, flowing down...")
        has_support_below = flow_down_debug(x, y + 1, clay_set, flowing, settled, min_y, max_y, depth + 1)
        print(f"{indent}  returned support={has_support_below}")
        if not has_support_below:
            return False

    print(f"{indent}  spreading horizontally...")
    # Simplified spread for debugging
    is_contained = False
    print(f"{indent}  is_contained={is_contained}")

    if is_contained:
        print(f"{indent}  -> settling")
        return True
    else:
        print(f"{indent}  -> overflow, support=False")
        return False

flow_down_debug(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)

print("\n" + "="*60)
print_grid(clay_set, flowing_water, settled_water, min_x, max_x, 0, max_y)
