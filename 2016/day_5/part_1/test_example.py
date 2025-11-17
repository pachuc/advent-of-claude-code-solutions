import hashlib

# Test with example door ID 'abc' - should produce '18f47a30'
PASSWORD_LENGTH = 8
door_id = 'abc'

index = 0
password = []
found_hashes = []

print(f"Testing with example door ID: {door_id}")
print(f"Expected password: 18f47a30")
print(f"{'='*60}")

while len(password) < PASSWORD_LENGTH:
    if index > 0 and index % 1_000_000 == 0:
        print(f"Checked {index:,} hashes, found {len(password)}/{PASSWORD_LENGTH} characters...")

    hash_input = (door_id + str(index)).encode()
    hash_result = hashlib.md5(hash_input).hexdigest()

    if hash_result.startswith('00000'):
        char = hash_result[5]
        password.append(char)
        found_hashes.append((index, hash_result, char))
        print(f"Found character {len(password)}/{PASSWORD_LENGTH}: '{char}' at index {index:,} (hash: {hash_result[:10]}...)")

    index += 1

final_password = ''.join(password)
print(f"{'='*60}")
print(f"\nActual password:   {final_password}")
print(f"Expected password: 18f47a30")
print(f"Match: {final_password == '18f47a30'}")

if final_password == '18f47a30':
    print("\n✓ TEST PASSED - Example verification successful!")
else:
    print("\n✗ TEST FAILED - Password mismatch!")
