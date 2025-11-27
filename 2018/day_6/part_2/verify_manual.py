#!/usr/bin/env python3
"""Manual verification script for spot-checking specific locations."""

def parse_coordinates(input_file):
    """Parse the input file to extract coordinate pairs."""
    coordinates = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                x, y = line.split(',')
                coordinates.append((int(x.strip()), int(y.strip())))
            except ValueError:
                continue
    return coordinates

def manhattan_distance(x1, y1, x2, y2):
    """Calculate Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)

def check_location(coordinates, location, threshold=10000):
    """Check if a location is in the safe region."""
    x, y = location
    total_distance = sum(manhattan_distance(x, y, cx, cy) for cx, cy in coordinates)
    status = "IN safe region" if total_distance < threshold else "OUT of safe region"
    print(f"Location {location}: total distance = {total_distance:,} ({status})")
    return total_distance

# Load coordinates
coordinates = parse_coordinates('input.md')
print(f"Loaded {len(coordinates)} coordinates")
print()

# Test locations
print("Spot checks:")
print("-" * 60)

# Center locations (should be IN)
check_location(coordinates, (200, 180))
check_location(coordinates, (220, 190))
check_location(coordinates, (217, 175))
print()

# Far locations (should be OUT)
check_location(coordinates, (0, 0))
check_location(coordinates, (500, 500))
print()

# Example from problem statement
print("Example verification (threshold=32):")
print("-" * 60)
example_coords = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]
total = check_location(example_coords, (4, 3), threshold=32)
print(f"Expected: 30, Got: {total}")
