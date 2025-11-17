import re
from solution import parse_input, add_self, calculate_happiness, find_optimal_seating

# Read input
with open("input.md", 'r') as f:
    input_text = f.read()

print("=" * 60)
print("TEST 1: PARSING CORRECTNESS")
print("=" * 60)

happiness_map, people = parse_input(input_text)

print(f"Number of people parsed: {len(people)}")
print(f"People: {sorted(people)}")
print()

# Count total relationships
total_relationships = sum(len(happiness_map[p]) for p in happiness_map)
print(f"Total relationships: {total_relationships}")
print(f"Expected: 56 (8 people × 7 relationships each)")
print()

# Check sample relationships
test_cases = [
    ("Alice", "Bob", -2),
    ("Bob", "Alice", 93),
    ("George", "Mallory", 7),
    ("Mallory", "George", -99)
]

print("Sample relationship checks:")
for person, neighbor, expected in test_cases:
    actual = happiness_map[person][neighbor]
    status = "✓" if actual == expected else "✗"
    print(f"  {status} happiness[{person}][{neighbor}] = {actual} (expected {expected})")

print()
assert len(people) == 8, f"Expected 8 people, got {len(people)}"
assert total_relationships == 56, f"Expected 56 relationships, got {total_relationships}"
for person, neighbor, expected in test_cases:
    assert happiness_map[person][neighbor] == expected
print("✓ Parsing test PASSED")
print()

print("=" * 60)
print("TEST 2: SELF-ADDITION CORRECTNESS")
print("=" * 60)

# Make a copy to preserve original
happiness_map_copy = {p: dict(h) for p, h in happiness_map.items()}
people_copy = set(people)

add_self(happiness_map_copy, people_copy)

print(f"Number of people after adding self: {len(people_copy)}")
print(f"Expected: 9")
print()

print(f"'Me' in people set: {'Me' in people_copy}")
print()

# Check all relationships with "Me"
print("Checking 0-happiness relationships with 'Me':")
all_zero = True
for person in people:
    me_to_person = happiness_map_copy["Me"][person]
    person_to_me = happiness_map_copy[person]["Me"]
    if me_to_person != 0 or person_to_me != 0:
        all_zero = False
        print(f"  ✗ Me↔{person}: Me→{person}={me_to_person}, {person}→Me={person_to_me}")
    else:
        print(f"  ✓ Me↔{person}: both directions = 0")

print()
assert len(people_copy) == 9, f"Expected 9 people, got {len(people_copy)}"
assert "Me" in people_copy
assert all_zero, "All relationships with 'Me' should be 0"
print("✓ Self-addition test PASSED")
print()

print("=" * 60)
print("TEST 3: HAPPINESS CALCULATION")
print("=" * 60)

# Test with simple case
test_happiness = {
    "Alice": {"Bob": 10, "Carol": 5},
    "Bob": {"Alice": 20, "Carol": 15},
    "Carol": {"Alice": 30, "Bob": 25}
}

arrangement = ["Alice", "Bob", "Carol"]
result = calculate_happiness(arrangement, test_happiness)

print("Test arrangement (circular): Alice - Bob - Carol")
print("Expected calculation:")
print("  Alice: Carol (left) + Bob (right) = 5 + 10 = 15")
print("  Bob: Alice (left) + Carol (right) = 20 + 15 = 35")
print("  Carol: Bob (left) + Alice (right) = 25 + 30 = 55")
print("  Total = 105")
print()
print(f"Actual result: {result}")
print()

assert result == 105, f"Expected 105, got {result}"
print("✓ Happiness calculation test PASSED")
print()

print("=" * 60)
print("TEST 4: MANUAL VERIFICATION OF OPTIMAL ARRANGEMENT")
print("=" * 60)

# Parse input again and add self
happiness_map, people = parse_input(input_text)
add_self(happiness_map, people)

# Find optimal
max_happiness, optimal_arrangement = find_optimal_seating(people, happiness_map)

print(f"Maximum happiness: {max_happiness}")
print(f"Optimal arrangement: {' → '.join(optimal_arrangement)}")
print()

# Manual calculation
print("Manual verification:")
print("-" * 60)
total = 0
n = len(optimal_arrangement)
for i in range(n):
    person = optimal_arrangement[i]
    left_neighbor = optimal_arrangement[(i - 1) % n]
    right_neighbor = optimal_arrangement[(i + 1) % n]

    left_val = happiness_map[person][left_neighbor]
    right_val = happiness_map[person][right_neighbor]
    contribution = left_val + right_val
    total += contribution

    print(f"{person:8s}: {left_neighbor:8s} (left) + {right_neighbor:8s} (right) = {left_val:4d} + {right_val:4d} = {contribution:4d}")

print("-" * 60)
print(f"Total: {total}")
print()

assert total == max_happiness, f"Manual calculation {total} doesn't match algorithm result {max_happiness}"
print("✓ Manual verification PASSED")
print()

print("=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print(f"\nFINAL ANSWER: {max_happiness}")
