def parse_input(input_data):
    """
    Parse the input to extract weights, children relationships, and find root.

    Args:
        input_data: String containing program descriptions

    Returns:
        weights: dict mapping program name -> own weight
        children: dict mapping program name -> list of child names
        root: name of the root program
    """
    lines = [line.strip() for line in input_data.strip().split('\n') if line.strip()]

    weights = {}
    children = {}
    all_programs = set()
    all_children = set()

    for line in lines:
        # Split by '->' to separate parent from children
        parts = line.split('->')
        parent_part = parts[0]

        # Extract name and weight
        name = parent_part.split('(')[0].strip()
        weight = int(parent_part.split('(')[1].split(')')[0])

        weights[name] = weight
        all_programs.add(name)

        # Extract children if they exist
        if len(parts) > 1 and parts[1].strip():
            child_list = [child.strip() for child in parts[1].split(',')]
            children[name] = child_list
            all_children.update(child_list)

    # Find root: program that is never a child
    root = (all_programs - all_children).pop()

    return weights, children, root


def calculate_total_weight(node, weights, children, memo):
    """
    Calculate the total weight of a node (own weight + all descendants).

    Args:
        node: program name
        weights: dict of own weights
        children: dict of children relationships
        memo: dict for memoization

    Returns:
        Total weight of the node and all its descendants
    """
    if node in memo:
        return memo[node]

    total = weights[node]
    if node in children:
        for child in children[node]:
            total += calculate_total_weight(child, weights, children, memo)

    memo[node] = total
    return total


def find_imbalanced_node(node, weights, children, total_weights):
    """
    Find the deepest node where children have mismatched total weights.

    Args:
        node: current node to check
        weights: dict of own weights
        children: dict of children relationships
        total_weights: dict of total weights for all nodes

    Returns:
        tuple (wrong_program, wrong_total_weight, correct_total_weight) or None
    """
    if node not in children or not children[node]:
        return None  # Leaf node, no imbalance here

    # Get total weights of all children
    child_weights = {child: total_weights[child] for child in children[node]}

    # Check if all equal
    if len(set(child_weights.values())) == 1:
        return None  # All balanced at this level

    # Find which child is different
    weight_counts = {}
    for child, weight in child_weights.items():
        if weight not in weight_counts:
            weight_counts[weight] = []
        weight_counts[weight].append(child)

    # The wrong child has a unique weight (appears once)
    wrong_child = None
    correct_weight = None
    for weight, nodes in weight_counts.items():
        if len(nodes) == 1:
            wrong_child = nodes[0]
        else:
            correct_weight = weight

    # Recursively check if the imbalance is deeper
    deeper_imbalance = find_imbalanced_node(wrong_child, weights, children, total_weights)
    if deeper_imbalance:
        return deeper_imbalance

    # This is the deepest imbalance
    return (wrong_child, total_weights[wrong_child], correct_weight)


def solve_part2(input_data):
    """
    Solve Part 2: Find the corrected weight for the wrong program.

    Args:
        input_data: String containing program descriptions

    Returns:
        The corrected weight that the wrong program should have
    """
    # Step 1: Parse input and find root
    weights, children, root = parse_input(input_data)

    # Step 2: Calculate total weights starting from root
    total_weights = {}
    calculate_total_weight(root, weights, children, total_weights)

    # Step 3: Find the imbalanced node
    imbalance = find_imbalanced_node(root, weights, children, total_weights)

    # Step 4: Calculate corrected weight
    wrong_program, wrong_total, correct_total = imbalance
    difference = correct_total - wrong_total
    corrected_weight = weights[wrong_program] + difference

    return corrected_weight


def main():
    # Test with example first
    print("=" * 50)
    print("Testing with example input...")
    print("=" * 50)

    example_input = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

    example_result = solve_part2(example_input)
    print(f"Example result: {example_result}")
    print(f"Expected: 60")

    if example_result == 60:
        print("✓ Example test PASSED!\n")
    else:
        print("✗ Example test FAILED!")
        return

    # Now solve the actual puzzle
    print("=" * 50)
    print("Solving actual puzzle...")
    print("=" * 50)

    with open('/app/agent_workspace/2017/day_7/part_2/input.md', 'r') as f:
        input_data = f.read()

    result = solve_part2(input_data)
    print(f"\n{'=' * 50}")
    print(f"ANSWER: {result}")
    print(f"{'=' * 50}")

    return result


if __name__ == "__main__":
    main()
