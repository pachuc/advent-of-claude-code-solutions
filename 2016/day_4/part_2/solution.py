import re
from collections import Counter

# ===== Part 1 Functions (Reused) =====

def parse_room_entry(line: str) -> tuple[str, int, str]:
    """Parse room entry and extract components."""
    pattern = r'^([a-z-]+)-(\d+)\[([a-z]{5})\]$'
    match = re.match(pattern, line)
    if match:
        encrypted_name = match.group(1)
        sector_id = int(match.group(2))
        checksum = match.group(3)
        return encrypted_name, sector_id, checksum
    return None

def generate_expected_checksum(encrypted_name: str) -> str:
    """Generate expected checksum from encrypted name."""
    # Remove dashes and count letter frequencies
    letters_only = encrypted_name.replace('-', '')
    frequency_dict = Counter(letters_only)

    # Sort by frequency (descending) then alphabetically (ascending)
    sorted_letters = sorted(
        frequency_dict.items(),
        key=lambda x: (-x[1], x[0])
    )

    # Take first 5 letters (or all if fewer than 5 unique letters)
    return ''.join([letter for letter, count in sorted_letters[:5]])

def is_real_room(encrypted_name: str, checksum: str) -> bool:
    """Validate room by comparing checksums."""
    expected = generate_expected_checksum(encrypted_name)
    return expected == checksum

# ===== Part 2 Functions (New) =====

def decrypt_room_name(encrypted_name: str, sector_id: int) -> str:
    """Decrypt room name using Caesar cipher with given sector ID shift."""
    shift = sector_id % 26  # Optimize: modulo 26 since alphabet repeats
    decrypted = []

    for char in encrypted_name:
        if char == '-':
            decrypted.append(' ')
        else:
            # Shift letter by sector_id positions
            char_index = ord(char) - ord('a')  # Convert to 0-25
            new_index = (char_index + shift) % 26  # Apply shift with wraparound
            decrypted.append(chr(new_index + ord('a')))  # Convert back to char

    return ''.join(decrypted)

def find_north_pole_storage(filename='input.md') -> int:
    """Find sector ID of room storing North Pole objects."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        parsed = parse_room_entry(line)
        if parsed:
            encrypted_name, sector_id, checksum = parsed

            # Only process real rooms
            if is_real_room(encrypted_name, checksum):
                decrypted_name = decrypt_room_name(encrypted_name, sector_id)

                # Search for North Pole objects (precise matching)
                if 'north pole' in decrypted_name or 'northpole' in decrypted_name:
                    return sector_id

    # If no match found, raise an error for clarity
    raise ValueError("No room containing 'North Pole' found in input")

def solve(filename='input.md'):
    """Main solving function."""
    return find_north_pole_storage(filename)

def validate_solution():
    """Run comprehensive validation tests."""
    print("Running validation tests...")

    # Test 1.1: Example verification
    result = decrypt_room_name("qzmt-zixmtkozy-ivhz", 343)
    assert result == "very encrypted name", f"Test 1.1 failed: {result}"
    print("✓ Test 1.1: Example verification passed")

    # Test 1.2: Zero shift
    assert decrypt_room_name("abc-xyz", 0) == "abc xyz"
    assert decrypt_room_name("abc-xyz", 26) == "abc xyz"
    print("✓ Test 1.2: Zero shift passed")

    # Test 1.2b: Modulo 26 boundary cases
    assert decrypt_room_name("abc", 25) == "zab"
    assert decrypt_room_name("abc", 27) == "bcd"
    print("✓ Test 1.2b: Modulo 26 boundaries passed")

    # Test 1.3: Full rotation with wraparound
    assert decrypt_room_name("zabc", 1) == "abcd"
    assert decrypt_room_name("xyz", 3) == "abc"
    print("✓ Test 1.3: Alphabet wraparound passed")

    # Test 1.4: Large sector IDs
    assert decrypt_room_name("abc", 1000) == "mno"
    print("✓ Test 1.4: Large sector IDs passed")

    # Test 2.1: Part 1 logic integration
    encrypted, sid, checksum = parse_room_entry("aaaaa-bbb-z-y-x-123[abxyz]")
    assert sid == 123
    assert is_real_room(encrypted, checksum) == True
    print("✓ Test 2.1: Part 1 integration passed")

    print("All validation tests passed!")

if __name__ == "__main__":
    validate_solution()
    result = solve()
    print(result)
