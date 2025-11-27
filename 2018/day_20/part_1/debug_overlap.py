#!/usr/bin/env python3
"""Debug overlapping paths test."""

from solution import parse_regex_and_build_graph, build_adjacency_graph

regex = "^(NNE|NEE)$"
print(f"Testing: {regex}")

# Parse and build graph
regex_content = regex[1:-1]
doors = parse_regex_and_build_graph(regex_content)
graph = build_adjacency_graph(doors)

print(f"\nDoors ({len(doors)}):")
for door in sorted(doors):
    pos1, pos2 = sorted(door)
    print(f"  {pos1} <-> {pos2}")

print(f"\nRooms ({len(graph)}):")
for room in sorted(graph.keys()):
    neighbors = sorted(graph[room])
    print(f"  {room}: {neighbors}")

print("\nPath analysis:")
print("  Path 1 (NNE): (0,0) -> (0,-1) -> (0,-2) -> (1,-2)")
print("  Path 2 (NEE): (0,0) -> (0,-1) -> (1,-1) -> (2,-1)")
print("\n  Doors from Path 1:")
print("    (0,0) <-> (0,-1)")
print("    (0,-1) <-> (0,-2)")
print("    (0,-2) <-> (1,-2)")
print("\n  Doors from Path 2:")
print("    (0,0) <-> (0,-1)  [DUPLICATE - already exists]")
print("    (0,-1) <-> (1,-1)")
print("    (1,-1) <-> (2,-1)")
print("\n  Expected: 5 unique doors (one is shared)")
print("  This is correct!")
