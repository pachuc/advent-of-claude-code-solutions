import heapq
from dataclasses import dataclass
from typing import Optional, Tuple

# Spell definitions
SPELLS = [
    {'name': 'Magic Missile', 'cost': 53, 'damage': 4, 'heal': 0, 'effect': None, 'duration': 0},
    {'name': 'Drain', 'cost': 73, 'damage': 2, 'heal': 2, 'effect': None, 'duration': 0},
    {'name': 'Shield', 'cost': 113, 'damage': 0, 'heal': 0, 'effect': 'shield', 'duration': 6},
    {'name': 'Poison', 'cost': 173, 'damage': 0, 'heal': 0, 'effect': 'poison', 'duration': 6},
    {'name': 'Recharge', 'cost': 229, 'damage': 0, 'heal': 0, 'effect': 'recharge', 'duration': 5}
]

@dataclass(frozen=True)
class State:
    player_hp: int
    player_mana: int
    boss_hp: int
    shield_timer: int
    poison_timer: int
    recharge_timer: int
    mana_spent: int
    turn: str  # 'player' or 'boss'

def parse_input(filename: str) -> Tuple[int, int]:
    """Parse input file to extract boss HP and damage."""
    with open(filename, 'r') as f:
        lines = f.readlines()

    boss_hp = int(lines[0].split(':')[1].strip())
    boss_damage = int(lines[1].split(':')[1].strip())

    return boss_hp, boss_damage

def apply_effects(state: State) -> Tuple[State, bool]:
    """
    Apply active effects at the start of a turn.
    Returns: (new_state, boss_died)
    """
    player_hp = state.player_hp
    player_mana = state.player_mana
    boss_hp = state.boss_hp
    shield_timer = state.shield_timer
    poison_timer = state.poison_timer
    recharge_timer = state.recharge_timer

    # Apply poison effect
    if poison_timer > 0:
        boss_hp -= 3
        poison_timer -= 1

    # Apply recharge effect
    if recharge_timer > 0:
        player_mana += 101
        recharge_timer -= 1

    # Shield timer (just decrement, armor is checked during boss attack)
    if shield_timer > 0:
        shield_timer -= 1

    # Check if boss died from effects
    boss_died = boss_hp <= 0

    new_state = State(
        player_hp=player_hp,
        player_mana=player_mana,
        boss_hp=boss_hp,
        shield_timer=shield_timer,
        poison_timer=poison_timer,
        recharge_timer=recharge_timer,
        mana_spent=state.mana_spent,
        turn=state.turn
    )

    return new_state, boss_died

def execute_player_turn(state: State, spell: dict) -> Optional[State]:
    """
    Execute a player turn with the given spell.
    Returns new state or None if the move is invalid/results in loss.
    """
    # Step 1: Hard mode penalty - player loses 1 HP FIRST
    player_hp = state.player_hp - 1

    # Step 2: Check if player died from hard mode penalty
    if player_hp <= 0:
        return None

    # Create temporary state with reduced HP for effect application
    temp_state = State(
        player_hp=player_hp,
        player_mana=state.player_mana,
        boss_hp=state.boss_hp,
        shield_timer=state.shield_timer,
        poison_timer=state.poison_timer,
        recharge_timer=state.recharge_timer,
        mana_spent=state.mana_spent,
        turn=state.turn
    )

    # Step 3: Apply effects
    temp_state, boss_died = apply_effects(temp_state)

    # Step 4: Check if boss died from effects
    if boss_died:
        return State(
            player_hp=temp_state.player_hp,
            player_mana=temp_state.player_mana,
            boss_hp=temp_state.boss_hp,
            shield_timer=temp_state.shield_timer,
            poison_timer=temp_state.poison_timer,
            recharge_timer=temp_state.recharge_timer,
            mana_spent=temp_state.mana_spent,
            turn='boss'
        )

    # Step 5: Validate spell can be cast
    if temp_state.player_mana < spell['cost']:
        return None  # Not enough mana

    # Check if effect spell is already active
    if spell['effect'] == 'shield' and temp_state.shield_timer > 0:
        return None
    if spell['effect'] == 'poison' and temp_state.poison_timer > 0:
        return None
    if spell['effect'] == 'recharge' and temp_state.recharge_timer > 0:
        return None

    # Step 6: Deduct mana cost
    player_mana = temp_state.player_mana - spell['cost']
    mana_spent = temp_state.mana_spent + spell['cost']

    # Step 7: Apply spell's instant effects
    boss_hp = temp_state.boss_hp - spell['damage']
    player_hp = temp_state.player_hp + spell['heal']

    # Step 8: Start new effect if spell has one
    shield_timer = temp_state.shield_timer
    poison_timer = temp_state.poison_timer
    recharge_timer = temp_state.recharge_timer

    if spell['effect'] == 'shield':
        shield_timer = spell['duration']
    elif spell['effect'] == 'poison':
        poison_timer = spell['duration']
    elif spell['effect'] == 'recharge':
        recharge_timer = spell['duration']

    # Step 9: Check if boss died from spell
    if boss_hp <= 0:
        return State(
            player_hp=player_hp,
            player_mana=player_mana,
            boss_hp=boss_hp,
            shield_timer=shield_timer,
            poison_timer=poison_timer,
            recharge_timer=recharge_timer,
            mana_spent=mana_spent,
            turn='boss'
        )

    # Step 10: Return new state with turn = 'boss'
    return State(
        player_hp=player_hp,
        player_mana=player_mana,
        boss_hp=boss_hp,
        shield_timer=shield_timer,
        poison_timer=poison_timer,
        recharge_timer=recharge_timer,
        mana_spent=mana_spent,
        turn='boss'
    )

def execute_boss_turn(state: State, boss_damage: int) -> Optional[State]:
    """
    Execute a boss turn.
    Returns new state or None if player dies.
    """
    # Step 1: Apply effects
    state, boss_died = apply_effects(state)

    # Step 2: Check if boss died from effects
    if boss_died:
        return state

    # Step 3: Calculate damage to player
    if state.shield_timer > 0:
        damage = max(1, boss_damage - 7)
    else:
        damage = boss_damage

    # Step 4: Deduct damage from player HP
    player_hp = state.player_hp - damage

    # Step 5: Check if player died
    if player_hp <= 0:
        return None

    # Step 6: Return new state with turn = 'player'
    return State(
        player_hp=player_hp,
        player_mana=state.player_mana,
        boss_hp=state.boss_hp,
        shield_timer=state.shield_timer,
        poison_timer=state.poison_timer,
        recharge_timer=state.recharge_timer,
        mana_spent=state.mana_spent,
        turn='player'
    )

def find_minimum_mana(boss_hp: int, boss_damage: int) -> Optional[int]:
    """
    Find the minimum mana needed to defeat the boss using priority queue search.
    """
    initial_state = State(
        player_hp=50,
        player_mana=500,
        boss_hp=boss_hp,
        shield_timer=0,
        poison_timer=0,
        recharge_timer=0,
        mana_spent=0,
        turn='player'
    )

    counter = 0  # Tie-breaker for heap
    pq = [(0, counter, initial_state)]
    visited = set()

    while pq:
        mana_spent, _, state = heapq.heappop(pq)

        # Check if boss is defeated
        if state.boss_hp <= 0:
            return mana_spent

        # Create hashable key (exclude mana_spent from state key)
        state_key = (
            state.player_hp,
            state.player_mana,
            state.boss_hp,
            state.shield_timer,
            state.poison_timer,
            state.recharge_timer,
            state.turn
        )

        if state_key in visited:
            continue
        visited.add(state_key)

        if state.turn == 'player':
            # Try casting each spell
            for spell in SPELLS:
                new_state = execute_player_turn(state, spell)
                if new_state:  # Valid move
                    counter += 1
                    heapq.heappush(pq, (new_state.mana_spent, counter, new_state))
        else:  # boss turn
            new_state = execute_boss_turn(state, boss_damage)
            if new_state:  # Player survived
                counter += 1
                heapq.heappush(pq, (new_state.mana_spent, counter, new_state))

    return None  # No winning path found

def main():
    # Parse input
    boss_hp, boss_damage = parse_input('input.md')

    # Find minimum mana
    result = find_minimum_mana(boss_hp, boss_damage)

    # Output result
    if result is None:
        print("No winning strategy found")
    else:
        print(result)

if __name__ == '__main__':
    main()
