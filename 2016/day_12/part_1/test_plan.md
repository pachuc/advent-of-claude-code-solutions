# Test Plan: Assembunny Code Interpreter

## Overview
Verify that the assembunny interpreter correctly executes instructions and produces the right value in register `a` for various test cases.

## Testing Strategy
Since this is a script to solve a specific problem, we focus on:
1. Correctness of the example case from the problem
2. Individual instruction correctness
3. Edge cases relevant to the instruction set
4. Final verification with the actual input

## Test Cases

### Test 1: Example from Problem Statement
**Purpose:** Verify basic functionality with the provided example

**Input:**
```
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
```

**Expected Output:** `42`

**What this tests:**
- `cpy` with literal value
- `inc` instruction
- `dec` instruction
- `jnz` with forward jump
- Program termination

**Manual trace:**
1. a=41, b=0, c=0, d=0, ip=0
2. a=42, ip=1
3. a=43, ip=2
4. a=42, ip=3
5. 42≠0, jump +2, ip=6
6. Program ends, a=42 ✓

### Test 2: Copy Register to Register
**Purpose:** Verify `cpy` works with register as source

**Input:**
```
cpy 10 a
cpy a b
cpy b c
```

**Expected Output:** `10` (and b=10, c=10 if we check)

**What this tests:**
- Chaining register copies
- Register-to-register data flow

### Test 3: Jump with Zero (No Jump)
**Purpose:** Verify `jnz` doesn't jump when value is zero

**Input:**
```
cpy 0 a
jnz a 5
inc a
inc a
inc a
```

**Expected Output:** `3`

**Manual trace:**
1. a=0, ip=0
2. a=0, jnz check: 0==0, no jump, ip=2
3. a=1, ip=3
4. a=2, ip=4
5. a=3, ip=5
6. Program ends, a=3 ✓

**What this tests:**
- `jnz` conditional logic when condition is false
- Sequential execution continues normally

### Test 4: Backward Jump (Loop)
**Purpose:** Verify backward jumps create loops correctly

**Input:**
```
cpy 5 a
dec a
jnz a -1
```

**Expected Output:** `0`

**Manual trace:**
1. a=5, ip=0 → ip advances to 1
2. a=4, ip=1 → ip advances to 2
3. a=4≠0, jump -1: ip=2+(-1)=1
4. a=3, ip=1 → ip advances to 2
5. a=3≠0, jump -1: ip=2+(-1)=1
6. a=2, ip=1 → ip advances to 2
7. a=2≠0, jump -1: ip=2+(-1)=1
8. a=1, ip=1 → ip advances to 2
9. a=1≠0, jump -1: ip=2+(-1)=1
10. a=0, ip=1 → ip advances to 2
11. a=0==0, no jump, ip advances to 3
12. Program ends, a=0 ✓

**What this tests:**
- Negative jump offsets
- Loop construction
- Loop termination when condition becomes false

### Test 5: Nested Loops (Simple Multiplication)
**Purpose:** Verify nested loops work correctly (similar to actual input structure)

**Input:**
```
cpy 3 a
cpy 2 b
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec c
jnz c -5
```

**Expected Output:** `9`

**What this tests:**
- Nested loop structures
- Register usage across loops
- Complex control flow

**Manual trace (first iteration):**
1. a=3, b=0, c=0, d=0, ip=0
2. a=3, b=2, ip=1
3. a=3, b=2, c=3, ip=2
4. Inner loop iteration 1: a=4, b=1, ip=3,4,5 (jump to ip=3)
5. Inner loop iteration 2: a=5, b=0, ip=3,4,5 (no jump)
6. After inner loop: a=5, b=3 (restored from c), c=2, ip=6,7,8 (jump to ip=3)
7. Outer loop continues with c=2, then c=1, then c=0
8. Final: a=9 (3 + 2*3 = 3 + 6 = 9), program ends

**Calculation:** The program effectively computes: a + (b × c) = 3 + (2 × 3) = 9

### Test 6: Jump Past End of Program
**Purpose:** Verify program terminates when jumping beyond last instruction

**Input:**
```
cpy 5 a
jnz a 10
inc a
```

**Expected Output:** `5`

**What this tests:**
- Large forward jump
- Program termination when ip exceeds instruction count
- No crash or infinite loop

### Test 7: All Registers Used
**Purpose:** Verify all four registers work independently

**Input:**
```
cpy 1 a
cpy 2 b
cpy 3 c
cpy 4 d
inc a
inc b
inc c
inc d
```

**Expected Output:** `2` (and b=3, c=4, d=5)

**What this tests:**
- All four registers are independent
- No register interference
- Multiple registers can be modified

### Test 8: Decrement Below Zero
**Purpose:** Verify registers can hold negative values

**Input:**
```
cpy 0 a
dec a
dec a
```

**Expected Output:** `-2`

**What this tests:**
- Registers are true integers (not unsigned)
- Negative values are handled correctly

### Test 9: Jump with Register Offset
**Purpose:** Verify `jnz` can use register value as jump offset

**Input:**
```
cpy 2 b
cpy 1 a
jnz a b
inc a
inc a
```

**Expected Output:** `1`

**What this tests:**
- Second argument of `jnz` can be a register
- Jump offset correctly read from register

### Test 10: Actual Input
**Purpose:** Solve the actual problem

**Input:** The full input from input.md

**Expected Output:** (Unknown - this is what we're solving for)

**Verification approach:**
1. Run the interpreter with actual input
2. Check that program terminates (doesn't infinite loop)
3. Record the result
4. Optionally: Add debug output to verify reasonable intermediate values

**Additional checks:**
- Execution completes in reasonable time (< 5 seconds)
- No crashes or exceptions
- Result is a reasonable integer value

## Edge Cases Considered

### Not Applicable for This Problem:
- Empty input (problem guarantees ~23 lines)
- Invalid instructions (we trust input is valid)
- Invalid register names (we trust input is valid)
- Concurrent execution (single-threaded only)

### Relevant Edge Cases Covered Above:
- ✓ Zero values in conditionals
- ✓ Negative register values
- ✓ Backward jumps
- ✓ Forward jumps
- ✓ Jump offsets from registers
- ✓ Nested loops
- ✓ Program termination conditions

## Test Execution Plan

### Phase 1: Unit Testing (Optional but Recommended)
Test individual functions:
1. `get_value()` with literals and registers
2. `parse_instructions()` with various instruction formats

### Phase 2: Integration Testing
Run test cases 1-9 in order:
1. Create a test input file or string for each test case
2. Run the interpreter
3. Compare output to expected value
4. Mark pass/fail

**Execution method:**
```python
def run_test(name, input_str, expected):
    instructions = parse_instructions(input_str.strip().split('\n'))
    result = execute(instructions)
    if result == expected:
        print(f"✓ {name}: PASS")
    else:
        print(f"✗ {name}: FAIL (expected {expected}, got {result})")
```

### Phase 3: Final Verification
1. Run with actual input.md
2. Verify program completes
3. Output the result
4. Manually verify the result makes sense:
   - Should be a positive integer
   - Given the loop structure, likely a large number
   - Should be deterministic (same result each run)

## Success Criteria

**Minimum requirements:**
- ✓ Example test case (Test 1) passes
- ✓ Actual input (Test 10) produces a result without crashing
- ✓ Execution completes in reasonable time

**Full validation:**
- All test cases 1-9 pass
- Code is readable and follows the implementation plan
- No infinite loops or crashes
- Result is reproducible

## Debugging Strategy (If Tests Fail)

1. **Add trace output:**
   - Print instruction pointer and registers after each instruction
   - Verify execution flow matches manual trace

2. **Check specific instruction:**
   - Add print statements in the failing instruction handler
   - Verify operands are parsed correctly

3. **Verify parsing:**
   - Print parsed instruction list
   - Ensure format matches expectations

4. **Check termination:**
   - Print instruction pointer value
   - Verify bounds checking logic

## Time Estimate
- Setting up test cases: 10-15 minutes
- Running tests: < 1 minute
- Debugging (if needed): 5-15 minutes
- Total: ~30 minutes maximum
