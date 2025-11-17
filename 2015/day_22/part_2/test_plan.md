# Test Plan: Wizard Simulator 20XX - Hard Mode

## Plan Updates (v2)

**Key improvements based on critique:**
1. ✓ Added explicit test for turn operation ordering (hard mode penalty → effects → spell)
2. ✓ Added detailed test case for effect re-casting on expiration turn
3. ✓ Replaced Part 1 comparison with state deduplication verification test
4. ✓ Added concrete test cases with expected outputs (3 simple boss scenarios)
5. ✓ Marked path reconstruction test as optional with implementation alternatives
6. ✓ Added failure criteria for performance testing
7. ✓ Clarified test methodology - scripting approach, not production testing
8. ✓ Added specific test case for impossible scenario
9. ✓ Updated success criteria with minimum vs recommended tests

## Testing Strategy

The solution requires verification of:
1. Correct game mechanics implementation (hard mode, effects, turn order)
2. Optimal path finding (minimum mana)
3. Edge cases and boundary conditions

## Test Categories

### Category 1: Game Mechanics Validation

#### Test 1.1: Hard Mode Penalty Application
**Purpose:** Verify player loses 1 HP at start of each player turn

**Test approach:**
- Manually trace through a simple spell sequence
- Verify player HP decreases by 1 at start of each player turn (before effects)
- Confirm death if hard mode penalty brings HP to 0

**Expected behavior:**
- Starting at 50 HP, after N player turns (before boss damage), HP should be (50 - N)
- If HP would go to 0 or below from penalty, player loses

#### Test 1.2: Effect Application Order and Turn Sequence
**Purpose:** Verify effects apply at correct time in turn sequence and verify exact order of operations

**Test approach for Player Turn:**
1. Set up: Player at 2 HP, no active effects
2. Start player turn
3. Verify order: Hard mode penalty (→1 HP) happens BEFORE effects apply
4. Player should be at 1 HP and still alive to cast spell

**Test approach for Player Turn with Recharge:**
1. Set up: Player at 1 HP, Recharge active (timer=1)
2. Start player turn
3. Verify: Hard mode penalty (→0 HP) happens BEFORE Recharge grants mana
4. Player should die immediately (before Recharge effect)

**Test approach for Boss Turn:**
1. Cast Poison and verify it applies at start of boss turn
2. Cast Recharge and verify mana is granted at start of boss turn
3. Cast Shield and verify armor is active during boss attacks (later in boss turn)

**Critical Order Validation:**
- **Player Turn:** Hard mode penalty → Effects apply → Check deaths → Cast spell → Check deaths
- **Boss Turn:** Effects apply → Check deaths → Boss attacks → Check deaths
- Poison should deal 3 damage to boss at start of each turn
- Recharge should grant 101 mana at start of each turn
- Shield should provide 7 armor (checked during boss attack calculation)
- Effects should decrement and expire correctly

#### Test 1.3: Effect Duration and Expiration
**Purpose:** Verify effect timers work correctly

**Test approach:**
- Cast Shield (duration 6) and track when it expires
- Cast Poison (duration 6) and verify it deals damage for exactly 6 turns
- Cast Recharge (duration 5) and verify mana gain for exactly 5 turns
- Verify cannot cast effect spell while effect is still active
- Verify CAN cast effect spell on the same turn it expires

**Expected behavior:**
- Shield: Timer starts at 6, applies 6 times (on turns where timer is 6,5,4,3,2,1), expires after timer reaches 0
- Poison: Timer starts at 6, deals damage 6 times, expires after 6 applications
- Recharge: Timer starts at 5, grants mana 5 times
- Effect with timer=1 applies one more time then timer decrements to 0 (effect removed)

**Critical Test Case - Re-casting on Expiration Turn:**
1. Turn 1: Cast Shield (timer=6)
2. Turn 2: Shield applies (timer becomes 5 after), cannot cast Shield
3. Turn 3: Shield applies (timer becomes 4 after), cannot cast Shield
4. Turn 4: Shield applies (timer becomes 3 after), cannot cast Shield
5. Turn 5: Shield applies (timer becomes 2 after), cannot cast Shield
6. Turn 6: Shield applies (timer becomes 1 after), cannot cast Shield
7. Turn 7: Shield applies (timer becomes 0 after, effect expires), CAN cast Shield this same turn
8. Verify Shield can be cast on turn 7 after the previous Shield expires

**Validation:**
- Effect is "active" (cannot cast) if timer > 0 before effect application
- Effect is "expired" (can cast) if timer = 0 after effect application
- Same-turn re-casting is allowed and important for optimal strategies

#### Test 1.4: Spell Casting Restrictions
**Purpose:** Verify spell casting validation

**Test approach:**
- Try casting spell without enough mana -> should not be allowed
- Try casting Shield while Shield active -> should not be allowed
- Try casting Poison while Poison active -> should not be allowed
- Try casting same effect on turn it expires -> should be allowed

#### Test 1.5: Boss Damage Calculation
**Purpose:** Verify boss damage respects armor and minimum damage rule

**Test approach:**
- Boss attacks without Shield: damage should be 10
- Boss attacks with Shield (7 armor): damage should be max(1, 10-7) = 3
- If boss damage would be 0 or negative: damage should be 1

### Category 2: Algorithm Correctness

#### Test 2.1: Simple Victory Path
**Purpose:** Verify algorithm can find a basic winning sequence

**Test Case 1: Simple Boss**
- Input: Boss HP: 20, Boss Damage: 5
- Expected strategy: Magic Missile spam (most straightforward)
- Calculation: 20 HP / 4 damage per missile = 5 casts = 265 mana
- Verify algorithm finds 265 mana or better

**Test Case 2: Very Weak Boss**
- Input: Boss HP: 8, Boss Damage: 3
- Expected strategy: 2× Magic Missile (4+4 = 8 damage)
- Expected mana: 2 × 53 = 106 mana
- Verify algorithm outputs exactly 106

**Test Case 3: Poison-Favorable Boss**
- Input: Boss HP: 18, Boss Damage: 3
- Expected strategy: Cast Poison once (deals 18 damage over 6 turns)
- Expected mana: 173 mana
- Player needs to survive 3 boss turns (hard mode penalty = 3 HP, boss damage ≈ 9 HP)
- With 50 starting HP, this is feasible
- Verify algorithm finds 173 mana or proves survival requires Shield

#### Test 2.2: Effect-Based Strategy Validation
**Purpose:** Verify algorithm considers effect spells when optimal

**Test approach:**
- For the given boss (HP: 71, Damage: 10), Poison is likely efficient
- Poison: 173 mana for 18 total damage (3 * 6 turns) = 9.6 mana per damage
- Magic Missile: 53 mana for 4 damage = 13.25 mana per damage
- Shield reduces damage taken by 7, effectively "saving" HP
- Recharge costs 229 but grants 505 mana (net gain: 276 mana)

**Validation:**
- Solution should use efficient spells (Poison, possibly Recharge+Shield)
- Can verify by adding logging to see which spells are cast in optimal path

#### Test 2.3: State Deduplication Verification
**Purpose:** Verify visited set prevents redundant state exploration

**Test approach:**
- Add logging to count total states explored vs unique states
- Verify same game configuration reached via different paths is only explored once
- Check that states with different turns (player vs boss) are treated as distinct

**Example scenario:**
- State A: Player HP=40, Mana=400, Boss HP=50, no effects, player turn
- Reach state A through path 1 (cast Drain twice)
- Reach state A through path 2 (cast Magic Missile + different spell)
- Verify only the first occurrence (with lower mana spent) is explored

**Validation:**
- Log visited set size at completion
- For given input, should be tens of thousands, not millions
- Verify no infinite loops occur

### Category 3: Edge Cases and Boundary Conditions

#### Test 3.1: Immediate Death Scenarios
**Purpose:** Handle cases where player cannot win

**Test approach:**
- Boss with extremely high damage (e.g., 50) and moderate HP
- Hard mode penalty + boss damage may kill player too quickly
- Verify algorithm correctly identifies no winning path and returns None

**Test Case:**
- Input: Boss HP: 50, Boss Damage: 50
- Expected: No winning strategy exists (boss one-shots player)
- Algorithm should return None (or handle gracefully)
- Verify doesn't run indefinitely or crash

**Note:** With given input (Boss Damage: 10), player should be able to win with correct strategy.

#### Test 3.2: Boss Death from Effects vs Spells
**Purpose:** Verify boss death detection at correct times

**Test approach:**
- Set up scenario where boss has 3 HP and Poison is active
- Boss should die from Poison effect, not from spell
- Verify victory is detected after effects apply

**Validation:**
- Check boss HP after effect application
- Victory should be detected before spell casting if boss dies from effects

#### Test 3.3: Player Death from Hard Mode Penalty
**Purpose:** Verify player can die from hard mode penalty alone

**Test approach:**
- Trace a path where player survives boss attacks but dies from penalty
- If player has 1 HP at start of player turn, hard mode penalty kills player
- Verify loss is detected immediately after penalty application

#### Test 3.4: Mana Management with Recharge
**Purpose:** Verify mana tracking with Recharge effects

**Test approach:**
- Cast Recharge and track mana changes
- Verify mana spent only counts spell costs, not Recharge gains
- A spell sequence costing 400 mana but including Recharge should count full 400, not adjusted for mana gain

**Expected behavior:**
- mana_spent tracks cumulative spell costs
- Recharge increases available mana but doesn't decrease mana_spent

#### Test 3.5: Maximum Spell Efficiency
**Purpose:** Verify algorithm doesn't waste mana

**Test approach:**
- Check that optimal solution doesn't:
  - Cast Shield when already active
  - Cast Poison when already active
  - Cast Recharge when already active
  - Cast unnecessary healing (Drain) when at full HP
  - Overkill boss with expensive spells

**Validation:**
- Add assertions or logging to verify spell casting rules are followed
- No duplicate active effects

### Category 4: Solution Verification for Given Input

#### Test 4.1: Validate Against Known Answer
**Purpose:** Verify solution produces correct result for given input

**Given Input:**
- Boss HP: 71
- Boss Damage: 10
- Player HP: 50
- Player Mana: 500
- Hard Mode: Yes

**Test approach:**
1. Run algorithm with given input
2. Record minimum mana output
3. Manually verify the solution makes sense:
   - Boss must take 71 damage from spells/poison
   - Player must survive boss attacks and hard mode penalties
   - Total mana spent should be reasonable (likely 900-1500 range)

**Manual estimation:**
- Poison deals 18 damage for 173 mana (efficient)
- Need ~71 damage total
- Could use: 2 Poison (36 damage, 346 mana) + additional spells for 35 damage
- Magic Missile for 35 damage: 9 casts = 477 mana
- Rough estimate: ~800-1000 mana minimum
- Shield may be needed for survival: +113 mana
- Recharge may be optimal for mana efficiency: +229 cost, +505 mana gain

#### Test 4.2: Trace Optimal Path (Optional Enhancement)
**Purpose:** Understand and verify the optimal spell sequence

**Test approach:**
1. OPTIONAL: Modify algorithm to track and output the spell sequence for optimal path
2. Manually simulate the battle with that sequence
3. Verify:
   - Player doesn't die
   - Boss dies
   - Total mana matches algorithm output
   - No illegal moves (casting effects while active)

**Implementation Options:**
- Option A: Add parent tracking in search algorithm (store state → (parent_state, spell_used) mapping)
- Option B: Add detailed logging during search to trace which path leads to optimal solution
- Option C: Manually verify with a reasonable spell sequence (calculate if it works)

**Note:** This test is optional for correctness but very helpful for debugging and confidence

### Category 5: Performance Testing

#### Test 5.1: Runtime Verification
**Purpose:** Ensure algorithm completes in reasonable time

**Test approach:**
- Time the algorithm execution
- Should complete in under 5 seconds (ideally under 1 second)

**Expected:** Sub-second runtime for given input size

**Failure Action:**
- If runtime exceeds 5 seconds, investigate:
  - State space explosion (check visited set size)
  - Inefficient state hashing
  - Missing visited set checks (infinite loops)
- If runtime is 1-5 seconds, acceptable but could optimize
- If runtime is <1 second, excellent performance

#### Test 5.2: State Space Analysis
**Purpose:** Understand how many states are explored

**Test approach:**
- Count number of states added to visited set
- Count number of states processed from priority queue
- Verify state space is manageable (< 1 million states)

**Validation:**
- Log visited set size at completion
- Should be in tens of thousands range

## Testing Execution Order

**Note on Test Methodology:**
Given this is a scripting task (not production code), tests will primarily be:
- Running the complete algorithm with different inputs
- Manual verification of outputs
- Strategic use of print statements for debugging
- Optional: Simple unit tests for critical functions if bugs are encountered

1. **Phase 1 - Basic Functionality:** Test with simple cases
   - Test Case: Boss HP=8, Damage=3 (expect 106 mana)
   - Test Case: Boss HP=20, Damage=5 (expect ~265 mana)
   - Verify algorithm completes and produces numeric output
   - Add debug logging if results seem wrong

2. **Phase 2 - Mechanics Validation:** Test specific game rules
   - Run simple scenarios and add logging to verify:
     - Hard mode penalty applies first on player turns
     - Effects apply at correct times
     - Effect timers decrement correctly
     - Boss damage calculation respects armor
   - Manual trace through a short game sequence

3. **Phase 3 - Given Input Test:** Run with actual problem input
   - Input: Boss HP=71, Damage=10
   - Verify output is reasonable (estimated 900-1500 range)
   - Check performance (should complete in <5 seconds)
   - Log visited state count

4. **Phase 4 - Edge Case Validation:** Test boundary conditions
   - Test: Boss HP=18, Damage=3 (Poison-optimal scenario)
   - Test: Impossible scenario (Boss Damage=50)
   - Test: Effect re-casting validation
   - Verify no crashes or infinite loops

## Success Criteria

The solution is considered correct if:
1. ✓ Produces a numeric answer for the given input (Boss HP=71, Damage=10)
2. ✓ Answer is logically reasonable (estimated range: 900-1500 mana)
3. ✓ Simple test cases produce correct/reasonable answers
4. ✓ All spell casting rules are followed (no casting effects while active)
5. ✓ Hard mode penalty is correctly applied (1 HP loss at start of player turns, before effects)
6. ✓ Effects work as specified (correct duration, correct timing)
7. ✓ Algorithm completes in reasonable time (< 5 seconds, ideally < 1 second)
8. ✓ No crashes, infinite loops, or illegal game states
9. ✓ Handles edge cases gracefully (impossible scenarios return None)

**Minimum Required Tests:**
- At least 2 simple boss scenarios with expected answers
- Main input (Boss HP=71, Damage=10)
- Performance check (runtime measurement)

**Recommended Additional Tests:**
- Hard mode penalty timing verification
- Effect expiration and re-casting
- State deduplication verification

## Debugging Strategies

If tests fail:
1. **Add detailed logging:** Log every state transition, spell cast, effect application
2. **Trace specific paths:** Follow priority queue to see which paths are explored first
3. **Verify state hashing:** Ensure visited set prevents infinite loops
4. **Check arithmetic:** Verify damage calculations, mana costs, effect durations
5. **Simplify problem:** Test with reduced boss HP/damage to find minimal failing case
