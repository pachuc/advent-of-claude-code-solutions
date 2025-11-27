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

print(f"Clay positions: {len(clay_set)}")
print(f"Y-range: {min_y} to {max_y}")
print(f"X-range: {min_x} to {max_x}")

# Initialize water sets
flowing_water = set()
settled_water = set()

# Increase recursion limit
sys.setrecursionlimit(10000)

# Start simulation
flow_down(500, 0, clay_set, flowing_water, settled_water, min_y, max_y)

# Print grid
print_grid(clay_set, flowing_water, settled_water, min_x, max_x, 0, max_y)

# Count water
water_in_range = {(x, y) for (x, y) in (flowing_water | settled_water) if min_y <= y <= max_y}

print(f"Water can reach {len(water_in_range)} tiles")
print(f"Flowing: {len([w for w in flowing_water if min_y <= w[1] <= max_y])}")
print(f"Settled: {len([w for w in settled_water if min_y <= w[1] <= max_y])}")
