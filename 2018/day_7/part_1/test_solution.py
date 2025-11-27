from solution import solve, parse_input_text, build_dependency_graph


def validate_solution(input_deps, output_order):
    """
    Validate that output_order is a correct topological sort.
    Returns (is_valid, error_message)
    """
    # Check 1: Completeness
    steps_in_input = set()
    for prereq, dep in input_deps:
        steps_in_input.add(prereq)
        steps_in_input.add(dep)

    if len(output_order) != len(steps_in_input):
        return False, f"Length mismatch: expected {len(steps_in_input)}, got {len(output_order)}"

    if set(output_order) != steps_in_input:
        return False, "Steps in output don't match steps in input"

    if len(output_order) != len(set(output_order)):
        return False, "Duplicate steps in output"

    # Check 2: Dependency satisfaction
    position = {step: idx for idx, step in enumerate(output_order)}

    for prereq, dependent in input_deps:
        if prereq not in position or dependent not in position:
            return False, f"Missing steps in output"

        if position[prereq] >= position[dependent]:
            return False, f"Dependency violated: {prereq} must come before {dependent}"

    return True, "Valid"


def verify_alphabetical_ordering(all_steps, dependencies, output_order):
    """
    Verify that at each step, the alphabetically first available step was chosen.
    Returns (is_valid, error_message)
    """
    completed = set()
    remaining_deps = {k: v.copy() for k, v in dependencies.items()}

    for i, step in enumerate(output_order):
        # Find all available steps at this point
        available = [s for s in all_steps
                     if s not in completed and len(remaining_deps[s]) == 0]

        if not available:
            return False, f"No available steps at position {i}, but output has {step}"

        # Verify the chosen step is alphabetically first
        expected = min(available)
        if step != expected:
            return False, f"At position {i}, should have chosen {expected}, not {step}. Available: {sorted(available)}"

        # Mark as completed and update dependencies
        completed.add(step)
        for other_step in remaining_deps:
            remaining_deps[other_step].discard(step)

    return True, "Alphabetical ordering verified"


def test_example():
    """Test against the example from problem statement."""
    input_text = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

    expected = "CABDFE"
    result = solve(input_text=input_text)
    assert result == expected, f"Expected {expected}, got {result}"
    print("✅ Example test passed")


def test_actual_input():
    """Test with actual input and validate properties."""
    # Solve the actual input
    result = solve(input_file='input.md')

    # Parse input for validation
    with open('input.md') as f:
        deps_list = parse_input_text(f.read())
    all_steps, dependencies = build_dependency_graph(deps_list)

    # Validate completeness and dependency satisfaction
    is_valid, message = validate_solution(deps_list, result)
    assert is_valid, f"Validation failed: {message}"

    # Validate alphabetical ordering
    is_valid, message = verify_alphabetical_ordering(all_steps, dependencies, result)
    assert is_valid, f"Alphabetical ordering failed: {message}"

    print(f"✅ Actual input test passed: {result}")
    return result


def test_edge_cases():
    """Run all edge case tests."""
    tests = [
        # Test 1: Minimal case
        ("Step A must be finished before step B can begin.", "AB"),

        # Test 2: Two independent branches
        ("Step A must be finished before step C can begin.\nStep B must be finished before step C can begin.", "ABC"),

        # Test 3: Simple chain
        ("Step A must be finished before step B can begin.\nStep B must be finished before step C can begin.", "ABC"),

        # Test 4: Reverse alphabetical dependencies
        ("Step Z must be finished before step A can begin.\nStep Y must be finished before step A can begin.\nStep X must be finished before step A can begin.", "XYZA"),

        # Test 5: Diamond
        ("Step A must be finished before step B can begin.\nStep A must be finished before step C can begin.\nStep B must be finished before step D can begin.\nStep C must be finished before step D can begin.", "ABCD"),

        # Test 6: Complex branch and merge
        ("Step A must be finished before step C can begin.\nStep B must be finished before step C can begin.\nStep C must be finished before step E can begin.\nStep D must be finished before step E can begin.", "ABCDE"),

        # Test 7: Duplicate dependencies
        ("Step A must be finished before step B can begin.\nStep A must be finished before step B can begin.\nStep A must be finished before step B can begin.", "AB"),
    ]

    for i, (input_text, expected) in enumerate(tests, 1):
        result = solve(input_text=input_text)
        assert result == expected, f"Test {i} failed: expected {expected}, got {result}"
        print(f"✅ Edge case test {i} passed")


def run_all_tests():
    """Run all tests in order."""
    print("Running Phase 1: Example Validation")
    test_example()

    print("\nRunning Phase 2: Actual Input Testing")
    answer = test_actual_input()

    print("\nRunning Phase 3: Edge Case Testing")
    test_edge_cases()

    print("\n" + "="*50)
    print("✅ All tests passed!")
    print(f"Final answer: {answer}")
    print("="*50)
    return answer


if __name__ == '__main__':
    run_all_tests()
