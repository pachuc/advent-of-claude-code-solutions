# Problem Report: Wizard Simulator 20XX - Hard Mode

## Objective
Find the **minimum amount of mana** that must be spent to defeat a boss in a turn-based RPG battle simulation running in **hard mode**.

## Hard Mode Modification
At the start of each **player turn** (before any other effects apply), the player loses 1 hit point. If this brings the player to or below 0 hit points, the player loses the game.

## Game Context

### Initial Player Stats
- Hit Points: 50
- Mana: 500 (no maximum limit)
- Armor: 0 (initially, can be increased by Shield spell)

### Boss Stats (from input)
- Hit Points: 71
- Damage: 10

### Combat Rules
1. Turn-based combat with player going first
2. Alternating turns: Player -> Boss -> Player -> Boss, etc.
3. First character to reach 0 or fewer hit points loses
4. Player must cast exactly one spell per turn
5. If player cannot afford any spell, player loses
6. Boss deals physical damage equal to its Damage stat minus player's armor (minimum 1 damage)
7. Boss's armor is ignored (magic damage)

### Available Spells

| Spell | Mana Cost | Effect |
|-------|-----------|--------|
| Magic Missile | 53 | Instantly deals 4 damage to boss |
| Drain | 73 | Instantly deals 2 damage to boss and heals player for 2 HP |
| Shield | 113 | Starts an effect lasting 6 turns; increases player armor by 7 |
| Poison | 173 | Starts an effect lasting 6 turns; deals 3 damage to boss each turn |
| Recharge | 229 | Starts an effect lasting 5 turns; gives player 101 mana each turn |

### Effect Rules
1. Effects apply at the **start** of both player and boss turns
2. Effects have a timer (number of turns remaining)
3. At the start of each turn:
   - Effect applies its benefit/damage
   - Timer decreases by 1
   - If timer reaches 0, effect ends after applying
4. **Cannot cast a spell that would start an effect that is already active**
5. Effects can be started on the same turn they end

### Turn Sequence (Hard Mode)
**Player Turn:**
1. Player loses 1 HP (hard mode penalty) - if this kills player, player loses
2. Active effects apply (Poison damages boss, Recharge gives mana, Shield remains active)
3. Effect timers decrement; effects ending at 0 are removed
4. Player casts one spell, mana is deducted immediately

**Boss Turn:**
1. Active effects apply (Poison damages boss, Recharge gives mana, Shield remains active)
2. Effect timers decrement; effects ending at 0 are removed
3. If boss is still alive, boss attacks player for (Damage - player's armor) damage, minimum 1

## Input Format
The input contains the boss's stats in the following format:
```
Hit Points: <integer>
Damage: <integer>
```

## Expected Output
A single integer representing the **minimum amount of mana** that must be spent to win the fight.

**Important:** Do not count mana gained from Recharge effects as negative spending. Only count mana spent on casting spells.

## Solution Approach
This is an optimization problem requiring search through possible spell sequences to find the minimum mana expenditure that results in victory. The hard mode constraint of losing 1 HP at the start of each player turn makes the problem more difficult and time-sensitive, as the player must defeat the boss before running out of hit points from the hard mode penalty combined with boss attacks.
