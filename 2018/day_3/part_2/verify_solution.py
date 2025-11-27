import re
from collections import namedtuple

Claim = namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])

def parse_claim(line):
    pattern = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
    match = re.match(pattern, line.strip())
    if not match:
        raise ValueError(f"Invalid claim format: {line}")
    claim_id, left, top, width, height = map(int, match.groups())
    return Claim(claim_id, left, top, width, height)

def get_fabric_dimensions(claims):
    max_width = max_height = 1000
    for claim in claims:
        max_width = max(max_width, claim.left + claim.width)
        max_height = max(max_height, claim.top + claim.height)
    return max_width, max_height

def create_fabric_grid(width, height):
    return [[0] * width for _ in range(height)]

def mark_claim_on_grid(grid, claim):
    for y in range(claim.top, claim.top + claim.height):
        for x in range(claim.left, claim.left + claim.width):
            grid[y][x] += 1

def is_claim_non_overlapping(grid, claim):
    for y in range(claim.top, claim.top + claim.height):
        for x in range(claim.left, claim.left + claim.width):
            if grid[y][x] != 1:
                return False
    return True

# Read input
with open('input.md', 'r') as f:
    lines = f.readlines()

claims = []
for line in lines:
    line = line.strip()
    if line:
        try:
            claims.append(parse_claim(line))
        except ValueError:
            continue

print(f"Total claims: {len(claims)}")

fabric_width, fabric_height = get_fabric_dimensions(claims)
grid = create_fabric_grid(fabric_width, fabric_height)

for claim in claims:
    mark_claim_on_grid(grid, claim)

# Find all non-overlapping claims (should be exactly 1)
non_overlapping = []
for claim in claims:
    if is_claim_non_overlapping(grid, claim):
        non_overlapping.append(claim.id)

print(f"Non-overlapping claims: {non_overlapping}")
print(f"Count of non-overlapping claims: {len(non_overlapping)}")

# Verify grid consistency with Part 1
overlap_count = sum(1 for row in grid for cell in row if cell >= 2)
print(f"Grid overlap count (should be 107820 from Part 1): {overlap_count}")
