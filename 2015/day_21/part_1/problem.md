# Problem Report: RPG Combat Optimization

## Objective
Find the minimum amount of gold required to purchase equipment that will allow the player to defeat the boss in a turn-based RPG combat scenario.

## Context
This is a turn-based combat simulation where the player and boss exchange attacks until one reaches 0 or fewer hit points. The player always attacks first. Victory requires selecting the most cost-effective combination of equipment from a shop.

## Combat Mechanics

### Turn Resolution
- Player and boss alternate attacks (player goes first)
- Damage dealt = attacker's damage score - defender's armor score
- Minimum damage per attack is always 1 (even if armor exceeds damage)
- First combatant to reach 0 or fewer hit points loses

### Player Stats
- Starting hit points: 100
- Starting damage: 0
- Starting armor: 0
- Stats increase based on purchased equipment

### Boss Stats (from input)
- Hit points: 103
- Damage: 9
- Armor: 2

## Shop Inventory

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

## Purchase Constraints
- Must buy exactly 1 weapon (required)
- Can buy 0 or 1 armor piece (optional)
- Can buy 0, 1, or 2 rings (optional, maximum one per hand)
- Each item is unique (cannot buy duplicates)
- All purchased items must be used

## Input
The boss stats are provided in the following format:
```
Hit Points: 103
Damage: 9
Armor: 2
```

## Expected Output
A single integer representing the minimum amount of gold needed to purchase equipment that guarantees a player victory.

## Algorithm Requirements
1. Generate all valid equipment combinations based on constraints
2. For each combination, calculate total cost and player stats (damage and armor)
3. Simulate combat to determine if player wins
4. Track the minimum cost among all winning combinations
5. Return the minimum cost
