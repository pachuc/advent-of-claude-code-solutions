#!/usr/bin/env python3
"""Verification script to validate the solution output."""

def parse_input(filename: str) -> list[str]:
    """Read input file and return list of box IDs."""
    with open(filename, 'r') as f:
        content = f.read()
    box_ids = [line.strip() for line in content.split('\n') if line.strip()]
    return box_ids

def count_differences(str1: str, str2: str) -> int:
    """Count the number of differing characters between two strings."""
    return sum(1 for a, b in zip(str1, str2) if a != b)

def verify_result(result: str, box_ids: list[str]) -> bool:
    """
    Verify the result by trying to reconstruct the two original box IDs.
    The result should be a 25-character string that can produce exactly 2
    box IDs from the input when a single character is inserted at some position.
    """
    print(f"Result to verify: {result}")
    print(f"Result length: {len(result)}")
    print()

    # Try to find box IDs that match this result pattern
    matching_pairs = []

    for i, id1 in enumerate(box_ids):
        for j in range(i + 1, len(box_ids)):
            id2 = box_ids[j]

            # Check if they differ by exactly 1 character
            if count_differences(id1, id2) == 1:
                # Extract common letters
                common = ''.join(a for a, b in zip(id1, id2) if a == b)

                # Check if this matches our result
                if common == result:
                    matching_pairs.append((id1, id2))
                    print(f"Found matching pair:")
                    print(f"  Box ID 1: {id1}")
                    print(f"  Box ID 2: {id2}")

                    # Find the differing position
                    for k, (a, b) in enumerate(zip(id1, id2)):
                        if a != b:
                            print(f"  Differ at position {k}: '{a}' vs '{b}'")
                    print()

    if len(matching_pairs) == 0:
        print("❌ ERROR: No matching pairs found!")
        return False
    elif len(matching_pairs) == 1:
        print(f"✓ SUCCESS: Found exactly 1 matching pair")
        return True
    else:
        print(f"⚠ WARNING: Found {len(matching_pairs)} matching pairs (expected 1)")
        return True  # Still valid, just unexpected

def main():
    # Read the box IDs
    box_ids = parse_input('input.md')
    print(f"Total box IDs: {len(box_ids)}")
    print(f"Box ID length: {len(box_ids[0]) if box_ids else 0}")
    print()

    # The result from the solution
    result = "xpysnnkqrbuhefmcajodplyzw"

    # Verify it
    is_valid = verify_result(result, box_ids)

    if is_valid:
        print("\n✓ Verification PASSED")
    else:
        print("\n❌ Verification FAILED")

    return is_valid

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
