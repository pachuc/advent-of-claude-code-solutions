# Problem Report: Immune System Simulator

## Overview
We are simulating a battle between two armies: the **Immune System** and the **Infection**. Each army consists of multiple groups of units that fight until only one army remains. We need to determine how many total units the winning army has after the battle concludes.

## Input Format
The input consists of two sections:

1. **Immune System:** A list of groups, each described on a single line
2. **Infection:** A list of groups, each described on a single line

Each group is described with the following format:
```
<units> units each with <hit_points> hit points (<modifiers>) with an attack that does <attack_damage> <attack_type> damage at initiative <initiative>
```

Where:
- `units`: number of identical units in the group
- `hit_points`: HP each unit can sustain before dying
- `modifiers`: (optional) weaknesses and/or immunities in parentheses
  - Format: `weak to <type1>, <type2>; immune to <type3>, <type4>`
  - Can be just weaknesses, just immunities, or both
  - Can be omitted entirely if no modifiers
- `attack_damage`: damage each unit deals per attack
- `attack_type`: type of damage (e.g., fire, cold, radiation, bludgeoning, slashing)
- `initiative`: determines attack order (higher goes first)

## Key Concepts

### Effective Power
- Calculated as: `units × attack_damage`
- Used for target selection ordering and tie-breaking

### Damage Calculation
- Base damage = attacker's effective power
- If defender is **immune** to attack type: damage = 0
- If defender is **weak** to attack type: damage = base damage × 2
- Otherwise: damage = base damage

### Unit Loss
- Only whole units die
- Units killed = floor(damage / hit_points)
- Remaining damage that doesn't kill a unit is ignored

## Combat Rules

Each fight has two phases that repeat until one army is eliminated:

### Phase 1: Target Selection
1. Groups select targets in order of:
   - Highest effective power first
   - Ties broken by highest initiative
2. Each group targets the enemy group it would damage the most
3. Tie-breaking for target selection (in order):
   - Choose target with highest potential damage
   - If tied, choose target with highest effective power
   - If still tied, choose target with highest initiative
4. Groups that cannot deal damage to any enemy don't select a target
5. Each group can only be targeted by one attacker

### Phase 2: Attacking
1. All groups attack in order of initiative (highest first), regardless of army
2. Groups with zero units cannot attack
3. Damage is dealt according to the damage calculation rules
4. Units are removed from defending groups

### Combat End
- Combat continues with new fights until one army has no units remaining

## Expected Output
A single integer: the total number of units remaining in the winning army after combat ends.

## Example
Given the example armies in the puzzle, the infection wins with 782 + 4434 = **5216** units.

## Task
Parse the input file, simulate the combat between the Immune System and Infection armies following the rules above, and output the total number of units in the winning army.
