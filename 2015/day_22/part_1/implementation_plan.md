# Implementation Plan: Wizard Combat Simulator (REVISED)

## Overview
Implement a solution to find the minimum mana cost to defeat the boss using Dijkstra's algorithm to explore the state space of possible spell sequences.

## Key Updates from Critique
This plan has been revised to address critical issues identified in the critique:

1. **Effect Timing Clarified (CRITICAL):** Explicitly defined the sequence: apply effects (if timer > 0) → decrement timers → check expiration
2. **Spell Recasting Logic (CRITICAL):** Specified that effect availability check must use `timer > 0` (not `>= 0`) to allow recasting on expiration turn
3. **Armor Calculation:** Added explicit armor determination in boss_attack function
4. **State Hashing Reasoning:** Explained why mana_spent is excluded from state key
5. **Mana Limits:** Clarified that mana can exceed 500 and there's no upper cap
6. **Turn Sequence:** Expanded Dijkstra's pseudocode with detailed turn-by-turn logic
7. **Recharge Tracking:** Emphasized that only mana SPENT counts, not mana GAINED

## Algorithm Choice: Dijkstra's Algorithm
- **Why Dijkstra's?** We need to find the minimum cost (mana spent) path to victory
- **State Space:** Each state represents a combat snapshot (HP, mana, active effects)
- **Priority Queue:** Always explore states with lowest mana spent first
- **Guaranteed Optimal:** Dijkstra's guarantees we find the minimum mana solution

## Data Structures

### 1. State Representation
```python
state = {
    'player_hp': int,
    'player_mana': int,
    'boss_hp': int,
    'shield_timer': int,     # 0 means inactive
    'poison_timer': int,
    'recharge_timer': int,
    'mana_spent': int        # Total mana spent so far
}
```

### 2. Spell Definitions
Create a dictionary/list with spell properties:
- Name
- Mana cost
- Instant damage (if any)
- Instant heal (if any)
- Effect type (if any)
- Effect duration (if any)

## Implementation Steps

### Step 1: Parse Input
- Read the input file
- Extract boss HP and damage using regex or string parsing
- Store in variables: `boss_hp_initial`, `boss_damage`

### Step 2: Define Constants and Spells
- Player initial HP: 50
- Player initial mana: 500
- **Note:** Mana can exceed 500 due to Recharge effects; no upper limit
- Define all 5 spells with their properties:
  - Magic Missile: 53 mana, 4 damage
  - Drain: 73 mana, 2 damage, 2 heal
  - Shield: 113 mana, 6 turns, +7 armor
  - Poison: 173 mana, 6 turns, 3 damage/turn
  - Recharge: 229 mana, 5 turns, +101 mana/turn
- **Important:** Only mana SPENT on spells counts toward total; mana GAINED from Recharge does NOT count

### Step 3: Implement Effect Application Logic
Create a function `apply_effects(state)` that processes effects in the correct order:

**CRITICAL TIMING SEQUENCE:**
1. **Apply effects** (if timer > 0):
   - Shield: sets armor to 7 for this turn
   - Poison: deals 3 damage to boss
   - Recharge: adds 101 mana to player
2. **Decrement timers** by 1 for all active effects
3. **Effects expire** when timer reaches 0 after decrement
4. **Return** updated state and whether boss died from effects

**Important:** This sequence means:
- Effect is active if timer > 0 BEFORE decrement
- After decrement, if timer = 0, effect expires
- On the NEXT turn, effect can be recast (timer will be 0, so effect inactive)

### Step 4: Implement Spell Casting Logic
Create a function `cast_spell(state, spell)` that:
- Checks if player has enough mana (return None if not)
- **Checks if spell effect is already active (return None if so)**
  - **CRITICAL:** For effect spells (Shield/Poison/Recharge), check `timer > 0`
  - This allows recasting on the turn the effect expires (timer = 0)
  - Example: Shield timer = 1 → effects apply → timer decrements to 0 → can cast Shield again
- Deducts mana cost from player's mana
- Increases mana_spent by the spell's cost
- Applies instant effects (damage/heal)
- Starts effect timer if spell has an effect (sets timer to full duration)
- Returns new state with updated mana_spent

### Step 5: Implement Boss Turn Logic
Create a function `boss_attack(state, boss_damage)` that:
- **Determines armor:** `armor = 7 if shield_timer > 0 else 0`
  - Armor must be checked AFTER effects have been applied for the boss turn
- Calculates damage: `max(1, boss_damage - armor)`
  - Boss ALWAYS deals at least 1 damage, even with high armor
- Reduces player HP by damage amount
- Returns updated state

### Step 6: Implement State Hashing
Create a function to generate a hashable state key:
- Only include: player_hp, player_mana, boss_hp, and effect timers
- **Exclude: mana_spent** (we track this separately for optimization)
  - **Reasoning:** Same game state reached via different paths should be considered identical
  - We track the MINIMUM mana to reach each state separately in visited dictionary
  - This allows proper state pruning in Dijkstra's algorithm
- Used to detect if we've visited a state before
- Return as immutable tuple for use as dictionary key

### Step 7: Implement Dijkstra's Search
Main algorithm with detailed turn sequence:
```
1. Initialize priority queue with starting state (priority = mana_spent)
2. Initialize visited dictionary: state_key -> minimum_mana_spent
3. While queue is not empty:
   a. Pop state with lowest mana_spent
   b. Generate state_key
   c. If we've visited this state with lower or equal cost, skip
   d. Mark state as visited with current mana_spent

   === PLAYER TURN ===
   e. Apply effects at start of player turn (apply_effects)
      - Effects apply if timer > 0
      - Timers decrement after applying
      - Check if boss dies from effects (e.g., Poison)
   f. If boss HP <= 0, return mana_spent (VICTORY!)
   g. If player HP <= 0, skip this state (player died from effects - shouldn't happen)

   h. For each spell in [Magic Missile, Drain, Shield, Poison, Recharge]:
      i. Try to cast spell (cast_spell)
      ii. If cast fails (insufficient mana or effect already active), skip this spell
      iii. Create new_state after spell cast
      iv. If boss HP <= 0 (killed by instant spell), add to queue and continue
          (Don't process boss turn if boss is already dead)

      === BOSS TURN ===
      v. Apply effects at start of boss turn (apply_effects)
      vi. If boss HP <= 0, add new_state to queue and continue (BOSS DIED FROM EFFECTS)
      vii. If player HP <= 0, skip (player died from effects - shouldn't happen)
      viii. Boss attacks (boss_attack)
      ix. If player HP > 0, add new_state to priority queue

4. If queue empties without finding victory, return -1 (impossible)
```

**Key Points:**
- Effects apply at start of BOTH player and boss turns
- Check for victory/death after effects AND after actions
- Boss doesn't attack if already dead from effects or instant spell damage

### Step 8: Main Function
- Parse input (read boss HP and damage from file)
- Validate input (boss stats should be positive - basic check)
- Set up initial state:
  - player_hp = 50
  - player_mana = 500
  - boss_hp = parsed value
  - all effect timers = 0
  - mana_spent = 0
- Call Dijkstra's search
- Handle results:
  - If solution found: print the minimum mana cost (single integer)
  - If no solution: print -1 or error message (shouldn't happen with valid input)
- Output format: Just print the single number (the minimum mana cost)

## Optimization Considerations

### State Pruning
- Track visited states with their minimum mana cost
- Skip states we've seen before with equal or higher cost
- This prevents exponential blowup

### Early Termination
- Return immediately when boss dies (Dijkstra's guarantees this is optimal)
- Skip branches where player dies

### Effect Timing
- Carefully apply effects at the START of each turn BEFORE actions
- This is critical for correctness

## Time Complexity Analysis
- **State Space:** Bounded by (player_hp × player_mana × boss_hp × effect_timers)
- **Upper Bound:** ~50 × 1500 × 71 × 6 × 6 × 5 ≈ 96M states (theoretical max)
- **Practical:** Much smaller due to pruning and early termination
- **Per State:** O(5) for trying each spell
- **Overall:** Should complete in under a second for this input size

## Memory Complexity
- Priority queue: O(states_explored)
- Visited dictionary: O(unique_states)
- Should be manageable for this problem size

## Implementation Notes
- Use Python's `heapq` for priority queue
- Use tuples for state hashing
- Be careful with effect timing (most common source of bugs)
- Remember: effects can be recast on the turn they expire
- Boss always deals at least 1 damage (even if armor is high)
