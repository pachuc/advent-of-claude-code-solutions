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


def topological_sort_alphabetical(all_steps, dependencies):
    """
    Perform topological sort with alphabetical tie-breaking.

    Returns: string of steps in execution order
    """
    result = []

    # Find initial available steps (no prerequisites)
    available = [step for step in all_steps if len(dependencies[step]) == 0]
    available.sort()

    # Deep copy dependencies to track remaining prerequisites
    remaining_dependencies = {k: v.copy() for k, v in dependencies.items()}

    while available:
        # Select alphabetically first available step
        current_step = available.pop(0)

        # Add to result
        result.append(current_step)

        # Update dependencies for all remaining steps
        for step in all_steps:
            if step not in result:
                # Remove completed step from prerequisites
                remaining_dependencies[step].discard(current_step)

                # If step now has no dependencies, add to available
                if len(remaining_dependencies[step]) == 0 and step not in available:
                    available.append(step)

        # Keep available list sorted
        available.sort()

    return ''.join(result)


def solve(input_text=None, input_file='input.md'):
    """
    Main solver function.

    Args:
        input_text: Optional string containing input data. If None, reads from input_file
        input_file: Path to input file (default: 'input.md')

    Returns:
        str: The order in which steps should be completed
    """
    # Parse input
    if input_text is not None:
        deps_list = parse_input_text(input_text)
    else:
        with open(input_file) as f:
            deps_list = parse_input_text(f.read())

    # Build graph
    all_steps, dependencies = build_dependency_graph(deps_list)

    # Solve
    result = topological_sort_alphabetical(all_steps, dependencies)

    return result


if __name__ == '__main__':
    answer = solve()
    print(answer)
