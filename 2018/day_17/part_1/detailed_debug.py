from solution import parse_input, get_y_range, get_x_range, flow_down
import sys

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

flowing_water = set()
settled_water = set()

sys.setrecursionlimit(10000)

flow_down(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)

# List all water positions by y coordinate
print("All water positions by row (in range):")
for y in range(min_y, max_y + 1):
    flowing_in_row = sorted([x for x, cy in flowing_water if cy == y])
    settled_in_row = sorted([x for x, cy in settled_water if cy == y])

    if flowing_in_row or settled_in_row:
        print(f"y={y}:")
        if flowing_in_row:
            print(f"  Flowing: {flowing_in_row} (count: {len(flowing_in_row)})")
        if settled_in_row:
            print(f"  Settled: {settled_in_row} (count: {len(settled_in_row)})")
        print(f"  Row total: {len(flowing_in_row) + len(settled_in_row)}")

total_flowing = len([p for p in flowing_water if min_y <= p[1] <= max_y])
total_settled = len([p for p in settled_water if min_y <= p[1] <= max_y])
print(f"\nTotal flowing: {total_flowing}")
print(f"Total settled: {total_settled}")
print(f"Grand total: {total_flowing + total_settled}")
