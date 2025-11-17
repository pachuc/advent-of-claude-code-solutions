from solution import parse_input, find_shortest_route, calculate_route_distance


def test_example():
    """Test with the example from the problem."""
    print("Test 1: Example input (3 cities)")
    locations, distances = parse_input('test_example.txt')

    print(f"  Locations: {sorted(locations)}")
    print(f"  Number of locations: {len(locations)}")

    min_distance = find_shortest_route(locations, distances)
    print(f"  Minimum distance: {min_distance}")
    print(f"  Expected: 605")
    print(f"  Result: {'PASS' if min_distance == 605 else 'FAIL'}")
    print()


def test_actual_input():
    """Test with the actual input."""
    print("Test 2: Actual input (8 cities)")
    locations, distances = parse_input('input.md')

    print(f"  Locations: {sorted(locations)}")
    print(f"  Number of locations: {len(locations)}")

    # Count distances
    distance_count = 0
    for loc1 in distances:
        for loc2 in distances[loc1]:
            if loc1 < loc2:  # Count each pair once
                distance_count += 1
    print(f"  Number of unique distance pairs: {distance_count}")
    print(f"  Expected: 28 (complete graph: 8 choose 2)")

    # Verify a few specific distances
    print("\n  Sample distance verification:")
    print(f"    Faerun to Norrath: {distances['Faerun']['Norrath']} (expected 129)")
    print(f"    AlphaCentauri to Snowdin: {distances['AlphaCentauri']['Snowdin']} (expected 12)")
    print(f"    Tambi to Straylight: {distances['Tambi']['Straylight']} (expected 70)")

    # Verify bidirectionality
    print("\n  Bidirectionality check:")
    print(f"    Faerun->Norrath: {distances['Faerun']['Norrath']}")
    print(f"    Norrath->Faerun: {distances['Norrath']['Faerun']}")
    print(f"    Bidirectional: {'PASS' if distances['Faerun']['Norrath'] == distances['Norrath']['Faerun'] else 'FAIL'}")

    # Test a specific route calculation
    print("\n  Manual route calculation:")
    test_route = ['Faerun', 'AlphaCentauri', 'Snowdin', 'Tambi', 'Arbre', 'Straylight', 'Norrath', 'Tristram']
    route_distance = calculate_route_distance(test_route, distances)
    print(f"    Route: {' -> '.join(test_route)}")
    expected_manual = 13 + 12 + 15 + 53 + 40 + 54 + 142
    print(f"    Calculated: {route_distance}")
    print(f"    Expected (manual): {expected_manual}")
    print(f"    Result: {'PASS' if route_distance == expected_manual else 'FAIL'}")

    # Find shortest route
    print("\n  Finding shortest route...")
    min_distance = find_shortest_route(locations, distances)
    print(f"  Minimum distance found: {min_distance}")

    # Sanity checks
    max_single_edge = max(distances[loc1][loc2] for loc1 in distances for loc2 in distances[loc1])
    print(f"\n  Sanity checks:")
    print(f"    Max single edge: {max_single_edge}")
    print(f"    Minimum > max single edge: {min_distance > max_single_edge}")
    print(f"    In reasonable range (150-400): {150 <= min_distance <= 400}")
    print()


if __name__ == "__main__":
    test_example()
    test_actual_input()
