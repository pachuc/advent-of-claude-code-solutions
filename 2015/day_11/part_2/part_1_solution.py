def increment_password(password: str) -> str:
    """
    Increment password by 1 in base-26, with forbidden character optimization.
    If increment produces 'i', 'o', or 'l', skip to next valid char and reset right positions.
    """
    chars = list(password)
    i = len(chars) - 1

    # Increment from rightmost position
    while i >= 0:
        if chars[i] == 'z':
            chars[i] = 'a'
            i -= 1  # Carry to next position
        else:
            # Increment current character
            chars[i] = chr(ord(chars[i]) + 1)

            # Optimization: skip forbidden characters
            if chars[i] == 'i':
                chars[i] = 'j'
                # Reset all positions to the right
                for j in range(i + 1, len(chars)):
                    chars[j] = 'a'
            elif chars[i] == 'o':
                chars[i] = 'p'
                # Reset all positions to the right
                for j in range(i + 1, len(chars)):
                    chars[j] = 'a'
            elif chars[i] == 'l':
                chars[i] = 'm'
                # Reset all positions to the right
                for j in range(i + 1, len(chars)):
                    chars[j] = 'a'

            break

    return ''.join(chars)


def has_no_forbidden_chars(password: str) -> bool:
    """Check if password contains no forbidden characters (i, o, l)."""
    return not any(c in password for c in 'iol')


def has_increasing_straight(password: str) -> bool:
    """Check if password has at least one sequence of three consecutive increasing letters."""
    for i in range(len(password) - 2):
        if ord(password[i+1]) == ord(password[i]) + 1 and ord(password[i+2]) == ord(password[i]) + 2:
            return True
    return False


def has_two_pairs(password: str) -> bool:
    """Check if password has at least two different non-overlapping pairs."""
    pairs_found = []
    i = 0

    while i < len(password) - 1:
        if password[i] == password[i+1]:
            pairs_found.append(password[i])
            i += 2  # Skip ahead to avoid overlap
        else:
            i += 1

    # Count unique pairs
    return len(set(pairs_found)) >= 2


def is_valid_password(password: str) -> bool:
    """Check if password meets all three validation requirements."""
    return (has_no_forbidden_chars(password) and
            has_increasing_straight(password) and
            has_two_pairs(password))


def find_next_password(current: str) -> str:
    """Find the next valid password after the current one."""
    password = increment_password(current)
    iterations = 0
    MAX_ITERATIONS = 10_000_000

    while iterations < MAX_ITERATIONS:
        if is_valid_password(password):
            return password
        password = increment_password(password)
        iterations += 1

    raise Exception("Max iterations exceeded")


if __name__ == "__main__":
    # Read input
    with open('input.md', 'r') as f:
        current_password = f.read().strip()

    # Find next valid password
    next_password = find_next_password(current_password)

    # Output result
    print(next_password)
