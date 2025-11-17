# Testing Plan: Computer Instruction Simulator

## Testing Strategy Overview

Since we're writing a script to solve a specific problem with given input, our testing should focus on:
1. Verifying correct instruction execution for each operation type
2. Ensuring proper control flow with jumps
3. Validating the solution against the actual input
4. Testing edge cases relevant to the instruction set

We do NOT need to test for:
- Invalid input formats
- Extensive error handling
- Production-grade robustness
- Every possible instruction combination

## Test Categories

### Category 1: Individual Instruction Testing

Test each instruction type in isolation to ensure correct behavior.

#### Test 1.1: Increment (inc)
**Purpose:** Verify register increments by 1 and IP advances

**Test case:**
```
inc a
inc b
```

**Expected behavior:**
- After line 0: a=1, b=0, ip=1
- After line 1: a=1, b=1, ip=2
- Program exits (ip out of bounds)

**Verification:** Check final values: a=1, b=1

#### Test 1.2: Triple (tpl)
**Purpose:** Verify register triples and IP advances

**Test case:**
```
inc a
tpl a
tpl b
```

**Expected behavior:**
- After line 0: a=1, b=0, ip=1
- After line 1: a=3, b=0, ip=2
- After line 2: a=3, b=0, ip=3 (0 * 3 = 0)
- Program exits

**Verification:** Check final values: a=3, b=0

#### Test 1.3: Half (hlf)
**Purpose:** Verify register integer division by 2

**Test case (odd number):**
```
inc a
inc a
inc a
hlf a
```

**Expected behavior:**
- After line 0-2: a=3
- After line 3: a=1 (3 // 2 = 1)

**Verification:** Check a=1 (integer division)

**Test case (even number):**
```
inc a
inc a
inc a
inc a
hlf a
```

**Expected:** a=2 (4 // 2 = 2)

**Test case (zero):**
```
hlf a
```

**Expected:** a=0 (0 // 2 = 0)
**Purpose:** Ensure halving zero doesn't cause issues

### Category 2: Jump Instruction Testing

#### Test 2.1: Unconditional Jump (jmp)
**Purpose:** Verify forward and backward jumps work correctly

**Test case (forward jump):**
```
jmp +2
inc a
inc a
inc b
```

**Expected behavior:**
- Line 0: Jump to line 2 (0 + 2)
- Line 2: inc a → a=1
- Line 3: inc b → b=1
- Program exits

**Verification:** a=1, b=1 (line 1 skipped)

**Test case (backward jump - actually taken):**
```
inc a
inc a
inc b
jie a, -2
inc b
```

**Expected behavior:**
- Line 0: a=1, ip=1
- Line 1: a=2, ip=2
- Line 2: b=1, ip=3
- Line 3: a=2 is even, jump to line 1 (3 + (-2))
- Line 1: a=3, ip=2
- Line 2: b=2, ip=3
- Line 3: a=3 is odd, no jump, ip=4
- Line 4: b=3, ip=5
- Program exits

**Verification:** a=3, b=3 (demonstrates backward jump actually working)

#### Test 2.2: Jump If Even (jie)
**Purpose:** Verify conditional jump based on even/odd

**Test case (even register - jump taken):**
```
inc a
inc a
jie a, +2
inc b
inc b
```

**Expected behavior:**
- After line 0-1: a=2 (even)
- Line 2: a is even, jump to line 4 (2 + 2)
- Program exits

**Verification:** a=2, b=0 (lines 3-4 skipped)

**Test case (odd register - jump not taken):**
```
inc a
jie a, +2
inc b
```

**Expected behavior:**
- After line 0: a=1 (odd)
- Line 1: a is odd, no jump, ip=2
- Line 2: b=1

**Verification:** a=1, b=1

**Test case (zero is even - jump taken):**
```
jie a, +2
inc b
inc b
```

**Expected behavior:**
- Line 0: a=0 (even), jump to line 2
- Program exits

**Verification:** a=0, b=0 (zero is treated as even, jump is taken)

#### Test 2.3: Jump If One (jio)
**Purpose:** Verify conditional jump when register equals 1

**Test case (register equals 1 - jump taken):**
```
inc a
jio a, +2
inc b
inc b
```

**Expected behavior:**
- After line 0: a=1
- Line 1: a==1, jump to line 3 (1 + 2)
- Program exits

**Verification:** a=1, b=0

**Test case (register not 1 - jump not taken):**
```
inc a
inc a
jio a, +2
inc b
```

**Expected behavior:**
- After line 0-1: a=2
- Line 2: a≠1, no jump, ip=3
- Line 3: b=1

**Verification:** a=2, b=1

**Test case (register equals 0 - jump not taken):**
```
jio a, +2
inc b
```

**Expected behavior:**
- Line 0: a==0 (not 1), no jump
- Line 1: b=1

**Verification:** a=0, b=1

### Category 3: Complex Flow Testing

#### Test 3.1: Example from Problem Statement
**Purpose:** Verify the provided example works correctly

**Test case:**
```
inc a
jio a, +2
tpl a
inc a
```

**Expected behavior:**
- Line 0: a=1, ip=1
- Line 1: a==1, jump to line 3 (1 + 2)
- Line 3: a=2, ip=4
- Program exits

**Verification:** a=2, b=0

#### Test 3.2: Simple Loop with Counter
**Purpose:** Test a simple loop that counts iterations

**Test case:**
```
inc a
inc a
inc a
inc a
inc b
hlf a
jio a, +2
jmp -2
```

**Expected behavior:**
- Lines 0-3: a=4
- Line 4: b=1, ip=5
- Line 5: a=2, ip=6
- Line 6: a≠1, no jump, ip=7
- Line 7: jump to line 5 (7 + (-2))
- Line 5: a=1, ip=6
- Line 6: a==1, jump to line 8 (6 + 2)
- Program exits

**Expected result:** a=1, b=1
**Verification:** Demonstrates loop with halving and exit condition

### Category 4: Boundary Condition Testing

#### Test 4.1: Program Termination (Forward)
**Purpose:** Verify program exits when IP exceeds last instruction

**Test case:**
```
inc a
jmp +1
```

**Expected behavior:**
- Line 0: a=1, ip=1
- Line 1: jump to line 2 (1 + 1)
- ip=2, which is out of bounds (only lines 0-1 exist)
- Program exits

**Verification:** a=1, program terminates correctly

#### Test 4.2: Program Termination (Backward)
**Purpose:** Verify program exits when IP goes negative

**Test case:**
```
jmp -1
```

**Expected behavior:**
- Line 0: jump to line -1 (0 + (-1))
- ip=-1, which is out of bounds
- Program exits

**Verification:** a=0, b=0, program terminates correctly

#### Test 4.3: Immediate Jump to End
**Purpose:** Verify large forward jump to exit

**Test case:**
```
jmp +10
inc a
```

**Expected behavior:**
- Line 0: jump to line 10 (0 + 10)
- ip=10, out of bounds (only 2 lines)
- Program exits

**Verification:** a=0, b=0

### Category 5: Register Independence Testing

#### Test 5.1: Operations on Different Registers
**Purpose:** Verify operations on register 'a' don't affect register 'b' and vice versa

**Test case:**
```
inc a
inc a
inc b
tpl a
tpl b
```

**Expected behavior:**
- After line 0-1: a=2, b=0
- After line 2: a=2, b=1
- After line 3: a=6, b=1
- After line 4: a=6, b=3

**Verification:** Ensure a and b maintain independent values

### Category 6: Actual Input Validation

#### Test 6.1: Run Against Actual Input
**Purpose:** Solve the actual problem with the given input

**Test case:** Use the provided input.md file

**Execution steps:**
1. Run the simulation with the full input
2. Observe the final value of register b
3. Verify the program terminates (doesn't loop infinitely)

**Validation methods:**
- Add optional debug output to trace execution (can be disabled for final run)
- Count number of instructions executed (should be finite)
- Verify program exits cleanly with IP out of bounds
- Check that the result is a reasonable non-negative integer

**Manual verification approach:**
1. Trace first few instructions manually to ensure correct parsing
2. Verify the jump at line 0 behaves correctly (jio a, +22 with a=0)
3. Check that line 22's jmp +19 lands at correct position (line 41)
4. Observe the loop structure at the end (lines 42-48)

#### Test 6.2: Execution Sanity Checks
**Purpose:** Ensure simulation doesn't run indefinitely

**Implementation:**
The simulate function should include an infinite loop guard:
```python
def simulate(instruction_strings):
    instructions = [parse_instruction(line) for line in instruction_strings]
    registers = {'a': 0, 'b': 0}
    ip = 0

    MAX_ITERATIONS = 1_000_000
    iteration_count = 0

    while 0 <= ip < len(instructions):
        if iteration_count > MAX_ITERATIONS:
            raise RuntimeError(f"Possible infinite loop: exceeded {MAX_ITERATIONS} iterations")
        iteration_count += 1
        ip = execute_instruction(instructions[ip], ip, registers)

    return registers
```

**Checks:**
- For this specific input, execution should complete in < 100,000 steps
- If MAX_ITERATIONS is exceeded, the error message will indicate potential infinite loop
- During development, can lower MAX_ITERATIONS to catch issues faster

### Category 7: Parsing Validation

#### Test 7.1: Instruction Format Parsing
**Purpose:** Verify all instruction formats parse correctly

**Implementation:**
```python
def test_parsing():
    """Test that parsing works for all instruction formats"""
    test_cases = [
        ('hlf a', ('hlf', 'a', None)),
        ('tpl b', ('tpl', 'b', None)),
        ('inc a', ('inc', 'a', None)),
        ('jmp +19', ('jmp', None, 19)),
        ('jmp -7', ('jmp', None, -7)),
        ('jie a, +4', ('jie', 'a', 4)),
        ('jio b, -3', ('jio', 'b', -3)),
    ]

    for input_str, expected in test_cases:
        result = parse_instruction(input_str)
        assert result == expected, f"Parse failed: {input_str} → {result}, expected {expected}"
        print(f"✓ Parsed '{input_str}' correctly")

    print("All parsing tests passed!")
    return True
```

**Verification:** Run test_parsing() to verify all instruction formats parse correctly

## Testing Execution Plan

### Phase 1: Unit Tests (Recommended for Core Instructions)
Create simple test cases for each instruction type and verify individually.

**Implementation approach:**
```python
def test_program(program_lines, expected_a, expected_b):
    """Test a program and verify final register values"""
    registers = simulate(program_lines)  # Returns full register dict
    assert registers['a'] == expected_a, f"Expected a={expected_a}, got {registers['a']}"
    assert registers['b'] == expected_b, f"Expected b={expected_b}, got {registers['b']}"
    print(f"✓ Test passed: a={registers['a']}, b={registers['b']}")
    return True
```

**Note:** Since `simulate()` returns the full register dictionary, we can access both `a` and `b` for testing.

**Minimum recommended tests:**
- Test 1.1 (inc)
- Test 1.2 (tpl)
- Test 1.3 (hlf) - including zero edge case
- Test 2.2 (jie) - including zero edge case
- Test 2.3 (jio) - including zero edge case
- Test 3.1 (problem example)
- Test 4.1 (forward termination)
- Test 4.2 (backward termination)

### Phase 2: Parsing Validation (Required)
Run test_parsing() to ensure all instruction formats are handled correctly.
- This catches parsing bugs before they cause mysterious execution errors

### Phase 3: Integration Test with Example (Required)
Run the example from the problem statement and verify output.
- Test 3.1: Example must produce a=2, b=0
- This validates the complete execution pipeline

### Phase 4: Actual Input Execution (Required)
Run against the actual input and observe:
1. Program terminates (no infinite loop)
2. Final value of register b is computed
3. Result is a non-negative integer
4. Execution completes in < 100,000 iterations

### Phase 5: Manual Verification (Optional - for debugging)
If the result seems wrong, manually trace the first 10 instructions:
- Instruction 0: jio a, +22 (a=0, so no jump, go to line 1)
- Instruction 1: inc a (a=1)
- Instruction 2: tpl a (a=3)
- Instruction 3: tpl a (a=9)
- ... and so on

Can add DEBUG flag to see execution trace:
```python
DEBUG = True  # Enable during debugging
```

## Success Criteria

The solution is correct if:
1. ✅ All individual instruction types work correctly (inc, tpl, hlf)
2. ✅ Jump offsets are calculated correctly (relative to current position)
3. ✅ Conditional jumps evaluate conditions properly (jie, jio, jmp)
4. ✅ Program terminates when IP goes out of bounds (< 0 or >= len)
5. ✅ The example from problem statement produces correct result (a=2, b=0)
6. ✅ The actual input produces a non-negative integer for register b
7. ✅ No infinite loops occur (execution completes in < 100,000 iterations)
8. ✅ Both registers maintain independent state throughout execution
9. ✅ Edge cases handled: zero register values, backward jumps, immediate termination

## Debug Output (Optional)
For development/debugging, add optional trace output at the top of solution file:
```python
DEBUG = False  # Set to True for debugging

# In simulate() function:
if DEBUG:
    print(f"IP={ip:3d} | {instruction_strings[ip]:20s} | a={registers['a']:10d}, b={registers['b']:10d}")
```

This helps verify execution flow without implementing a full test suite. Particularly useful for:
- Tracing the first 20-30 instructions to verify initial behavior
- Watching loop iterations to ensure they progress correctly
- Identifying where the program terminates

## Final Validation
The ultimate test is: **Does the solution produce the correct answer for the given input?**

Since this is an Advent of Code style problem, the correctness is validated by:
1. Running the program
2. Getting the value of register b
3. Verifying the result is reasonable:
   - Non-negative integer
   - Program terminated normally (not via MAX_ITERATIONS)
   - Execution trace (if enabled) shows sensible behavior

## Summary of Required vs Optional Testing

**Required (Must implement):**
- Phase 2: Parsing validation
- Phase 3: Problem example test (a=2, b=0)
- Phase 4: Run actual input and get result
- Infinite loop protection (MAX_ITERATIONS guard)

**Recommended (Should implement at least 2-3):**
- Test 1.1-1.3: Basic instruction tests
- Test 2.2-2.3: Conditional jump tests with edge cases
- Test 4.1-4.2: Termination tests

**Optional (Only if debugging issues):**
- Test 3.2: Complex loop test
- Test 5.1: Register independence
- Phase 5: Manual execution tracing
- Debug output mode

This testing approach balances thoroughness with practicality for a script-level solution.
