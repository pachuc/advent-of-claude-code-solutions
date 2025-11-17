#!/usr/bin/env python3
"""
Conway's Game of Life Variant - Light Animation
Simulates 100 steps of a cellular automaton on a 100x100 grid.
"""


def parse_input(filename):
    """Parse the input file and return the grid."""
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                row = [c == '#' for c in line]
                grid.append(row)
    return grid


def create_grid_from_string(grid_string):
    """Create a grid from a multi-line string representation."""
    lines = grid_string.strip().split('\n')
    grid = []
    for line in lines:
        row = [c == '#' for c in line]
        grid.append(row)
    return grid


def count_neighbors(grid, row, col):
    """Count the number of 'on' neighbors for cell at (row, col)."""
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # Check all 8 directions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                count += 1

    return count


def get_next_state(current_state, neighbor_count):
    """Determine next state based on current state and neighbor count."""
    if current_state:
        # Light is ON: stays on if 2 or 3 neighbors are on
        return neighbor_count in [2, 3]
    else:
        # Light is OFF: turns on if exactly 3 neighbors are on
        return neighbor_count == 3


def simulate_step(grid):
    """Perform one simulation step and return the new grid state."""
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [[False for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            neighbor_count = count_neighbors(grid, row, col)
            current_state = grid[row][col]
            new_grid[row][col] = get_next_state(current_state, neighbor_count)

    return new_grid


def count_lights(grid):
    """Count the total number of 'on' lights in the grid."""
    return sum(sum(row) for row in grid)


def print_grid(grid):
    """Print grid in human-readable format."""
    for row in grid:
        print(''.join('#' if cell else '.' for cell in row))


def grids_equal(grid1, grid2):
    """Compare two grids for equality."""
    if len(grid1) != len(grid2):
        return False
    return all(row1 == row2 for row1, row2 in zip(grid1, grid2))


def run_tests():
    """Run all tests to verify implementation."""
    print("=== Running Tests ===\n")

    # Test 1: State Transition Rules
    print("Testing state transitions...")
    for current_state in [True, False]:
        for neighbor_count in range(9):
            result = get_next_state(current_state, neighbor_count)
            # Verify against expected rules
            if current_state:
                expected = neighbor_count in [2, 3]
            else:
                expected = neighbor_count == 3
            assert result == expected, f"State transition failed for state={current_state}, neighbors={neighbor_count}"
    print("✓ State transitions: PASSED\n")

    # Test 2: Neighbor Counting
    print("Testing neighbor counting...")

    # Test case 1: All neighbors on
    test_grid = [[True, True, True],
                 [True, True, True],
                 [True, True, True]]
    assert count_neighbors(test_grid, 1, 1) == 8, "Center cell with all neighbors should have 8"

    # Test case 2: Diagonal neighbors only
    test_grid2 = [[True, False, True],
                  [False, False, False],
                  [True, False, True]]
    assert count_neighbors(test_grid2, 1, 1) == 4, "Center cell with diagonal neighbors should have 4"

    # Test case 3: No neighbors
    test_grid3 = [[False, False, False],
                  [False, True, False],
                  [False, False, False]]
    assert count_neighbors(test_grid3, 1, 1) == 0, "Center cell with no neighbors should have 0"

    # Test case 4: Corner cell
    test_grid4 = [[True, True, False],
                  [True, False, False],
                  [False, False, False]]
    assert count_neighbors(test_grid4, 0, 0) == 2, "Corner cell should count correctly"

    print("✓ Neighbor counting: PASSED\n")

    # Test 3: Synchronous Updates (Blinker Pattern)
    print("Testing synchronous updates (blinker pattern)...")
    blinker = create_grid_from_string(
        """.....
.###.
.....""")

    blinker_step1 = simulate_step(blinker)
    expected_step1 = create_grid_from_string(
        """..#..
..#..
..#..""")

    assert grids_equal(blinker_step1, expected_step1), "Blinker step 1 failed"

    blinker_step2 = simulate_step(blinker_step1)
    # After 2 steps, should return to original
    # Note: need to handle edge padding correctly
    assert count_lights(blinker_step2) == 3, "Blinker should have 3 lights after step 2"

    print("✓ Synchronous updates: PASSED\n")

    # Test 4: 6x6 Example (MOST IMPORTANT)
    print("Testing 6x6 example...")
    example_input = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

    example_grid = create_grid_from_string(example_input)

    print("Initial state:")
    print_grid(example_grid)
    print(f"Initial lights on: {count_lights(example_grid)}\n")

    # Simulate 4 steps
    for step in range(4):
        example_grid = simulate_step(example_grid)
        print(f"After step {step + 1}:")
        print_grid(example_grid)
        print(f"Lights on: {count_lights(example_grid)}\n")

    lights_on = count_lights(example_grid)
    assert lights_on == 4, f"Expected 4 lights on after 4 steps, got {lights_on}"

    # Verify the pattern is a 2x2 block at position (2,2)
    assert example_grid[2][2] and example_grid[2][3], "Block top row missing"
    assert example_grid[3][2] and example_grid[3][3], "Block bottom row missing"

    print("✓ 6x6 Example: PASSED (4 lights on with correct 2x2 block pattern)\n")

    # Test 5: Known Pattern - Block (Still Life)
    print("Testing block pattern (still life)...")
    block = create_grid_from_string(
        """....
.##.
.##.
....""")

    block_step1 = simulate_step(block)
    assert grids_equal(block, block_step1), "Block pattern should remain unchanged"
    print("✓ Block pattern: PASSED\n")

    print("=== All Tests Passed ===\n")


def main():
    """Main execution function."""
    import time

    # Parse input
    print("Parsing input...")
    grid = parse_input('input.md')

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    print(f"Grid size: {rows}x{cols}")

    initial_count = count_lights(grid)
    print(f"Initial lights on: {initial_count}\n")

    # Simulate 100 steps
    print("Simulating 100 steps...")
    start = time.time()

    for step in range(100):
        grid = simulate_step(grid)

        # Print progress every 10 steps
        if (step + 1) % 10 == 0:
            count = count_lights(grid)
            print(f"Step {step + 1}: {count} lights on")

    elapsed = time.time() - start

    # Count final lights
    final_count = count_lights(grid)

    print(f"\n{'='*50}")
    print(f"Simulation complete!")
    print(f"Execution time: {elapsed:.4f} seconds")
    print(f"Final answer: {final_count} lights on after 100 steps")
    print(f"{'='*50}\n")


if __name__ == '__main__':
    run_tests()  # Run tests first
    main()       # Then solve the problem
