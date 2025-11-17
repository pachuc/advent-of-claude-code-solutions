import hashlib

# Verify the answer
secret_key = "ckczppom"
answer = 3938038

print("=" * 60)
print("VERIFICATION OF ANSWER")
print("=" * 60)

# Check n (the answer)
test_string_n = f"{secret_key}{answer}"
hash_n = hashlib.md5(test_string_n.encode()).hexdigest()
print(f"\nn = {answer}")
print(f"String: {test_string_n}")
print(f"Hash: {hash_n}")
print(f"Starts with 000000: {hash_n.startswith('000000')}")
print(f"Leading zeroes count: {len(hash_n) - len(hash_n.lstrip('0'))}")

# Check n-1 (should NOT have 6 leading zeroes)
test_string_n_minus_1 = f"{secret_key}{answer - 1}"
hash_n_minus_1 = hashlib.md5(test_string_n_minus_1.encode()).hexdigest()
print(f"\nn - 1 = {answer - 1}")
print(f"String: {test_string_n_minus_1}")
print(f"Hash: {hash_n_minus_1}")
print(f"Starts with 000000: {hash_n_minus_1.startswith('000000')}")
print(f"Leading zeroes count: {len(hash_n_minus_1) - len(hash_n_minus_1.lstrip('0'))}")

print("\n" + "=" * 60)
print("VERIFICATION RESULT")
print("=" * 60)
if hash_n.startswith('000000') and not hash_n_minus_1.startswith('000000'):
    print("✓ VERIFIED: Answer is correct!")
    print(f"  - {answer} produces a hash with 6+ leading zeroes")
    print(f"  - {answer - 1} does NOT produce a hash with 6 leading zeroes")
    print(f"  - Therefore, {answer} is the LOWEST integer satisfying the condition")
else:
    print("✗ FAILED: Answer verification failed!")
print("=" * 60)
