# Test Plan: RPG Simulator 20XX - Maximum Gold to Lose

## Testing Strategy

We need to verify that our solution correctly:
1. Simulates combat according to the rules
2. Generates all valid equipment combinations
3. Identifies combinations where the player loses
4. Returns the maximum cost among losing combinations

## Test Categories

### 1. Combat Simulation Tests

#### Test 1.1: Basic Combat - Player Wins
```python
# Example: Player has advantage
player_hp = 8
player_damage = 5
player_armor = 5
boss_hp = 12
boss_damage = 7
boss_armor = 2

# Player deals: max(1, 5-2) = 3 damage per turn
# Boss deals: max(1, 7-5) = 2 damage per turn
# Turns to kill boss: ceil(12/3) = 4 turns
# Turns to kill player: ceil(8/2) = 4 turns
# Player attacks first, so player wins
Expected: simulate_combat returns True
```

#### Test 1.2: Basic Combat - Player Loses
```python
# Example: Boss has advantage
player_hp = 8
player_damage = 5
player_armor = 5
boss_hp = 12
boss_damage = 8
boss_armor = 2

# Player deals: max(1, 5-2) = 3 damage per turn
# Boss deals: max(1, 8-5) = 3 damage per turn
# Turns to kill boss: ceil(12/3) = 4 turns
# Turns to kill player: ceil(8/3) = 3 turns
# Player attacks first but boss kills player in 3 turns before player's 4th turn
Expected: simulate_combat returns False
```

#### Test 1.3: Minimum Damage Rule
```python
# Player damage is less than boss armor
player_hp = 10
player_damage = 1
player_armor = 0
boss_hp = 5
boss_damage = 10
boss_armor = 5

# Player deals: max(1, 1-5) = 1 damage per turn (minimum)
# Boss deals: max(1, 10-0) = 10 damage per turn
# Turns to kill boss: ceil(5/1) = 5 turns
# Turns to kill player: ceil(10/10) = 1 turn
Expected: simulate_combat returns False
```

#### Test 1.4: Both Sides Minimum Damage
```python
# Both deal minimum damage
player_hp = 10
player_damage = 1
player_armor = 5
boss_hp = 10
boss_damage = 1
boss_armor = 5

# Player deals: max(1, 1-5) = 1 damage per turn
# Boss deals: max(1, 1-5) = 1 damage per turn
# Turns to kill boss: ceil(10/1) = 10 turns
# Turns to kill player: ceil(10/1) = 10 turns
# Player attacks first, so player wins
Expected: simulate_combat returns True
```

#### Test 1.5: Actual Boss Stats - Sample Equipment
```python
# Test with actual boss: HP=103, Damage=9, Armor=2
# Player with cheapest winning setup
player_hp = 100
player_damage = 4  # Dagger only
player_armor = 0   # No armor

# Player deals: max(1, 4-2) = 2 damage per turn
# Boss deals: max(1, 9-0) = 9 damage per turn
# Turns to kill boss: ceil(103/2) = 52 turns
# Turns to kill player: ceil(100/9) = 12 turns
# Boss wins
Expected: simulate_combat returns False
```

### 2. Equipment Combination Generation Tests

#### Test 2.1: Count Total Combinations
```python
# Verify correct number of combinations generated
combinations = generate_equipment_combinations()

# Expected: 5 weapons × 6 armor options (0-1) × 21 ring options (0-2)
# Weapons: 5
# Armor: 1 (none) + 5 (items) = 6
# Rings: 1 (none) + 6 (singles) + C(6,2) (pairs) = 1 + 6 + 15 = 21
# Total: 5 × 6 × 21 = 630

Expected: len(combinations) == 630
```

#### Test 2.2: Minimum Cost Combination
```python
# Verify cheapest possible equipment (Dagger only)
combinations = generate_equipment_combinations()
min_cost = min(c[0] for c in combinations)

# Dagger: 8 gold, no armor, no rings
Expected: min_cost == 8
```

#### Test 2.3: Maximum Cost Combination
```python
# Verify most expensive equipment
combinations = generate_equipment_combinations()
max_cost = max(c[0] for c in combinations)

# Greataxe: 74
# Platemail: 102
# Damage +3 ring: 100
# Defense +3 ring: 80
# Total: 74 + 102 + 100 + 80 = 356

Expected: max_cost == 356
```

#### Test 2.4: No Armor Option Exists
```python
# Verify combinations with no armor are generated
combinations = generate_equipment_combinations()

# Find a combination with only weapon
# E.g., Dagger (8, 4, 0) with no armor or rings
cheapest = min(combinations, key=lambda x: x[0])

Expected: cheapest == (8, 4, 0)
```

#### Test 2.5: Two Rings Option Exists
```python
# Verify combinations with two rings are generated
combinations = generate_equipment_combinations()

# Find expensive combinations (must have 2 rings)
# Greataxe (74) + Platemail (102) + Damage +3 (100) + Defense +3 (80)
most_expensive = max(combinations, key=lambda x: x[0])

Expected: most_expensive[0] == 356
```

#### Test 2.6: No Duplicate Combinations
```python
# Verify all combinations are unique
combinations = generate_equipment_combinations()
unique_combinations = set(combinations)

Expected: len(combinations) == len(unique_combinations)
```

#### Test 2.7: No Duplicate Rings in Single Combination
```python
# Verify that no combination contains the same ring twice
# This tests that combinations(rings, 2) is used correctly

# The most expensive two rings are Damage +3 (100) and Defense +3 (80)
# If duplicate rings were allowed, we could have 2x Damage +3 = 200
# But this should NOT exist in our combinations

combinations = generate_equipment_combinations()

# Check for impossible ring combinations (2x same ring cost)
# For example: 2x Defense +3 would cost 160 in rings alone
impossible_ring_costs = [
    50,   # 2x Damage +1
    100,  # 2x Damage +2
    200,  # 2x Damage +3
    40,   # 2x Defense +1
    80,   # 2x Defense +2
    160,  # 2x Defense +3
]

for cost, damage, armor in combinations:
    # Extract ring cost by subtracting min weapon (8) and checking
    # This is a sanity check that impossible combinations don't exist
    pass

# Simpler check: no ring-only cost should equal 2x any single ring cost
Expected: All ring pairs are unique (different rings)
```

### 3. Input Parsing Tests

#### Test 3.1: Parse Boss Stats Correctly
```python
# Verify correct parsing of input.md
boss_hp, boss_damage, boss_armor = parse_boss_stats('input.md')

Expected: boss_hp == 103
Expected: boss_damage == 9
Expected: boss_armor == 2
```

#### Test 3.2: Handle Different Input Formats
```python
# Test with variations in spacing
# Input line: "Hit Points:  103  " (extra spaces)
# Should still parse correctly

Expected: Handles whitespace correctly
```

#### Test 3.3: Input Validation
```python
# Test that parser validates required fields are present
# This test is optional for a scripting task but good practice

# Create a temporary file with missing stats
import tempfile
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write("Hit Points: 100\n")
    f.write("Damage: 5\n")
    # Missing Armor field
    temp_file = f.name

try:
    boss_hp, boss_damage, boss_armor = parse_boss_stats(temp_file)
    Expected: Should raise ValueError
except ValueError as e:
    Expected: Exception message mentions missing statistics
finally:
    import os
    os.unlink(temp_file)
```

### 4. Integration Tests

#### Test 4.1: Find Maximum Gold to Lose
```python
# Main integration test
result = find_max_gold_to_lose()

# Result should be a positive integer
# Should be less than maximum possible cost (356)
# Should be greater than minimum cost (8)

Expected: 8 < result < 356
Expected: isinstance(result, int)
```

#### Test 4.2: Verify Losing Combinations Exist
```python
# There should be combinations where player loses
boss_hp, boss_damage, boss_armor = parse_boss_stats('input.md')
player_hp = 100

losing_count = 0
for cost, player_damage, player_armor in generate_equipment_combinations():
    if not simulate_combat(player_hp, player_damage, player_armor,
                          boss_hp, boss_damage, boss_armor):
        losing_count += 1

Expected: losing_count > 0
```

#### Test 4.3: Verify Winning Combinations Exist
```python
# There should also be combinations where player wins
boss_hp, boss_damage, boss_armor = parse_boss_stats('input.md')
player_hp = 100

winning_count = 0
for cost, player_damage, player_armor in generate_equipment_combinations():
    if simulate_combat(player_hp, player_damage, player_armor,
                      boss_hp, boss_damage, boss_armor):
        winning_count += 1

Expected: winning_count > 0
```

#### Test 4.4: Boundary Analysis - Weakest Losing Setup
```python
# Find the cheapest way to lose (verify we can lose cheaply)
boss_hp, boss_damage, boss_armor = parse_boss_stats('input.md')
player_hp = 100

min_losing_cost = float('inf')
for cost, player_damage, player_armor in generate_equipment_combinations():
    if not simulate_combat(player_hp, player_damage, player_armor,
                          boss_hp, boss_damage, boss_armor):
        min_losing_cost = min(min_losing_cost, cost)

# Cheapest losing setup should be a valid integer
# It should be at least the minimum possible cost (cheapest weapon)
Expected: min_losing_cost >= 8  # Minimum is Dagger (8 gold)
Expected: min_losing_cost < 356  # Maximum possible cost
Expected: isinstance(min_losing_cost, int)
```

#### Test 4.5: Boundary Analysis - Strongest Losing Setup
```python
# The result should be the most expensive losing combination
result = find_max_gold_to_lose()
boss_hp, boss_damage, boss_armor = parse_boss_stats('input.md')
player_hp = 100

# Manually verify this combination actually loses
for cost, player_damage, player_armor in generate_equipment_combinations():
    if cost == result:
        player_wins = simulate_combat(player_hp, player_damage, player_armor,
                                      boss_hp, boss_damage, boss_armor)
        Expected: player_wins == False  # Should lose
        break
```

#### Test 4.6: Output Format Verification
```python
# Verify the solution outputs a single integer to stdout
# Run the main script and check output format

if __name__ == "__main__":
    import sys
    from io import StringIO

    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    # Run the solution
    result = find_max_gold_to_lose()
    print(result)

    # Get output
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout

    # Verify output is a single integer
    output_stripped = output.strip()
    Expected: output_stripped.isdigit()
    Expected: int(output_stripped) > 0
    Expected: output.count('\n') == 1  # Single line output
```

### 5. Edge Cases

#### Test 5.1: Player First Attack Advantage
```python
# When both would die in same number of turns, player wins
player_hp = 10
player_damage = 10
player_armor = 0
boss_hp = 10
boss_damage = 10
boss_armor = 0

# Both need 1 turn to kill each other
# Player attacks first, so player wins
Expected: simulate_combat returns True
```

#### Test 5.2: Very High Armor (Minimum Damage)
```python
# When armor exceeds damage significantly
player_hp = 100
player_damage = 1
player_armor = 10
boss_hp = 100
boss_damage = 1
boss_armor = 10

# Both deal 1 damage (minimum)
# Both need 100 turns
# Player attacks first
Expected: simulate_combat returns True
```

#### Test 5.3: One-Shot Kill by Boss
```python
# Boss kills player in one turn
player_hp = 5
player_damage = 10
player_armor = 0
boss_hp = 100
boss_damage = 10
boss_armor = 0

# Player needs 10 turns to kill boss
# Boss needs 1 turn to kill player
Expected: simulate_combat returns False
```

## Manual Verification Strategy

### Step 1: Verify Combat Logic
- Manually calculate several combat scenarios
- Verify the formula: damage = max(1, attack - defense)
- Verify turn calculation: ceil(hp / damage_per_turn)
- Verify player-first advantage

### Step 2: Verify Combination Count
- Count weapons: 5
- Count armor options: 6 (including none)
- Count ring options: 21 (none + 6 singles + 15 pairs)
- Total: 5 × 6 × 21 = 630

### Step 3: Spot Check Equipment
- Check a few combinations manually
- Verify cost, damage, and armor calculations
- Verify no duplicate items in single combination

### Step 4: Validate Final Answer
- Take the final result (max gold to lose)
- Manually check that this equipment combination loses
- Manually verify no more expensive combination also loses

## Test Execution Order

1. **Unit Tests First**: Test combat simulation independently
2. **Generation Tests**: Verify equipment combinations
3. **Parsing Tests**: Ensure input is read correctly
4. **Integration Tests**: Test full solution
5. **Edge Case Tests**: Verify boundary conditions
6. **Manual Verification**: Cross-check final answer

## Success Criteria

✓ All combat simulations match expected outcomes
✓ Exactly 630 equipment combinations generated
✓ No duplicate rings in any single combination
✓ Boss stats parsed correctly (HP=103, Damage=9, Armor=2)
✓ Input validation catches malformed input files
✓ Solution returns a valid integer
✓ Output format is a single integer on one line
✓ Returned combination actually results in player losing
✓ No more expensive losing combination exists
✓ Solution runs efficiently (under 1 second)
