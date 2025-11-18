# Testing Plan: Jump Instruction Maze Escape

## Testing Objectives
1. Verify the algorithm correctly implements the jump instruction logic
2. Ensure the offset modification happens in the correct order
3. Validate exit conditions work properly
4. Confirm the step counter is accurate
5. Test edge cases that could cause incorrect behavior

## Test Strategy

### 1. Example Test Case (From Problem Statement)
**Purpose**: Validate against the provided example to ensure basic correctness

**Input**: `[0, 3, 0, 1, -3]`

**Expected Output**: `5 steps`

**Expected Execution Trace**:
| Step | Position | Offset Read | Next Position | List After Modification |
|------|----------|-------------|---------------|------------------------|
| 0    | 0        | 0           | 0             | [1, 3, 0, 1, -3]       |
| 1    | 0        | 1           | 1             | [2, 3, 0, 1, -3]       |
| 2    | 1        | 3           | 4             | [2, 4, 0, 1, -3]       |
| 3    | 4        | -3          | 1             | [2, 4, 0, 1, -2]       |
| 4    | 1        | 4           | 5             | [2, 5, 0, 1, -2]       |
| 5    | 5        | OUT         | EXIT          | -                      |

**Validation Method**:
- Run the algorithm with this input
- Verify step count equals 5
- Optionally trace through to verify each state matches the table above

**Test Code**:
```python
def test_example():
    instructions = [0, 3, 0, 1, -3]
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    assert steps == 5, f"Expected 5 steps, got {steps}"
    print("✓ Example test passed")
```

---

### 2. Edge Case: Single Instruction That Exits Immediately
**Purpose**: Test minimal case where we escape on first jump

**Input**: `[5]`

**Expected Behavior**:
- Start at position 0
- Read offset 5
- Increment to 6
- Jump to position 5 (out of bounds, length is 1)
- Exit after 1 step

**Expected Output**: `1 step`

**Test Code**:
```python
def test_immediate_exit():
    instructions = [5]
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    assert steps == 1, f"Expected 1 step, got {steps}"
    print("✓ Immediate exit test passed")
```

---

### 3. Edge Case: Backward Jump to Negative Index
**Purpose**: Ensure negative position correctly triggers exit

**Input**: `[-1]`

**Expected Behavior**:
- Start at position 0
- Read offset -1
- Increment to 0
- Jump to position -1 (out of bounds)
- Exit after 1 step

**Expected Output**: `1 step`

**Test Code**:
```python
def test_backward_exit():
    instructions = [-1]
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    assert steps == 1, f"Expected 1 step, got {steps}"
    print("✓ Backward exit test passed")
```

---

### 4. Edge Case: All Zeros (Self-Loop that Eventually Escapes)
**Purpose**: Test case where initial offset is 0, creating a self-loop that must resolve

**Input**: `[0]`

**Expected Behavior**:
- Step 0: pos=0, read 0, increment to 1, jump to 0
- Step 1: pos=0, read 1, increment to 2, jump to 1
- Position 1 is out of bounds, exit

**Expected Output**: `2 steps`

**Test Code**:
```python
def test_zero_offset():
    instructions = [0]
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    assert steps == 2, f"Expected 2 steps, got {steps}"
    print("✓ Zero offset test passed")
```

---

### 5. Edge Case: Multiple Zeros
**Purpose**: Verify behavior with several zero offsets in sequence

**Input**: `[0, 0, 0]`

**Expected Behavior**:
- The first position will increment until it jumps past itself
- Each zero will eventually become positive and help escape

**Manual Trace** (all steps):
- Step 0: pos=0, read 0, inc to 1, jump to 0 → [1,0,0]
- Step 1: pos=0, read 1, inc to 2, jump to 1 → [2,0,0]
- Step 2: pos=1, read 0, inc to 1, jump to 1 → [2,1,0]
- Step 3: pos=1, read 1, inc to 2, jump to 2 → [2,2,0]
- Step 4: pos=2, read 0, inc to 1, jump to 2 → [2,2,1]
- Step 5: pos=2, read 1, inc to 2, jump to 3 → [2,2,2] → EXIT

**Expected Output**: `6 steps`

**Test Code**:
```python
def test_multiple_zeros():
    instructions = [0, 0, 0]
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    assert steps == 6, f"Expected 6 steps, got {steps}"
    print("✓ Multiple zeros test passed")
```

---

### 6. Edge Case: Large Forward Jump
**Purpose**: Test that large positive offsets work correctly

**Input**: `[100, 1, 1]`

**Expected Behavior**:
- Start at position 0
- Read offset 100
- Jump to position 100 (out of bounds)
- Exit after 1 step

**Expected Output**: `1 step`

**Test Code**:
```python
def test_large_forward_jump():
    instructions = [100, 1, 1]
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    assert steps == 1, f"Expected 1 step, got {steps}"
    print("✓ Large forward jump test passed")
```

---

### 7. Correctness Test: Offset Modification Order
**Purpose**: Ensure we read the offset BEFORE incrementing it

**Input**: `[1, 1]`

**Expected Behavior**:
- Step 0: pos=0, READ 1 (not 2!), increment to 2, jump to pos 1
- Step 1: pos=1, read 1, increment to 2, jump to pos 2 (out of bounds)

**Expected Output**: `2 steps`

**Critical**: If we increment before reading, we'd read 2, jump to pos 2, and exit in 1 step (WRONG)

**Test Code**:
```python
def test_modification_order():
    instructions = [1, 1]
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]  # Read FIRST
        instructions[position] += 1        # Then modify
        position += offset                 # Jump using original value
        steps += 1

    assert steps == 2, f"Expected 2 steps, got {steps}"
    print("✓ Modification order test passed")
```

---

### 8. Complex Pattern Test: Oscillation
**Purpose**: Test a pattern that jumps back and forth before escaping

**Input**: `[2, -1, 0]`

**Expected Trace**:
- Step 0: pos=0, read 2, inc to 3, jump to 2 → [3,-1,0]
- Step 1: pos=2, read 0, inc to 1, jump to 2 → [3,-1,1]
- Step 2: pos=2, read 1, inc to 2, jump to 3 → [3,-1,2] → EXIT

**Expected Output**: `3 steps`

**Test Code**:
```python
def test_oscillation_pattern():
    instructions = [2, -1, 0]
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    assert steps == 3, f"Expected 3 steps, got {steps}"
    print("✓ Oscillation pattern test passed")
```

---

### 9. Full Input Test
**Purpose**: Verify the algorithm completes successfully on the actual input

**Input**: The full 1038-instruction input from `input.md`

**Expected Behavior**:
- Algorithm completes without errors
- Returns a positive integer
- Completes in reasonable time (< 1 second expected)

**Validation**:
- No specific expected output (we don't know the answer beforehand)
- Check that result is > 0
- Check that result is reasonable (not absurdly large)
- Verify no infinite loop (set a safety timeout if needed)

**Test Code**:
```python
def test_full_input():
    import time

    with open('input.md', 'r') as f:
        instructions = [int(line.strip()) for line in f if line.strip()]

    position = 0
    steps = 0
    start_time = time.time()

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    elapsed_time = time.time() - start_time

    assert steps > 0, "Step count should be positive"
    assert elapsed_time < 10, f"Took too long: {elapsed_time}s"

    print(f"✓ Full input test passed: {steps} steps in {elapsed_time:.3f}s")
    return steps
```

---

### 10. Verification: List Modification Persistence
**Purpose**: Ensure modifications to the list persist across iterations

**Input**: `[0, 1, 0]`

**Expected Behavior**:
- The list should be modified in-place
- Changes from previous iterations should be visible in later iterations

**Manual Trace**:
- Step 0: pos=0, read 0, modify to 1, jump to 0 → [1,1,0]
- Step 1: pos=0, read 1 (was modified!), modify to 2, jump to 1 → [2,1,0]
- Step 2: pos=1, read 1, modify to 2, jump to 2 → [2,2,0]
- Step 3: pos=2, read 0, modify to 1, jump to 2 → [2,2,1]
- Step 4: pos=2, read 1, modify to 2, jump to 3 → EXIT

**Expected Output**: `5 steps`

**Test Code**:
```python
def test_modification_persistence():
    instructions = [0, 1, 0]
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    # Verify the list was actually modified
    assert instructions != [0, 1, 0], "List should be modified"
    assert steps == 5, f"Expected 5 steps, got {steps}"
    print("✓ Modification persistence test passed")
```

---

## Test Execution Plan

### Phase 1: Unit Tests
Run all individual test cases (Tests 1-8, 10) in sequence:
1. Example test
2. Edge cases (immediate exit, backward exit, zeros, large jump)
3. Correctness tests (modification order, persistence)
4. Complex pattern tests

**Success Criteria**: All tests pass with expected step counts

### Phase 2: Integration Test
Run the full input test (Test 9):
1. Execute with actual input file
2. Verify completion and reasonable performance
3. Record the actual answer for the problem

**Success Criteria**:
- Completes without error
- Returns positive integer
- Completes in < 10 seconds

### Phase 3: Manual Verification
If possible, verify the example case by hand or with detailed logging:
1. Add print statements to trace execution for the example input
2. Verify each step matches the expected trace from the problem statement

**Success Criteria**: Trace matches problem specification exactly

## Test Implementation Structure

```python
def run_all_tests():
    print("Running Jump Instruction Maze Tests...")
    print("=" * 50)

    # Phase 1: Unit tests
    test_example()
    test_immediate_exit()
    test_backward_exit()
    test_zero_offset()
    test_multiple_zeros()
    test_large_forward_jump()
    test_modification_order()
    test_oscillation_pattern()
    test_modification_persistence()

    print("=" * 50)

    # Phase 2: Integration test
    result = test_full_input()

    print("=" * 50)
    print(f"All tests passed! Final answer: {result}")

if __name__ == "__main__":
    run_all_tests()
```

## Critical Verification Points

### Must Verify
1. ✓ Offset is read BEFORE incrementing
2. ✓ Position is updated using the ORIGINAL offset value
3. ✓ Offset is incremented AFTER reading but BEFORE jumping
4. ✓ Exit condition checks both negative and beyond-end bounds
5. ✓ Step counter increments exactly once per iteration
6. ✓ List modifications persist across iterations

### Common Pitfalls to Avoid
- ❌ Incrementing before reading (changes which offset value is used)
- ❌ Forgetting to increment the offset
- ❌ Incrementing the offset at the destination instead of source
- ❌ Only checking one boundary condition (negative OR beyond-end)
- ❌ Off-by-one errors in step counting
- ❌ Creating a new list instead of modifying in-place

## Expected Test Results Summary

| Test | Input | Expected Steps | Purpose |
|------|-------|---------------|---------|
| Example | [0,3,0,1,-3] | 5 | Validate against spec |
| Immediate Exit | [5] | 1 | Forward boundary |
| Backward Exit | [-1] | 1 | Backward boundary |
| Zero Offset | [0] | 2 | Self-loop resolution |
| Multiple Zeros | [0,0,0] | 6 | Multiple self-loops |
| Large Jump | [100,1,1] | 1 | Large forward offset |
| Mod Order | [1,1] | 2 | Read before increment |
| Oscillation | [2,-1,0] | 3 | Back-and-forth pattern |
| Persistence | [0,1,0] | 5 | In-place modification |
| Full Input | 1038 instructions | Unknown | Real problem |
