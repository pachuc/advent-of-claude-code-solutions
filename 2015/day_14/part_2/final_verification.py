import solution

def verify_final_solution():
    """Verify the final solution with detailed output."""
    # Parse input
    reindeer_data = solution.parse_input('input.md')
    reindeer_list = solution.initialize_reindeer(reindeer_data)

    print("=" * 70)
    print("Reindeer Racing Simulation - Point-Based Scoring")
    print("=" * 70)
    print(f"\nSimulating race with {len(reindeer_list)} reindeer for 2503 seconds...\n")

    # Run simulation for 2503 seconds
    for second in range(1, 2504):
        # Update all reindeer positions
        for reindeer in reindeer_list:
            solution.update_reindeer_position(reindeer)

        # Find leaders
        leaders = solution.find_leaders(reindeer_list)

        # Award points to leaders
        for leader in leaders:
            leader['points'] += 1

    # Sort by points (descending)
    reindeer_list.sort(key=lambda r: r['points'], reverse=True)

    # Display results
    print("Final Results after 2503 seconds:")
    print("-" * 70)
    print(f"{'Rank':<6} {'Name':<10} {'Distance (km)':<15} {'Points':<10}")
    print("-" * 70)

    for i, reindeer in enumerate(reindeer_list, 1):
        print(f"{i:<6} {reindeer['name']:<10} {reindeer['distance']:<15} {reindeer['points']:<10}")

    print("-" * 70)

    # Winner
    winner = reindeer_list[0]
    print(f"\nWinner: {winner['name']} with {winner['points']} points!")

    # Validation checks
    print("\n" + "=" * 70)
    print("Validation Checks:")
    print("=" * 70)

    total_points = sum(r['points'] for r in reindeer_list)
    print(f"✓ Total points awarded: {total_points}")
    print(f"  (Should be >= 2503, more if there were ties)")

    max_points = max(r['points'] for r in reindeer_list)
    print(f"✓ Maximum points: {max_points}")
    print(f"  (Should be <= 2503)")

    all_positive_distance = all(r['distance'] > 0 for r in reindeer_list)
    print(f"✓ All reindeer have positive distance: {all_positive_distance}")

    all_non_negative_points = all(r['points'] >= 0 for r in reindeer_list)
    print(f"✓ All reindeer have non-negative points: {all_non_negative_points}")

    print("\n" + "=" * 70)
    print(f"FINAL ANSWER: {winner['points']}")
    print("=" * 70)

    return winner['points']

if __name__ == '__main__':
    verify_final_solution()
