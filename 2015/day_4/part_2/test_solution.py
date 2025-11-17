import hashlib
from solution import find_adventcoin


def test_known_examples():
    """Test with known examples from Advent of Code 2015 Day 4 Part 1."""
    print("Testing with known examples (5 zeroes):")
    print("-" * 50)

    # Test case 1: abcdef
    print("Test 1: secret_key='abcdef', expected=609043")
    result1 = find_adventcoin("abcdef", num_zeroes=5)
    print(f"Result: {result1}")
    # Verify the hash
    hash1 = hashlib.md5(f"abcdef{result1}".encode()).hexdigest()
    print(f"Hash: {hash1}")
    print(f"Starts with 5 zeroes: {hash1.startswith('00000')}")
    assert result1 == 609043, f"Expected 609043, got {result1}"
    print("✓ PASSED\n")

    # Test case 2: pqrstuv
    print("Test 2: secret_key='pqrstuv', expected=1048970")
    result2 = find_adventcoin("pqrstuv", num_zeroes=5)
    print(f"Result: {result2}")
    # Verify the hash
    hash2 = hashlib.md5(f"pqrstuv{result2}".encode()).hexdigest()
    print(f"Hash: {hash2}")
    print(f"Starts with 5 zeroes: {hash2.startswith('00000')}")
    assert result2 == 1048970, f"Expected 1048970, got {result2}"
    print("✓ PASSED\n")

    print("=" * 50)
    print("All tests passed! Algorithm is correct.")
    print("=" * 50)


if __name__ == "__main__":
    test_known_examples()
