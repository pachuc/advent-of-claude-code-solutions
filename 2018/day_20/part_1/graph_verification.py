#!/usr/bin/env python3
"""Verify graph structure properties."""

from solution import parse_regex_and_build_graph, build_adjacency_graph, find_max_distance
from collections import deque

def verify_bidirectionality(graph):
    """Verify that all doors are bidirectional."""
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if node not in graph[neighbor]:
                return False, f"Door from {node} to {neighbor} is not bidirectional"
    return True, "All doors are bidirectional"

def verify_connectivity(graph, start=(0, 0)):
    """Verify that all rooms in the graph are reachable from start."""
    if not graph:
        return True, "Empty graph is trivially connected"

    if start not in graph:
        return True, "Start position not in graph (no moves made)"

    # BFS to find all reachable nodes
    queue = deque([start])
    visited = {start}

    while queue:
        pos = queue.popleft()
        for neighbor in graph[pos]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Check if all nodes are reachable
    all_nodes = set(graph.keys())
    unreachable = all_nodes - visited

    if unreachable:
        return False, f"Found {len(unreachable)} unreachable nodes: {list(unreachable)[:5]}"
    return True, f"All {len(all_nodes)} rooms are reachable from start"

def verify_graph_properties(regex):
    """Verify all graph properties for a given regex."""
    print(f"\nVerifying regex: {regex[:60]}{'...' if len(regex) > 60 else ''}")

    # Parse regex
    regex_content = regex.strip()[1:-1]  # Remove ^ and $
    doors = parse_regex_and_build_graph(regex_content)
    graph = build_adjacency_graph(doors)

    print(f"  Doors: {len(doors)}")
    print(f"  Rooms: {len(graph)}")

    # Verify bidirectionality
    passed, msg = verify_bidirectionality(graph)
    print(f"  Bidirectionality: {'✓' if passed else '✗'} {msg}")
    if not passed:
        return False

    # Verify connectivity
    passed, msg = verify_connectivity(graph)
    print(f"  Connectivity: {'✓' if passed else '✗'} {msg}")
    if not passed:
        return False

    # Find max distance
    max_dist = find_max_distance(graph)
    print(f"  Max distance: {max_dist}")

    return True

def main():
    """Run verification on test cases."""
    test_cases = [
        "^WNE$",
        "^ENWWW(NEEE|SSE(EE|N))$",
        "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$",
        "^$",  # Empty
        "^N(E|W)N$",  # Simple branch
    ]

    print("=" * 70)
    print("Graph Structure Verification")
    print("=" * 70)

    all_passed = True
    for regex in test_cases:
        if not verify_graph_properties(regex):
            all_passed = False

    # Test actual input
    print("\nVerifying actual puzzle input...")
    with open('input.md', 'r') as f:
        actual_input = f.read()

    if not verify_graph_properties(actual_input):
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL GRAPH STRUCTURE CHECKS PASSED")
    else:
        print("✗ SOME GRAPH STRUCTURE CHECKS FAILED")
    print("=" * 70)

if __name__ == "__main__":
    main()
