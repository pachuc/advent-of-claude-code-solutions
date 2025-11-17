"""Test that input parsing works correctly."""
from solution import parse_input

# Read and parse the input
with open('input.md', 'r') as f:
    input_text = f.read()

floors = parse_input(input_text)

print("Parsed input:")
for floor_num in range(4):
    items = floors[floor_num]
    print(f"Floor {floor_num}: {sorted(items)}")

# Count total items
total_items = sum(len(floors[i]) for i in range(4))
print(f"\nTotal items: {total_items}")

# Count generators and microchips
generators = sum(1 for i in range(4) for elem, item_type in floors[i] if item_type == 'G')
microchips = sum(1 for i in range(4) for elem, item_type in floors[i] if item_type == 'M')

print(f"Generators: {generators}")
print(f"Microchips: {microchips}")

# Verify expected content
expected_floor_0 = {('strontium', 'G'), ('strontium', 'M'), ('plutonium', 'G'), ('plutonium', 'M')}
expected_floor_1 = {('thulium', 'G'), ('ruthenium', 'G'), ('ruthenium', 'M'), ('curium', 'G'), ('curium', 'M')}
expected_floor_2 = {('thulium', 'M')}
expected_floor_3 = set()

print("\nVerification:")
print(f"Floor 0 correct: {floors[0] == expected_floor_0}")
print(f"Floor 1 correct: {floors[1] == expected_floor_1}")
print(f"Floor 2 correct: {floors[2] == expected_floor_2}")
print(f"Floor 3 correct: {floors[3] == expected_floor_3}")
