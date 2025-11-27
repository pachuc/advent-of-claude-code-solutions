# Implementation Plan: Immune System Simulator

## Problem Analysis

This is a turn-based combat simulation between two armies (Immune System and Infection) with complex rules for target selection, damage calculation, and attack ordering. The key challenges are:

1. **Parsing complexity**: Groups have optional modifiers (weaknesses/immunities) in varying formats
2. **Multiple sorting criteria**: Target selection and attack ordering use multi-level tie-breaking
3. **State management**: Groups lose units during combat, affecting future calculations
4. **Combat loop**: Battle continues until one army is eliminated

### Algorithm Efficiency Considerations

- **Input size**: 10 groups for Immune System, 10 groups for Infection (20 groups total)
- **Expected runtime**: O(R × G²) where R is number of rounds and G is number of groups
- **Per round complexity**:
  - Target selection: O(G²) - each group considers all enemy groups
  - Attacking: O(G log G) - sorting by initiative
- **Overall**: Small input size means efficiency is not critical, but clean O(G²) per round is acceptable
- **Termination**: Combat ends when one army has 0 units, guaranteed to terminate

## Implementation Steps

### Step 1: Define Data Structures

Create a `Group` class to represent each combat group with:

**Attributes:**
- `id`: int (unique identifier for debugging/tracking)
- `army`: string ("Immune System" or "Infection")
- `units`: int (current number of units, decreases during combat)
- `hit_points`: int (HP per unit)
- `attack_damage`: int (damage per unit)
- `attack_type`: string (fire, cold, radiation, etc.)
- `initiative`: int (attack order priority)
- `weaknesses`: set of strings (damage types this group is weak to)
- `immunities`: set of strings (damage types this group is immune to)

**Methods:**
- `effective_power()`: returns `units × attack_damage`
- `calculate_damage_to(defender)`: calculates damage this group would deal to another
  - Returns 0 if defender is immune
  - Returns `effective_power() × 2` if defender is weak
  - Returns `effective_power()` otherwise
- `take_damage(damage)`: reduces units based on damage received
  - Units killed = `damage // hit_points`
  - Updates `units` attribute
- `is_alive()`: returns `units > 0`

### Step 2: Parse Input File

Create a `parse_input(filename)` function that:

1. Reads the file and splits into two sections (Immune System and Infection)
2. For each line in each section:
   - Use regex to extract: units, hit_points, attack_damage, attack_type, initiative
   - Parse optional modifiers section (text in parentheses):
     - Split by semicolon to separate weaknesses and immunities
     - Extract damage types after "weak to" into weaknesses set
     - Extract damage types after "immune to" into immunities set
     - Handle cases where only one or neither is present
   - Create a Group object with the parsed data
3. Return two lists: `immune_system_groups` and `infection_groups`

**Regex pattern approach:**
- Main pattern: `(\d+) units each with (\d+) hit points (?:\(([^)]+)\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)`
  - Capture groups: (1) units, (2) hit_points, (3) modifiers (optional), (4) attack_damage, (5) attack_type, (6) initiative
  - The `(?:...)` is a non-capturing group for the entire modifier section
  - `[^)]+` captures everything inside parentheses
  - The space after the closing `)` is inside the optional group to handle lines without modifiers
- Modifier parsing: Split the parentheses content, look for "weak to" and "immune to" keywords
  - Handle both orderings: "weak to X; immune to Y" and "immune to Y; weak to X"

### Step 3: Implement Target Selection Phase

Create a `target_selection(immune_groups, infection_groups)` function:

1. Combine all alive groups from both armies into a single list
2. Sort groups by:
   - Primary: effective power (descending)
   - Secondary: initiative (descending)
3. Initialize empty dictionary `targets = {}` to map attacker → defender
4. Track which groups have been selected as targets in a set
5. For each group in sorted order:
   - Identify enemy army groups (opposite of current group's army)
   - Filter out groups already selected as targets
   - For each potential target, calculate damage this group would deal
   - Filter out targets where damage would be 0 (immunity cases - don't select these)
   - If no valid targets remain (all would take 0 damage), skip this group entirely
   - Select target with:
     - Primary: highest damage
     - Secondary: highest effective power
     - Tertiary: highest initiative
   - Add mapping to `targets` dictionary
   - Mark selected target as taken
6. Return `targets` dictionary

### Step 4: Implement Attack Phase

Create an `attack_phase(targets)` function:

1. Get all attacking groups (keys from targets dictionary)
2. Sort attackers by initiative (descending)
3. Initialize counter: `units_killed_this_round = 0`
4. For each attacker in sorted order:
   - Check if attacker is still alive (units > 0)
     - Groups may have been killed in previous attacks this round
   - If not alive, skip to next attacker
   - If alive, get the target from the targets dictionary
   - Calculate current damage (use current effective power)
   - Store target's units before damage: `units_before = target.units`
   - Apply damage to target using `take_damage()` method
   - Calculate units killed: `units_killed_this_round += (units_before - target.units)`
5. Return `units_killed_this_round`
   - This value is used to detect stalemate (if 0, no progress made)

### Step 5: Implement Combat Simulation Loop

Create a `simulate_combat(immune_groups, infection_groups)` function:

1. While both armies have living units:
   - Filter out dead groups (units <= 0) from both armies
   - Check termination conditions (in order):
     a. If Immune System has 0 units, Infection wins
     b. If Infection has 0 units, Immune System wins
     c. If both are empty (edge case), return tie/stalemate
   - Run target selection phase
   - If no targets selected (all immunities, stalemate), break and return current state
   - Run attack phase and track if any units were killed
   - If 0 units were killed this round (stalemate), break and return current state
2. Determine winner:
   - Count remaining units in each army
   - Return tuple: (winning_army_name, total_units_remaining)
   - If stalemate (both armies have units but can't damage each other), return ("Stalemate", 0)
3. Handle edge cases:
   - **Stalemate detection**: Combat ends if a full round completes with 0 units killed
   - **No valid targets**: Combat ends if no group can select a target (all immune)
   - **One army eliminated**: Standard win condition
   - **Both armies eliminated**: Unlikely but handle as tie

### Step 6: Main Execution Flow

Create a `main()` function:

1. Parse input from "input.md"
2. Run combat simulation
3. Print the total number of units in the winning army

**File structure:**
```python
# Parse input
immune_groups, infection_groups = parse_input("input.md")

# Simulate combat
winner, units_remaining = simulate_combat(immune_groups, infection_groups)

# Output result
print(units_remaining)
```

## Implementation Details

### Parsing Modifiers

The modifiers section is optional and can contain:
- Just weaknesses: `(weak to fire, cold)`
- Just immunities: `(immune to radiation)`
- Both: `(weak to fire; immune to radiation, slashing)`
- Neither: no parentheses at all

**Parsing approach:**
1. Check if parentheses exist in the line
2. Extract content between parentheses
3. Split by semicolon to separate weak/immune sections
4. For each section:
   - If contains "weak to", extract comma-separated types after it
   - If contains "immune to", extract comma-separated types after it
5. Strip whitespace and store in sets

### Tie-Breaking Implementation

Python's `sorted()` with tuple keys handles multi-level sorting:
```python
# Target selection order
groups.sort(key=lambda g: (-g.effective_power(), -g.initiative))

# Attack order
attackers.sort(key=lambda g: -g.initiative)

# Target choice (for max selection)
target = max(valid_targets, key=lambda t: (
    damage_to_target[t],
    t.effective_power(),
    t.initiative
))
```

### Memory and Performance

- **Space complexity**: O(G) for storing groups
- **Time per round**: O(G²) for target selection, O(G log G) for attacking
- **Expected rounds**: Typically 10-100 rounds for inputs of this size
- **Total runtime**: Well under 1 second for this problem size

## Debug Logging (Optional)

For debugging and verification, add optional logging at key points:
- Start of each round: Print round number and alive groups
- Target selection: Print which group targets which
- Each attack: Print attacker, defender, damage dealt, units killed
- End of round: Print total units remaining per army

Implement with a global `DEBUG` flag that can be toggled:
```python
DEBUG = False  # Set to True for detailed logging

def log(message):
    if DEBUG:
        print(message)
```

## Potential Issues and Solutions

1. **Dead groups attacking**: Groups killed earlier in attack phase shouldn't attack
   - Solution: Check `is_alive()` before each attack

2. **Stalemate detection**: If no damage is dealt, combat never ends
   - Solution: Track units killed each round; if 0, terminate combat
   - Also check if no targets can be selected (all immunities)

3. **Integer division**: Ensure proper floor division for unit deaths
   - Solution: Use `//` operator in Python

4. **Empty armies**: Handle case where all groups in one army die
   - Solution: Filter dead groups at start of each round, check for empty armies

5. **Parsing edge cases**: Lines without modifiers
   - Solution: Make parentheses section optional in regex with `(?:...)?`, check for None

6. **Modifier order variations**: Modifiers can be "weak; immune" or "immune; weak"
   - Solution: Parse both sections independently by searching for keywords
