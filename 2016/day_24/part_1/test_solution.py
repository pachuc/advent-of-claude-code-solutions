from solution import parse_grid, calculate_distances, solve_tsp

def test_example():
    """Test with the example from the problem statement."""
    grid = [
        "###########",
        "#0.1.....2#",
        "#.#######.#",
        "#4.......3#",
        "###########"
    ]

    # Parse grid
    locations = parse_grid(grid)
    print(f"Locations found: {locations}")
    assert 0 in locations, "Location 0 not found"
    assert len(locations) == 5, f"Expected 5 locations, found {len(locations)}"

    # Calculate distances
    distances, location_mapping = calculate_distances(grid, locations)

    # Print distance matrix
    print("\nDistance matrix:")
    sorted_locs = sorted(locations.keys())
    print("   ", " ".join(f"{loc:3d}" for loc in sorted_locs))
    for i, loc_i in enumerate(sorted_locs):
        row_str = " ".join(f"{distances[i][j]:3.0f}" if distances[i][j] != float('inf') else "inf"
                          for j in range(len(distances)))
        print(f"{loc_i:2d}: {row_str}")

    # Verify distance matrix symmetry
    for i in range(len(distances)):
        for j in range(len(distances)):
            assert distances[i][j] == distances[j][i], f"Distance matrix not symmetric at ({i}, {j})"

    # Solve TSP
    min_steps = solve_tsp(distances, location_mapping, start_location=0)
    print(f"\nMinimum steps: {min_steps}")

    expected = 14
    if min_steps == expected:
        print(f"✓ Test PASSED! Expected {expected}, got {min_steps}")
    else:
        print(f"✗ Test FAILED! Expected {expected}, got {min_steps}")

    return min_steps == expected


def test_two_locations():
    """Test with just two locations."""
    grid = [
        "#####",
        "#0.1#",
        "#####"
    ]

    locations = parse_grid(grid)
    distances, location_mapping = calculate_distances(grid, locations)
    min_steps = solve_tsp(distances, location_mapping, start_location=0)

    expected = 2
    print(f"\nTwo locations test: {min_steps} steps (expected {expected})")
    assert min_steps == expected, f"Expected {expected}, got {min_steps}"
    print("✓ Two locations test PASSED!")


def test_linear_path():
    """Test with linear path."""
    grid = [
        "#########",
        "#0.1.2.3#",
        "#########"
    ]

    locations = parse_grid(grid)
    distances, location_mapping = calculate_distances(grid, locations)
    min_steps = solve_tsp(distances, location_mapping, start_location=0)

    expected = 6
    print(f"\nLinear path test: {min_steps} steps (expected {expected})")
    assert min_steps == expected, f"Expected {expected}, got {min_steps}"
    print("✓ Linear path test PASSED!")


if __name__ == "__main__":
    print("=" * 60)
    print("Running test: Two locations")
    print("=" * 60)
    test_two_locations()

    print("\n" + "=" * 60)
    print("Running test: Linear path")
    print("=" * 60)
    test_linear_path()

    print("\n" + "=" * 60)
    print("Running test: Example from problem statement")
    print("=" * 60)
    test_example()
