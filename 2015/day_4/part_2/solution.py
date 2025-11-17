import hashlib


def read_input(filename='input.md'):
    """Read and parse the secret key from input file."""
    with open(filename, 'r') as f:
        secret_key = f.read().strip()
    return secret_key


def find_adventcoin(secret_key, num_zeroes=6):
    """
    Find the lowest positive integer that, when appended to secret_key,
    produces an MD5 hash starting with the specified number of zeroes.

    Args:
        secret_key: The secret key string
        num_zeroes: Number of leading zeroes required in hex hash

    Returns:
        The lowest positive integer satisfying the condition
    """
    n = 1
    prefix = '0' * num_zeroes

    while True:
        # Concatenate secret key with current integer
        test_string = f"{secret_key}{n}"

        # Compute MD5 hash
        hash_object = hashlib.md5(test_string.encode())
        hash_hex = hash_object.hexdigest()

        # Check if hash starts with required number of zeroes
        if hash_hex.startswith(prefix):
            return n

        # Progress indicator for long-running searches
        if n % 100000 == 0:
            print(f"Checked {n:,} candidates...")

        n += 1


def main():
    """Main execution logic."""
    # Read input
    secret_key = read_input('input.md')
    print(f"Secret key: {secret_key}")

    # Find the answer
    print("Searching for hash with 6 leading zeroes...")
    result = find_adventcoin(secret_key, num_zeroes=6)

    # Output the result
    print(f"\nAnswer: {result}")

    # Verify the result
    test_string = f"{secret_key}{result}"
    hash_hex = hashlib.md5(test_string.encode()).hexdigest()
    print(f"Hash: {hash_hex}")
    print(f"Verification: Hash starts with {'000000' if hash_hex.startswith('000000') else 'INVALID'}")


if __name__ == "__main__":
    main()
