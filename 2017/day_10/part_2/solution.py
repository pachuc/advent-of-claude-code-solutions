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


def parse_input_as_ascii(input_string):
    """Parse input string as ASCII codes and append standard suffix.

    Args:
        input_string: The input string to convert

    Returns:
        List of ASCII codes with standard suffix appended
    """
    # Strip whitespace
    clean_input = input_string.strip()

    # Convert to ASCII codes
    ascii_codes = [ord(char) for char in clean_input]

    # Append standard suffix
    suffix = [17, 31, 73, 47, 23]
    ascii_codes.extend(suffix)

    return ascii_codes


def knot_hash_rounds(lengths, num_rounds=64, list_size=256):
    """Execute the knot hash algorithm for multiple rounds.

    Args:
        lengths: List of length values to process
        num_rounds: Number of rounds to execute (default 64)
        list_size: Size of the circular list (default 256)

    Returns:
        The final sparse hash (256-element list) after all rounds
    """
    # Initialize
    lst = initialize_list(list_size)
    current_position = 0
    skip_size = 0

    # Run multiple rounds
    for round_num in range(num_rounds):
        for length in lengths:
            # Reverse section
            reverse_circular(lst, current_position, length)

            # Update position (with wrapping)
            current_position = (current_position + length + skip_size) % list_size

            # Increment skip size
            skip_size += 1

    return lst


def create_dense_hash(sparse_hash):
    """Convert 256-element sparse hash to 16-element dense hash via XOR.

    Args:
        sparse_hash: 256-element list

    Returns:
        16-element list where each element is XOR of 16 sparse hash elements
    """
    dense_hash = []
    for i in range(16):
        block = sparse_hash[i*16:(i+1)*16]
        # XOR all elements in the block
        xor_result = block[0]
        for j in range(1, 16):
            xor_result ^= block[j]
        dense_hash.append(xor_result)
    return dense_hash


def to_hex_string(dense_hash):
    """Convert dense hash to 32-character hexadecimal string.

    Args:
        dense_hash: 16-element list of integers (0-255)

    Returns:
        32-character lowercase hexadecimal string
    """
    hex_string = ''.join(format(num, '02x') for num in dense_hash)
    return hex_string


def compute_knot_hash(input_string):
    """Compute the complete Knot Hash of an input string.

    Args:
        input_string: The string to hash

    Returns:
        32-character hexadecimal hash string
    """
    # Step 1: Parse and convert to ASCII
    lengths = parse_input_as_ascii(input_string)

    # Step 2: Run 64 rounds
    sparse_hash = knot_hash_rounds(lengths, num_rounds=64)

    # Step 3: Create dense hash
    dense_hash = create_dense_hash(sparse_hash)

    # Step 4: Convert to hex
    hex_hash = to_hex_string(dense_hash)

    return hex_hash


# Test functions
def test_parse_simple_ascii():
    input_str = "1,2,3"
    result = parse_input_as_ascii(input_str)

    # Expected ASCII codes
    expected_ascii = [49, 44, 50, 44, 51]  # '1', ',', '2', ',', '3'
    expected_with_suffix = [49, 44, 50, 44, 51, 17, 31, 73, 47, 23]

    assert result == expected_with_suffix
    print("✓ Simple ASCII parsing passed")


def test_parse_empty_ascii():
    input_str = ""
    result = parse_input_as_ascii(input_str)

    # Should only have suffix
    expected = [17, 31, 73, 47, 23]

    assert result == expected
    print("✓ Empty string ASCII parsing passed")


def test_hex_conversion_full():
    dense = list(range(16))  # [0, 1, 2, ..., 15]
    result = to_hex_string(dense)

    # Should be "000102030405060708090a0b0c0d0e0f"
    expected = "000102030405060708090a0b0c0d0e0f"
    assert result == expected
    assert len(result) == 32

    print("✓ Full hex conversion test passed")


def test_dense_hash_xor():
    # Example from problem statement
    sparse_block = [65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]

    # Create sparse hash with this as first block
    sparse_hash = sparse_block + [0] * 240  # Fill rest with zeros

    dense = create_dense_hash(sparse_hash)

    # First element should be 64 (from problem statement)
    expected_first = 65 ^ 27 ^ 9 ^ 1 ^ 4 ^ 3 ^ 40 ^ 50 ^ 91 ^ 7 ^ 6 ^ 0 ^ 2 ^ 5 ^ 68 ^ 22
    assert expected_first == 64, f"Expected 64, calculated {expected_first}"
    assert dense[0] == 64

    # Verify length
    assert len(dense) == 16

    # All other blocks XOR to 0 (since all elements are 0)
    for i in range(1, 16):
        assert dense[i] == 0

    print("✓ Dense hash XOR test passed")


def test_example_empty_string():
    input_str = ""
    result = compute_knot_hash(input_str)
    expected = "a2582a3a0e66e6e86e3812dcb672a272"

    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 32
    print("✓ Empty string example passed")


def test_example_aoc_2017():
    input_str = "AoC 2017"
    result = compute_knot_hash(input_str)
    expected = "33efeb34ea91902bb2f59c9920caa6cd"

    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 32
    print("✓ 'AoC 2017' example passed")


def test_example_1_2_3():
    input_str = "1,2,3"
    result = compute_knot_hash(input_str)
    expected = "3efbe78a8d82f29979031a4aa0b16a9d"

    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 32
    print("✓ '1,2,3' example passed")


def test_example_1_2_4():
    input_str = "1,2,4"
    result = compute_knot_hash(input_str)
    expected = "63960835bcdc130f0b66d7ff4f6a5a8e"

    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 32
    print("✓ '1,2,4' example passed")


def test_actual_puzzle_input():
    with open('input.md', 'r') as f:
        input_string = f.read()

    result = compute_knot_hash(input_string)

    # Validation checks (no known answer yet)
    assert isinstance(result, str), "Result must be string"
    assert len(result) == 32, f"Result must be 32 chars, got {len(result)}"

    # Verify hex format
    valid_hex_chars = set('0123456789abcdef')
    assert all(c in valid_hex_chars for c in result), "Invalid hex characters"

    # Verify lowercase
    assert result == result.lower(), "Hash must be lowercase"

    print(f"Actual input hash: {result}")
    print("✓ Actual puzzle input validation passed")

    return result


def main():
    # Read input
    with open('input.md', 'r') as f:
        input_string = f.read()

    # Compute hash
    result = compute_knot_hash(input_string)

    # Output
    print(result)
    return result


if __name__ == "__main__":
    # Run tests first
    print("Running unit tests...")
    test_parse_simple_ascii()
    test_parse_empty_ascii()
    test_hex_conversion_full()
    test_dense_hash_xor()

    print("\nTesting examples...")
    test_example_empty_string()
    test_example_aoc_2017()
    test_example_1_2_3()
    test_example_1_2_4()

    print("\nTesting actual puzzle input...")
    result = test_actual_puzzle_input()

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print(f"FINAL ANSWER: {result}")
    print("="*50)
