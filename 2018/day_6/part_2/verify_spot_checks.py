#!/usr/bin/env python3
"""
Verification script to manually check specific locations.
"""

# All coordinates from input.md
coordinates = [
    (181, 47), (337, 53), (331, 40), (137, 57), (200, 96),
    (351, 180), (157, 332), (113, 101), (285, 55), (189, 188),
    (174, 254), (339, 81), (143, 61), (131, 155), (239, 334),
    (357, 291), (290, 89), (164, 149), (248, 73), (311, 190),
    (54, 217), (285, 268), (354, 113), (318, 191), (182, 230),
    (156, 252), (114, 232), (159, 299), (324, 280), (152, 155),
    (295, 293), (194, 214), (252, 345), (233, 172), (272, 311),
    (230, 82), (62, 160), (275, 96), (335, 215), (185, 347),
    (134, 272), (58, 113), (112, 155), (220, 83), (153, 244),
    (279, 149), (302, 167), (185, 158), (72, 91), (264, 67)
]

def manhattan_distance(x1, y1, x2, y2):
    """Calculate Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)

def check_location(x, y, threshold=10000):
    """Check if a location is in the safe region."""
    total_dist = sum(manhattan_distance(x, y, cx, cy) for cx, cy in coordinates)
    status = "IN" if total_dist < threshold else "OUT"
    print(f"Location ({x}, {y}): total distance = {total_dist} - {status} of safe region")
    return total_dist

print("=== Manual Spot Checks ===\n")

# Check 1: Center location (should be IN safe region)
print("Check 1: Center location near all coordinates")
check_location(200, 180)
print()

# Check 2: Another center location
print("Check 2: Another center location")
check_location(220, 190)
print()

# Check 3: Far location (should be OUT of safe region)
print("Check 3: Far location (top-left corner)")
check_location(0, 0)
print()

# Check 4: Another far location
print("Check 4: Far location (bottom-right corner)")
check_location(500, 500)
print()

# Check 5: Example location from Part 1 problem (4, 3) with our coordinates
print("Check 5: Location from example (4, 3) - expected total=30 for example coords")
# Note: This is for the example coordinates, not our actual input
example_coords = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]
total = sum(manhattan_distance(4, 3, cx, cy) for cx, cy in example_coords)
status = "IN" if total < 32 else "OUT"
print(f"Location (4, 3) with example coords: total distance = {total} - {status} of safe region (threshold=32)")
print()

# Calculate the centroid of all coordinates
avg_x = sum(x for x, y in coordinates) / len(coordinates)
avg_y = sum(y for x, y in coordinates) / len(coordinates)
print(f"Centroid of all coordinates: ({avg_x:.1f}, {avg_y:.1f})")
check_location(int(avg_x), int(avg_y))
