# Testing Plan: RTG and Microchip Transportation Puzzle

## Testing Strategy

We need to verify:
1. **Correctness:** Solution produces the right answer
2. **Safety:** All intermediate states respect frying rule
3. **Optimality:** BFS finds minimum steps
4. **Performance:** Runs in reasonable time for given input

## Test Categories

### 1. Unit Tests

#### 1.1 Input Parsing Tests

**Test Case 1.1.1: Parse single floor with multiple items**
```
Input: "The first floor contains a hydrogen generator and a lithium-compatible microchip."
Expected: {0: {('hydrogen', 'G'), ('lithium', 'M')}, 1: set(), 2: set(), 3: set()}
```

**Test Case 1.1.2: Parse empty floor**
```
Input: "The fourth floor contains nothing relevant."
Expected: Floor 3 has empty set
```

**Test Case 1.1.3: Parse all four floors**
```
Input: Full input from input.md
Expected: Correct distribution across all floors
Verify: Total of 10 items (5 generators, 5 microchips)
```

#### 1.2 Safety Validation Tests

**Test Case 1.2.1: Safe - Empty floor**
```
Floor: {}
Expected: True (safe)
```

**Test Case 1.2.2: Safe - Only generators**
```
Floor: {('A', 'G'), ('B', 'G')}
Expected: True (generators don't harm each other)
```

**Test Case 1.2.3: Safe - Only microchips**
```
Floor: {('A', 'M'), ('B', 'M')}
Expected: True (microchips don't harm each other)
```

**Test Case 1.2.4: Safe - Microchip with its own generator**
```
Floor: {('A', 'M'), ('A', 'G')}
Expected: True (protected)
```

**Test Case 1.2.5: Safe - Multiple pairs**
```
Floor: {('A', 'M'), ('A', 'G'), ('B', 'M'), ('B', 'G')}
Expected: True (all protected)
```

**Test Case 1.2.6: UNSAFE - Microchip with different generator**
```
Floor: {('A', 'M'), ('B', 'G')}
Expected: False (microchip A will fry)
```

**Test Case 1.2.7: UNSAFE - Microchip with multiple generators, missing its own**
```
Floor: {('A', 'M'), ('B', 'G'), ('C', 'G')}
Expected: False (microchip A unprotected)
```

**Test Case 1.2.8: UNSAFE - One protected, one unprotected microchip**
```
Floor: {('A', 'M'), ('A', 'G'), ('B', 'M')}
Expected: False (microchip A is protected, but microchip B is unprotected with generator A present)
```

#### 1.3 Move Generation Tests

**Test Case 1.3.1: Ground floor - can only move up**
```
State: Elevator on floor 0
Expected: Generated moves only have elevator on floor 1
```

**Test Case 1.3.2: Top floor - can only move down**
```
State: Elevator on floor 3
Expected: Generated moves only have elevator on floor 2
```

**Test Case 1.3.3: Middle floor - can move both directions**
```
State: Elevator on floor 1
Expected: Moves to both floor 0 and floor 2
```

**Test Case 1.3.4: Single item moves**
```
State: Floor has 3 items
Expected: 3 moves with 1 item (if valid)
```

**Test Case 1.3.5: Two item moves**
```
State: Floor has 3 items
Expected: C(3,2) = 3 moves with 2 items (if valid)
```

**Test Case 1.3.6: Invalid moves filtered out**
```
State: {('A','M'), ('B','G')} on floor 0, elevator on floor 0
Action: Try moving only A's microchip up, leaving it with B's generator on floor 0
Expected: This move should NOT be generated (source floor becomes unsafe)
```

**Test Case 1.3.7: Destination safety check**
```
State: Moving ('A','M') to floor with ('B','G')
Expected: This move should NOT be generated (destination unsafe)
```

**Test Case 1.3.8: Elevator must carry items**
```
State: Elevator on floor with items
Expected: All generated moves involve taking 1 or 2 items (no empty elevator moves)
```

#### 1.4 State Canonicalization Tests

**Test Case 1.4.1: Equivalent states**
```
State1: {('hydrogen', 'G'), ('hydrogen', 'M')} on floor 0
State2: {('lithium', 'G'), ('lithium', 'M')} on floor 0
Expected: Same canonical form
```

**Test Case 1.4.2: Non-equivalent states**
```
State1: {('A', 'G'), ('A', 'M')} on floor 0
State2: {('A', 'G'), ('B', 'M')} on floor 0
Expected: Different canonical forms (one is paired, one is not)
```

**Test Case 1.4.3: Complex equivalence**
```
State1: Floor0={('A','G'),('A','M')}, Floor1={('B','G'),('B','M')}
State2: Floor0={('X','G'),('X','M')}, Floor1={('Y','G'),('Y','M')}
Expected: Same canonical form
```

**Test Case 1.4.4: Same items, different floors - NOT equivalent**
```
State1: {('A','G'),('A','M')} on floor 0, elevator on floor 0
State2: {('A','G'),('A','M')} on floor 1, elevator on floor 1
Expected: Different canonical forms (floor position matters!)
```

**Test Case 1.4.5: Same pattern, different elevator position - NOT equivalent**
```
State1: Elevator on floor 0, {('A','G')} on floor 0
State2: Elevator on floor 1, {('A','G')} on floor 0
Expected: Different canonical forms (elevator position matters!)
```

**Test Case 1.4.6: Different pairing patterns - NOT equivalent**
```
State1: Floor0={('A','G'),('A','M')}, Floor1={('B','G'),('B','M')}  (both paired)
State2: Floor0={('A','G'),('B','M')}, Floor1={('A','M'),('B','G')}  (both unpaired)
Expected: Different canonical forms (pairing pattern matters!)
```

### 2. Integration Tests

#### 2.1 Simple Example from Problem Statement

**Test Case 2.1.1: Small example (11 steps)**
```
Input:
F4 .  .  .  .  .
F3 .  .  .  LG .
F2 .  HG .  .  .
F1 E  .  HM .  LM

Expected Output: 11 steps
```

This is the gold standard test from the problem statement.

#### 2.2 Minimal Test Cases

**Test Case 2.2.1: Everything already on floor 4**
```
State: All items on floor 3, elevator on floor 3
Expected: 0 steps
```

**Test Case 2.2.2: Single pair, one move needed**
```
State: Elevator + both items on floor 2
Expected: 1 step (move both items up to floor 3, which is the goal)
```

**Test Case 2.2.3: Single pair on floor 0**
```
State: {('A','G'), ('A','M')} on floor 0
Expected: 3 steps (F0→F1, F1→F2, F2→F3)
Move 1: Take both up to F1
Move 2: Take both up to F2
Move 3: Take both up to F3
```

#### 2.3 Edge Cases

**Test Case 2.3.1: All items on floor 0**
```
Input: All generators and microchips start on floor 0
Expected: Should complete without errors
Verify: No unsafe states generated
```

**Test Case 2.3.2: Maximum dispersion**
```
Input: Items spread across all floors maximally
Expected: Should complete without errors
```

**Test Case 2.3.3: Unpaired items**
```
Input: Generators on floor 0, all microchips on floor 1
Expected: Requires careful sequencing to avoid frying
```

#### 2.4 BFS Optimality Tests

**Test Case 2.4.1: Verify BFS finds shortest path**
```
Setup: Simple scenario with multiple possible solutions of different lengths
Example: Two pairs starting on floor 0
- Optimal: Move both pairs together when possible
- Suboptimal: Move each pair separately
Expected: BFS returns the minimum number of steps
Verification: Manually calculate optimal solution and compare
```

**Test Case 2.4.2: First solution is optimal**
```
Concept: In BFS, the first goal state found has minimum depth
Verification: For test cases with known optimal solutions, verify answer matches
```

### 3. Actual Input Test

**Test Case 3.1: Given puzzle input**
```
Input: From input.md
- Floor 0: Strontium G+M, Plutonium G+M
- Floor 1: Thulium G, Ruthenium G+M, Curium G+M
- Floor 2: Thulium M
- Floor 3: Empty

Expected: Run completes in < 5 seconds
Output: Integer representing minimum steps (exact value TBD - to be established on first correct run and used for regression testing)
```

**Validation steps:**
1. Parse input correctly (10 items total: 5 generators, 5 microchips)
2. BFS completes without infinite loop
3. Returns a positive integer
4. Result is consistent across multiple runs (deterministic)
5. **Action item:** Document the first correct answer and use it for all future regression tests

### 4. Performance Tests

**Test Case 4.1: Execution time**
```
Requirement: Complete in < 5 seconds for given input
Measure: Time from start to result output
```

**Test Case 4.2: Memory usage**
```
Requirement: Use < 500 MB RAM
Measure: Peak memory during BFS
```

**Test Case 4.3: State space size**
```
Monitor: Number of unique states visited
With canonicalization: Target < 50,000 states (rough estimate)
Note: This is informational; actual count depends on puzzle complexity
Primary metrics are time and memory, not state count
```

### 5. Validation Tests

#### 5.1 Solution Path Validation

**Test Case 5.1.1: Trace solution path**
```
Modify BFS to return actual path, not just step count
Verify each step:
- Moves 1 or 2 items
- Both source and destination floors are safe
- Elevator moves exactly one floor up or down
```

**Test Case 5.1.2: Goal state verification**
```
Final state should have:
- All 10 items on floor 3 (5 generators + 5 microchips)
- Floors 0, 1, 2 completely empty
- Elevator position doesn't matter for goal state (all items are on floor 3)
```

#### 5.2 Negative Test Cases

**Test Case 5.2.1: Malformed input**
```
Input: Gibberish text or missing floor descriptions
Expected: Graceful error message (or can skip if not implementing error handling)
```

**Test Case 5.2.2: Invalid state detection**
```
Setup: Manually create an invalid state (microchip with wrong generator)
Expected: is_valid() returns False
Verification: This state should never be added to BFS queue
```

### 6. Regression Tests

**Test Case 6.1: Consistency check**
```
Run solution 3 times on same input
Expected: Same answer all three times
```

**Test Case 6.2: Different input orderings**
```
Note: Input lines describe specific floors ("first floor", "second floor", etc.)
They should not be reordered as that would change the problem
Instead: Test that parsing correctly maps floor descriptions to indices
- "first floor" always → floor 0
- "fourth floor" always → floor 3
```

**Test Case 6.3: Visited state tracking**
```
Monitor: Ensure each unique canonical state is only processed once
Method: Add debug logging to count how many times each state is encountered
Expected: Each canonical state appears in visited set exactly once
```

## Test Execution Order

1. **Phase 1 - Unit Tests (Bottom-up)**
   - Input parsing (1.1.1 - 1.1.3)
   - Safety validation (1.2.1 - 1.2.8)
   - Move generation (1.3.1 - 1.3.8)
   - Canonicalization (1.4.1 - 1.4.6)

2. **Phase 2 - Integration Tests**
   - Small example (11 steps) - Test 2.1.1
   - Minimal cases (2.2.1 - 2.2.3)
   - Edge cases (2.3.1 - 2.3.3)
   - BFS optimality (2.4.1 - 2.4.2)

3. **Phase 3 - Actual Input**
   - Full puzzle from input.md (Test 3.1)
   - Performance measurement (Tests 4.1 - 4.3)

4. **Phase 4 - Validation**
   - Solution path verification (5.1.1 - 5.1.2)
   - Negative tests (5.2.1 - 5.2.2)
   - Regression tests (6.1 - 6.3)

## Success Criteria

✅ All unit tests pass (safety, parsing, move generation)
✅ Small example (Test 2.1.1) produces 11 steps
✅ Actual input completes in < 5 seconds
✅ No unsafe states generated during BFS
✅ Result is consistent and deterministic across multiple runs
✅ Memory usage reasonable (< 500 MB)
✅ Canonicalization correctly identifies equivalent states
✅ BFS finds optimal solution (verified against known examples)
✅ Each canonical state visited at most once

## Debugging Strategies

If tests fail:

1. **Wrong answer:**
   - Print intermediate states
   - Trace BFS expansion
   - Check canonicalization logic
   - Verify safety checking

2. **Too slow:**
   - Verify canonicalization is working
   - Count unique states visited
   - Profile code to find bottlenecks
   - Consider A* with heuristic

3. **Safety violations:**
   - Log each state validation
   - Check move generation carefully
   - Verify both source and destination checks

4. **Infinite loop:**
   - Check visited set is working
   - Verify state hashing is correct
   - Ensure immutability of states

## Test Implementation

Tests can be implemented as:
1. Simple Python script with assertions
2. Print statements to verify intermediate results
3. Manual inspection of small examples
4. Timing measurements using `time.time()`
5. Debug counters for state tracking

**Recommended approach:**
- Create a separate `test.py` file with test functions
- Each test function tests one specific aspect
- Use simple assert statements or print validation
- Keep tests focused on correctness, not exhaustive coverage

No need for unittest framework - keep it simple and focused on correctness.

## Additional Verification

**Solution Path Tracking (Optional but Recommended):**
To build confidence in the solution, consider modifying BFS to track the path:
- Store parent pointers: `{state: parent_state}`
- When goal found, backtrack to reconstruct path
- Validate each step in the path:
  - Elevator moves exactly one floor
  - Carries 1 or 2 items
  - Both source and destination floors are safe
  - No items appear or disappear

This helps debug and verify the solution is not just correct in step count, but also valid in execution.
