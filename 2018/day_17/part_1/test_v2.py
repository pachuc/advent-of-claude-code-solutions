import sys

# Import solution
with open('solution_v2.py', 'r') as f:
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

# Initialize water sets
water = set()
settled = set()

# Increase recursion limit
sys.setrecursionlimit(10000)

# Start simulation
flow(500, 0, clay_set, water, settled, min_y, max_y)

# Print grid
print_grid(clay_set, water - settled, settled, min_x, max_x, 0, max_y)

# Count water
water_in_range = {(x, y) for (x, y) in water if min_y <= y <= max_y}

print(f"\nWater can reach {len(water_in_range)} tiles (expected 57)")
flowing_count = len(water - settled)
settled_count = len(settled)
print(f"Flowing: {len([w for w in (water - settled) if min_y <= w[1] <= max_y])}")
print(f"Settled: {len([w for w in settled if min_y <= w[1] <= max_y])}")
