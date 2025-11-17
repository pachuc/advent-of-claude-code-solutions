#!/usr/bin/env python3
"""Test script to verify the solution implementation."""

from solution import (
    player_wins, generate_ring_combinations, generate_loadouts,
    calculate_stats, weapons, armor_items, rings, PLAYER_HP
)

def test_combat_simulation():
    """Test combat simulation with various scenarios from test plan."""
    print("Testing Combat Simulation...")

    # Test 1.1: Basic Combat - Player Wins
    result = player_wins(8, 5, 5, 12, 7, 2)
    assert result == True, "Test 1.1 failed: Player should win"
    print("✓ Test 1.1: Basic player victory")

    # Test 1.2: Basic Combat - Player Loses
    result = player_wins(8, 5, 5, 12, 7, 3)
    assert result == False, "Test 1.2 failed: Player should lose"
    print("✓ Test 1.2: Basic player defeat")

    # Test 1.3: Minimum Damage Rule (High Armor)
    result = player_wins(10, 3, 0, 10, 2, 5)
    assert result == False, "Test 1.3 failed: Player should lose despite minimum damage"
    print("✓ Test 1.3: Minimum damage rule")

    # Test 1.4: Armor Exceeds Damage - Both Sides
    result = player_wins(100, 1, 10, 100, 1, 10)
    assert result == True, "Test 1.4 failed: Player should win with first-move advantage"
    print("✓ Test 1.4: Equal stats with minimum damage")

    # Test 1.5: One-Shot Victory
    result = player_wins(10, 100, 0, 50, 50, 0)
    assert result == True, "Test 1.5 failed: Player should win in one turn"
    print("✓ Test 1.5: One-shot victory")

    # Test 1.6: Equal Stats - First Move Advantage
    result = player_wins(50, 5, 2, 50, 5, 2)
    assert result == True, "Test 1.6 failed: Player should win with first-move advantage"
    print("✓ Test 1.6: First-move advantage")

    print("All combat simulation tests passed!\n")


def test_combination_generation():
    """Test equipment combination generation."""
    print("Testing Equipment Combination Generation...")

    # Test ring combinations
    ring_combos = list(generate_ring_combinations(rings))
    assert len(ring_combos) == 22, f"Expected 22 ring combos, got {len(ring_combos)}"
    print(f"✓ Ring combinations: {len(ring_combos)} (expected 22)")

    # Test total loadouts
    loadouts = generate_loadouts(weapons, armor_items, rings)
    assert len(loadouts) == 660, f"Expected 660 loadouts, got {len(loadouts)}"
    print(f"✓ Total loadouts: {len(loadouts)} (expected 660)")

    # Verify breakdown
    without_armor = sum(1 for loadout in loadouts if not any(item in armor_items for item in loadout))
    with_armor = len(loadouts) - without_armor
    print(f"  - Without armor: {without_armor} (expected 110)")
    print(f"  - With armor: {with_armor} (expected 550)")

    assert without_armor == 110, f"Expected 110 loadouts without armor, got {without_armor}"
    assert with_armor == 550, f"Expected 550 loadouts with armor, got {with_armor}"

    # Check constraints on first few loadouts
    for i, loadout in enumerate(loadouts[:20]):
        weapon_count = sum(1 for item in loadout if item in weapons)
        armor_count = sum(1 for item in loadout if item in armor_items)
        ring_count = sum(1 for item in loadout if item in rings)

        assert weapon_count == 1, f"Loadout {i} has {weapon_count} weapons (should be 1)"
        assert armor_count in [0, 1], f"Loadout {i} has {armor_count} armor (should be 0 or 1)"
        assert ring_count in [0, 1, 2], f"Loadout {i} has {ring_count} rings (should be 0, 1, or 2)"
        assert len(loadout) == len(set([item['name'] for item in loadout])), f"Loadout {i} has duplicate items"

    print("✓ Loadout constraints verified\n")


def test_stats_calculation():
    """Test stats calculation."""
    print("Testing Stats Calculation...")

    # Test 3.1: Single Weapon Only
    dagger = [weapons[0]]  # Dagger
    cost, damage, armor = calculate_stats(dagger)
    assert cost == 8 and damage == 4 and armor == 0, "Test 3.1 failed"
    print("✓ Test 3.1: Single weapon (cost=8, dmg=4, arm=0)")

    # Test 3.2: Weapon + Armor
    loadout = [weapons[0], armor_items[0]]  # Dagger + Leather
    cost, damage, armor = calculate_stats(loadout)
    assert cost == 21 and damage == 4 and armor == 1, "Test 3.2 failed"
    print("✓ Test 3.2: Weapon + armor (cost=21, dmg=4, arm=1)")

    # Test 3.3: Weapon + Two Rings
    loadout = [weapons[0], rings[0], rings[3]]  # Dagger + Damage+1 + Defense+1
    cost, damage, armor = calculate_stats(loadout)
    assert cost == 53 and damage == 5 and armor == 1, "Test 3.3 failed"
    print("✓ Test 3.3: Weapon + 2 rings (cost=53, dmg=5, arm=1)")

    # Test 3.4: Full Loadout
    loadout = [weapons[4], armor_items[4], rings[2], rings[5]]  # Greataxe + Platemail + Damage+3 + Defense+3
    cost, damage, armor = calculate_stats(loadout)
    assert cost == 356 and damage == 11 and armor == 8, "Test 3.4 failed"
    print("✓ Test 3.4: Full loadout (cost=356, dmg=11, arm=8)\n")


def test_winning_loadout():
    """Test the specific winning loadout mentioned in implementation summary."""
    print("Testing Winning Loadout (121 gold)...")

    # Boss stats from input
    boss_hp, boss_damage, boss_armor = 103, 9, 2

    # According to implementation summary:
    # Longsword (40g, 7 damage) + Chainmail (31g, 2 armor) + Damage +2 ring (50g, 2 damage)
    longsword = weapons[3]  # Longsword
    chainmail = armor_items[1]  # Chainmail
    damage_2_ring = rings[1]  # Damage +2

    loadout = [longsword, chainmail, damage_2_ring]
    cost, damage, armor = calculate_stats(loadout)

    print(f"Loadout items: {[item['name'] for item in loadout]}")
    print(f"Total cost: {cost} gold (expected 121)")
    print(f"Player stats: HP={PLAYER_HP}, Damage={damage}, Armor={armor}")
    print(f"Boss stats: HP={boss_hp}, Damage={boss_damage}, Armor={boss_armor}")

    assert cost == 121, f"Cost should be 121, got {cost}"
    assert damage == 9, f"Damage should be 9, got {damage}"
    assert armor == 2, f"Armor should be 2, got {armor}"

    # Verify player wins
    wins = player_wins(PLAYER_HP, damage, armor, boss_hp, boss_damage, boss_armor)

    # Manual calculation
    player_damage_per_hit = max(1, damage - boss_armor)  # max(1, 9-2) = 7
    boss_damage_per_hit = max(1, boss_damage - armor)  # max(1, 9-2) = 7

    import math
    turns_to_kill_boss = math.ceil(boss_hp / player_damage_per_hit)  # ceil(103/7) = 15
    turns_to_kill_player = math.ceil(PLAYER_HP / boss_damage_per_hit)  # ceil(100/7) = 15

    print(f"Player damage per turn: {player_damage_per_hit}")
    print(f"Boss damage per turn: {boss_damage_per_hit}")
    print(f"Turns to kill boss: {turns_to_kill_boss}")
    print(f"Turns to kill player: {turns_to_kill_player}")
    print(f"Player wins: {wins} (expected True due to first-move advantage)")

    assert wins == True, "Player should win with this loadout"
    print("✓ Winning loadout verified!\n")


def test_no_cheaper_winner():
    """Verify no cheaper loadout can win."""
    print("Testing that no cheaper loadout wins...")

    from solution import parse_input, find_minimum_cost
    boss_stats = parse_input('input.md')

    # Generate all loadouts and check those costing less than 121
    cheaper_winners = []
    for loadout in generate_loadouts(weapons, armor_items, rings):
        cost, damage, armor = calculate_stats(loadout)
        if cost < 121:
            if player_wins(PLAYER_HP, damage, armor,
                          boss_stats['hit_points'], boss_stats['damage'], boss_stats['armor']):
                cheaper_winners.append((cost, loadout))

    if cheaper_winners:
        print(f"ERROR: Found {len(cheaper_winners)} cheaper winning loadouts!")
        for cost, loadout in sorted(cheaper_winners)[:5]:
            print(f"  Cost {cost}: {[item['name'] for item in loadout]}")
        return False
    else:
        print("✓ No cheaper winning loadout exists")
        return True


if __name__ == '__main__':
    print("=" * 60)
    print("SOLUTION VERIFICATION TESTS")
    print("=" * 60 + "\n")

    test_combat_simulation()
    test_combination_generation()
    test_stats_calculation()
    test_winning_loadout()
    no_cheaper = test_no_cheaper_winner()

    print("=" * 60)
    if no_cheaper:
        print("ALL TESTS PASSED!")
        print("Solution is CORRECT: 121 gold")
    else:
        print("TESTS FAILED!")
        print("Solution may be INCORRECT")
    print("=" * 60)
