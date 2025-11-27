import re
from collections import namedtuple

# Define the Claim data structure
Claim = namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])


def parse_claim(line):
    """Parse a claim line into components.

    Format: #<ID> @ <left>,<top>: <width>x<height>
    Example: #123 @ 3,2: 5x4

    Returns: Claim namedtuple with (id, left, top, width, height)
    """
    # Use regex to extract all components
    pattern = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
    match = re.match(pattern, line.strip())

    if not match:
        raise ValueError(f"Invalid claim format: {line}")

    # Extract and convert to integers
    claim_id, left, top, width, height = map(int, match.groups())
    return Claim(claim_id, left, top, width, height)


def get_fabric_dimensions(claims):
    """Calculate required fabric dimensions.

    Returns: (max_width, max_height)
    """
    # Start with minimum dimensions of 1000x1000
    max_width = max_height = 1000

    # Expand to accommodate all claims
    for claim in claims:
        max_width = max(max_width, claim.left + claim.width)
        max_height = max(max_height, claim.top + claim.height)

    return max_width, max_height


def create_fabric_grid(width, height):
    """Create a 2D grid initialized to zeros.

    Returns: 2D list where each cell stores count of claims
    """
    return [[0] * width for _ in range(height)]


def mark_claim_on_grid(grid, claim):
    """Mark a claim on the fabric grid.

    For each cell covered by the claim, increment its counter.

    Coordinate system: (0,0) is top-left corner
    - x increases rightward (left coordinate)
    - y increases downward (top coordinate)
    - Claim at (left, top) with (width, height) covers:
      rows from top to (top + height - 1), inclusive
      cols from left to (left + width - 1), inclusive
    """
    for y in range(claim.top, claim.top + claim.height):
        for x in range(claim.left, claim.left + claim.width):
            grid[y][x] += 1


def is_claim_non_overlapping(grid, claim):
    """Check if a claim doesn't overlap with any other claim.

    A claim is non-overlapping if ALL of its cells have a count of exactly 1.

    Returns: True if non-overlapping, False otherwise
    """
    for y in range(claim.top, claim.top + claim.height):
        for x in range(claim.left, claim.left + claim.width):
            if grid[y][x] != 1:
                return False
    return True


def main():
    # 1. Read input file
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # 2. Parse all claims (skip empty lines)
    claims = []
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            try:
                claims.append(parse_claim(line))
            except ValueError as e:
                print(f"Warning: Skipping malformed line: {e}")
                continue

    # 3. Determine required fabric dimensions
    fabric_width, fabric_height = get_fabric_dimensions(claims)

    # 4. Create fabric grid
    grid = create_fabric_grid(fabric_width, fabric_height)

    # 5. Mark all claims on grid
    for claim in claims:
        mark_claim_on_grid(grid, claim)

    # 6. Find the non-overlapping claim
    for claim in claims:
        if is_claim_non_overlapping(grid, claim):
            print(claim.id)
            return

    # If we get here, something went wrong (problem guarantees exactly one)
    print("Error: No non-overlapping claim found")


if __name__ == '__main__':
    main()
