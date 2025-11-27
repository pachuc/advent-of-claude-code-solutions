#!/usr/bin/env python3
"""Verification script to test the solution against test cases"""

from solution import parse_input, simulate_combat, calculate_outcome, sort_units, find_targets

def test_parse_input():
    """Test 1.1: Parse Input"""
    test_input = """#######
#.G.E.#
#######"""

    grid, units = parse_input(test_input)

    assert len(units) == 2, f"Expected 2 units, got {len(units)}"
    assert units[0].type == 'G', f"First unit should be G, got {units[0].type}"
    assert units[0].x == 2 and units[0].y == 1, f"First unit position should be (2,1), got ({units[0].x},{units[0].y})"
    assert units[1].type == 'E', f"Second unit should be E, got {units[1].type}"
    assert units[1].x == 4 and units[1].y == 1, f"Second unit position should be (4,1), got ({units[1].x},{units[1].y})"

    print("✓ Test 1.1: Parse Input - PASSED")


def test_reading_order():
    """Test 1.2: Reading Order Sort"""
    from solution import Unit

    units = [
        Unit(5, 2, 'G'),
        Unit(1, 1, 'E'),
        Unit(3, 1, 'G'),
        Unit(2, 3, 'E')
    ]

    sorted_units = sort_units(units)
    sorted_positions = [(u.x, u.y) for u in sorted_units]
    expected = [(1, 1), (3, 1), (5, 2), (2, 3)]

    assert sorted_positions == expected, f"Expected {expected}, got {sorted_positions}"

    print("✓ Test 1.2: Reading Order Sort - PASSED")


def test_find_targets():
    """Test 1.3: Find Targets"""
    from solution import Unit

    units = [
        Unit(1, 1, 'G'),
        Unit(2, 1, 'G'),
        Unit(3, 1, 'G'),
        Unit(4, 1, 'E'),
        Unit(5, 1, 'E')
    ]

    goblin = units[0]
    targets = find_targets(goblin, units)

    assert len(targets) == 2, f"Expected 2 targets, got {len(targets)}"
    assert all(t.type == 'E' for t in targets), "All targets should be Elves"

    print("✓ Test 1.3: Find Targets - PASSED")


def test_adjacent_combat():
    """Test 3.4: No Movement Needed - Adjacent Combat"""
    test_input = """#####
#GE##
#####"""

    grid, units = parse_input(test_input)

    # Run combat
    rounds = simulate_combat(grid, units)

    # Expected: 66 completed rounds (Round 67 ends mid-round when Goblin kills Elf)
    # After 66 rounds: both should have 200 - 66*3 = 2 HP
    # Round 67: Goblin attacks first (reading order), Elf dies

    living = [u for u in units if u.alive]

    assert len(living) == 1, f"Expected 1 survivor, got {len(living)}"
    assert living[0].type == 'G', f"Expected Goblin to win, got {living[0].type}"
    assert rounds == 66, f"Expected 66 completed rounds, got {rounds}"
    assert living[0].hp == 2, f"Expected winner to have 2 HP, got {living[0].hp}"

    outcome = calculate_outcome(rounds, units)
    expected_outcome = 66 * 2
    assert outcome == expected_outcome, f"Expected outcome {expected_outcome}, got {outcome}"

    print("✓ Test 3.4: Adjacent Combat - PASSED")
    print(f"  Rounds: {rounds}, Winner HP: {living[0].hp}, Outcome: {outcome}")


def test_move_and_attack():
    """Test 2.2: Move and Attack in One Turn"""
    test_input = """#####
#G.E#
#####"""

    grid, units = parse_input(test_input)

    goblin = units[0]
    elf = units[1]

    # Execute one round
    from solution import execute_round
    execute_round(units, grid)

    # After round 1:
    # - Goblin should have moved to (2, 1) and attacked
    # - Elf should have attacked back

    assert goblin.x == 2 and goblin.y == 1, f"Goblin should be at (2,1), got ({goblin.x},{goblin.y})"
    assert elf.hp == 197, f"Elf should have 197 HP, got {elf.hp}"
    assert goblin.hp == 197, f"Goblin should have 197 HP, got {goblin.hp}"

    print("✓ Test 2.2: Move and Attack - PASSED")
    print(f"  Goblin moved to ({goblin.x},{goblin.y}), both have 197 HP")


def test_actual_input():
    """Test 4.1: Actual Input Validation"""
    with open('input.md', 'r') as f:
        input_text = f.read()

    grid, units = parse_input(input_text)

    initial_goblins = sum(1 for u in units if u.type == 'G')
    initial_elves = sum(1 for u in units if u.type == 'E')

    print(f"Initial state: {initial_elves} Elves, {initial_goblins} Goblins")

    rounds = simulate_combat(grid, units)

    living = [u for u in units if u.alive]
    total_hp = sum(u.hp for u in living)
    outcome = calculate_outcome(rounds, units)

    # Verify all living units are same type
    if living:
        winner_type = living[0].type
        assert all(u.type == winner_type for u in living), "All survivors should be same type"

    assert len(living) > 0, "At least one unit should survive"
    assert outcome > 0, "Outcome should be positive"

    print("✓ Test 4.1: Actual Input - PASSED")
    print(f"  Rounds: {rounds}")
    print(f"  Survivors: {len(living)} {living[0].type if living else 'None'}")
    print(f"  Total HP: {total_hp}")
    print(f"  Outcome: {outcome}")

    return outcome


def main():
    """Run all tests"""
    print("=" * 60)
    print("VERIFICATION TESTS")
    print("=" * 60)
    print()

    try:
        test_parse_input()
        test_reading_order()
        test_find_targets()
        test_move_and_attack()
        test_adjacent_combat()
        print()
        print("=" * 60)
        outcome = test_actual_input()
        print("=" * 60)
        print()
        print(f"FINAL ANSWER: {outcome}")
        print()
        print("ALL TESTS PASSED!")
        return outcome

    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"TEST FAILED: {e}")
        print("=" * 60)
        return None


if __name__ == "__main__":
    main()
