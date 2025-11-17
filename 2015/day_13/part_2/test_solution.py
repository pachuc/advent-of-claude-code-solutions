import solution


def test_parse_input():
    """Test 1: Verify input parsing"""
    print("=== Test 1: Parse Input Correctness ===")

    with open("input.md", 'r') as f:
        input_text = f.read()

    happiness_map, people = solution.parse_input(input_text)

    # Check we have 8 people
    assert len(people) == 8, f"Expected 8 people, got {len(people)}"
    print(f"✓ Found {len(people)} people: {sorted(people)}")

    # Check all people have 7 relationships
    for person in people:
        assert len(happiness_map[person]) == 7, f"{person} should have 7 relationships"
    print("✓ Each person has 7 relationships")

    # Verify total relationships
    total_relationships = sum(len(happiness_map[p]) for p in happiness_map)
    assert total_relationships == 56, f"Expected 56 relationships, got {total_relationships}"
    print(f"✓ Total of {total_relationships} directed relationships")

    # Check sample relationships
    assert happiness_map["Alice"]["Bob"] == -2, "Alice-Bob should be -2"
    assert happiness_map["Bob"]["Alice"] == 93, "Bob-Alice should be 93"
    assert happiness_map["George"]["Mallory"] == 7, "George-Mallory should be 7"
    assert happiness_map["Mallory"]["George"] == -99, "Mallory-George should be -99"
    print("✓ Sample relationships verified")

    print()
    return happiness_map, people


def test_add_self(happiness_map, people):
    """Test 2: Verify self addition"""
    print("=== Test 2: Self Addition Correctness ===")

    original_people = people.copy()
    solution.add_self(happiness_map, people)

    # Check we now have 9 people
    assert len(people) == 9, f"Expected 9 people after adding self, got {len(people)}"
    print(f"✓ Now have {len(people)} people including 'Me'")

    # Check "Me" is in the set
    assert "Me" in people, "'Me' should be in people set"
    print("✓ 'Me' is in people set")

    # Check "Me" has 8 relationships
    assert len(happiness_map["Me"]) == 8, "'Me' should have 8 relationships"
    print("✓ 'Me' has 8 relationships")

    # Verify all relationships with "Me" are 0
    for person in original_people:
        assert happiness_map["Me"][person] == 0, f"Me's happiness with {person} should be 0"
        assert happiness_map[person]["Me"] == 0, f"{person}'s happiness with Me should be 0"
    print("✓ All relationships with 'Me' are 0 (neutral)")

    print()


def test_happiness_calculation():
    """Test 3: Verify happiness calculation"""
    print("=== Test 3: Happiness Calculation - Simple Cases ===")

    # Test case 3a: Three person circle
    arrangement = ["Alice", "Bob", "Carol"]
    happiness_map = {
        "Alice": {"Bob": 10, "Carol": 5},
        "Bob": {"Alice": 20, "Carol": 15},
        "Carol": {"Alice": 30, "Bob": 25}
    }

    # Expected: Alice(5+10) + Bob(20+15) + Carol(25+30) = 15 + 35 + 55 = 105
    result = solution.calculate_happiness(arrangement, happiness_map)
    expected = 105
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Simple 3-person test: {result} (expected {expected})")

    # Test case 3b: Verify circular property (4 people)
    arrangement = ["A", "B", "C", "D"]
    happiness_map = {
        "A": {"B": 1, "C": 0, "D": 10},  # A's neighbors: D (left) and B (right)
        "B": {"A": 2, "C": 3, "D": 0},   # B's neighbors: A (left) and C (right)
        "C": {"A": 0, "B": 4, "D": 5},   # C's neighbors: B (left) and D (right)
        "D": {"A": 6, "B": 0, "C": 7}    # D's neighbors: C (left) and A (right)
    }
    # Expected: A(10+1) + B(2+3) + C(4+5) + D(7+6) = 11 + 5 + 9 + 13 = 38
    result = solution.calculate_happiness(arrangement, happiness_map)
    expected = 38
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Circular property test (4 people): {result} (expected {expected})")

    print()


def test_permutation_count():
    """Test 5: Verify permutation count"""
    print("=== Test 5: Permutation Coverage ===")

    from itertools import permutations

    # For 9 people with first fixed, we should have 8! = 40,320 permutations
    people = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    fixed = people[0]
    others = people[1:]

    perms = list(permutations(others))
    expected = 40320  # 8!
    assert len(perms) == expected, f"Expected {expected} permutations, got {len(perms)}"
    print(f"✓ Generated {len(perms)} permutations (8! = 40,320)")

    print()


def test_manual_verification():
    """Test 9: Manual verification of optimal arrangement"""
    print("=== Test 9: Manual Verification of Optimal Arrangement ===")

    with open("input.md", 'r') as f:
        input_text = f.read()

    happiness_map, people = solution.parse_input(input_text)
    solution.add_self(happiness_map, people)

    max_happiness, optimal_arrangement = solution.find_optimal_seating(people, happiness_map)

    print(f"Optimal arrangement: {' -> '.join(optimal_arrangement)}")
    print(f"Maximum happiness: {max_happiness}")
    print()

    # Manually calculate happiness for optimal arrangement
    print("Manual calculation:")
    total = 0
    n = len(optimal_arrangement)

    for i in range(n):
        person = optimal_arrangement[i]
        left = optimal_arrangement[(i - 1) % n]
        right = optimal_arrangement[(i + 1) % n]

        left_happiness = happiness_map[person][left]
        right_happiness = happiness_map[person][right]
        person_total = left_happiness + right_happiness

        print(f"  {person:8} (left: {left:8}, right: {right:8}) = {left_happiness:4} + {right_happiness:4} = {person_total:4}")
        total += person_total

    print(f"Manual total: {total}")
    assert total == max_happiness, f"Manual calculation {total} doesn't match result {max_happiness}"
    print("✓ Manual calculation matches algorithm result")

    print()


def test_regression():
    """Test 10: Regression test"""
    print("=== Test 10: Regression Test ===")

    results = []
    for run in range(3):
        result = solution.solve("input.md")
        results.append(result)

    # All results should be the same
    assert all(r == results[0] for r in results), f"Results are not consistent: {results}"
    print(f"✓ Three runs all produced the same result: {results[0]}")

    print()


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING TEST SUITE")
    print("=" * 60)
    print()

    # Test 1: Parse input
    happiness_map, people = test_parse_input()

    # Test 2: Add self
    test_add_self(happiness_map, people)

    # Test 3: Happiness calculation
    test_happiness_calculation()

    # Test 5: Permutation count
    test_permutation_count()

    # Test 9: Manual verification
    test_manual_verification()

    # Test 10: Regression test
    test_regression()

    print("=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
