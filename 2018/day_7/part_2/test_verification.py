"""Comprehensive verification tests for the solution."""

from solution import (
    parse_input_text, build_dependency_graph, get_step_duration,
    get_available_steps, simulate_parallel_execution, solve
)


def test_step_durations():
    """Test step duration calculations."""
    print("Testing step durations...")

    # Test with base_time=60 (actual problem)
    assert get_step_duration('A', 60) == 61
    assert get_step_duration('B', 60) == 62
    assert get_step_duration('G', 60) == 67
    assert get_step_duration('Z', 60) == 86

    # Test with base_time=0 (example)
    assert get_step_duration('A', 0) == 1
    assert get_step_duration('C', 0) == 3
    assert get_step_duration('F', 0) == 6

    print("✓ Step duration tests passed")


def test_example():
    """Test the provided example from the problem."""
    print("\nTesting provided example...")

    example_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

    result = solve(input_text=example_input, num_workers=2, base_time=0)
    assert result == 15, f"Example test failed: expected 15, got {result}"
    print(f"✓ Example test passed: {result} seconds")


def test_edge_cases():
    """Test various edge cases."""
    print("\nTesting edge cases...")

    # Test 1: Single step, no dependencies
    all_steps = {'A'}
    deps = {'A': set()}
    result = simulate_parallel_execution(all_steps, deps, num_workers=5, base_time=60)
    assert result == 61, f"Single step test failed: expected 61, got {result}"
    print("✓ Single step test passed")

    # Test 2: Linear chain (no parallelism possible)
    all_steps = {'A', 'B'}
    deps = {'A': set(), 'B': {'A'}}
    result = simulate_parallel_execution(all_steps, deps, num_workers=5, base_time=60)
    assert result == 123, f"Linear chain test failed: expected 123, got {result}"
    print("✓ Linear chain test passed")

    # Test 3: Fully parallel (all independent)
    all_steps = {'A', 'B', 'C', 'D', 'E'}
    deps = {s: set() for s in all_steps}
    result = simulate_parallel_execution(all_steps, deps, num_workers=5, base_time=60)
    # All 5 start at time 0, longest is E at 65 seconds
    assert result == 65, f"Fully parallel test failed: expected 65, got {result}"
    print("✓ Fully parallel test passed")

    # Test 4: More steps than workers (6 steps, 5 workers)
    all_steps = {'A', 'B', 'C', 'D', 'E', 'F'}
    deps = {s: set() for s in all_steps}
    result = simulate_parallel_execution(all_steps, deps, num_workers=5, base_time=60)
    # First 5 start: A(61), B(62), C(63), D(64), E(65)
    # A finishes first at 61, F starts at 61, finishes at 61+66=127
    assert result == 127, f"More steps than workers test failed: expected 127, got {result}"
    print("✓ More steps than workers test passed")


def test_actual_input():
    """Test with the actual problem input."""
    print("\nTesting actual input...")

    result = solve()
    print(f"Result: {result} seconds")

    # Validation checks
    assert isinstance(result, int), f"Result should be int, got {type(result)}"
    assert result > 0, "Result should be positive"
    assert 400 < result < 2000, f"Result {result} outside reasonable range (400-2000)"

    print("✓ Actual input test passed")
    return result


def test_determinism():
    """Test that the solution is deterministic."""
    print("\nTesting determinism...")

    result1 = solve()
    result2 = solve()
    result3 = solve()

    assert result1 == result2 == result3, f"Results not deterministic: {result1}, {result2}, {result3}"
    print(f"✓ Determinism test passed (all runs returned {result1})")
    return result1


def test_alphabetical_ordering():
    """Test that steps are assigned in alphabetical order."""
    print("\nTesting alphabetical ordering...")

    # 4 independent steps, 2 workers
    # Should assign A, B first (not C, D or any other order)
    all_steps = {'D', 'A', 'C', 'B'}
    deps = {s: set() for s in all_steps}

    result = simulate_parallel_execution(all_steps, deps, num_workers=2, base_time=60)

    # Expected timeline:
    # Time 0: Worker 0 starts A (61s), Worker 1 starts B (62s)
    # Time 61: A completes, Worker 0 starts C (63s)
    # Time 62: B completes, Worker 1 starts D (64s)
    # Time 124: C completes (61 + 63)
    # Time 126: D completes (62 + 64)
    # Total: 126 seconds

    assert result == 126, f"Alphabetical ordering test failed: expected 126, got {result}"
    print("✓ Alphabetical ordering test passed")


def verify_dependencies():
    """Verify that dependencies are correctly respected."""
    print("\nVerifying dependency handling...")

    # Test with a complex dependency graph
    all_steps = {'A', 'B', 'C', 'D'}
    deps = {
        'A': set(),
        'B': set(),
        'C': {'A', 'B'},  # C depends on both A and B
        'D': {'C'}         # D depends on C
    }

    result = simulate_parallel_execution(all_steps, deps, num_workers=5, base_time=60)

    # Timeline:
    # Time 0: A and B start (61s, 62s)
    # Time 61: A completes
    # Time 62: B completes, C can now start (63s)
    # Time 125: C completes (62 + 63), D can now start (64s)
    # Time 189: D completes (125 + 64)

    assert result == 189, f"Dependency test failed: expected 189, got {result}"
    print("✓ Dependency handling test passed")


if __name__ == '__main__':
    print("=" * 60)
    print("COMPREHENSIVE SOLUTION VERIFICATION")
    print("=" * 60)

    # Run all tests
    test_step_durations()
    test_example()
    test_edge_cases()
    test_alphabetical_ordering()
    verify_dependencies()
    final_result = test_actual_input()
    test_determinism()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print(f"\nFinal Answer: {final_result} seconds")
    print("\nThe solution is correct and ready for submission.")
