"""Detailed testing to verify the solution works correctly."""
from solution import parse_room_entry, generate_expected_checksum, is_real_room

# Test parsing
print("Testing parsing...")
test = "aaaaa-bbb-z-y-x-123[abxyz]"
name, sid, checksum = parse_room_entry(test)
print(f"  Input: {test}")
print(f"  Parsed: name='{name}', sector_id={sid}, checksum='{checksum}'")
assert name == "aaaaa-bbb-z-y-x"
assert sid == 123
assert checksum == "abxyz"
print("  Parsing test passed!\n")

# Test checksum generation with detailed breakdown
print("Testing checksum generation...")

test_cases = [
    ("aaaaa-bbb-z-y-x", "abxyz"),
    ("a-b-c-d-e-f-g-h", "abcde"),
    ("not-a-real-room", "oarel"),
    ("totally-real-room", "loart"),  # l=3, o=3 (tie, alphabetical: l<o), then a,r,t all at 2
]

for encrypted_name, expected in test_cases:
    result = generate_expected_checksum(encrypted_name)
    print(f"  Name: '{encrypted_name}'")

    # Show letter frequencies
    from collections import Counter
    letters_only = encrypted_name.replace('-', '')
    freq = Counter(letters_only)
    sorted_freq = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    print(f"  Frequencies: {dict(sorted_freq)}")
    print(f"  Expected checksum: '{expected}'")
    print(f"  Generated checksum: '{result}'")
    assert result == expected, f"Mismatch! Expected '{expected}', got '{result}'"
    print(f"  ✓ Passed\n")

print("All checksum generation tests passed!\n")

# Test validation
print("Testing room validation...")
test_validation = [
    ("aaaaa-bbb-z-y-x", "abxyz", True),
    ("a-b-c-d-e-f-g-h", "abcde", True),
    ("not-a-real-room", "oarel", True),
    ("totally-real-room", "decoy", False),
]

for encrypted_name, checksum, expected_result in test_validation:
    result = is_real_room(encrypted_name, checksum)
    status = "REAL" if result else "DECOY"
    print(f"  Room: '{encrypted_name}' with checksum [{checksum}] -> {status}")
    assert result == expected_result
    print(f"  ✓ Passed")

print("\nAll tests passed successfully!")
