#!/usr/bin/env python3
"""Verify the solution result is correct."""

def verify_result(instructions, position):
    """
    Verify that the given position is correct.

    Args:
        instructions: The input string
        position: The claimed position (1-indexed) where floor -1 is first reached
    """
    # Calculate floor at the given position
    floor = 0
    for i, char in enumerate(instructions[:position], 1):
        if char == '(':
            floor += 1
        else:
            floor -= 1

    print(f"At position {position}: floor = {floor}")

    # Check floor is -1 at this position
    if floor != -1:
        print(f"❌ ERROR: At position {position}, floor should be -1, got {floor}")
        return False

    # Check floor is NOT -1 at position-1 (if position > 1)
    if position > 1:
        floor = 0
        for char in instructions[:position-1]:
            floor += 1 if char == '(' else -1

        print(f"At position {position-1}: floor = {floor}")

        if floor == -1:
            print(f"❌ ERROR: Floor -1 reached before position {position}")
            return False

    print(f"✓ Result {position} verified correct")
    return True


if __name__ == "__main__":
    # Read input
    with open('input.md', 'r') as f:
        instructions = f.read().strip()

    position = 1783

    # Verify
    if verify_result(instructions, position):
        print(f"\n✅ Position {position} is CORRECT!")
    else:
        print(f"\n❌ Position {position} is INCORRECT!")
