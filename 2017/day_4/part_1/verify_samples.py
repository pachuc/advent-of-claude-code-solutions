from solution import is_valid_passphrase

# Test samples from input.md
test_cases = [
    # Line 20 - should be INVALID (duplicate "duciqf")
    ("hmo fdayx duciqf cgt duciqf", False, 20),

    # Line 23 - should be INVALID (duplicate "zekj")
    ("vtjzc ntkh zekj qrbkjhn zekj lyfnbg", False, 23),

    # Line 46 - should be INVALID (duplicates "ivaby" and "vkef")
    ("hnio shccluw cpu ivaby tormn vkef abv vkef ivaby", False, 46),

    # Line 54 - should be INVALID (duplicate "rrol")
    ("oicgs rrol zvnbna rrol", False, 54),

    # Line 1 - should be VALID
    ("bdwdjjo avricm cjbmj ran lmfsom ivsof", True, 1),

    # Line 7 - should be VALID (no exact duplicates)
    ("srceh xdwao reshc shecr", True, 7),
]

print("Manual verification of sample lines:")
print("=" * 60)

all_passed = True
for passphrase, expected, line_num in test_cases:
    result = is_valid_passphrase(passphrase)
    status = "✓ PASS" if result == expected else "✗ FAIL"
    validity = "VALID" if result else "INVALID"

    if result != expected:
        all_passed = False

    print(f"Line {line_num:3d}: {status}")
    print(f"  Expected: {'VALID' if expected else 'INVALID'}")
    print(f"  Got:      {validity}")
    print(f"  Passphrase: {passphrase[:50]}...")
    print()

print("=" * 60)
if all_passed:
    print("✓ All manual verifications PASSED")
else:
    print("✗ Some manual verifications FAILED")
