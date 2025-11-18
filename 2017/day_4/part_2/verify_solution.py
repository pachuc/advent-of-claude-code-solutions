from solution import is_valid_passphrase

# Read the input
with open('input.md', 'r') as f:
    lines = f.read().strip().split('\n')

# Test line 7 specifically mentioned in test_plan.md
# Line 7: srceh xdwao reshc shecr
# Expected: INVALID (reshc and shecr are anagrams of srceh)
line_7 = lines[6]  # 0-indexed
print(f"Line 7: {line_7}")
print(f"Is valid: {is_valid_passphrase(line_7)}")

words = line_7.split()
sorted_forms = [''.join(sorted(word)) for word in words]
print(f"Words: {words}")
print(f"Sorted forms: {sorted_forms}")
print()

# Test line 1
line_1 = lines[0]
print(f"Line 1: {line_1}")
print(f"Is valid: {is_valid_passphrase(line_1)}")

words = line_1.split()
sorted_forms = [''.join(sorted(word)) for word in words]
print(f"Words: {words}")
print(f"Sorted forms: {sorted_forms}")
print()

# Count total valid
valid_count = sum(1 for line in lines if line.strip() and is_valid_passphrase(line))
print(f"Total valid passphrases: {valid_count}")

# Verify it's less than 455
if valid_count < 455:
    print("✓ Result is less than Part 1 answer (455) - CORRECT!")
else:
    print("✗ Result should be less than 455!")
