# Testing Plan: Instruction Pointer Simulation

## Testing Strategy

Our testing approach will validate:
1. **Individual opcode correctness** - Each of the 16 opcodes works as expected
2. **Execution model correctness** - IP binding, increment, and halt behavior
3. **Integration testing** - Complete program execution with the provided example
4. **Final solution validation** - Running against the actual input

## Test Categories

### Category 1: Opcode Unit Tests

Test each opcode individually to ensure correct behavior.

#### 1.1 Addition Opcodes

**Test `addr` (add register)**
- Input: `registers = [5, 3, 0, 0, 0, 0]`, instruction: `addr 0 1 2`
- Expected: `registers[2] = 8` (5 + 3)

**Test `addi` (add immediate)**
- Input: `registers = [5, 0, 0, 0, 0, 0]`, instruction: `addi 0 10 1`
- Expected: `registers[1] = 15` (5 + 10)

#### 1.2 Multiplication Opcodes

**Test `mulr` (multiply register)**
- Input: `registers = [4, 3, 0, 0, 0, 0]`, instruction: `mulr 0 1 2`
- Expected: `registers[2] = 12` (4 * 3)

**Test `muli` (multiply immediate)**
- Input: `registers = [7, 0, 0, 0, 0, 0]`, instruction: `muli 0 5 1`
- Expected: `registers[1] = 35` (7 * 5)

#### 1.3 Bitwise AND Opcodes

**Test `banr` (bitwise AND register)**
- Input: `registers = [12, 10, 0, 0, 0, 0]`, instruction: `banr 0 1 2`
- Expected: `registers[2] = 8` (12 & 10 = 0b1100 & 0b1010 = 0b1000)

**Test `bani` (bitwise AND immediate)**
- Input: `registers = [15, 0, 0, 0, 0, 0]`, instruction: `bani 0 7 1`
- Expected: `registers[1] = 7` (15 & 7 = 0b1111 & 0b0111 = 0b0111)

#### 1.4 Bitwise OR Opcodes

**Test `borr` (bitwise OR register)**
- Input: `registers = [12, 10, 0, 0, 0, 0]`, instruction: `borr 0 1 2`
- Expected: `registers[2] = 14` (12 | 10 = 0b1100 | 0b1010 = 0b1110)

**Test `bori` (bitwise OR immediate)**
- Input: `registers = [8, 0, 0, 0, 0, 0]`, instruction: `bori 0 5 1`
- Expected: `registers[1] = 13` (8 | 5 = 0b1000 | 0b0101 = 0b1101)

#### 1.5 Assignment Opcodes

**Test `setr` (set register)**
- Input: `registers = [0, 42, 0, 0, 0, 0]`, instruction: `setr 1 999 2`
- Expected: `registers[2] = 42` (B parameter ignored)

**Test `seti` (set immediate)**
- Input: `registers = [0, 0, 0, 0, 0, 0]`, instruction: `seti 123 999 3`
- Expected: `registers[3] = 123` (B parameter ignored)

#### 1.6 Greater-Than Comparison Opcodes

**Test `gtir` (greater-than immediate/register) - true case**
- Input: `registers = [0, 5, 0, 0, 0, 0]`, instruction: `gtir 10 1 2`
- Expected: `registers[2] = 1` (10 > 5)

**Test `gtir` - false case**
- Input: `registers = [0, 10, 0, 0, 0, 0]`, instruction: `gtir 5 1 2`
- Expected: `registers[2] = 0` (5 > 10 is false)

**Test `gtri` (greater-than register/immediate) - true case**
- Input: `registers = [10, 0, 0, 0, 0, 0]`, instruction: `gtri 0 5 1`
- Expected: `registers[1] = 1` (10 > 5)

**Test `gtri` - false case**
- Input: `registers = [5, 0, 0, 0, 0, 0]`, instruction: `gtri 0 10 1`
- Expected: `registers[1] = 0` (5 > 10 is false)

**Test `gtrr` (greater-than register/register) - true case**
- Input: `registers = [10, 5, 0, 0, 0, 0]`, instruction: `gtrr 0 1 2`
- Expected: `registers[2] = 1` (10 > 5)

**Test `gtrr` - false case**
- Input: `registers = [5, 10, 0, 0, 0, 0]`, instruction: `gtrr 0 1 2`
- Expected: `registers[2] = 0` (5 > 10 is false)

#### 1.7 Equality Comparison Opcodes

**Test `eqir` (equal immediate/register) - true case**
- Input: `registers = [0, 7, 0, 0, 0, 0]`, instruction: `eqir 7 1 2`
- Expected: `registers[2] = 1` (7 == 7)

**Test `eqir` - false case**
- Input: `registers = [0, 5, 0, 0, 0, 0]`, instruction: `eqir 7 1 2`
- Expected: `registers[2] = 0` (7 == 5 is false)

**Test `eqri` (equal register/immediate) - true case**
- Input: `registers = [7, 0, 0, 0, 0, 0]`, instruction: `eqri 0 7 1`
- Expected: `registers[1] = 1` (7 == 7)

**Test `eqri` - false case**
- Input: `registers = [5, 0, 0, 0, 0, 0]`, instruction: `eqri 0 7 1`
- Expected: `registers[1] = 0` (5 == 7 is false)

**Test `eqrr` (equal register/register) - true case**
- Input: `registers = [7, 7, 0, 0, 0, 0]`, instruction: `eqrr 0 1 2`
- Expected: `registers[2] = 1` (7 == 7)

**Test `eqrr` - false case**
- Input: `registers = [7, 5, 0, 0, 0, 0]`, instruction: `eqrr 0 1 2`
- Expected: `registers[2] = 0` (7 == 5 is false)

### Category 2: Execution Model Tests

#### 2.1 IP Binding Behavior

**Test: IP written to register before execution**
- Program:
  ```
  #ip 0
  seti 5 0 1
  ```
- After first instruction: `registers[0]` should be 0 when executing, then incremented to 1
- Result: `registers = [1, 5, 0, 0, 0, 0]` (IP is 1 after halt)

**Test: IP read from register after execution**
- Program:
  ```
  #ip 0
  addi 0 2 0
  seti 99 0 1
  ```
- Line 0: IP=0, execute `addi 0 2 0` → sets reg[0]=2, IP reads 2, increments to 3
- Should skip instruction at index 1 and 2, halt at index 3
- Result: `registers[1]` should remain 0 (instruction skipped)

#### 2.2 Jump Instructions

**Test: Absolute jump with `seti`**
- Program:
  ```
  #ip 0
  seti 3 0 0
  seti 1 0 1
  seti 2 0 1
  seti 3 0 1
  seti 99 0 2
  ```
- Line 0: Sets IP to 3, increments to 4
- Should jump to line 4, setting `registers[2] = 99`

**Test: Relative jump with `addi`**
- Program:
  ```
  #ip 0
  addi 0 1 0
  seti 1 0 1
  seti 99 0 2
  ```
- Line 0: IP=0, `addi 0 1 0` → reg[0]=1, IP reads 1, increments to 2
- Skips line 1, executes line 2
- Result: `registers[1] = 0`, `registers[2] = 99`

#### 2.3 Halt Conditions

**Test: Halt when IP exceeds instruction count**
- Program:
  ```
  #ip 0
  seti 10 0 0
  ```
- After execution: IP becomes 11, program halts

**Test: Halt when IP becomes negative**
- Program:
  ```
  #ip 0
  seti -2 0 0
  ```
- Execution sequence:
  - ip=0: Write IP (0) to reg[0], execute `seti -2 0 0` → reg[0]=-2
  - Read IP from reg[0]: ip=-2
  - Increment: ip=-1
  - Next iteration: ip=-1 < 0, halt
- **Expected: Program halts with `registers[0] = -2`**

**Test: Empty program**
- Program:
  ```
  #ip 0
  ```
- IP starts at 0, no instructions, halts immediately
- Result: `registers[0] = 0`

### Category 3: Integration Tests

#### 3.1 Provided Example Validation

**Test the example from problem statement**
- Input:
  ```
  #ip 0
  seti 5 0 1
  seti 6 0 2
  addi 0 1 0
  addr 1 2 3
  setr 1 0 0
  seti 8 0 4
  seti 9 0 5
  ```
- Expected execution trace (register state shown AFTER each complete cycle):
  - **Initial state**: ip=0, regs=[0, 0, 0, 0, 0, 0]
  - **After instruction 0** (seti 5 0 1): ip=1, regs=[0, 5, 0, 0, 0, 0]
    - (IP was written to reg[0] as 0, instruction sets reg[1]=5, IP read back as 0, incremented to 1)
  - **After instruction 1** (seti 6 0 2): ip=2, regs=[1, 5, 6, 0, 0, 0]
  - **After instruction 2** (addi 0 1 0): ip=4, regs=[3, 5, 6, 0, 0, 0]
    - (IP written to reg[0] as 2, addi sets reg[0]=2+1=3, IP reads 3, increments to 4)
    - **Instruction 3 is skipped**
  - **After instruction 4** (setr 1 0 0): ip=6, regs=[5, 5, 6, 0, 0, 0]
    - (setr sets reg[0]=reg[1]=5, IP reads 5, increments to 6)
    - **Instruction 5 is skipped**
  - **After instruction 6** (seti 9 0 5): ip=7, regs=[6, 5, 6, 0, 0, 9]
  - **ip=7**: Out of bounds (only 7 instructions, indices 0-6), program halts
- **Expected final result: `registers[0] = 6`**

**Note**: The trace shows the state after the IP increment, not during instruction execution. This is important because reg[0] is the IP-bound register.

#### 3.2 Loop Test

**Test: Simple counting loop**
- Program:
  ```
  #ip 3
  addi 0 1 0
  addi 1 1 1
  gtrr 1 2 4
  addr 4 3 3
  seti 1 0 3
  ```
- Simplified loop that uses reg[3] as IP (easier to reason about)
- Loop logic:
  - Line 0: Increment reg[0] by 1
  - Line 1: Increment reg[1] by 1
  - Line 2: Check if reg[1] > reg[2] (initially 0), store result in reg[4]
  - Line 3: If true (reg[4]=1), add 1 to IP (jump to line 5, which is out of bounds)
  - Line 4: If false, set IP to 1 (jump back to line 2 after increment)
- Expected: After 1 iteration, reg[1]=1, reg[1]>0 is true, jump out
- **Expected: `registers[0] = 1`, `registers[1] = 1`**

**Note**: This is a simpler test than the original. The goal is to verify loop behavior without complex IP manipulation.

### Category 4: Final Solution Validation

#### 4.1 Actual Input Execution

**Test with provided input.md**
- Run the program from input.md
- Verify it halts (doesn't run indefinitely)
- Record the final value in `registers[0]`

**Performance check:**
- Monitor execution time with different thresholds:
  - **Excellent**: < 1 second
  - **Good**: 1-5 seconds
  - **Acceptable**: 5-30 seconds
  - **Warning**: 30-60 seconds (may indicate inefficiency)
  - **Failure**: > 60 seconds (likely infinite loop or very inefficient algorithm)
- Optionally count total iterations executed to understand program behavior

#### 4.2 Sanity Checks

**Verify the result is reasonable:**
- Should be a non-negative integer
- Given the program structure with multiplications, might be a moderately large number
- Check that all register values are integers

### Category 5: Edge Case Tests

#### 5.1 Register Boundary Tests

**Test: Modifying IP register indirectly**
- Already covered in execution model tests (jumps modify the IP-bound register)

**Test: Different IP register bindings**
- The provided example uses `#ip 0`, the actual input uses `#ip 3`
- If time permits, test with `#ip 5` to verify any register can be bound
- Example mini-program:
  ```
  #ip 5
  seti 10 0 0
  ```
  Expected: `registers[0] = 10`, program halts immediately after

#### 5.2 Opcode Parameter Edge Cases

**Test: Self-referential operations**
- Program:
  ```
  #ip 3
  seti 5 0 0
  addr 0 0 0
  ```
- Line 0: reg[0] = 5
- Line 1: reg[0] = reg[0] + reg[0] = 5 + 5 = 10
- **Expected: `registers[0] = 10`**

**Test: Zero values**
- Program:
  ```
  #ip 3
  seti 7 0 0
  muli 0 0 0
  ```
- Line 0: reg[0] = 7
- Line 1: reg[0] = 7 * 0 = 0
- **Expected: `registers[0] = 0`**

**Test: Large values**
- Python handles arbitrary precision integers natively
- If multiplication chains create large values (millions or billions), they should work correctly
- No explicit test needed unless issues arise

## Test Execution Order

1. **Phase 1**: Run all opcode unit tests (Category 1)
   - Validate each opcode works in isolation
   - Fix any issues before proceeding

2. **Phase 2**: Run execution model tests (Category 2)
   - Verify IP binding, jumps, and halt conditions
   - Ensure the execution loop is correct

3. **Phase 3**: Run integration tests (Category 3)
   - Validate the provided example produces correct output
   - Test loop behavior

4. **Phase 4**: Run final solution (Category 4)
   - Execute against actual input
   - Verify performance and correctness

5. **Phase 5**: Edge case validation (Category 5)
   - Run edge case tests to ensure robustness

## Success Criteria

**Minimum Requirements** (must pass):
- ✓ All critical opcode tests pass (at least 1-2 tests per opcode category)
- ✓ Execution model tests pass (IP binding, jumps, halts)
- ✓ Provided example returns `registers[0] = 6`
- ✓ Program with actual input halts successfully
- ✓ Final answer is a valid positive integer

**Quality Indicators** (should pass):
- ✓ Execution completes in < 5 seconds
- ✓ No errors or warnings during execution
- ✓ At least one loop test passes

**Optional** (nice to have):
- ✓ All edge case tests pass
- ✓ Comprehensive opcode unit testing
- ✓ Debug trace available for troubleshooting

## Debugging Strategy

If tests fail:
1. **Enable debug mode**: Add a flag to print execution trace showing:
   - Current IP value
   - Instruction being executed
   - Register state after execution
   - Example format: `IP=2: seti 5 0 1 -> [0, 5, 0, 0, 0, 0]`
2. **Compare traces**: Run the failing test with debug mode and compare against expected execution trace
3. **Verify opcodes**: Test each opcode individually with simple programs if suspecting opcode bugs
4. **Check IP logic**:
   - Ensure IP is written to bound register BEFORE instruction execution
   - Ensure IP is read FROM bound register AFTER instruction execution
   - Ensure IP is incremented AFTER reading from register
5. **Verify halt condition**: Ensure loop exits when `ip < 0` or `ip >= len(instructions)`
6. **Use a debugger**: For complex issues, step through the execution loop with a Python debugger (pdb)

## Test Implementation Approach

Since we're writing a script (not production code):
- Tests can be simple assert statements or manual verification
- **Primary test**: The provided example must return `registers[0] = 6`
- **Secondary test**: Run against actual input and verify it halts
- Manual inspection of execution trace if needed
- No need for comprehensive test framework (unittest/pytest)
- Simple test functions with print statements are sufficient
- Focus on correctness over exhaustive coverage
