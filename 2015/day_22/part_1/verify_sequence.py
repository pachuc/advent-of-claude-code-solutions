#!/usr/bin/env python3
"""Verify that the winning sequence from the implementation summary is correct."""

# From the implementation summary, the winning sequence is:
# 1. Poison (173) = 173
# 2. Recharge (229) = 402
# 3. Shield (113) = 515
# 4. Poison (173) = 688
# 5. Recharge (229) = 917
# 6. Shield (113) = 1030
# 7. Poison (173) = 1203
# 8. Recharge (229) = 1432
# 9. Shield (113) = 1545
# 10. Magic Missile (53) = 1598
# 11. Poison (173) = 1771
# 12. Magic Missile (53) = 1824

# Let's simulate this manually
def simulate_combat(spell_sequence, boss_hp, boss_damage):
    """Simulate combat with a given spell sequence."""
    player_hp = 50
    player_mana = 500
    shield_timer = 0
    poison_timer = 0
    recharge_timer = 0
    mana_spent = 0

    spell_costs = {
        'Poison': 173,
        'Recharge': 229,
        'Shield': 113,
        'Magic Missile': 53,
        'Drain': 73
    }

    turn = 0
    for spell in spell_sequence:
        turn += 1
        print(f"\n=== Turn {turn} - Player ===")

        # Apply effects at start of player turn
        if shield_timer > 0:
            print(f"Shield active (armor = 7), timer: {shield_timer}")
        if poison_timer > 0:
            boss_hp -= 3
            print(f"Poison deals 3 damage, boss HP: {boss_hp}, timer: {poison_timer}")
        if recharge_timer > 0:
            player_mana += 101
            print(f"Recharge gives 101 mana, mana: {player_mana}, timer: {recharge_timer}")

        # Decrement timers
        if shield_timer > 0:
            shield_timer -= 1
        if poison_timer > 0:
            poison_timer -= 1
        if recharge_timer > 0:
            recharge_timer -= 1

        # Check if boss died from effects
        if boss_hp <= 0:
            print(f"Boss died from effects! Player wins with {mana_spent} mana spent")
            return True

        # Player casts spell
        cost = spell_costs[spell]
        if player_mana < cost:
            print(f"ERROR: Not enough mana to cast {spell}! Have {player_mana}, need {cost}")
            return False

        player_mana -= cost
        mana_spent += cost
        print(f"Player casts {spell} (cost {cost}), mana: {player_mana}, total spent: {mana_spent}")

        # Apply spell effects
        if spell == 'Magic Missile':
            boss_hp -= 4
            print(f"Magic Missile deals 4 damage, boss HP: {boss_hp}")
        elif spell == 'Drain':
            boss_hp -= 2
            player_hp += 2
            print(f"Drain deals 2 damage and heals 2, boss HP: {boss_hp}, player HP: {player_hp}")
        elif spell == 'Shield':
            shield_timer = 6
            print(f"Shield effect started, timer: {shield_timer}")
        elif spell == 'Poison':
            poison_timer = 6
            print(f"Poison effect started, timer: {poison_timer}")
        elif spell == 'Recharge':
            recharge_timer = 5
            print(f"Recharge effect started, timer: {recharge_timer}")

        # Check if boss died from instant damage
        if boss_hp <= 0:
            print(f"Boss died! Player wins with {mana_spent} mana spent")
            return True

        # Boss turn
        print(f"\n=== Turn {turn} - Boss ===")

        # Apply effects at start of boss turn
        if shield_timer > 0:
            print(f"Shield active (armor = 7), timer: {shield_timer}")
        if poison_timer > 0:
            boss_hp -= 3
            print(f"Poison deals 3 damage, boss HP: {boss_hp}, timer: {poison_timer}")
        if recharge_timer > 0:
            player_mana += 101
            print(f"Recharge gives 101 mana, mana: {player_mana}, timer: {recharge_timer}")

        # Decrement timers
        if shield_timer > 0:
            shield_timer -= 1
        if poison_timer > 0:
            poison_timer -= 1
        if recharge_timer > 0:
            recharge_timer -= 1

        # Check if boss died from effects
        if boss_hp <= 0:
            print(f"Boss died from effects! Player wins with {mana_spent} mana spent")
            return True

        # Boss attacks
        armor = 7 if shield_timer > 0 else 0
        damage = max(1, boss_damage - armor)
        player_hp -= damage
        print(f"Boss attacks for {damage} damage (armor: {armor}), player HP: {player_hp}")

        # Check if player died
        if player_hp <= 0:
            print(f"Player died! Lost with {mana_spent} mana spent")
            return False

    print(f"\nFinal state: Player HP: {player_hp}, Boss HP: {boss_hp}, Mana spent: {mana_spent}")
    return boss_hp <= 0

# Test with the winning sequence from implementation summary
winning_sequence = [
    'Poison',
    'Recharge',
    'Shield',
    'Poison',
    'Recharge',
    'Shield',
    'Poison',
    'Recharge',
    'Shield',
    'Magic Missile',
    'Poison',
    'Magic Missile'
]

print("Testing winning sequence from implementation summary:")
print("="*60)
result = simulate_combat(winning_sequence, 71, 10)
print(f"\nResult: {'SUCCESS' if result else 'FAILURE'}")
