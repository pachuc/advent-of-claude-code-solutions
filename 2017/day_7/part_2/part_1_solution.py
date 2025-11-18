def find_bottom_program(input_data: str) -> str:
    """
    Find the bottom program (root) of the tower.

    The bottom program is the one that holds other programs but is not held by any program itself.

    Args:
        input_data: String containing program descriptions, one per line

    Returns:
        Name of the bottom program (root of the tree)
    """
    # Step 1: Preprocess input - clean and filter lines
    lines = input_data.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    # Step 2: Initialize sets for tracking programs
    all_programs = set()
    all_children = set()

    # Step 3: Parse each line to extract parent and children
    for line in lines:
        # Split by '->' to separate parent from children
        parts = line.split('->')

        # Extract parent name (everything before '(')
        parent_part = parts[0]
        parent_name = parent_part.split('(')[0].strip()

        # Add parent to all_programs set
        all_programs.add(parent_name)

        # If children exist (has '->' and content after it)
        if len(parts) > 1 and parts[1].strip():
            children_part = parts[1]
            # Split by comma and strip whitespace from each child
            children = [child.strip() for child in children_part.split(',') if child.strip()]
            # Add all children to all_children set
            all_children.update(children)

    # Step 4: Find the root - program that is never a child
    root_set = all_programs - all_children

    # Step 5: Sanity check - should have exactly one root
    assert len(root_set) == 1, f"Expected 1 root, found {len(root_set)}"

    # Step 6: Extract and return the root
    root = next(iter(root_set))
    return root


def main():
    """Main function to read input and solve the problem."""
    # Read the actual input file
    with open('/app/agent_workspace/2017/day_7/part_1/input.md', 'r') as f:
        input_data = f.read()

    # Find the bottom program
    result = find_bottom_program(input_data)

    # Print the result
    print(f"The bottom program is: {result}")
    return result


if __name__ == "__main__":
    main()
