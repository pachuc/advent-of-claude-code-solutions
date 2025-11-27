from solution import *


input_text = """#####
#G.E#
#####"""
grid, units = parse_input(input_text)

goblin = units[0]
elf = units[1]

print("Initial state:")
print(f"Goblin at ({goblin.x}, {goblin.y})")
print(f"Elf at ({elf.x}, {elf.y})")
print("Grid:")
for row in grid:
    print(''.join(row))

# Find targets
targets = find_targets(goblin, units)
print(f"\nTargets for goblin: {len(targets)}")

# Check if adjacent
already_adjacent = any(abs(t.x - goblin.x) + abs(t.y - goblin.y) == 1 for t in targets)
print(f"Already adjacent: {already_adjacent}")

# Find in-range squares
in_range = find_in_range_squares(targets, grid)
print(f"In-range squares: {in_range}")

# BFS from goblin position
print(f"\nTrying BFS from goblin position ({goblin.x}, {goblin.y})")
print(f"Grid at goblin position: '{grid[goblin.y][goblin.x]}'")
distances = bfs_distances(grid, goblin.x, goblin.y, from_unit=True)
print(f"BFS distances: {distances}")

# Choose destination
destination = choose_destination(goblin, targets, grid)
print(f"\nChosen destination: {destination}")
