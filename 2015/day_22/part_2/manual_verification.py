#!/usr/bin/env python3
"""Manually verify the spell sequence to ensure correctness."""

def simulate_battle():
    """Manually simulate the optimal battle sequence."""
    # Spell sequence
    spells = [
        'Shield', 'Recharge', 'Poison', 'Shield', 'Recharge',
        'Poison', 'Shield', 'Recharge', 'Poison', 'Shield',
        'Magic Missile', 'Poison', 'Magic Missile'
    ]

    player_hp = 50
    player_mana = 500
    boss_hp = 71
    boss_damage = 10
    shield_timer = 0
    poison_timer = 0
    recharge_timer = 0
    mana_spent = 0
    spell_idx = 0

    print(f"Initial: Player HP={player_hp}, Mana={player_mana}, Boss HP={boss_hp}")
    print()

    turn = 1
    while boss_hp > 0 and player_hp > 0 and spell_idx < len(spells):
        # Player turn
        print(f"--- Turn {turn} (Player) ---")

        # Hard mode penalty
        player_hp -= 1
        print(f"Hard mode: Player HP -> {player_hp}")
        if player_hp <= 0:
            print("Player dies from hard mode penalty!")
            break

        # Apply effects
        if poison_timer > 0:
            boss_hp -= 3
            poison_timer -= 1
            print(f"Poison deals 3 damage. Boss HP -> {boss_hp}, Poison timer -> {poison_timer}")

        if recharge_timer > 0:
            player_mana += 101
            recharge_timer -= 1
            print(f"Recharge gives 101 mana. Player Mana -> {player_mana}, Recharge timer -> {recharge_timer}")

        if shield_timer > 0:
            shield_timer -= 1
            print(f"Shield timer -> {shield_timer}")

        if boss_hp <= 0:
            print(f"Boss dies from effects!")
            break

        # Cast spell
        spell = spells[spell_idx]
        spell_idx += 1

        if spell == 'Magic Missile':
            cost = 53
            player_mana -= cost
            mana_spent += cost
            boss_hp -= 4
            print(f"Cast {spell} (cost {cost}). Boss HP -> {boss_hp}, Player Mana -> {player_mana}")

        elif spell == 'Drain':
            cost = 73
            player_mana -= cost
            mana_spent += cost
            boss_hp -= 2
            player_hp += 2
            print(f"Cast {spell} (cost {cost}). Boss HP -> {boss_hp}, Player HP -> {player_hp}, Player Mana -> {player_mana}")

        elif spell == 'Shield':
            cost = 113
            player_mana -= cost
            mana_spent += cost
            shield_timer = 6
            print(f"Cast {spell} (cost {cost}). Shield timer -> {shield_timer}, Player Mana -> {player_mana}")

        elif spell == 'Poison':
            cost = 173
            player_mana -= cost
            mana_spent += cost
            poison_timer = 6
            print(f"Cast {spell} (cost {cost}). Poison timer -> {poison_timer}, Player Mana -> {player_mana}")

        elif spell == 'Recharge':
            cost = 229
            player_mana -= cost
            mana_spent += cost
            recharge_timer = 5
            print(f"Cast {spell} (cost {cost}). Recharge timer -> {recharge_timer}, Player Mana -> {player_mana}")

        if boss_hp <= 0:
            print(f"Boss dies!")
            break

        print(f"End of player turn: Player HP={player_hp}, Mana={player_mana}, Boss HP={boss_hp}")
        print()

        # Boss turn
        print(f"--- Turn {turn} (Boss) ---")

        # Apply effects
        if poison_timer > 0:
            boss_hp -= 3
            poison_timer -= 1
            print(f"Poison deals 3 damage. Boss HP -> {boss_hp}, Poison timer -> {poison_timer}")

        if recharge_timer > 0:
            player_mana += 101
            recharge_timer -= 1
            print(f"Recharge gives 101 mana. Player Mana -> {player_mana}, Recharge timer -> {recharge_timer}")

        if shield_timer > 0:
            shield_timer -= 1
            print(f"Shield timer -> {shield_timer}")

        if boss_hp <= 0:
            print(f"Boss dies from effects!")
            break

        # Boss attacks
        if shield_timer > 0:
            damage = max(1, boss_damage - 7)
            armor_text = " (with 7 armor)"
        else:
            damage = boss_damage
            armor_text = ""

        player_hp -= damage
        print(f"Boss attacks for {damage} damage{armor_text}. Player HP -> {player_hp}")

        if player_hp <= 0:
            print("Player dies!")
            break

        print(f"End of boss turn: Player HP={player_hp}, Mana={player_mana}, Boss HP={boss_hp}")
        print()

        turn += 1

    print()
    print("=" * 70)
    if boss_hp <= 0:
        print(f"VICTORY! Player wins with {player_hp} HP remaining")
        print(f"Total mana spent: {mana_spent}")
    else:
        print(f"DEFEAT! Player loses")
    print("=" * 70)

if __name__ == '__main__':
    simulate_battle()
