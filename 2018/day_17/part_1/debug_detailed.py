import sys

# Import solution
with open('solution.py', 'r') as f:
    exec(f.read())

# Read example input
with open('test_example.txt', 'r') as f:
    input_text = f.read()

lines = input_text.strip().split('\n')

# Parse input
clay_set = parse_input(lines)

# Get valid y-range
min_y, max_y = get_y_range(clay_set)
min_x, max_x = get_x_range(clay_set)

print("Clay positions:")
for y in range(0, max_y + 1):
    clay_at_y = sorted([x for (x, cy) in clay_set if cy == y])
    if clay_at_y:
        print(f"  y={y}: x={clay_at_y}")

# Initialize water sets
flowing_water = set()
settled_water = set()

# Increase recursion limit
sys.setrecursionlimit(10000)

# Start simulation
flow_down(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)

print("\nWater positions:")
for y in range(min_y, max_y + 1):
    flowing_at_y = sorted([x for (x, cy) in flowing_water if cy == y])
    settled_at_y = sorted([x for (x, cy) in settled_water if cy == y])
    if flowing_at_y or settled_at_y:
        print(f"  y={y}: flowing={flowing_at_y}, settled={settled_at_y}")

# Print grid
print_grid(clay_set, flowing_water, settled_water, min_x, max_x, 0, max_y)

# Count water
water_in_range = {(x, y) for (x, y) in (flowing_water | settled_water) if min_y <= y <= max_y}

print(f"\nWater can reach {len(water_in_range)} tiles (expected 57)")
print(f"Flowing: {len([w for w in flowing_water if min_y <= w[1] <= max_y])}")
print(f"Settled: {len([w for w in settled_water if min_y <= w[1] <= max_y])}")
