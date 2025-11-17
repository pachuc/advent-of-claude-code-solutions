#!/usr/bin/env python3
"""Test script to verify input parsing."""

from solution import parse_input

def test_parsing():
    """Test parsing of actual input."""

    print("Testing input parsing...")

    # Read the actual input
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse it
    floors = parse_input(input_text)

    # Expected configuration based on input.md
    expected_floor_0 = {
        ('strontium', 'G'),
        ('strontium', 'M'),
        ('plutonium', 'G'),
        ('plutonium', 'M')
    }

    expected_floor_1 = {
        ('thulium', 'G'),
        ('ruthenium', 'G'),
        ('ruthenium', 'M'),
        ('curium', 'G'),
        ('curium', 'M')
    }

    expected_floor_2 = {
        ('thulium', 'M')
    }

    expected_floor_3 = set()

    # Check each floor
    tests_passed = 0
    tests_total = 4

    print("\nFloor 0 (First floor):")
    print(f"  Parsed: {sorted(floors[0])}")
    print(f"  Expected: {sorted(expected_floor_0)}")
    if floors[0] == expected_floor_0:
        print("  ✓ PASSED")
        tests_passed += 1
    else:
        print("  ✗ FAILED")

    print("\nFloor 1 (Second floor):")
    print(f"  Parsed: {sorted(floors[1])}")
    print(f"  Expected: {sorted(expected_floor_1)}")
    if floors[1] == expected_floor_1:
        print("  ✓ PASSED")
        tests_passed += 1
    else:
        print("  ✗ FAILED")

    print("\nFloor 2 (Third floor):")
    print(f"  Parsed: {sorted(floors[2])}")
    print(f"  Expected: {sorted(expected_floor_2)}")
    if floors[2] == expected_floor_2:
        print("  ✓ PASSED")
        tests_passed += 1
    else:
        print("  ✗ FAILED")

    print("\nFloor 3 (Fourth floor):")
    print(f"  Parsed: {sorted(floors[3])}")
    print(f"  Expected: {sorted(expected_floor_3)}")
    if floors[3] == expected_floor_3:
        print("  ✓ PASSED")
        tests_passed += 1
    else:
        print("  ✗ FAILED")

    # Count total items
    total_items = sum(len(floor) for floor in floors.values())
    generators = sum(1 for floor in floors.values() for elem, type in floor if type == 'G')
    microchips = sum(1 for floor in floors.values() for elem, type in floor if type == 'M')

    print(f"\n{'='*60}")
    print(f"Total items: {total_items} (Expected: 10)")
    print(f"Generators: {generators} (Expected: 5)")
    print(f"Microchips: {microchips} (Expected: 5)")
    print(f"Parsing Tests: {tests_passed}/{tests_total} passed")
    print(f"{'='*60}")

    return tests_passed == tests_total and total_items == 10 and generators == 5 and microchips == 5

if __name__ == '__main__':
    success = test_parsing()
    exit(0 if success else 1)
