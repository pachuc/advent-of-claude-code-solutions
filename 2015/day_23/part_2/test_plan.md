# Test Plan: Computer Instruction Simulator (Part 2)

## Testing Strategy

The goal is to verify that our instruction simulator correctly executes the given program and produces the correct value for register `b`. Since this is a script to solve a specific problem (not production code), we focus on correctness and relevant edge cases.

## Test Categories

### 1. Instruction Parsing Tests

**Objective:** Verify that all instruction types are parsed correctly from the input

**Test Cases:**

1.1. **Single Register Instructions**
- Test: `inc a` → Should parse to ("inc", "a", None)
- Test: `hlf a` → Should parse to ("hlf", "a", None)
- Test: `tpl b` → Should parse to ("tpl", "b", None)

1.2. **Jump Instructions with Offset**
- Test: `jmp +19` → Should parse to ("jmp", None, 19) or ("jmp", 19)
- Test: `jmp -7` → Should parse to ("jmp", None, -7) or ("jmp", -7)

1.3. **Conditional Jump Instructions**
- Test: `jio a, +22` → Should parse to ("jio", "a", 22)
- Test: `jie a, +4` → Should parse to ("jie", "a", 4)
- Test: Handle comma and space separation correctly

**Verification Method:**
- Parse the first 10 lines of input.md manually
- Compare parsed output with expected structure
- Ensure no parsing errors or exceptions

### 2. Individual Instruction Execution Tests

**Objective:** Verify each instruction type works correctly in isolation

**Test Cases:**

2.1. **Halve (hlf) Instruction**
- Initial: a=10, PC=0, Execute: hlf a → Result: a=5, PC=1
- Initial: a=7, PC=0, Execute: hlf a → Result: a=3, PC=1 (integer division)
- Initial: a=1, PC=0, Execute: hlf a → Result: a=0, PC=1

2.2. **Triple (tpl) Instruction**
- Initial: a=5, PC=0, Execute: tpl a → Result: a=15, PC=1
- Initial: b=0, PC=0, Execute: tpl b → Result: b=0, PC=1
- Initial: a=1, PC=0, Execute: tpl a → Result: a=3, PC=1

2.3. **Increment (inc) Instruction**
- Initial: a=0, PC=0, Execute: inc a → Result: a=1, PC=1
- Initial: b=5, PC=0, Execute: inc b → Result: b=6, PC=1

2.4. **Unconditional Jump (jmp)**
- PC=5, Execute: jmp +3 → Result: PC=8 (5+3)
- PC=10, Execute: jmp -5 → Result: PC=5 (10-5)
- PC=20, Execute: jmp +1 → Result: PC=21 (20+1)
- **Key:** Offset is relative to current PC, not next PC

2.5. **Jump If Even (jie)**
- a=4 (even), PC=5, Execute: jie a, +3 → Result: PC=8 (jump taken)
- a=5 (odd), PC=5, Execute: jie a, +3 → Result: PC=6 (jump not taken, increment)
- a=0 (even), PC=10, Execute: jie a, +2 → Result: PC=12 (0 is even)
- a=2 (even), PC=10, Execute: jie a, -3 → Result: PC=7 (negative jump)

2.6. **Jump If One (jio)**
- a=1, PC=5, Execute: jio a, +10 → Result: PC=15 (jump taken, a==1)
- a=2, PC=5, Execute: jio a, +10 → Result: PC=6 (jump not taken, a≠1)
- a=0, PC=5, Execute: jio a, +5 → Result: PC=6 (jump not taken, a≠1)
- **Key:** Only jumps when register equals exactly 1

**Verification Method:**
- Create small test programs with 1-3 instructions
- Execute and verify register values and PC position
- Print intermediate states for manual verification

### 3. Simple Program Tests

**Objective:** Test the execution of complete small programs

**Test Case 3.1: Example from Problem Description**
```
inc a
jio a, +2
tpl a
inc a
```
- Initial: a=0, b=0
- Expected: a=2, b=0
- **Correct step-by-step trace:**
  1. PC=0: `inc a` → a=1, PC=1
  2. PC=1: `jio a, +2` → a==1, so PC = 1+2 = 3 (skip `tpl a`)
  3. PC=3: `inc a` → a=2, PC=4
  4. PC=4: Out of bounds, terminate with a=2, b=0

**Test Case 3.2: Simple Loop Test**
```
inc a
jie a, +2
inc b
jmp -2
```
- Initial: a=0, b=0
- **Correct step-by-step trace:**
  1. PC=0: `inc a` → a=1, PC=1
  2. PC=1: `jie a, +2` → a is odd, so PC=2
  3. PC=2: `inc b` → b=1, PC=3
  4. PC=3: `jmp -2` → PC = 3+(-2) = 1
  5. PC=1: `jie a, +2` → a is odd, so PC=2
  6. PC=2: `inc b` → b=2, PC=3
  7. PC=3: `jmp -2` → PC = 1
  8. ... (infinite loop)
- Expected: This creates an infinite loop (for testing max iteration detection)
- Verify max_iterations safety feature triggers

**Test Case 3.3: Initial Condition Test (Part 1 vs Part 2)**
```
jio a, +2
inc b
inc b
```
- **Test with a=0 (Part 1 condition):**
  1. PC=0: `jio a, +2` → a≠1, so PC=1
  2. PC=1: `inc b` → b=1, PC=2
  3. PC=2: `inc b` → b=2, PC=3
  4. PC=3: Out of bounds, terminate with b=2

- **Test with a=1 (Part 2 condition):**
  1. PC=0: `jio a, +2` → a==1, so PC = 0+2 = 2
  2. PC=2: `inc b` → b=1, PC=3
  3. PC=3: Out of bounds, terminate with b=1

- **Purpose:** Verify initial conditions affect control flow correctly

**Verification Method:**
- Manually trace execution step-by-step
- Compare final register values with manual calculation
- Add debug output showing PC and registers at each step

### 4. Full Input Execution Tests

**Objective:** Verify the complete solution with the actual input

**Test Case 4.1: Full Program with a=1 (Part 2)**
- Initial: a=1, b=0
- Execute all 48 instructions from input.md
- Verify program terminates (doesn't loop forever)
- Record final value of register b
- Verify no errors or exceptions occur

**Test Case 4.2: Execution Trace Verification**
- Enable verbose mode for first 10 iterations
- Verify PC movement is correct
- **Critical checks:**
  - First instruction (PC=0): `jio a, +22` should jump to PC=22 (since a=1)
  - Second instruction executed (PC=22): `jmp +19` should jump to PC=41
  - Third instruction executed (PC=41): `jio a, +8` - behavior depends on a value

**Test Case 4.3: Loop Analysis**
- The loop structure is PC=41 to PC=48 (with `jmp -7` going back to PC=41)
- Monitor loop iterations (count how many times PC=42 is executed)
- Verify b increments by 1 each loop iteration
- Verify loop terminates when a reaches 1
- **Expected behavior:** Loop implements Collatz-like sequence on `a`, counting iterations in `b`

**Test Case 4.4: Part 1 vs Part 2 Comparison**
- Run simulation with a=0, b=0 (Part 1 conditions)
- Run simulation with a=1, b=0 (Part 2 conditions)
- Verify different results (different execution paths)
- **Purpose:** Ensure initial value of `a` correctly affects program behavior

**Verification Method:**
- Add optional verbose mode to print each instruction execution
- Set max_iterations=1,000,000 to detect infinite loops
- Verify final b value is a positive integer
- Compare final states between Part 1 and Part 2

### 5. Boundary and Edge Cases

**Objective:** Test program behavior at boundaries

**Test Cases:**

5.1. **Program Counter Boundaries**
- Verify termination when PC goes negative
- Verify termination when PC exceeds program length
- Test jump that lands exactly at program end

5.2. **Register Value Boundaries**
- Verify behavior with register value = 0
- Verify behavior with register value = 1 (important for jio)
- Test large register values after many tpl operations

5.3. **Jump Edge Cases**
- Test `jmp +0` (infinite loop - should be caught by max_iterations)
- Test jump to PC=0 (jump backwards to start)
- Test jump that results in PC < 0 (should terminate)
- Test jump that results in PC >= len(instructions) (should terminate)

**Verification Method:**
- Create minimal test programs targeting each edge case
- Verify correct termination or detection
- Ensure no index out of bounds errors

## Testing Procedure

### Phase 1: Unit Testing (Instruction Level)
1. Test instruction parsing on sample inputs
2. Test each instruction type individually
3. Verify PC updates correctly for each instruction
4. Fix any issues before proceeding

### Phase 2: Integration Testing (Small Programs)
1. Run example program from problem description
2. Run custom small test programs
3. Verify correct execution flow
4. Debug any control flow issues

### Phase 3: Full Solution Testing
1. Run complete program with a=1, b=0 (Part 2)
2. Monitor execution with iteration counter
3. Verify termination (check PC goes out of bounds)
4. Record final register b value
5. Run complete program with a=0, b=0 (Part 1) for comparison
6. Enable verbose mode for first 10 iterations to verify control flow

### Phase 4: Validation
1. **Termination check:** Verify program terminates within max_iterations
2. **Result sanity:** Check final b value is non-negative integer
3. **Manual trace:** Verify critical sections:
   - Initial jump (PC=0 → PC=22 when a=1)
   - Second jump (PC=22 → PC=41)
   - Loop iterations and termination
4. **Comparison:** Ensure Part 1 and Part 2 produce different results
5. **Error check:** Verify no runtime errors or exceptions
6. **Output:** Final answer is just the integer value of register b

## Success Criteria

1. **Parsing:** All instruction types parse correctly from input.md
2. **Execution:** Each instruction executes with correct register and PC updates
3. **Simple Tests:** All small test programs produce expected results
4. **Termination:** Full program terminates successfully (within max_iterations)
5. **Result:** Final register b value is a non-negative integer
6. **Stability:** No runtime errors, exceptions, or unhandled infinite loops
7. **Consistency:** Part 1 (a=0) and Part 2 (a=1) produce different results as expected
8. **PC Semantics:** Jump offsets are correctly calculated relative to current instruction

## Debug Instrumentation

For testing and verification, implement:
- **Verbose mode (optional):** Print each instruction execution with register state
- **Iteration counter:** Track total instructions executed
- **Max iteration limit:** Prevent infinite loops during testing (default: 1,000,000)
  - When exceeded: Raise RuntimeError with clear message
  - Purpose: Detect bugs causing infinite loops
- **PC trace:** Log PC movements for control flow verification

Example debug output:
```
[0] PC=0 | a=1, b=0 | {'op': 'jio', 'reg': 'a', 'offset': 22} → PC=22
[1] PC=22 | a=1, b=0 | {'op': 'jmp', 'offset': 19} → PC=41
[2] PC=41 | a=1, b=0 | {'op': 'jio', 'reg': 'a', 'offset': 8} → PC=49
Program terminated at PC=49 after 3 iterations
Final: a=1, b=0
```

**Note:** This would be the trace if `a` starts at 1 and never changes (simplified example).

## Known Edge Cases in This Problem

1. **Initial jump**: First instruction `jio a, +22` with a=1 causes immediate jump to PC=22
   - This skips instructions 1-21 entirely
   - With a=0 (Part 1), this jump is not taken

2. **Loop structure**: The `jmp -7` at PC=48 creates a loop back to PC=41
   - Loop condition: continues while a ≠ 1
   - Loop body: increments b, modifies a using Collatz-like rules
   - Termination: when a==1, `jio a, +8` at PC=41 jumps to PC=49 (end)

3. **Register a manipulation**: Multiple tpl and inc operations can create large values
   - Initial section (PC=1-21): Builds up `a` value when executed (Part 1 only)
   - Loop (PC=41-48): Applies Collatz-like transformation to `a`

4. **Termination**: Loop eventually reduces `a` to 1, then jumps to PC=49 (out of bounds)
   - PC=49 is beyond the 48 instructions (indices 0-47)
   - This correctly terminates the program

5. **Jump offset semantics**: All offsets are relative to current PC
   - Not relative to next PC (which would be PC+1)
   - Critical for correct implementation
