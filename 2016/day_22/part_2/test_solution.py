#!/usr/bin/env python3
"""
Test suite for Part 2 solution.
Run with: python test_solution.py
"""

from solution import parse_input, find_minimum_steps
import sys


def run_test(test_name, test_func):
    """Helper to run a test and report results."""
    try:
        test_func()
        print(f"✓ {test_name}")
        return True
    except AssertionError as e:
        print(f"✗ {test_name}: {e}")
        return False
    except Exception as e:
        print(f"✗ {test_name}: Unexpected error: {e}")
        return False


def test_parsing():
    """Test that input parsing extracts correct grid structure."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    # Verify grid dimensions (note: coordinates are 0-indexed)
    assert max_x >= 0, f"max_x should be non-negative, got {max_x}"
    assert max_y >= 0, f"max_y should be non-negative, got {max_y}"

    # Verify reasonable grid size (should be ~30-40 × ~25-30)
    assert 20 <= max_x <= 50, f"Expected max_x in range 20-50, got {max_x}"
    assert 20 <= max_y <= 50, f"Expected max_y in range 20-50, got {max_y}"

    # Verify number of nodes
    expected_nodes = (max_x + 1) * (max_y + 1)
    assert len(nodes_dict) == expected_nodes, \
        f"Expected {expected_nodes} nodes, got {len(nodes_dict)}"

    # Verify empty node exists and is valid
    assert empty_pos is not None, "No empty node found"
    assert empty_pos in nodes_dict, "Empty position not in grid"
    assert nodes_dict[empty_pos]['used'] == 0, \
        f"Empty node should have used=0, got {nodes_dict[empty_pos]['used']}"

    # Verify exactly one empty node
    empty_count = sum(1 for n in nodes_dict.values() if n['used'] == 0)
    assert empty_count == 1, f"Expected 1 empty node, found {empty_count}"

    # Verify goal position
    assert goal_pos == (max_x, 0), \
        f"Goal should be at (max_x, 0) = ({max_x}, 0), got {goal_pos}"
    assert goal_pos in nodes_dict, "Goal position not in grid"

    # Verify all coordinates are within bounds
    for (x, y) in nodes_dict.keys():
        assert 0 <= x <= max_x, f"Node x-coordinate {x} out of bounds [0, {max_x}]"
        assert 0 <= y <= max_y, f"Node y-coordinate {y} out of bounds [0, {max_y}]"

    # Verify all nodes have required fields
    for pos, node in nodes_dict.items():
        assert 'size' in node, f"Node {pos} missing 'size'"
        assert 'used' in node, f"Node {pos} missing 'used'"
        assert 'avail' in node, f"Node {pos} missing 'avail'"
        assert node['size'] >= 0, f"Node {pos} has negative size"
        assert node['used'] >= 0, f"Node {pos} has negative used"
        assert node['avail'] >= 0, f"Node {pos} has negative avail"


def test_wall_detection():
    """Test that wall positions are correctly identified."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    # Get empty capacity for verification
    empty_capacity = nodes_dict[empty_pos]['size']
    assert empty_capacity > 0, "Empty capacity should be positive"

    # Verify walls are correctly identified
    # A wall is any node whose used data is larger than empty capacity
    for pos in wall_positions:
        assert pos in nodes_dict, f"Wall position {pos} not in grid"
        assert nodes_dict[pos]['used'] > empty_capacity, \
            f"Wall {pos} has used={nodes_dict[pos]['used']} but empty capacity is {empty_capacity}"

    # Verify non-walls are not in wall_positions
    for pos, node in nodes_dict.items():
        if node['used'] <= empty_capacity:
            assert pos not in wall_positions, \
                f"Node {pos} with used={node['used']} should not be a wall (capacity={empty_capacity})"

    # Verify wall count is reasonable (should be some but not all nodes)
    assert len(wall_positions) > 0, "Expected some wall nodes"
    assert len(wall_positions) < len(nodes_dict) / 2, \
        f"Too many walls: {len(wall_positions)} out of {len(nodes_dict)} nodes"

    # Verify goal is not a wall (critical!)
    assert goal_pos not in wall_positions, \
        f"Goal {goal_pos} cannot be a wall!"

    # Verify no walls at y=0 (goal needs to move along top row)
    walls_at_y0 = [pos for pos in wall_positions if pos[1] == 0]
    assert len(walls_at_y0) == 0, \
        f"Found {len(walls_at_y0)} walls at y=0, which would block goal movement"


def test_part1_compatibility():
    """Verify Part 1 answer (981) can still be computed with extended parser."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse with new Part 2 parser
    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    # Extract data in Part 1 format: list of (used, avail) tuples
    nodes_part1 = [(node['used'], node['avail']) for node in nodes_dict.values()]

    # Reimplement Part 1's viable pair counting logic
    count = 0
    for i in range(len(nodes_part1)):
        used_a, avail_a = nodes_part1[i]
        if used_a == 0:
            continue
        for j in range(len(nodes_part1)):
            if i == j:
                continue
            used_b, avail_b = nodes_part1[j]
            if used_a <= avail_b:
                count += 1

    # Part 1 answer should still be 981
    assert count > 0, "Viable pair count should be positive"
    # From Part 1 context, we expect 981
    assert count == 981, f"Part 1 answer should be 981, got {count}"


def test_bfs_basic():
    """Test BFS with simple, known cases."""

    # Test 1: Goal already at target - should return 0
    test_grid_1 = {
        (0, 0): {'size': 10, 'used': 5, 'avail': 5},
        (1, 0): {'size': 10, 'used': 0, 'avail': 10},
    }
    result = find_minimum_steps(test_grid_1, 1, 0, set(), (0, 0), (1, 0), (0, 0))
    assert result == 0, f"Goal at target should return 0, got {result}"

    # Test 2: Simple 1-step move
    # Goal at (1, 0), Empty at (0, 0), just swap them
    test_grid_2 = {
        (0, 0): {'size': 10, 'used': 0, 'avail': 10},
        (1, 0): {'size': 10, 'used': 5, 'avail': 5},
    }
    result = find_minimum_steps(test_grid_2, 1, 0, set(), (1, 0), (0, 0), (0, 0))
    assert result == 1, f"Simple swap should be 1 step, got {result}"

    # Test 3: Impossible due to wall
    test_grid_3 = {
        (0, 0): {'size': 10, 'used': 0, 'avail': 10},
        (1, 0): {'size': 500, 'used': 500, 'avail': 0},  # Wall
        (2, 0): {'size': 10, 'used': 5, 'avail': 5},
    }
    wall_set = {(1, 0)}  # Middle node is a wall
    result = find_minimum_steps(test_grid_3, 2, 0, wall_set, (2, 0), (0, 0), (0, 0))
    assert result is None, f"Blocked path should return None, got {result}"


def test_edge_cases():
    """Test various edge cases."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    # Edge case 1: Empty and goal coordinates are within bounds
    assert 0 <= empty_pos[0] <= max_x, f"Empty x-coord {empty_pos[0]} out of bounds"
    assert 0 <= empty_pos[1] <= max_y, f"Empty y-coord {empty_pos[1]} out of bounds"
    assert 0 <= goal_pos[0] <= max_x, f"Goal x-coord {goal_pos[0]} out of bounds"
    assert 0 <= goal_pos[1] <= max_y, f"Goal y-coord {goal_pos[1]} out of bounds"

    # Edge case 2: Goal is at y=0 (top row)
    assert goal_pos[1] == 0, f"Goal should be at y=0, got y={goal_pos[1]}"

    # Edge case 3: Goal x-coordinate is max_x (rightmost)
    assert goal_pos[0] == max_x, f"Goal should be at x={max_x}, got x={goal_pos[0]}"

    # Edge case 4: Empty is not the goal
    assert empty_pos != goal_pos, "Empty and goal should be different positions"

    # Edge case 5: Empty node has capacity to hold goal's data
    empty_capacity = nodes_dict[empty_pos]['size']
    goal_used = nodes_dict[goal_pos]['used']
    assert goal_used <= empty_capacity, \
        f"Goal data ({goal_used}T) must fit in empty capacity ({empty_capacity}T)"


def test_integration():
    """Test complete solution on actual input."""
    import time

    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input
    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    # Run BFS
    target_pos = (0, 0)
    start_time = time.time()
    result = find_minimum_steps(
        nodes_dict, max_x, max_y, wall_positions, goal_pos, empty_pos, target_pos
    )
    elapsed = time.time() - start_time

    # Verify result is valid
    assert result is not None, "BFS should find a solution"
    assert isinstance(result, int), f"Result should be an integer, got {type(result)}"
    assert result > 0, f"Result should be positive, got {result}"

    # Sanity check: result should be at least the Manhattan distance from goal to target
    manhattan_distance = abs(goal_pos[0] - target_pos[0]) + abs(goal_pos[1] - target_pos[1])
    assert result >= manhattan_distance, \
        f"Result {result} should be >= Manhattan distance {manhattan_distance}"

    # Sanity check: result shouldn't be absurdly large
    # Upper bound estimate: grid has ~1000 nodes, shouldn't need more than that many steps
    assert result < len(nodes_dict), \
        f"Result {result} seems too large for grid with {len(nodes_dict)} nodes"

    print(f"  Solution found: {result} steps in {elapsed:.2f}s")


def test_performance():
    """Test that solution completes in reasonable time."""
    import time

    with open('input.md', 'r') as f:
        input_text = f.read()

    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    target_pos = (0, 0)

    # Time the BFS
    start = time.time()
    result = find_minimum_steps(
        nodes_dict, max_x, max_y, wall_positions, goal_pos, empty_pos, target_pos
    )
    elapsed = time.time() - start

    # Concrete performance criteria
    assert elapsed < 60, \
        f"Solution took {elapsed:.1f}s, should complete in < 60s"

    assert result is not None, "Solution should be found"

    print(f"  Completed in {elapsed:.2f}s")


def main():
    """Run all tests."""
    tests = [
        ("Input Parsing", test_parsing),
        ("Wall Detection", test_wall_detection),
        ("Part 1 Compatibility", test_part1_compatibility),
        ("BFS Basic Functionality", test_bfs_basic),
        ("Edge Cases", test_edge_cases),
        ("Integration Test", test_integration),
        ("Performance Test", test_performance),
    ]

    passed = 0
    for name, func in tests:
        if run_test(name, func):
            passed += 1

    print(f"\n{passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
