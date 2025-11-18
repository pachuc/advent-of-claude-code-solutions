# Testing Plan: Permutation Promenade Part 2

## Testing Strategy Overview

The main challenges in testing this solution are:
1. **Correctness of dance execution** - ensuring each move type works properly
2. **Cycle detection accuracy** - finding the correct cycle length
3. **Modulo arithmetic correctness** - calculating the right position in the cycle
4. **Edge case handling** - dealing with boundary conditions

Since we cannot manually verify 1 billion iterations, we must build confidence through:
- Unit tests of individual components
- Integration tests with known small examples
- Verification against Part 1 answer
- Sanity checks on cycle properties

## Counting Convention

Throughout these tests, we use this convention:
- **Iteration 0**: Initial state `abcdefghijklmnop` (before any dances)
- **Iteration 1**: State after 1 dance (Part 1 answer: `eojfmbpkldghncia`)
- **Iteration N**: State after N dances

## Test Cases

### Test 1: Verify Part 1 Answer (CRITICAL)

**Purpose**: Confirm that our dance execution logic is correct by reproducing the Part 1 answer

**Test**:
```python
# After exactly 1 iteration, result should be Part 1 answer
with open('input.md', 'r') as f:
    input_data = f.read().strip()
moves = [m for m in input_data.split(',') if m]

initial = list('abcdefghijklmnop')
perform_dance(initial, moves)
result = ''.join(initial)

assert result == 'eojfmbpkldghncia', f"Expected 'eojfmbpkldghncia', got '{result}'"
print("✓ Test 1 PASSED: Part 1 answer verified")
```

**Expected**: PASS
**If fails**: Critical bug in move implementation or parsing - must fix before proceeding

---

### Test 2: Verify Dance Move Functions (Unit Tests)

**Purpose**: Ensure each move type works correctly in isolation

**Test 2a - Spin**:
```python
# Test spin with 5 programs
programs = list('abcde')
spin(programs, 3)
assert programs == list('cdeab'), f"Expected ['c','d','e','a','b'], got {programs}"

# Test spin with 16 programs (actual problem size)
programs = list('abcdefghijklmnop')
spin(programs, 1)
assert programs == list('pabcdefghijklmno')

# Test spin with 0 (edge case)
programs = list('abcde')
spin(programs, 0)
assert programs == list('abcde')  # No change

print("✓ Test 2a PASSED: Spin function works correctly")
```

**Test 2b - Exchange**:
```python
# Test exchange at boundaries
programs = list('abcde')
exchange(programs, 0, 4)
assert programs == list('ebcda')

# Test exchange with same position (edge case)
programs = list('abcde')
exchange(programs, 2, 2)
assert programs == list('abcde')  # No change when swapping with self

print("✓ Test 2b PASSED: Exchange function works correctly")
```

**Test 2c - Partner**:
```python
# Test partner swap
programs = list('abcde')
partner(programs, 'a', 'e')
assert programs == list('ebcda')

# Test partner with example from problem
programs = list('eabdc')
partner(programs, 'e', 'b')
assert programs == list('baedc')

print("✓ Test 2c PASSED: Partner function works correctly")
```

---

### Test 3: Small Example Cycle Detection

**Purpose**: Verify cycle detection with manually traceable examples

**Test 3a - Simple spin cycle**:
```python
# Create a simple dance that cycles quickly
simple_moves = ['s1']  # Just spin by 1
initial = list('abcd')

# Manually trace:
# Start (iteration 0): abcd
# After 1: dabc
# After 2: cdab
# After 3: bcda
# After 4: abcd (back to start)

cycle_length = find_cycle_length(initial, simple_moves)
assert cycle_length == 4, f"Expected cycle length 4, got {cycle_length}"

print("✓ Test 3a PASSED: Simple cycle detected correctly")
```

**Test 3b - Multi-move example**:
```python
# Use example from problem description: s1,x3/4,pe/b on 'abcde'
simple_moves = ['s1', 'x3/4', 'pe/b']
initial = list('abcde')

# Find cycle length (will need to be verified by iteration)
cycle_length = find_cycle_length(initial, simple_moves)
assert cycle_length > 0 and cycle_length <= 120, "Cycle length should be reasonable"

# Verify it actually cycles
current = initial.copy()
for _ in range(cycle_length):
    perform_dance(current, simple_moves)
assert current == initial, "Should return to initial after cycle_length iterations"

print(f"✓ Test 3b PASSED: Multi-move cycle detected (length: {cycle_length})")
```

---

### Test 4: Verify Cycle Properties

**Purpose**: Ensure the detected cycle actually cycles back to the initial state

**Test 4a - Single cycle**:
```python
# After cycle_length iterations, should return to initial state
with open('input.md', 'r') as f:
    input_data = f.read().strip()
moves = [m for m in input_data.split(',') if m]
initial = list('abcdefghijklmnop')

cycle_length = find_cycle_length(initial, moves)

current = initial.copy()
for _ in range(cycle_length):
    perform_dance(current, moves)

assert current == initial, "Should return to initial state after one cycle"
print(f"✓ Test 4a PASSED: Cycle returns to initial (length: {cycle_length})")
```

**Test 4b - Double cycle**:
```python
# After 2 * cycle_length iterations, should also be at initial state
current = initial.copy()
for _ in range(2 * cycle_length):
    perform_dance(current, moves)

assert current == initial, "Should return to initial state after two cycles"
print("✓ Test 4b PASSED: Double cycle also returns to initial")
```

---

### Test 5: Modulo Arithmetic Correctness

**Purpose**: Verify correct handling of modulo operations and edge cases

**Test 5a - Modulo equals zero case**:
```python
# When target is exactly divisible by cycle_length
# Example: If cycle_length = 60, test with target = 60, 120, 180

# After cycle_length iterations using solve()
result_solve = solve(cycle_length)
result_list = list(result_solve)

# After cycle_length iterations using direct iteration
current = initial.copy()
for _ in range(cycle_length):
    perform_dance(current, moves)

# These should match (and both should equal initial state)
assert result_list == current, "solve(cycle_length) should match direct iteration"
assert current == initial, "After cycle_length iterations, should be back at initial"

print("✓ Test 5a PASSED: Modulo zero case handled correctly")
```

**Test 5b - Small target values**:
```python
# Test that small values (1, 2, 3, 10) work correctly
for n in [1, 2, 3, 10]:
    # Direct iteration
    result_direct = initial.copy()
    for _ in range(n):
        perform_dance(result_direct, moves)

    # Using solve function
    result_solve = list(solve(n))

    assert result_solve == result_direct, f"solve({n}) should match {n} direct iterations"

print("✓ Test 5b PASSED: Small target values work correctly")
```

**Test 5c - Values around cycle boundary**:
```python
# Test values just before, at, and after the cycle length
test_values = [cycle_length - 1, cycle_length, cycle_length + 1]

for n in test_values:
    result_direct = initial.copy()
    for _ in range(n):
        perform_dance(result_direct, moves)

    result_solve = list(solve(n))
    assert result_solve == result_direct, f"solve({n}) should match direct iteration"

print("✓ Test 5c PASSED: Values around cycle boundary work correctly")
```

---

### Test 6: Verify No Off-by-One Errors

**Purpose**: Ensure we're counting iterations correctly

**Test**:
```python
# Iteration 1 should give Part 1 answer
result_1 = solve(1)
assert result_1 == 'eojfmbpkldghncia', "After 1 iteration should be Part 1 answer"

# Iteration 2 should be: apply dance to Part 1 answer
part1_state = list('eojfmbpkldghncia')
result_2_expected = part1_state.copy()
perform_dance(result_2_expected, moves)
result_2_actual = solve(2)
assert result_2_actual == ''.join(result_2_expected), "After 2 iterations should match"

# Iteration 0 edge case (if supported - may want initial state)
# This depends on implementation; may not be needed for the actual problem

print("✓ Test 6 PASSED: No off-by-one errors detected")
```

---

### Test 7: Cycle Detection Performance

**Purpose**: Ensure cycle detection terminates in reasonable time

**Test**:
```python
import time

with open('input.md', 'r') as f:
    input_data = f.read().strip()
moves = [m for m in input_data.split(',') if m]
initial = list('abcdefghijklmnop')

start = time.time()
cycle_length = find_cycle_length(initial, moves)
elapsed = time.time() - start

# Should complete quickly (under 10 seconds)
assert elapsed < 10.0, f"Cycle detection took {elapsed:.2f}s, should be < 10s"

# Cycle length should be reasonable (not billions!)
assert cycle_length < 10_000_000, f"Cycle length {cycle_length} seems too large"

print(f"✓ Test 7 PASSED: Cycle detection completed in {elapsed:.2f}s")
print(f"  Cycle length: {cycle_length}")
```

---

### Test 8: State Immutability Check

**Purpose**: Ensure we're not accidentally modifying states during detection

**Test**:
```python
initial = list('abcdefghijklmnop')
initial_backup = initial.copy()

# Run cycle detection
cycle_length = find_cycle_length(initial, moves)

# Initial should be unchanged (find_cycle_length should work on a copy)
assert initial == initial_backup, "find_cycle_length should not modify initial state"

print("✓ Test 8 PASSED: Initial state not modified during cycle detection")
```

---

### Test 9: Full Solution with 1 Billion Iterations

**Purpose**: Verify the solution handles the actual 1 billion target

**Test**:
```python
import time

start = time.time()
result = solve(1_000_000_000)
elapsed = time.time() - start

# Result should be valid (16 programs, all unique)
assert len(result) == 16, f"Result should be 16 characters, got {len(result)}"
assert sorted(result) == sorted('abcdefghijklmnop'), "Result should be a valid permutation"

# Should complete quickly (< 10 seconds)
assert elapsed < 10.0, f"Full solution took {elapsed:.2f}s, should be < 10s"

print(f"✓ Test 9 PASSED: Full solution completed in {elapsed:.2f}s")
print(f"  Final result: {result}")
```

---

### Test 10: Verify All States in Cycle are Unique

**Purpose**: Ensure we have a proper cycle with no sub-cycles

**Test**:
```python
# Collect all states in one cycle
states = []
current = initial.copy()

for i in range(cycle_length):
    perform_dance(current, moves)
    states.append(tuple(current))

# All states in the cycle should be unique
assert len(states) == len(set(states)), "All states in cycle should be unique"

# The last state should be the initial state (completing the cycle)
assert list(states[-1]) == initial, "After cycle_length iterations, should return to initial"

# The initial state itself should NOT be in the states list
# (since we collect states AFTER each dance, not before)
initial_tuple = tuple(initial)
assert states[0] != initial_tuple, "First state should be different from initial (after 1 dance)"

print(f"✓ Test 10 PASSED: All {cycle_length} states in cycle are unique")
```

---

### Test 11: Move Parsing Edge Cases

**Purpose**: Ensure move parsing handles edge cases correctly

**Test**:
```python
# Empty move strings (should be filtered out)
test_moves = ['s1', '', 'x0/1', '']
programs = list('abcde')
perform_dance(programs, test_moves)
# Should not crash

# Large spin (maximum for 16 programs)
test_moves = ['s15']
programs = list('abcdefghijklmnop')
perform_dance(programs, test_moves)
# Should rotate 15 elements to front

# Maximum position indices
test_moves = ['x14/15', 'x0/15']
programs = list('abcdefghijklmnop')
perform_dance(programs, test_moves)
# Should not crash

print("✓ Test 11 PASSED: Edge cases handled correctly")
```

---

## Integration Testing Procedure

### Complete Validation Workflow

Run these steps in order to validate the complete solution:

```python
def run_integration_tests():
    """Run all integration tests in sequence."""

    print("=" * 60)
    print("INTEGRATION TEST SUITE")
    print("=" * 60)

    # Read input
    with open('input.md', 'r') as f:
        input_data = f.read().strip()
    moves = [m for m in input_data.split(',') if m]
    initial = list('abcdefghijklmnop')

    # Step 1: Verify Part 1 answer
    print("\n[1/5] Verifying Part 1 answer...")
    result_1 = initial.copy()
    perform_dance(result_1, moves)
    assert ''.join(result_1) == 'eojfmbpkldghncia'
    print(f"  ✓ After 1 iteration: {''.join(result_1)}")

    # Step 2: Find and verify cycle length
    print("\n[2/5] Finding cycle length...")
    cycle_length = find_cycle_length(initial, moves)
    print(f"  ✓ Detected cycle length: {cycle_length}")

    # Step 3: Verify cycle closure
    print("\n[3/5] Verifying cycle returns to initial state...")
    current = initial.copy()
    for _ in range(cycle_length):
        perform_dance(current, moves)
    assert current == initial
    print(f"  ✓ After {cycle_length} iterations: returns to initial state")

    # Step 4: Compute final answer
    print("\n[4/5] Computing final answer for 1 billion iterations...")
    result = solve(1_000_000_000)
    print(f"  ✓ After 1,000,000,000 iterations: {result}")

    # Step 5: Sanity check final answer
    print("\n[5/5] Sanity checking final answer...")
    assert len(result) == 16, "Should be 16 characters"
    assert sorted(result) == sorted('abcdefghijklmnop'), "Should be valid permutation"
    assert result != 'abcdefghijklmnop', "Unlikely to be initial state"
    print(f"  ✓ Result is a valid 16-character permutation")

    print("\n" + "=" * 60)
    print("ALL INTEGRATION TESTS PASSED")
    print("=" * 60)
    print(f"\nFINAL ANSWER: {result}")
```

---

## Expected Behavior & Sanity Checks

### Cycle Length Expectations

Based on permutation theory:
- For 16 elements, cycle length is determined by the LCM of the cycle lengths of the individual permutation components
- Common cycle lengths for permutation problems: 12, 24, 30, 60, 120, 420, 840
- We expect something in the range of **10-1000** most likely
- Anything over 1,000,000 would be suspicious

### Output Format Validation

```python
def validate_output(result):
    """Validate the output format and content."""
    # Must be exactly 16 characters
    assert len(result) == 16, f"Expected 16 characters, got {len(result)}"

    # Must contain each letter exactly once
    assert sorted(result) == sorted('abcdefghijklmnop'), "Invalid permutation"

    # Should be different from initial (the dance should do something)
    assert result != 'abcdefghijklmnop', "Result shouldn't be initial state"

    return True
```

---

## Test Execution Order

1. **Unit tests** (Test 2a, 2b, 2c) - Verify basic operations work
2. **Small examples** (Test 3a, 3b) - Verify cycle detection logic with simple cases
3. **Part 1 verification** (Test 1) - CRITICAL: Confirms dance execution is correct
4. **Cycle properties** (Test 4a, 4b) - Verify cycle is real and repeats
5. **Off-by-one** (Test 6) - Verify counting is correct
6. **Modulo tests** (Test 5a, 5b, 5c) - Verify arithmetic is correct
7. **Performance** (Test 7, 9) - Verify solution runs in reasonable time
8. **Robustness** (Test 8, 10, 11) - Verify edge cases and invariants
9. **Integration** - Run complete workflow

---

## Success Criteria

The solution is correct if ALL of the following are true:

- ✅ All unit tests pass (move functions work correctly)
- ✅ Part 1 answer is reproduced after 1 iteration
- ✅ Cycle detection finds a valid cycle that returns to initial state
- ✅ Modulo arithmetic matches direct iteration for small test values
- ✅ Final answer is a valid permutation of 16 programs
- ✅ Solution completes in under 10 seconds
- ✅ Cycle length is reasonable (< 1,000,000)
- ✅ All states in one cycle are unique (no sub-cycles)

**If any test fails**: There is a bug that must be fixed before trusting the final answer.

---

## Debugging Output

For transparency and debugging, the solution should print:

```
Verifying Part 1 answer...
✓ Part 1 verification passed: eojfmbpkldghncia

Solving Part 2...
Finding cycle length...
Cycle detected at length: {cycle_length}
Effective iterations: 1000000000 % {cycle_length} = {effective_iterations}
Final result: {final_result}

Final Answer: {final_result}
```

This output helps verify:
1. Part 1 answer is correct (sanity check)
2. Cycle was detected successfully
3. Modulo arithmetic was applied correctly
4. Final answer is displayed clearly
