# Testing Plan: Immune System Simulator

## Testing Strategy

The testing approach will focus on:
1. **Unit tests**: Individual components (parsing, damage calculation, effective power)
2. **Integration tests**: Combat phases working together
3. **End-to-end tests**: Full combat simulation with known outcomes
4. **Edge case validation**: Boundary conditions and special scenarios

## Test Categories

### Category 1: Parsing Tests

**Test 1.1: Parse group without modifiers**
- Input: `"1017 units each with 10287 hit points with an attack that does 88 cold damage at initiative 1"`
- Expected:
  - units = 1017
  - hit_points = 10287
  - attack_damage = 88
  - attack_type = "cold"
  - initiative = 1
  - weaknesses = empty set
  - immunities = empty set
- Verification: Assert all attributes match expected values

**Test 1.2: Parse group with only weaknesses**
- Input: `"6638 units each with 2292 hit points (weak to radiation) with an attack that does 3 cold damage at initiative 18"`
- Expected:
  - weaknesses = {"radiation"}
  - immunities = empty set
  - Other attributes parsed correctly
- Verification: Check sets contain correct damage types

**Test 1.3: Parse group with only immunities**
- Input: `"3906 units each with 12319 hit points (immune to bludgeoning, cold, fire) with an attack that does 24 cold damage at initiative 14"`
- Expected:
  - weaknesses = empty set
  - immunities = {"bludgeoning", "cold", "fire"}
- Verification: All three immunities present in set

**Test 1.4: Parse group with both weaknesses and immunities**
- Input: `"20 units each with 1333 hit points (immune to radiation, slashing; weak to bludgeoning) with an attack that does 508 fire damage at initiative 3"`
- Expected:
  - weaknesses = {"bludgeoning"}
  - immunities = {"radiation", "slashing"}
- Verification: Both sets populated correctly

**Test 1.4b: Parse group with reversed modifier order**
- Input: `"100 units each with 1000 hit points (weak to fire, cold; immune to slashing) with an attack that does 50 radiation damage at initiative 10"`
- Expected:
  - weaknesses = {"fire", "cold"}
  - immunities = {"slashing"}
- Verification: Parsing works regardless of weak/immune ordering

**Test 1.5: Parse group with multiple weaknesses**
- Input: `"807 units each with 4206 hit points (weak to slashing, bludgeoning) with an attack that does 44 fire damage at initiative 7"`
- Expected:
  - weaknesses = {"slashing", "bludgeoning"}
- Verification: Multiple comma-separated values handled

**Test 1.6: Parse full input file**
- Input: The complete input.md file
- Expected: 10 Immune System groups + 10 Infection groups
- Verification:
  - Count groups in each army
  - Spot-check specific groups for correct attributes:
    - First Immune group: 6638 units, 2292 HP, weak to radiation, 3 cold damage, initiative 18
    - First Infection group: 1756 units, 36633 HP, immune to bludgeoning, 38 bludgeoning damage, initiative 17
    - An Immune group with multiple immunities (line 2): immune to {bludgeoning, cold, fire}
  - Ensure no groups are missing or duplicated

### Category 2: Damage Calculation Tests

**Test 2.1: Normal damage (no modifiers)**
- Attacker: 100 units, 10 damage/unit (effective power = 1000)
- Defender: No immunities or weaknesses to attacker's type
- Expected damage: 1000
- Verification: `calculate_damage_to()` returns 1000

**Test 2.2: Immunity (zero damage)**
- Attacker: 100 units, 10 fire damage/unit
- Defender: Immune to fire
- Expected damage: 0
- Verification: `calculate_damage_to()` returns 0

**Test 2.3: Weakness (double damage)**
- Attacker: 100 units, 10 cold damage/unit (effective power = 1000)
- Defender: Weak to cold
- Expected damage: 2000
- Verification: `calculate_damage_to()` returns 2000

**Test 2.4: Unit death calculation**
- Damage: 1000
- Defender: Units with 100 HP each
- Expected: 10 units killed (1000 // 100)
- Verification: `take_damage()` reduces units by exactly 10

**Test 2.5: Partial damage (not enough to kill a unit)**
- Damage: 50
- Defender: Units with 100 HP each
- Expected: 0 units killed
- Verification: Units count remains unchanged

**Test 2.6: Exact damage (no remainder)**
- Damage: 500
- Defender: 10 units with 50 HP each
- Expected: All 10 units killed
- Verification: Units reduced to 0

### Category 3: Effective Power and Ordering Tests

**Test 3.1: Effective power calculation**
- Group: 100 units, 50 damage/unit
- Expected: 5000
- Verification: `effective_power()` returns 5000

**Test 3.2: Effective power after taking damage**
- Initial: 100 units, 50 damage/unit (EP = 5000)
- Take damage: Kill 30 units
- Expected: 70 units remain, EP = 3500
- Verification: Effective power updates dynamically

**Test 3.3: Target selection ordering (by effective power)**
- Groups with different effective powers
- Expected: Sorted descending by effective power
- Verification: Check order after sorting

**Test 3.4: Target selection tie-breaking (by initiative)**
- Groups with same effective power but different initiatives
- Expected: Higher initiative comes first
- Verification: Group with initiative 20 before initiative 10

**Test 3.5: Attack ordering (by initiative only)**
- Mix of groups from both armies
- Expected: All groups sorted by initiative descending
- Verification: Initiative values in descending order

### Category 4: Target Selection Logic Tests

**Test 4.1: Select target that takes most damage**
- Attacker deals fire damage
- Target A: Takes 1000 damage (normal)
- Target B: Takes 2000 damage (weak to fire)
- Expected: Target B selected
- Verification: `target_selection()` pairs attacker with B

**Test 4.2: No valid targets (all immune)**
- Attacker deals fire damage
- All enemies immune to fire
- Expected: Attacker selects no target
- Verification: Attacker not in targets dictionary

**Test 4.3: Target tie-breaking by effective power**
- Two targets take same damage
- Target A: Effective power 5000
- Target B: Effective power 3000
- Expected: Target A selected
- Verification: Higher effective power chosen

**Test 4.4: Target tie-breaking by initiative**
- Two targets with same damage and effective power
- Target A: Initiative 15
- Target B: Initiative 20
- Expected: Target B selected
- Verification: Higher initiative chosen

**Test 4.5: Each target selected only once**
- Multiple attackers, fewer defenders
- Expected: No defender targeted by two attackers
- Verification: All values in targets dict are unique

**Test 4.6: Lower-priority attacker gets no target**
- 2 attackers, 1 valid defender
- Expected: First attacker (by selection order) gets the target, second gets none
- Verification: Second attacker not in targets dict

### Category 5: Attack Phase Tests

**Test 5.1: Attacks in initiative order**
- Create groups with initiatives: 5, 15, 10, 20
- Expected attack order: 20, 15, 10, 5
- Verification: Log attack order and verify sequence

**Test 5.2: Dead groups don't attack**
- Group A targets Group B
- Group B targets Group A
- Group A has higher initiative and kills B
- Expected: B doesn't attack (already dead)
- Verification: Check that A's units unchanged after B's "turn"

**Test 5.3: Damage calculation updates with current units**
- Setup: 2v2 scenario where attacker gets damaged before attacking
  - Group A (Immune): 100 units, 100 HP, 10 damage, initiative 5
  - Group B (Immune): 50 units, 50 HP, 1 damage, initiative 1
  - Group C (Infection): 50 units, 100 HP, 20 damage, initiative 10
  - Group D (Infection): 10 units, 50 HP, 1 damage, initiative 1
- Round 1 attacks:
  - C attacks A first (initiative 10): deals damage, kills 10 units from A
  - A attacks (initiative 5): should deal damage based on remaining 90 units
- Expected: A's damage reflects current 90 units (900 effective power), not initial 100
- Verification: Damage dealt by A is calculated with updated unit count

**Test 5.4: Multiple rounds of combat**
- Small scenario: 2v2 groups
- Expected: Multiple rounds until one side eliminated
- Verification: Combat continues until win condition met

### Category 6: Combat Simulation Tests

**Test 6.1: Combat ends when one army eliminated**
- Set up scenario where Immune System is much stronger
- Expected: Infection eliminated, combat ends
- Verification: Infection has 0 total units remaining

**Test 6.2: Winning army unit count**
- Run full combat simulation
- Expected: Sum of all winning army's group units
- Verification: Count matches expected total

**Test 6.3: Stalemate detection**
- Setup:
  ```
  Immune System:
  100 units each with 1000 hit points (immune to fire) with an attack that does 50 fire damage at initiative 10

  Infection:
  50 units each with 500 hit points (immune to fire) with an attack that does 100 fire damage at initiative 5
  ```
- Expected: Combat ends immediately (no targets selected as all damage would be 0)
- Verification:
  - Combat terminates without infinite loop
  - Returns stalemate status or current state
  - No units killed

**Test 6.4: All groups in one army die same round**
- Set up scenario where all defenders killed in one round
- Expected: Clean termination, correct winner
- Verification: Winner declared correctly

### Category 7: End-to-End Integration Tests

**Test 7.1: Small custom scenario**
Create a minimal test case:
```
Immune System:
100 units each with 100 hit points with an attack that does 50 fire damage at initiative 10

Infection:
50 units each with 50 hit points (weak to fire) with an attack that does 10 cold damage at initiative 5
```

Expected outcome:
- Round 1 target selection: Both target each other
- Round 1 attacks:
  - Immune group attacks first (initiative 10): deals 5000×2=10000 damage, kills 200 units (all 50 die)
  - Infection already dead, can't attack
- Winner: Immune System with 100 units

Verification:
- Parse correctly
- Run combat
- Immune System wins with 100 units (taking no damage)

**Test 7.2: Actual input file**
- **Important**: Only run this test AFTER validating logic with Test 7.1 and other small examples
- Input: The provided input.md
- Process:
  1. First, ensure all smaller tests pass (especially Test 7.1)
  2. Run simulation on actual input with debug logging enabled
  3. Manually verify first 2-3 rounds make logical sense
  4. Record the final result (winner and unit count)
  5. Use this as regression test for future runs
- Expected: Specific winner and unit count (to be determined by validated first run)
- Verification:
  - Combat terminates within reasonable rounds (< 1000)
  - Result is consistent across multiple runs
  - No errors or exceptions
  - No infinite loops (stalemate detection works)

**Test 7.3: Example from problem description**
- Note: Problem description mentions example with 5216 units for infection
- This appears to be a reference example, not provided input
- If example input is available in problem statement, use it
- Expected: 5216 units for infection (if using problem's example)
- Verification: Output matches exactly
- **If no example input provided**: Skip this test

### Category 8: Edge Case Tests

**Test 8.0: Same damage type for weakness and immunity**
- Setup: Group with both weakness and immunity to fire (invalid but test handling)
- Expected: Implementation should treat immunity as taking precedence (0 damage) OR reject during parsing
- Verification: No crashes, deterministic behavior
- **Note**: This is likely impossible in valid Advent of Code input, but worth considering

**Test 8.1: Single group per army**
- Minimal scenario: 1v1
- Expected: Combat works correctly
- Verification: Proper winner determination

**Test 8.2: Massive damage overkill**
- Attacker deals 1,000,000 damage
- Defender has 10 units with 100 HP (1000 total HP)
- Expected: All 10 units die, no overflow errors
- Verification: Units reduced to exactly 0

**Test 8.3: Group with 1 unit remaining**
- Group reduced to 1 unit
- Expected: Still attacks with reduced effective power
- Verification: Correct damage calculation

**Test 8.4: Zero damage scenarios**
- Attacker deals 0 effective power (shouldn't happen but test defensive code)
- Expected: 0 units killed
- Verification: Defender unchanged

**Test 8.5: All groups have same initiative**
- Multiple groups with initiative 10
- Expected: Deterministic ordering (stable sort)
- Verification: Combat still works, no crashes

**Test 8.6: Very high initiative values**
- Group with initiative 1000
- Expected: Still processed correctly
- Verification: Attack order correct

## Verification Methods

### Method 1: Manual Calculation
For small test scenarios, manually calculate expected outcomes:
1. Compute effective powers
2. Determine target selection order
3. Calculate damage for each attack
4. Verify unit deaths
5. Check final state

### Method 2: Intermediate State Logging
Add debug output to track:
- Round number
- Groups alive at start of round
- Target selections
- Attack sequence
- Damage dealt and units killed
- Armies' total units after each round

Compare logged state against expected progression.

### Method 3: Invariant Checking
After each round, verify:
- Total units only decrease or stay same (never increase)
- Dead groups (units <= 0) are filtered out
- No group targets itself
- No group from same army targeted
- Attack order matches initiative order

### Method 4: Regression Testing
Once the correct answer for input.md is determined:
1. Save the answer
2. Run solution multiple times
3. Verify answer is always the same
4. Any code changes must maintain same output

### Method 5: Property-Based Testing (Optional - Nice to Have)
Check general properties hold for all test cases:
- Combat always terminates within reasonable rounds (< 1000 rounds)
- At end: Winner has units > 0 (unless stalemate)
- At end: Loser has units = 0
- Invariant: Total units across both armies never increases (only decreases or stays same)
- Invariant: Each round, at least one unit must die OR combat must terminate

Implementation: Add assertions in combat loop to check these properties

## Test Execution Order

1. **Phase 1**: Parsing tests (1.1-1.6) - ensure input processing works
2. **Phase 2**: Component tests (2.1-2.6, 3.1-3.5) - verify calculations
3. **Phase 3**: Logic tests (4.1-4.6, 5.1-5.4) - test combat mechanics
4. **Phase 4**: Integration tests (6.1-6.4) - full simulation
5. **Phase 5**: End-to-end tests (7.1-7.3) - validate against known outcomes
6. **Phase 6**: Edge cases (8.1-8.6) - boundary conditions

## Success Criteria

The solution is correct if:
1. ✓ All parsing tests pass (correct data extraction)
2. ✓ All damage calculation tests pass (correct formulas)
3. ✓ All ordering tests pass (correct sorting/selection)
4. ✓ All combat logic tests pass (rules followed correctly)
5. ✓ End-to-end test with actual input produces consistent result
6. ✓ No infinite loops (terminates within reasonable time)
7. ✓ Edge cases handled without crashes
8. ✓ If reference answer available, output matches exactly

## Debugging Strategy

If tests fail:
1. **Parsing failures**: Print parsed group attributes, check regex
2. **Wrong damage**: Log damage calculations with intermediate values
3. **Wrong targets**: Print selection order, available targets, damage to each
4. **Wrong attack order**: Print initiative values and sort keys
5. **Infinite loop**: Add max rounds limit, print round counter
6. **Wrong answer**: Enable full combat logging, trace through manually
