# Testing Plan: Duet Assembly Interpreter

## Testing Strategy Overview

We need to verify:
1. Correct parsing of instructions
2. Correct execution of each instruction type
3. Correct handling of jumps and loops
4. Correct termination condition (rcv with non-zero)
5. Correct final result

## Test Categories

### 1. Unit Tests - Individual Instructions

#### Test 1.1: `snd` Instruction
**Purpose**: Verify sound frequency is stored correctly

**Test Cases**:
- `snd 5` - Play sound with literal value 5
  - Expected: `last_sound = 5`
- Set register a=10, then `snd a` - Play sound from register
  - Expected: `last_sound = 10`

**Verification**:
```python
# Test literal
registers = defaultdict(int)
last_sound = None
# Execute: snd 5
last_sound = 5
assert last_sound == 5

# Test register
registers['a'] = 10
# Execute: snd a
last_sound = registers['a']
assert last_sound == 10
```

#### Test 1.2: `set` Instruction
**Purpose**: Verify register assignment

**Test Cases**:
- `set a 5` - Set register to literal
  - Expected: `registers['a'] = 5`
- `set a 5`, `set b a` - Set register to another register's value
  - Expected: `registers['b'] = 5`

**Verification**:
```python
registers = defaultdict(int)
registers['a'] = 5  # set a 5
assert registers['a'] == 5

registers['b'] = registers['a']  # set b a
assert registers['b'] == 5
```

#### Test 1.3: `add` Instruction
**Purpose**: Verify addition operation

**Test Cases**:
- `set a 5`, `add a 3` - Add literal to register
  - Expected: `registers['a'] = 8`
- `set a 5`, `set b 3`, `add a b` - Add register to register
  - Expected: `registers['a'] = 8`
- `set a 5`, `add a -2` - Add negative number
  - Expected: `registers['a'] = 3`

**Verification**:
```python
registers = defaultdict(int)
registers['a'] = 5
registers['a'] += 3
assert registers['a'] == 8

registers['a'] = 5
registers['a'] += -2
assert registers['a'] == 3
```

#### Test 1.4: `mul` Instruction
**Purpose**: Verify multiplication operation

**Test Cases**:
- `set a 5`, `mul a 3` - Multiply by literal
  - Expected: `registers['a'] = 15`
- `set a 5`, `mul a a` - Multiply register by itself
  - Expected: `registers['a'] = 25`
- `set a 5`, `mul a 0` - Multiply by zero
  - Expected: `registers['a'] = 0`

**Verification**:
```python
registers = defaultdict(int)
registers['a'] = 5
registers['a'] *= 3
assert registers['a'] == 15

registers['a'] = 5
registers['a'] *= registers['a']
assert registers['a'] == 25
```

#### Test 1.5: `mod` Instruction
**Purpose**: Verify modulo operation

**Test Cases**:
- `set a 9`, `mod a 5` - Basic modulo
  - Expected: `registers['a'] = 4`
- `set a 10`, `mod a 10` - Modulo by same number
  - Expected: `registers['a'] = 0`
- `set a 7`, `mod a 3` - Another test
  - Expected: `registers['a'] = 1`

**Verification**:
```python
registers = defaultdict(int)
registers['a'] = 9
registers['a'] %= 5
assert registers['a'] == 4

registers['a'] = 10
registers['a'] %= 10
assert registers['a'] == 0
```

#### Test 1.6: `rcv` Instruction
**Purpose**: Verify recovery behavior

**Test Cases**:
- `snd 10`, `set a 0`, `rcv a` - rcv with zero value (should not recover)
  - Expected: Continue execution, don't return
- `snd 10`, `set a 1`, `rcv a` - rcv with non-zero value (should recover)
  - Expected: Return 10

**Verification**:
```python
last_sound = 10
registers['a'] = 0
# Execute rcv a
value = registers['a']
if value != 0:
    # Should NOT reach here
    assert False

registers['a'] = 1
value = registers['a']
if value != 0:
    result = last_sound
    assert result == 10
```

#### Test 1.7: `jgz` Instruction
**Purpose**: Verify conditional jump behavior

**Test Cases**:
- `set a 5`, `jgz a 3` - Jump when positive
  - Expected: pc += 3
- `set a 0`, `jgz a 3` - Don't jump when zero
  - Expected: pc += 1
- `set a -5`, `jgz a 3` - Don't jump when negative
  - Expected: pc += 1
- `set a 5`, `jgz a -2` - Jump backwards
  - Expected: pc += -2
- `jgz 1 3` - Jump with literal condition (always jump)
  - Expected: pc += 3
- `set a 5`, `set b 2`, `jgz a b` - Jump with register offset
  - Expected: pc += 2 (value of b)
- `set a 3`, `jgz a a` - Jump offset is same register as condition
  - Expected: pc += 3 (value of a)

**Verification**:
```python
registers = defaultdict(int)
pc = 0

# Test positive jump
registers['a'] = 5
if registers['a'] > 0:
    pc += 3
assert pc == 3

# Test zero (no jump)
pc = 0
registers['a'] = 0
if registers['a'] > 0:
    pc += 3
else:
    pc += 1
assert pc == 1

# Test register offset
pc = 0
registers['a'] = 5
registers['b'] = 2
if registers['a'] > 0:
    pc += registers['b']
assert pc == 2
```

### 2. Integration Tests - Small Programs

#### Test 2.1: Example from Problem Statement
**Purpose**: Verify the provided example works correctly

**Input**:
```
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
```

**Expected Output**: 4

**Execution Trace**:
1. `set a 1` → a=1, pc=1
2. `add a 2` → a=3, pc=2
3. `mul a a` → a=9, pc=3
4. `mod a 5` → a=4, pc=4
5. `snd a` → last_sound=4, pc=5
6. `set a 0` → a=0, pc=6
7. `rcv a` → a=0 (zero), do nothing, pc=7
8. `jgz a -1` → a=0 (not > 0), don't jump, pc=8
9. `set a 1` → a=1, pc=9
10. `jgz a -2` → a=1 (>0), jump: pc = 9 + (-2) = 7
11. (Now at pc=7) `rcv a` → a=1 (non-zero), **RETURN 4** ✓

**Note**: At step 10, we're at instruction index 9 (the second `jgz`). Jumping by -2 brings us to index 7, which is the `rcv a` instruction.

**Verification**: Create this as a test file and run the interpreter

#### Test 2.2: Simple Sound and Recover
**Purpose**: Test basic snd/rcv flow

**Input**:
```
snd 42
set a 1
rcv a
```

**Expected Output**: 42

#### Test 2.3: Multiple Sounds
**Purpose**: Verify only the LAST sound is recovered

**Input**:
```
snd 10
snd 20
snd 30
set a 1
rcv a
```

**Expected Output**: 30 (last sound played)

#### Test 2.4: Loop with Counter
**Purpose**: Test loop execution

**Input**:
```
set i 3
set a 1
add a 1
add i -1
jgz i -2
snd a
set b 1
rcv b
```

**Expected Execution**:
- i=3, a=1
- a=2, i=2, jump back
- a=3, i=1, jump back
- a=4, i=0, don't jump
- snd 4
- b=1, rcv returns 4

**Expected Output**: 4

### 3. Edge Case Tests

#### Test 3.1: Jump Out of Bounds
**Purpose**: Verify program terminates when jumping past end

**Input**:
```
jgz 1 100
```

**Expected**: Program terminates (pc out of bounds)

#### Test 3.2: Negative Numbers
**Purpose**: Test negative values throughout

**Input**:
```
set a -5
add a -3
mul a 2
snd a
set b 1
rcv b
```

**Expected Execution**:
- a = -5
- a = -5 + (-3) = -8
- a = -8 * 2 = -16
- last_sound = -16
- b = 1
- rcv returns -16

**Expected Output**: -16

#### Test 3.2b: Sound with Negative Literal
**Purpose**: Explicitly test snd with negative literal value

**Input**:
```
snd -42
set a 1
rcv a
```

**Expected Output**: -42

#### Test 3.3: Zero Values
**Purpose**: Test operations with zero

**Input**:
```
set a 0
mul a 100
add a 5
snd a
set b 1
rcv b
```

**Expected Output**: 5

#### Test 3.4: Register Not Previously Set
**Purpose**: Verify defaultdict behavior (auto-initialize to 0)

**Input**:
```
add x 10
snd x
set y 1
rcv y
```

**Expected Output**: 10 (x starts at 0, becomes 10)

#### Test 3.5: RCV Before Any SND
**Purpose**: Test edge case where rcv executes before any sound is played

**Input**:
```
set a 1
rcv a
```

**Expected Behavior**:
- last_sound would be None
- Program should handle this gracefully (return None or raise error)
- This scenario is unlikely in valid input but good to test

#### Test 3.6: Jump with Register Offset
**Purpose**: Verify that jump offset can come from a register

**Input**:
```
set a 10
set b 3
jgz a b
snd 1
snd 2
snd 3
set c 1
rcv c
```

**Expected Execution**:
- a=10, b=3
- jgz: a>0, so jump by 3 (skip next 3 instructions)
- Lands on `set c 1`
- c=1, rcv returns... wait, no sound played!

Let me fix this test:

**Input (corrected)**:
```
snd 100
set a 10
set b 2
jgz a b
snd 200
set c 1
rcv c
```

**Expected Execution**:
- last_sound=100
- a=10, b=2
- jgz: a>0, jump by 2 (skip next 2 instructions: `snd 200` and `set c 1`)
- Wait, this doesn't work either...

**Input (final)**:
```
snd 100
set offset 3
set a 1
jgz a offset
snd 200
snd 300
snd 400
set b 1
rcv b
```

**Expected Execution**:
- last_sound=100, offset=3, a=1
- jgz: a>0, jump by 3 (skip snd 200, snd 300, snd 400)
- Set b=1, rcv returns 100

**Expected Output**: 100

### 4. Full Integration Test - Actual Input

#### Test 4.1: Run Against Actual Input
**Purpose**: Solve the actual problem

**Steps**:
1. Run the interpreter with input.md
2. Verify program terminates (doesn't infinite loop)
3. Verify a result is returned
4. Manually trace first few iterations to verify correctness

**Expected Behavior**:
- Program should terminate in reasonable time (< 5 seconds)
- Should return a positive integer
- No crashes or errors

### 5. Verification Strategy for Actual Input

Since we don't know the expected answer beforehand, we verify by:

#### 5.1: Manual Trace (First Few Instructions)
Manually execute first 10-15 instructions to verify:
- Registers are initialized correctly
- Operations work as expected
- Instruction pointer advances correctly

**From input.md**:
```
set i 31      -> i=31, pc=1
set a 1       -> a=1, pc=2
mul p 17      -> p=0*17=0, pc=3
jgz p p       -> p=0, not >0, pc=4
mul a 2       -> a=2, pc=5
add i -1      -> i=30, pc=6
jgz i -2      -> i>0, pc=6-2=4
...
```

#### 5.2: Add Debug Output
Temporarily add print statements to verify:
- When `snd` is executed (print frequency)
- When `rcv` is checked (print register value)
- Final return value

#### 5.3: Sanity Checks
- Result should be positive integer
- Result should be one of the values played by `snd` instructions
- Program should have executed multiple `snd` before terminating

#### 5.4: State Inspection
Add ability to print:
- Final register values
- Number of instructions executed
- All frequencies played (to verify returned value was one of them)

### 6. Test Execution Checklist

**Basic Tests:**
- [ ] Run example from problem statement (expected: 4)
- [ ] Run Test 2.2 (expected: 42)
- [ ] Run Test 2.3 (expected: 30)
- [ ] Run Test 2.4 (expected: 4)

**Edge Case Tests:**
- [ ] Run Test 3.2 (negative numbers, expected: -16)
- [ ] Run Test 3.2b (negative literal in snd, expected: -42)
- [ ] Run Test 3.4 (uninitialized registers, expected: 10)
- [ ] Run Test 3.5 (rcv before snd - should handle gracefully)
- [ ] Run Test 3.6 (jump with register offset, expected: 100)

**Instruction-Specific Tests:**
- [ ] Test jgz with literal condition (e.g., `jgz 1 3`)
- [ ] Test jgz with register offset (e.g., `jgz a b` where b contains offset)
- [ ] Test all arithmetic with negative numbers

**Actual Input:**
- [ ] Run actual input and verify:
  - [ ] Terminates without error
  - [ ] Returns integer value
  - [ ] Execution time < 5 seconds
  - [ ] Can manually verify first few steps
  - [ ] Result is one of the `snd` values

### 7. Testing Code Structure

```python
def test_example():
    """Test the example from problem statement"""
    input_str = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

    result = solve_with_string(input_str)
    assert result == 4, f"Expected 4, got {result}"
    print("✓ Example test passed")

def test_simple():
    """Test simple snd/rcv"""
    input_str = """snd 42
set a 1
rcv a"""

    result = solve_with_string(input_str)
    assert result == 42, f"Expected 42, got {result}"
    print("✓ Simple test passed")

def test_multiple_sounds():
    """Test that last sound is recovered"""
    input_str = """snd 10
snd 20
snd 30
set a 1
rcv a"""

    result = solve_with_string(input_str)
    assert result == 30, f"Expected 30, got {result}"
    print("✓ Multiple sounds test passed")

def test_negative_numbers():
    """Test negative values"""
    input_str = """set a -5
add a -3
mul a 2
snd a
set b 1
rcv b"""

    result = solve_with_string(input_str)
    assert result == -16, f"Expected -16, got {result}"
    print("✓ Negative numbers test passed")

def test_register_jump_offset():
    """Test jgz with register offset"""
    input_str = """snd 100
set offset 3
set a 1
jgz a offset
snd 200
snd 300
snd 400
set b 1
rcv b"""

    result = solve_with_string(input_str)
    assert result == 100, f"Expected 100, got {result}"
    print("✓ Register jump offset test passed")

def run_all_tests():
    """Run all test cases"""
    print("Running tests...\n")
    test_example()
    test_simple()
    test_multiple_sounds()
    test_negative_numbers()
    test_register_jump_offset()
    print("\n" + "="*50)
    print("✓ All tests passed!")
    print("="*50)

if __name__ == "__main__":
    # Run test suite
    run_all_tests()

    # Run actual input
    print("\nRunning actual input:")
    result = solve()
    if result is not None:
        print(f"Result: {result}")
    else:
        print("ERROR: No result obtained")
```

## Summary

This testing plan covers:
1. **Unit tests** for each instruction type
2. **Integration tests** with small programs
3. **Edge cases** (negative numbers, jumps, uninitialized registers)
4. **Full integration** with actual input
5. **Verification strategy** for unknown expected output

The tests progress from simple to complex, ensuring each component works before testing the full system.
