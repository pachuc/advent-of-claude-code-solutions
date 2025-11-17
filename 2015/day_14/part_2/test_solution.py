import solution

def test_1000_second_example():
    """Test the 1000-second example from the problem."""
    # Create test data for Dancer and Comet
    test_data = [
        ('Dancer', 27, 5, 132),
        ('Comet', 18, 6, 103)
    ]

    reindeer_list = solution.initialize_reindeer(test_data)

    # Run simulation for 1000 seconds
    for second in range(1, 1001):
        for reindeer in reindeer_list:
            solution.update_reindeer_position(reindeer)

        leaders = solution.find_leaders(reindeer_list)

        for leader in leaders:
            leader['points'] += 1

    # Print results
    for reindeer in reindeer_list:
        print(f"{reindeer['name']}: {reindeer['distance']} km, {reindeer['points']} points")

    # Verify against expected results
    dancer = reindeer_list[0]
    comet = reindeer_list[1]

    print(f"\nExpected: Dancer=1120 km, 689 points")
    print(f"Actual: Dancer={dancer['distance']} km, {dancer['points']} points")
    print(f"\nExpected: Comet=1056 km, 312 points")
    print(f"Actual: Comet={comet['distance']} km, {comet['points']} points")

    # Verify
    assert dancer['distance'] == 1120, f"Dancer distance mismatch: {dancer['distance']}"
    assert dancer['points'] == 689, f"Dancer points mismatch: {dancer['points']}"
    assert comet['distance'] == 1056, f"Comet distance mismatch: {comet['distance']}"
    assert comet['points'] == 312, f"Comet points mismatch: {comet['points']}"

    print("\n✓ 1000-second example test passed!")

def test_parsing():
    """Test that all reindeer are parsed correctly."""
    reindeer_data = solution.parse_input('input.md')
    print(f"\nParsed {len(reindeer_data)} reindeer:")
    for name, speed, fly_time, rest_time in reindeer_data:
        print(f"  {name}: {speed} km/s for {fly_time}s, rest {rest_time}s")

    assert len(reindeer_data) == 9, f"Expected 9 reindeer, got {len(reindeer_data)}"
    print("\n✓ Parsing test passed!")

def test_first_second():
    """Test behavior at the first second."""
    reindeer_data = solution.parse_input('input.md')
    reindeer_list = solution.initialize_reindeer(reindeer_data)

    # Simulate first second
    for reindeer in reindeer_list:
        solution.update_reindeer_position(reindeer)

    leaders = solution.find_leaders(reindeer_list)

    for leader in leaders:
        leader['points'] += 1

    print(f"\nAfter first second:")
    print(f"  Number of leaders: {len(leaders)}")
    print(f"  Total points awarded: {sum(r['points'] for r in reindeer_list)}")

    # At second 1, all should have moved and be in the lead (tied)
    for reindeer in reindeer_list:
        print(f"  {reindeer['name']}: {reindeer['distance']} km, {reindeer['points']} points")

    print("\n✓ First second test completed!")

if __name__ == '__main__':
    print("=" * 60)
    print("Running tests...")
    print("=" * 60)

    test_parsing()
    test_first_second()
    test_1000_second_example()

    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
