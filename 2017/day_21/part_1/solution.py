def pattern_to_grid(pattern_str):
    """Convert slash-separated pattern string to list of strings."""
    return pattern_str.split('/')


def grid_to_pattern(grid):
    """Convert list of strings back to slash-separated pattern."""
    return '/'.join(grid)


def rotate_grid(grid):
    """Rotate a grid 90 degrees clockwise."""
    n = len(grid)
    rotated = []
    for i in range(n):
        row = ''
        for j in range(n - 1, -1, -1):
            row += grid[j][i]
        rotated.append(row)
    return rotated


def flip_grid(grid):
    """Flip a grid horizontally (reverse each row)."""
    return [row[::-1] for row in grid]


def generate_all_orientations(pattern_str):
    """Generate all 8 possible orientations (rotations and flips) of a pattern."""
    grid = pattern_to_grid(pattern_str)
    orientations = set()

    # Add 4 rotations
    current = grid
    for _ in range(4):
        orientations.add(grid_to_pattern(current))
        current = rotate_grid(current)

    # Flip and add 4 more rotations
    flipped = flip_grid(grid)
    current = flipped
    for _ in range(4):
        orientations.add(grid_to_pattern(current))
        current = rotate_grid(current)

    return orientations


def parse_rules(input_text):
    """Parse enhancement rules and generate all orientations for pattern matching."""
    rules = {}
    for line in input_text.strip().split('\n'):
        if not line.strip():
            continue
        input_pattern, output_pattern = line.split(' => ')

        # Generate all orientations of the input pattern
        orientations = generate_all_orientations(input_pattern)

        # Map each orientation to the same output
        for orientation in orientations:
            rules[orientation] = output_pattern

    return rules


def divide_grid(grid, block_size):
    """Divide grid into blocks of given size."""
    grid_size = len(grid)
    num_blocks = grid_size // block_size
    blocks = []

    for block_row in range(num_blocks):
        block_row_list = []
        for block_col in range(num_blocks):
            block = []
            for r in range(block_row * block_size, (block_row + 1) * block_size):
                row_section = grid[r][block_col * block_size:(block_col + 1) * block_size]
                block.append(row_section)
            block_row_list.append(block)
        blocks.append(block_row_list)

    return blocks


def enhance_block(block, rules):
    """Enhance a single block using the rules."""
    pattern = grid_to_pattern(block)

    if pattern not in rules:
        raise KeyError(f"Pattern not found in rules: {pattern}")

    output_pattern = rules[pattern]
    return pattern_to_grid(output_pattern)


def reassemble_grid(enhanced_blocks):
    """Reassemble enhanced blocks back into a single grid."""
    result = []

    for block_row in enhanced_blocks:
        # Get the height of blocks in this row
        block_height = len(block_row[0])

        # For each row within the blocks
        for row_idx in range(block_height):
            row = ''
            # Concatenate corresponding rows from all blocks in this block-row
            for block in block_row:
                row += block[row_idx]
            result.append(row)

    return result


def perform_iterations(initial_grid, rules, num_iterations):
    """Perform the specified number of enhancement iterations."""
    grid = initial_grid

    for iteration in range(num_iterations):
        grid_size = len(grid)

        # Determine block size
        if grid_size % 2 == 0:
            block_size = 2
        else:
            block_size = 3

        # Divide, enhance, and reassemble
        blocks = divide_grid(grid, block_size)
        enhanced_blocks = []

        for block_row in blocks:
            enhanced_row = []
            for block in block_row:
                enhanced = enhance_block(block, rules)
                enhanced_row.append(enhanced)
            enhanced_blocks.append(enhanced_row)

        grid = reassemble_grid(enhanced_blocks)

    return grid


def count_on_pixels(grid):
    """Count the number of '#' pixels in the grid."""
    count = 0
    for row in grid:
        count += row.count('#')
    return count


def main():
    # Read input from file
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse rules
    rules = parse_rules(input_text)

    # Initialize starting grid
    initial_grid = ['.#.', '..#', '###']

    # Perform 5 iterations
    final_grid = perform_iterations(initial_grid, rules, 5)

    # Count on pixels
    result = count_on_pixels(final_grid)

    print(result)


if __name__ == '__main__':
    main()
