#!/usr/bin/env python3
"""
Test verification script to validate the minimum boost solution.
"""

from solution import parse_input, apply_boost, simulate_combat, find_minimum_boost

def test_minimum_boost():
    """Test that the minimum boost is truly minimal."""

    # Find the minimum boost
    min_boost = find_minimum_boost()
    print(f"Minimum boost found: {min_boost}")

    # Test boost - 1 (should NOT win)
    print(f"\nTesting boost {min_boost - 1} (should NOT win):")
    immune_groups, infection_groups = parse_input("input.md")
    apply_boost(immune_groups, min_boost - 1)
    winner, units = simulate_combat(immune_groups, infection_groups)
    print(f"  Winner: {winner}, Units: {units}")

    if winner == "Immune System":
        print(f"  ❌ FAIL: Boost {min_boost - 1} should not win!")
        return False
    else:
        print(f"  ✓ PASS: Boost {min_boost - 1} correctly does not win")

    # Test minimum boost (should win)
    print(f"\nTesting boost {min_boost} (should win):")
    immune_groups, infection_groups = parse_input("input.md")
    apply_boost(immune_groups, min_boost)
    winner, units = simulate_combat(immune_groups, infection_groups)
    print(f"  Winner: {winner}, Units: {units}")

    if winner != "Immune System":
        print(f"  ❌ FAIL: Boost {min_boost} should win!")
        return False
    else:
        print(f"  ✓ PASS: Boost {min_boost} correctly wins with {units} units")

    # Test boost + 1 (should also win)
    print(f"\nTesting boost {min_boost + 1} (should also win):")
    immune_groups, infection_groups = parse_input("input.md")
    apply_boost(immune_groups, min_boost + 1)
    winner, units = simulate_combat(immune_groups, infection_groups)
    print(f"  Winner: {winner}, Units: {units}")

    if winner != "Immune System":
        print(f"  ❌ FAIL: Boost {min_boost + 1} should also win!")
        return False
    else:
        print(f"  ✓ PASS: Boost {min_boost + 1} correctly wins with {units} units")

    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60)

    return True

if __name__ == "__main__":
    success = test_minimum_boost()
    exit(0 if success else 1)
