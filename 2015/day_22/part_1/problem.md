# Problem Report: Wizard Combat Simulator

## Objective
Find the minimum amount of mana required to defeat a boss in a turn-based combat system where the player is a wizard with spell-casting abilities.

## Combat Rules

### Initial Conditions
- Player starts with: 50 hit points, 500 mana
- Boss stats (from input): 71 hit points, 10 damage
- Player always goes first
- First character to reach 0 or below hit points loses

### Turn Structure
1. Player turn: Must cast one spell (if affordable)
2. Boss turn: Attacks the player
3. Effects are applied at the START of both player and boss turns (before any actions)
4. Effects tick down by 1 at the start of each turn after applying their effect
5. Effects expire when their timer reaches 0

### Available Spells

| Spell | Mana Cost | Effect |
|-------|-----------|--------|
| Magic Missile | 53 | Instant 4 damage to boss |
| Drain | 73 | Instant 2 damage to boss, heal player 2 HP |
| Shield | 113 | Effect lasting 6 turns: +7 armor to player |
| Poison | 173 | Effect lasting 6 turns: 3 damage to boss per turn |
| Recharge | 229 | Effect lasting 5 turns: +101 mana per turn |

### Important Constraints
- Cannot cast a spell if you don't have enough mana (instant loss)
- Cannot cast a spell that would start an effect that is already active
- Effects CAN be started on the same turn they end
- Mana costs are deducted immediately when spell is cast
- Boss attacks are reduced by armor, but always deal at least 1 damage
- Boss effectively has 0 armor (magic damage ignores armor)

### Effect Timing
- Effects apply at the start of BOTH player and boss turns
- Effects apply BEFORE the player chooses a spell or the boss attacks
- After applying effects, timers decrease by 1
- When timer reaches 0, the effect ends

## Input Format
The input provides the boss's initial statistics in the format:
```
Hit Points: <number>
Damage: <number>
```

For this puzzle:
- Boss Hit Points: 71
- Boss Damage: 10

## Expected Output
A single integer representing the minimum amount of mana that must be spent to win the fight.

Note: Mana gained from Recharge effects does NOT count as "spending negative mana" - only mana spent on casting spells counts toward the total.

## Solution Approach
This is an optimization problem requiring finding the optimal sequence of spell casts that:
1. Defeats the boss (reduces boss HP to 0 or below)
2. Keeps the player alive (player HP stays above 0)
3. Minimizes total mana spent

This likely requires exploring different spell casting sequences (e.g., using search algorithms like BFS, DFS, Dijkstra's, or A*) to find the winning strategy with minimal mana cost.
