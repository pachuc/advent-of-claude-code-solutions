from solution import *

# Read actual input
with open('input.md', 'r') as f:
    input_text = f.read()

rules = parse_rules(input_text)
initial_grid = ['.#.', '..#', '###']

print("Grid size progression:")
print(f"Start: {len(initial_grid)}x{len(initial_grid)}")

grid = initial_grid
expected_sizes = [3, 4, 6, 9, 12, 18]

for i in range(5):
    grid_size = len(grid)

    # Determine block size
    if grid_size % 2 == 0:
        block_size = 2
        new_size = grid_size // 2 * 3
    else:
        block_size = 3
        new_size = grid_size // 3 * 4

    print(f"Iteration {i+1}: {grid_size}x{grid_size} → divide by {block_size}x{block_size} → {new_size}x{new_size}")

    # Perform iteration
    blocks = divide_grid(grid, block_size)
    enhanced_blocks = []
    for block_row in blocks:
        enhanced_row = []
        for block in block_row:
            enhanced = enhance_block(block, rules)
            enhanced_row.append(enhanced)
        enhanced_blocks.append(enhanced_row)
    grid = reassemble_grid(enhanced_blocks)

    # Verify size
    actual_size = len(grid)
    print(f"  Actual result: {actual_size}x{actual_size}, On pixels: {count_on_pixels(grid)}")
    print(f"  Expected: {expected_sizes[i+1]}x{expected_sizes[i+1]}")
    print(f"  {'✓ MATCH' if actual_size == expected_sizes[i+1] else '✗ MISMATCH'}")
    print()

print(f"Final answer: {count_on_pixels(grid)} pixels are on")
