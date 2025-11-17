from solution import (
    has_increasing_straight,
    has_forbidden_chars,
    has_two_pairs,
    is_valid_password
)

# The result from running the solution
result = "vzbxxyzz"

print(f"Verifying output: {result}")
print(f"Input was: vzbxkghb")
print()

# Verify basic properties
print("Basic checks:")
print(f"  Length is 8: {len(result) == 8}")
print(f"  All lowercase: {result.islower()}")
print(f"  Comes after input: {result > 'vzbxkghb'}")
print()

# Verify three requirements
print("Requirement 1: Has increasing straight")
print(f"  Result: {has_increasing_straight(result)}")
if has_increasing_straight(result):
    # Find the straight
    for i in range(len(result) - 2):
        if (ord(result[i+1]) == ord(result[i]) + 1 and
            ord(result[i+2]) == ord(result[i+1]) + 1):
            print(f"  Found: '{result[i:i+3]}' at positions {i}-{i+2}")
print()

print("Requirement 2: No forbidden characters (i, o, l)")
print(f"  Has forbidden chars: {has_forbidden_chars(result)}")
print(f"  Contains 'i': {'i' in result}")
print(f"  Contains 'o': {'o' in result}")
print(f"  Contains 'l': {'l' in result}")
print()

print("Requirement 3: Two different, non-overlapping pairs")
print(f"  Has two pairs: {has_two_pairs(result)}")
# Find the pairs
pairs = []
i = 0
while i < len(result) - 1:
    if result[i] == result[i+1]:
        pairs.append((result[i], i))
        i += 2
    else:
        i += 1
print(f"  Found pairs: {[(p[0]*2, f'at positions {p[1]}-{p[1]+1}') for p in pairs]}")
print()

print("="*50)
print(f"Overall valid: {is_valid_password(result)}")
print("="*50)
