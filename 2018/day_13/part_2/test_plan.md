# Test Plan - Part 2: Last Cart Standing

## Testing Strategy

We need to verify that:
1. Carts are correctly removed when they collide
2. Simulation continues after collisions
3. The last remaining cart is correctly identified
4. **Multi-cart pile-ups (3+ carts at same position) are handled correctly** - CRITICAL
5. collision_positions tracking mechanism works as intended
6. Edge cases are handled properly (zero carts remaining, etc.)

## Key Testing Focus

The **most critical test** is verifying that multi-cart pile-ups are handled correctly. This is where the collision_positions set mechanism is essential:

- If Cart A and B collide at (5,5), and Cart C later moves to (5,5) in the same tick, Cart C must also be removed
- This requires the collision_positions set to track collision locations per tick
- Without this mechanism, Cart C would incorrectly survive

## Test Categories

### 1. Basic Functionality Tests

#### Test 1.1: Simple Two-Cart Removal
**Setup:**
- Create minimal track with 3 carts
- Arrange so 2 carts collide first, leaving 1

**Expected Behavior:**
- First collision removes 2 carts
- Third cart continues alone
- Returns position of third cart

**Verification:**
- Check that collision removes exactly 2 carts
- Check that remaining cart's position is returned correctly

#### Test 1.2: Multiple Sequential Collisions
**Setup:**
- Start with 5 carts
- Arrange collisions to occur sequentially

**Expected Behavior:**
- Each collision removes 2 carts
- Simulation continues after each collision
- Last cart position is returned

**Verification:**
- Count cart removals (should have 2 collisions, removing 4 carts total)
- Verify 1 cart remains

### 2. Edge Case Tests

#### Test 2.1: Multi-Cart Pile-Up (3+ carts)
**Setup:**
- Three carts arranged to all reach same position in one tick
- Example: Cart A at (4,5) moving right, Cart B at (5,5) not moved yet, Cart C at (6,5) moving left
- Sequence: A moves to (5,5), collides with B, both removed and position marked. C moves to (5,5), should also be removed

**Expected Behavior:**
- All three carts should be removed
- Position (5,5) should be in collision_positions set after tick
- If there's a 4th cart, it should remain

**Verification:**
- Check that all three carts involved are marked as removed
- Verify collision_positions set contains (5,5)
- Verify simulation handles this without error
- Verify 4th cart (if present) is still active

**Critical Test:** This verifies the collision_positions tracking mechanism works correctly

#### Test 2.2: Cart Collision Order Matters
**Setup:**
- Cart A at (3,5) moving right
- Cart B at (5,5) moving left
- Cart C at (6,5) moving left
- When A and B collide at (4,5), C should still move

**Expected Behavior:**
- A and B collide and are removed
- C continues moving (doesn't collide with removed carts)
- C should be the last cart standing

**Verification:**
- Verify A and B are removed after collision
- Verify C continues to move in subsequent ticks
- Verify C's final position is correct

#### Test 2.3: All Carts Collide (Zero Remaining)
**Setup:**
- Even number of carts that all pair off and collide
- Example: 6 carts → 3 simultaneous collisions → 0 remaining

**Expected Behavior:**
- All carts should be removed
- Should raise Exception("No carts remaining!")
- Should NOT infinite loop or crash

**Verification:**
- Verify exception is raised with correct message
- Verify all carts are marked as removed
- Verify no silent failure or unexpected behavior
- Test that exception is catchable and has clear message

**Important:** This tests defensive programming for edge case that may not occur in real input

#### Test 2.4: Last Two Carts Collide
**Setup:**
- Arrange scenario where exactly 2 carts remain
- These 2 carts collide

**Expected Behavior:**
- Both removed
- Should raise Exception("No carts remaining!")
- No carts remain (error condition)

**Verification:**
- Should detect this edge case gracefully
- Should raise exception with clear message
- Should not crash or infinite loop
- Verify exception type and message are correct

### 3. Correctness Tests with Real Input

#### Test 3.1: Parse Input Correctly
**Verification Steps:**
1. Read `input.md`
2. Count number of initial carts (should be > 2)
3. Verify track dimensions are reasonable (~150x150)
4. Check that cart characters are replaced with track underneath

**Pass Criteria:**
- No parsing errors
- Cart count matches visual inspection
- All carts have valid positions and directions

#### Test 3.2: Movement Mechanics
**Verification:**
- Run simulation for 10 ticks without collision checking
- Verify carts follow track correctly
- Check intersection turning (left, straight, right pattern)
- Verify curve handling (/ and \)

**Pass Criteria:**
- No carts go off-track
- Intersection counters increment correctly
- Directions update properly on curves

#### Test 3.3: Full Simulation
**Verification:**
1. Run full simulation on real input
2. Track number of collisions that occur
3. Verify exactly 1 cart remains
4. Check final position is on valid track

**Pass Criteria:**
- Simulation completes (doesn't infinite loop)
- Returns coordinates in `X,Y` format
- Coordinates are within track bounds
- Position is on a valid track piece

#### Test 3.4: Collision Detection Accuracy
**Instrumentation:**
- Add debug output to log each collision
- Log: tick number, carts involved, position, whether it's a pile-up

**Verification:**
- Collisions only occur when carts are at same (x,y)
- Both carts are immediately marked as removed
- No removed cart moves in subsequent iterations
- Pile-ups (3+ carts at same position) are detected correctly
- collision_positions set correctly tracks collision locations per tick

**Pass Criteria:**
- Collision positions are all valid
- Total carts removed = initial_carts - 1 (assuming 1 remains)
- No cart marked as removed continues to move

### 4. Comparison Tests

#### Test 4.1: Part 1 vs Part 2 First Collision
**Verification:**
- Run Part 1 solution to get first collision position
- Run Part 2 solution with collision logging
- Verify Part 2's first collision matches Part 1

**Expected:**
- Part 1 answer: `58,93` (from part_1_answer.txt)
- Part 2 should log first collision at same position

**Pass Criteria:**
- First collision in Part 2 logs shows `58,93`

#### Test 4.2: Part 1 and Part 2 Movement Consistency
**Verification:**
- Run both Part 1 and Part 2 solutions
- Compare cart positions after first 10 ticks (before any collisions affect movement)
- Verify all cart positions are identical

**Expected Behavior:**
- Before any collisions, cart movements should be identical
- Same track parsing, same initial positions
- Same movement mechanics

**Pass Criteria:**
- All cart positions match between Part 1 and Part 2 for first N ticks
- Track dimensions match
- Initial cart count matches

#### Test 4.3: Expected Final Answer Format
**Verification:**
- Output should be `X,Y` format
- X and Y should be integers
- Should be valid track coordinates
- Position should be on a valid track piece

**Pass Criteria:**
- Output matches regex: `^\d+,\d+$`
- Coordinates within track bounds
- Verify: `track[final_y][final_x] in ['|', '-', '/', '\\', '+']`

### 5. Robustness Tests

#### Test 5.1: No Infinite Loops
**Setup:**
- Add iteration counter with max limit (e.g., 100,000 ticks)

**Verification:**
- Simulation should complete well before limit
- If limit reached, raise error

**Pass Criteria:**
- Simulation completes in reasonable time (< 1 second)

#### Test 5.2: All Carts Eventually Removed or One Remains
**Verification:**
- After simulation, count removed carts
- Should be (total_carts - 1)

**Pass Criteria:**
- Exactly 1 active cart remains
- All other carts marked as removed

### 6. Visual Debugging Tests (Optional)

#### Test 6.1: Print Track State
**Implementation:**
- Function to print track with current cart positions
- Mark removed carts differently (or don't show them)

**Use:**
- Debug unexpected behavior
- Visualize collision sequences

#### Test 6.2: Step-by-Step Execution
**Implementation:**
- Option to pause after each tick
- Show cart positions and states

**Use:**
- Verify collision detection timing
- Check cart movement order

## Test Execution Order

1. **First**: Test 3.1 (Parse Input) - ensures we can read the data
2. **Second**: Test 3.2 (Movement Mechanics) - ensures basic simulation works
3. **Third**: Test 4.2 (Movement Consistency) - verify Part 1 and Part 2 start the same
4. **Fourth**: Test 4.1 (Compare first collision) - ensures consistency with Part 1
5. **Fifth**: Test 2.1 (Multi-cart pile-up) - verify collision_positions mechanism works
6. **Sixth**: Test 3.3 (Full Simulation) - get the answer
7. **Seventh**: Test 3.4 (Collision Accuracy) - verify correctness with logging
8. **Eighth**: Test 4.3 (Answer format) - verify output format
9. **Finally**: Other edge case tests (2.2-2.4) if issues found

## Success Criteria

### Minimum Requirements:
- ✓ Simulation completes without errors
- ✓ Returns exactly one cart's position
- ✓ Position is valid (on track, within bounds)
- ✓ Output format is `X,Y`
- ✓ First collision matches Part 1 answer (58,93)

### Comprehensive Validation:
- ✓ All collision removals are correct (both carts removed)
- ✓ Multi-cart pile-ups handled correctly (3+ carts at same position all removed)
- ✓ collision_positions set correctly tracks collision locations per tick
- ✓ No removed carts continue to move
- ✓ Simulation terminates when 1 cart remains
- ✓ Zero-cart scenario raises appropriate exception
- ✓ Cart movement follows all rules (curves, intersections, straight)
- ✓ Collision detection happens after each cart move, not end of tick
- ✓ Movement consistency with Part 1 before collisions diverge behavior

## Manual Verification Steps

1. **Count initial carts**: Manually count cart symbols in input.md
2. **Verify final answer**: Position should be on track
3. **Sanity check**: Final cart should be far from start (many ticks passed)
4. **Cross-reference**: If AoC site available, submit answer to verify

## Debugging Strategy

If simulation fails:
1. Add print statements for each collision (including pile-ups)
2. Print cart count after each tick
3. Print collision_positions set after each tick
4. Verify first collision matches Part 1
5. Check for off-by-one errors in collision detection
6. Ensure removed carts are skipped properly
7. Verify termination condition (exactly 1 cart check)
8. Check for multi-cart pile-ups being handled correctly
9. Verify collision_positions is cleared/reset each tick (if using that approach)

## Expected Output Characteristics

Based on problem structure:
- Initial carts: ~10-20 carts
- Collisions needed: (carts - 1) / 2 = ~5-10 collisions
- Simulation duration: 100-10,000 ticks (estimate)
- Final position: Should be valid track coordinates
- Runtime: < 1 second
