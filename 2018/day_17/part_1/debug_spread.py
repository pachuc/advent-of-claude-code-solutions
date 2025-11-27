from solution import parse_input, get_y_range
import sys

example_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7"""

lines = example_input.strip().split('\n')
clay_set = parse_input(lines)
min_y, max_y = get_y_range(clay_set)

# Manually test spread_horizontal at y=2, x=500
y = 2
x = 500

print(f"Testing spread at ({x}, {y})")
print(f"Clay at y={y}: {sorted([cx for cx, cy in clay_set if cy == y])}")
print(f"Clay at y={y+1}: {sorted([cx for cx, cy in clay_set if cy == y+1])}")

# Simulate spread left
print("\nSpreading left from x=500:")
curr_x = 499
while (curr_x, y) not in clay_set:
    print(f"  x={curr_x}: ", end="")
    below = (curr_x, y + 1)
    if below in clay_set:
        print(f"clay below")
    else:
        print(f"NO clay below - would overflow")
        print(f"    left_bound would be {curr_x}, breaking")
        break
    curr_x -= 1
else:
    print(f"  Hit clay wall at x={curr_x}")
    print(f"  left_bound would be {curr_x + 1}")

# Simulate spread right
print("\nSpreading right from x=500:")
curr_x = 501
settled = set()  # empty for this test
while (curr_x, y) not in clay_set:
    print(f"  x={curr_x}: ", end="")
    below = (curr_x, y + 1)
    if below in clay_set or below in settled:
        print(f"support below (clay or settled)")
    else:
        print(f"NO support below - would overflow")
        print(f"    right_bound would be {curr_x}, breaking")
        break
    curr_x += 1
else:
    print(f"  Hit clay wall at x={curr_x}")
    print(f"  right_bound would be {curr_x - 1}")
