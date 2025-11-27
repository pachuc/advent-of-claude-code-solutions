from solution import parse_input, get_y_range, get_x_range, flow_down, print_grid
import sys

# Example from problem description
example_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=10..13
x=506, y=1..2
y=13, x=498..504"""

lines = example_input.strip().split('\n')
clay_set = parse_input(lines)

min_y, max_y = get_y_range(clay_set)
min_x, max_x = get_x_range(clay_set)

print(f"Y range: {min_y} to {max_y}")
print(f"X range: {min_x} to {max_x}")

flowing_water = set()
settled_water = set()

sys.setrecursionlimit(10000)

flow_down(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)

print_grid(clay_set, flowing_water, settled_water, min_x, max_x, 0, max_y)

water_in_range = {(x, y) for (x, y) in (flowing_water | settled_water) if min_y <= y <= max_y}

print(f"Flowing water: {len([p for p in flowing_water if min_y <= p[1] <= max_y])}")
print(f"Settled water: {len([p for p in settled_water if min_y <= p[1] <= max_y])}")
print(f"Total water in range: {len(water_in_range)}")
