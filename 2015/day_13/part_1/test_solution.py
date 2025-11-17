import os
import re
from itertools import permutations
from solution import parse_input, calculate_happiness, find_optimal_seating


def test_input_file():
    """Test 0: Input File Content Validation"""
    print("\n=== Test 0: Input File Content Validation ===")

    filename = 'input.md'
    assert os.path.exists(filename), f"Input file {filename} not found"

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Check line count
    assert len(lines) == 56, f"Expected 56 lines, got {len(lines)}"

    # Verify format of first line
    pattern = r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.'
    assert re.match(pattern, lines[0].strip()), f"First line doesn't match expected format"

    # Check for expected people
    content = ''.join(lines)
    expected_people = ['Alice', 'Bob', 'Carol', 'David', 'Eric', 'Frank', 'George', 'Mallory']
    for person in expected_people:
        assert person in content, f"Expected person {person} not found in input"

    print("✓ Input file validation passed")


def test_parsing():
    """Test 1: Input Parsing Validation"""
    print("\n=== Test 1: Input Parsing Validation ===")

    with open('input.md', 'r') as f:
        input_text = f.read()

    happiness_map, people = parse_input(input_text)

    assert len(people) == 8, f"Expected 8 people, got {len(people)}"

    total_relationships = sum(len(neighbors) for neighbors in happiness_map.values())
    assert total_relationships == 56, f"Expected 56 relationships, got {total_relationships}"

    # Spot checks
    assert happiness_map['Alice']['Bob'] == -2, f"Alice->Bob should be -2, got {happiness_map['Alice']['Bob']}"
    assert happiness_map['Alice']['David'] == 65, f"Alice->David should be 65, got {happiness_map['Alice']['David']}"
    assert happiness_map['Bob']['Alice'] == 93, f"Bob->Alice should be 93, got {happiness_map['Bob']['Alice']}"
    assert happiness_map['George']['Mallory'] == 7, f"George->Mallory should be 7, got {happiness_map['George']['Mallory']}"

    print("✓ Parsing test passed")
    return happiness_map, people


def test_happiness_calculation(happiness_map):
    """Test 2: Happiness Calculation - Simple Example"""
    print("\n=== Test 2: Happiness Calculation - Simple Example ===")

    arrangement = ['Alice', 'David', 'Carol', 'Bob']
    result = calculate_happiness(arrangement, happiness_map)

    # Manual calculation based on the implementation plan:
    # Alice (index 0): left=Bob(3), right=David(1) -> -2 + 65 = 63
    # David (index 1): left=Alice(0), right=Carol(2) -> 43 + (-53) = -10
    # Carol (index 2): left=David(1), right=Bob(3) -> (-37) + (-70) = -107
    # Bob (index 3): left=Carol(2), right=Alice(0) -> 19 + 93 = 112
    # Total: 63 + (-10) + (-107) + 112 = 58
    expected = 58
    assert result == expected, f"Expected {expected}, got {result}"

    print(f"✓ Happiness calculation test passed (result: {result})")


def test_circular_property(happiness_map):
    """Test 3: Circular Property Validation"""
    print("\n=== Test 3: Circular Property Validation ===")

    arrangement = ['Alice', 'Bob', 'Carol']
    result = calculate_happiness(arrangement, happiness_map)

    # Manual calculation:
    # Alice: left=Carol, right=Bob -> -62 + (-2) = -64
    # Bob: left=Alice, right=Carol -> 93 + 19 = 112
    # Carol: left=Bob, right=Alice -> -70 + (-54) = -124
    # Total: -64 + 112 + (-124) = -76
    expected = -76
    assert result == expected, f"Expected {expected}, got {result}"

    print(f"✓ Circular property test passed (result: {result})")


def test_permutation_count(people):
    """Test 4: Permutation Generation Count and Uniqueness"""
    print("\n=== Test 4: Permutation Generation Count and Uniqueness ===")

    people_sorted = sorted(people)
    fixed_person = people_sorted[0]
    remaining_people = people_sorted[1:]

    seen_arrangements = set()
    count = 0

    for perm in permutations(remaining_people):
        arrangement = tuple([fixed_person] + list(perm))

        # Verify first person is fixed
        assert arrangement[0] == fixed_person, f"First person should be {fixed_person}, got {arrangement[0]}"

        # Verify uniqueness
        assert arrangement not in seen_arrangements, f"Duplicate permutation found: {arrangement}"

        seen_arrangements.add(arrangement)
        count += 1

    expected = 5040  # 7!
    assert count == expected, f"Expected {expected} permutations, got {count}"

    print(f"✓ Permutation count test passed - {count} unique arrangements verified")


def test_rotational_symmetry(happiness_map):
    """Test 5: Symmetry Validation"""
    print("\n=== Test 5: Rotational Symmetry Validation ===")

    arr1 = ['Alice', 'Bob', 'Carol', 'David']
    arr2 = ['Bob', 'Carol', 'David', 'Alice']  # Rotated by 1
    arr3 = ['Carol', 'David', 'Alice', 'Bob']  # Rotated by 2

    h1 = calculate_happiness(arr1, happiness_map)
    h2 = calculate_happiness(arr2, happiness_map)
    h3 = calculate_happiness(arr3, happiness_map)

    assert h1 == h2 == h3, f"Rotational symmetry broken: {h1}, {h2}, {h3}"

    print(f"✓ Rotational symmetry test passed (all rotations = {h1})")


def test_full_algorithm(happiness_map, people):
    """Test 6: Main Algorithm - Full Input Test"""
    print("\n=== Test 6: Main Algorithm - Full Input Test ===")

    result = find_optimal_seating(happiness_map, people)

    assert isinstance(result, (int, float)), f"Result should be numeric, got {type(result)}"
    assert result > 0, f"Optimal arrangement should have positive happiness, got {result}"
    assert result < 1520, f"Result suspiciously high: {result}"

    print(f"✓ Full algorithm test passed - Maximum happiness: {result}")

    if 400 <= result <= 800:
        print("  (Result is within expected range 400-800)")
    else:
        print(f"  (Result is outside typical range 400-800, but may be correct for this input)")

    return result


def test_all_negative():
    """Test 7: Edge Case - All Negative Values"""
    print("\n=== Test 7: Edge Case - All Negative Values ===")

    test_happiness = {
        'A': {'B': -10, 'C': -20},
        'B': {'A': -5, 'C': -15},
        'C': {'A': -25, 'B': -30}
    }
    test_people = ['A', 'B', 'C']

    result = find_optimal_seating(test_happiness, test_people)
    assert result == -105, f"Expected -105, got {result}"

    print(f"✓ All negative test passed (result: {result})")


def test_optimal_pairing():
    """Test 8: Edge Case - Single Optimal Solution"""
    print("\n=== Test 8: Edge Case - Single Optimal Solution ===")

    test_happiness = {
        'A': {'B': 100, 'C': 0, 'D': 0},
        'B': {'A': 100, 'C': 0, 'D': 0},
        'C': {'A': 0, 'B': 0, 'D': 100},
        'D': {'A': 0, 'B': 0, 'C': 100}
    }
    test_people = ['A', 'B', 'C', 'D']

    result = find_optimal_seating(test_happiness, test_people)
    assert result == 400, f"Expected 400, got {result}"

    print(f"✓ Optimal pairing test passed (result: {result})")


def run_all_tests():
    """Run all tests in order"""
    print("=" * 60)
    print("Running All Tests")
    print("=" * 60)

    # Phase 0: Input Validation
    test_input_file()

    # Parse input for all subsequent tests
    with open('input.md', 'r') as f:
        input_text = f.read()
    happiness_map, people = parse_input(input_text)

    # Phase 1: Unit Tests
    test_parsing()
    test_permutation_count(people)
    test_happiness_calculation(happiness_map)
    test_circular_property(happiness_map)

    # Phase 2: Integration Tests
    test_rotational_symmetry(happiness_map)
    final_result = test_full_algorithm(happiness_map, people)

    # Phase 3: Edge Cases
    test_all_negative()
    test_optimal_pairing()

    print("\n" + "=" * 60)
    print("All Tests Passed!")
    print("=" * 60)
    print(f"\nFinal Answer: {final_result}")


if __name__ == '__main__':
    run_all_tests()
