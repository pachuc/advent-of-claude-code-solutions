# Implementation Plan: RPG Simulator 20XX - Maximum Gold to Lose

## Problem Analysis

We need to find the maximum gold we can spend while still **losing** to the boss. This is the inverse of part 1 where we wanted to minimize gold and win.

### Key Constraints
- Must buy exactly 1 weapon (5 options)
- Can buy 0 or 1 armor (6 options: none or one of 5 armors)
- Can buy 0, 1, or 2 rings (21 options: none, any single ring, or any pair of rings)
- Total combinations: 5 × 6 × 21 = 630 combinations

### Boss Stats
- HP: 103, Damage: 9, Armor: 2

### Player Stats
- HP: 100 (fixed)
- Damage: sum of equipment damage
- Armor: sum of equipment armor

## Algorithm Strategy

### Approach: Exhaustive Search with Combat Simulation
**Time Complexity**: O(n) where n = 630 combinations
**Space Complexity**: O(1) - only tracking max cost

This is optimal because:
1. The search space is small (630 combinations)
2. Each combat simulation is O(k) where k = max turns ≈ 100
3. Total runtime: O(630 × 100) ≈ 63,000 operations - very fast
4. No need for optimization or dynamic programming

## Step-by-Step Implementation

### Step 1: Define Data Structures
```python
# Define shop inventory as lists of tuples: (name, cost, damage, armor)
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
```

### Step 2: Implement Combat Simulator
```python
def simulate_combat(player_hp, player_damage, player_armor, boss_hp, boss_damage, boss_armor):
    """
    Simulates turn-based combat. Returns True if player wins, False if player loses.

    Algorithm:
    1. Player always attacks first
    2. Calculate damage per turn for both sides: max(1, attacker_damage - defender_armor)
    3. Alternate attacks until one reaches 0 or fewer HP
    4. Return True if boss dies first, False if player dies first
    """
    # Calculate damage per turn
    player_damage_per_turn = max(1, player_damage - boss_armor)
    boss_damage_per_turn = max(1, boss_damage - player_armor)

    # Calculate turns needed to defeat each other
    turns_to_kill_boss = (boss_hp + player_damage_per_turn - 1) // player_damage_per_turn
    turns_to_kill_player = (player_hp + boss_damage_per_turn - 1) // boss_damage_per_turn

    # Player attacks first, so player wins if they need same or fewer turns
    return turns_to_kill_boss <= turns_to_kill_player
```

**Optimization Note**: Instead of simulating turn-by-turn, we calculate how many turns each side needs to win. Since player attacks first, player wins if `turns_to_kill_boss <= turns_to_kill_player`.

### Step 3: Generate Equipment Combinations
```python
from itertools import combinations

def generate_equipment_combinations():
    """
    Generates all valid equipment combinations.
    Returns list of tuples: (total_cost, total_damage, total_armor)
    """
    all_combinations = []

    # Pre-generate all ring combinations (optimization: done once instead of 30 times)
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
```

### Step 4: Parse Boss Stats from Input
```python
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
```

### Step 5: Main Solution Logic
```python
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
```

### Step 6: Main Entry Point
```python
if __name__ == "__main__":
    result = find_max_gold_to_lose()
    print(result)
```

## Implementation Order

1. **First**: Define shop inventory data structures
2. **Second**: Implement combat simulator with mathematical optimization
3. **Third**: Implement equipment combination generator
4. **Fourth**: Implement input parser for boss stats
5. **Fifth**: Implement main solution logic
6. **Sixth**: Add main entry point and test

## Efficiency Considerations

### Why This Approach is Optimal
1. **Small search space**: Only 630 combinations
2. **Mathematical combat**: O(1) combat simulation instead of O(k) turn-by-turn
3. **No backtracking needed**: Simple exhaustive search is fastest
4. **No memoization needed**: Each combination tested once

### Runtime Analysis
- Combinations: 5 weapons × 6 armor options × 21 ring options = 630
- Per combination: O(1) cost calculation + O(1) combat simulation
- Total: O(630) ≈ instant execution

### Memory Usage
- Shop inventory: ~30 items stored
- Combinations list: 630 tuples × 3 integers ≈ negligible
- No additional data structures needed
- Space complexity: O(1) effective

## Edge Cases Handled

1. **Minimum damage rule**: `max(1, damage - armor)` ensures always at least 1 damage
2. **No armor purchased**: Handled by including `None` in armor options
3. **No rings purchased**: Handled by including empty tuple in ring combinations
4. **Player attacks first**: Handled in combat simulator comparison
5. **Integer division for turns**: Using ceiling division `(hp + dmg - 1) // dmg`
6. **Duplicate rings prevented**: Using `combinations(rings, 2)` ensures no ring appears twice
7. **Input validation**: Parser validates all required boss stats are present

## Output Format

The solution should output a single integer representing the maximum gold spent while losing.
