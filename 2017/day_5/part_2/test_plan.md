# Testing Plan: Jump Instruction Maze (Part 2)

## Overview
Comprehensive testing strategy to verify the Part 2 solution with conditional offset modification rules.

## Test Categories

### 1. Example Verification Test
**Purpose**: Verify the solution matches the provided example

**Test Case**: Example from problem statement
- **Input**: `[0, 3, 0, 1, -3]`
- **Expected Output**: 10 steps
- **Verification**: Step-by-step trace matches the table in problem.md
- **Why Important**: This is the canonical example; if this fails, the logic is fundamentally wrong

### 2. Part 1 Regression and Comparison Tests
**Purpose**: Verify Part 1 logic still works correctly and Part 2 differs appropriately

**Test 2.1: Part 1 Example Verification**
- **Input**: `[0, 3, 0, 1, -3]` with Part 1 rules (always increment)
- **Expected**: 5 steps
- **Why Important**: Validates baseline logic before adding conditional

**Test 2.2: Part 1 Actual Input Verification**
- **Input**: Actual input.md with Part 1 rules
- **Expected**: 339,351 steps (from part_1_answer.txt)
- **Why Important**: Regression test to ensure Part 1 logic is correctly implemented

**Test 2.3: Part 2 Example Comparison**
- **Input**: `[0, 3, 0, 1, -3]` with Part 2 rules
- **Expected**: 10 steps (different from Part 1's 5 steps)
- **Why Important**: Confirms the conditional logic creates different behavior

### 3. Boundary Condition Tests

#### Test 3.1: Offset Exactly 3
**Purpose**: Verify the >= 3 condition (not > 3)
- **Input**: `[3]`
- **Expected**: 1 step (offset 3 decrements to 2, then jumps +3 to exit)
- **Critical**: Tests the boundary condition

#### Test 3.2: Offset Exactly 2
**Purpose**: Verify offsets < 3 increment
- **Input**: `[2]`
- **Expected**: 1 step (offset 2 increments to 3, then jumps +2 to exit)

#### Test 3.3: Immediate Exit Forward
**Purpose**: Large positive offset
- **Input**: `[100]`
- **Expected**: 1 step (decrements to 99, jumps far past bounds)

#### Test 3.4: Immediate Exit Backward
**Purpose**: Negative offset exit
- **Input**: `[-1]`
- **Expected**: 1 step (increments to 0, but jumps backward to exit)

### 4. Zero and Small Value Tests

#### Test 4.1: Single Zero
**Purpose**: Verify zero handling
- **Input**: `[0]`
- **Expected**: 2 steps
- **Trace**:
  - Step 0: pos=0, offset=0 → increment to 1, jump +0 → pos=0
  - Step 1: pos=0, offset=1 → increment to 2, jump +1 → pos=1 (exit)

#### Test 4.2: Multiple Zeros
**Purpose**: Verify incremental growth from zero
- **Input**: `[0, 0, 0]`
- **Expected**: 6 steps
- **Reasoning**: Each zero increments gradually, creating a complex pattern

### 5. Offset Decrement Behavior Tests

#### Test 5.1: High Offset Decrement
**Purpose**: Verify offsets >= 3 decrease over time
- **Input**: `[5, 0]`
- **Expected**: 1 step (offset 5 decrements to 4, jump +5 exits forward)
- **Key Insight**: Even with decrement, high offsets still cause immediate exit

#### Test 5.2: Offset Crossing Threshold
**Purpose**: Verify transition from decrement (>=3) to increment (<3)
- **Input**: `[3, 0, 0, 0]`
- **Expected**: 1 step (offset 3 decrements to 2, jump +3 to position 3 exits)
- **Trace**:
  - Step 0: pos=0, offset=3 → decrement to 2, jump +3 → pos=3 (exit)
- **Why Important**: Tests the threshold crossover behavior

### 6. Negative Offset Tests

#### Test 6.1: Negative Offset Increment
**Purpose**: Verify negative offsets (< 3) increment toward zero
- **Input**: `[-3, 0]`
- **Expected**: 1 step (offset -3 increments to -2, jump -3 exits backward)
- **Trace**:
  - Step 0: pos=0, offset=-3 → inc to -2, jump -3 → pos=-3 (exit)

#### Test 6.2: Small Negative Loop
**Purpose**: Verify negative offset behavior in a loop
- **Input**: `[1, -1]`
- **Expected**: 3 steps
- **Trace**:
  - Step 0: pos=0, offset=1 → inc to 2, jump +1 → pos=1
  - Step 1: pos=1, offset=-1 → inc to 0, jump -1 → pos=0
  - Step 2: pos=0, offset=2 → inc to 3, jump +2 → pos=2 (exit)
- **Why Important**: Tests backward jumping with increments

### 7. Order of Operations Test

#### Test 7.1: Modification Before Jump
**Purpose**: Verify offset is modified BEFORE jumping (but jump uses original value)
- **Input**: `[1, 1]`
- **Expected**: 2 steps
- **Trace**:
  - Step 0: pos=0, offset=1 → increment to 2, jump +1 → pos=1
  - Step 1: pos=1, offset=1 → increment to 2, jump +1 → pos=2 (exit)
- **Critical**: If jump used modified value, behavior would differ

### 8. Actual Input Validation

#### Test 8.1: Full Input Run
**Purpose**: Solve the actual puzzle
- **Input**: The 1,038-line input from input.md
- **Expected**: A positive integer (value unknown - may be higher or lower than 339,351)
- **Validation Checks**:
  - Result is an integer
  - Result is positive
  - Result is different from Part 1 answer (339,351)
  - Execution completes in reasonable time (< 5 minutes)
  - Log warning if result < 100,000 or > 100,000,000 (suspiciously extreme)

#### Test 8.2: Input Integrity
**Purpose**: Verify input parsing
- **Implementation**:
```python
def test_input_integrity():
    instructions = parse_input('input.md')
    assert len(instructions) == 1038, f"Expected 1038 instructions, got {len(instructions)}"
    assert instructions[0] == 1, f"Expected first value 1, got {instructions[0]}"
    assert instructions[-1] == -572, f"Expected last value -572, got {instructions[-1]}"
    print("✓ Input integrity verified")
```
- **Why Important**: Catches corrupted or incorrect input files

### 9. Edge Case Tests

#### Test 9.1: Single Element List
**Purpose**: Minimal valid input
- **Various inputs**: `[1]`, `[0]`, `[-1]`, `[3]`, `[5]`
- **Verify**: All exit correctly in 1-2 steps

#### Test 9.2: All Same Values
**Purpose**: Uniform behavior
- **Input**: `[2, 2, 2, 2, 2]`
- **Expected**: Pattern where all offsets increment uniformly

#### Test 9.3: Alternating Pattern
**Purpose**: Complex interaction
- **Input**: `[3, -1, 3, -1, 3]`
- **Expected**: Oscillation with decrement/increment mix

## Testing Execution Strategy

### Phase 1: Unit Tests (Quick Validation)
Run tests 1-7 in sequence:
1. Example verification (MUST PASS)
2. Part 1 regression tests (verify baseline)
3. All boundary conditions
4. Zero handling
5. Decrement behavior
6. Negative offsets
7. Order of operations

**Success Criteria**: All unit tests pass

### Phase 2: Integration Test
Run test 8 (actual input):
1. Verify input parsing (Test 8.2)
2. Run full simulation (Test 8.1)
3. Validate result is reasonable

**Success Criteria**:
- Result is a positive integer
- Result is different from Part 1 answer (339,351)
- Completes in < 5 minutes
- No extreme values (warn if < 100k or > 100M)

### Phase 3: Manual Verification (if needed)
If result seems questionable:
1. Add debug logging for first 100 steps
2. Manually trace first 10 steps
3. Verify pattern matches expected behavior
4. Check for off-by-one errors in conditional logic

## Test Implementation Approach

### Helper Function Structure
Create a `simulate()` helper function that can be reused in tests:
```python
def simulate(instructions):
    """Run simulation on a list of instructions (modifies in place)."""
    position = 0
    steps = 0
    while 0 <= position < len(instructions):
        offset = instructions[position]
        if offset >= 3:
            instructions[position] -= 1
        else:
            instructions[position] += 1
        position += offset
        steps += 1
    return steps

def simulate_part1(instructions):
    """Run Part 1 simulation for regression testing."""
    position = 0
    steps = 0
    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1
    return steps
```

### Inline Test Functions
Create a `run_all_tests()` function with nested test functions:
```python
def run_all_tests():
    print("Running Part 2 Tests...")

    def test_example():
        instructions = [0, 3, 0, 1, -3]
        result = simulate(instructions)
        assert result == 10, f"Expected 10, got {result}"
        print("✓ Example test passed")

    def test_part1_regression():
        instructions = [0, 3, 0, 1, -3]
        result = simulate_part1(instructions)
        assert result == 5, f"Expected 5, got {result}"
        print("✓ Part 1 regression test passed")

    # ... more tests

    # Run all
    test_example()
    test_part1_regression()
    # ...

    print("All tests passed!")
```

### Test Output Format
- Print test name before running
- Use assertions to validate
- Print checkmark/success message on pass
- Let assertions raise errors on failure

## Success Criteria Summary

### Must Pass:
1. ✓ Example produces 10 steps
2. ✓ Part 1 example produces 5 steps (regression test)
3. ✓ Part 1 actual input produces 339,351 steps (regression test)
4. ✓ Boundary condition (offset = 3) decrements
5. ✓ Boundary condition (offset = 2) increments
6. ✓ Zero offset increments
7. ✓ Negative offsets increment
8. ✓ Actual input produces a positive integer different from 339,351

### Should Verify:
1. Input parsing loads 1,038 values
2. First value is 1, last value is -572
3. Execution completes in < 5 minutes
4. Result is plausible (warn if < 100k or > 100M)

## Debugging Strategy (if tests fail)

### If Example Test Fails:
1. Add step-by-step trace logging
2. Compare each step to the table in problem.md
3. Check conditional logic (>= 3 vs > 3)
4. Verify order of operations

### If Actual Input Hangs:
1. If > 5 minutes, may indicate infinite loop or extremely long execution
2. Add iteration counter and break after 100 million steps
3. Check for logic error creating permanent loops
4. The conditional decrement may create complex patterns - be patient

### If Result Seems Wrong:
1. Don't assume it must be > or < Part 1 result - the algorithm determines this
2. Check input parsing (should be 1,038 integers)
3. Verify Part 1 regression test passed (339,351)
4. Manually verify first 20 steps match expected pattern
5. Look for off-by-one errors in conditional (>= 3, not > 3)
