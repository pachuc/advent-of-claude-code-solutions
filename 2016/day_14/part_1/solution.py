import hashlib

def generate_hash(salt, index):
    """Generate MD5 hash for salt + index."""
    text = salt + str(index)
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def find_first_triplet(hash_str):
    """Find the first character that appears three times in a row."""
    for i in range(len(hash_str) - 2):
        if hash_str[i] == hash_str[i+1] == hash_str[i+2]:
            return hash_str[i]
    return None

def contains_quintuplet(hash_str, char):
    """Check if hash contains five consecutive occurrences of char."""
    return char * 5 in hash_str

def get_hash(salt, index, cache):
    """Get hash from cache or generate and cache it."""
    if index not in cache:
        cache[index] = generate_hash(salt, index)
    return cache[index]

def is_valid_key(salt, index, hash_cache):
    """Check if the hash at index is a valid key."""
    # Get hash for current index
    current_hash = get_hash(salt, index, hash_cache)

    # Find first triplet
    triplet_char = find_first_triplet(current_hash)
    if triplet_char is None:
        return False

    # Check next 1000 hashes for quintuplet
    for future_index in range(index + 1, index + 1001):
        future_hash = get_hash(salt, future_index, hash_cache)
        if contains_quintuplet(future_hash, triplet_char):
            return True

    return False

def find_64th_key(salt):
    """Find the index that produces the 64th valid key."""
    hash_cache = {}
    keys_found = 0
    current_index = 0

    while keys_found < 64:
        if is_valid_key(salt, current_index, hash_cache):
            keys_found += 1
            if keys_found == 64:
                return current_index
        current_index += 1

    return current_index

if __name__ == "__main__":
    # Read salt from input
    with open('input.md', 'r') as f:
        salt = f.read().strip()

    # Find 64th key
    result = find_64th_key(salt)

    # Print result
    print(result)
