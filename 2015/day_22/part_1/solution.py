import heapq
import re

# Spell definitions
SPELLS = {
    'Magic Missile': {'cost': 53, 'damage': 4, 'heal': 0, 'effect': None, 'duration': 0},
    'Drain': {'cost': 73, 'damage': 2, 'heal': 2, 'effect': None, 'duration': 0},
    'Shield': {'cost': 113, 'damage': 0, 'heal': 0, 'effect': 'shield', 'duration': 6},
    'Poison': {'cost': 173, 'damage': 0, 'heal': 0, 'effect': 'poison', 'duration': 6},
    'Recharge': {'cost': 229, 'damage': 0, 'heal': 0, 'effect': 'recharge', 'duration': 5},
}

def parse_input(filename):
    """Parse boss stats from input file."""
    with open(filename, 'r') as f:
        content = f.read()

    hp_match = re.search(r'Hit Points:\s*(\d+)', content)
    damage_match = re.search(r'Damage:\s*(\d+)', content)

    boss_hp = int(hp_match.group(1))
    boss_damage = int(damage_match.group(1))

    return boss_hp, boss_damage

def apply_effects(state):
    """
    Apply effects at the start of a turn.
    Effects apply if timer > 0, then timers decrement.
    Returns updated state and whether boss died from effects.
    """
    new_state = state.copy()
    boss_died = False

    # Apply Shield effect (armor = 7 when shield_timer > 0)
    # Armor is handled in boss_attack, just need to track timer

    # Apply Poison effect
    if new_state['poison_timer'] > 0:
        new_state['boss_hp'] -= 3
        if new_state['boss_hp'] <= 0:
            boss_died = True

    # Apply Recharge effect
    if new_state['recharge_timer'] > 0:
        new_state['player_mana'] += 101

    # Decrement all timers
    if new_state['shield_timer'] > 0:
        new_state['shield_timer'] -= 1
    if new_state['poison_timer'] > 0:
        new_state['poison_timer'] -= 1
    if new_state['recharge_timer'] > 0:
        new_state['recharge_timer'] -= 1

    return new_state, boss_died

def cast_spell(state, spell_name):
    """
    Attempt to cast a spell.
    Returns new state if successful, None if invalid.
    """
    spell = SPELLS[spell_name]

    # Check if player has enough mana
    if state['player_mana'] < spell['cost']:
        return None

    # Check if effect is already active (timer > 0)
    if spell['effect'] == 'shield' and state['shield_timer'] > 0:
        return None
    if spell['effect'] == 'poison' and state['poison_timer'] > 0:
        return None
    if spell['effect'] == 'recharge' and state['recharge_timer'] > 0:
        return None

    # Create new state
    new_state = state.copy()

    # Deduct mana cost
    new_state['player_mana'] -= spell['cost']
    new_state['mana_spent'] += spell['cost']

    # Apply instant effects
    new_state['boss_hp'] -= spell['damage']
    new_state['player_hp'] += spell['heal']

    # Start effect timer if applicable
    if spell['effect'] == 'shield':
        new_state['shield_timer'] = spell['duration']
    elif spell['effect'] == 'poison':
        new_state['poison_timer'] = spell['duration']
    elif spell['effect'] == 'recharge':
        new_state['recharge_timer'] = spell['duration']

    return new_state

def boss_attack(state, boss_damage):
    """
    Boss attacks the player.
    Returns new state with reduced player HP.
    """
    new_state = state.copy()

    # Determine armor (7 if shield active, 0 otherwise)
    armor = 7 if new_state['shield_timer'] > 0 else 0

    # Calculate damage (minimum 1)
    damage = max(1, boss_damage - armor)

    # Apply damage
    new_state['player_hp'] -= damage

    return new_state

def state_key(state):
    """
    Generate a hashable key for a state.
    Excludes mana_spent for proper state comparison.
    """
    return (
        state['player_hp'],
        state['player_mana'],
        state['boss_hp'],
        state['shield_timer'],
        state['poison_timer'],
        state['recharge_timer']
    )

def find_min_mana(boss_hp, boss_damage):
    """
    Use Dijkstra's algorithm to find minimum mana to defeat the boss.
    """
    # Initial state
    initial_state = {
        'player_hp': 50,
        'player_mana': 500,
        'boss_hp': boss_hp,
        'shield_timer': 0,
        'poison_timer': 0,
        'recharge_timer': 0,
        'mana_spent': 0
    }

    # Priority queue: (mana_spent, counter, state)
    # Counter is used to break ties when mana_spent is equal
    counter = 0
    pq = [(0, counter, initial_state)]

    # Visited dictionary: state_key -> minimum mana_spent
    visited = {}

    while pq:
        mana_spent, _, state = heapq.heappop(pq)

        # Generate state key
        key = state_key(state)

        # Skip if we've seen this state with lower or equal cost
        if key in visited and visited[key] <= mana_spent:
            continue

        # Mark state as visited
        visited[key] = mana_spent

        # === PLAYER TURN ===
        # Apply effects at start of player turn
        state, boss_died = apply_effects(state)

        # Check if boss died from effects
        if boss_died or state['boss_hp'] <= 0:
            return state['mana_spent']

        # Check if player died from effects (shouldn't happen, but just in case)
        if state['player_hp'] <= 0:
            continue

        # Try each spell
        for spell_name in SPELLS:
            # Try to cast spell
            new_state = cast_spell(state, spell_name)

            # Skip if spell cast failed
            if new_state is None:
                continue

            # Check if boss died from instant spell damage
            if new_state['boss_hp'] <= 0:
                counter += 1
                heapq.heappush(pq, (new_state['mana_spent'], counter, new_state))
                continue

            # === BOSS TURN ===
            # Apply effects at start of boss turn
            boss_turn_state, boss_died = apply_effects(new_state)

            # Check if boss died from effects
            if boss_died or boss_turn_state['boss_hp'] <= 0:
                counter += 1
                heapq.heappush(pq, (boss_turn_state['mana_spent'], counter, boss_turn_state))
                continue

            # Check if player died from effects (shouldn't happen)
            if boss_turn_state['player_hp'] <= 0:
                continue

            # Boss attacks
            final_state = boss_attack(boss_turn_state, boss_damage)

            # Only add to queue if player survived
            if final_state['player_hp'] > 0:
                counter += 1
                heapq.heappush(pq, (final_state['mana_spent'], counter, final_state))

    # No solution found
    return -1

def main():
    # Parse input
    boss_hp, boss_damage = parse_input('input.md')

    # Find minimum mana
    result = find_min_mana(boss_hp, boss_damage)

    # Print result
    print(result)

if __name__ == '__main__':
    main()
