# Test Plan - Part 2: First Location Visited Twice

## Testing Strategy Overview

The testing approach focuses on:
1. **Example verification** - Validate against the provided example
2. **Edge case testing** - Verify boundary conditions and special scenarios
3. **Logic correctness** - Ensure step-by-step tracking works properly
4. **Sanity checks** - Verify result is mathematically reasonable

## Test Categories

### 1. Example Verification Tests

#### Test 1.1: Official Example from Problem Statement
**Input**: `R8, R4, R4, R8`

**Expected behavior**:
- First revisited position: (4, 0)
- Manhattan distance: 4

**Verification steps**:
1. Manually trace the path:
   - Start at (0,0) facing North
   - R8 (East): (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0)
   - R4 (South): (8,-1), (8,-2), (8,-3), (8,-4)
   - R4 (West): (7,-4), (6,-4), (5,-4), (4,-4)
   - R8 (North): (4,-3), (4,-2), (4,-1), (4,0) ← STOP
2. Verify (4,0) was in the set from first instruction
3. Confirm function returns (4, 0) and distance = 4

**Success criteria**: Function returns exactly (4, 0) and distance 4

---

### 2. Edge Case Tests

#### Test 2.1: Immediate Return to Origin
**Input**: `R1, R1, R1, R1`

**Expected behavior**:
- Creates a 1×1 square, returns to (0,0) on 4th instruction
- Path: (0,0) → (1,0) → (1,-1) → (0,-1) → (0,0)
- First revisit: (0, 0)
- Distance: 0

**Rationale**: Tests that starting position (0,0) is properly tracked

---

#### Test 2.2: Revisit on Very Next Move
**Input**: `R2, L1, L1, L2`

**Expected behavior**:
- Path creates immediate overlap
- R2: (1,0), (2,0)
- L1 (North): (2,1)
- L1 (West): (1,1)
- L2 (South): (1,0) ← STOP (visited during R2)
- First revisit: (1, 0)
- Distance: 1

**Rationale**: Tests early detection without traversing full path

---

#### Test 2.3: Revisit in Middle of Long Move
**Input**: `R10, R1, R1, R10`

**Expected behavior**:
- Similar to official example but with R10 instead of R8
- First R10 visits (1,0) through (10,0)
- After R1, R1 turns, final R10 going North will revisit a position
- Tests that revisit during a long move is caught mid-move, not at end

**Rationale**: Ensures we check each step, not just final position

---

#### Test 2.4: Cross-Over Path (X Pattern)
**Input**: `R5, L1, L5, L1, L5, L1, L3`

**Expected behavior**:
- Creates a path that crosses itself forming an X-like pattern
- Should detect first crossing point

**Rationale**: Tests complex path intersection scenarios

---

#### Test 2.5: Multiple Revisits in Single Instruction
**Input**: `R10, L1, L1, R20`

**Expected behavior**:
- R10: Visit (1,0) through (10,0)
- L1 (North): Visit (10,1)
- L1 (West): Visit (9,1)
- R20 (South): Will cross multiple previously visited positions
  - Goes from (9,1) southward to (9,-19)
  - Crosses (9,0) which was NOT visited (only went to x=10)
  - Let me recalculate: Actually need better example

**Better Input**: `R5, R1, R1, R10`
- R5 (East): Visit (1,0), (2,0), (3,0), (4,0), (5,0)
- R1 (South): Visit (5,-1)
- R1 (West): Visit (4,-1)
- R10 (North): Visit (4,0), (4,1), ...
  - **STOP at (4,0)** - first revisit (was visited during R5)
  - Should NOT continue to check (3,0), (2,0), (1,0) even though they were also visited

**Expected**: Returns immediately at (4,0), distance = 4

**Rationale**: Verifies algorithm stops at FIRST revisit in a move, not after completing the move

---

#### Test 2.6: Negative Coordinates
**Input**: `L5, L5`

**Expected behavior**:
- Start at (0,0) facing North
- L5 (West): Visit (-1,0), (-2,0), (-3,0), (-4,0), (-5,0)
- L5 (South): Visit (-5,-1), (-5,-2), (-5,-3), (-5,-4), (-5,-5)
- No revisit occurs
- Final position: (-5, -5)
- Manhattan distance: |-5| + |-5| = 10

**Rationale**: Ensures Manhattan distance calculation handles negative coordinates correctly

---

### 3. Logic Correctness Tests

#### Test 3.1: Direction Handling
**Verification**:
- Confirm turning logic works correctly (reused from Part 1)
- North → R → East → R → South → R → West → R → North
- North → L → West → L → South → L → East → L → North

**Method**: Unit test the turn_right() and turn_left() functions

---

#### Test 3.2: Step-by-Step Movement Verification
**Test**: Create a custom instruction like `R3`

**Manual verification**:
- Starting at (0,0), after R3:
  - Should add (1,0) to visited
  - Then add (2,0) to visited
  - Then add (3,0) to visited
- Verify visited set contains exactly {(0,0), (1,0), (2,0), (3,0)}

**Method**: Add debug output or assertions to check visited set contents

---

#### Test 3.3: Single Block Movement
**Input**: `R1, R1, R1, R1` (from Test 2.1)

**Verification**:
- Ensure steps=1 is handled correctly
- Each move adds exactly one new position

---

### 4. Sanity Checks for Actual Input

#### Test 4.1: Result Bounds Validation
**Input**: Actual puzzle input from `input.md`

**Validation**:
```python
total_steps = sum(steps for _, steps in instructions)
assert 0 <= result <= total_steps
```

**Rationale**: Distance cannot exceed total steps taken

---

#### Test 4.2: Result Plausibility
**Checks**:
1. Result is a non-negative integer
2. Result comparison with Part 1 answer (300)
   - **Reasoning**: First revisit *typically* happens before reaching final destination
   - **Important**: This is NOT guaranteed - the revisit could theoretically occur late in the path
   - **Action**: If result ≥ 300, print a warning but DO NOT fail the test
   - Warning message: "Warning: Result ≥ Part 1 answer (300), verify manually"
3. Revisited position is a tuple of two integers

---

#### Test 4.3: Execution Performance
**Measure**:
- Time to execute on actual input
- Memory usage for visited set

**Expected performance**:
- **Optimal**: Complete in < 100ms
- **Warning threshold**: If execution takes > 500ms, print warning
- **Failure threshold**: If execution takes > 5 seconds, algorithm is inefficient (likely using list instead of set)
- Memory usage should be reasonable (< 100 MB, likely < 1 MB)

**Rationale**: Given input size (< 10,000 positions), set operations should be very fast

---

### 5. Component Integration Tests

#### Test 5.1: Parse Input Correctness
**Method**: Reuse Part 1 verification
- Ensure `parse_input()` correctly parses actual input
- Verify first few instructions match expected format
- Check total instruction count

---

#### Test 5.2: Manhattan Distance Calculation
**Method**: Reuse Part 1 verification
- Test with known coordinates:
  - (3, 4) → 7
  - (-3, 4) → 7
  - (0, 0) → 0
  - (-5, -5) → 10

---

### 6. End-to-End Test

#### Test 6.1: Full Solution Pipeline
**Steps**:
1. Parse input from `input.md`
2. Find first revisited position
3. Calculate Manhattan distance
4. Verify result is within expected bounds
5. Print clear output showing position and distance

**Success criteria**:
- No exceptions raised
- Result is a positive integer
- Result < 300 (Part 1 answer)
- Output is clear and unambiguous

---

## Test Execution Order

1. **First**: Run example verification (Test 1.1)
   - If this fails, algorithm is fundamentally wrong
2. **Second**: Run component tests (Tests 5.1, 5.2)
   - Verify reused components still work
3. **Third**: Run edge cases (Tests 2.1-2.6)
   - Catch boundary condition bugs
4. **Fourth**: Run logic tests (Tests 3.1-3.3)
   - Verify core algorithm correctness
5. **Finally**: Run actual input with sanity checks (Tests 4.1-4.3)
   - Verify complete solution

---

## Debugging Strategies

### If Example Test Fails:
1. Add debug output to print visited set after each move
2. Manually trace path on paper
3. Check if positions are being added before or after checking
4. Verify starting position (0,0) is in visited set initially

### If Answer Seems Wrong:
1. Print the revisited position found
2. Verify this position makes sense geometrically
3. Check if distance calculation is correct
4. Add visualization: print path coordinates

### If Performance is Slow:
1. Check if accidentally using list instead of set for visited
2. Verify not doing redundant work in inner loops
3. Profile code to identify bottleneck

---

## Expected Test Results Summary

| Test | Expected Result |
|------|----------------|
| Example R8,R4,R4,R8 | Distance = 4, Position = (4,0) |
| Return to origin (2.1) | Distance = 0, Position = (0,0) |
| Early revisit (2.2) | Distance = 1, Position = (1,0) |
| Multiple revisits (2.5) | Distance = 4, Position = (4,0), stops immediately |
| Negative coords (2.6) | Handles negative coordinates correctly |
| Actual input | 0 < distance, warn if ≥ 300 |
| Performance | < 100ms optimal, < 500ms acceptable, fail if > 5s |
| Memory | < 100 MB used |

---

## Acceptance Criteria

The solution is correct if:
1. [ ] Example test passes with distance = 4
2. [ ] Edge case tests (2.1-2.6) pass with expected positions
3. [ ] Actual input produces valid answer (warn if ≥ 300, but don't fail)
4. [ ] Sanity checks pass (bounds, type, performance < 5s)
5. [ ] No exceptions or errors during execution
6. [ ] Output clearly shows the position found and distance calculated
7. [ ] Multiple revisits in one move stops at FIRST revisit (Test 2.5)
8. [ ] Negative coordinates handled correctly (Test 2.6)
