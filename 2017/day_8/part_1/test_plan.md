# Testing Plan: Register Instruction Processor

## Test Strategy Overview

The testing approach will verify correctness through:
1. **Unit tests** for individual functions
2. **Integration tests** for the complete flow
3. **Edge case validation** for boundary conditions
4. **Example verification** against provided sample
5. **Manual verification** of final answer with actual input
6. **Regression testing** to ensure answer consistency

## Updates Based on Critique

This plan has been updated to address the following improvements:
- Fixed function naming to match implementation (`parse_instruction_line` instead of `parse_single_line`)
- Added explicit test for multi-character comparators (>=, <=)
- Enhanced integration test with regression testing (record answer for future verification)
- Added test for large values to verify Python's integer handling
- Improved debugging strategy with specific verbose mode usage
- Clarified test file structure and imports
- Added manual trace verification steps for higher confidence

## Test Cases

### 1. Example Input Validation

**Purpose**: Verify solution works correctly with the provided example

**Test Data**:
```
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
```

**Expected Behavior**:
- After instruction 1: a=0, b=0 (condition false: 0 > 1)
- After instruction 2: a=1, b=0 (condition true: 0 < 5)
- After instruction 3: a=1, b=0, c=10 (condition true: 1 >= 1, dec -10 = +10)
- After instruction 4: a=1, b=0, c=-10 (condition true: 10 == 10, inc -20 = -20)
- Maximum value: 1

**Verification Method**:
```python
# Create test file with example input
# Run solution
# Assert output == 1
```

**Pass Criteria**: Output must be exactly `1`

---

### 2. Parsing Function Tests

**Purpose**: Ensure input parsing correctly extracts all instruction components

**Test Cases**:

#### 2.1 Standard Instruction Parsing
```python
line = "a inc 5 if b < 10"
result = parse_instruction_line(line)
assert result == {
    'target_reg': 'a',
    'operation': 'inc',
    'amount': 5,
    'cond_reg': 'b',
    'comparator': '<',
    'cond_val': 10
}
```

#### 2.2 Negative Amount Parsing
```python
line = "c dec -10 if a >= 1"
result = parse_instruction_line(line)
assert result['amount'] == -10
```

#### 2.3 Multi-character Register Names
```python
line = "pq inc -45 if cfa == 7"
result = parse_instruction_line(line)
assert result['target_reg'] == 'pq'
assert result['cond_reg'] == 'cfa'
```

#### 2.4 Multi-character Comparators
```python
line = "x inc 10 if y >= 5"
result = parse_instruction_line(line)
assert result['comparator'] == '>='

line2 = "a dec 3 if b <= 0"
result2 = parse_instruction_line(line2)
assert result2['comparator'] == '<='
```

**Pass Criteria**: All parsed fields match expected values

---

### 3. Comparator Function Tests

**Purpose**: Verify all six comparison operators work correctly

**Test Cases**:

```python
comparators_to_test = [
    ('>', 5, 3, True),
    ('>', 3, 5, False),
    ('>', 5, 5, False),
    ('<', 3, 5, True),
    ('<', 5, 3, False),
    ('<', 5, 5, False),
    ('>=', 5, 3, True),
    ('>=', 5, 5, True),
    ('>=', 3, 5, False),
    ('<=', 3, 5, True),
    ('<=', 5, 5, True),
    ('<=', 5, 3, False),
    ('==', 5, 5, True),
    ('==', 5, 3, False),
    ('!=', 5, 3, True),
    ('!=', 5, 5, False)
]

for op, a, b, expected in comparators_to_test:
    comp = get_comparator(op)
    assert comp(a, b) == expected
```

**Pass Criteria**: All 16 comparison tests pass

---

### 4. Register Initialization Tests

**Purpose**: Verify registers default to 0 when first referenced

**Test Case**:
```python
instructions = [
    {'target_reg': 'a', 'operation': 'inc', 'amount': 5,
     'cond_reg': 'b', 'comparator': '==', 'cond_val': 0}
]
# b doesn't exist, should default to 0
# Condition: b == 0 should be True
# Result: a should be 5
```

**Expected**:
- Condition evaluates as true (b defaults to 0)
- Register 'a' is set to 5

**Pass Criteria**: Final state has a=5

---

### 5. Operation Tests

**Purpose**: Verify inc and dec operations work correctly with positive and negative amounts

**Test Cases**:

#### 5.1 Inc with Positive Amount
```python
# a inc 10 (with condition true)
# Expected: a = 0 + 10 = 10
```

#### 5.2 Inc with Negative Amount
```python
# a inc -10 (with condition true)
# Expected: a = 0 + (-10) = -10
```

#### 5.3 Dec with Positive Amount
```python
# a dec 10 (with condition true)
# Expected: a = 0 - 10 = -10
```

#### 5.4 Dec with Negative Amount
```python
# a dec -10 (with condition true)
# Expected: a = 0 - (-10) = 10
```

#### 5.5 Multiple Operations on Same Register
```python
instructions = [
    # a inc 100 if x == 0  -> a = 100
    # a dec 30 if x == 0   -> a = 70
    # a inc -50 if x == 0  -> a = 20
]
# Expected final value: 20
```

**Pass Criteria**: All operations produce mathematically correct results

---

### 6. Conditional Execution Tests

**Purpose**: Ensure instructions only execute when conditions are true

**Test Cases**:

#### 6.1 False Condition - No Modification
```python
instructions = [
    {'target_reg': 'a', 'operation': 'inc', 'amount': 100,
     'cond_reg': 'b', 'comparator': '>', 'cond_val': 10}
]
# b = 0, condition is 0 > 10 = False
# a should remain 0 (never created)
```

**Expected**: Register 'a' does not exist or equals 0

#### 6.2 True Condition - Modification Occurs
```python
instructions = [
    {'target_reg': 'a', 'operation': 'inc', 'amount': 100,
     'cond_reg': 'b', 'comparator': '<', 'cond_val': 10}
]
# b = 0, condition is 0 < 10 = True
# a should be 100
```

**Expected**: Register 'a' equals 100

**Pass Criteria**: Modifications only occur when conditions are true

---

### 7. Edge Case Tests

**Purpose**: Handle unusual but valid scenarios

#### 7.1 Empty Register Dictionary
```python
registers = {}
max_val = find_max_register_value(registers)
assert max_val == 0
```

#### 7.2 All Negative Values
```python
registers = {'a': -100, 'b': -50, 'c': -200}
max_val = find_max_register_value(registers)
assert max_val == -50
```

#### 7.3 Single Register
```python
registers = {'a': 42}
max_val = find_max_register_value(registers)
assert max_val == 42
```

#### 7.4 Zero is Maximum
```python
registers = {'a': -10, 'b': 0, 'c': -5}
max_val = find_max_register_value(registers)
assert max_val == 0
```

#### 7.5 All Instructions Have False Conditions
```python
# All conditions false, no registers modified
# Should return 0
```

#### 7.6 Large Values
```python
# Test with very large positive and negative amounts
instructions = [
    {'target_reg': 'a', 'operation': 'inc', 'amount': 10000,
     'cond_reg': 'x', 'comparator': '==', 'cond_val': 0}
]
# Expected: a = 10000
# Python handles arbitrary integers, but verify no issues
```

**Pass Criteria**: All edge cases return correct values

---

### 8. Integration Test with Actual Input

**Purpose**: Verify solution works end-to-end with the full input file

**Test Procedure**:
1. Run the solution on `input.md`
2. Capture the output value
3. Verify the output is a single integer
4. Manually trace a few instructions to validate correctness
5. Record the answer for regression testing

**Manual Verification Steps**:
```python
# Trace first 5-10 instructions manually:
# 1. "a dec -511 if x >= -4"
#    - x = 0 (default), condition: 0 >= -4 (TRUE)
#    - a = 0 - (-511) = 511

# 2. "pq inc -45 if cfa == 7"
#    - cfa = 0 (default), condition: 0 == 7 (FALSE)
#    - pq unchanged

# 3. "vby dec 69 if tl < 1"
#    - tl = 0 (default), condition: 0 < 1 (TRUE)
#    - vby = 0 - 69 = -69

# Continue for a few more to build confidence...
```

**Validation Method**:
1. Check that output is a reasonable integer (not error message)
2. Verify output is neither 0 (all conditions false - unlikely) nor absurdly large
3. Use verbose mode to spot-check a few intermediate states
4. Run multiple times to ensure deterministic behavior
5. **After first successful run**: Record the answer and use it as a regression test

**Pass Criteria**:
- Program executes without errors
- Outputs a single integer
- Value is deterministic (same answer on multiple runs)
- Manual trace of first few instructions matches expected behavior
- **Regression**: Answer matches recorded value on subsequent runs

---

### 9. State Consistency Tests

**Purpose**: Ensure register state is maintained correctly across instructions

**Test Case**:
```python
instructions = [
    # Set a = 100
    {'target_reg': 'a', 'operation': 'inc', 'amount': 100,
     'cond_reg': 'x', 'comparator': '==', 'cond_val': 0},
    # Use a's value in a condition
    {'target_reg': 'b', 'operation': 'inc', 'amount': 50,
     'cond_reg': 'a', 'comparator': '>', 'cond_val': 50},
    # Should execute because a=100 > 50
]
```

**Expected**:
- After instruction 1: a=100
- After instruction 2: a=100, b=50 (condition true)

**Pass Criteria**: Register values from previous instructions are correctly used in later conditions

---

### 10. Final Answer Validation

**Purpose**: Confirm the final answer is correct

**Validation Steps**:

1. **Sanity Checks**:
   - Output is an integer
   - Output is not 0 (extremely unlikely all conditions are false)
   - Output is reasonable given input size and values

2. **Determinism Check**:
   - Run the program multiple times
   - Verify same output each time

3. **Register Count Check**:
   - Print number of unique registers created
   - Verify it matches expectation from input scan (should be around 20-30 unique register names)

4. **Manual Trace Verification**:
   - Use verbose mode to trace first 10-20 instructions
   - Verify intermediate states match hand calculations
   - Spot-check a few middle and late instructions

5. **Alternative Implementation** (optional, for high confidence):
   - Implement using `collections.defaultdict(int)` instead of `dict.get()`
   - Compare results from both implementations
   - Should produce identical output

6. **Record Answer for Regression**:
   - Once validated, record the answer
   - Add a regression test that verifies future runs produce the same answer
   - This prevents accidental code changes from breaking the solution

**Pass Criteria**:
- Consistent output across runs
- Value passes sanity checks
- Manual trace matches expected behavior
- Answer recorded for future regression testing
- (Optional) Matches alternative implementation if implemented

---

## Test Execution Order

1. **Unit Tests First**: Test individual functions (parsing, comparators)
2. **Example Test**: Verify against provided example (must pass)
3. **Operation Tests**: Verify inc/dec with various amounts
4. **Conditional Tests**: Ensure conditions work correctly
5. **Edge Cases**: Test boundary conditions
6. **Integration Test**: Run on actual input
7. **Final Validation**: Manual verification and sanity checks

## Success Criteria

The solution is correct if:
- ✅ Example test returns 1
- ✅ All unit tests pass
- ✅ All edge cases handled correctly
- ✅ Actual input produces consistent output
- ✅ Manual trace of first 10-20 instructions matches expected state
- ✅ Output value is reasonable and reproducible

## Debugging Strategy

If tests fail:

1. **Parsing Issues**: Print parsed instructions, verify format
2. **Comparison Issues**: Add logging to show condition evaluations
3. **Operation Issues**: Enable verbose mode (`verbose=True`) to see register state after each instruction
4. **Wrong Answer**:
   - Use verbose mode to print state after each instruction
   - Compare against example walkthrough step-by-step
   - Check for off-by-one errors or operator precedence issues
   - Verify that inc/dec operations are applied correctly (inc adds, dec subtracts)
   - Trace the first 20-30 instructions manually if needed
5. **Unexpected Output**:
   - Ensure all comparators are working correctly
   - Verify registers default to 0 when not yet created
   - Check that conditions are evaluated before operations

## Test Implementation

Create a separate `test_solution.py` file that imports from `solution.py`:

```python
# test_solution.py
from solution import (
    parse_instruction_line,
    parse_input,
    get_comparator,
    process_instructions,
    find_max_register_value
)

def test_example():
    """Test with provided example"""
    # Create test data or temp file with example
    # Implementation here

def test_parsing():
    """Test instruction parsing"""
    line = "a inc 5 if b < 10"
    result = parse_instruction_line(line)
    assert result['target_reg'] == 'a'
    assert result['amount'] == 5
    # ... etc

def test_comparators():
    """Test all comparison operators"""
    # Implementation here

# ... etc for all test cases

if __name__ == '__main__':
    # Run all tests
    test_example()
    test_parsing()
    test_comparators()
    # ...
    print("All tests passed!")
```

**File Structure**:
```
/app/agent_workspace/2017/day_8/part_1/
├── input.md          (problem input)
├── solution.py       (main implementation)
└── test_solution.py  (test suite)
```

Run with: `python test_solution.py` or use pytest if available
