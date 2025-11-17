# Testing Plan: RPG Combat Optimization

## Testing Strategy

Given this is a script to solve a specific problem (not production code), we need to focus on:
1. Verifying the combat simulation logic is correct
2. Ensuring all equipment combinations are properly generated
3. Validating the optimization finds the true minimum
4. Confirming edge cases in combat mechanics are handled

## Test Categories

### 1. Unit Tests - Combat Simulation

**Test 1.1: Basic Combat - Player Wins**
- Player: 8 HP, 5 damage, 5 armor
- Boss: 12 HP, 7 damage, 2 armor
- Expected: Player wins
- Calculation:
  - Player deals: max(1, 5-2) = 3 damage/turn → 4 turns to kill boss
  - Boss deals: max(1, 7-5) = 2 damage/turn → 4 turns to kill player
  - Player attacks first → Player wins (tie goes to player)

**Test 1.2: Basic Combat - Player Loses**
- Player: 8 HP, 5 damage, 5 armor
- Boss: 12 HP, 7 damage, 3 armor
- Expected: Player loses
- Calculation:
  - Player deals: max(1, 5-3) = 2 damage/turn → 6 turns to kill boss
  - Boss deals: max(1, 7-5) = 2 damage/turn → 4 turns to kill player
  - Boss kills player first → Player loses

**Test 1.3: Minimum Damage Rule (High Armor)**
- Player: 10 HP, 3 damage, 0 armor
- Boss: 10 HP, 2 damage, 5 armor
- Expected: Player loses
- Calculation:
  - Player deals: max(1, 3-5) = max(1, -2) = 1 damage/turn → 10 turns to kill boss
  - Boss deals: max(1, 2-0) = 2 damage/turn → 5 turns to kill player
  - Boss kills player first → Player loses (verifies minimum damage rule doesn't save player from overwhelming defense disadvantage)

**Test 1.4: Armor Exceeds Damage - Both Sides**
- Player: 100 HP, 1 damage, 10 armor
- Boss: 100 HP, 1 damage, 10 armor
- Expected: Player wins (eventually, due to first-move advantage)
- Calculation:
  - Both deal 1 damage/turn → 100 turns each
  - Player attacks first → Player wins

**Test 1.5: One-Shot Victory**
- Player: 10 HP, 100 damage, 0 armor
- Boss: 50 HP, 50 damage, 0 armor
- Expected: Player wins in 1 turn
- Calculation:
  - Player deals: 100 damage → 1 turn to kill
  - Boss never gets to attack

**Test 1.6: Equal Stats - First Move Advantage**
- Player: 50 HP, 5 damage, 2 armor
- Boss: 50 HP, 5 damage, 2 armor
- Expected: Player wins
- Calculation:
  - Both deal: max(1, 5-2) = 3 damage/turn
  - Both take: ceil(50/3) = 17 turns to kill opponent
  - Turns are equal, but player attacks first → Player wins

### 2. Unit Tests - Equipment Combination Generation

**Test 2.1: Count Total Combinations**
- Expected: 660 total valid loadouts
- Calculation: 5 weapons × 6 armor options (0 or 1 of 5) × 22 ring options
  - Ring options: 1 (none) + 6 (single) + 15 (pairs) = 22
- Breakdown verification:
  - Loadouts with no armor: 5 weapons × 22 ring combos = 110
  - Loadouts with armor: 5 weapons × 5 armor pieces × 22 ring combos = 550
  - Total: 110 + 550 = 660 ✓

**Test 2.2: Weapon Requirement**
- Verify: Every generated loadout contains exactly 1 weapon
- Method: Check that each loadout has exactly one item from weapons list

**Test 2.3: Armor Optionality**
- Verify: Each loadout has 0 or 1 armor piece
- Method: Check that each loadout has 0 or 1 item from armor list

**Test 2.4: Ring Constraints**
- Verify: Each loadout has 0, 1, or 2 rings
- Verify: No duplicate rings in any loadout
- Method: Check ring count and uniqueness in each loadout

**Test 2.5: No Duplicate Items**
- Verify: Each equipment piece appears at most once per loadout
- Method: Check that all items in a loadout are unique

### 3. Integration Tests - Stats Calculation

**Test 3.1: Single Weapon Only**
- Loadout: [Dagger (8g, 4dmg, 0arm)]
- Expected: cost=8, damage=4, armor=0

**Test 3.2: Weapon + Armor**
- Loadout: [Dagger (8g, 4dmg, 0arm), Leather (13g, 0dmg, 1arm)]
- Expected: cost=21, damage=4, armor=1

**Test 3.3: Weapon + Two Rings**
- Loadout: [Dagger (8g, 4dmg, 0arm), Damage+1 (25g, 1dmg, 0arm), Defense+1 (20g, 0dmg, 1arm)]
- Expected: cost=53, damage=5, armor=1

**Test 3.4: Full Loadout**
- Loadout: [Greataxe (74g, 8dmg, 0arm), Platemail (102g, 0dmg, 5arm), Damage+3 (100g, 3dmg, 0arm), Defense+3 (80g, 0dmg, 3arm)]
- Expected: cost=356, damage=11, armor=8

### 4. Integration Tests - Complete Optimization

**Test 4.1: Simple Manual Verification**
- Create a mini-problem with reduced shop:
  - Weapons: Dagger (8g, 4dmg), Sword (20g, 6dmg)
  - Armor: None or Leather (10g, 1arm)
  - Rings: None
  - Boss: 10 HP, 3 damage, 0 armor
- Manually determine minimum:
  - Player has 100 HP base
  - Dagger only: 4 dmg, 0 arm → deals 4/turn, takes 3/turn → wins, cost=8
  - Dagger + Leather: 4 dmg, 1 arm → deals 4/turn, takes 2/turn → wins, cost=18
  - Minimum should be 8 (Dagger only)

**Test 4.2: Verify Against Problem Example (Actual Input)**
- Use the actual boss stats: 103 HP, 9 damage, 2 armor
- Run the complete algorithm to get minimum cost
- Verification steps:
  1. Identify the specific equipment combination that produces this cost
  2. Calculate player stats from this loadout
  3. Manually simulate combat to verify player wins
  4. Test at least 3 loadouts costing 1-3 gold less to verify they all lose
  5. Ensure no winning loadout exists with lower cost

### 5. Edge Cases

**Test 5.1: Boss with 0 Armor**
- Verify: Algorithm handles boss armor = 0 correctly
- Check: No issues with damage calculation

**Test 5.2: Boss with Very High Armor**
- Boss: 100 HP, 5 damage, 20 armor
- Verify: Minimum damage of 1 is applied correctly
- Player needs enough damage to overcome armor

**Test 5.3: Boss with 1 HP**
- Boss: 1 HP, 10 damage, 0 armor
- Verify: Player should win with cheapest weapon (Dagger - 8g)
- Even with low damage, one hit kills

**Test 5.4: Maximum Cost Loadout**
- Verify the most expensive loadout is calculated correctly
- Greataxe (74) + Platemail (102) + Damage+3 (100) + Defense+3 (80) = 356 gold

**Test 5.5: Minimum Cost Loadout**
- Verify the cheapest possible loadout
- Dagger (8) only = 8 gold

### 6. Input Parsing Tests

**Test 6.1: Standard Format**
- Input:
  ```
  Hit Points: 103
  Damage: 9
  Armor: 2
  ```
- Expected: `{'hit_points': 103, 'damage': 9, 'armor': 2}`

**Test 6.2: Different Ordering**
- Input:
  ```
  Armor: 2
  Hit Points: 103
  Damage: 9
  ```
- Expected: Should still parse correctly (order-independent)

**Test 6.3: Extra Whitespace**
- Input with extra spaces/tabs
- Expected: Should handle gracefully

**Note**: Testing malformed input is not critical for this script since the input format is known and fixed.

## Testing Execution Plan

### Phase 1: Unit Test - Combat Simulation
1. Implement the `player_wins()` function
2. Test with Tests 1.1 - 1.6 using hardcoded player/boss stats
3. Verify output matches expected win/loss results for each test
4. Debug any discrepancies in combat logic (especially minimum damage and first-move advantage)

### Phase 2: Unit Test - Combination Generation
1. Implement ring combination generator
2. Verify it produces exactly 22 combinations (1 + 6 + 15)
3. Implement full loadout generator
4. Count total combinations (should be exactly 660)
5. Verify breakdown: 110 without armor, 550 with armor
6. Sample 10-20 random loadouts and manually verify constraints (1 weapon, 0-1 armor, 0-2 unique rings)

### Phase 3: Unit Test - Stats Calculation
1. Implement `calculate_stats()` function
2. Test with Tests 3.1 - 3.4
3. Verify cost, damage, and armor sums are correct for each test case

### Phase 4: End-to-End Testing with Actual Input
1. Run complete algorithm on actual input (Boss: 103 HP, 9 damage, 2 armor)
2. Record the minimum cost result
3. Output the winning loadout details (enable debug output)
4. Manually verify the winning loadout:
   - Confirm the equipment combination costs exactly this amount
   - Calculate player stats: 100 HP + loadout damage + loadout armor
   - Manually calculate combat: turns to kill boss, turns for boss to kill player
   - Verify player wins (player turns <= boss turns)
5. Test verification of minimum:
   - Identify 3-5 loadouts that cost 1-3 gold less
   - Verify each one results in a player loss
   - Confirm no winning loadout exists with lower cost

### Phase 5: Edge Cases
1. Test edge case scenarios (Tests 5.1-5.5) by modifying boss stats
2. Verify algorithm handles extreme cases without crashes
3. Ensure no infinite loops or errors occur

### Phase 6: Performance Testing
1. Time the execution of the complete algorithm
2. Verify it completes in under 1 second
3. Expected: ~660 combinations × O(1) combat simulation = effectively instant

## Validation Approach for Final Answer

To validate the final answer is correct:

1. **Identify the loadout**: Determine which equipment combination costs the minimum gold
2. **Calculate final stats**:
   - Player: 100 HP + equipment damage + equipment armor
   - Boss: 103 HP, 9 damage, 2 armor
3. **Simulate combat manually**:
   - Player damage per turn = max(1, player_damage - 2)
   - Boss damage per turn = max(1, 9 - player_armor)
   - Calculate turns to kill each other
   - Verify player wins
4. **Verify no cheaper option exists**:
   - Try a few loadouts costing 1 less gold
   - Verify they all lose the combat

## Expected Output Format

The program should output a single integer representing minimum gold cost.

Example: If minimum cost is 78, output should be:
```
78
```

## Additional Test: Verify Minimum Among All Winners

**Test 7.1: Ensure True Minimum**
- Collect all winning loadouts and their costs
- Verify the returned cost is the minimum among all winning costs
- This ensures we're not just finding A winning loadout, but THE minimum-cost winner

**Implementation for testing**:
```python
# During testing, modify find_minimum_cost to track all winners
all_winning_costs = []
for loadout in generate_loadouts(...):
    if player_wins(...):
        all_winning_costs.append(cost)

assert min_cost == min(all_winning_costs)
```

## Success Criteria

- All combat simulation unit tests pass (Tests 1.1-1.6)
- Combination count equals exactly 660
- Combination breakdown: 110 without armor + 550 with armor
- Manual verification of final answer confirms player victory
- At least 3 loadouts costing less than the answer result in defeat
- No winning loadout exists with cost less than the answer
- Program runs in under 1 second
- Output is a single integer (the minimum gold cost)

## Debugging Strategy

If the answer is incorrect:
1. Enable debug output to show the winning loadout details
2. Print all winning loadouts sorted by cost (first 10-20)
3. Manually verify the cheapest 3-5 winning loadouts
4. Check if any expected winning combinations are missing from generation
5. Verify combat simulation with manual calculation for edge cases
6. Ensure minimum damage rule (max(1, damage - armor)) is applied correctly
7. Confirm player-first advantage is implemented (use <= not < for turn comparison)
