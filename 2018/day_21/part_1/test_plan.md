# Test Plan: Chronal Conversion - Part 1

## Testing Strategy

The goal is to verify that our solution correctly:
1. Parses the input program
2. Executes the VM correctly
3. Identifies the correct halting value for register 0

## Test Categories

### 1. Input Parsing Tests

**Test 1.1: IP Register Binding**
- **Objective**: Verify we correctly parse the `#ip N` directive
- **Input**: `#ip 2`
- **Expected**: `ip_register = 2`
- **Verification**: Print or assert the parsed IP register value

**Test 1.2: Instruction Parsing**
- **Objective**: Verify we correctly parse instruction lines
- **Test Cases**:
  - `seti 123 0 5` → `('seti', 123, 0, 5)`
  - `bani 5 456 5` → `('bani', 5, 456, 5)`
  - `addr 5 2 2` → `('addr', 5, 2, 2)`
- **Verification**: Assert parsed tuples match expected values

**Test 1.3: Instruction Count**
- **Objective**: Verify we parse the correct number of instructions
- **Expected**: 31 instructions (indices 0-30) based on the input
- **Verification**: `assert len(instructions) == 31`

### 2. Instruction Execution Tests

**Test 2.1: Validate All Opcodes**

Test each opcode with known inputs and expected outputs. Consider implementing these as structured test cases for easier verification:

```python
# Example structure for systematic testing
test_cases = [
    # (opcode, initial_registers, a, b, c, expected_registers)
    ('addr', [0, 5, 3, 0, 0, 0], 1, 2, 3, [0, 5, 3, 8, 0, 0]),
    ('addi', [0, 5, 0, 0, 0, 0], 1, 10, 2, [0, 5, 15, 0, 0, 0]),
    # ... etc
]
```

**Individual Opcode Tests:**

**Addition:**
- `addr 1 2 3` with `r1=5, r2=3` → `r3=8`
- `addi 1 10 2` with `r1=5` → `r2=15`

**Multiplication:**
- `mulr 1 2 3` with `r1=4, r2=5` → `r3=20`
- `muli 1 3 2` with `r1=7` → `r2=21`

**Bitwise AND:**
- `banr 1 2 3` with `r1=0b1111, r2=0b1010` → `r3=0b1010 (10)`
- `bani 1 456 2` with `r1=123` → `r2=72` (123 & 456 = 72)

**Bitwise OR:**
- `borr 1 2 3` with `r1=0b1100, r2=0b0011` → `r3=0b1111 (15)`
- `bori 1 10 2` with `r1=5` → `r2=15`

**Assignment:**
- `setr 1 X 2` with `r1=42` → `r2=42` (X is ignored)
- `seti 99 X 3` → `r3=99` (both inputs ignored)

**Greater-than:**
- `gtir 10 1 2` with `r1=5` → `r2=1` (10 > 5)
- `gtir 3 1 2` with `r1=5` → `r2=0` (3 not > 5)
- `gtri 1 10 2` with `r1=15` → `r2=1` (15 > 10)
- `gtri 1 10 2` with `r1=5` → `r2=0` (5 not > 10)
- `gtrr 1 2 3` with `r1=10, r2=5` → `r3=1`
- `gtrr 1 2 3` with `r1=5, r2=10` → `r3=0`

**Equality:**
- `eqir 10 1 2` with `r1=10` → `r2=1` (equal)
- `eqir 10 1 2` with `r1=5` → `r2=0` (not equal)
- `eqri 1 10 2` with `r1=10` → `r2=1`
- `eqri 1 10 2` with `r1=5` → `r2=0`
- `eqrr 1 2 3` with `r1=7, r2=7` → `r3=1`
- `eqrr 1 2 3` with `r1=7, r2=8` → `r3=0`

**Verification**: Create unit tests for each opcode to ensure correct behavior.

### 3. VM Execution Model Tests

**Test 3.1: IP Register Binding**
- **Objective**: Verify IP is correctly written to bound register before execution and read after
- **Test**: Simple program with IP bound to register 0:
  ```
  #ip 0
  seti 5 0 1   # Set r1 = 5
  ```
- **Expected**: After first instruction, `r0` should be 0 (current IP), then after execution it becomes 0, then increments to 1
- **Verification**: Trace register 0 values through execution

**Test 3.2: Jump/Branch Behavior**
- **Objective**: Verify that modifying the IP register causes jumps
- **Test**: Program that modifies IP register:
  ```
  #ip 1
  addi 1 2 1   # r1 = 0+2 = 2, IP jumps to 2, then increments to 3
  seti 99 0 0  # Instruction 1: skipped
  seti 88 0 0  # Instruction 2: skipped
  seti 42 0 0  # Instruction 3: this executes
  ```
- **Expected**: `r0 = 42`, instructions 1 and 2 are skipped
- **Verification**: Check final register state (r0 should be 42, not 99 or 88)

**Test 3.3: Halt Condition**
- **Objective**: Verify program halts when IP goes out of bounds
- **Test**: Program that jumps past last instruction
- **Expected**: Program stops, doesn't crash
- **Verification**: Execution completes without error

### 4. Validation Loop Test

**Test 4.1: Initial Validation**
- **Objective**: Verify the program passes the initial validation (instructions 0-4)
- **Test**: Execute instructions 0-4 manually or with VM
- **Expected Behavior** (with IP bound to register 2):
  - Instruction 0: `seti 123 0 5` → `r5 = 123`
  - Instruction 1: `bani 5 456 5` → `r5 = 123 & 456 = 72`
  - Instruction 2: `eqri 5 72 5` → `r5 = 1` (since 72 == 72)
  - Instruction 3: `addr 5 2 2` → `r2 (IP) = 1 + 3 = 4`, then incremented to 5 (skips instruction 4)
  - Instruction 4: `seti 0 0 2` → Should be skipped (this would create infinite loop)
  - Next: IP should be at instruction 5, continuing to main program
- **Verification**: After validation, IP should be at instruction 5 or beyond, not stuck in a loop at instruction 0

### 5. Solution Verification Tests

**Test 5.1: First Reach of Instruction 29**
- **Objective**: Verify we detect the first time IP reaches instruction 29
- **Test**: Run the VM with instruction counter, log when we hit instruction 29
- **Verification**:
  - We do reach instruction 29 at some point
  - We capture register 5's value at that moment
  - Log the instruction count to ensure it's reasonable (likely in the thousands to millions range)

**Test 5.2: Value Range Check**
- **Objective**: Verify the answer is a reasonable non-negative integer
- **Expected**: The value should be >= 0 and likely < 2^24 (based on `bani 5 16777215 5` which masks to 24 bits)
- **Verification**: `assert 0 <= result < 16777216`

**Test 5.3: Halting Verification**
- **Objective**: Verify that using our found value in register 0 actually causes the program to halt quickly
- **Test**:
  1. Find the halting value (register 5 when IP first reaches 29)
  2. Run the VM again with register 0 set to that value
  3. Count total instructions executed and verify the program halts
- **Expected Execution Path** (when r5 == r0):
  - At instruction 29: `eqrr 5 0 3` sets r3 = 1 (since r5 == r0)
  - At instruction 30: `addr 3 2 2` sets r2 = 1 + 30 = 31
  - After increment: IP = 32 (out of bounds → halt)
- **Verification**:
  - Program halts (doesn't run forever)
  - Instruction count in second run is much smaller than first run
  - Final IP is 32 (out of bounds)

**Test 5.4: Complete Solution Integration Test**
- **Objective**: Verify the complete solution works end-to-end
- **Test Steps**:
  1. Parse the actual input file
  2. Run VM to find the value in r5 when first reaching instruction 29 (run 1)
  3. Run VM again with r0 set to that value (run 2)
  4. Compare instruction counts between both runs
  5. Print both instruction counts and the found value
- **Expected**:
  - Run 1: Many instructions (thousands to millions)
  - Run 2: Much fewer instructions (should halt at instruction 29/30 transition)
  - The found value is the correct answer to minimize instruction count

### 6. Edge Case Tests

**Test 6.1: Register Overflow**
- **Objective**: Ensure we handle large register values correctly
- **Note**: Python handles big integers naturally, but verify bitwise operations work correctly with large values
- **Test**: The program uses `bani 5 16777215 5` to mask values, verify this works for large numbers
- **Verification**: `assert (99999999999 & 16777215) < 16777216`


## Test Execution Plan

### Phase 1: Unit Tests
1. Test input parsing (Tests 1.1-1.3)
2. Test each opcode independently (Test 2.1)
3. Run validation loop test (Test 4.1)

### Phase 2: Integration Tests
1. Test VM execution model (Tests 3.1-3.3)
2. Test full program execution until instruction 29 (Test 5.1)

### Phase 3: Solution Validation
1. Run solution and capture result (Test 5.1)
2. Verify result is reasonable (Test 5.2)
3. Verify result causes halt (Test 5.3)
4. Run complete integration test (Test 5.4)
5. Compare instruction counts from both runs

### Success Criteria

The solution is correct if:
1. All opcode tests pass ✓
2. Validation loop passes (doesn't enter infinite loop at instruction 0) ✓
3. We reach instruction 29 within reasonable time ✓
4. The captured value from register 5 is non-negative and < 16777216 ✓
5. When register 0 is set to this value, the program halts ✓
6. The halt occurs at instruction 29/30 transition (IP becomes 32) ✓
7. The second run executes significantly fewer instructions than the first run ✓

## Manual Verification Steps

1. **Print intermediate states** (optional debug mode): Add debug logging to print:
   - IP value before each instruction
   - Current instruction being executed
   - Register states after each instruction
   - Special marker when hitting instruction 29
   - Instruction counter

2. **Instruction count**: Count how many instructions execute before first reaching instruction 29

3. **Second run verification**: After finding the value, run the program again with r0 set to that value and verify:
   - Execution follows the same path until instruction 29
   - At instruction 29, `r5 == r0`, so `r3 = 1`
   - At instruction 30, `addr 3 2 2` sets r2 (IP) to `1 + 30 = 31`
   - After incrementing, IP = 32, which is out of bounds → halt
   - Total instruction count is much lower than first run

4. **Manual trace of critical section**: Manually trace execution from instruction 29-30 to verify halting logic:
   ```
   IP=29: r2=29, execute eqrr 5 0 3 → r3 = (r5==r0 ? 1 : 0), r2=29, IP becomes 30
   IP=30: r2=30, execute addr 3 2 2 → r2 = r3 + 30, IP becomes r2+1
          If r3=1: IP becomes 32 (halt)
          If r3=0: IP becomes 31 (continue)
   ```
