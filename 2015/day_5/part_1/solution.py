def read_input(filename):
    """Read strings from input file, filtering empty lines."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def has_three_vowels(s):
    """Check if string contains at least 3 vowels (a, e, i, o, u)."""
    vowels = {'a', 'e', 'i', 'o', 'u'}
    count = sum(1 for char in s if char in vowels)
    return count >= 3


def has_double_letter(s):
    """Check if string contains at least one pair of consecutive identical letters."""
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            return True
    return False


def no_forbidden_substrings(s):
    """Check that string does NOT contain ab, cd, pq, or xy."""
    forbidden = ['ab', 'cd', 'pq', 'xy']
    for substring in forbidden:
        if substring in s:
            return False
    return True


def is_nice(s):
    """Determine if a string is 'nice' by checking all three criteria."""
    return (no_forbidden_substrings(s) and
            has_double_letter(s) and
            has_three_vowels(s))


def count_nice_strings(filename):
    """Count total nice strings in input file."""
    strings = read_input(filename)
    nice_count = sum(1 for s in strings if is_nice(s))
    return nice_count


if __name__ == '__main__':
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    result = count_nice_strings(filename)
    print(result)
