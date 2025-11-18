from solution import *

# Test example from problem statement
test_rules_text = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

rules = parse_rules(test_rules_text)
initial_grid = ['.#.', '..#', '###']

print("Initial grid (3x3):")
for row in initial_grid:
    print(row)
print()

# After 1 iteration
grid_1 = perform_iterations(initial_grid, rules, 1)
print(f"After 1 iteration ({len(grid_1)}x{len(grid_1)}):")
for row in grid_1:
    print(row)
print(f"On pixels: {count_on_pixels(grid_1)}")
print()

# After 2 iterations
grid_2 = perform_iterations(initial_grid, rules, 2)
print(f"After 2 iterations ({len(grid_2)}x{len(grid_2)}):")
for row in grid_2:
    print(row)
print(f"On pixels: {count_on_pixels(grid_2)}")
print()

print(f"Expected: 12 pixels")
print(f"Actual: {count_on_pixels(grid_2)} pixels")
print(f"Test {'PASSED' if count_on_pixels(grid_2) == 12 else 'FAILED'}")
