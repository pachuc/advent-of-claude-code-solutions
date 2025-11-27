#!/usr/bin/env python3
"""Verification script for the solution."""

import solution

def test_parsing():
    """Test that parsing works correctly."""
    print("Testing parsing...")
    immune_groups, infection_groups = solution.parse_input("input.md")

    print(f"  Immune System groups: {len(immune_groups)}")
    print(f"  Infection groups: {len(infection_groups)}")

    # Verify we have 10 groups for each army (as mentioned in implementation summary)
    assert len(immune_groups) == 10, f"Expected 10 Immune groups, got {len(immune_groups)}"
    assert len(infection_groups) == 10, f"Expected 10 Infection groups, got {len(infection_groups)}"

    # Test specific parsing examples from test plan
    # First immune group: 6638 units, 2292 HP, weak to radiation, 3 cold damage, initiative 18
    g = immune_groups[0]
    assert g.units == 6638, f"Expected 6638 units, got {g.units}"
    assert g.hit_points == 2292, f"Expected 2292 HP, got {g.hit_points}"
    assert "radiation" in g.weaknesses, f"Expected weak to radiation"
    assert g.attack_damage == 3, f"Expected 3 attack damage, got {g.attack_damage}"
    assert g.attack_type == "cold", f"Expected cold attack type, got {g.attack_type}"
    assert g.initiative == 18, f"Expected initiative 18, got {g.initiative}"

    # Second immune group should have multiple immunities
    g = immune_groups[1]
    assert "bludgeoning" in g.immunities, "Expected immune to bludgeoning"
    assert "cold" in g.immunities, "Expected immune to cold"
    assert "fire" in g.immunities, "Expected immune to fire"

    # First infection group: immune to bludgeoning
    g = infection_groups[0]
    assert g.units == 1756, f"Expected 1756 units, got {g.units}"
    assert "bludgeoning" in g.immunities, "Expected immune to bludgeoning"

    print("  ✓ Parsing tests passed!")
    return True

def test_damage_calculations():
    """Test damage calculation logic."""
    print("\nTesting damage calculations...")

    # Create test groups
    attacker = solution.Group(1, "Immune System", 100, 100, 10, "fire", 10)

    # Normal damage (no modifiers)
    defender_normal = solution.Group(2, "Infection", 50, 50, 5, "cold", 5)
    damage = attacker.calculate_damage_to(defender_normal)
    assert damage == 1000, f"Expected 1000 damage, got {damage}"

    # Immunity (zero damage)
    defender_immune = solution.Group(3, "Infection", 50, 50, 5, "cold", 5, immunities={"fire"})
    damage = attacker.calculate_damage_to(defender_immune)
    assert damage == 0, f"Expected 0 damage (immune), got {damage}"

    # Weakness (double damage)
    defender_weak = solution.Group(4, "Infection", 50, 50, 5, "cold", 5, weaknesses={"fire"})
    damage = attacker.calculate_damage_to(defender_weak)
    assert damage == 2000, f"Expected 2000 damage (weak), got {damage}"

    print("  ✓ Damage calculation tests passed!")
    return True

def test_unit_death():
    """Test unit death calculations."""
    print("\nTesting unit death...")

    group = solution.Group(1, "Infection", 100, 50, 10, "fire", 5)

    # Kill exactly 10 units
    killed = group.take_damage(500)
    assert killed == 10, f"Expected 10 killed, got {killed}"
    assert group.units == 90, f"Expected 90 remaining, got {group.units}"

    # Partial damage (not enough to kill)
    killed = group.take_damage(25)
    assert killed == 0, f"Expected 0 killed, got {killed}"
    assert group.units == 90, f"Expected 90 remaining, got {group.units}"

    # Kill all remaining
    killed = group.take_damage(4500)
    assert killed == 90, f"Expected 90 killed, got {killed}"
    assert group.units == 0, f"Expected 0 remaining, got {group.units}"
    assert not group.is_alive(), "Group should be dead"

    print("  ✓ Unit death tests passed!")
    return True

def test_full_simulation():
    """Test full simulation."""
    print("\nTesting full simulation...")

    immune_groups, infection_groups = solution.parse_input("input.md")
    winner, units = solution.simulate_combat(immune_groups, infection_groups)

    print(f"  Winner: {winner}")
    print(f"  Remaining units: {units}")

    # According to implementation summary, Infection should win with 22244 units
    assert winner == "Infection", f"Expected Infection to win, got {winner}"
    assert units == 22244, f"Expected 22244 units, got {units}"

    print("  ✓ Full simulation test passed!")
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("VERIFICATION TESTS")
    print("=" * 60)

    all_passed = True

    try:
        all_passed &= test_parsing()
        all_passed &= test_damage_calculations()
        all_passed &= test_unit_death()
        all_passed &= test_full_simulation()
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        all_passed = False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
