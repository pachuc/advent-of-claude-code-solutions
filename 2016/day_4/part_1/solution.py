import re
from collections import Counter

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

def solve(filename='input.md'):
    """Main processing function."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total_sector_id_sum = 0

    for line in lines:
        parsed = parse_room_entry(line)
        if parsed:
            encrypted_name, sector_id, checksum = parsed
            if is_real_room(encrypted_name, checksum):
                total_sector_id_sum += sector_id

    return total_sector_id_sum

def validate_solution():
    """Run validation tests on provided examples."""
    test_cases = [
        ("aaaaa-bbb-z-y-x-123[abxyz]", True, 123),
        ("a-b-c-d-e-f-g-h-987[abcde]", True, 987),
        ("not-a-real-room-404[oarel]", True, 404),
        ("totally-real-room-200[decoy]", False, 200)
    ]

    total = 0
    for line, should_be_real, sector_id in test_cases:
        encrypted_name, sid, checksum = parse_room_entry(line)
        is_real = is_real_room(encrypted_name, checksum)
        assert is_real == should_be_real, f"Failed on {line}"
        if is_real:
            total += sector_id

    assert total == 1514, f"Expected 1514, got {total}"
    print("All validation tests passed!")

if __name__ == "__main__":
    validate_solution()
    result = solve()
    print(result)
