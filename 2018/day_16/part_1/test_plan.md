# Testing Plan: Chronal Classification - Part 1

## Overview
This testing plan ensures our solution correctly identifies samples that behave like three or more opcodes. We need to verify: input parsing, opcode simulation accuracy, and counting logic.

## Testing Strategy

Since this is a script to solve a specific problem (not production code), we focus on:
1. **Correctness**: Verify core logic works with known examples
2. **Coverage**: Test each opcode type at least once
3. **Integration**: Ensure end-to-end solution works with actual input

We do NOT need:
- Extensive error handling for malformed input
- Performance benchmarking (input size is manageable)
- Edge case testing for invalid register numbers (input is guaranteed valid)

## Test Plan Steps

### 1. Unit Test: Individual Opcode Functions

**Objective**: Verify each of the 16 opcodes produces correct output

**Test Cases** (one per opcode family):

#### Addition Operations
```python
# addr: registers[C] = registers[A] + registers[B]
registers = [3, 2, 1, 1]
result = execute_opcode('addr', registers, 1, 2, 3)
expected = [3, 2, 1, 3]  # registers[1]=2 + registers[2]=1 = 3
assert result == expected

# addi: registers[C] = registers[A] + value B
registers = [3, 2, 1, 1]
result = execute_opcode('addi', registers, 2, 1, 2)
expected = [3, 2, 2, 1]  # registers[2]=1 + 1 = 2
assert result == expected
```

#### Multiplication Operations
```python
# mulr: registers[C] = registers[A] * registers[B]
registers = [3, 2, 1, 1]
result = execute_opcode('mulr', registers, 0, 1, 3)
expected = [3, 2, 1, 6]  # registers[0]=3 * registers[1]=2 = 6
assert result == expected

# muli: registers[C] = registers[A] * value B
registers = [3, 2, 1, 1]
result = execute_opcode('muli', registers, 1, 3, 2)
expected = [3, 2, 6, 1]  # registers[1]=2 * 3 = 6
assert result == expected
```

#### Bitwise AND Operations
```python
# banr: registers[C] = registers[A] & registers[B]
registers = [3, 2, 1, 1]  # 3=0b11, 2=0b10
result = execute_opcode('banr', registers, 0, 1, 3)
expected = [3, 2, 1, 2]  # 3 & 2 = 0b11 & 0b10 = 0b10 = 2
assert result == expected

# bani: registers[C] = registers[A] & value B
registers = [3, 2, 1, 1]
result = execute_opcode('bani', registers, 0, 1, 2)
expected = [3, 2, 1, 1]  # 3 & 1 = 0b11 & 0b01 = 0b01 = 1
assert result == expected
```

#### Bitwise OR Operations
```python
# borr: registers[C] = registers[A] | registers[B]
registers = [1, 2, 0, 0]  # 1=0b01, 2=0b10
result = execute_opcode('borr', registers, 0, 1, 3)
expected = [1, 2, 0, 3]  # 1 | 2 = 0b01 | 0b10 = 0b11 = 3
assert result == expected

# bori: registers[C] = registers[A] | value B
registers = [1, 2, 0, 0]
result = execute_opcode('bori', registers, 0, 2, 3)
expected = [1, 2, 0, 3]  # 1 | 2 = 0b01 | 0b10 = 0b11 = 3
assert result == expected
```

#### Assignment Operations
```python
# setr: registers[C] = registers[A] (B is ignored)
registers = [5, 2, 1, 1]
result = execute_opcode('setr', registers, 0, 99, 2)
expected = [5, 2, 5, 1]  # registers[2] = registers[0] = 5
assert result == expected

# seti: registers[C] = value A (B is ignored)
registers = [5, 2, 1, 1]
result = execute_opcode('seti', registers, 7, 99, 3)
expected = [5, 2, 1, 7]  # registers[3] = 7
assert result == expected
```

#### Greater-than Testing
```python
# gtir: registers[C] = 1 if value A > registers[B] else 0
registers = [0, 1, 2, 3]
result = execute_opcode('gtir', registers, 5, 2, 3)
expected = [0, 1, 2, 1]  # 5 > registers[2]=2 → True → 1
assert result == expected

result = execute_opcode('gtir', registers, 1, 2, 3)
expected = [0, 1, 2, 0]  # 1 > registers[2]=2 → False → 0
assert result == expected

# gtri: registers[C] = 1 if registers[A] > value B else 0
registers = [5, 1, 2, 3]
result = execute_opcode('gtri', registers, 0, 3, 2)
expected = [5, 1, 1, 3]  # registers[0]=5 > 3 → True → 1
assert result == expected

# gtrr: registers[C] = 1 if registers[A] > registers[B] else 0
registers = [5, 1, 2, 3]
result = execute_opcode('gtrr', registers, 0, 1, 3)
expected = [5, 1, 2, 1]  # registers[0]=5 > registers[1]=1 → True → 1
assert result == expected
```

#### Equality Testing
```python
# eqir: registers[C] = 1 if value A == registers[B] else 0
registers = [0, 1, 2, 3]
result = execute_opcode('eqir', registers, 2, 2, 3)
expected = [0, 1, 2, 1]  # 2 == registers[2]=2 → True → 1
assert result == expected

result = execute_opcode('eqir', registers, 5, 2, 3)
expected = [0, 1, 2, 0]  # 5 == registers[2]=2 → False → 0
assert result == expected

# eqri: registers[C] = 1 if registers[A] == value B else 0
registers = [5, 1, 2, 3]
result = execute_opcode('eqri', registers, 0, 5, 2)
expected = [5, 1, 1, 3]  # registers[0]=5 == 5 → True → 1
assert result == expected

# eqrr: registers[C] = 1 if registers[A] == registers[B] else 0
registers = [2, 1, 2, 3]
result = execute_opcode('eqrr', registers, 0, 2, 3)
expected = [2, 1, 2, 1]  # registers[0]=2 == registers[2]=2 → True → 1
assert result == expected
```

**Verification Method**: Create a test file `test_opcodes.py` with these assertions

### 2. Integration Test: Example from Problem Statement

**Objective**: Verify the complete flow works with the given example

**Test Case**:
```python
Before: [3, 2, 1, 1]
Instruction: 9 2 1 2
After: [3, 2, 2, 1]
```

**Expected Behavior**:
- Should match exactly 3 opcodes: mulr, addi, seti
- Verify count_matching_opcodes returns 3
- This sample should be counted in the final answer (since 3 >= 3)

**Manual Verification**:
1. **mulr** (A=2, B=1, C=2): registers[2] * registers[1] = 1 * 2 = 2 ✓
2. **addi** (A=2, B=1, C=2): registers[2] + 1 = 1 + 1 = 2 ✓
3. **seti** (A=2, B=1, C=2): 2 → registers[2] ✓

**Test Implementation**:
```python
before = (3, 2, 1, 1)
instruction = (9, 2, 1, 2)
after = (3, 2, 2, 1)

count = count_matching_opcodes(before, instruction, after)
assert count == 3, f"Expected 3 matches, got {count}"

# Optionally verify which opcodes match (using helper function if implemented)
# matches = find_matching_opcodes(before, instruction, after)
# assert 'mulr' in matches
# assert 'addi' in matches
# assert 'seti' in matches
```

### 3. Integration Test: Input Parsing

**Objective**: Verify input parsing correctly extracts samples and stops at the right boundary

**Test Approach**:
1. Create a small test input file with 2-3 samples followed by double blank line
2. Parse it and verify:
   - Correct number of samples extracted
   - Register values are tuples of integers
   - Instruction values are tuples of integers
   - Format matches expected structure
   - Parsing stops at double blank line (doesn't try to parse test program)

**Test Input** (`test_input.txt`):
```
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

Before: [1, 1, 1, 1]
5 0 0 0
After:  [2, 1, 1, 1]


4 0 2 0
13 2 0 2
```

**Test Code**:
```python
samples = parse_input('test_input.txt')
assert len(samples) == 2, f"Expected 2 samples, got {len(samples)}"

before1, instr1, after1 = samples[0]
assert before1 == (3, 2, 1, 1)
assert instr1 == (9, 2, 1, 2)
assert after1 == (3, 2, 2, 1)

before2, instr2, after2 = samples[1]
assert before2 == (1, 1, 1, 1)
assert instr2 == (5, 0, 0, 0)
assert after2 == (2, 1, 1, 1)
```

### 4. Edge Case Tests

**Objective**: Test boundary conditions and special cases

#### Test Case 1: Sample that matches exactly 3 opcodes (boundary - should be counted)
```python
# Using the example from problem statement
before = (3, 2, 1, 1)
instruction = (9, 2, 1, 2)
after = (3, 2, 2, 1)
count = count_matching_opcodes(before, instruction, after)
assert count == 3
# This should be counted in final result
```

#### Test Case 2: Sample that matches exactly 2 opcodes (boundary - should NOT be counted)
```python
# Need to find or create an example with exactly 2 matches
before = (1, 1, 1, 1)
instruction = (0, 0, 0, 0)
after = (1, 1, 1, 1)
count = count_matching_opcodes(before, instruction, after)
# Verify count < 3 (this sample should NOT be counted in final result)
assert count < 3
```

#### Test Case 3: Sample that matches 4+ opcodes (should be counted)
```python
# Find an example that matches multiple opcodes
# Verify it's counted in the final result
```

#### Test Case 4: Zero values in registers
```python
before = (0, 0, 0, 0)
instruction = (1, 0, 1, 2)
after = (0, 0, 0, 0)
# Test that operations work correctly with zeros
# This tests edge cases for multiplication, addition, and comparisons
```

#### Test Case 5: Larger register values
```python
before = (100, 200, 50, 75)
instruction = (0, 0, 1, 2)
after = (100, 200, 300, 75)
# Test with larger values to ensure arithmetic works correctly
# Python handles arbitrary integers, so no overflow concerns
```

### 5. Full Solution Test

**Objective**: Run against actual input and verify output format

**Test Steps**:
1. Run `python solution.py`
2. Verify output is a single integer
3. Verify output is reasonable (likely between 0 and ~1000)
4. Check that program completes in reasonable time (< 1 second expected)

**Validation**:
- Output should be printed to stdout
- No errors or exceptions
- No extraneous output (debug prints should be removed)

### 6. Regression Tests

**Objective**: Ensure changes don't break working functionality

**Approach**:
1. Run the solution against input.md to get the initial answer
2. Manually verify the answer makes sense (should be between 0 and total number of samples)
3. Save the answer for future regression testing
4. Use this test for any refactoring or debugging

**Setup Process**:
1. First run: `python solution.py` and note the output
2. Add the output to the regression test
3. Future runs verify consistency

```python
def test_regression():
    result = solve('input.md')
    # After first successful run, record the answer here:
    EXPECTED_ANSWER = None  # Replace with actual answer after first run
    if EXPECTED_ANSWER is not None:
        assert result == EXPECTED_ANSWER
```

## Test Execution Order

1. **First**: Test individual opcodes (catch implementation bugs early)
2. **Second**: Test example from problem (verify integration)
3. **Third**: Test input parsing (ensure data loading works)
4. **Fourth**: Test edge cases (ensure robustness)
5. **Fifth**: Run full solution (get the answer)
6. **Sixth**: Set up regression test (prevent future breaks)

## Debugging Strategies

If tests fail:

1. **Opcode test fails**:
   - Print before/after states
   - Manually calculate expected result
   - Check if/elif logic for typos

2. **Example test fails**:
   - Print which opcodes matched
   - Manually verify each opcode
   - Check parameter extraction (A, B, C)

3. **Parsing test fails**:
   - Print raw input
   - Check regex patterns
   - Verify line splitting logic

4. **Wrong final answer**:
   - Add debug output to show count per sample
   - Find samples with unexpected match counts
   - Manually verify those samples

## Success Criteria

✓ All 16 individual opcode tests pass
✓ Problem example returns count of 3
✓ Input parsing extracts correct number of samples
✓ Final solution runs without errors
✓ Output is a reasonable integer value
✓ Solution completes in < 1 second

## Test File Structure

```
/app/agent_workspace/2018/day_16/part_1/
├── solution.py           # Main solution
├── test_solution.py      # Comprehensive test suite (optional)
├── test_input.txt        # Small test input for parsing tests (optional)
└── input.md              # Actual problem input
```

**Note**: For this scripting task, a simple test file or inline tests in solution.py are sufficient. No need for complex test infrastructure.

## Manual Verification Checklist

Before submitting answer:
- [ ] Verified example from problem.md works correctly
- [ ] Checked at least 2-3 samples from input.md manually
- [ ] Confirmed all 16 opcodes are implemented
- [ ] Verified output is single integer
- [ ] No debug print statements in final code
