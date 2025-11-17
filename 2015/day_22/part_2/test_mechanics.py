#!/usr/bin/env python3
"""Test game mechanics in detail."""

from solution import State, execute_player_turn, execute_boss_turn, apply_effects, SPELLS

# Get spell references
magic_missile = SPELLS[0]
shield = SPELLS[2]
poison = SPELLS[3]

print("=" * 60)
print("TEST 1: Hard Mode Penalty Application")
print("=" * 60)
# Player starts at 2 HP
state = State(
    player_hp=2,
    player_mana=500,
    boss_hp=50,
    shield_timer=0,
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='player'
)

print(f"Initial: Player HP={state.player_hp}, Mana={state.player_mana}")
new_state = execute_player_turn(state, magic_missile)
if new_state:
    print(f"After player turn: Player HP={new_state.player_hp}, Boss HP={new_state.boss_hp}")
    print("✓ PASS: Player survives with 1 HP (2 - 1 hard mode penalty)")
else:
    print("✗ FAIL: Player should survive")

print()

# Player at 1 HP - should die from hard mode penalty
state2 = State(
    player_hp=1,
    player_mana=500,
    boss_hp=50,
    shield_timer=0,
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='player'
)

print(f"Initial: Player HP={state2.player_hp}")
new_state2 = execute_player_turn(state2, magic_missile)
if new_state2 is None:
    print("✓ PASS: Player dies from hard mode penalty (1 - 1 = 0)")
else:
    print("✗ FAIL: Player should die from hard mode penalty")

print()
print("=" * 60)
print("TEST 2: Effect Application Order")
print("=" * 60)

# Test poison application on boss turn
state3 = State(
    player_hp=50,
    player_mana=500,
    boss_hp=10,
    shield_timer=0,
    poison_timer=3,  # 3 turns remaining
    recharge_timer=0,
    mana_spent=0,
    turn='boss'
)

print(f"Initial: Boss HP={state3.boss_hp}, Poison Timer={state3.poison_timer}")
new_state3 = execute_boss_turn(state3, 10)
print(f"After boss turn: Boss HP={new_state3.boss_hp}, Poison Timer={new_state3.poison_timer}")
expected_boss_hp = 10 - 3  # Poison deals 3 damage
expected_poison_timer = 3 - 1  # Timer decrements
if new_state3.boss_hp == expected_boss_hp and new_state3.poison_timer == expected_poison_timer:
    print(f"✓ PASS: Poison applied correctly (Boss HP: {expected_boss_hp}, Timer: {expected_poison_timer})")
else:
    print(f"✗ FAIL: Expected Boss HP={expected_boss_hp}, Timer={expected_poison_timer}")

print()
print("=" * 60)
print("TEST 3: Effect Expiration and Re-casting")
print("=" * 60)

# Test Shield expiring and re-casting
state4 = State(
    player_hp=50,
    player_mana=500,
    boss_hp=50,
    shield_timer=1,  # Will expire this turn
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='player'
)

print(f"Initial: Shield Timer={state4.shield_timer} (will expire this turn)")

# Try casting shield - should NOT be allowed (timer > 0 before effect application)
new_state4 = execute_player_turn(state4, shield)
if new_state4 is None:
    print("✓ PASS: Cannot cast Shield while Shield timer > 0")
else:
    print("✗ FAIL: Should not be able to cast Shield while active")

# Now manually apply effects to expire the shield
state5 = State(
    player_hp=49,  # After hard mode penalty
    player_mana=500,
    boss_hp=50,
    shield_timer=0,  # Expired
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='player'
)

print(f"\nAfter shield expires: Shield Timer={state5.shield_timer}")
new_state5 = execute_player_turn(state5, shield)
if new_state5 and new_state5.shield_timer == 6:
    print("✓ PASS: Can cast Shield after it expires (timer now 6)")
else:
    print("✗ FAIL: Should be able to cast Shield after expiration")

print()
print("=" * 60)
print("TEST 4: Boss Damage with Shield")
print("=" * 60)

# Without shield
state6 = State(
    player_hp=50,
    player_mana=500,
    boss_hp=50,
    shield_timer=0,
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='boss'
)

print("Without Shield:")
print(f"Initial: Player HP={state6.player_hp}, Shield Timer={state6.shield_timer}")
new_state6 = execute_boss_turn(state6, 10)
print(f"After boss attack: Player HP={new_state6.player_hp}")
if new_state6.player_hp == 40:  # 50 - 10
    print("✓ PASS: Boss deals 10 damage without shield")
else:
    print(f"✗ FAIL: Expected 40 HP, got {new_state6.player_hp}")

# With shield
state7 = State(
    player_hp=50,
    player_mana=500,
    boss_hp=50,
    shield_timer=3,
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='boss'
)

print("\nWith Shield:")
print(f"Initial: Player HP={state7.player_hp}, Shield Timer={state7.shield_timer}")
new_state7 = execute_boss_turn(state7, 10)
print(f"After boss attack: Player HP={new_state7.player_hp}")
expected_hp = 50 - max(1, 10 - 7)  # 50 - 3 = 47
if new_state7.player_hp == expected_hp:
    print(f"✓ PASS: Boss deals {10-7}=3 damage with shield (armor 7)")
else:
    print(f"✗ FAIL: Expected {expected_hp} HP, got {new_state7.player_hp}")

print()
print("=" * 60)
print("TEST 5: Boss Death from Effects")
print("=" * 60)

state8 = State(
    player_hp=50,
    player_mana=500,
    boss_hp=3,  # Will die from poison
    shield_timer=0,
    poison_timer=2,
    recharge_timer=0,
    mana_spent=0,
    turn='boss'
)

print(f"Initial: Boss HP={state8.boss_hp}, Poison Timer={state8.poison_timer}")
new_state8 = execute_boss_turn(state8, 10)
print(f"After boss turn: Boss HP={new_state8.boss_hp}")
if new_state8.boss_hp <= 0:
    print("✓ PASS: Boss dies from poison effect (3 HP - 3 poison damage)")
else:
    print("✗ FAIL: Boss should die from poison")

print()
print("=" * 60)
print("All mechanics tests completed!")
print("=" * 60)
