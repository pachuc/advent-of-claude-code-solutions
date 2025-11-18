from solution import is_valid_passphrase

# Read input
with open('input.md', 'r') as f:
    lines = f.read().strip().split('\n')

# Count valid and invalid passphrases
valid_count = 0
invalid_count = 0
invalid_lines = []

for idx, line in enumerate(lines, 1):
    if line.strip():
        if is_valid_passphrase(line):
            valid_count += 1
        else:
            invalid_count += 1
            invalid_lines.append(idx)

print(f"Total lines: {len(lines)}")
print(f"Valid passphrases: {valid_count}")
print(f"Invalid passphrases: {invalid_count}")
print(f"Total passphrases: {valid_count + invalid_count}")
print()
print(f"First 10 invalid lines: {invalid_lines[:10]}")
print()

# Verify against implementation summary which claims 455 valid passphrases
expected = 455
if valid_count == expected:
    print(f"✓ Count matches implementation summary: {expected}")
else:
    print(f"✗ Count mismatch! Expected: {expected}, Got: {valid_count}")
