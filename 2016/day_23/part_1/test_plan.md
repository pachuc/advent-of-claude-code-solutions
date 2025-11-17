# Test Plan: Assembunny Code Interpreter with Toggle

## Testing Strategy

We need to verify that our interpreter correctly:
1. Executes all 5 instruction types correctly
2. Handles dynamic instruction modification via `tgl`
3. Validates instructions and skips invalid ones
4. Manages program counter and jumps correctly
5. Returns the correct final value for register `a`

## Test Categories

### 1. Basic Instruction Tests

#### Test 1.1: Copy Instruction (`cpy`)
**Purpose**: Verify copying values between registers and from literals

**Test Case**:
```
cpy 5 a
cpy a b
cpy 10 c
```

**Expected Results**:
- Register a = 5
- Register b = 5
- Register c = 10

**Verification**: Check final register values

#### Test 1.2: Increment Instruction (`inc`)
**Purpose**: Verify incrementing register values

**Test Case**:
```
cpy 0 a
inc a
inc a
inc a
```

**Expected Results**:
- Register a = 3 (starting from 0, not the default value of 7)

**Note**: This test explicitly sets `a = 0` first to have a known starting point.

**Verification**: Check final register value

#### Test 1.3: Decrement Instruction (`dec`)
**Purpose**: Verify decrementing register values

**Test Case**:
```
cpy 5 a
dec a
dec a
```

**Expected Results**:
- Register a = 3

**Verification**: Check final register value

#### Test 1.4: Jump If Not Zero (`jnz`)
**Purpose**: Verify conditional jumping with both literal and register offsets

**Test Case 1** (jump taken):
```
cpy 1 a
jnz a 2
inc a
inc a
```

**Expected**: Register a = 1 (second inc skipped)

**Test Case 2** (jump not taken):
```
cpy 0 a
jnz a 2
inc a
inc a
```

**Expected**: Register a = 2 (both inc executed)

**Test Case 3** (backward jump for loop):
```
cpy 3 a
cpy 0 b
inc b
dec a
jnz a -2
```

**Expected**: a = 0, b = 3

**Verification**: Check register values after execution

### 2. Toggle Instruction Tests

#### Test 2.1: Toggle One-Argument Instructions
**Purpose**: Verify `inc` ↔ `dec` toggling

**Test Case**:
```
cpy 2 a
tgl a
inc b
```

**Expected Behavior**:
- `tgl a` toggles instruction at offset 2 (the `inc b`)
- `inc b` becomes `dec b`
- Register b = -1

**Verification**: Check that instruction was modified and b = -1

#### Test 2.2: Toggle Two-Argument Instructions
**Purpose**: Verify `jnz` ↔ `cpy` toggling

**Test Case**:
```
cpy 1 a
tgl a
jnz 5 b
```

**Expected Behavior**:
- `tgl a` toggles instruction at offset 1 (the `jnz 5 b`)
- `jnz 5 b` becomes `cpy 5 b`
- Register b = 5

**Verification**: Check that instruction was modified and b = 5

#### Test 2.3: Toggle Out of Bounds
**Purpose**: Verify nothing happens when toggling outside program

**Test Case**:
```
cpy 10 a
tgl a
inc b
```

**Expected Behavior**:
- `tgl a` attempts to toggle instruction at offset 10 (out of bounds)
- Nothing changes
- `inc b` executes normally
- Register b = 1

**Verification**: Check b = 1 and no errors occur

#### Test 2.4: The Example from Problem Statement
**Purpose**: Verify the exact example given in the problem

**Test Case** (with a starting at 2):
```
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
```

**Expected Result**: Register a = 3

**Execution Trace**:
1. cpy 2 a → a = 2
2. tgl a → toggles line 4 (tgl a → inc a)
3. tgl a → toggles line 5 (cpy 1 a → jnz 1 a)
4. inc a → a = 3
5. jnz 1 a → jumps 3 ahead (exits)

**Verification**: Register a must equal 3

### 3. Invalid Instruction Tests

#### Test 3.1: Invalid CPY (Non-Register Destination)
**Purpose**: Verify invalid instructions are skipped

**Test Case**:
```
cpy 1 a
tgl a
jnz 5 2
inc b
```

**Expected Behavior**:
- `tgl a` toggles instruction at offset 1 (line 2: `jnz 5 2`)
- `jnz 5 2` becomes `cpy 5 2`
- `cpy 5 2` is invalid (destination `2` is not a register)
- Invalid instruction is skipped
- `inc b` executes normally, b = 1

**Verification**: Check that invalid instructions don't crash, are skipped, and b = 1

#### Test 3.2: Invalid INC/DEC (Non-Register Target)
**Purpose**: Verify inc/dec with invalid targets are skipped

**Test Case**:
```
cpy 0 a
tgl a
dec a
```

**Expected Behavior**:
- `tgl a` toggles `dec a` to `inc a`
- `inc a` executes normally
- a = 1

**Verification**: Check a = 1

### 4. Complex Interaction Tests

#### Test 4.1: Self-Toggling
**Purpose**: Verify `tgl` can toggle itself

**Test Case**:
```
cpy 0 a
tgl a
inc a
```

**Expected Behavior**:
- PC = 0: `cpy 0 a` executes, a = 0, PC advances to 1
- PC = 1: `tgl a` reads a (value 0), toggles instruction at PC + 0 = 1 (itself)
- Line 1: `tgl a` becomes `inc a` (but PC already advanced)
- PC = 2: `inc a` executes, a = 1
- Program ends

**Expected Result**: Register a = 1

**Note**: The toggled instruction at line 1 is not executed again unless we jump back to it.

**Verification**: Register a = 1

#### Test 4.2: Multiple Toggles of Same Instruction
**Purpose**: Verify toggling the same instruction multiple times

**Test Case**:
```
cpy 3 a
tgl a
tgl a
tgl a
inc b
```

**Expected Behavior**:
- First `tgl a`: toggles `inc b` to `dec b`
- Second `tgl a`: toggles `dec b` back to `inc b`
- Third `tgl a`: toggles `inc b` to `dec b`
- Final: b = -1

**Verification**: Register b = -1

#### Test 4.3: Basic Loop (No Toggle)
**Purpose**: Verify basic loop functionality

**Test Case**:
```
cpy 2 a
cpy 0 b
inc b
dec a
jnz a -2
```

**Expected Behavior**:
- Simple loop: a counts down from 2, b counts up
- Final: a = 0, b = 2

**Note**: This is a basic loop test without toggle functionality.

**Verification**: Check a = 0, b = 2

#### Test 4.4: Toggled Instruction Persistence
**Purpose**: Verify toggled instructions remain toggled across multiple executions

**Test Case**:
```
cpy 1 a
tgl a
cpy 3 b
dec b
jnz b -1
```

**Expected Behavior**:
- `tgl a` toggles instruction at offset 1 (line 3: `dec b` → `inc b`)
- Loop at lines 4-5 executes `inc b` multiple times
- b starts at 3, increments in loop until b becomes large
- After 3 iterations: b = 6 (3 + 3 increments)
- Actually, this creates an infinite loop. Better test case:

**Better Test Case**:
```
cpy 1 a
tgl a
cpy 2 c
dec b
dec c
jnz c -2
```

**Expected Behavior**:
- `tgl a` toggles line 3 (`dec b` → `inc b`)
- Loop executes twice (c goes from 2 to 0)
- Each iteration executes `inc b`, so b = 2

**Verification**: Check that b = 2, confirming toggled instruction persists

### 5. Final Solution Test

#### Test 5.1: Actual Input Verification
**Purpose**: Verify the solution produces correct output for the given input

**Test Procedure**:
1. Run interpreter with the actual input from `input.md`
2. Initial state: a=7, b=0, c=0, d=0
3. Execute all instructions
4. Record final value of register `a`

**Expected Result**:
- The problem doesn't provide the expected answer initially, but we can verify:
  - Program completes without errors
  - Result is a positive integer
  - Result is consistent across multiple runs

**Verification Methods**:
1. **No Runtime Errors**: Program completes successfully
2. **Deterministic**: Multiple runs produce same result (same output, consistent execution)
3. **Reasonable Value**: Result should be greater than 7 (initial value)
4. **Execution Completes**: Program doesn't infinite loop

**Post-Solution**:
- Once the answer is verified as correct (e.g., through problem submission), document the expected value here for regression testing
- Future runs should produce this exact value

### 6. Edge Cases

#### Test 6.1: Jump Beyond Program End
**Purpose**: Verify jumping past the last instruction terminates correctly

**Test Case**:
```
jnz 1 10
inc a
```

**Expected Behavior**:
- Jump takes program counter beyond bounds
- Program terminates
- Register a = 7 (unchanged from initial)

**Verification**: Program terminates cleanly

#### Test 6.2: Backward Jump to Negative Index
**Purpose**: Verify jumping before first instruction terminates correctly

**Test Case**:
```
jnz 1 -5
inc a
```

**Expected Behavior**:
- Jump takes program counter to negative index
- Program terminates
- Register a = 7 (unchanged)

**Verification**: Program terminates cleanly

#### Test 6.3: Zero Jump Offset (Note Only)
**Purpose**: Document potential infinite loop scenario

**Note**: A `jnz` instruction with offset 0 would create an infinite loop:
```
jnz 1 0
```

For this simple Advent of Code script, we will not implement a maximum iteration counter. The problem input is trusted not to contain infinite loops. If an infinite loop occurs during testing, it indicates either:
- A bug in the implementation
- An error in understanding the problem
- Invalid test input

**Verification**: Not a formal test; just awareness of the scenario

#### Test 6.4: Register Used as Jump Offset
**Purpose**: Verify dynamic jump offsets from registers

**Test Case**:
```
cpy 2 a
cpy 3 b
jnz a b
inc c
inc c
inc c
```

**Expected Behavior**:
- jnz uses register b (value 3) as offset
- Jumps 3 instructions forward
- c remains 0

**Verification**: Register c = 0

## Testing Execution Plan

### Phase 1: Unit Tests (Basic Instructions)
1. Test each instruction type independently
2. Verify register updates are correct
3. Verify program counter updates correctly

### Phase 2: Toggle Tests
1. Test toggle transformations for all instruction types
2. Test out-of-bounds toggle attempts
3. Test self-toggling
4. Verify example from problem statement

### Phase 3: Integration Tests
1. Test instruction combinations
2. Test loops with various instructions
3. Test toggle within loops
4. Test invalid instruction handling

### Phase 4: Final Solution Test
1. Run with actual input file
2. Verify completion without errors
3. Verify deterministic output
4. Record and validate final answer

## Success Criteria

The implementation passes if:
1. All basic instruction tests pass
2. All toggle tests pass, including the example
3. Invalid instructions are handled gracefully
4. All edge cases pass without crashes
5. The actual input produces a deterministic integer result
6. No infinite loops occur

## Manual Verification Steps

For the actual input:
1. Run: `python solution.py`
2. Observe output value
3. Run again to verify same output (deterministic, including consistent execution time)
4. Verify execution completes in reasonable time (< 1 minute)
5. Check no error messages or exceptions
6. Document the correct answer once verified for future regression testing

## Debugging Strategy

If tests fail:
1. Add print statements to show instruction execution trace
2. Print register values after each instruction
3. Print when instructions are toggled (show before/after)
4. Track program counter to verify jumps
5. Verify instruction parsing is correct
