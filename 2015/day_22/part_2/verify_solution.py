#!/usr/bin/env python3
"""Extended version that shows the spell sequence for verification."""

import heapq
from dataclasses import dataclass
from typing import Optional, Tuple, List

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

def apply_effects(state: State) -> Tuple[State, bool]:
    """Apply active effects at the start of a turn."""
    player_hp = state.player_hp
    player_mana = state.player_mana
    boss_hp = state.boss_hp
    shield_timer = state.shield_timer
    poison_timer = state.poison_timer
    recharge_timer = state.recharge_timer

    if poison_timer > 0:
        boss_hp -= 3
        poison_timer -= 1

    if recharge_timer > 0:
        player_mana += 101
        recharge_timer -= 1

    if shield_timer > 0:
        shield_timer -= 1

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
    """Execute a player turn with the given spell."""
    player_hp = state.player_hp - 1
    if player_hp <= 0:
        return None

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

    temp_state, boss_died = apply_effects(temp_state)

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

    if temp_state.player_mana < spell['cost']:
        return None

    if spell['effect'] == 'shield' and temp_state.shield_timer > 0:
        return None
    if spell['effect'] == 'poison' and temp_state.poison_timer > 0:
        return None
    if spell['effect'] == 'recharge' and temp_state.recharge_timer > 0:
        return None

    player_mana = temp_state.player_mana - spell['cost']
    mana_spent = temp_state.mana_spent + spell['cost']
    boss_hp = temp_state.boss_hp - spell['damage']
    player_hp = temp_state.player_hp + spell['heal']

    shield_timer = temp_state.shield_timer
    poison_timer = temp_state.poison_timer
    recharge_timer = temp_state.recharge_timer

    if spell['effect'] == 'shield':
        shield_timer = spell['duration']
    elif spell['effect'] == 'poison':
        poison_timer = spell['duration']
    elif spell['effect'] == 'recharge':
        recharge_timer = spell['duration']

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
    """Execute a boss turn."""
    state, boss_died = apply_effects(state)

    if boss_died:
        return state

    if state.shield_timer > 0:
        damage = max(1, boss_damage - 7)
    else:
        damage = boss_damage

    player_hp = state.player_hp - damage

    if player_hp <= 0:
        return None

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

def find_minimum_mana_with_path(boss_hp: int, boss_damage: int) -> Tuple[Optional[int], List[str]]:
    """Find minimum mana with spell sequence."""
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

    counter = 0
    pq = [(0, counter, initial_state)]
    visited = set()
    parent = {}  # state -> (parent_state, spell_name)

    while pq:
        mana_spent, _, state = heapq.heappop(pq)

        if state.boss_hp <= 0:
            # Reconstruct path
            path = []
            current = state
            while current in parent:
                prev_state, spell_name = parent[current]
                path.append(spell_name)
                current = prev_state
            path.reverse()
            return mana_spent, path

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
            for spell in SPELLS:
                new_state = execute_player_turn(state, spell)
                if new_state:
                    counter += 1
                    heapq.heappush(pq, (new_state.mana_spent, counter, new_state))
                    if new_state not in parent:
                        parent[new_state] = (state, spell['name'])
        else:
            new_state = execute_boss_turn(state, boss_damage)
            if new_state:
                counter += 1
                heapq.heappush(pq, (new_state.mana_spent, counter, new_state))
                if new_state not in parent:
                    parent[new_state] = (state, "Boss turn")

    return None, []

if __name__ == '__main__':
    print("=" * 70)
    print("Verifying Solution for Boss HP=71, Damage=10")
    print("=" * 70)
    print()

    result, path = find_minimum_mana_with_path(71, 10)

    if result:
        print(f"Minimum mana: {result}")
        print()
        print("Spell sequence (player turns only):")
        player_turn = 0
        for spell in path:
            if spell != "Boss turn":
                player_turn += 1
                print(f"  Turn {player_turn}: {spell}")
        print()
        print(f"Total player turns: {player_turn}")
    else:
        print("No winning strategy found")
