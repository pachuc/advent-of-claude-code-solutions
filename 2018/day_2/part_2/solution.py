def parse_input(filename: str) -> list[str]:
    """Read input file and return list of box IDs."""
    with open(filename, 'r') as f:
        content = f.read()

    # Split by newlines and filter out empty lines
    box_ids = [line.strip() for line in content.split('\n') if line.strip()]
    return box_ids

def count_differences(str1: str, str2: str) -> int:
    """Count the number of differing characters between two strings."""
    return sum(1 for a, b in zip(str1, str2) if a != b)

def get_common_letters(str1: str, str2: str) -> str:
    """Extract common letters from two strings (where characters match)."""
    return ''.join(a for a, b in zip(str1, str2) if a == b)

def find_prototype_boxes(box_ids: list[str]) -> str:
    """Find two box IDs that differ by exactly one character and return their common letters."""
    for i in range(len(box_ids)):
        for j in range(i + 1, len(box_ids)):
            if count_differences(box_ids[i], box_ids[j]) == 1:
                return get_common_letters(box_ids[i], box_ids[j])

    raise ValueError("No matching box IDs found")

def main():
    box_ids = parse_input('input.md')
    result = find_prototype_boxes(box_ids)
    print(result)

if __name__ == '__main__':
    main()
