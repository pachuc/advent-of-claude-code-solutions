def parse_input_text(text):
    """Parse input text and return list of (prerequisite, dependent) tuples."""
    dependencies = []
    for line in text.strip().split('\n'):
        if line:
            # Line format: "Step X must be finished before step Y can begin."
            # X is at position 5, Y is at position 36
            prerequisite = line[5]
            dependent = line[36]
            dependencies.append((prerequisite, dependent))
    return dependencies


def build_dependency_graph(dependencies_list):
    """
    Build graph from dependency list.

    Args:
        dependencies_list: List of (prerequisite, dependent) tuples

    Returns:
        tuple: (all_steps: set[str], dependencies: dict[str, set[str]])
            - all_steps: set of all unique step names
            - dependencies: dict mapping each step to set of its prerequisites
    """
    all_steps = set()
    dependencies_dict = {}

    # Collect all steps and build dependencies
    for prerequisite, dependent in dependencies_list:
        all_steps.add(prerequisite)
        all_steps.add(dependent)

        if dependent not in dependencies_dict:
            dependencies_dict[dependent] = set()
        dependencies_dict[dependent].add(prerequisite)

    # Ensure all steps have an entry (even those with no dependencies)
    for step in all_steps:
        if step not in dependencies_dict:
            dependencies_dict[step] = set()

    return all_steps, dependencies_dict


def get_step_duration(step_letter, base_time=60):
    """Calculate duration for a step: base_time + position in alphabet.

    Args:
        step_letter: Single uppercase letter (A-Z)
        base_time: Base seconds to add (default 60 for actual problem, 0 for example)

    Returns:
        Duration in seconds
    """
    # A=1, B=2, ..., Z=26
    return base_time + (ord(step_letter) - ord('A') + 1)


def get_available_steps(all_steps, completed_steps, in_progress_steps, remaining_dependencies):
    """Find steps that are ready to start (all prerequisites done, not started yet)."""
    available = []
    for step in all_steps:
        if step not in completed_steps and step not in in_progress_steps:
            if len(remaining_dependencies[step]) == 0:
                available.append(step)
    return sorted(available)  # Return in alphabetical order


def assign_workers(workers, available_steps, base_time=60):
    """Assign available steps to idle workers in alphabetical order."""
    assigned = []

    for step in available_steps:
        # Find an idle worker
        idle_worker_idx = None
        for i in range(len(workers)):
            if workers[i] is None:  # Worker is idle
                idle_worker_idx = i
                break

        if idle_worker_idx is None:
            break  # No more idle workers available

        # Assign step to this worker
        workers[idle_worker_idx] = {
            'step': step,
            'time_remaining': get_step_duration(step, base_time)
        }
        assigned.append(step)

    return assigned


def simulate_parallel_execution(all_steps, dependencies, num_workers=5, base_time=60):
    """Simulate parallel execution of steps with multiple workers.

    Args:
        all_steps: Set of all step names
        dependencies: Dict mapping step -> set of prerequisites
        num_workers: Number of workers available (default 5)
        base_time: Base time for step duration calculation (default 60)

    Returns:
        Total time in seconds to complete all steps
    """
    current_time = 0
    workers = [None] * num_workers  # All workers start idle
    completed_steps = set()
    in_progress_steps = set()

    # Deep copy dependencies to track remaining prerequisites
    remaining_dependencies = {k: v.copy() for k, v in dependencies.items()}

    while len(completed_steps) < len(all_steps):
        # 1. Check for completed work at current time
        for i in range(len(workers)):
            if workers[i] is not None and workers[i]['time_remaining'] == 0:
                # Step just completed
                completed_step = workers[i]['step']
                completed_steps.add(completed_step)
                in_progress_steps.remove(completed_step)

                # Update dependencies - remove this step from all prerequisites
                for step in all_steps:
                    remaining_dependencies[step].discard(completed_step)

                # Worker becomes idle
                workers[i] = None

        # 2. Assign new work to idle workers
        available = get_available_steps(all_steps, completed_steps,
                                        in_progress_steps, remaining_dependencies)
        newly_assigned = assign_workers(workers, available, base_time)
        in_progress_steps.update(newly_assigned)

        # 3. Advance time to next event
        busy_workers = [w for w in workers if w is not None]
        if busy_workers:
            # Find minimum time until next completion
            min_time = min(w['time_remaining'] for w in busy_workers)
            current_time += min_time

            # Decrement all workers' remaining time
            for i in range(len(workers)):
                if workers[i] is not None:
                    workers[i]['time_remaining'] -= min_time
        else:
            # All workers idle but steps remain - should not happen with valid input
            if len(completed_steps) < len(all_steps):
                raise RuntimeError(
                    f"Simulation stuck: {len(completed_steps)} steps completed, "
                    f"{len(all_steps)} total, no workers busy, "
                    f"available steps: {get_available_steps(all_steps, completed_steps, in_progress_steps, remaining_dependencies)}"
                )
            break

    return current_time


def solve(input_text=None, input_file='input.md', num_workers=5, base_time=60):
    """Solve the parallel task execution problem.

    Args:
        input_text: Optional string containing input data. If None, reads from input_file
        input_file: Path to input file (default: 'input.md')
        num_workers: Number of workers available (default: 5)
        base_time: Base seconds for duration calculation (default: 60)

    Returns:
        int: Total time in seconds to complete all steps
    """
    # Parse input (reuse from Part 1)
    if input_text is not None:
        deps_list = parse_input_text(input_text)
    else:
        with open(input_file) as f:
            deps_list = parse_input_text(f.read())

    # Build graph (reuse from Part 1)
    all_steps, dependencies = build_dependency_graph(deps_list)

    # Simulate parallel execution (new)
    total_time = simulate_parallel_execution(all_steps, dependencies,
                                             num_workers=num_workers,
                                             base_time=base_time)

    return total_time


if __name__ == '__main__':
    # Quick unit tests
    print("Testing step durations...")
    assert get_step_duration('A', 60) == 61
    assert get_step_duration('Z', 60) == 86
    assert get_step_duration('A', 0) == 1  # For example testing
    assert get_step_duration('C', 0) == 3
    print("✓ Step durations correct")

    # Test the provided example (CRITICAL - must pass)
    print("\nTesting provided example...")
    example_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

    result = solve(input_text=example_input, num_workers=2, base_time=0)
    assert result == 15, f"Example failed: expected 15, got {result}"
    print(f"✓ Example test passed: {result} seconds")

    # Test worker idle bug
    print("\nTesting worker idle transition...")
    all_steps = {'A', 'B'}
    deps = {'A': set(), 'B': {'A'}}
    result = simulate_parallel_execution(all_steps, deps, num_workers=1, base_time=60)
    assert result == 123, f"Worker idle test failed: expected 123, got {result}"
    print("✓ Worker idle test passed")

    # Solve actual problem
    print("\nSolving actual problem...")
    answer = solve()
    print(f"\nAnswer: {answer} seconds")

    # Sanity check
    assert 400 < answer < 2000, f"Answer {answer} outside expected range"
    print("✓ Answer is in reasonable range")
