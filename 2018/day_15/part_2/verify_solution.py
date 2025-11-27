#!/usr/bin/env python3
"""
Comprehensive test suite to verify the Part 2 solution.
"""

from solution import (
    parse_input, simulate_combat, calculate_outcome,
    simulate_with_elf_check, find_minimum_elf_attack_power
)


def test_part1_regression():
    """Test that Part 1 still works correctly with attack power 3 for both sides"""
    print("Test 1: Part 1 regression test...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    # Simulate with attack power 3 for both (Part 1 scenario)
    grid, units = parse_input(input_text, 3, 3)
    rounds = simulate_combat(grid, units)
    outcome = calculate_outcome(rounds, units)

    expected = 218272
    if outcome == expected:
        print(f"  ✓ PASS: Part 1 outcome = {outcome}")
        return True
    else:
        print(f"  ✗ FAIL: Expected {expected}, got {outcome}")
        return False


def test_minimum_power_constraint():
    """Test that minimum attack power is at least 4"""
    print("\nTest 2: Minimum power constraint...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    min_power, _, _ = find_minimum_elf_attack_power(input_text)

    if min_power >= 4:
        print(f"  ✓ PASS: Minimum power = {min_power} >= 4")
        return True
    else:
        print(f"  ✗ FAIL: Minimum power = {min_power} < 4")
        return False


def test_all_elves_survive():
    """Test that all Elves survive with minimum attack power"""
    print("\nTest 3: All Elves survive...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    min_power, _, _ = find_minimum_elf_attack_power(input_text)

    # Count initial Elves
    grid, units = parse_input(input_text, min_power, 3)
    initial_elves = sum(1 for u in units if u.type == 'E')

    # Run simulation
    simulate_combat(grid, units)

    # Count surviving Elves
    surviving_elves = sum(1 for u in units if u.alive and u.type == 'E')

    if surviving_elves == initial_elves:
        print(f"  ✓ PASS: {surviving_elves}/{initial_elves} Elves survived")
        return True
    else:
        print(f"  ✗ FAIL: Only {surviving_elves}/{initial_elves} Elves survived")
        return False


def test_all_goblins_defeated():
    """Test that all Goblins are defeated"""
    print("\nTest 4: All Goblins defeated...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    min_power, _, _ = find_minimum_elf_attack_power(input_text)

    # Run simulation
    grid, units = parse_input(input_text, min_power, 3)
    simulate_combat(grid, units)

    # Count surviving Goblins
    surviving_goblins = sum(1 for u in units if u.alive and u.type == 'G')

    if surviving_goblins == 0:
        print(f"  ✓ PASS: All Goblins defeated (0 remaining)")
        return True
    else:
        print(f"  ✗ FAIL: {surviving_goblins} Goblins still alive")
        return False


def test_minimum_is_actually_minimum():
    """Test that (min_power - 1) results in failure"""
    print("\nTest 5: Minimum is actually minimum...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    min_power, _, _ = find_minimum_elf_attack_power(input_text)

    # Test that min_power - 1 fails
    if min_power > 4:
        success_lower, _, _ = simulate_with_elf_check(input_text, min_power - 1)

        if not success_lower:
            print(f"  ✓ PASS: Attack power {min_power - 1} fails (Elf casualty)")

            # Verify min_power succeeds
            success_min, _, _ = simulate_with_elf_check(input_text, min_power)
            if success_min:
                print(f"  ✓ PASS: Attack power {min_power} succeeds (no casualties)")
                return True
            else:
                print(f"  ✗ FAIL: Attack power {min_power} unexpectedly fails")
                return False
        else:
            print(f"  ✗ FAIL: Attack power {min_power - 1} succeeds (should fail)")
            return False
    else:
        print(f"  ⊗ SKIP: Min power is 4, can't test lower")
        return True


def test_outcome_calculation():
    """Test that outcome calculation is correct"""
    print("\nTest 6: Outcome calculation...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    min_power, reported_rounds, reported_outcome = find_minimum_elf_attack_power(input_text)

    # Re-simulate to verify
    grid, units = parse_input(input_text, min_power, 3)
    actual_rounds = simulate_combat(grid, units)

    # Calculate outcome manually
    surviving_units = [u for u in units if u.alive]
    total_hp = sum(u.hp for u in surviving_units)
    expected_outcome = actual_rounds * total_hp

    if reported_outcome == expected_outcome and reported_rounds == actual_rounds:
        print(f"  ✓ PASS: Outcome = {reported_rounds} × {total_hp} = {reported_outcome}")
        return True
    else:
        print(f"  ✗ FAIL: Expected {expected_outcome}, got {reported_outcome}")
        print(f"         Rounds: expected {actual_rounds}, got {reported_rounds}")
        return False


def test_determinism():
    """Test that multiple runs produce identical results"""
    print("\nTest 7: Determinism...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    # Run simulation 3 times with same attack power
    results = []
    for i in range(3):
        success, rounds, outcome = simulate_with_elf_check(input_text, 25)
        results.append((success, rounds, outcome))

    # Check all results are identical
    if all(r == results[0] for r in results):
        print(f"  ✓ PASS: All 3 runs produced identical results: {results[0]}")
        return True
    else:
        print(f"  ✗ FAIL: Results differ across runs:")
        for i, r in enumerate(results):
            print(f"         Run {i+1}: {r}")
        return False


def test_attack_power_propagation():
    """Test that Elves actually use custom attack power"""
    print("\nTest 8: Attack power propagation...")

    # Simple test case
    sample_input = """#######
#..G..#
#.E...#
#######"""

    # With attack 200, should kill Goblin (200 HP) very quickly
    grid, units = parse_input(sample_input, 200, 3)

    # Verify Elf has attack 200
    elf = [u for u in units if u.type == 'E'][0]
    if elf.attack != 200:
        print(f"  ✗ FAIL: Elf attack power is {elf.attack}, expected 200")
        return False

    # Run simulation - should be very quick
    rounds = simulate_combat(grid, units)

    if rounds <= 3:  # Should be 1-2 rounds max
        print(f"  ✓ PASS: High attack power leads to quick victory ({rounds} rounds)")
        return True
    else:
        print(f"  ✗ FAIL: Too many rounds ({rounds}) with attack 200")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("PART 2 SOLUTION VERIFICATION")
    print("="*60)

    tests = [
        test_part1_regression,
        test_minimum_power_constraint,
        test_all_elves_survive,
        test_all_goblins_defeated,
        test_minimum_is_actually_minimum,
        test_outcome_calculation,
        test_determinism,
        test_attack_power_propagation,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            results.append(False)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    passed = sum(results)
    total = len(results)

    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("\n✓ ALL TESTS PASSED - Solution is correct!")
        return 0
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED - Solution has issues")
        return 1


if __name__ == "__main__":
    exit(main())
