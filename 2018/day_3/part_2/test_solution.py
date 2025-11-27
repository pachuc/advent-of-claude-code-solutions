import re
from collections import namedtuple

# Define the Claim data structure
Claim = namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])

def parse_claim(line):
    """Parse a claim line into components."""
    pattern = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
    match = re.match(pattern, line.strip())
    if not match:
        raise ValueError(f"Invalid claim format: {line}")
    claim_id, left, top, width, height = map(int, match.groups())
    return Claim(claim_id, left, top, width, height)

def get_fabric_dimensions(claims):
    """Calculate required fabric dimensions."""
    max_width = max_height = 1000
    for claim in claims:
        max_width = max(max_width, claim.left + claim.width)
        max_height = max(max_height, claim.top + claim.height)
    return max_width, max_height

def create_fabric_grid(width, height):
    """Create a 2D grid initialized to zeros."""
    return [[0] * width for _ in range(height)]

def mark_claim_on_grid(grid, claim):
    """Mark a claim on the fabric grid."""
    for y in range(claim.top, claim.top + claim.height):
        for x in range(claim.left, claim.left + claim.width):
            grid[y][x] += 1

def is_claim_non_overlapping(grid, claim):
    """Check if a claim doesn't overlap with any other claim."""
    for y in range(claim.top, claim.top + claim.height):
        for x in range(claim.left, claim.left + claim.width):
            if grid[y][x] != 1:
                return False
    return True

# Read test example
with open('test_example.txt', 'r') as f:
    lines = f.readlines()

claims = []
for line in lines:
    line = line.strip()
    if line:
        claims.append(parse_claim(line))

fabric_width, fabric_height = get_fabric_dimensions(claims)
grid = create_fabric_grid(fabric_width, fabric_height)

for claim in claims:
    mark_claim_on_grid(grid, claim)

for claim in claims:
    if is_claim_non_overlapping(grid, claim):
        print(claim.id)
        break
