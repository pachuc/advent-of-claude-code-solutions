#!/usr/bin/env python3
"""Test script for the wizard simulator solution."""

from solution import find_minimum_mana

def test_very_weak_boss():
    """Test Case: Very Weak Boss - Boss HP: 8, Damage: 3"""
    print("Test 1: Very Weak Boss (HP: 8, Damage: 3)")
    print("Expected: 106 mana (2 Magic Missiles)")
    result = find_minimum_mana(8, 3)
    print(f"Result: {result} mana")
    print(f"Status: {'PASS' if result == 106 else 'FAIL'}")
    print()

def test_simple_boss():
    """Test Case: Simple Boss - Boss HP: 20, Damage: 5"""
    print("Test 2: Simple Boss (HP: 20, Damage: 5)")
    print("Expected: ~265 mana (5 Magic Missiles)")
    result = find_minimum_mana(20, 5)
    print(f"Result: {result} mana")
    # Magic Missile spam: 5 * 53 = 265 mana
    print(f"Status: {'PASS' if result <= 265 else 'UNCERTAIN'}")
    print()

def test_poison_favorable():
    """Test Case: Poison-Favorable Boss - Boss HP: 18, Damage: 3"""
    print("Test 3: Poison-Favorable Boss (HP: 18, Damage: 3)")
    print("Expected: 173 mana (1 Poison)")
    result = find_minimum_mana(18, 3)
    print(f"Result: {result} mana")
    print(f"Status: {'PASS' if result == 173 else 'UNCERTAIN'}")
    print()

def test_impossible_scenario():
    """Test Case: Impossible scenario - Boss damage too high"""
    print("Test 4: Impossible Scenario (HP: 50, Damage: 50)")
    print("Expected: None (no winning strategy)")
    result = find_minimum_mana(50, 50)
    print(f"Result: {result}")
    print(f"Status: {'PASS' if result is None else 'FAIL'}")
    print()

def test_actual_input():
    """Test Case: Actual input - Boss HP: 71, Damage: 10"""
    print("Test 5: Actual Input (HP: 71, Damage: 10)")
    print("Expected: ~900-1500 mana range")
    result = find_minimum_mana(71, 10)
    print(f"Result: {result} mana")
    print(f"Status: {'PASS' if 900 <= result <= 1500 else 'UNCERTAIN'}")
    print()

if __name__ == '__main__':
    print("=" * 60)
    print("Running Tests for Wizard Simulator (Hard Mode)")
    print("=" * 60)
    print()

    test_very_weak_boss()
    test_simple_boss()
    test_poison_favorable()
    test_impossible_scenario()
    test_actual_input()

    print("=" * 60)
    print("Tests Complete")
    print("=" * 60)
