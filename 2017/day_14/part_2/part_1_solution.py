"""
Disk Defragmentation Grid Analysis - Advent of Code 2017 Day 14 Part 1
Count the total number of used squares in a 128x128 grid.
"""

# ============================================================================
# Knot Hash Functions (from Day 10 Part 2)
# ============================================================================

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


# ============================================================================
# Day 14 Part 1 Functions
# ============================================================================

def hex_to_binary(hex_string):
    """Convert hexadecimal string to binary string.

    Args:
        hex_string: Hexadecimal string

    Returns:
        Binary string with 4 bits per hex character
    """
    return ''.join(format(int(c, 16), '04b') for c in hex_string)


def generate_row_input(key, row_number):
    """Generate input string for a specific row.

    Args:
        key: The key string
        row_number: Row number (0-127)

    Returns:
        Formatted string "{key}-{row_number}"
    """
    return f"{key}-{row_number}"


def count_used_bits(binary_string):
    """Count number of '1' bits in binary string.

    Args:
        binary_string: Binary string

    Returns:
        Count of '1' characters
    """
    return binary_string.count('1')


def calculate_used_squares(key):
    """Calculate total number of used squares in the 128x128 grid.

    Args:
        key: The key string

    Returns:
        Total count of used squares (1 bits)
    """
    total_used = 0

    for row in range(128):
        # Generate row input
        row_input = generate_row_input(key, row)

        # Compute knot hash
        hash_hex = compute_knot_hash(row_input)

        # Convert to binary
        hash_binary = hex_to_binary(hash_hex)

        # Count used bits
        used_count = count_used_bits(hash_binary)

        # Accumulate
        total_used += used_count

    return total_used


# ============================================================================
# Test Functions
# ============================================================================

def test_knot_hash():
    """Test knot hash implementation with known value"""
    # Test case 1.1a - verify algorithm correctness
    result = compute_knot_hash('')
    expected = 'a2582a3a0e66e6e86e3812dcb672a272'
    assert result == expected, f"Knot hash failed: expected {expected}, got {result}"

    # Test case 1.1b - verify format for actual input
    result = compute_knot_hash('flqrgnkx-0')
    assert isinstance(result, str), "Hash must be string"
    assert len(result) == 32, f"Hash must be 32 chars, got {len(result)}"
    assert all(c in '0123456789abcdef' for c in result), "Hash must be lowercase hex"

    print("✓ Knot hash tests passed")


def test_hex_to_binary():
    """Test hex to binary conversion"""
    # Test cases 2.1 - single and multi-character hex strings
    assert hex_to_binary('0') == '0000', "Single '0' failed"
    assert hex_to_binary('f') == '1111', "Single 'f' failed"
    assert hex_to_binary('a') == '1010', "Single 'a' failed"
    assert hex_to_binary('00') == '00000000', "Double '00' failed"
    assert hex_to_binary('ff') == '11111111', "Double 'ff' failed"

    # Test case 2.2 - full hash with all zeros
    assert hex_to_binary('0' * 32) == '0' * 128, "All zeros failed"

    # Test case 2.3 - full hash with all ones
    assert hex_to_binary('f' * 32) == '1' * 128, "All ones failed"

    # Test case 2.4 - mixed hex string
    assert hex_to_binary('a0c2') == '1010000011000010', "Mixed hex failed"

    # Test case 2.5 - leading zeros preservation
    result = hex_to_binary('0' + 'f' * 31)
    assert result[:4] == '0000', "Leading zeros not preserved"
    assert len(result) == 128, f"Length should be 128, got {len(result)}"

    print("✓ Hex to binary conversion tests passed")


def test_generate_row_input():
    """Test row input generation"""
    # Test cases 3.1-3.4
    assert generate_row_input('jxqlasbh', 0) == 'jxqlasbh-0', "Row 0 failed"
    assert generate_row_input('jxqlasbh', 127) == 'jxqlasbh-127', "Row 127 failed"
    assert generate_row_input('flqrgnkx', 0) == 'flqrgnkx-0', "Example key failed"
    assert '-' in generate_row_input('test', 10), "Missing hyphen separator"

    print("✓ Row input generation tests passed")


def test_count_used_bits():
    """Test bit counting"""
    # Test cases 4.1-4.5
    assert count_used_bits('0' * 128) == 0, "All zeros should be 0"
    assert count_used_bits('1' * 128) == 128, "All ones should be 128"
    assert count_used_bits('10' * 64) == 64, "Alternating pattern failed"
    assert count_used_bits('0' * 127 + '1') == 1, "Single one failed"
    assert count_used_bits('10100000110000100000000101110000') == 9, "Known pattern failed"

    print("✓ Bit counting tests passed")


def test_example_case():
    """Test with known example"""
    # Test case 5.1
    result = calculate_used_squares('flqrgnkx')
    expected = 8108
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Example case passed: {result} used squares")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main function to compute the solution."""
    # Read input
    with open('input.md', 'r') as f:
        key = f.read().strip()

    # Calculate result
    result = calculate_used_squares(key)

    # Output result
    print(result)
    return result


if __name__ == "__main__":
    print("Running tests...\n")

    # Run unit tests
    print("Unit tests:")
    test_knot_hash()
    test_hex_to_binary()
    test_generate_row_input()
    test_count_used_bits()

    print("\nIntegration test:")
    test_example_case()

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)

    # Compute actual answer
    print("\nComputing answer for actual input...")
    with open('input.md', 'r') as f:
        key = f.read().strip()

    result = calculate_used_squares(key)

    print(f"\nFINAL ANSWER: {result}")
