"""Verify the solution by adding some debug output to understand the winning strategy."""
from solution import find_min_mana, apply_effects, cast_spell, boss_attack, state_key, SPELLS
import heapq

def find_min_mana_debug(boss_hp, boss_damage):
    """
    Use Dijkstra's algorithm to find minimum mana to defeat the boss.
    This version tracks the path to winning.
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

    # Priority queue: (mana_spent, counter, state, path)
    counter = 0
    pq = [(0, counter, initial_state, [])]

    # Visited dictionary: state_key -> minimum mana_spent
    visited = {}

    while pq:
        mana_spent, _, state, path = heapq.heappop(pq)

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
            print(f"\n=== WINNING STRATEGY ===")
            print(f"Total mana spent: {state['mana_spent']}")
            print(f"Spell sequence ({len(path)} spells):")
            for i, spell_name in enumerate(path, 1):
                spell = SPELLS[spell_name]
                print(f"  {i}. {spell_name} (cost: {spell['cost']})")
            return state['mana_spent']

        # Check if player died from effects
        if state['player_hp'] <= 0:
            continue

        # Try each spell
        for spell_name in SPELLS:
            # Try to cast spell
            new_state = cast_spell(state, spell_name)

            # Skip if spell cast failed
            if new_state is None:
                continue

            new_path = path + [spell_name]

            # Check if boss died from instant spell damage
            if new_state['boss_hp'] <= 0:
                counter += 1
                heapq.heappush(pq, (new_state['mana_spent'], counter, new_state, new_path))
                continue

            # === BOSS TURN ===
            # Apply effects at start of boss turn
            boss_turn_state, boss_died = apply_effects(new_state)

            # Check if boss died from effects
            if boss_died or boss_turn_state['boss_hp'] <= 0:
                counter += 1
                heapq.heappush(pq, (boss_turn_state['mana_spent'], counter, boss_turn_state, new_path))
                continue

            # Check if player died from effects
            if boss_turn_state['player_hp'] <= 0:
                continue

            # Boss attacks
            final_state = boss_attack(boss_turn_state, boss_damage)

            # Only add to queue if player survived
            if final_state['player_hp'] > 0:
                counter += 1
                heapq.heappush(pq, (final_state['mana_spent'], counter, final_state, new_path))

    # No solution found
    return -1

# Test with actual input
print("Finding optimal strategy for the puzzle...")
result = find_min_mana_debug(71, 10)
print(f"\nFinal answer: {result}")
