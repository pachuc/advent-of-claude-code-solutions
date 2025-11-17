from itertools import combinations

# Define shop inventory
weapons = [
    ("Dagger", 8, 4, 0),
    ("Shortsword", 10, 5, 0),
    ("Warhammer", 25, 6, 0),
    ("Longsword", 40, 7, 0),
    ("Greataxe", 74, 8, 0)
]

armor = [
    ("Leather", 13, 0, 1),
    ("Chainmail", 31, 0, 2),
    ("Splintmail", 53, 0, 3),
    ("Bandedmail", 75, 0, 4),
    ("Platemail", 102, 0, 5)
]

rings = [
    ("Damage +1", 25, 1, 0),
    ("Damage +2", 50, 2, 0),
    ("Damage +3", 100, 3, 0),
    ("Defense +1", 20, 0, 1),
    ("Defense +2", 40, 0, 2),
    ("Defense +3", 80, 0, 3)
]


def simulate_combat(player_hp, player_damage, player_armor, boss_hp, boss_damage, boss_armor):
    """
    Simulates turn-based combat. Returns True if player wins, False if player loses.

    Uses mathematical optimization: calculates how many turns each side needs to win
    instead of simulating turn-by-turn.
    """
    # Calculate damage per turn (minimum 1)
    player_damage_per_turn = max(1, player_damage - boss_armor)
    boss_damage_per_turn = max(1, boss_damage - player_armor)

    # Calculate turns needed to defeat each other (ceiling division)
    turns_to_kill_boss = (boss_hp + player_damage_per_turn - 1) // player_damage_per_turn
    turns_to_kill_player = (player_hp + boss_damage_per_turn - 1) // boss_damage_per_turn

    # Player attacks first, so player wins if they need same or fewer turns
    return turns_to_kill_boss <= turns_to_kill_player


def generate_equipment_combinations():
    """
    Generates all valid equipment combinations.
    Returns list of tuples: (total_cost, total_damage, total_armor)
    """
    all_combinations = []

    # Pre-generate all ring combinations
    ring_combinations = [()]  # No rings
    for ring in rings:
        ring_combinations.append((ring,))  # Single rings
    for ring_pair in combinations(rings, 2):
        ring_combinations.append(ring_pair)  # Pairs of rings

    # Iterate through all weapons (required - exactly 1)
    for weapon_name, weapon_cost, weapon_damage, weapon_armor in weapons:

        # Iterate through armor options (optional - 0 or 1)
        armor_options = [None] + armor  # None represents no armor
        for armor_item in armor_options:
            if armor_item is None:
                armor_cost, armor_damage, armor_armor = 0, 0, 0
            else:
                armor_name, armor_cost, armor_damage, armor_armor = armor_item

            # Iterate through ring options (0, 1, or 2 rings)
            for ring_combo in ring_combinations:
                ring_cost = sum(r[1] for r in ring_combo)
                ring_damage = sum(r[2] for r in ring_combo)
                ring_armor = sum(r[3] for r in ring_combo)

                total_cost = weapon_cost + armor_cost + ring_cost
                total_damage = weapon_damage + armor_damage + ring_damage
                total_armor = weapon_armor + armor_armor + ring_armor

                all_combinations.append((total_cost, total_damage, total_armor))

    return all_combinations


def parse_boss_stats(filename):
    """
    Parses boss statistics from input file.
    Expected format:
        Hit Points: 103
        Damage: 9
        Armor: 2
    """
    boss_stats = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)  # Split only on first colon
                key = key.strip()
                value = int(value.strip())

                if 'Hit Points' in key:
                    boss_stats['hp'] = value
                elif 'Damage' in key:
                    boss_stats['damage'] = value
                elif 'Armor' in key:
                    boss_stats['armor'] = value

    # Validate all required fields are present
    required_fields = ['hp', 'damage', 'armor']
    if not all(field in boss_stats for field in required_fields):
        raise ValueError(f"Invalid input format: missing required boss statistics. Found: {list(boss_stats.keys())}")

    return boss_stats['hp'], boss_stats['damage'], boss_stats['armor']


def find_max_gold_to_lose():
    """
    Finds the maximum amount of gold you can spend while still losing.

    Algorithm:
    1. Parse boss stats from input
    2. Generate all equipment combinations
    3. For each combination, simulate combat
    4. Track maximum cost among combinations where player loses
    5. Return maximum cost
    """
    # Parse input
    boss_hp, boss_damage, boss_armor = parse_boss_stats('input.md')

    # Player constants
    player_hp = 100

    # Generate all combinations
    combinations = generate_equipment_combinations()

    # Track maximum cost for losing
    max_cost_to_lose = 0

    # Test each combination
    for cost, player_damage, player_armor in combinations:
        player_wins = simulate_combat(
            player_hp, player_damage, player_armor,
            boss_hp, boss_damage, boss_armor
        )

        # We want to lose, so player_wins should be False
        if not player_wins:
            max_cost_to_lose = max(max_cost_to_lose, cost)

    return max_cost_to_lose


if __name__ == "__main__":
    result = find_max_gold_to_lose()
    print(result)
