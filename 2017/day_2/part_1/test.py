from solution import calculate_checksum
import tempfile
import os


def test_case(input_data, expected, description):
    """Test a single case by writing data to temp file and running solution."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(input_data)
        temp_file = f.name

    try:
        result = calculate_checksum(temp_file)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: {description}")
        if result != expected:
            print(f"  Expected: {expected}, Got: {result}")
        return result == expected
    finally:
        os.unlink(temp_file)


# Run all tests
print("Running edge case tests...")
print()

all_pass = True
all_pass &= test_case("5 1 9 5\n7 5 3\n2 4 6 8\n", 18, "Test 1: Provided example")
all_pass &= test_case("10 20 5 15\n", 15, "Test 2: Single row")
all_pass &= test_case("100\n200 50\n", 150, "Test 3: Single value row")
all_pass &= test_case("5 5 5 5\n10 20 30\n", 20, "Test 4: Identical values")
all_pass &= test_case("-5 10 -20\n0 5 -3\n", 38, "Test 5: Negative numbers")
all_pass &= test_case("1000000 1\n", 999999, "Test 6: Large numbers")
all_pass &= test_case("5 10 15\n\n20 25 30\n\n", 20, "Test 7: Empty lines")

print()
print(f"All tests {'PASSED' if all_pass else 'FAILED'}")
