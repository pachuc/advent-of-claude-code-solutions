"""
Disk Defragmentation - Region Counting - Advent of Code 2017 Day 14 Part 2
Count the total number of distinct regions in a 128x128 grid.
"""

from collections import deque

# ============================================================================
# Knot Hash Functions (from Part 1)
# ============================================================================

def initialize_list(size=256):
    """Create initial list from 0 to size-1."""
    return list(range(size))


def reverse_circular(lst, start, length):
    """Reverse a circular section of the list.

    Args:
        lst: The list to modify (in-place)
        start: Starting index for reversal
        length: Number of elements to reverse
    """
    if length <= 1:
        return  # No reversal needed

    n = len(lst)

    # Extract elements circularly
    elements = []
    for i in range(length):
        elements.append(lst[(start + i) % n])

    # Reverse the extracted elements
    elements.reverse()

    # Place them back circularly
    for i in range(length):
        lst[(start + i) % n] = elements[i]


def parse_input_as_ascii(input_string):
    """Parse input string as ASCII codes and append standard suffix.

    Args:
        input_string: The input string to convert

    Returns:
        List of ASCII codes with standard suffix appended
    """
    # Strip whitespace
    clean_input = input_string.strip()

    # Convert to ASCII codes
    ascii_codes = [ord(char) for char in clean_input]

    # Append standard suffix
    suffix = [17, 31, 73, 47, 23]
    ascii_codes.extend(suffix)

    return ascii_codes


def knot_hash_rounds(lengths, num_rounds=64, list_size=256):
    """Execute the knot hash algorithm for multiple rounds.

    Args:
        lengths: List of length values to process
        num_rounds: Number of rounds to execute (default 64)
        list_size: Size of the circular list (default 256)

    Returns:
        The final sparse hash (256-element list) after all rounds
    """
    # Initialize
    lst = initialize_list(list_size)
    current_position = 0
    skip_size = 0

    # Run multiple rounds
    for round_num in range(num_rounds):
        for length in lengths:
            # Reverse section
            reverse_circular(lst, current_position, length)

            # Update position (with wrapping)
            current_position = (current_position + length + skip_size) % list_size

            # Increment skip size
            skip_size += 1

    return lst


def create_dense_hash(sparse_hash):
    """Convert 256-element sparse hash to 16-element dense hash via XOR.

    Args:
        sparse_hash: 256-element list

    Returns:
        16-element list where each element is XOR of 16 sparse hash elements
    """
    dense_hash = []
    for i in range(16):
        block = sparse_hash[i*16:(i+1)*16]
        # XOR all elements in the block
        xor_result = block[0]
        for j in range(1, 16):
            xor_result ^= block[j]
        dense_hash.append(xor_result)
    return dense_hash


def to_hex_string(dense_hash):
    """Convert dense hash to 32-character hexadecimal string.

    Args:
        dense_hash: 16-element list of integers (0-255)

    Returns:
        32-character lowercase hexadecimal string
    """
    hex_string = ''.join(format(num, '02x') for num in dense_hash)
    return hex_string


def compute_knot_hash(input_string):
    """Compute the complete Knot Hash of an input string.

    Args:
        input_string: The string to hash

    Returns:
        32-character hexadecimal hash string
    """
    # Step 1: Parse and convert to ASCII
    lengths = parse_input_as_ascii(input_string)

    # Step 2: Run 64 rounds
    sparse_hash = knot_hash_rounds(lengths, num_rounds=64)

    # Step 3: Create dense hash
    dense_hash = create_dense_hash(sparse_hash)

    # Step 4: Convert to hex
    hex_hash = to_hex_string(dense_hash)

    return hex_hash


# ============================================================================
# Grid Generation Functions (from Part 1)
# ============================================================================

def hex_to_binary(hex_string):
    """Convert hexadecimal string to binary string.

    Args:
        hex_string: Hexadecimal string

    Returns:
        Binary string with 4 bits per hex character
    """
    return ''.join(format(int(c, 16), '04b') for c in hex_string)


def generate_row_input(key, row_number):
    """Generate input string for a specific row.

    Args:
        key: The key string
        row_number: Row number (0-127)

    Returns:
        Formatted string "{key}-{row_number}"
    """
    return f"{key}-{row_number}"


def generate_grid(key):
    """Generate the 128x128 binary grid.

    Args:
        key: The key string

    Returns:
        List of 128 strings, each containing 128 binary characters
    """
    grid = []
    for row in range(128):
        row_input = generate_row_input(key, row)
        hash_hex = compute_knot_hash(row_input)
        hash_binary = hex_to_binary(hash_hex)
        grid.append(hash_binary)
    return grid


# ============================================================================
# Part 2: Region Counting Functions
# ============================================================================

def flood_fill_bfs(grid, start_row, start_col, visited):
    """Mark all cells in a connected region as visited using BFS.

    Args:
        grid: Grid (list of strings)
        start_row: Starting row coordinate
        start_col: Starting column coordinate
        visited: Set of visited coordinates (modified in-place)
    """
    # Get grid dimensions
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    queue = deque([(start_row, start_col)])
    visited.add((start_row, start_col))

    while queue:
        row, col = queue.popleft()

        # Check all 4 orthogonal neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc

            # Check bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                # Check if used and not visited
                if (new_row, new_col) not in visited:
                    if grid[new_row][new_col] == '1':
                        visited.add((new_row, new_col))
                        queue.append((new_row, new_col))


def count_regions(grid):
    """Count the total number of distinct regions in the grid.

    Args:
        grid: Grid (list of strings)

    Returns:
        Total number of regions
    """
    visited = set()
    region_count = 0

    # Get grid dimensions
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for row in range(rows):
        for col in range(cols):
            # Check if cell is used and not yet visited
            if grid[row][col] == '1' and (row, col) not in visited:
                # Found a new region
                region_count += 1
                # Mark all cells in this region as visited
                flood_fill_bfs(grid, row, col, visited)

    return region_count


def solve_part2(key):
    """Solve Part 2: Count regions in the grid.

    Args:
        key: The key string

    Returns:
        Total number of regions
    """
    # Step 1: Generate grid (reuse from Part 1)
    grid = generate_grid(key)

    # Validation: Verify grid matches Part 1 expectations
    if key == 'jxqlasbh':
        total_used = sum(row.count('1') for row in grid)
        assert total_used == 8140, f"Grid mismatch: expected 8140 used squares, got {total_used}"

    # Step 2: Count regions
    region_count = count_regions(grid)

    # Sanity check: regions must be between 1 and total used squares
    total_used = sum(row.count('1') for row in grid)
    if total_used > 0:
        assert 1 <= region_count <= total_used, f"Invalid region count: {region_count}"

    return region_count


# ============================================================================
# Test Functions
# ============================================================================

def test_flood_fill_single_cell():
    """Test flood fill on isolated single cell"""
    grid = [
        '000',
        '010',
        '000'
    ]
    visited = set()
    flood_fill_bfs(grid, 1, 1, visited)

    assert (1, 1) in visited, "Center cell should be visited"
    assert len(visited) == 1, f"Expected 1 visited cell, got {len(visited)}"
    print("  ✓ Single cell test passed")


def test_flood_fill_no_diagonal():
    """Verify diagonal cells are NOT treated as connected"""
    grid = [
        '101',
        '010',
        '101'
    ]
    visited = set()
    flood_fill_bfs(grid, 1, 1, visited)

    # Only center cell should be in this region
    assert len(visited) == 1, f"Expected 1 visited cell, got {len(visited)}"
    assert visited == {(1, 1)}, f"Only center should be visited: {visited}"
    print("  ✓ No diagonal connection test passed")


def test_count_regions_empty():
    """Test grid with no used squares"""
    grid = ['0' * 128 for _ in range(128)]
    count = count_regions(grid)
    assert count == 0, f"Expected 0 regions, got {count}"
    print("  ✓ Empty grid test passed")


def test_count_regions_full():
    """Test grid completely filled"""
    grid = ['1' * 128 for _ in range(128)]
    count = count_regions(grid)
    assert count == 1, f"Expected 1 region (all connected), got {count}"
    print("  ✓ Full grid test passed")


def test_count_regions_multiple():
    """Test grid with several separate regions"""
    grid = [
        '1100110',
        '1100110',
        '0000000',
        '0111000',
        '0111000',
        '0000011',
        '0000011'
    ]
    count = count_regions(grid)
    # Should find 4 distinct regions
    assert count == 4, f"Expected 4 regions, got {count}"
    print("  ✓ Multiple regions test passed")


def test_example_key():
    """Test with known example"""
    result = solve_part2('flqrgnkx')
    expected = 1242
    assert result == expected, f"Expected {expected} regions, got {result}"
    print(f"  ✓ Example key test passed: {result} regions")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main function to compute the solution."""
    # Read input
    with open('input.md', 'r') as f:
        key = f.read().strip()

    # Solve
    result = solve_part2(key)

    # Output
    print(result)
    return result


if __name__ == "__main__":
    print("Running tests...\n")

    print("Unit tests:")
    test_flood_fill_single_cell()
    test_flood_fill_no_diagonal()
    test_count_regions_empty()
    test_count_regions_full()
    test_count_regions_multiple()

    print("\nIntegration test:")
    test_example_key()

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)

    print("\nComputing answer for actual input...")
    result = main()

    print(f"\nFINAL ANSWER: {result}")
