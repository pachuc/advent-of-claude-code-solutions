"""
Comprehensive tests for Part 2 solution
"""
from solution import solve, parse_regex_and_build_graph, build_adjacency_graph, count_distant_rooms


def test_simple_threshold_counting():
    """Test 1.1: Simple threshold counting with known distances"""
    print("Test 1.1: Simple threshold counting...")
    regex_input = '^EEENNN$'

    # Test various thresholds
    result_0 = solve(regex_input, threshold=0)
    result_1 = solve(regex_input, threshold=1)
    result_3 = solve(regex_input, threshold=3)
    result_6 = solve(regex_input, threshold=6)
    result_7 = solve(regex_input, threshold=7)

    assert result_0 == 7, f"Threshold 0: Expected 7, got {result_0}"
    assert result_1 == 6, f"Threshold 1: Expected 6, got {result_1}"
    assert result_3 == 4, f"Threshold 3: Expected 4, got {result_3}"
    assert result_6 == 1, f"Threshold 6: Expected 1, got {result_6}"
    assert result_7 == 0, f"Threshold 7: Expected 0, got {result_7}"

    print("  ✓ All simple threshold tests passed")


def test_branching():
    """Test 1.2: Graph with branches"""
    print("Test 1.2: Branch handling...")
    regex_input = '^N(E|W)N$'

    # This creates: start -> N -> (E or W) -> N
    # Should have unique rooms counted only once
    result = solve(regex_input, threshold=0)

    # Rooms: (0,0), (0,-1), (1,-2), (-1,-2), (1,-3), (-1,-3)
    # Total: 6 rooms
    assert result == 6, f"Expected 6 rooms, got {result}"

    print("  ✓ Branch handling test passed")


def test_empty_branch():
    """Test 1.3: Empty branch handling"""
    print("Test 1.3: Empty branch handling...")
    regex_input = '^NNNN(EE|)NNNN$'

    result = solve(regex_input, threshold=0)
    # One path: NNNNNNNN (8 north) = 9 rooms
    # Other path: NNNNEENNNN (creates 2 additional rooms)
    # Total unique rooms should be counted
    assert result > 0, "Should have rooms"

    print(f"  ✓ Empty branch test passed (found {result} rooms)")


def test_graph_construction():
    """Test 3.1: Graph construction validation"""
    print("Test 3.1: Graph construction...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    regex = input_text.strip()[1:-1]
    doors = parse_regex_and_build_graph(regex)
    graph = build_adjacency_graph(doors)

    total_rooms = len(graph)
    total_doors = len(doors)

    print(f"  Total rooms: {total_rooms}")
    print(f"  Total doors: {total_doors}")

    assert total_rooms > 1000, "Graph should have many rooms"
    assert total_doors > 1000, "Graph should have many doors"

    print("  ✓ Graph construction test passed")


def test_max_distance_consistency():
    """Test 3.2: Verify max distance matches Part 1"""
    print("Test 3.2: Maximum distance verification...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    regex = input_text.strip()[1:-1]
    doors = parse_regex_and_build_graph(regex)
    graph = build_adjacency_graph(doors)

    # Modified count function to also track max distance
    from collections import deque

    queue = deque([((0, 0), 0)])
    visited = {(0, 0)}
    max_dist = 0

    while queue:
        pos, dist = queue.popleft()
        max_dist = max(max_dist, dist)

        for neighbor in graph[pos]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    print(f"  Maximum distance found: {max_dist}")
    assert max_dist == 3672, f"Expected max distance 3672 (from Part 1), got {max_dist}"

    print("  ✓ Max distance matches Part 1 answer")


def test_boundary_conditions():
    """Test 2.2 & 2.3: Boundary condition tests"""
    print("Test 2.2 & 2.3: Boundary conditions...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    # Threshold beyond maximum distance
    result_4000 = solve(input_text, threshold=4000)
    assert result_4000 == 0, f"Expected 0 for threshold 4000, got {result_4000}"
    print(f"  Threshold 4000: {result_4000} rooms (expected 0) ✓")

    # Threshold at 0 (should count all rooms)
    regex = input_text.strip()[1:-1]
    doors = parse_regex_and_build_graph(regex)
    graph = build_adjacency_graph(doors)
    total_rooms = len(graph)

    result_0 = solve(input_text, threshold=0)
    assert result_0 == total_rooms, f"Expected {total_rooms} for threshold 0, got {result_0}"
    print(f"  Threshold 0: {result_0} rooms (all rooms) ✓")

    print("  ✓ Boundary condition tests passed")


def test_monotonicity():
    """Test 4.2: Verify monotonic decrease with increasing threshold"""
    print("Test 4.2: Threshold monotonicity...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    count_500 = solve(input_text, threshold=500)
    count_1000 = solve(input_text, threshold=1000)
    count_2000 = solve(input_text, threshold=2000)
    count_3000 = solve(input_text, threshold=3000)

    print(f"  Distance >= 500:  {count_500}")
    print(f"  Distance >= 1000: {count_1000}")
    print(f"  Distance >= 2000: {count_2000}")
    print(f"  Distance >= 3000: {count_3000}")

    assert count_500 >= count_1000, "Higher threshold should not increase count"
    assert count_1000 >= count_2000, "Higher threshold should not increase count"
    assert count_2000 >= count_3000, "Higher threshold should not increase count"

    print("  ✓ Monotonicity verified")


def test_actual_puzzle():
    """Test 4.1: Verify actual puzzle answer"""
    print("Test 4.1: Actual puzzle answer...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)

    print(f"  Answer: {result} rooms require at least 1000 doors")

    # Sanity checks
    assert result > 0, "Should have at least one room beyond 1000 doors"
    assert result < 10000, "Shouldn't have an unreasonably large count"

    # According to implementation summary, expected answer is 8586
    assert result == 8586, f"Expected 8586, got {result}"

    print("  ✓ Actual puzzle answer verified")

    return result


if __name__ == '__main__':
    print("="*60)
    print("Running Part 2 Solution Tests")
    print("="*60)

    try:
        test_simple_threshold_counting()
        test_branching()
        test_empty_branch()
        test_graph_construction()
        test_max_distance_consistency()
        test_boundary_conditions()
        test_monotonicity()
        answer = test_actual_puzzle()

        print("\n" + "="*60)
        print("ALL TESTS PASSED!")
        print("="*60)
        print(f"\nFinal Answer: {answer}")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
