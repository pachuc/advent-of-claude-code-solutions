#!/usr/bin/env python3
"""Test the solution with a simple example to verify logic."""

from solution import find_min_mana

# Test Case 1: Simple boss that should be killed quickly
# Boss: 14 HP, 8 damage
# Expected: Should be able to win with minimal mana

result = find_min_mana(14, 8)
print(f"Test Case 1 (Boss: 14 HP, 8 damage): {result} mana")

# Analyze the strategy:
# Magic Missile: 4 damage for 53 mana (need 4 casts = 212 mana)
# But player only has 50 HP and takes 8 damage per turn
# May need Shield (113 mana) to survive

# With Shield (armor 7): boss deals max(1, 8-7) = 1 damage
# This gives us 50 turns to kill boss

# Poison: 173 mana, deals 3 damage per turn for 6 turns = 18 damage
# So Poison alone would kill the boss (14 HP) in ~5 turns

# Test Case 2: Very weak boss - just to verify basic logic
result2 = find_min_mana(4, 1)
print(f"Test Case 2 (Boss: 4 HP, 1 damage): {result2} mana")
# Should be just Magic Missile (53 mana) since it deals exactly 4 damage

# Test Case 3: Actual puzzle input
result3 = find_min_mana(71, 10)
print(f"Test Case 3 (Boss: 71 HP, 10 damage): {result3} mana")
