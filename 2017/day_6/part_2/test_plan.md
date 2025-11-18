# Testing Plan: Memory Reallocation Loop Size Detection (Part 2)

## Testing Objectives
1. Verify the loop size calculation is correct
2. Ensure dictionary tracking works properly
3. Validate redistribution logic remains correct from Part 1
4. Confirm the solution handles the actual input correctly

## Test Strategy Overview
- **Unit Tests**: Test individual functions in isolation
- **Integration Tests**: Test the complete loop detection with known examples
- **Edge Case Tests**: Test boundary conditions and special scenarios
- **Validation Test**: Verify against the actual input

---

## 1. Unit Tests

### Test 1.1: Parse Input Function
**Purpose**: Verify input parsing works correctly

**Note**: The `split()` method without arguments handles all whitespace (spaces, tabs, newlines).

**Test Cases**:
```python
# Test case 1: Normal input with spaces
input_str = "11 11 13 7 0 15 5 5 4 4 1 1 7 1 15 11"
expected = [11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11]
assert parse_input(input_str) == expected

# Test case 2: Input with tabs (as in actual input.md)
input_str = "11\t11\t13\t7\t0\t15\t5\t5\t4\t4\t1\t1\t7\t1\t15\t11"
expected = [11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11]
assert parse_input(input_str) == expected

# Test case 3: Small input
input_str = "0 2 7 0"
expected = [0, 2, 7, 0]
assert parse_input(input_str) == expected
```

### Test 1.2: Find Max Bank Function
**Purpose**: Verify max bank detection with tie-breaking

**Test Cases**:
```python
# Test case 1: Clear maximum
banks = [0, 2, 7, 0]
assert find_max_bank(banks) == 2  # Index 2 has value 7

# Test case 2: Tie - should return lowest index
banks = [7, 2, 7, 0]
assert find_max_bank(banks) == 0  # Tie between index 0 and 2, choose 0

# Test case 3: Maximum at first position
banks = [15, 11, 11, 7, 0]
assert find_max_bank(banks) == 0

# Test case 4: Maximum at last position
banks = [0, 2, 3, 8]
assert find_max_bank(banks) == 3

# Test case 5: All same values - should return index 0
banks = [5, 5, 5, 5]
assert find_max_bank(banks) == 0
```

### Test 1.3: Redistribute Function
**Purpose**: Verify redistribution logic is correct

**Test Cases**:
```python
# Test case 1: Example from problem (0 2 7 0 -> 2 4 1 2)
banks = [0, 2, 7, 0]
redistribute(banks)
assert banks == [2, 4, 1, 2]

# Test case 2: Second redistribution (2 4 1 2 -> 3 1 2 3)
banks = [2, 4, 1, 2]
redistribute(banks)
assert banks == [3, 1, 2, 3]

# Test case 3: Wrap-around case
banks = [0, 0, 0, 5]  # Bank 3 has 5 blocks
redistribute(banks)
assert banks == [2, 1, 1, 1]  # Distributes to indices 0, 1, 2, 3, 0 (in that order)

# Test case 4: Single block redistribution
banks = [0, 1, 0, 0]
redistribute(banks)
assert banks == [0, 0, 1, 0]

# Test case 5: Large redistribution
banks = [0, 0, 10, 0]
redistribute(banks)
assert banks == [3, 2, 2, 3]  # 10 blocks distributed starting at index 3: [3,0,1,2,3,0,1,2,3,0]
```

---

## 2. Integration Tests

### Test 2.1: Example from Problem Statement
**Purpose**: Verify complete loop size calculation with known example

**Test Case**:
```python
banks = [0, 2, 7, 0]
loop_size = find_loop_size(banks)
assert loop_size == 4
```

**Manual Verification**:
- Cycle 0: `(0, 2, 7, 0)` - stored at cycle 0
- Cycle 1: `(2, 4, 1, 2)` - stored at cycle 1
- Cycle 2: `(3, 1, 2, 3)` - stored at cycle 2
- Cycle 3: `(0, 2, 3, 4)` - stored at cycle 3
- Cycle 4: `(1, 3, 4, 1)` - stored at cycle 4
- Cycle 5: `(2, 4, 1, 2)` - **REPEAT!** First seen at cycle 1
- Loop size = 5 - 1 = 4 ✓

### Test 2.2: Immediate Loop
**Purpose**: Test case where configuration repeats immediately

**Test Case**:
```python
# Configuration that returns to itself in one step
# This is a theoretical case for testing logic
banks = [2, 0, 0]  # After redistribution: [0, 1, 1]
# Continue cycling until it repeats
loop_size = find_loop_size(banks)
assert loop_size > 0  # Should find some loop size
```

### Test 2.3: Small Loop
**Purpose**: Test a configuration with a small loop size

**Test Case**:
```python
banks = [5]  # Single bank - should loop immediately
loop_size = find_loop_size(banks)
# Manually trace:
# Cycle 0: (5,) - stored
# Redistribute: max at index 0, distribute 5 blocks starting at (0+1)%1=0
# Result: [5]
# Cycle 1: (5,) - REPEAT at cycle 0
# Loop size = 1 - 0 = 1
assert loop_size == 1
```

---

## 3. Edge Case Tests

### Test 3.1: Single Bank
**Purpose**: Verify behavior with minimal configuration

**Test Case**:
```python
banks = [5]
loop_size = find_loop_size(banks)
# With one bank, redistribution gives [5] -> [0] + 5 to bank 0 = [5]
# Should loop immediately
assert loop_size == 1
```

### Test 3.2: All Zeros
**Purpose**: Test with no blocks to redistribute

**Test Case**:
```python
banks = [0, 0, 0, 0]
loop_size = find_loop_size(banks)
# All zeros should stay all zeros
assert loop_size == 1
```

### Test 3.3: Large Number of Banks
**Purpose**: Ensure algorithm scales reasonably

**Test Case**:
```python
# Create a larger bank configuration
banks = [i for i in range(20)]  # [0, 1, 2, ..., 19]
loop_size = find_loop_size(banks)
# Should complete in reasonable time and return valid loop size
assert loop_size > 0
assert isinstance(loop_size, int)
```

---

## 4. Validation Tests

### Test 4.1: Actual Input Validation
**Purpose**: Verify the solution works on the actual puzzle input

**Test Case**:
```python
# Read actual input
with open('input.md', 'r') as f:
    input_data = f.read()

banks = parse_input(input_data)
assert len(banks) == 16  # Verify we have 16 banks
assert banks == [11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11]

loop_size = find_loop_size(banks)
assert loop_size > 0
assert isinstance(loop_size, int)
print(f"Loop size for actual input: {loop_size}")
```

### Test 4.2: Relationship with Part 1
**Purpose**: Verify logical consistency between Part 1 and Part 2

**Validation Logic**:
```python
# The loop size should be < the total cycles from Part 1
# Part 1 answer: 4074 cycles until first repeat
# Part 2 answer should be loop_size < 4074 (or == 4074 if loop returns to initial state)

assert loop_size <= 4074  # Loop can't be larger than total cycles
assert loop_size > 0      # Loop size must be positive
```

**Reasoning**:
- Part 1 tells us it takes 4074 cycles to see the first repeated configuration
- Part 2 tells us the loop size (cycles between first and second occurrence)
- The loop size must be ≤ 4074 since the first occurrence happens by cycle 4074
- Most likely loop_size < 4074 (equality only if the repeated config is the initial state)

---

## 5. Manual Trace Test

### Test 5.1: Step-by-Step Trace of Example
**Purpose**: Manually verify the algorithm step by step

**Procedure**:
1. Start with `banks = [0, 2, 7, 0]`
2. Initialize `seen_at = {(0, 2, 7, 0): 0}`
3. Run redistribution and track:

```
Cycle 0: Config (0, 2, 7, 0) -> seen_at[(0, 2, 7, 0)] = 0

Redistribute:
  Max bank: index 2 (value 7)
  Distribute 7 blocks starting at index 3
  Result: [2, 4, 1, 2]

Cycle 1: Config (2, 4, 1, 2) -> seen_at[(2, 4, 1, 2)] = 1

Redistribute:
  Max bank: index 1 (value 4)
  Distribute 4 blocks starting at index 2
  Result: [3, 1, 2, 3]

Cycle 2: Config (3, 1, 2, 3) -> seen_at[(3, 1, 2, 3)] = 2

Redistribute:
  Max bank: index 0 (value 3, wins tie)
  Distribute 3 blocks starting at index 1
  Result: [0, 2, 3, 4]

Cycle 3: Config (0, 2, 3, 4) -> seen_at[(0, 2, 3, 4)] = 3

Redistribute:
  Max bank: index 3 (value 4)
  Distribute 4 blocks starting at index 0
  Result: [1, 3, 4, 1]

Cycle 4: Config (1, 3, 4, 1) -> seen_at[(1, 3, 4, 1)] = 4

Redistribute:
  Max bank: index 2 (value 4)
  Distribute 4 blocks starting at index 3
  Result: [2, 4, 1, 2]

Cycle 5: Config (2, 4, 1, 2) -> FOUND in seen_at! First at cycle 1
Loop size = 5 - 1 = 4 ✓
```

---

## 6. Test Execution Strategy

### Phase 1: Component Testing
1. Run unit tests for `parse_input()`
2. Run unit tests for `find_max_bank()`
3. Run unit tests for `redistribute()`
4. Verify all component tests pass before proceeding

### Phase 2: Integration Testing
1. Test with the example from problem statement
2. Test edge cases (single bank, all zeros, etc.)
3. Verify loop size calculation is correct

### Phase 3: Final Validation
1. Run solution on actual input
2. Verify output is a positive integer
3. Check relationship with Part 1 answer (loop_size ≤ 4074)
4. Print and verify the final answer

### Phase 4: Performance Check
1. Time the execution on actual input
2. Verify it completes in under 1 second
3. Check memory usage is reasonable

---

## Expected Test Results

### Example Input Test
- **Input**: `[0, 2, 7, 0]`
- **Expected Output**: `4`

### Actual Input Test
- **Input**: `[11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11]`
- **Expected Output**: A positive integer ≤ 4074

### Performance Expectations
- **Runtime**: < 1 second
- **Memory**: < 100 MB
- **Correctness**: 100% pass rate on all test cases

---

## Test Completion Checklist
- [ ] All unit tests pass
- [ ] Example test produces output of 4
- [ ] Edge cases handled correctly
- [ ] Actual input produces valid output
- [ ] Loop size ≤ 4074 (Part 1 answer)
- [ ] Solution completes in reasonable time
- [ ] No errors or exceptions during execution
