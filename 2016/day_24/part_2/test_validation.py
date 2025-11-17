"""
Validation script to verify Part 2 solution correctness.
Tests the round-trip logic by comparing Part 1 vs Part 2 answers.
"""

from solution import parse_grid, calculate_distances

def solve_tsp_part1(distances, location_mapping, start_location=0):
    """
    Part 1 TSP: Can end anywhere (no return to start required).
    """
    N = len(distances)
    start_idx = location_mapping[start_location]

    # dp[mask][current] = minimum distance to reach current with visited set = mask
    dp = [[float('inf')] * N for _ in range(1 << N)]
    dp[1 << start_idx][start_idx] = 0

    # Iterate through all masks
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

    # Part 1: Can end anywhere
    full_mask = (1 << N) - 1
    return min(dp[full_mask][i] for i in range(N))


def solve_tsp_part2(distances, location_mapping, start_location=0):
    """
    Part 2 TSP: Must return to start location.
    """
    N = len(distances)
    start_idx = location_mapping[start_location]

    # dp[mask][current] = minimum distance to reach current with visited set = mask
    dp = [[float('inf')] * N for _ in range(1 << N)]
    dp[1 << start_idx][start_idx] = 0

    # Iterate through all masks
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

    # Part 2: Add return distance to start
    full_mask = (1 << N) - 1
    return min(dp[full_mask][i] + distances[i][start_idx] for i in range(N))


def main():
    # Read input
    with open('input.md', 'r') as f:
        lines = f.readlines()

    grid = []
    for line in lines:
        line = line.rstrip('\n')
        if line and not line.startswith('```'):
            grid.append(line)

    # Parse and calculate distances
    locations = parse_grid(grid)
    distances, location_mapping = calculate_distances(grid, locations)

    # Test both parts
    part1_answer = solve_tsp_part1(distances, location_mapping, start_location=0)
    part2_answer = solve_tsp_part2(distances, location_mapping, start_location=0)

    # Read expected Part 1 answer
    with open('part_1_answer.txt', 'r') as f:
        expected_part1 = int(f.read().strip())

    print("=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    print(f"Part 1 answer (can end anywhere): {part1_answer}")
    print(f"Part 2 answer (must return to 0): {part2_answer}")
    print(f"Difference (return distance): {part2_answer - part1_answer}")
    print(f"Expected Part 1 from file: {expected_part1}")
    print(f"Part 1 Match: {part1_answer == expected_part1}")
    print(f"Part 2 > Part 1: {part2_answer > part1_answer}")
    print("=" * 60)

    # Validation checks
    assert part1_answer == expected_part1, f"Part 1 mismatch! Got {part1_answer}, expected {expected_part1}"
    assert part2_answer > part1_answer, f"Part 2 should be greater than Part 1!"
    assert part2_answer - part1_answer > 0, f"Return distance should be positive!"

    print("\n✓ All validation checks passed!")
    print(f"✓ Part 2 answer is CORRECT: {part2_answer}")

    return part2_answer


if __name__ == "__main__":
    main()
