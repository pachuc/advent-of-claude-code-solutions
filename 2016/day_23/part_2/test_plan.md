# Testing Plan for Part 2

## Overview
Part 2 modifies Part 1 by changing the initial register value from 7 to 12. The critical challenge is performance - without optimization, the program would run for hours or days. Our testing strategy must verify both correctness and performance.

## Testing Objectives
1. **Correctness**: Verify the interpreter executes all instructions properly with a=12
2. **Optimization validity**: Ensure optimized execution produces same result as unoptimized (for small values)
3. **Performance**: Confirm the solution completes in reasonable time (<5 seconds)
4. **Edge cases**: Test instruction toggling and invalid instructions

## Expected Results
- **Part 1 (a=7)**: Result = **11340** (verified from part_1_answer.txt, completed in Part 1)
- **Part 2 (a=12)**: Result ≈ **479,007,900** (calculated as 12! + 84*75)
- **Performance**: Optimized solution should complete in <1 second

## Test Strategy

### Phase 1: Regression Testing
**Objective**: Ensure our modifications don't break the working Part 1 solution

**Test 1.1: Reproduce Part 1 Answer**
- **Input**: Original input with `initial_a=7`
- **Expected output**: `11340` (from part_1_answer.txt)
- **Method**:
  ```python
  interpreter = AssembunnyInterpreter(initial_a=7)
  interpreter.parse_instructions(input_text)
  result = interpreter.run()
  assert result == 11340, f"Expected 11340, got {result}"
  ```
- **Pass criteria**: Result matches exactly
- **Why important**: Regression test - ensures we didn't break existing functionality

**Test 1.2: Part 1 Example with Toggle**
- **Input**: The example from Part 1 problem statement with a=2
  ```
  cpy 2 a
  tgl a
  tgl a
  tgl a
  cpy 1 a
  dec a
  dec a
  ```
- **Expected output**: `a = 3`
- **Method**: Run interpreter and verify result
- **Pass criteria**: Matches expected output
- **Why important**: Ensures toggle logic still works correctly (moved from Phase 3 per critique)

### Phase 2: Test Optimization Correctness
**Objective**: Verify that optimization produces identical results to naive execution

**Test 2.1: Small Input Comparison**
- **Input**: Original input with small initial_a value
- **Method**: Run both optimized and unoptimized versions, starting with a=7
  ```python
  # First, try a=7 to see if unoptimized completes in reasonable time (60 seconds)
  # If it times out, fall back to a=3
  test_value = 7  # or 3 if a=7 is too slow

  # Optimized version
  interp_opt = AssembunnyInterpreter(initial_a=test_value, optimize=True)
  interp_opt.parse_instructions(input_text)
  result_opt = interp_opt.run()

  # Unoptimized version (test with timeout)
  interp_no_opt = AssembunnyInterpreter(initial_a=test_value, optimize=False)
  interp_no_opt.parse_instructions(input_text)
  result_no_opt = interp_no_opt.run()  # May take 30-60 seconds for a=7

  assert result_opt == result_no_opt, f"Results differ: {result_opt} vs {result_no_opt}"
  ```
- **Pass criteria**: Both produce identical results
- **Why important**: Validates optimization doesn't change semantics
- **Note**: Part 1 completed with a=7 (result 11340), suggesting a=7 unoptimized may be feasible. If it takes >60 seconds, use a=3 instead.

**Test 2.2: Minimal Multiplication Pattern**
- **Input**: Simplified program with just a multiplication pattern
  ```
  cpy 5 b
  cpy 3 d
  cpy 0 a
  cpy b c
  inc a
  dec c
  jnz c -2
  dec d
  jnz d -5
  ```
- **Expected output**: `a = 15` (5 * 3), `c = 0`, `d = 0`
- **Method**: Run and verify final register states
  ```python
  assert interpreter.registers['a'] == 15
  assert interpreter.registers['c'] == 0
  assert interpreter.registers['d'] == 0
  ```
- **Pass criteria**: Correct multiplication result and final register states
- **Why important**: Isolates optimization logic from rest of interpreter

**Test 2.3: Multiplication with Zero**
- **Input**: Pattern where one factor is 0
  ```
  cpy 0 b
  cpy 5 d
  cpy 0 a
  [multiplication pattern]
  ```
- **Expected output**: `a = 0` (0 * 5)
- **Pass criteria**: Result is 0
- **Why important**: Tests edge case of zero multiplication

**Test 2.4: Nested Patterns**
- **Input**: Multiple multiplication patterns in sequence
- **Method**: Verify each pattern is detected and optimized correctly
- **Pass criteria**: Correct final result
- **Why important**: Ensures optimization works repeatedly in same program

### Phase 3: Test Toggle Instruction Interaction
**Objective**: Verify optimization is disabled when code is modified and that actual input handles toggles correctly

**Test 3.1: Actual Input with Toggles**
- **Input**: The actual input (which contains `tgl` instructions) with a=12
- **Method**: Run the full solution and verify it completes correctly
- **Pass criteria**:
  - Completes successfully
  - Result is close to expected value (479,007,900)
  - No crashes or errors
- **Why important**: The actual input uses `tgl` instructions, so this verifies toggle interaction works in practice. Simpler than constructing artificial test cases.

### Phase 4: Test Invalid Instructions
**Objective**: Verify invalid instructions are skipped properly

**Test 4.1: Invalid CPY Destination**
- **Input**: Program with `cpy 5 5` (number as destination)
- **Method**: Verify instruction is skipped, no crash
- **Pass criteria**: Program completes without error
- **Why important**: Tests error handling for toggled instructions

**Test 4.2: Invalid INC/DEC**
- **Input**: Program with `inc 5` (literal instead of register)
- **Method**: Verify instruction is skipped
- **Pass criteria**: No crash, correct result
- **Why important**: Tests robustness of instruction validation

### Phase 5: Performance Testing
**Objective**: Verify solution completes in reasonable time

**Test 5.1: Actual Part 2 Input (a=12)**
- **Input**: Actual input with `initial_a=12`
- **Method**:
  ```python
  import time
  start = time.time()
  result = interpreter.run()
  elapsed = time.time() - start
  print(f"Result: {result}, Time: {elapsed:.2f}s")
  ```
- **Pass criteria**:
  - Completes in <5 seconds (well-optimized should be <1 second)
  - Produces a valid integer result close to 479,007,900
- **Why important**: Main test - verifies optimization makes problem solvable

**Test 5.1b: Verify Optimization is Applied**
- **Input**: Same as above
- **Method**: Performance is the indicator - if it completes in <1 second, optimization clearly worked
- **Alternative (optional)**: Add debug print in `try_optimize_multiplication()` when pattern is detected
  ```python
  # In try_optimize_multiplication(), before returning True:
  # print(f"Optimizing multiplication at PC={self.pc}")
  ```
- **Pass criteria**: Either completes in <1 second OR (if debug enabled) prints optimization messages
- **Why important**: Confirms optimization is actually being triggered
- **Note**: Performance alone is sufficient indicator; instrumentation is optional

**Test 5.2: Performance Comparison**
- **Input**: Run with a=7 (optimized) and measure time
- **Method**: Time execution
- **Expected**: Sub-second execution (since a=7 worked in Part 1)
- **Pass criteria**: Fast completion
- **Why important**: Baseline performance measurement

### Phase 6: Boundary and Edge Cases
**Objective**: Test unusual but valid scenarios

**Test 6.1: Jump Out of Bounds**
- **Input**: `jnz 1 1000` (jump far beyond program end)
- **Method**: Verify program terminates cleanly
- **Pass criteria**: No crash, program exits
- **Why important**: Tests bounds checking

**Test 6.2: Toggle Out of Bounds**
- **Input**: `tgl 1000` (toggle beyond program)
- **Method**: Verify no crash, nothing toggled
- **Pass criteria**: Instruction is no-op, program continues
- **Why important**: Tests toggle bounds checking

**Test 6.3: Backward Jump**
- **Input**: Program with `jnz 1 -100` (jump before start)
- **Method**: Verify program terminates or loops correctly
- **Pass criteria**: Correct behavior per specification
- **Why important**: Tests negative jump handling

**Test 6.4: Empty Program**
- **Input**: Empty instruction list
- **Method**: Run interpreter
- **Expected output**: `a = 12` (initial value, unchanged)
- **Pass criteria**: Returns initial value
- **Why important**: Tests minimal input case

**Test 6.5: Optimization at Program End**
- **Input**: Multiplication pattern that extends to last instruction
- **Method**: Verify bounds checking works
- **Pass criteria**: No index out of bounds error
- **Why important**: Tests pattern detection boundary conditions

### Phase 7: Register State Verification
**Objective**: Verify register values are correct (for debugging if needed)

**Test 7.1: Final Register Values (a=12)**
- **Input**: Actual Part 2 input
- **Method**: After execution, optionally print register values for sanity check
  ```python
  result = interpreter.run()
  print(f"Final registers: {interpreter.registers}")
  ```
- **Pass criteria**: Register `a` contains final answer, reasonable values in other registers
- **Why important**: Optional sanity check on execution
- **Note**: This is a debug-only test, not essential for validation

### Phase 8: Integration Test
**Objective**: End-to-end test of complete solution

**Test 8.1: Full Part 2 Solution**
- **Input**: Read from `input.md` file
- **Method**: Run complete `main()` function
  ```bash
  python solution.py
  ```
- **Expected output**: Single integer printed to stdout
- **Pass criteria**:
  - Executes without error
  - Outputs a valid integer (close to 479,007,900)
- **Why important**: Validates complete solution end-to-end
- **Note**: Performance is covered by Test 5.1; this focuses on I/O and integration

**Test 8.2: Input File Reading**
- **Method**: Verify file is read correctly, handles newlines/whitespace
- **Pass criteria**: All instructions parsed correctly
- **Why important**: Tests file I/O robustness

## Test Execution Order

**Priority 1 - Essential Tests (Must Pass)**:
1. **Test 1.1** - Reproduce Part 1 answer (11340)
2. **Test 1.2** - Part 1 toggle example
3. **Test 2.2** - Minimal multiplication pattern
4. **Test 5.1** - Main Part 2 test with a=12 (performance + correctness)

**Priority 2 - Validation Tests (Recommended)**:
5. **Test 2.1** - Optimization correctness comparison (if a=7 unoptimized completes)
6. **Test 3.1** - Actual input with toggles (covered by 5.1, optional separate run)
7. **Test 4.1-4.2** - Invalid instructions

**Priority 3 - Optional Tests**:
8. **Phase 6** - Edge cases (only if suspicious of bugs)
9. **Phase 8** - Integration (covered by running solution, optional)
10. **Phase 7** - Debug only if problems found

**Note**: Phase 5 (performance test) is run early because with optimization it should complete quickly. If it times out, we know optimization failed and can debug immediately.

## Success Criteria

### Minimum Viable Solution (Must Pass)
- ✅ Test 1.1: Part 1 regression - Result = 11340
- ✅ Test 1.2: Toggle example works correctly
- ✅ Test 2.2: Minimal multiplication pattern works
- ✅ Test 5.1: Part 2 with a=12 completes in <5 seconds
- ✅ Result is close to 479,007,900 (±10,000 for potential calculation variations)

### Full Validation (Ideal)
- ✅ All Priority 1 and Priority 2 tests pass
- ✅ Performance test completes in <1 second (well-optimized)
- ✅ No crashes or exceptions
- ✅ Result matches expected answer closely

## Expected Test Results

Based on the problem analysis:

**Part 1 (a=7)**: Result = **11340** ✓ (verified from part_1_answer.txt)

**Part 2 (a=12)**: Result ≈ **479,007,900** (calculated as follows)
- Lines 1-10 compute factorial: 12! = 479,001,600
- Lines 20-26 add constant: 84 * 75 = 6,300
- **Expected total**: 479,001,600 + 6,300 = **479,007,900**

**Why this formula**:
- Lines 1-4: Setup (b = a-1, d = a, a = 0)
- Lines 5-10: Multiplication pattern computes factorial of initial a
- Lines 11-19: Control flow and setup for final addition
- Lines 20-26: Second multiplication pattern adds 84 * 75

## Debugging Strategy

If tests fail:

1. **Wrong result for a=7**: Implementation error, review instruction execution
2. **Timeout for a=12**: Optimization not working, verify pattern detection
3. **Different results (opt vs no-opt)**: Bug in optimization, check arithmetic
4. **Crash**: Bounds checking issue, review array access and PC management
5. **Toggle test failure**: Issue with instruction modification tracking

## Manual Verification Steps

1. **Inspect pattern detection**: Add print statements when pattern is detected
   ```python
   if pattern_detected:
       print(f"Optimizing multiplication at PC={self.pc}")
   ```

2. **Count optimizations**: Track how many times optimization is applied
   ```python
   self.optimization_count = 0
   # In optimization code:
   self.optimization_count += 1
   ```

3. **Compare instruction counts**: Optimized vs unoptimized execution
   ```python
   self.instruction_count = 0
   # In run loop:
   self.instruction_count += 1
   ```

## Test Coverage Summary

| Category | Test Cases | Priority |
|----------|-----------|----------|
| Regression | 1 | High |
| Optimization Correctness | 4 | High |
| Toggle Interaction | 2 | High |
| Invalid Instructions | 2 | Medium |
| Performance | 2 | High |
| Edge Cases | 5 | Medium |
| Register State | 2 | Low (debug) |
| Integration | 2 | High |
| **Total** | **20** | - |

## Automated Test Script Structure

```python
def test_part1_regression():
    """Test 1.1"""
    # Implementation

def test_optimization_correctness():
    """Tests 2.1-2.4"""
    # Implementation

def test_toggle_interaction():
    """Tests 3.1-3.2"""
    # Implementation

def test_performance():
    """Tests 5.1-5.2"""
    # Implementation

def run_all_tests():
    tests = [
        test_part1_regression,
        test_optimization_correctness,
        test_toggle_interaction,
        test_performance
    ]
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
```

## Time Estimates

- **Priority 1 Tests**: <5 seconds total (all 4 essential tests with optimization)
- **Priority 2 Tests**: 5-60 seconds (depends on whether a=7 unoptimized completes; may need to use a=3)
- **Priority 3 Tests**: <10 seconds (optional edge cases)

**Total estimated test time for essential tests**: <5 seconds
**Total estimated test time including validation**: 10-70 seconds

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Optimization incorrect | Wrong answer | Test 2.1 - compare with unoptimized |
| Pattern not detected | Timeout | Add debug logging for pattern detection |
| Toggle breaks optimization | Wrong answer | Test 3.1 - verify modified_instructions tracking |
| Off-by-one in pattern | Wrong answer | Test 2.2 - isolated multiplication test |
| Bounds checking error | Crash | Test 6.x - various boundary conditions |

## Final Validation Checklist

Before submitting solution:

- [ ] Part 1 answer reproduced (11340)
- [ ] Part 2 completes in <60 seconds
- [ ] Result is a positive integer
- [ ] No exceptions or crashes
- [ ] Toggle functionality works
- [ ] Invalid instructions skipped
- [ ] Optimization applied (verify via debug output)
- [ ] Code is readable and commented

## Quick Validation Strategy

For rapid validation, run these tests in order:

### Essential Tests Only (Priority 1)
Run these 4 tests to achieve 90% confidence:

1. **Test 1.1** - Reproduce Part 1 (a=7, expect 11340)
2. **Test 1.2** - Toggle example (a=2, expect 3)
3. **Test 2.2** - Minimal multiplication (expect 15)
4. **Test 5.1** - Part 2 main test (a=12, expect ~479,007,900 in <5 sec)

**Estimated time**: <5 seconds total

If all pass, solution is very likely correct.

### Additional Validation (Priority 2)
If you have more time or want higher confidence:

5. **Test 2.1** - Compare optimized vs unoptimized (a=7 or a=3)
6. **Test 4.1-4.2** - Invalid instruction handling

**Estimated time**: +5-60 seconds

### Debug Only (If Problems Found)
- Check if optimization is triggered (add debug print)
- Verify register states at key points
- Test with smaller values (a=2, a=3) to trace execution
