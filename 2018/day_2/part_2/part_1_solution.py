from collections import Counter

def parse_input(filename: str) -> list[str]:
    """Read input file and return list of box IDs."""
    with open(filename, 'r') as f:
        content = f.read()

    # Split by newlines and filter out empty lines
    box_ids = [line.strip() for line in content.split('\n') if line.strip()]
    return box_ids

def has_exact_count(box_id: str, target_count: int) -> bool:
    """Check if any letter in box_id appears exactly target_count times."""
    freq = Counter(box_id)
    return target_count in freq.values()

def calculate_checksum(box_ids: list[str]) -> int:
    """Calculate checksum by counting box IDs with exact letter frequencies."""
    twos_count = 0
    threes_count = 0

    for box_id in box_ids:
        if has_exact_count(box_id, 2):
            twos_count += 1
        if has_exact_count(box_id, 3):
            threes_count += 1

    return twos_count * threes_count

def main():
    box_ids = parse_input('input.md')
    checksum = calculate_checksum(box_ids)
    print(checksum)

if __name__ == '__main__':
    main()
