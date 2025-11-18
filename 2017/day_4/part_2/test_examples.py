from solution import is_valid_passphrase

# Test cases from problem.md
test_cases = [
    ("abcde fghij", True, "No words are anagrams of each other"),
    ("abcde xyz ecdab", False, "'ecdab' is an anagram of 'abcde'"),
    ("a ab abc abd abf abj", True, "All letters must be used, so these are not anagrams"),
    ("iiii oiii ooii oooi oooo", True, "None of these are anagrams of each other"),
    ("oiii ioii iioi iiio", False, "All of these words can be rearranged to form any other"),
]

print("Testing provided examples from problem.md:")
print("=" * 60)

all_passed = True
for i, (passphrase, expected, reason) in enumerate(test_cases, 1):
    result = is_valid_passphrase(passphrase)
    status = "PASS" if result == expected else "FAIL"

    if result != expected:
        all_passed = False

    print(f"\nTest {i}: {status}")
    print(f"  Input: {passphrase}")
    print(f"  Expected: {'VALID' if expected else 'INVALID'}")
    print(f"  Got: {'VALID' if result else 'INVALID'}")
    print(f"  Reason: {reason}")

    # Debug info for failures
    if result != expected:
        words = passphrase.split()
        sorted_forms = [''.join(sorted(word)) for word in words]
        print(f"  DEBUG - Words: {words}")
        print(f"  DEBUG - Sorted forms: {sorted_forms}")

print("\n" + "=" * 60)
if all_passed:
    print("All tests PASSED!")
else:
    print("Some tests FAILED!")
