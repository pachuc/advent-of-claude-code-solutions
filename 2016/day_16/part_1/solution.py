def dragon_curve_step(data):
    """
    Perform one iteration of the dragon curve algorithm.

    Args:
        data: Current binary string

    Returns:
        New binary string after one iteration
    """
    a = data
    b = data[::-1]  # Reverse
    # Flip bits
    b_flipped = ''.join('1' if c == '0' else '0' for c in b)
    return a + '0' + b_flipped


def generate_data(initial_state, disk_length):
    """
    Generate data using dragon curve algorithm until it meets or exceeds disk_length,
    then truncate to exact disk_length.

    Args:
        initial_state: Starting binary string
        disk_length: Target length for the data

    Returns:
        Binary string of exact disk_length
    """
    data = initial_state
    while len(data) < disk_length:
        data = dragon_curve_step(data)
    return data[:disk_length]  # Truncate to exact length


def calculate_checksum_step(data):
    """
    Calculate one iteration of checksum (reduce by half).

    Args:
        data: Binary string to checksum

    Returns:
        Checksum string (half the length of input)
    """
    checksum = []
    for i in range(0, len(data), 2):
        pair = data[i:i+2]
        if pair[0] == pair[1]:
            checksum.append('1')
        else:
            checksum.append('0')
    return ''.join(checksum)


def compute_final_checksum(data):
    """
    Repeatedly calculate checksum until result has odd length.

    Args:
        data: Binary string to checksum

    Returns:
        Final odd-length checksum
    """
    checksum = data
    while len(checksum) % 2 == 0:
        checksum = calculate_checksum_step(checksum)
    return checksum


def read_input(file_path):
    """
    Read initial state from input file.

    Args:
        file_path: Path to input file

    Returns:
        Initial binary string (stripped of whitespace)
    """
    with open(file_path, 'r') as f:
        initial_state = f.read().strip()
    return initial_state


def solve(input_file, disk_length=272):
    """
    Main solution function.

    Args:
        input_file: Path to input file
        disk_length: Length of disk to fill (default 272)

    Returns:
        Final checksum string
    """
    initial_state = read_input(input_file)
    data = generate_data(initial_state, disk_length)
    checksum = compute_final_checksum(data)
    return checksum


if __name__ == '__main__':
    result = solve('input.md')
    print(result)
