#!/usr/bin/env python3
"""Test that effects can be recast on the turn they expire."""

# In solution.py, the check is:
# if spell['effect'] == 'shield' and state['shield_timer'] > 0:
#     return None
# This means shield can be cast when timer = 0 (expired)

# Let's verify with a practical test
from solution import apply_effects, cast_spell, SPELLS

# Create a state where shield timer = 1
state = {
    'player_hp': 50,
    'player_mana': 500,
    'boss_hp': 50,
    'shield_timer': 1,
    'poison_timer': 0,
    'recharge_timer': 0,
    'mana_spent': 0
}

print("Initial state: shield_timer = 1")
print(f"Can cast Shield? {'No' if cast_spell(state, 'Shield') is None else 'Yes'}")

# Apply effects (timer should decrement to 0)
state, boss_died = apply_effects(state)
print(f"\nAfter applying effects: shield_timer = {state['shield_timer']}")
print(f"Can cast Shield? {'No' if cast_spell(state, 'Shield') is None else 'Yes'}")

# This should be 'Yes' because timer is now 0
result = cast_spell(state, 'Shield')
if result is not None:
    print(f"\nSUCCESS: Shield can be recast when timer = 0")
    print(f"New shield_timer after recasting: {result['shield_timer']}")
else:
    print(f"\nFAILURE: Shield cannot be recast when timer = 0 (BUG!)")
