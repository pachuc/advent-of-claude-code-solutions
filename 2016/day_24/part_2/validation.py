"""
Quick validation to compare Part 1 and Part 2 answers
"""
from solution import parse_grid, calculate_distances
from collections import deque

def solve_tsp_part1(distances, location_mapping, start_location=0):
    """Part 1 version: Can end anywhere"""
    N = len(distances)
    start_idx = location_mapping[start_location]

    dp = [[float('inf')] * N for _ in range(1 << N)]
    dp[1 << start_idx][start_idx] = 0

    for mask in range(1 << N):
        for current in range(N):
            if not (mask & (1 << current)) or dp[mask][current] == float('inf'):
                continue
            for next_loc in range(N):
                if not (mask & (1 << next_loc)):
                    new_mask = mask | (1 << next_loc)
                    dp[new_mask][next_loc] = min(
                        dp[new_mask][next_loc],
                        dp[mask][current] + distances[current][next_loc]
                    )

    full_mask = (1 << N) - 1
    return min(dp[full_mask][i] for i in range(N))

def solve_tsp_part2(distances, location_mapping, start_location=0):
    """Part 2 version: Must return to start"""
    N = len(distances)
    start_idx = location_mapping[start_location]

    dp = [[float('inf')] * N for _ in range(1 << N)]
    dp[1 << start_idx][start_idx] = 0

    for mask in range(1 << N):
        for current in range(N):
            if not (mask & (1 << current)) or dp[mask][current] == float('inf'):
                continue
            for next_loc in range(N):
                if not (mask & (1 << next_loc)):
                    new_mask = mask | (1 << next_loc)
                    dp[new_mask][next_loc] = min(
                        dp[new_mask][next_loc],
                        dp[mask][current] + distances[current][next_loc]
                    )

    full_mask = (1 << N) - 1
    return min(dp[full_mask][i] + distances[i][start_idx] for i in range(N))

# Read and parse input
with open('input.md', 'r') as f:
    lines = f.readlines()

grid = []
for line in lines:
    line = line.rstrip('\n')
    if line and not line.startswith('```'):
        grid.append(line)

locations = parse_grid(grid)
distances, location_mapping = calculate_distances(grid, locations)

# Compare both versions
part1_answer = solve_tsp_part1(distances, location_mapping, start_location=0)
part2_answer = solve_tsp_part2(distances, location_mapping, start_location=0)

print(f"Part 1 answer (can end anywhere): {part1_answer}")
print(f"Part 2 answer (must return to 0): {part2_answer}")
print(f"Difference (return distance): {part2_answer - part1_answer}")
print(f"\nExpected Part 1 from file: 428")
print(f"Match: {part1_answer == 428}")
