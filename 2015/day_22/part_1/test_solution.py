from solution import find_min_mana, SPELLS

# Test with a very simple case
# Boss with 10 HP, 8 damage
# Player: 50 HP, 500 mana
# Magic Missile costs 53, deals 4 damage
# Need 3 casts = 159 mana to kill boss
# But player might die without Shield

print("Test 1: Simple boss (10 HP, 8 damage)")
result = find_min_mana(10, 8)
print(f"Result: {result} mana")
print(f"Expected: 226 (Poison 173 + Magic Missile 53) or similar")
print()

# Test with actual input
print("Test 2: Actual puzzle (71 HP, 10 damage)")
result = find_min_mana(71, 10)
print(f"Result: {result} mana")
print()

# Verify result is reasonable
# We need to deal 71 damage
# Most efficient damage: Poison deals 18 damage over 6 turns for 173 mana
# 4 Poisons = 72 damage for 692 mana (but they overlap, inefficient)
# Need a mix of spells
# Poison + other spells, with Shield for defense and Recharge for mana
print("Analysis:")
print(f"Pure Magic Missile: {71 // 4 + 1} casts = {(71 // 4 + 1) * 53} mana (but need Recharge)")
print(f"Pure Poison: {71 // 18 + 1} casts = {(71 // 18 + 1) * 173} mana (inefficient due to timing)")
print(f"Actual result: {result} mana - uses optimal spell combination")
