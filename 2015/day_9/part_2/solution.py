from itertools import permutations

def parse_input(filename):
    """Parse input file and return locations set and distances dict"""
    locations = set()
    distances = {}

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse format: "Location1 to Location2 = Distance"
            parts = line.split(' to ')
            loc1 = parts[0].strip()

            right_parts = parts[1].split(' = ')
            loc2 = right_parts[0].strip()
            distance = int(right_parts[1].strip())

            locations.add(loc1)
            locations.add(loc2)

            # Store bidirectional
            distances[(loc1, loc2)] = distance
            distances[(loc2, loc1)] = distance

    return locations, distances

def calculate_route_distance(route, distances):
    """Calculate total distance for a given route"""
    total = 0
    for i in range(len(route) - 1):
        total += distances[(route[i], route[i+1])]
    return total

def find_longest_route(locations, distances):
    """Find the longest route through all locations"""
    max_distance = max(
        calculate_route_distance(route, distances)
        for route in permutations(locations)
    )
    return max_distance

def main():
    locations, distances = parse_input('input.md')
    result = find_longest_route(locations, distances)
    print(result)

if __name__ == '__main__':
    main()
