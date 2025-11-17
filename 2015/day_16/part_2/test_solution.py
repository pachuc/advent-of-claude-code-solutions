from solution import matches_target

# Target MFCSAM values
target = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}

# Define which compounds use which comparison rules
greater_than_compounds = {'cats', 'trees'}
less_than_compounds = {'pomeranians', 'goldfish'}


def test_greater_than_cats():
    """Test cats > 7 rule"""
    print("Testing cats > 7 rule...")

    # Should NOT match - boundary cases
    assert not matches_target({'cats': 6}, target, greater_than_compounds, less_than_compounds), "cats: 6 should NOT match"
    assert not matches_target({'cats': 7}, target, greater_than_compounds, less_than_compounds), "cats: 7 should NOT match (boundary)"

    # Should match
    assert matches_target({'cats': 8}, target, greater_than_compounds, less_than_compounds), "cats: 8 should match"
    assert matches_target({'cats': 9}, target, greater_than_compounds, less_than_compounds), "cats: 9 should match"
    assert matches_target({'cats': 100}, target, greater_than_compounds, less_than_compounds), "cats: 100 should match"

    print("✓ cats > 7 rule tests passed")


def test_greater_than_trees():
    """Test trees > 3 rule"""
    print("Testing trees > 3 rule...")

    # Should NOT match - boundary cases
    assert not matches_target({'trees': 2}, target, greater_than_compounds, less_than_compounds), "trees: 2 should NOT match"
    assert not matches_target({'trees': 3}, target, greater_than_compounds, less_than_compounds), "trees: 3 should NOT match (boundary)"

    # Should match
    assert matches_target({'trees': 4}, target, greater_than_compounds, less_than_compounds), "trees: 4 should match"
    assert matches_target({'trees': 5}, target, greater_than_compounds, less_than_compounds), "trees: 5 should match"
    assert matches_target({'trees': 10}, target, greater_than_compounds, less_than_compounds), "trees: 10 should match"

    print("✓ trees > 3 rule tests passed")


def test_less_than_pomeranians():
    """Test pomeranians < 3 rule"""
    print("Testing pomeranians < 3 rule...")

    # Should match
    assert matches_target({'pomeranians': 0}, target, greater_than_compounds, less_than_compounds), "pomeranians: 0 should match"
    assert matches_target({'pomeranians': 1}, target, greater_than_compounds, less_than_compounds), "pomeranians: 1 should match"
    assert matches_target({'pomeranians': 2}, target, greater_than_compounds, less_than_compounds), "pomeranians: 2 should match"

    # Should NOT match - boundary cases
    assert not matches_target({'pomeranians': 3}, target, greater_than_compounds, less_than_compounds), "pomeranians: 3 should NOT match (boundary)"
    assert not matches_target({'pomeranians': 4}, target, greater_than_compounds, less_than_compounds), "pomeranians: 4 should NOT match"

    print("✓ pomeranians < 3 rule tests passed")


def test_less_than_goldfish():
    """Test goldfish < 5 rule"""
    print("Testing goldfish < 5 rule...")

    # Should match
    assert matches_target({'goldfish': 0}, target, greater_than_compounds, less_than_compounds), "goldfish: 0 should match"
    assert matches_target({'goldfish': 1}, target, greater_than_compounds, less_than_compounds), "goldfish: 1 should match"
    assert matches_target({'goldfish': 4}, target, greater_than_compounds, less_than_compounds), "goldfish: 4 should match"

    # Should NOT match - boundary cases
    assert not matches_target({'goldfish': 5}, target, greater_than_compounds, less_than_compounds), "goldfish: 5 should NOT match (boundary)"
    assert not matches_target({'goldfish': 6}, target, greater_than_compounds, less_than_compounds), "goldfish: 6 should NOT match"

    print("✓ goldfish < 5 rule tests passed")


def test_exact_matches():
    """Test exact match rules for children, samoyeds, akitas, vizslas, cars, perfumes"""
    print("Testing exact match rules...")

    # Should match
    assert matches_target({'children': 3}, target, greater_than_compounds, less_than_compounds), "children: 3 should match"
    assert matches_target({'samoyeds': 2}, target, greater_than_compounds, less_than_compounds), "samoyeds: 2 should match"
    assert matches_target({'akitas': 0}, target, greater_than_compounds, less_than_compounds), "akitas: 0 should match"
    assert matches_target({'vizslas': 0}, target, greater_than_compounds, less_than_compounds), "vizslas: 0 should match"
    assert matches_target({'cars': 2}, target, greater_than_compounds, less_than_compounds), "cars: 2 should match"
    assert matches_target({'perfumes': 1}, target, greater_than_compounds, less_than_compounds), "perfumes: 1 should match"

    # Should NOT match
    assert not matches_target({'children': 2}, target, greater_than_compounds, less_than_compounds), "children: 2 should NOT match"
    assert not matches_target({'children': 4}, target, greater_than_compounds, less_than_compounds), "children: 4 should NOT match"
    assert not matches_target({'perfumes': 0}, target, greater_than_compounds, less_than_compounds), "perfumes: 0 should NOT match"
    assert not matches_target({'perfumes': 2}, target, greater_than_compounds, less_than_compounds), "perfumes: 2 should NOT match"

    print("✓ exact match rule tests passed")


def test_unlisted_compounds():
    """Test that unlisted compounds don't disqualify a match"""
    print("Testing unlisted compounds are ignored...")

    # Should match - only listed compounds are checked
    assert matches_target({'cats': 8, 'perfumes': 1, 'cars': 2}, target, greater_than_compounds, less_than_compounds), \
        "Should match even though 7 compounds are unlisted"

    print("✓ unlisted compounds test passed")


def test_multiple_compounds():
    """Test that ALL listed compounds must match"""
    print("Testing multiple compounds - ALL must match...")

    # Should NOT match - goldfish fails boundary (5 is not < 5)
    assert not matches_target({'cats': 8, 'goldfish': 5, 'perfumes': 1}, target, greater_than_compounds, less_than_compounds), \
        "Should NOT match - goldfish: 5 fails < 5 rule"

    # Should match - all three pass
    assert matches_target({'cats': 8, 'goldfish': 4, 'perfumes': 1}, target, greater_than_compounds, less_than_compounds), \
        "Should match - all three compounds pass"

    # Should match - mix of all three rule types
    assert matches_target({'children': 3, 'trees': 5, 'pomeranians': 1}, target, greater_than_compounds, less_than_compounds), \
        "Should match - exact, >, and < rules all pass"

    print("✓ multiple compounds test passed")


def test_actual_sue_241():
    """Test the actual answer: Sue 241"""
    print("Testing Sue 241 (actual answer)...")

    sue_241 = {'cars': 2, 'pomeranians': 1, 'samoyeds': 2}
    assert matches_target(sue_241, target, greater_than_compounds, less_than_compounds), \
        "Sue 241 should match"

    print("✓ Sue 241 matches correctly")


def run_all_tests():
    """Run all test cases"""
    print("="*60)
    print("Running unit tests for Part 2 matching logic")
    print("="*60)

    test_greater_than_cats()
    test_greater_than_trees()
    test_less_than_pomeranians()
    test_less_than_goldfish()
    test_exact_matches()
    test_unlisted_compounds()
    test_multiple_compounds()
    test_actual_sue_241()

    print("="*60)
    print("All tests passed! ✓")
    print("="*60)


if __name__ == '__main__':
    run_all_tests()
