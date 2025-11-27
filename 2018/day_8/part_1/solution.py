"""
Tree License Number Calculator

Parses a tree structure encoded as space-separated integers and calculates
the sum of all metadata entries in the tree.
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
    Recursively parse a node starting at the given index.

    Args:
        data: List of integers representing the tree
        index: Current position in the data list

    Returns:
        tuple: (new_index, metadata_sum)
            - new_index: Position after this node's data
            - metadata_sum: Sum of all metadata in this subtree
    """
    # Bounds check: ensure we can read the header
    if index + 2 > len(data):
        raise ValueError(f"Unexpected end of data at index {index}: cannot read header")

    # Read header
    num_children = data[index]
    num_metadata = data[index + 1]
    index += 2

    # Process all child nodes
    child_metadata_sum = 0
    for _ in range(num_children):
        index, child_sum = parse_node(data, index)
        child_metadata_sum += child_sum

    # Bounds check: ensure we can read metadata
    if index + num_metadata > len(data):
        raise ValueError(f"Unexpected end of data at index {index}: need {num_metadata} metadata entries")

    # Read and sum metadata entries
    own_metadata_sum = sum(data[index:index + num_metadata])
    index += num_metadata

    # Return new index and total sum
    total_sum = child_metadata_sum + own_metadata_sum
    return index, total_sum


def calculate_license_sum(data):
    """
    Calculate the sum of all metadata entries in the tree.

    Args:
        data: List of integers representing the tree structure

    Returns:
        int: Sum of all metadata entries
    """
    final_index, metadata_sum = parse_node(data, 0)

    # Verify that all data was consumed
    if final_index != len(data):
        raise ValueError(f"Data not fully consumed: {final_index}/{len(data)} integers processed")

    return metadata_sum


def main():
    """Main entry point for the solution."""
    data = parse_input('input.md')
    result = calculate_license_sum(data)
    print(result)
    return result


if __name__ == '__main__':
    main()
