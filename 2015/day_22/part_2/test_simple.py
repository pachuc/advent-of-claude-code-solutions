#!/usr/bin/env python3
"""Test solution with simple boss scenarios."""

from solution import find_minimum_mana

# Test Case 1: Very weak boss (HP: 8, Damage: 3)
# Expected: 2× Magic Missile = 106 mana
result1 = find_minimum_mana(8, 3)
print(f"Test 1 (Boss HP=8, Damage=3): {result1} mana (expected: 106)")

# Test Case 2: Simple boss (HP: 20, Damage: 5)
# Expected: Magic Missile spam ≤ 265 mana
result2 = find_minimum_mana(20, 5)
print(f"Test 2 (Boss HP=20, Damage=5): {result2} mana (expected: ≤265)")

# Test Case 3: Poison-favorable boss (HP: 18, Damage: 3)
result3 = find_minimum_mana(18, 3)
print(f"Test 3 (Boss HP=18, Damage=3): {result3} mana")

# Test Case 4: Impossible scenario (HP: 50, Damage: 50)
result4 = find_minimum_mana(50, 50)
print(f"Test 4 (Boss HP=50, Damage=50): {result4} (expected: None)")

# Test Case 5: Actual input
result5 = find_minimum_mana(71, 10)
print(f"Test 5 (Boss HP=71, Damage=10): {result5} mana (expected: 1937)")
