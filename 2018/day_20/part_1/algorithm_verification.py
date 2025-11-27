#!/usr/bin/env python3
"""Verify BFS shortest path algorithm correctness."""

from solution import solve, parse_regex_and_build_graph, build_adjacency_graph, find_max_distance
from collections import deque

def verify_bfs_shortest_path():
    """
    Verify BFS finds the shortest path when multiple routes exist to the same room.

    Test case: ^EE(SS|WSSEE)$
      - Room (2, 2) is reachable via:
        - Path 1: EESS: 4 doors from origin
        - Path 2: EEWSSEE: 6 doors from origin
      - BFS should record distance 4 for (2, 2), not 6
    """
    regex = "^EE(SS|WSSEE)$"
    print(f"Testing BFS shortest path property with: {regex}")

    # Parse and build graph
    regex_content = regex[1:-1]
    doors = parse_regex_and_build_graph(regex_content)
    graph = build_adjacency_graph(doors)

    # Manually compute distances
    start = (0, 0)
    queue = deque([(start, 0)])
    visited = {start: 0}

    while queue:
        pos, dist = queue.popleft()
        for neighbor in graph[pos]:
            if neighbor not in visited:
                visited[neighbor] = dist + 1
                queue.append((neighbor, dist + 1))

    # Check that (2, 2) has the shortest distance
    target = (2, 2)
    if target in visited:
        distance_to_target = visited[target]
        print(f"  Distance to {target}: {distance_to_target}")

        # The shortest path is EESS (4 doors)
        if distance_to_target == 4:
            print("  ✓ BFS correctly found shortest path (4 doors)")
            return True
        else:
            print(f"  ✗ BFS found distance {distance_to_target}, expected 4")
            return False
    else:
        print(f"  ✗ Room {target} not found in graph")
        return False

def verify_path_overlap():
    """
    Verify that overlapping paths share rooms correctly.

    Test case: ^(NNE|NEE)$
      - Both paths should reach different endpoints
      - But they may share some rooms
    """
    regex = "^(NNE|NEE)$"
    print(f"\nTesting overlapping paths with: {regex}")

    # Parse and build graph
    regex_content = regex[1:-1]
    doors = parse_regex_and_build_graph(regex_content)
    graph = build_adjacency_graph(doors)

    print(f"  Total doors: {len(doors)}")
    print(f"  Total rooms: {len(graph)}")

    # Both paths create 3 doors each, but share one door
    # Path 1: N, N, E -> (0,0) -> (0,-1) -> (0,-2) -> (1,-2)
    # Path 2: N, E, E -> (0,0) -> (0,-1) -> (1,-1) -> (2,-1)
    # Shared door: (0,0) <-> (0,-1)

    # Expected rooms: (0,0), (0,-1), (0,-2), (1,-2), (1,-1), (2,-1) = 6 rooms
    # Expected doors: 3 + 3 - 1 shared = 5 unique doors

    if len(doors) == 5 and len(graph) == 6:
        print("  ✓ Overlapping paths handled correctly")
        return True
    else:
        print(f"  ✗ Expected 5 doors and 6 rooms, got {len(doors)} doors and {len(graph)} rooms")
        return False

def verify_empty_branch_handling():
    """
    Verify that empty branches are handled correctly.

    Test case: ^N(EW|)S$
      - Should create two paths: NEWS and NS
    """
    regex = "^N(EW|)S$"
    print(f"\nTesting empty branch with: {regex}")

    result = solve(regex)

    # Path 1: NEWS = 4 doors, ends at (0, 0)
    # Path 2: NS = 2 doors, ends at (0, 0)
    # Max distance should be 2 (from the furthest point reached)
    # Actually, let me trace this more carefully:
    # - Start at (0, 0)
    # - N -> (0, -1)
    # - Branch:
    #   - Path 1: E -> (1, -1), W -> (0, -1)
    #   - Path 2: nothing
    # - Both paths continue from (0, -1) (path 1) and (0, -1) (path 2)
    # - S -> (0, 0)
    # Max distance: furthest from origin is (1, -1) which is 2 doors away

    print(f"  Result: {result}")
    if result == 2:
        print("  ✓ Empty branch handled correctly")
        return True
    else:
        print(f"  ✗ Expected 2, got {result}")
        return False

def main():
    """Run all algorithm verification tests."""
    print("=" * 70)
    print("Algorithm Correctness Verification")
    print("=" * 70)

    tests = [
        verify_bfs_shortest_path,
        verify_path_overlap,
        verify_empty_branch_handling,
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL ALGORITHM CHECKS PASSED")
    else:
        print("✗ SOME ALGORITHM CHECKS FAILED")
    print("=" * 70)

if __name__ == "__main__":
    main()
