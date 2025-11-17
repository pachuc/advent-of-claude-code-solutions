# Implementation Summary: Wizard Combat Simulator

## Overview
Successfully implemented a solution to find the minimum mana cost to defeat a boss in a turn-based wizard combat game using Dijkstra's algorithm for optimal pathfinding.

## Solution Approach
Used **Dijkstra's algorithm** to explore the state space of all possible spell-casting sequences, guaranteeing the optimal (minimum mana) solution.

## Files Created
1. **solution.py** - Main implementation file containing:
   - Input parsing logic
   - Spell definitions and game mechanics
   - Core game functions (apply_effects, cast_spell, boss_attack)
   - Dijkstra's search algorithm
   - Main function to solve the puzzle

2. **test_solution.py** - Test file for basic validation
3. **verify_solution.py** - Debug version that outputs the winning spell sequence

## Implementation Details

### Key Components

#### 1. Data Structures
- **State Dictionary**: Tracks player HP, player mana, boss HP, and active effect timers
- **Spell Dictionary**: Defines all 5 spells with their costs, effects, and durations
- **Priority Queue**: Uses heapq with (mana_spent, counter, state) tuples for Dijkstra's algorithm
- **Visited Dictionary**: Maps state keys to minimum mana spent to reach that state

#### 2. Core Functions

**apply_effects(state)**
- Applies active effects at the start of each turn
- Correct timing sequence: apply effects → decrement timers → check expiration
- Shield provides 7 armor when timer > 0
- Poison deals 3 damage per turn
- Recharge adds 101 mana per turn
- Returns updated state and whether boss died from effects

**cast_spell(state, spell_name)**
- Validates spell can be cast (enough mana, effect not already active)
- Critical logic: checks `timer > 0` to determine if effect is active
- This allows recasting effects on the turn they expire (timer = 0)
- Deducts mana cost and applies instant effects
- Returns new state or None if invalid

**boss_attack(state, boss_damage)**
- Determines armor based on Shield timer
- Calculates damage with minimum of 1 (boss always deals at least 1 damage)
- Applies damage to player HP

**state_key(state)**
- Creates hashable tuple for state comparison
- Excludes mana_spent for proper Dijkstra's optimization
- Allows tracking minimum cost to reach each game state

#### 3. Dijkstra's Algorithm
The search explores states in order of increasing mana spent:
1. Start with initial state (50 HP, 500 mana)
2. For each state, simulate player turn with all possible spells
3. Apply effects, check for victory/defeat
4. Simulate boss turn if boss still alive
5. Prune states already visited with lower cost
6. Return mana spent when boss reaches 0 HP

### Critical Implementation Details
- **Effect Timing**: Effects apply at the START of both player and boss turns, BEFORE any actions
- **Effect Recasting**: Used `timer > 0` check (not `>= 0`) to allow recasting on expiration turn
- **Heap Comparison Fix**: Added counter to break ties in priority queue to avoid dict comparison errors
- **Mana Tracking**: Only spell costs count toward total; mana gained from Recharge doesn't subtract
- **State Pruning**: Skip states visited with equal or lower cost for efficiency

## Testing Process

### Test Cases Run
1. **Simple Boss Test** (10 HP, 8 damage)
   - Result: 159 mana (3× Magic Missile)
   - Verified optimal for quick kill scenario

2. **Actual Puzzle Input** (71 HP, 10 damage)
   - Result: 1824 mana
   - Winning sequence verified

3. **Winning Strategy Validation**
   - Used debug version to extract spell sequence
   - Verified all spell costs sum correctly
   - Confirmed strategy makes tactical sense

### Winning Strategy for Puzzle Input
The algorithm found the optimal 12-spell sequence:

| Spell # | Spell Name | Cost | Running Total |
|---------|------------|------|---------------|
| 1 | Poison | 173 | 173 |
| 2 | Recharge | 229 | 402 |
| 3 | Shield | 113 | 515 |
| 4 | Poison | 173 | 688 |
| 5 | Recharge | 229 | 917 |
| 6 | Shield | 113 | 1030 |
| 7 | Poison | 173 | 1203 |
| 8 | Recharge | 229 | 1432 |
| 9 | Shield | 113 | 1545 |
| 10 | Magic Missile | 53 | 1598 |
| 11 | Poison | 173 | 1771 |
| 12 | Magic Missile | 53 | 1824 |

**Strategy Analysis:**
- **Poison** (4 casts): Primary damage dealer, 18 damage per cast over 6 turns = 72 total damage for 692 mana
- **Recharge** (3 casts): Maintains mana supply, generates 505 mana per cast for 687 mana investment
- **Shield** (3 casts): Reduces damage taken, extends survival time for 339 mana
- **Magic Missile** (2 casts): Finishing damage for 106 mana

This strategy balances offense (Poison), defense (Shield), and resource management (Recharge) to achieve minimum mana cost.

### Issues Encountered and Resolved

#### Issue 1: TypeError in Heap Comparison
**Problem**: When two states had the same mana_spent value, heapq tried to compare dict objects directly, causing a TypeError.

**Solution**: Added a counter as a tie-breaker in the priority queue tuple: `(mana_spent, counter, state)`. The counter increments for each new state added, ensuring unique ordering even when mana costs are equal.

**Code Change**: Modified all `heapq.heappush()` calls to include counter value.

### Verification
- ✅ Correct input parsing (Boss: 71 HP, 10 damage)
- ✅ Proper effect timing implementation
- ✅ Effect recasting works correctly
- ✅ Boss always deals minimum 1 damage
- ✅ Dijkstra's finds optimal path
- ✅ Spell sequence sums to correct total
- ✅ Solution completes in reasonable time (~1 second)

## Final Answer
**1824 mana**

The solution correctly implements all game rules, uses an optimal search algorithm, and finds the minimum mana cost to defeat the boss while keeping the player alive.
