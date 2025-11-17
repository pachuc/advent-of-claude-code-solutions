#!/usr/bin/env python3
"""Quick verification test for the solution"""

from solution import parse_input, calculate_happiness, find_optimal_seating

# Read input
with open('input.md', 'r') as f:
    input_text = f.read()

# Parse input
happiness_map, people = parse_input(input_text)

# Test 1: Verify parsing - check number of people and relationships
print(f"Number of people: {len(people)}")
print(f"Expected: 8")
print(f"People: {sorted(people)}")
print()

# Test 2: Verify specific relationships from input
print("Spot-checking specific relationships:")
print(f"Alice -> Bob: {happiness_map['Alice']['Bob']} (expected: -2)")
print(f"Alice -> David: {happiness_map['Alice']['David']} (expected: 65)")
print(f"Bob -> Alice: {happiness_map['Bob']['Alice']} (expected: 93)")
print(f"George -> Mallory: {happiness_map['George']['Mallory']} (expected: 7)")
print()

# Test 3: Test simple calculation - ['Alice', 'David', 'Carol', 'Bob']
test_arrangement = ['Alice', 'David', 'Carol', 'Bob']
result = calculate_happiness(test_arrangement, happiness_map)
print(f"Test arrangement {test_arrangement}:")
print(f"Calculated happiness: {result}")
print(f"Expected: 58")
print()

# Test 4: Test circular property - ['Alice', 'Bob', 'Carol']
test_arrangement2 = ['Alice', 'Bob', 'Carol']
result2 = calculate_happiness(test_arrangement2, happiness_map)
print(f"Test arrangement {test_arrangement2}:")
print(f"Calculated happiness: {result2}")
print(f"Expected: -76")
print()

# Test 5: Run the full algorithm
max_happiness = find_optimal_seating(happiness_map, people)
print(f"Maximum happiness from optimal seating: {max_happiness}")
print(f"Expected: 664")
print()

# Verify all tests pass
all_tests_pass = (
    len(people) == 8 and
    happiness_map['Alice']['Bob'] == -2 and
    happiness_map['Alice']['David'] == 65 and
    happiness_map['Bob']['Alice'] == 93 and
    happiness_map['George']['Mallory'] == 7 and
    result == 58 and
    result2 == -76 and
    max_happiness == 664
)

if all_tests_pass:
    print("✓ All verification tests PASSED")
else:
    print("✗ Some tests FAILED")
