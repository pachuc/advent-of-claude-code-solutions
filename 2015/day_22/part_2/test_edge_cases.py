#!/usr/bin/env python3
"""Test edge cases."""

from solution import State, execute_player_turn, SPELLS
import time

magic_missile = SPELLS[0]
drain = SPELLS[1]

print("=" * 60)
print("TEST 1: Not Enough Mana")
print("=" * 60)

state = State(
    player_hp=50,
    player_mana=50,  # Less than magic missile cost
    boss_hp=50,
    shield_timer=0,
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='player'
)

print(f"Player mana: {state.player_mana}, Magic Missile cost: {magic_missile['cost']}")
result = execute_player_turn(state, magic_missile)
if result is None:
    print("✓ PASS: Cannot cast spell without enough mana")
else:
    print("✗ FAIL: Should not be able to cast without mana")

print()
print("=" * 60)
print("TEST 2: Mana Tracking (Recharge doesn't reduce mana_spent)")
print("=" * 60)

recharge = SPELLS[4]
state2 = State(
    player_hp=50,
    player_mana=500,
    boss_hp=50,
    shield_timer=0,
    poison_timer=0,
    recharge_timer=0,
    mana_spent=100,
    turn='player'
)

print(f"Initial mana_spent: {state2.mana_spent}")
result2 = execute_player_turn(state2, recharge)
print(f"After casting Recharge: mana_spent={result2.mana_spent}")
expected_spent = 100 + 229
if result2.mana_spent == expected_spent:
    print(f"✓ PASS: mana_spent correctly increased by {229} (Recharge cost)")
else:
    print(f"✗ FAIL: Expected mana_spent={expected_spent}, got {result2.mana_spent}")

print()
print("=" * 60)
print("TEST 3: Performance Check")
print("=" * 60)

from solution import find_minimum_mana

print("Running algorithm with actual input (Boss HP=71, Damage=10)...")
start_time = time.time()
result = find_minimum_mana(71, 10)
end_time = time.time()
runtime = end_time - start_time

print(f"Result: {result} mana")
print(f"Runtime: {runtime:.3f} seconds")

if runtime < 5:
    print(f"✓ PASS: Completed in {runtime:.3f}s (< 5s requirement)")
else:
    print(f"✗ FAIL: Runtime {runtime:.3f}s exceeds 5s limit")

print()
print("=" * 60)
print("TEST 4: Player Death from Combined Damage")
print("=" * 60)

# Player with low HP should die from boss attack
from solution import execute_boss_turn

state3 = State(
    player_hp=5,
    player_mana=500,
    boss_hp=50,
    shield_timer=0,
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='boss'
)

print(f"Player HP: {state3.player_hp}, Boss Damage: 10")
result3 = execute_boss_turn(state3, 10)
if result3 is None:
    print("✓ PASS: Player dies from boss attack (5 HP - 10 damage)")
else:
    print("✗ FAIL: Player should die")

print()
print("=" * 60)
print("TEST 5: Victory Detection at Correct Time")
print("=" * 60)

# Boss at low HP should die from spell
state4 = State(
    player_hp=50,
    player_mana=500,
    boss_hp=4,  # Will die from Magic Missile (4 damage)
    shield_timer=0,
    poison_timer=0,
    recharge_timer=0,
    mana_spent=0,
    turn='player'
)

print(f"Boss HP: {state4.boss_hp}, Magic Missile damage: 4")
result4 = execute_player_turn(state4, magic_missile)
if result4 and result4.boss_hp <= 0:
    print("✓ PASS: Boss dies from Magic Missile (4 HP - 4 damage)")
else:
    print("✗ FAIL: Boss should die")

print()
print("=" * 60)
print("All edge case tests completed!")
print("=" * 60)
