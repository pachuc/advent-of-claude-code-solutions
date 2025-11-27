"""
Tree Node Value Calculator (Part 2)

Parses a tree structure encoded as space-separated integers and calculates
the value of the root node based on special rules:
- Leaf nodes (no children): value = sum of metadata
- Internal nodes (has children): metadata entries are 1-based indexes to children,
  value = sum of referenced child values
"""


def parse_input(filename='input.md'):
    """
    Read and parse the input file into a list of integers.

    Args:
        filename: Path to the input file

    Returns:
        list[int]: List of integers representing the tree structure
    """
    with open(filename, 'r') as f:
        content = f.read()

    # Split by whitespace and convert to integers
    numbers = [int(x) for x in content.split()]
    return numbers


def parse_node(data, index):
    """
    Recursively parse a node starting at the given index and calculate its value.

    Args:
        data: List of integers representing the tree
        index: Current position in the data list

    Returns:
        tuple: (new_index, node_value)
            - new_index: Position after this node's data
            - node_value: The calculated value of this node
    """
    # Bounds check: ensure we can read the header
    if index + 2 > len(data):
        raise ValueError(f"Unexpected end of data at index {index}: cannot read header")

    # Read header
    num_children = data[index]
    num_metadata = data[index + 1]
    index += 2

    # Process all child nodes and store their values
    child_values = []
    for _ in range(num_children):
        index, child_value = parse_node(data, index)
        child_values.append(child_value)

    # Bounds check: ensure we can read metadata
    if index + num_metadata > len(data):
        raise ValueError(f"Unexpected end of data at index {index}: need {num_metadata} metadata entries")

    # Read metadata entries
    metadata = data[index:index + num_metadata]
    index += num_metadata

    # Calculate node value based on whether it has children
    if num_children == 0:
        # Leaf node: value = sum of metadata
        node_value = sum(metadata)
    else:
        # Internal node: metadata are 1-based child indexes
        node_value = 0
        for meta in metadata:
            # Convert 1-based index to 0-based
            child_index = meta - 1
            # Only add if valid index (handles meta=0 or meta > num_children)
            if 0 <= child_index < len(child_values):
                node_value += child_values[child_index]
            # Invalid indexes are skipped

    return index, node_value


def calculate_root_value(data):
    """
    Calculate the value of the root node.

    Args:
        data: List of integers representing the tree

    Returns:
        int: Value of the root node
    """
    final_index, root_value = parse_node(data, 0)

    # Verify all data consumed
    if final_index != len(data):
        raise ValueError(f"Data not fully consumed: {final_index}/{len(data)} integers processed")

    return root_value


def main():
    """Main entry point for the solution."""
    data = parse_input('input.md')
    result = calculate_root_value(data)
    print(result)
    return result


if __name__ == '__main__':
    main()
