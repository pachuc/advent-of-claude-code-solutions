# Implementation Summary: RPG Simulator 20XX - Maximum Gold to Lose

## Problem Overview
The goal was to find the **maximum amount of gold** you can spend on equipment while still **losing** the fight against the boss. This is the inverse of part 1, where the goal was to minimize cost while winning.

## Solution Approach

### Algorithm
1. **Parse boss statistics** from input.md (HP: 103, Damage: 9, Armor: 2)
2. **Generate all valid equipment combinations** following purchase rules:
   - Exactly 1 weapon (required)
   - 0 or 1 armor (optional)
   - 0, 1, or 2 rings (optional)
3. **Simulate combat** for each combination using mathematical optimization
4. **Track the maximum cost** among combinations where the player loses
5. **Return the result**

### Key Implementation Details

#### Combat Simulation
Instead of simulating turn-by-turn combat, I used a mathematical approach:
- Calculate damage per turn: `max(1, attacker_damage - defender_armor)`
- Calculate turns needed to win: `ceil(hp / damage_per_turn)`
- Player wins if `turns_to_kill_boss <= turns_to_kill_player` (player attacks first)

This optimization reduces combat simulation from O(k) to O(1) where k is the number of turns.

#### Equipment Combinations
Generated all valid combinations by:
1. Pre-generating all ring combinations (none, singles, pairs)
2. Iterating through all weapons (5 options)
3. Iterating through armor options including "no armor" (6 options)
4. Iterating through ring combinations (22 options)

Total combinations: 5 × 6 × 22 = **660 combinations**

Note: The test plan expected 630 combinations (5 × 6 × 21), but the correct count is 660 because there are 22 ring combinations (1 none + 6 singles + 15 pairs), not 21.

#### Duplicate Handling
The implementation generates 660 combinations, but only 616 are unique. This is expected because different equipment sets can produce the same (cost, damage, armor) stats. For example:
- Dagger (8) + Splintmail (53) = (61, 4, 3)
- Other combinations can also result in (61, 4, 3)

These duplicates don't affect the correctness of the solution because we're finding the maximum cost for losing combinations.

## Files Created

### solution.py
Main solution file containing:
- `weapons`, `armor`, `rings`: Shop inventory data structures
- `simulate_combat()`: Mathematical combat simulator
- `generate_equipment_combinations()`: Generates all valid equipment combinations
- `parse_boss_stats()`: Parses boss statistics from input file
- `find_max_gold_to_lose()`: Main solution logic
- Main entry point that prints the result

## Testing Process

### Unit Tests - Combat Simulation
Tested the combat simulator with various scenarios:
- ✓ Basic combat where player wins
- ✓ Basic combat where player loses
- ✓ Minimum damage rule (when armor > damage)
- ✓ Both sides dealing minimum damage
- ✓ Actual boss stats with cheap equipment

All combat tests passed successfully.

### Unit Tests - Equipment Generation
Tested the combination generator:
- ✓ Total combinations: 660 (not 630 as initially expected)
- ✓ Minimum cost: 8 gold (Dagger only)
- ✓ Maximum cost: 356 gold (Greataxe + Platemail + Damage+3 + Defense+3)
- ✓ Cheapest combination: (8, 4, 0)
- ✓ Most expensive combination: (356, 11, 8)

Note: Found 44 duplicate stat combinations (660 total, 616 unique), which is expected and doesn't affect correctness.

### Integration Tests
- ✓ Solution runs successfully and outputs: **201**
- ✓ Verified the answer: cost 201 with stats (7 damage, 4 armor) loses to the boss
  - Player deals 5 damage/turn, needs 21 turns to win
  - Boss deals 5 damage/turn, needs 20 turns to win
  - Boss wins!
- ✓ Verified no losing combinations exist with cost > 201
- ✓ Total combinations: 660 (381 winning, 279 losing)

### Boundary Analysis
- Minimum cost to lose: 8 gold
- Maximum cost to lose: **201 gold** ← Our answer
- Minimum cost to win: 121 gold
- Maximum cost to win: 356 gold

The ranges overlap (121-201), demonstrating that spending more doesn't guarantee victory - equipment choice matters!

### Input Parsing
- ✓ Successfully parsed boss stats from input.md
- ✓ Boss HP: 103, Damage: 9, Armor: 2

## Result

**Answer: 201 gold**

This is the maximum amount you can spend on equipment while still losing to the boss. The losing equipment combination with this cost has:
- Damage: 7
- Armor: 4

In combat:
- Player deals 5 damage per turn (7 - 2 armor)
- Boss deals 5 damage per turn (9 - 4 armor)
- Player needs 21 turns to defeat boss (103 HP / 5 damage)
- Boss needs 20 turns to defeat player (100 HP / 5 damage)
- Since the boss needs fewer turns, the player loses!

## Performance

The solution runs efficiently:
- Time complexity: O(660) combinations × O(1) combat simulation = O(1) effective
- Space complexity: O(660) to store combinations = O(1) effective
- Execution time: < 0.1 seconds

The exhaustive search approach is optimal for this problem size and doesn't require any optimization techniques.
