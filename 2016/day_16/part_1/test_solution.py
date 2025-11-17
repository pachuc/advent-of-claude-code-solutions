import tempfile
import os
from solution import (
    dragon_curve_step,
    generate_data,
    calculate_checksum_step,
    compute_final_checksum,
    solve
)


def test_dragon_curve_step():
    """Test single iteration of dragon curve algorithm"""
    print("Testing dragon_curve_step...")
    assert dragon_curve_step("1") == "100", "Test 1 failed"
    assert dragon_curve_step("0") == "001", "Test 0 failed"
    assert dragon_curve_step("11111") == "11111000000", "Test 11111 failed"
    assert dragon_curve_step("111100001010") == "1111000010100101011110000", "Test 111100001010 failed"
    print("✓ All dragon_curve_step tests passed")


def test_bit_flipping():
    """Ensure bit flipping is correct (not just reversal)"""
    print("Testing bit flipping...")
    # For input "10", reversed is "01", flipped is "10"
    # Result should be "10" + "0" + "10" = "10010"
    result = dragon_curve_step("10")
    assert result == "10010", f"Expected '10010', got '{result}'"

    # For input "01", reversed is "10", flipped is "01"
    # Result should be "01" + "0" + "01" = "01001"
    result = dragon_curve_step("01")
    assert result == "01001", f"Expected '01001', got '{result}'"
    print("✓ All bit flipping tests passed")


def test_generate_data():
    """Test data generation expands and truncates correctly"""
    print("Testing generate_data...")

    # Test from problem example
    result = generate_data("10000", 20)
    assert len(result) == 20, f"Length should be 20, got {len(result)}"
    assert result == "10000011110010000111", f"Expected '10000011110010000111', got '{result}'"

    # Test various lengths
    result = generate_data("1", 5)
    assert len(result) == 5, f"Length should be 5, got {len(result)}"

    result = generate_data("11111", 11)
    assert len(result) == 11, f"Length should be 11, got {len(result)}"
    assert result == "11111000000", f"Expected '11111000000', got '{result}'"

    # Test edge case: initial state already meets disk length
    result = generate_data("10101", 5)
    assert len(result) == 5, f"Length should be 5, got {len(result)}"
    assert result == "10101", f"Expected '10101', got '{result}'"

    # Test edge case: initial state exceeds disk length
    result = generate_data("11111000000", 5)
    assert len(result) == 5, f"Length should be 5, got {len(result)}"
    assert result == "11111", f"Expected '11111', got '{result}'"

    print("✓ All generate_data tests passed")


def test_calculate_checksum_step():
    """Test one iteration of checksum calculation"""
    print("Testing calculate_checksum_step...")
    assert calculate_checksum_step("110010110100") == "110101", "Test 1 failed"
    assert calculate_checksum_step("110101") == "100", "Test 2 failed"
    assert calculate_checksum_step("11") == "1", "Test 3 failed"
    assert calculate_checksum_step("01") == "0", "Test 4 failed"
    assert calculate_checksum_step("1100") == "11", "Test 5 failed"  # 11 matches, 00 matches -> 11
    print("✓ All calculate_checksum_step tests passed")


def test_compute_final_checksum():
    """Test checksum loop terminates at odd length"""
    print("Testing compute_final_checksum...")

    # From problem examples
    result = compute_final_checksum("110010110100")
    assert result == "100", f"Expected '100', got '{result}'"
    assert len(result) % 2 == 1, "Result must have odd length"

    result = compute_final_checksum("10000011110010000111")
    assert result == "01100", f"Expected '01100', got '{result}'"
    assert len(result) % 2 == 1, "Result must have odd length"

    print("✓ All compute_final_checksum tests passed")


def test_complete_example():
    """Validate end-to-end solution with provided example"""
    print("Testing complete example...")

    # Create temporary test input
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("10000")
        temp_path = f.name

    try:
        result = solve(temp_path, disk_length=20)
        assert result == "01100", f"Expected '01100', got '{result}'"
        assert len(result) % 2 == 1, "Result must have odd length"
        print("✓ Complete example test passed")
    finally:
        os.unlink(temp_path)


def test_checksum_progression():
    """Verify checksum reduces correctly for disk length 272"""
    print("Testing checksum progression for actual input...")

    # Generate data of length 272
    data = generate_data("11011110011011101", 272)
    assert len(data) == 272, f"Data length should be 272, got {len(data)}"

    # Manually track iterations
    checksum = data
    lengths = [len(checksum)]

    while len(checksum) % 2 == 0:
        checksum = calculate_checksum_step(checksum)
        lengths.append(len(checksum))

    # Verify progression: 272 = 16 × 17, so 272 → 136 → 68 → 34 → 17
    assert lengths == [272, 136, 68, 34, 17], f"Expected [272, 136, 68, 34, 17], got {lengths}"
    assert len(checksum) == 17, f"Final checksum length should be 17, got {len(checksum)}"
    assert len(checksum) % 2 == 1, "Final checksum must have odd length"

    print("✓ Checksum progression test passed")


def test_generation_iterations():
    """Verify number of dragon curve iterations for actual input"""
    print("Testing generation iterations...")

    data = "11011110011011101"
    lengths = [len(data)]

    # Manually verify first iteration for content correctness
    first_iteration = dragon_curve_step(data)
    # data reversed: "10111011001111011"
    # data flipped:  "01000100110000100"
    expected_first = "11011110011011101" + "0" + "01000100110000100"
    assert first_iteration == expected_first, f"First iteration content mismatch"

    # Continue tracking lengths
    data = first_iteration
    lengths.append(len(data))

    while len(data) < 272:
        data = dragon_curve_step(data)
        lengths.append(len(data))

    # Verify iteration count and final length
    # Expected: 17 → 35 → 71 → 143 → 287
    assert lengths == [17, 35, 71, 143, 287], f"Expected [17, 35, 71, 143, 287], got {lengths}"
    assert len(data) >= 272, f"Final data length should be >= 272, got {len(data)}"

    print("✓ Generation iterations test passed")


def test_minimal_cases():
    """Test boundary conditions"""
    print("Testing minimal cases...")

    # Already at disk length
    result = generate_data("1", 1)
    assert result == "1", f"Expected '1', got '{result}'"

    result = generate_data("0", 1)
    assert result == "0", f"Expected '0', got '{result}'"

    # One iteration needed
    result = generate_data("1", 3)
    assert result == "100", f"Expected '100', got '{result}'"

    print("✓ All minimal cases tests passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running all tests...")
    print("=" * 60)

    test_dragon_curve_step()
    test_bit_flipping()
    test_generate_data()
    test_calculate_checksum_step()
    test_compute_final_checksum()
    test_complete_example()
    test_minimal_cases()
    test_generation_iterations()
    test_checksum_progression()

    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
