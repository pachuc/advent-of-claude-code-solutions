import hashlib

def read_input(filename='input.md'):
    """Read and parse the secret key from input file."""
    with open(filename, 'r') as f:
        secret_key = f.read().strip()
    return secret_key

def compute_md5_hex(text):
    """Compute MD5 hash and return hexadecimal representation."""
    return hashlib.md5(text.encode()).hexdigest()

def starts_with_five_zeroes(hex_hash):
    """Check if hash starts with five zeroes."""
    return hex_hash.startswith('00000')

def find_advent_coin(secret_key):
    """Find lowest positive integer that produces hash with five leading zeroes."""
    number = 1
    while True:
        combined = secret_key + str(number)
        hash_result = compute_md5_hex(combined)

        if starts_with_five_zeroes(hash_result):
            return number

        number += 1

if __name__ == '__main__':
    secret_key = read_input()
    result = find_advent_coin(secret_key)
    print(result)
