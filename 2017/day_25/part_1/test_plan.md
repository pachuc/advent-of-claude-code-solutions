# Test Plan: Turing Machine Simulator

## Testing Strategy Overview

We need to verify correctness at multiple levels:
1. Input parsing accuracy
2. Turing machine simulation correctness
3. Checksum calculation accuracy
4. End-to-end solution validation

## Test 1: Input Parsing Validation

### Objective
Verify that the input blueprint is correctly parsed into data structures

### Test Cases

#### Test 1.1: Initial State Parsing
- **Input**: "Begin in state A."
- **Expected**: initial_state = 'A'
- **Validation**: Print and verify the extracted initial state

#### Test 1.2: Step Count Parsing
- **Input**: "Perform a diagnostic checksum after 12172063 steps."
- **Expected**: num_steps = 12172063
- **Validation**: Print and verify the extracted step count matches exactly

#### Test 1.3: State Rules Parsing
- **Input**: Full state A definition from input.md
- **Expected**:
  ```python
  states['A'][0] = {'write': 1, 'move': 1, 'next_state': 'B'}
  states['A'][1] = {'write': 0, 'move': -1, 'next_state': 'C'}
  ```
- **Validation**:
  - Print entire states dictionary
  - Verify all 6 states (A-F) are present
  - Verify each state has rules for both 0 and 1
  - Manually check a few rules against input

#### Test 1.4: Move Direction Parsing
- **Test**: Verify "right" maps to +1 and "left" maps to -1
- **Validation**: Check move values in parsed dictionary

### How to Execute
```python
# Add debug output in parsing function
initial_state, num_steps, states = parse_input(input_text)
print(f"Initial State: {initial_state}")
print(f"Number of Steps: {num_steps}")
print(f"States parsed: {list(states.keys())}")
for state_name, rules in states.items():
    print(f"\nState {state_name}:")
    for value, rule in rules.items():
        print(f"  Value {value}: {rule}")
```

## Test 2: Simple Example Validation

### Objective
Verify simulation works correctly with the 6-step example from problem description

### Test Case: 6-Step Example

**How to Execute**: Since `parse_input` accepts a string parameter, we can test directly:

```python
# Define the 6-step test input as a string
test_input = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
"""

# Parse and run
initial_state, num_steps, states = parse_input(test_input)
tape = simulate_turing_machine(states, initial_state, num_steps)
checksum = calculate_checksum(tape)

assert checksum == 3, f"Expected 3, got {checksum}"
print("6-step example test PASSED")
```

- **Expected Output**: Checksum = 3
- **Validation**: If output matches 3, basic simulation logic is correct

### Manual Trace (for verification)
Complete trace through all 6 steps:
```
Initial: State=A, Cursor=0, Tape={} (all zeros)

Step 0: Read 0 at pos 0 -> Write 1, Move right, State=B
        Tape={0:1}, Cursor=1

Step 1: Read 0 at pos 1 -> Write 1, Move left, State=A
        Tape={0:1, 1:1}, Cursor=0

Step 2: Read 1 at pos 0 -> Write 0, Move left, State=B
        Tape={0:0, 1:1}, Cursor=-1

Step 3: Read 0 at pos -1 -> Write 1, Move left, State=A
        Tape={-1:1, 0:0, 1:1}, Cursor=-2

Step 4: Read 0 at pos -2 -> Write 1, Move right, State=B
        Tape={-2:1, -1:1, 0:0, 1:1}, Cursor=-1

Step 5: Read 1 at pos -1 -> Write 1, Move right, State=A
        Tape={-2:1, -1:1, 0:0, 1:1}, Cursor=0

Final: Count 1s: positions -2, -1, and 1 have value 1 = 3 total
```

**Checksum**: 3 ✓

## Test 3: Tape Data Structure Validation

### Objective
Verify tape correctly handles negative and positive indices

### Test Cases

#### Test 3.1: Negative Index Support
- **Action**: Write to positions -5, -1, 0, 1, 5
- **Validation**: All positions should be accessible and retain their values

#### Test 3.2: Default Zero Values
- **Action**: Read from position 1000 without writing
- **Expected**: Returns 0
- **Validation**: Uninitialized positions default to 0

#### Test 3.3: Overwriting Values
- **Action**: Write 1 to position 0, then write 0 to position 0
- **Expected**: Final value at position 0 is 0
- **Validation**: Tape correctly updates values

### How to Execute
```python
tape = defaultdict(int)
tape[-5] = 1
tape[0] = 1
tape[5] = 1
assert tape[-5] == 1
assert tape[0] == 1
assert tape[5] == 1
assert tape[1000] == 0  # uninitialized
tape[0] = 0
assert tape[0] == 0  # updated
print("Tape structure tests passed!")
```

## Test 4: Checksum Calculation Validation

### Objective
Verify checksum correctly counts 1s

### Test Cases

#### Test 4.1: Empty Tape
- **Input**: tape = defaultdict(int)
- **Expected**: checksum = 0

#### Test 4.2: Mixed Values with Explicit Zeros
- **Input**: tape = {0: 1, 1: 0, 2: 1, 3: 1, -1: 0}
- **Expected**: checksum = 3 (three 1s)
- **Purpose**: Verify that explicit zeros in the tape don't contribute to checksum
- **Note**: This tests the case where we write 0 to overwrite a previous 1

#### Test 4.3: All Zeros
- **Input**: tape = {0: 0, 1: 0, 2: 0}
- **Expected**: checksum = 0

#### Test 4.4: All Ones
- **Input**: tape = {0: 1, 1: 1, 2: 1}
- **Expected**: checksum = 3

### How to Execute
```python
from collections import defaultdict

# Test 4.1: Empty tape
tape = defaultdict(int)
assert calculate_checksum(tape) == 0, "Empty tape should have checksum 0"

# Test 4.2: Mixed values with explicit zeros
tape = defaultdict(int)
tape[0] = 1
tape[1] = 0  # Explicit zero
tape[2] = 1
tape[3] = 1
tape[-1] = 0  # Explicit zero
# Only counts the three 1s (at positions 0, 2, 3), not the two 0s
assert calculate_checksum(tape) == 3, "Should count only 1s, not 0s"

# Test 4.3: All zeros
tape = defaultdict(int)
tape[0] = 0
tape[1] = 0
tape[2] = 0
assert calculate_checksum(tape) == 0, "All zeros should have checksum 0"

# Test 4.4: All ones
tape = defaultdict(int)
tape[0] = 1
tape[1] = 1
tape[2] = 1
assert calculate_checksum(tape) == 3, "All ones should count all values"

print("Checksum tests passed!")
```

## Test 5: Cursor Movement Validation

### Objective
Verify cursor moves correctly based on direction

### Test Cases

#### Test 5.1: Right Movement
- **Initial**: cursor = 0
- **Action**: cursor += 1
- **Expected**: cursor = 1

#### Test 5.2: Left Movement
- **Initial**: cursor = 0
- **Action**: cursor += -1
- **Expected**: cursor = -1

#### Test 5.3: Multiple Movements
- **Actions**: Start at 0, move right twice, left once
- **Expected**: cursor = 1

### How to Execute
Built into simulation - verify with debug output on small example

## Test 5.5: Step Count Off-By-One Verification

### Objective
Verify that we execute exactly the specified number of steps (common bug)

### Test Case: Simple Linear State Machine
```python
# Create a test where State A always writes 1 and moves right
test_input = """Begin in state A.
Perform a diagnostic checksum after 10 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
"""

initial_state, num_steps, states = parse_input(test_input)
tape = simulate_turing_machine(states, initial_state, num_steps)
checksum = calculate_checksum(tape)

# After 10 steps, should have written 1 to positions 0-9 (10 ones)
assert checksum == 10, f"Expected 10 steps to write 10 ones, got {checksum}"
print("Step count verification PASSED - no off-by-one error")
```

**Critical**: This verifies that `range(num_steps)` executes exactly `num_steps` iterations (0 through num_steps-1)

## Test 6: State Transition Validation

### Objective
Verify state transitions occur correctly

### Test Case: Trace State Transitions
- **Method**: Add debug output to print state after each step
- **Validation**: Verify states transition according to rules
- **Example**: For first few steps of actual input:
  ```
  Step 0: A -> B (because value=0 at start)
  Step 1: B -> A (check what value is at new position)
  etc.
  ```

## Test 7: Full Solution Validation

### Objective
Verify the complete solution with actual input

### Test Approach

#### Test 7.1: Reasonableness Check
- **Expected**: Checksum should be a positive integer
- **Expected**: Checksum should be less than total steps (can't write more 1s than steps)
- **Expected**: Checksum should be > 0 (machine does write some 1s)

#### Test 7.2: Performance Check
- **Expected**: Simulation completes within reasonable time (< 2 minutes)
- **Method**: Time the execution

#### Test 7.3: Determinism Check
- **Method**: Run the simulation twice
- **Expected**: Both runs produce identical results
- **Purpose**: This mainly serves as a sanity check and catches non-deterministic bugs
  - e.g., iterating over sets in undefined order
  - e.g., using random/time-based operations
  - e.g., uninitialized variables with inconsistent values
- **Validation**: Ensures no randomness or bugs causing different outputs

### How to Execute
```python
import time

# Run 1
start = time.time()
result1 = main('input.md')
time1 = time.time() - start

# Run 2
start = time.time()
result2 = main('input.md')
time2 = time.time() - start

print(f"Result 1: {result1} (took {time1:.2f}s)")
print(f"Result 2: {result2} (took {time2:.2f}s)")

# Validation checks
assert result1 == result2, "Results should be deterministic"
assert isinstance(result1, int), "Result should be an integer"
assert result1 > 0, "Should have some 1s on tape"
assert result1 < 12172063, "Can't have more 1s than steps executed"

print("All validation checks PASSED")
```

## Test 8: Edge Cases

### Test 8.1: Consecutive Writes to Same Position
- **Scenario**: Machine writes to same position multiple times
- **Expected**: Only final write matters
- **How**: This naturally occurs in simulation; verify tape only stores final value

### Test 8.2: Wide Cursor Range
- **Scenario**: Cursor moves far left and far right
- **Expected**: Tape handles large positive and negative indices
- **Validation**: Check min/max cursor positions reached during simulation
  ```python
  # Add tracking:
  min_cursor = 0
  max_cursor = 0
  # Update during simulation
  # Print at end
  ```

### Test 8.3: State Self-Loops
- **Scenario**: State transitions to itself
- **Expected**: Should work correctly (some states might loop)
- **Validation**: Check state transition paths in actual input

## Test Execution Order

**Recommended sequence with dependencies:**

1. **Test Tape Structure** → Independent unit test, can run first
2. **Test Checksum** → Independent unit test, can run first
3. **Parse Input** → Verify parsing works on actual input
4. **Test 6-Step Example** → Depends on parsing; validates parsing + simulation together
5. **Test Step Count (Off-by-one)** → Depends on parsing; validates loop iteration count
6. **Run Full Solution** → Get actual answer with real input
7. **Validate Full Solution** → Reasonableness and determinism checks

**Rationale**:
- Tests 1-2 are independent and can run in any order
- Tests 4-5 depend on parsing working correctly (test 3)
- Test 6-7 validate the complete solution

## Success Criteria

✅ All parsing tests pass (correct states, initial state, step count)
✅ 6-step example produces checksum of 3
✅ Step count test passes (no off-by-one errors)
✅ Tape structure handles positive/negative indices correctly
✅ Checksum calculation correctly handles both 1s and explicit 0s
✅ Full solution completes in < 2 minutes
✅ Full solution produces deterministic results (same output on multiple runs)
✅ Final checksum is an integer > 0 and < 12,172,063

## Debugging Strategy

If tests fail:
1. **Parsing failures**: Print raw input and parsed structures, compare manually
2. **Wrong checksum on example**: Add step-by-step trace output
3. **Performance issues**: Profile code, check if using list instead of dict
4. **Wrong final answer**: Verify with step trace on first 100 steps, check for off-by-one errors
