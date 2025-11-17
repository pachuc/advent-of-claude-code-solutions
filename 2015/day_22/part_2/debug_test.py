#!/usr/bin/env python3
"""Debug test to understand why Poison doesn't work for HP:18, Damage:3 scenario."""

# Simulate the scenario manually
def simulate_poison_strategy():
    """Manually simulate using Poison spell on Boss HP:18, Damage:3"""
    print("Simulating: Boss HP=18, Boss Damage=3, Player HP=50")
    print("Strategy: Cast Poison only (173 mana)")
    print()

    player_hp = 50
    boss_hp = 18
    boss_damage = 3
    poison_timer = 0
    turn = 1

    # Turn 1 - Player turn
    print(f"Turn 1 (Player):")
    print(f"  Before: Player HP={player_hp}, Boss HP={boss_hp}")
    player_hp -= 1  # Hard mode penalty
    print(f"  After hard mode penalty: Player HP={player_hp}")

    if poison_timer > 0:
        boss_hp -= 3
        poison_timer -= 1
        print(f"  After effects: Boss HP={boss_hp}, Poison timer={poison_timer}")

    # Cast Poison
    poison_timer = 6
    print(f"  Cast Poison: Poison timer={poison_timer}")
    print(f"  End of turn: Player HP={player_hp}, Boss HP={boss_hp}")
    print()

    # Subsequent turns
    turn_num = 2
    while boss_hp > 0 and player_hp > 0:
        # Boss turn
        print(f"Turn {turn_num} (Boss):")
        print(f"  Before: Player HP={player_hp}, Boss HP={boss_hp}, Poison timer={poison_timer}")

        if poison_timer > 0:
            boss_hp -= 3
            poison_timer -= 1
            print(f"  After effects: Boss HP={boss_hp}, Poison timer={poison_timer}")

        if boss_hp <= 0:
            print(f"  Boss dies from poison!")
            break

        # Boss attacks
        player_hp -= boss_damage
        print(f"  Boss attacks: Player HP={player_hp}")
        print()

        if player_hp <= 0:
            print(f"  Player dies!")
            break

        turn_num += 1

        # Player turn
        print(f"Turn {turn_num} (Player):")
        print(f"  Before: Player HP={player_hp}, Boss HP={boss_hp}, Poison timer={poison_timer}")
        player_hp -= 1  # Hard mode penalty
        print(f"  After hard mode penalty: Player HP={player_hp}")

        if player_hp <= 0:
            print(f"  Player dies from hard mode penalty!")
            break

        if poison_timer > 0:
            boss_hp -= 3
            poison_timer -= 1
            print(f"  After effects: Boss HP={boss_hp}, Poison timer={poison_timer}")

        if boss_hp <= 0:
            print(f"  Boss dies from poison!")
            break

        # Would need to cast another spell here, but we only have Poison strategy
        print(f"  Would need to cast a spell here...")
        print(f"  Without additional spells, checking if boss is dead: boss_hp={boss_hp}")

        # For this test, just wait (in real game, must cast a spell)
        print()
        turn_num += 1

    print()
    if boss_hp <= 0:
        print(f"VICTORY! Player survived with {player_hp} HP")
    else:
        print(f"DEFEAT! Boss survived with {boss_hp} HP")

if __name__ == '__main__':
    simulate_poison_strategy()
