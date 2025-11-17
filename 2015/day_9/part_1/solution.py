from itertools import permutations
from collections import defaultdict


def parse_input(filename):
    """Parse the input file to extract locations and distances."""
    locations = set()
    distances = defaultdict(dict)

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse: "Location1 to Location2 = distance"
            parts = line.split(' to ')
            loc1 = parts[0]
            rest = parts[1].split(' = ')
            loc2 = rest[0]
            distance = int(rest[1])

            # Add locations
            locations.add(loc1)
            locations.add(loc2)

            # Store bidirectional distances
            distances[loc1][loc2] = distance
            distances[loc2][loc1] = distance

    return list(locations), distances


def calculate_route_distance(route, distances):
    """Calculate total distance for a given route."""
    total_distance = 0
    for i in range(len(route) - 1):
        current = route[i]
        next_loc = route[i + 1]
        total_distance += distances[current][next_loc]
    return total_distance


def find_shortest_route(locations, distances):
    """Generate all permutations and find the minimum distance."""
    min_distance = float('inf')

    for route in permutations(locations):
        distance = calculate_route_distance(route, distances)
        if distance < min_distance:
            min_distance = distance

    return min_distance


def main():
    # Parse input from 'input.md'
    locations, distances = parse_input('input.md')

    # Find shortest route
    min_distance = find_shortest_route(locations, distances)

    # Print result
    print(min_distance)


if __name__ == "__main__":
    main()
