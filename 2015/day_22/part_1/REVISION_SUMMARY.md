# Revision Summary

This document summarizes the changes made to the implementation and test plans based on the critique.

## Implementation Plan Updates

### Critical Fixes
1. **Effect Timing Logic (Step 3)**
   - Added explicit sequence: apply effects (if timer > 0) → decrement timers → effects expire at 0
   - Clarified that effects are active when timer > 0 BEFORE decrement
   - Emphasized that expired effects (timer = 0) can be recast on the same turn

2. **Spell Recasting Logic (Step 4)**
   - Specified that effect availability must check `timer > 0` (not `>= 0`)
   - Added example showing Shield recasting when timer goes 1 → 0
   - This allows immediate recasting when effects expire

3. **Boss Attack Logic (Step 5)**
   - Added explicit armor calculation: `armor = 7 if shield_timer > 0 else 0`
   - Clarified armor is checked AFTER effects apply
   - Emphasized minimum 1 damage rule

4. **State Hashing (Step 6)**
   - Added reasoning for excluding mana_spent from state key
   - Explained how this enables proper Dijkstra's state pruning

5. **Dijkstra's Algorithm (Step 7)**
   - Completely rewrote with detailed turn-by-turn sequence
   - Added clear markers for PLAYER TURN and BOSS TURN phases
   - Emphasized checking for victory/death after effects AND actions
   - Clarified that boss doesn't attack if already dead

### Clarifications
6. **Constants (Step 2)**
   - Added note that mana can exceed 500 (no upper limit)
   - Emphasized that only mana SPENT counts, not mana GAINED

7. **Main Function (Step 8)**
   - Added input validation
   - Specified output format (single integer)
   - Added error handling for no solution case

## Test Plan Updates

### Critical Additions
1. **Test Case 1 (Improved)**
   - Provided more complete worked example
   - Showed multiple scenarios including failures
   - Made expectations clearer

2. **Test Case 4 (Enhanced - CRITICAL)**
   - Added emphasis on critical nature of this test
   - Specified exact verification criteria (timer > 0 check)
   - Added explicit confirmation requirement

3. **New Test Case 12 (Recharge Mana Tracking)**
   - Tests that Recharge adds mana correctly
   - Verifies gained mana doesn't count as spent
   - Confirms mana can exceed 500
   - Critical for correct answer calculation

4. **New Test Case 16 (Winning Sequence Validation)**
   - Implements replay/simulation of winning sequence
   - Validates the solution is actually achievable
   - Catches bugs where algorithm reports invalid paths

### Adjustments
5. **Performance Tests (Test Cases 17-18)**
   - Changed from requirements to guidelines
   - Prioritized correctness over performance
   - Adjusted time expectation to 10 seconds (from 5)
   - Marked memory limit as guideline only

6. **Testing Execution Order**
   - Reorganized to prioritize critical effect timing tests
   - Added specific test case callouts
   - Included new tests in proper sequence

7. **Test Case Numbering**
   - Renumbered test cases 12-16 to 13-18
   - Added new Test Case 12 (Recharge)
   - Added new Test Case 16 (Validation)

## Summary of Improvements

### What Was Fixed
- **Effect timing ambiguity** - Now crystal clear with explicit sequence
- **Spell recasting bug potential** - Specified `timer > 0` check
- **Missing armor calculation** - Added explicit logic
- **Incomplete test case** - Improved Test Case 1
- **Missing Recharge test** - Added Test Case 12
- **No validation test** - Added Test Case 16

### Why These Changes Matter
1. **Effect timing** is the #1 source of bugs in this type of problem
2. **Spell recasting logic** can cause missed optimal solutions if wrong
3. **Recharge tracking** directly affects the final answer
4. **Sequence validation** catches implementation bugs that unit tests miss

### Confidence Level
With these revisions, the plans are now **READY FOR IMPLEMENTATION** with high confidence that:
- The algorithm will correctly handle all timing edge cases
- The solution will find the true minimum mana cost
- Tests will catch any implementation errors
- The final answer will be correct

## Next Steps
Proceed to implementation following the updated plans. Pay special attention to:
1. Effect timing in `apply_effects()` function
2. Spell availability check in `cast_spell()` function (timer > 0)
3. Turn sequence in main Dijkstra's loop
4. Implementing Test Cases 4, 12, and 16 as validation
