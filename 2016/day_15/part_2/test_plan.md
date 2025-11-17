# Test Plan - Part 2: Disc Timing Puzzle

## Overview
This test plan provides comprehensive verification for the Part 2 solution, which adds a 7th disc to the original 6-disc system. The plan includes 10 test cases covering correctness, minimality, performance, edge cases, and comparison with Part 1.

## Testing Objectives
1. Verify the solution correctly adds and processes 7th disc
2. Validate the answer satisfies all 7 disc constraints
3. Confirm the answer is minimal (earliest possible time)
4. Ensure the algorithm handles the additional disc efficiently
5. Verify disc ordering and sequential numbering
6. Confirm Part 1 answer fails with the new disc configuration

## Test 1: Input Parsing and 7th Disc Addition
**Purpose**: Verify 6 discs are parsed from file and 7th disc is added correctly

**Test Steps**:
1. Run the solution with `input.md`
2. Check printed output shows exactly 7 discs
3. Verify disc #7 has: 11 positions, initial position 0

**Expected Output**:
```
Parsed discs:
  Disc #1: 13 positions, initial position 10
  Disc #2: 17 positions, initial position 15
  Disc #3: 19 positions, initial position 17
  Disc #4: 7 positions, initial position 1
  Disc #5: 5 positions, initial position 0
  Disc #6: 3 positions, initial position 1
  Disc #7: 11 positions, initial position 0
```

**Pass Criteria**: All 7 discs present with correct parameters

## Test 2: Solution Correctness
**Purpose**: Verify the computed answer T satisfies all disc constraints

**Test Steps**:
For the solution T, manually verify each disc constraint:
1. Disc #1: `(10 + T + 1) % 13 == 0`
2. Disc #2: `(15 + T + 2) % 17 == 0`
3. Disc #3: `(17 + T + 3) % 19 == 0`
4. Disc #4: `(1 + T + 4) % 7 == 0`
5. Disc #5: `(0 + T + 5) % 5 == 0`
6. Disc #6: `(1 + T + 6) % 3 == 0`
7. Disc #7: `(0 + T + 7) % 11 == 0`

**Expected Output**:
```
✓ Solution verified: All discs align correctly
```

**Pass Criteria**: All 7 modular constraints satisfied

## Test 3: Minimality Verification
**Purpose**: Confirm T is the earliest time (T-1 should fail)

**Test Steps**:
1. Check if T-1 satisfies all constraints
2. Verify that at least one disc fails for T-1

**Expected Output**:
```
✓ Solution is minimal (T-1 does not work)
```

**Pass Criteria**: T-1 fails at least one constraint

## Test 4: Manual Constraint Calculation
**Purpose**: Double-check the math for each disc independently

**Test Steps**:
For each disc i, calculate what T must satisfy:
- Disc 1: `T ≡ -(10+1) ≡ -11 ≡ 2 (mod 13)`
- Disc 2: `T ≡ -(15+2) ≡ -17 ≡ 0 (mod 17)`
- Disc 3: `T ≡ -(17+3) ≡ -20 ≡ 18 (mod 19)` (since -20 + 38 = 18)
- Disc 4: `T ≡ -(1+4) ≡ -5 ≡ 2 (mod 7)`
- Disc 5: `T ≡ -(0+5) ≡ -5 ≡ 0 (mod 5)`
- Disc 6: `T ≡ -(1+6) ≡ -7 ≡ 2 (mod 3)` (since -7 + 9 = 2)
- Disc 7: `T ≡ -(0+7) ≡ -7 ≡ 4 (mod 11)` (since -7 + 11 = 4)

Then verify solution T against each congruence:
- `T % 13 == 2`
- `T % 17 == 0`
- `T % 19 == 18`
- `T % 7 == 2`
- `T % 5 == 0`
- `T % 3 == 2`
- `T % 11 == 4`

**Pass Criteria**: All congruences satisfied by T

## Test 5: Algorithm Efficiency
**Purpose**: Ensure solution completes quickly despite large search space

**Test Steps**:
1. Run the solution and measure execution time
2. Verify it completes in < 1 second

**Expected Behavior**:
- LCM optimization reduces search space dramatically
- Step size after all 7 discs: `lcm(13,17,19,7,5,3,11) = 4,849,845`
- Algorithm should find answer in microseconds/milliseconds

**Pass Criteria**: Execution time < 1 second

## Test 6: Edge Case - 7th Disc Starting at Position 0
**Purpose**: Verify handling of disc that starts at position 0

**Test Steps**:
1. Confirm disc #7 starts at position 0
2. At time T=0, disc #7 is at position 0
3. At time T+7, disc #7 is at position `(0 + T + 7) % 11`
4. For success: `(T + 7) % 11 == 0` → `T ≡ 4 (mod 11)`

**Expected Behavior**:
- Algorithm correctly handles initial_position = 0
- No division by zero or special case errors
- Constraint correctly computed

**Pass Criteria**: No errors, constraint properly enforced

## Test 7: Comparison with Part 1
**Purpose**: Sanity check that Part 2 answer differs from Part 1 and verify why

**Test Steps**:
1. Compare Part 2 answer with Part 1 answer (203660)
2. Verify they are different (additional disc changes the solution)
3. **Explicitly verify Part 1 answer fails disc #7 constraint**:
   - For T = 203660, check disc #7: `(0 + 203660 + 7) % 11`
   - Calculate: `203667 % 11 = 4` (not 0, so it fails)
   - This confirms disc #7 genuinely changes the problem
4. Verify Part 2 answer satisfies disc #7: `(0 + T + 7) % 11 == 0`

**Expected Behavior**:
- Part 2 answer ≠ 203660 (Part 1 answer)
- Part 1 answer fails disc #7: `203667 % 11 = 4 ≠ 0`
- Part 2 answer satisfies all 7 constraints including disc #7

**Pass Criteria**: Answers differ, Part 1 fails disc #7, Part 2 satisfies all discs

## Test 8: Step-by-Step Simulation
**Purpose**: Manually trace capsule falling through discs at solution time T

**Test Steps**:
For the solution T, trace each step:
1. At time T, button pressed, capsule drops
2. At time T+1, capsule reaches disc #1 at position `(10+T+1)%13` → should be 0
3. At time T+2, capsule reaches disc #2 at position `(15+T+2)%17` → should be 0
4. At time T+3, capsule reaches disc #3 at position `(17+T+3)%19` → should be 0
5. At time T+4, capsule reaches disc #4 at position `(1+T+4)%7` → should be 0
6. At time T+5, capsule reaches disc #5 at position `(0+T+5)%5` → should be 0
7. At time T+6, capsule reaches disc #6 at position `(1+T+6)%3` → should be 0
8. At time T+7, capsule reaches disc #7 at position `(0+T+7)%11` → should be 0

**Pass Criteria**: All positions are 0, capsule successfully falls through

## Test 9: Boundary Testing
**Purpose**: Verify solution handles T=0 case and large T values correctly

**Test Steps**:
1. Check if T=0 is tested as a candidate
2. Verify T=0 likely fails (based on initial positions)
3. Confirm final answer is reasonable (not astronomically large)

**Expected Behavior**:
- T=0 should fail multiple constraints
- Solution should be in reasonable range (millions or less)

**Pass Criteria**: T > 0 and algorithm finds it efficiently

## Test 10: Disc Ordering Verification
**Purpose**: Verify disc #7 is properly appended with correct sequential numbering

**Test Steps**:
1. Check that parsed output shows discs #1 through #7 in order
2. Verify disc #7 is the last disc in the list
3. Confirm disc numbers are sequential (no gaps, no duplicates)
4. Verify disc #7 has correct parameters: 11 positions, initial position 0

**Expected Behavior**:
- Discs appear in order: 1, 2, 3, 4, 5, 6, 7
- Each disc number appears exactly once
- Disc #7 parameters match specification

**Pass Criteria**: All 7 discs present in sequential order with correct parameters

## Acceptance Criteria Summary
All tests must pass:
- ✓ 7 discs parsed/added correctly (Test 1)
- ✓ Disc ordering is sequential 1-7 (Test 10)
- ✓ Solution satisfies all 7 constraints (Test 2)
- ✓ Solution is minimal (T-1 fails) (Test 3)
- ✓ Manual math verification confirms correctness (Test 4)
- ✓ Algorithm completes quickly (< 1 second) (Test 5)
- ✓ No errors with position 0 initial value (Test 6)
- ✓ Answer differs from Part 1 (Test 7)
- ✓ Part 1 answer explicitly fails disc #7 (Test 7)
- ✓ Step-by-step simulation succeeds (Test 8)
- ✓ Boundary cases handled properly (Test 9)

## Quick Verification Command
After running solution, verify with Python one-liner:
```python
T = <solution_value>
all([
    (10+T+1)%13==0, (15+T+2)%17==0, (17+T+3)%19==0,
    (1+T+4)%7==0, (0+T+5)%5==0, (1+T+6)%3==0, (0+T+7)%11==0
])
```
Should return `True`.
