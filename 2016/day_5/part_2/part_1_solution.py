import hashlib

# Constants
PASSWORD_LENGTH = 8
PROGRESS_INTERVAL = 1_000_000

# Read input
with open('input.md', 'r') as f:
    door_id = f.read().strip()

# Validate input
assert door_id, "Door ID cannot be empty"

# Initialize
index = 0
password = []
found_hashes = []

print(f"Searching for password with door ID: {door_id}")
print(f"{'='*60}")

# Main loop
while len(password) < PASSWORD_LENGTH:
    # Periodic progress output
    if index > 0 and index % PROGRESS_INTERVAL == 0:
        print(f"Checked {index:,} hashes, found {len(password)}/{PASSWORD_LENGTH} characters...")

    # Create hash input
    hash_input = (door_id + str(index)).encode()

    # Compute MD5
    hash_result = hashlib.md5(hash_input).hexdigest()

    # Check for five leading zeros
    if hash_result.startswith('00000'):
        # Extract 6th character
        char = hash_result[5]
        password.append(char)
        found_hashes.append((index, hash_result, char))
        print(f"Found character {len(password)}/{PASSWORD_LENGTH}: '{char}' at index {index:,} (hash: {hash_result[:10]}...)")

    index += 1

# Validate and output result
final_password = ''.join(password)
assert all(c in '0123456789abcdef' for c in final_password), "Invalid characters in password"

print(f"{'='*60}")
print(f"\nPassword: {final_password}")
print(f"\nTotal indices checked: {index:,}")

# Verify all hashes
print(f"\n{'='*60}")
print("Verification:")
for idx, hash_val, char in found_hashes:
    # Re-verify hash
    reverify = hashlib.md5((door_id + str(idx)).encode()).hexdigest()
    assert reverify == hash_val, f"Hash changed on recomputation at {idx}"
    assert reverify.startswith('00000'), f"Hash at {idx} doesn't start with 00000"
    assert reverify[5] == char, f"Character mismatch at {idx}"
    print(f"✓ Index {idx:,}: {hash_val[:10]}... -> '{char}'")

print(f"{'='*60}")
print("All validations passed!")
