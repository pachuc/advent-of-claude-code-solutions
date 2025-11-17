#!/usr/bin/env python3
"""Deep test of effect re-casting behavior."""

from solution import State, execute_player_turn, SPELLS

shield = SPELLS[2]

print("Testing effect re-casting on expiration turn")
print("=" * 60)

# According to the problem, at the start of each turn:
# 1. Effect applies its benefit/damage
# 2. Timer decreases by 1
# 3. If timer reaches 0, effect ends after applying
# 4. Effects can be started on the same turn they end

# Let's trace through what happens when shield_timer = 1

state = State(
    player_hp=50,
    player_mana=500,
    boss_hp=50,
    shield_timer=1,  # This is the last turn shield is active
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='player'
)

print(f"Starting state: shield_timer={state.shield_timer}")
print()

# When execute_player_turn is called:
# 1. Hard mode penalty: HP 50 -> 49
# 2. Apply effects: shield_timer decrements from 1 to 0
# 3. Check spell validity: shield_timer is now 0, so we CAN cast Shield

print("During execute_player_turn:")
print("  1. Hard mode penalty applied")
print("  2. Effects applied: shield_timer decrements 1 -> 0")
print("  3. Spell validation: shield_timer == 0, so Shield CAN be cast")
print()

result = execute_player_turn(state, shield)

if result is None:
    print("✗ FAIL: Shield was rejected, but shield_timer should be 0 after effects")
    print("This suggests the check happens BEFORE timer decrement")
else:
    print("✓ PASS: Shield was accepted after previous shield expired")
    print(f"New shield_timer: {result.shield_timer}")

print()
print("=" * 60)
print("Checking the exact timing in the code...")
print("=" * 60)

# Let me check the code logic
print("\nLooking at execute_player_turn in solution.py:")
print("Line 82-86: Hard mode penalty")
print("Line 101-102: apply_effects() is called")
print("Line 122-127: Spell validation checks")
print()

# The validation checks shield_timer > 0 AFTER apply_effects
# So if shield_timer starts at 1, apply_effects makes it 0, then validation passes

# Let me trace manually
print("Manual trace:")
print(f"  Initial shield_timer: 1")
print(f"  After apply_effects: shield_timer should be 0 (decremented)")
print(f"  Validation check: shield_timer > 0? No (0 is not > 0)")
print(f"  Result: Shield CAN be cast")
print()

# But the test says it failed. Let me check if shield even gets decremented during player turn
from solution import apply_effects

test_state = State(
    player_hp=49,  # After penalty
    player_mana=500,
    boss_hp=50,
    shield_timer=1,
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='player'
)

print("Testing apply_effects directly:")
print(f"  Input shield_timer: {test_state.shield_timer}")
new_state, boss_died = apply_effects(test_state)
print(f"  Output shield_timer: {new_state.shield_timer}")
print()

if new_state.shield_timer == 0:
    print("✓ apply_effects correctly decrements shield_timer from 1 to 0")
else:
    print("✗ apply_effects did NOT decrement shield_timer correctly")
