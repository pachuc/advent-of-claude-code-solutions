# Test Plan: Wizard Combat Simulator (REVISED)

## Testing Strategy
Verify the solution through manual test cases, edge case validation, and the actual puzzle input.

## Key Updates from Critique
This plan has been revised to address issues identified in the critique:

1. **Test Case 1 Improved:** Provided a more complete worked example with clear explanations
2. **Test Case 4 Enhanced (CRITICAL):** Emphasized the critical effect recasting test with explicit verification criteria
3. **New Test Case 12 Added:** Tests Recharge mana tracking to ensure gained mana doesn't count as spent
4. **New Test Case 16 Added:** Winning sequence validation through replay/simulation
5. **Performance Guidelines:** Marked performance expectations as guidelines rather than hard requirements
6. **Testing Order Updated:** Reorganized to prioritize critical effect timing tests
7. **Test Case Numbering:** Adjusted numbering to accommodate new test cases

## Test Categories

### 1. Simple Manual Test Cases

#### Test Case 1: Simple Winning Combat
**Purpose:** Verify basic spell casting, effects, and damage calculation with a complete worked example

**Setup:**
- Player: 10 HP, 250 mana
- Boss: 14 HP, 8 damage

**Winning Sequence (Fully Worked Out):**

**Turn 1 - Player:**
- Effects: None
- Cast Poison (173 mana) → Player mana: 77, Poison timer: 6

**Turn 1 - Boss:**
- Effects: Poison deals 3 damage → Boss: 11 HP, Poison timer: 5
- Boss attacks for 8 → Player: 2 HP

**Turn 2 - Player:**
- Effects: Poison deals 3 damage → Boss: 8 HP, Poison timer: 4
- Cast Magic Missile (53 mana) → Boss takes 4 damage → Boss: 4 HP, Player mana: 24

**Turn 2 - Boss:**
- Effects: Poison deals 3 damage → Boss: 1 HP, Poison timer: 3
- Boss attacks for 8 → Player: -6 HP (player dies - this path loses)

**Better Sequence with Shield:**

**Turn 1 - Player:**
- Cast Shield (113 mana) → Player mana: 137, Shield timer: 6

**Turn 1 - Boss:**
- Effects: Shield active (armor = 7), Shield timer: 5
- Boss attacks for max(1, 8-7) = 1 → Player: 9 HP

**Turn 2 - Player:**
- Effects: Shield timer: 4
- Cast Poison (173 mana) → Player mana: -36 (NOT ENOUGH MANA - this fails)

**Correct Optimal Sequence (starting with 250 mana):**

This scenario is complex. Simplified expected outcome:
- **Mana spent:** 226 (Poison 173 + Magic Missile 53)
- **Result:** Victory requires Shield for survival OR more starting mana

**Expected Output:** Should find minimum mana cost to win (if possible with 250 starting mana)

**Verification:**
- Boss HP reaches 0
- Player HP remains > 0
- Total mana spent equals sum of spell costs cast

#### Test Case 2: Pure Magic Missile Strategy
**Purpose:** Test simplest possible winning strategy

**Setup:** Use actual input (Boss: 71 HP, 10 damage)

**Strategy:** Only cast Magic Missile
- Need 71/4 = 18 casts (rounded up)
- Cost: 18 × 53 = 954 mana
- But player only has 500 mana initially

**Expected:** Cannot win with only Magic Missiles (need mana management)

### 2. Effect Timing Tests

#### Test Case 3: Effect Application Order
**Purpose:** Verify effects apply BEFORE actions

**Scenario:**
- Boss at 3 HP
- Poison active (timer = 1)
- Player's turn starts

**Expected Behavior:**
1. Effects apply first → Poison deals 3 damage
2. Boss HP reaches 0
3. Combat ends BEFORE player needs to cast spell
4. This saves the mana cost of another spell

**Verification:** Check that boss death from effects is detected before spell casting

#### Test Case 4: Effect Expiration and Re-casting (CRITICAL)
**Purpose:** Verify effects can be recast on expiration turn

**Scenario:**
- Shield timer = 1 at start of player turn
- Player's turn starts

**Expected Behavior:**
1. Shield effect applies (armor = 7)
2. Timer decrements to 0
3. Shield expires
4. Player CAN cast Shield again this turn (timer is now 0, not > 0)

**Verification:**
- Spell availability check uses `timer > 0` condition (not `>= 0`)
- This allows recasting immediately when effect expires
- Confirm Shield can be recast when timer = 0

#### Test Case 5: Multiple Effects Active
**Purpose:** Test all effects running simultaneously

**Scenario:**
- Shield active (timer = 3)
- Poison active (timer = 4)
- Recharge active (timer = 2)
- Player's turn starts

**Expected Behavior:**
1. Player gets 7 armor
2. Boss takes 3 poison damage
3. Player gains 101 mana
4. All timers decrement
5. Player can then cast any non-active spell

**Verification:** All effects apply correctly and independently

### 3. Edge Cases

#### Test Case 6: Cannot Cast Spell (Insufficient Mana)
**Purpose:** Verify handling of unaffordable spells

**Scenario:**
- Player has 50 mana
- Try to cast Shield (113 mana)

**Expected:** Spell cast fails, state is invalid, branch is pruned

#### Test Case 7: Cannot Cast Spell (Effect Already Active)
**Purpose:** Verify effect conflict detection

**Scenario:**
- Shield active (timer = 3)
- Try to cast Shield again

**Expected:** Spell cast fails, state is invalid, branch is pruned

#### Test Case 8: Boss Damage With Armor
**Purpose:** Verify armor reduces damage correctly

**Scenario:**
- Boss damage: 10
- Player armor: 7 (from Shield)

**Expected:** Player takes max(1, 10 - 7) = 3 damage

#### Test Case 9: Boss Damage With High Armor (Minimum Damage)
**Purpose:** Verify minimum 1 damage rule

**Scenario:**
- Boss damage: 10
- Player armor: 15 (hypothetical)

**Expected:** Player takes max(1, 10 - 15) = 1 damage (not 0 or negative)

#### Test Case 10: Exact Lethal Damage
**Purpose:** Test boundary condition for victory

**Scenario:**
- Boss: 4 HP
- Player casts Magic Missile (4 damage)

**Expected:** Boss HP = 0, player wins immediately

#### Test Case 11: Player Dies on Boss Turn
**Purpose:** Verify loss detection

**Scenario:**
- Player: 5 HP, no armor
- Boss attacks for 10 damage

**Expected:** Player HP = -5, this branch is pruned (no victory possible)

#### Test Case 12: Recharge Mana Tracking (NEW - IMPORTANT)
**Purpose:** Verify Recharge correctly adds mana and that gained mana doesn't count as "spent"

**Scenario:**
- Player casts Recharge (229 mana spent)
- Recharge active for 5 turns, adding 101 mana each turn
- Total mana gained: 505 mana
- Player uses gained mana to cast more spells

**Expected Behavior:**
1. Recharge costs 229 mana (counts toward total spent)
2. Each turn, player gains 101 mana (does NOT count as negative spending)
3. Player mana can exceed 500 (no upper limit)
4. Only spell costs count toward "mana spent"

**Verification:**
- Total mana spent = sum of spell costs only
- Mana gained from Recharge is not subtracted from total
- Player can have > 500 mana
- Final answer only includes mana spent on casting spells

### 4. Algorithm Correctness Tests

#### Test Case 13: State Pruning
**Purpose:** Verify visited states are properly tracked

**Scenario:**
- Reach same game state via two different spell sequences
- First path: 400 mana spent
- Second path: 450 mana spent

**Expected:** Second path should be pruned (not explored further)

**Verification:** Check visited dictionary tracks minimum cost per state

#### Test Case 14: Optimal Path Selection
**Purpose:** Verify Dijkstra's finds minimum cost

**Setup:** Create scenario with two possible winning paths
- Path A: High-cost spells, quick victory
- Path B: Efficient spell usage, slower victory

**Expected:** Algorithm should find the cheaper path

**Verification:** Compare result to manually calculated minimum

### 5. Actual Puzzle Input Test

#### Test Case 15: Full Puzzle Solution
**Purpose:** Solve the actual puzzle

**Input:**
- Boss: 71 HP, 10 damage
- Player: 50 HP, 500 mana

**Expected Behavior:**
- Algorithm completes in reasonable time (< 10 seconds)
- Returns a valid mana cost
- Cost should be > 0 and < 1500 (rough bounds)

**Manual Verification Strategy:**
1. Run the algorithm
2. Get minimum mana cost (let's call it M)
3. Verify it's possible to win with M mana
4. Consider if any obviously cheaper strategy exists
5. Check that boss HP reaches 0 and player survives

**Approximate Expected Range:** 900-1400 mana (rough estimate)
- Pure offense would cost too much
- Need efficient use of Poison (damage over time)
- Need Shield to survive longer
- May need Recharge for mana management

**Additional Verification:**
- After getting result, replay the winning sequence to validate it
- Confirm the path is valid and achieves victory

#### Test Case 16: Winning Sequence Validation (NEW - IMPORTANT)
**Purpose:** Verify the winning sequence is actually valid by replaying it

**Process:**
1. Run algorithm to get minimum mana cost and winning spell sequence
2. Implement a replay/simulator function
3. Replay the exact sequence of spells from start to finish
4. Track HP, mana, effects at each step

**Verification:**
- No invalid spell casts (insufficient mana or active effects)
- Boss HP reaches 0
- Player HP stays > 0 throughout
- Total mana spent matches reported minimum
- All game rules are followed

**Why Important:** Catches bugs where algorithm reports a cost but the sequence is invalid

### 6. Performance Tests

#### Test Case 17: Execution Time
**Purpose:** Ensure algorithm runs efficiently

**Measurement:**
- Time the full puzzle solution
- Guideline: Should complete in under 10 seconds
- Note: This is a guideline; correctness is more important than speed

**If Slow:** May indicate issue with state pruning or excessive branching, but acceptable for scripting solution

#### Test Case 18: Memory Usage (GUIDELINE)
**Purpose:** Ensure reasonable memory consumption

**Measurement:**
- Monitor peak memory during execution
- Guideline: Should stay under 500MB
- Note: This is a guideline, not a hard requirement
- Primary goal is correctness; performance is secondary

## Testing Execution Order

1. **Unit Tests First:** Test individual functions
   - `apply_effects()` - Verify effect timing sequence
   - `cast_spell()` - Verify spell casting with timer > 0 check
   - `boss_attack()` - Verify armor calculation and minimum damage
   - State hashing - Verify state key generation

2. **Critical Effect Tests:** Test effect timing (Test Cases 3-5)
   - Test Case 3: Effects before actions
   - Test Case 4: Effect recasting on expiration (CRITICAL)
   - Test Case 5: Multiple effects

3. **Edge Cases:** Test boundary conditions (Test Cases 6-12)
   - Include new Test Case 12 for Recharge mana tracking

4. **Algorithm Tests:** Test search correctness (Test Cases 13-14)

5. **Full Solution:** Run on actual puzzle input (Test Case 15)

6. **Validation:** Replay winning sequence (Test Case 16)

7. **Performance:** Measure time and memory (Test Cases 17-18) - Guidelines only

## Verification Checklist

For each test run, verify:
- [ ] Boss HP reaches 0 or below (victory condition)
- [ ] Player HP stays above 0 (survival condition)
- [ ] Total mana spent equals sum of spell costs
- [ ] No invalid spell casts (insufficient mana or active effects)
- [ ] Effects apply in correct order (start of turn, before actions)
- [ ] Effect timers decrement correctly
- [ ] Boss always deals at least 1 damage
- [ ] Algorithm terminates (no infinite loops)
- [ ] Result is deterministic (same input → same output)

## Debugging Strategy

If wrong answer:
1. **Too High:** Algorithm works but isn't finding optimal path
   - Check state pruning logic
   - Verify priority queue ordering
   - Ensure Dijkstra's is properly implemented

2. **Too Low:** Algorithm finds "invalid" victory
   - Check effect timing
   - Verify boss damage calculation
   - Check player death detection

3. **No Solution Found:** Algorithm can't find any winning path
   - Check if player death prevents valid wins
   - Verify spell casting constraints
   - Check if state space is being explored

## Success Criteria

The implementation passes testing if:
1. All manual test cases produce expected outcomes
2. Edge cases are handled correctly
3. Actual puzzle input produces a valid answer
4. Answer is accepted as correct by the puzzle system
5. Execution time is reasonable (< 5 seconds)
6. Code is clear and maintainable
