def is_valid_passphrase(passphrase):
    """
    Check if passphrase has no duplicate words.

    Args:
        passphrase (str): A space-separated string of words

    Returns:
        bool: True if valid (no duplicates), False otherwise
    """
    words = passphrase.split()
    return len(words) == len(set(words))


def main():
    # Read input
    with open('input.md', 'r') as f:
        lines = f.read().strip().split('\n')

    # Count valid passphrases
    valid_count = sum(1 for line in lines if line.strip() and is_valid_passphrase(line))

    # Output result
    print(valid_count)


if __name__ == "__main__":
    main()
