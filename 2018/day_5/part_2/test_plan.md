# Testing Plan: Optimized Polymer Reaction (Part 2)

## Overview
This testing plan ensures the Part 2 solution correctly finds the minimum polymer length achievable by removing one unit type. We'll verify correctness through multiple test levels.

## Testing Strategy

### 1. Unit Tests - Individual Components

#### Test 1.1: `reacts()` function (inherited from Part 1)
**Purpose**: Verify the basic reaction logic works correctly

**Test Cases**:
| Input a | Input b | Expected | Description |
|---------|---------|----------|-------------|
| 'a' | 'A' | True | Same type, opposite polarity |
| 'A' | 'a' | True | Same type, opposite polarity (reversed) |
| 'a' | 'a' | False | Same type, same polarity |
| 'A' | 'A' | False | Same type, same polarity |
| 'a' | 'B' | False | Different types |
| 'a' | 'b' | False | Different types, same polarity |

**Verification Method**: Direct function calls with assertions

#### Test 1.2: `react_polymer()` function (inherited from Part 1)
**Purpose**: Verify polymer reaction works correctly

**Test Cases**:
| Input | Expected Length | Expected Result | Description |
|-------|----------------|-----------------|-------------|
| 'aA' | 0 | '' | Simple reaction |
| 'abBA' | 0 | '' | Cascading reaction |
| 'abAB' | 4 | 'abAB' | No reactions |
| 'aabAAB' | 6 | 'aabAAB' | Same polarity pairs don't react |
| 'dabAcCaCBAcCcaDA' | 10 | 'dabCBAcaDA' | Example from Part 1 |
| '' | 0 | '' | Empty string edge case |
| 'a' | 1 | 'a' | Single character |
| 'aAaAaA' | 0 | '' | Multiple sequential reactions |

**Verification Method**: Direct function calls comparing both length and final polymer string

#### Test 1.3: `remove_unit_and_react()` function
**Purpose**: Verify removal and reaction work together correctly

**Test Cases**:
| Input Polymer | Unit to Remove | Expected Length | Description |
|---------------|----------------|-----------------|-------------|
| 'dabAcCaCBAcCcaDA' | 'a' | 6 | Example from problem (remove A/a) |
| 'dabAcCaCBAcCcaDA' | 'b' | 8 | Example from problem (remove B/b) |
| 'dabAcCaCBAcCcaDA' | 'c' | 4 | Example from problem (remove C/c) - best |
| 'dabAcCaCBAcCcaDA' | 'd' | 6 | Example from problem (remove D/d) |
| 'aAbBcC' | 'a' | 0 | Removing one type allows complete collapse |
| 'aAbBcC' | 'b' | 0 | Removing different type, same result |
| 'aaAA' | 'a' | 0 | Removing only type leaves empty |
| 'aAbB' | 'c' | 0 | Removing non-existent type (original reacts fully) |

**Verification Method**: Direct function calls with length assertions

### 2. Integration Tests - Full Solution

#### Test 2.1: Example from Problem Statement
**Input**: `dabAcCaCBAcCcaDA`

**Expected Process**:
- Remove A/a: length 6
- Remove B/b: length 8
- Remove C/c: length 4 (minimum)
- Remove D/d: length 6

**Expected Output**: `4`

**Verification Method**:
1. Run `find_shortest_polymer('dabAcCaCBAcCcaDA')`
2. Verify result equals 4
3. Optionally trace each removal to verify individual lengths

#### Test 2.2: Edge Case - Complete Collapse
**Input**: `aAbBcC`

**Expected**: After removing any unit type, the polymer should completely collapse

**Expected Output**: `0`

**Rationale**: Tests that the algorithm handles complete polymer collapse

#### Test 2.3: Edge Case - No Reactions in Original
**Input**: `abc` (no uppercase, no reactions possible)

**Expected**: Removing any single letter leaves 2 characters
- Remove 'a': `bc` (length 2)
- Remove 'b': `ac` (length 2)
- Remove 'c': `ab` (length 2)

**Expected Output**: `2`

**Rationale**: Tests behavior when original polymer has no reactions

#### Test 2.4: Edge Case - Empty Input
**Input**: `''` (empty string)

**Expected Output**: `0`

**Rationale**: Verify handling of empty input

#### Test 2.5: Edge Case - Single Character
**Input**: `'a'`

**Expected**: Removing 'a' leaves empty string (length 0)

**Expected Output**: `0`

#### Test 2.6: Edge Case - All Same Type
**Input**: `'aAaAaA'`

**Expected**:
- Without removal: length 0 (complete reaction)
- Remove 'a': length 0 (empty string)
- Removing any other letter: length 0 (original reactions still occur)

**Expected Output**: `0`

### 3. Validation Tests - Actual Input

#### Test 3.1: Part 1 Consistency Check
**Purpose**: Verify that without any removal, we get the Part 1 answer

**Input**: Read from `input.md`

**Test**:
```python
polymer = read_input('input.md')
original_length = react_polymer(polymer)
assert original_length == 11546  # Part 1 answer
```

**Rationale**: This ensures our Part 1 functions still work correctly

#### Test 3.2: Actual Part 2 Solution
**Purpose**: Solve the actual problem

**Input**: Read from `input.md`

**Expected**: Some value less than 11546 (Part 1 answer)

**Validation**:
1. Result should be a positive integer
2. Result should be less than 11546 (we should find improvement)
3. Result should be greater than 0 (unlikely to completely collapse)
4. Result should be reasonable (probably in range 4000-8000 based on typical reductions)

**Verification Method**:
```python
polymer = read_input('input.md')
result = find_shortest_polymer(polymer)
assert 0 < result < 11546
```

#### Test 3.3: Performance Test
**Purpose**: Verify solution runs in reasonable time

**Input**: Read from `input.md` (~50,000 characters)

**Expected**: Solution completes in < 5 seconds (should actually be well under 1 second)

**Verification Method**:
```python
import time
polymer = read_input('input.md')
start = time.time()
result = find_shortest_polymer(polymer)
elapsed = time.time() - start
print(f"Execution time: {elapsed:.3f} seconds")
assert elapsed < 5.0  # Very conservative - should be < 1s
```

**Note**: The 5-second threshold is very conservative. On modern hardware, this should complete in well under 1 second.

### 4. Correctness Verification Strategy

#### Verification 4.1: Manual Spot Check
**Method**: Pick a random unit type from the actual input and manually verify its removal and reaction

**Steps**:
1. Read actual input
2. Choose a specific unit (e.g., 'e')
3. Manually remove all 'e' and 'E' from input
4. React the result using Part 1 algorithm
5. Verify this length matches what our Part 2 algorithm reports for unit 'e'

#### Verification 4.2: Exhaustive Testing
**Method**: Verify all 26 unit types are tested

**Steps**:
1. Test all 26 letters 'a' through 'z'
2. For each unit type, verify we can compute a length
3. Verify the minimum is one of these computed lengths
4. Optionally log all 26 results to inspect manually

#### Verification 4.3: Boundary Check
**Method**: Verify the result is sensible

**Checks**:
- Result ≥ 0
- Result < original polymer length (50,000)
- Result < Part 1 answer (11,546)
- Result is an integer

### 5. Test Execution Order

**Recommended sequence**:

1. **Unit Tests First** (fastest, catch basic errors):
   - Test `reacts()`
   - Test `react_polymer()` with small examples
   - Test `remove_unit_and_react()`

2. **Integration Tests** (verify full logic):
   - Test example from problem statement (dabAcCaCBAcCcaDA → 4)
   - Test edge cases (empty, single char, etc.)

3. **Validation Tests** (verify actual solution):
   - Part 1 consistency check (should output 11546)
   - Actual Part 2 solution (should be < 11546)
   - Performance test (should complete quickly)

4. **Manual Verification** (if needed):
   - Spot check one unit type removal manually
   - Review all 26 unit type results

## Test Implementation

### Simple Test Script
Create a file `test_solution.py`:

```python
def test_examples():
    """Test with the example from the problem statement."""
    from solution import find_shortest_polymer, remove_unit_and_react

    test_polymer = 'dabAcCaCBAcCcaDA'

    # Test individual removals
    assert remove_unit_and_react(test_polymer, 'a') == 6
    assert remove_unit_and_react(test_polymer, 'b') == 8
    assert remove_unit_and_react(test_polymer, 'c') == 4
    assert remove_unit_and_react(test_polymer, 'd') == 6

    # Test finding minimum
    assert find_shortest_polymer(test_polymer) == 4

    print("✓ All example tests passed")

def test_part1_consistency():
    """Verify Part 1 answer is reproducible."""
    from solution import react_polymer, read_input

    polymer = read_input('input.md')
    result = react_polymer(polymer)
    assert result == 11546

    print("✓ Part 1 consistency check passed")

def test_actual_solution():
    """Test the actual Part 2 solution."""
    from solution import find_shortest_polymer, read_input

    polymer = read_input('input.md')
    result = find_shortest_polymer(polymer)

    # Sanity checks
    assert isinstance(result, int)
    assert result > 0
    assert result < 11546  # Should improve on Part 1

    print(f"✓ Part 2 solution: {result}")
    print(f"  Improvement over Part 1: {11546 - result} units")

if __name__ == '__main__':
    test_examples()
    test_part1_consistency()
    test_actual_solution()
```

### Running Tests

**Command**: `python test_solution.py`

**Expected Output**:
```
✓ All example tests passed
✓ Part 1 consistency check passed
✓ Part 2 solution: [some number < 11546]
  Improvement over Part 1: [positive number] units
```

## Success Criteria

The solution is correct if:

1. ✅ All unit tests pass
2. ✅ Example from problem statement returns 4
3. ✅ Part 1 consistency check returns 11546
4. ✅ Part 2 solution returns a value between 0 and 11546
5. ✅ Solution runs in under 5 seconds
6. ✅ No runtime errors or exceptions

## Edge Cases Summary

| Edge Case | Input Example | Expected Behavior |
|-----------|---------------|-------------------|
| Empty polymer | '' | Return 0 |
| Single character | 'a' | Return 0 (remove it) |
| No reactions | 'abc' | Return length - 1 |
| Complete collapse | 'aAbBcC' | Return 0 |
| All same type | 'aAaAaA' | Return 0 |
| Large input | input.md (50k chars) | Complete in < 5s |
| Part 1 baseline | input.md, no removal | Return 11546 |
