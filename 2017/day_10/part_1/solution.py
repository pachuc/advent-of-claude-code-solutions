def parse_input(input_string):
    """Parse comma-separated integers from input string."""
    return [int(x.strip()) for x in input_string.strip().split(',')]


def initialize_list(size=256):
    """Create initial list from 0 to size-1."""
    return list(range(size))


def reverse_circular(lst, start, length):
    """Reverse a circular section of the list.

    Args:
        lst: The list to modify (in-place)
        start: Starting index for reversal
        length: Number of elements to reverse
    """
    if length <= 1:
        return  # No reversal needed

    n = len(lst)

    # Extract elements circularly
    elements = []
    for i in range(length):
        elements.append(lst[(start + i) % n])

    # Reverse the extracted elements
    elements.reverse()

    # Place them back circularly
    for i in range(length):
        lst[(start + i) % n] = elements[i]


def knot_hash(lengths, list_size=256):
    """Execute the knot hash algorithm.

    Args:
        lengths: List of length values to process
        list_size: Size of the circular list (default 256)

    Returns:
        The final state of the list after all operations
    """
    # Initialize
    lst = initialize_list(list_size)
    current_position = 0
    skip_size = 0

    # Process each length
    for length in lengths:
        # Reverse the section (handles length 0 and 1 internally)
        reverse_circular(lst, current_position, length)

        # Update position (with wrapping)
        current_position = (current_position + length + skip_size) % list_size

        # Increment skip size
        skip_size += 1

    return lst


def compute_result(lst):
    """Multiply first two elements of the list."""
    return lst[0] * lst[1]


# Test functions
def test_parse_input():
    assert parse_input("3,4,1,5") == [3, 4, 1, 5]
    assert parse_input("3, 4, 1, 5") == [3, 4, 1, 5]
    print("✓ parse_input tests passed")


def test_initialize_list():
    lst5 = initialize_list(5)
    assert lst5 == [0, 1, 2, 3, 4]
    assert len(lst5) == 5

    lst256 = initialize_list(256)
    assert len(lst256) == 256
    assert lst256[0] == 0
    assert lst256[255] == 255
    print("✓ initialize_list tests passed")


def test_reverse_circular():
    # Test: No wrapping - beginning
    lst = [0, 1, 2, 3, 4]
    reverse_circular(lst, 0, 3)
    assert lst == [2, 1, 0, 3, 4], f"Expected [2,1,0,3,4], got {lst}"

    # Test: Wrapping - indices 3,4,0
    lst = [0, 1, 2, 3, 4]
    reverse_circular(lst, 3, 3)
    assert lst == [3, 1, 2, 0, 4], f"Expected [3,1,2,0,4], got {lst}"

    # Test: Wrapping - indices 3,4,0,1
    lst = [0, 1, 2, 3, 4]
    reverse_circular(lst, 3, 4)
    assert lst == [4, 3, 2, 1, 0], f"Expected [4,3,2,1,0], got {lst}"

    # Test: Edge case - length 0
    lst = [0, 1, 2, 3, 4]
    reverse_circular(lst, 2, 0)
    assert lst == [0, 1, 2, 3, 4], "Length 0 should not change list"

    # Test: Edge case - length 1
    lst = [0, 1, 2, 3, 4]
    reverse_circular(lst, 2, 1)
    assert lst == [0, 1, 2, 3, 4], "Length 1 should not change list"

    # Test: Entire list reversal
    lst = [0, 1, 2, 3, 4]
    reverse_circular(lst, 0, 5)
    assert lst == [4, 3, 2, 1, 0], f"Expected [4,3,2,1,0], got {lst}"

    print("✓ reverse_circular tests passed")


def test_example_case():
    lengths = [3, 4, 1, 5]
    final_list = knot_hash(lengths, list_size=5)

    # Verify list is still a permutation
    assert sorted(final_list) == list(range(5)), "List should be permutation of 0-4"

    # Verify expected final state
    assert final_list == [3, 4, 2, 1, 0], f"Expected [3,4,2,1,0], got {final_list}"

    # Verify result
    result = compute_result(final_list)
    print(f"Final list: {final_list}")
    print(f"Result: {final_list[0]} × {final_list[1]} = {result}")

    assert result == 12, f"Expected 12, got {result}"
    print("✓ Example case test passed")


def test_actual_input():
    with open('input.md', 'r') as f:
        input_string = f.read()

    lengths = parse_input(input_string)

    # Verify parsed correctly
    assert len(lengths) == 16, f"Expected 16 lengths, got {len(lengths)}"
    assert lengths[0] == 130, f"First length should be 130, got {lengths[0]}"
    assert lengths[-1] == 224, f"Last length should be 224, got {lengths[-1]}"

    # Run algorithm
    final_list = knot_hash(lengths, list_size=256)

    # Verify list integrity
    assert len(final_list) == 256, "List should still have 256 elements"
    assert sorted(final_list) == list(range(256)), "List should be permutation of 0-255"

    # Compute result
    result = compute_result(final_list)

    # Sanity checks
    assert isinstance(result, int), "Result should be integer"
    assert 0 <= result <= 65025, f"Result {result} out of valid range"

    print(f"First two elements: {final_list[0]}, {final_list[1]}")
    print(f"Final result: {result}")
    print("✓ Actual input test passed")

    return result


def main():
    # Read input
    with open('input.md', 'r') as f:
        input_string = f.read()

    # Parse lengths
    lengths = parse_input(input_string)

    # Execute algorithm
    final_list = knot_hash(lengths)

    # Compute result
    result = compute_result(final_list)

    # Output
    print(result)
    return result


if __name__ == "__main__":
    # Run tests first
    print("Running unit tests...")
    test_parse_input()
    test_initialize_list()
    test_reverse_circular()

    print("\nRunning integration test...")
    test_example_case()

    print("\nRunning actual input test...")
    result = test_actual_input()

    print("\n" + "="*50)
    print("All tests passed!")
    print("="*50)
    print(f"\nFinal Answer: {result}")
