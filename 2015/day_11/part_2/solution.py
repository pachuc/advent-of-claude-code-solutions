def increment_password(password: str) -> str:
    """Increment password by one in base-26 (a-z)."""
    chars = list(password)
    i = len(chars) - 1

    while i >= 0:
        if chars[i] == 'z':
            chars[i] = 'a'
            i -= 1
        else:
            chars[i] = chr(ord(chars[i]) + 1)
            break

    return ''.join(chars)


def has_increasing_straight(password: str) -> bool:
    """Check if password has at least one sequence of 3 consecutive letters."""
    for i in range(len(password) - 2):
        if (ord(password[i+1]) == ord(password[i]) + 1 and
            ord(password[i+2]) == ord(password[i+1]) + 1):
            return True
    return False


def has_forbidden_chars(password: str) -> bool:
    """Check if password contains forbidden characters (i, o, l)."""
    return any(c in password for c in 'iol')


def has_two_pairs(password: str) -> bool:
    """Check if password has at least two different, non-overlapping pairs."""
    pairs = set()
    i = 0
    while i < len(password) - 1:
        if password[i] == password[i+1]:
            pairs.add(password[i])
            i += 2  # Skip both characters in the pair
        else:
            i += 1
    return len(pairs) >= 2


def is_valid_password(password: str) -> bool:
    """Check if password meets all three requirements."""
    if has_forbidden_chars(password):
        return False
    if not has_two_pairs(password):
        return False
    if not has_increasing_straight(password):
        return False
    return True


def skip_forbidden_chars(password: str) -> str:
    """Skip ahead past forbidden characters for optimization."""
    chars = list(password)

    # Find leftmost forbidden character
    for i in range(len(chars)):
        if chars[i] in 'iol':
            # Increment the forbidden character
            if chars[i] == 'i':
                chars[i] = 'j'
            elif chars[i] == 'l':
                chars[i] = 'm'
            elif chars[i] == 'o':
                chars[i] = 'p'

            # Set all characters to the right to 'a'
            for j in range(i + 1, len(chars)):
                chars[j] = 'a'
            break

    return ''.join(chars)


def find_next_password(current: str) -> str:
    """Find the next valid password after the current one."""
    password = increment_password(current)

    while True:
        # Skip ahead if forbidden chars present
        if has_forbidden_chars(password):
            password = skip_forbidden_chars(password)
            continue

        # Check all validation rules
        if is_valid_password(password):
            return password

        # Increment and try again
        password = increment_password(password)


def main():
    # Read Part 1 answer as starting password for Part 2
    with open('part_1_answer.txt', 'r') as f:
        current_password = f.read().strip()

    # Find next password
    next_password = find_next_password(current_password)

    # Output result
    print(next_password)


if __name__ == '__main__':
    main()
