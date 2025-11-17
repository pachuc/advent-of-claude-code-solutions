from math import ceil
from itertools import combinations

# Constants
PLAYER_HP = 100

# Shop inventory
weapons = [
    {'name': 'Dagger', 'cost': 8, 'damage': 4, 'armor': 0},
    {'name': 'Shortsword', 'cost': 10, 'damage': 5, 'armor': 0},
    {'name': 'Warhammer', 'cost': 25, 'damage': 6, 'armor': 0},
    {'name': 'Longsword', 'cost': 40, 'damage': 7, 'armor': 0},
    {'name': 'Greataxe', 'cost': 74, 'damage': 8, 'armor': 0}
]

armor_items = [
    {'name': 'Leather', 'cost': 13, 'damage': 0, 'armor': 1},
    {'name': 'Chainmail', 'cost': 31, 'damage': 0, 'armor': 2},
    {'name': 'Splintmail', 'cost': 53, 'damage': 0, 'armor': 3},
    {'name': 'Bandedmail', 'cost': 75, 'damage': 0, 'armor': 4},
    {'name': 'Platemail', 'cost': 102, 'damage': 0, 'armor': 5}
]

rings = [
    {'name': 'Damage +1', 'cost': 25, 'damage': 1, 'armor': 0},
    {'name': 'Damage +2', 'cost': 50, 'damage': 2, 'armor': 0},
    {'name': 'Damage +3', 'cost': 100, 'damage': 3, 'armor': 0},
    {'name': 'Defense +1', 'cost': 20, 'damage': 0, 'armor': 1},
    {'name': 'Defense +2', 'cost': 40, 'damage': 0, 'armor': 2},
    {'name': 'Defense +3', 'cost': 80, 'damage': 0, 'armor': 3}
]


def parse_input(filename):
    """Parse boss stats from input file."""
    boss_stats = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':')
                key = key.strip().lower().replace(' ', '_')
                boss_stats[key] = int(value.strip())
    return boss_stats


def generate_ring_combinations(rings):
    """Generate all valid ring combinations (0, 1, or 2 rings)."""
    # 0 rings
    yield []

    # 1 ring
    for ring in rings:
        yield [ring]

    # 2 rings
    for ring_pair in combinations(rings, 2):
        yield list(ring_pair)


def generate_loadouts(weapons, armor_items, rings):
    """Generate all valid equipment loadouts."""
    loadouts = []

    for weapon in weapons:
        for ring_combo in generate_ring_combinations(rings):
            # Loadout with no armor
            loadout = [weapon] + ring_combo
            loadouts.append(loadout)

            # Loadouts with each armor piece
            for armor in armor_items:
                loadout = [weapon, armor] + ring_combo
                loadouts.append(loadout)

    return loadouts


def calculate_stats(loadout):
    """Calculate total cost, damage, and armor from a loadout."""
    total_cost = sum(item['cost'] for item in loadout)
    total_damage = sum(item['damage'] for item in loadout)
    total_armor = sum(item['armor'] for item in loadout)
    return total_cost, total_damage, total_armor


def player_wins(player_hp, player_damage, player_armor,
                boss_hp, boss_damage, boss_armor):
    """Simulate combat and determine if player wins."""
    # Calculate damage per hit for each combatant (minimum 1)
    player_damage_per_hit = max(1, player_damage - boss_armor)
    boss_damage_per_hit = max(1, boss_damage - player_armor)

    # Calculate turns to kill
    turns_to_kill_boss = ceil(boss_hp / player_damage_per_hit)
    turns_to_kill_player = ceil(player_hp / boss_damage_per_hit)

    # Player attacks first, so wins if turns are equal
    return turns_to_kill_boss <= turns_to_kill_player


def find_minimum_cost(boss_stats, weapons, armor_items, rings):
    """Find the minimum cost equipment loadout that allows player to win."""
    min_cost = float('inf')
    winning_loadout = None

    for loadout in generate_loadouts(weapons, armor_items, rings):
        cost, damage, armor = calculate_stats(loadout)

        if player_wins(PLAYER_HP, damage, armor,
                      boss_stats['hit_points'], boss_stats['damage'], boss_stats['armor']):
            if cost < min_cost:
                min_cost = cost
                winning_loadout = loadout

    return min_cost, winning_loadout


def main():
    # Parse input
    boss_stats = parse_input('input.md')

    # Find minimum cost
    min_cost, winning_loadout = find_minimum_cost(boss_stats, weapons, armor_items, rings)

    # Output result
    print(min_cost)


if __name__ == '__main__':
    main()
