# Problem Report: RPG Simulator 20XX - Maximum Gold to Lose

## Objective

Find the **maximum** amount of gold you can spend on equipment and still **lose** the fight against the boss. This is an optimization problem where we want to spend as much as possible while still being defeated.

## Context

You're playing an RPG where you fight a boss in turn-based combat. A shopkeeper (who is working with the boss) is trying to get you to buy expensive equipment that won't help you win. You need to determine the most expensive equipment combination that will still result in your defeat.

## Game Mechanics

### Combat Rules
- Turn-based combat where the player **always attacks first**
- Damage per turn = attacker's damage score - defender's armor score
- Minimum damage per turn is always **1** (even if armor exceeds damage)
- First character to reach 0 or fewer hit points loses
- Player has **100 hit points**

### Damage Calculation Formula
```
damage_dealt = max(1, attacker_damage - defender_armor)
```

## Input

Boss statistics (from input.md):
- Hit Points: 103
- Damage: 9
- Armor: 2

## Shop Inventory and Purchase Rules

### Weapons (Cost, Damage, Armor)
- Dagger: 8 gold, 4 damage, 0 armor
- Shortsword: 10 gold, 5 damage, 0 armor
- Warhammer: 25 gold, 6 damage, 0 armor
- Longsword: 40 gold, 7 damage, 0 armor
- Greataxe: 74 gold, 8 damage, 0 armor

### Armor (Cost, Damage, Armor)
- Leather: 13 gold, 0 damage, 1 armor
- Chainmail: 31 gold, 0 damage, 2 armor
- Splintmail: 53 gold, 0 damage, 3 armor
- Bandedmail: 75 gold, 0 damage, 4 armor
- Platemail: 102 gold, 0 damage, 5 armor

### Rings (Cost, Damage, Armor)
- Damage +1: 25 gold, 1 damage, 0 armor
- Damage +2: 50 gold, 2 damage, 0 armor
- Damage +3: 100 gold, 3 damage, 0 armor
- Defense +1: 20 gold, 0 damage, 1 armor
- Defense +2: 40 gold, 0 damage, 2 armor
- Defense +3: 80 gold, 0 damage, 3 armor

### Purchase Constraints
- **Must buy exactly 1 weapon** (required)
- **Can buy 0 or 1 armor** (optional)
- **Can buy 0, 1, or 2 rings** (optional, at most one per hand)
- Each item can only be purchased once (shop has one of each)
- Your total damage = sum of damage from all items
- Your total armor = sum of armor from all items

## Expected Output

A single integer representing the **maximum amount of gold** you can spend on equipment while still **losing** the fight against the boss.

## Algorithm Requirements

1. Generate all valid equipment combinations based on purchase constraints
2. For each combination:
   - Calculate total cost
   - Calculate player's total damage and armor
   - Simulate the fight to determine winner
3. Filter combinations where the player **loses**
4. Return the **maximum** cost among losing combinations

## Success Criteria

The fight outcome is determined by simulating turn-by-turn combat until either the player or boss reaches 0 or fewer hit points. The player loses if the boss defeats them.
