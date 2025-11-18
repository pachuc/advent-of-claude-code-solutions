def is_valid_passphrase(passphrase):
    """
    Check if passphrase has no words that are anagrams of each other.

    Two words are anagrams if they contain the same letters with same frequencies.
    We detect this by sorting the letters of each word and comparing.

    Args:
        passphrase (str): A space-separated string of words

    Returns:
        bool: True if valid (no anagrams), False otherwise
    """
    words = passphrase.split()

    # Create canonical form of each word by sorting its letters
    canonical_forms = [''.join(sorted(word)) for word in words]

    # Check if all canonical forms are unique
    # If any two words have the same sorted form, they are anagrams
    return len(canonical_forms) == len(set(canonical_forms))


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
