# Implementation Plan: Wizard Simulator 20XX - Hard Mode

## Plan Updates (v2)

**Key improvements based on critique:**
1. ✓ Clarified effect duration mechanics - effects apply exactly N times for duration N
2. ✓ Emphasized hard mode penalty timing - happens FIRST before effects on player turns
3. ✓ Specified effect re-casting rules - can cast on same turn effect expires
4. ✓ Fixed function signature in pseudocode - removed unnecessary boss_damage from player turn
5. ✓ Added explanation for why Dijkstra works with Recharge (tracks spent, not balance)
6. ✓ Added None handling in main function
7. ✓ Added optional path reconstruction suggestion for debugging
8. ✓ Clarified state dominance pruning as optional enhancement

## Problem Analysis

This is a shortest-path optimization problem in a game state space where:
- **Goal**: Find minimum mana expenditure to defeat the boss
- **Constraint**: Hard mode - player loses 1 HP at start of each player turn
- **Search space**: All possible sequences of spell castings
- **Optimization**: Minimum total mana spent

The problem requires exploring different spell sequences while tracking game state (HP, mana, active effects) and finding the path with minimum mana cost that leads to victory.

## Algorithm Choice: Priority Queue Search (Dijkstra-like)

**Why this approach:**
- We need to find the minimum cost (mana) path to victory
- State space is finite but large (HP ranges, mana values, effect combinations)
- Dijkstra's algorithm guarantees finding the optimal (minimum cost) solution
- Priority queue ensures we explore cheaper paths first
- Early termination when first winning state is found (since we're exploring in order of increasing cost)

**Time Complexity Estimate:** O(S * log S) where S is the number of unique states explored
**Space Complexity:** O(S) for storing visited states and priority queue

## Step-by-Step Implementation Plan

### Step 1: Parse Input
- Read the input file to extract boss stats
- Parse "Hit Points: X" and "Damage: Y" format
- Store as integers for boss_hp and boss_damage

### Step 2: Define Data Structures

#### Spell Data Structure
Create a dictionary/list defining each spell with:
- Name (for debugging)
- Mana cost
- Instant damage to boss (if applicable)
- Instant healing to player (if applicable)
- Effect type (Shield/Poison/Recharge)
- Effect duration (if applicable)

```python
SPELLS = [
    {'name': 'Magic Missile', 'cost': 53, 'damage': 4, 'heal': 0, 'effect': None},
    {'name': 'Drain', 'cost': 73, 'damage': 2, 'heal': 2, 'effect': None},
    {'name': 'Shield', 'cost': 113, 'damage': 0, 'heal': 0, 'effect': 'shield', 'duration': 6},
    {'name': 'Poison', 'cost': 173, 'damage': 0, 'heal': 0, 'effect': 'poison', 'duration': 6},
    {'name': 'Recharge', 'cost': 229, 'damage': 0, 'heal': 0, 'effect': 'recharge', 'duration': 5}
]
```

#### Game State Structure
Create a state class/tuple representing:
- Player HP
- Player mana
- Boss HP
- Shield timer (0 if not active)
- Poison timer (0 if not active)
- Recharge timer (0 if not active)
- Total mana spent so far
- Whose turn it is (player/boss)

**Key insight:** Use immutable state representation (tuples/frozen dataclass) for hashability and visited set tracking.

### Step 3: Implement Effect Application Logic

Create a function `apply_effects(state)` that:
1. Checks each active effect (timer > 0)
2. For Shield: Maintains armor at 7 (armor is checked during boss attacks, not applied here)
3. For Poison: Deals 3 damage to boss
4. For Recharge: Gives player 101 mana
5. Decrements all active effect timers by 1
6. Returns new state and whether boss died from effects

**Critical Effect Duration Mechanics:**
- An effect with timer=6 applies its effect 6 times total (once per turn it's active)
- Timer decrements AFTER the effect applies
- When timer reaches 0, the effect is removed (no longer active)
- Example: Shield cast on turn 1 with timer=6 → applies on turns 1,2,3,4,5,6 → expires after turn 6
- Effect is considered "active" if timer > 0 BEFORE that turn's effect application
- Effect is considered "expired/inactive" if timer = 0 AFTER that turn's effect application

**Critical:** This function is called at the start of BOTH player and boss turns.

### Step 4: Implement Player Turn Logic

Create a function `execute_player_turn(state, spell)` that follows this EXACT sequence:

1. **Hard mode penalty**: Deduct 1 HP from player FIRST (before anything else)
2. Check if player died from hard mode penalty (HP <= 0) -> return None (loss)
3. Apply effects using `apply_effects()`
4. Check if boss died from effects (boss_hp <= 0) -> return winning state
5. Validate spell can be cast:
   - Player has enough mana (current_mana >= spell_cost)
   - If spell creates an effect, that effect must not be currently active (timer must be 0 after step 3)
   - If invalid, return None
6. Deduct mana cost from available mana, ADD mana cost to mana_spent tracker
7. Apply spell's instant effects (damage to boss, healing to player)
8. Start new effect if spell has one (set timer to spell's duration)
9. Check if boss died from spell damage (boss_hp <= 0) -> return winning state
10. Return new state with turn = 'boss'

**Critical timing note:** Effects that expire during step 3 (timer becomes 0) are no longer active, so the same effect spell CAN be cast on this turn in step 5.

### Step 5: Implement Boss Turn Logic

Create a function `execute_boss_turn(state, boss_damage)` that follows this EXACT sequence:

1. Apply effects using `apply_effects()`
2. Check if boss died from effects (boss_hp <= 0) -> return winning state
3. Calculate damage to player:
   - If shield active (shield_timer > 0 after step 1): damage = max(1, boss_damage - 7)
   - Otherwise: damage = boss_damage
4. Deduct damage from player HP
5. Check if player died (player_hp <= 0) -> return None (loss)
6. Return new state with turn = 'player'

**Note:** Boss turn does NOT have hard mode penalty - only player turns have the 1 HP loss.

### Step 6: Implement Main Search Algorithm

Use priority queue (min-heap) based search:

```python
def find_minimum_mana(boss_hp, boss_damage):
    initial_state = State(
        player_hp=50, player_mana=500, boss_hp=boss_hp,
        shield_timer=0, poison_timer=0, recharge_timer=0,
        mana_spent=0, turn='player'
    )

    pq = [(0, initial_state)]  # (mana_spent, state)
    visited = set()

    while pq:
        mana_spent, state = heappop(pq)

        # Check if boss is defeated (check before processing to handle initial wins)
        if state.boss_hp <= 0:
            return mana_spent

        # Create hashable key (exclude mana_spent from state key)
        state_key = (state.player_hp, state.player_mana, state.boss_hp,
                     state.shield_timer, state.poison_timer,
                     state.recharge_timer, state.turn)

        if state_key in visited:
            continue
        visited.add(state_key)

        if state.turn == 'player':
            # Try casting each spell
            for spell in SPELLS:
                new_state = execute_player_turn(state, spell)
                if new_state:  # Valid move (didn't result in loss)
                    heappush(pq, (new_state.mana_spent, new_state))
        else:  # boss turn
            new_state = execute_boss_turn(state, boss_damage)
            if new_state:  # Player survived
                heappush(pq, (new_state.mana_spent, new_state))

    return None  # No winning path found
```

**Why Dijkstra's Algorithm Works Here:**
- All spell costs are positive (no negative cost edges)
- We track total mana SPENT, not remaining mana
- Recharge grants mana but still costs 229 to cast, so it increases mana_spent by 229
- The priority queue ensures we explore states in order of increasing mana spent
- First winning state found is guaranteed to be optimal
- This is true even though Recharge provides a net mana gain - we're optimizing spent, not balance

### Step 7: State Representation Optimization

**Critical optimization:** The visited set should track states without the "mana_spent" component, but we should only skip a state if we've seen the exact same game configuration before. Since we're using a priority queue and exploring in order of increasing mana cost, the first time we visit a state is guaranteed to be with the minimum mana to reach that state.

**State key for visited set:**
```python
(player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer, turn)
```

**Rationale for including player_mana:**
- Mana can be gained through Recharge effects
- Reaching the same HP/boss HP/effects configuration with different available mana represents different strategic situations
- A state with more available mana has more spell options

**Optional Enhancement - State Dominance Pruning:**
If performance becomes an issue, consider this optimization: if we've visited a state with (same HP, same boss_hp, same effects, same turn) but with more or equal available mana for less or equal total spent, we can prune the new state. However, this adds complexity and is likely unnecessary for the given input size.

### Step 8: Handle Edge Cases in Implementation

1. **Hard mode death before effects**: Player loses 1 HP before anything else on player turns
2. **Boss death from effects**: Check after each effect application
3. **Effect expiration**: Effects that reach timer=0 apply one last time then end
4. **Cannot cast effect spell if effect active**: Check timer > 0 before allowing cast
5. **Mana insufficiency**: Skip spells player cannot afford
6. **Minimum damage rule**: Boss always deals at least 1 damage

### Step 9: Main Program Structure

```python
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
```

**Optional Debugging Enhancement:**
For debugging and verification purposes, consider adding an optional parameter to track and return the spell sequence used:
- Store parent pointers in the search (state -> (parent_state, spell_used))
- When winning state is found, backtrack to reconstruct the spell sequence
- This is NOT required for the solution but very helpful for validation

## Implementation Order

1. Define constants (SPELLS, initial player stats)
2. Create State class/namedtuple
3. Implement `apply_effects()`
4. Implement `execute_player_turn()`
5. Implement `execute_boss_turn()`
6. Implement `find_minimum_mana()` with priority queue
7. Implement input parsing
8. Implement main()
9. Test with provided input

## Expected Runtime

With the given input (Boss HP: 71, Damage: 10), the state space is manageable:
- Player HP: ~1-50 (starts at 50, decreases each turn)
- Boss HP: ~1-71 (decreases from spells/poison)
- Mana: Variable (starts at 500, can increase with Recharge)
- Effect combinations: 3 effects with various timer values

Estimated states to explore: Tens of thousands at most.
Expected runtime: Sub-second on modern hardware.

## Memory Considerations

- Priority queue will grow as we explore states
- Visited set prevents revisiting states
- Each state is relatively small (~7 integers)
- Expected memory usage: A few MB at most

## Potential Optimizations (if needed)

1. **A* heuristic**: Estimate minimum remaining mana needed (optimistic: boss_hp / 4 * 53 for Magic Missile spam)
2. **Prune dominated states**: If we've seen a state with same/better HP and same/more mana for less total spent, prune new state
3. **Limit mana tracking**: Cap mana at reasonable maximum (e.g., 1500) since extremely high mana values are unlikely to be optimal
