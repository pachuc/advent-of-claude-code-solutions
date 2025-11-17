# Testing Plan: Package Balancing and Quantum Entanglement Optimization

## Plan Updates (Based on Critique)

This testing plan has been updated to address the following key issues:

1. **Fixed Test 1.2 Case D**: Corrected the incorrect test case where `sum(remaining) == target`. Changed to a valid case where `sum(remaining) == 2 * target` and can be split into two equal groups.

2. **Fixed Test 3.1**: Properly formatted the test for indivisible total weight with executable code instead of just showing input examples.

3. **Completed Test 3.2**: Added a concrete, valid example of an impossible partition scenario (where Group 1 can be formed but remaining packages cannot be split).

4. **Improved Test 3.4**: Added clear validation logic and expected outcomes for testing multiple valid configurations.

5. **Added Test 3.0**: New test for invalid input handling (empty input, negative weights, zero weights).

6. **Fixed Test 1.1**: Updated to use proper file I/O with temporary files instead of passing strings directly.

7. **Added executable memory test**: Included actual code using `tracemalloc` for Test 4.2 instead of vague instructions.

8. **Clarified Test 5.2**: Changed from "search online" to "submit to Advent of Code system" as the verification method.

## Testing Strategy Overview

The testing approach focuses on:
1. Validating algorithm correctness with known examples
2. Verifying edge cases and boundary conditions
3. Ensuring the solution handles the actual input correctly
4. Performance validation for acceptable runtime

## Test Categories

### 1. Unit Tests - Individual Components

#### Test 1.1: Input Parsing
**Objective:** Verify input parsing correctly reads and converts package weights

**Test cases:**
- Valid input with multiple lines
- Input with trailing newlines
- Input with empty lines (should be filtered)

**Validation:**
```python
# Create a temporary test file
import tempfile
import os

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write("1\n2\n3\n\n")
    test_file = f.name

try:
    result = parse_input(test_file)
    assert result == [1, 2, 3], f"Expected [1, 2, 3], got {result}"
finally:
    os.unlink(test_file)
```

**Expected outcome:** List of integers matching input

#### Test 1.2: Subset Sum Validation (can_partition_remaining)
**Objective:** Verify DP algorithm correctly identifies if remaining packages can form two equal groups

**Test cases:**

**Case A: Simple valid partition**
```python
remaining = [1, 2, 3, 4, 5, 6]
target = 9
# Can form: [6, 3] and [5, 4] or [6, 2, 1] and [5, 4]
assert can_partition_remaining(remaining, target) == True
```

**Case B: No valid partition**
```python
remaining = [5, 7, 11]
target = 10
# Cannot sum to 10 with any subset
assert can_partition_remaining(remaining, target) == False
```

**Case C: Exact single package**
```python
remaining = [10, 5, 3]
target = 10
# Single package equals target
assert can_partition_remaining(remaining, target) == True
```

**Case D: Valid partition with all packages needed for one subset**
```python
remaining = [1, 2, 3, 4]  # sum = 10
target = 5
# Can form [1, 4] = 5 and [2, 3] = 5
assert can_partition_remaining(remaining, target) == True
```

**Expected outcomes:** Boolean values matching possibility of partition

#### Test 1.3: Quantum Entanglement Calculation
**Objective:** Verify QE calculation (product of weights)

**Test cases:**
```python
# Test case 1
packages = [11, 9]
assert calculate_qe(packages) == 99

# Test case 2
packages = [1, 2, 3, 4]
assert calculate_qe(packages) == 24

# Test case 3 - single package
packages = [100]
assert calculate_qe(packages) == 100

# Test case 4 - large values
packages = [113, 109, 107]
assert calculate_qe(packages) == 1319419
```

**Expected outcomes:** Correct product values

### 2. Integration Tests - Complete Algorithm

#### Test 2.1: Example from Problem Statement
**Objective:** Verify solution matches the given example

**Input:**
```
1
2
3
4
5
7
8
9
10
11
```

**Expected behavior:**
- Total weight: 60
- Target per group: 20
- Minimum Group 1 size: 2
- Optimal Group 1: [11, 9]
- QE: 99

**Validation:**
```python
result = solve(example_packages)
assert result == 99
```

**Expected outcome:** Result = 99

#### Test 2.2: Actual Input
**Objective:** Verify solution completes and produces a result for the actual input

**Input:** The 28 packages from `input.md`

**Validation steps:**
1. Calculate total weight = 1548
2. Verify divisible by 3: 1548 % 3 == 0 ✓
3. Target per group = 516
4. Run solver
5. Verify result is a positive integer
6. Verify runtime < 30 seconds (acceptable threshold)

**Expected outcome:** A positive integer representing minimum QE

### 3. Edge Case Tests

#### Test 3.0: Invalid Input Handling
**Objective:** Verify handling of invalid inputs

**Test cases:**

**Empty input:**
```python
packages = []
result = solve(packages)
assert result is None, "Should handle empty input"
```

**Negative weights:**
```python
packages = [1, -2, 3]
result = solve(packages)
assert result is None, "Should reject negative weights"
```

**Zero weights:**
```python
packages = [0, 1, 2]
result = solve(packages)
assert result is None, "Should reject zero weights"
```

**Expected outcome:** Return None for all invalid inputs

#### Test 3.1: Indivisible Total Weight
**Objective:** Verify handling when total weight not divisible by 3

**Input:**
```python
packages = [1, 2, 3, 4, 6]  # total = 16 (not divisible by 3)
result = solve(packages)
assert result is None, f"Expected None for indivisible total, got {result}"
```

**Expected outcome:** Return None since no valid partition exists

#### Test 3.2: Impossible Partition
**Objective:** Test case where Group 1 can sum to target, but remaining cannot be split

**Constructed example:**
```python
packages = [9, 3, 3, 3]  # total = 18, target = 6
# Possible Group 1: [3, 3] = 6
# Remaining: [9, 3] = 12, need to split into two groups of 6 each
# But [9, 3] cannot form [6, 6] because 9 > 6 and 3 < 6

# Test the partition validation directly
remaining = [9, 3]
target = 6
assert can_partition_remaining(remaining, target) == False, \
    "Should be False because we cannot form a subset of 6 from [9, 3]"
```

**Note:** In this scenario, when we try Group 1 = [3, 3], the `can_partition_remaining()`
function should correctly return False, and the algorithm will skip this Group 1
configuration. It will then try other configurations until it finds a valid one, or
determine no solution exists.

**Expected outcome:** The validation correctly identifies impossible partitions

#### Test 3.3: Minimum Group Size = 1
**Objective:** Test when a single package equals target weight

**Input:**
```
packages = [10, 5, 3, 2]
total = 20
target = 20/3 = 6.67 (not integer, invalid)
```

**Better example:**
```
packages = [6, 3, 2, 1]
total = 12
target = 4
```
- Group 1: [3, 1] or [2, 2] (wait, only one 2)
- Group 1: [3, 1] = 4, remaining [6, 2] = 8, need to split into [4] and [4]
- [6, 2] cannot form [4, 4] - no valid subset sums to 4

This is complex to construct; we'll rely on algorithm correctness.

#### Test 3.4: Multiple Valid Configurations at Same Size
**Objective:** Verify algorithm finds MINIMUM QE among multiple valid configurations of the same group size

**Constructed example:**
```python
# Simplified test case
packages = [6, 5, 4, 3, 2, 1, 3, 2, 1]  # total = 27, target = 9

# Possible Group 1 configurations of size 2:
# [6, 3] = 9, QE = 18
# [5, 4] = 9, QE = 20
# (and potentially others)

# The algorithm should find BOTH valid configurations at size 2
# and return the minimum QE

result = solve(packages)
# Verify result is positive (solution exists)
assert result is not None and result > 0, \
    f"Expected valid solution, got {result}"

# To fully test this, we'd need to manually verify which Group 1
# combinations of the minimum size are valid, then check that
# the returned QE matches the minimum among them.
```

**Expected outcome:** Algorithm returns the minimum QE among all valid configurations of the smallest group size

### 4. Performance Tests

#### Test 4.1: Runtime Validation
**Objective:** Ensure solution completes within reasonable time

**Validation:**
```python
import time
start = time.time()
result = solve(actual_packages)
duration = time.time() - start

assert duration < 30  # Should complete in under 30 seconds
print(f"Completed in {duration:.2f} seconds")
```

**Expected outcome:** Completion in under 30 seconds

#### Test 4.2: Memory Usage
**Objective:** Verify solution doesn't exhaust memory

**Validation:**
```python
import tracemalloc

# Start tracking memory
tracemalloc.start()

# Run the solution
result = solve(actual_packages)

# Get peak memory usage
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Convert to MB for readability
peak_mb = peak / 1024 / 1024

print(f"Peak memory usage: {peak_mb:.2f} MB")
assert peak_mb < 1024, f"Memory usage too high: {peak_mb:.2f} MB"
```

**Expected outcome:** Memory usage remains reasonable (< 1 GB)

### 5. Validation of Final Answer

#### Test 5.1: Manual Verification of Result
**Objective:** Verify the final answer makes logical sense

**Validation steps:**
1. Run solver on actual input
2. Get the optimal Group 1 configuration (modify code to print it)
3. Verify:
   - Sum of Group 1 = 516
   - QE calculation is correct (multiply weights manually)
   - Remaining packages sum to 1032 (2 × 516)
   - Remaining packages CAN be split into two groups of 516

**Example validation:**
```python
result = solve_and_return_details(actual_packages)
group1 = result['group1']
qe = result['qe']

# Verify sum
assert sum(group1) == 516

# Verify QE
assert math.prod(group1) == qe

# Verify remaining
remaining = [p for p in packages if p not in group1]
assert sum(remaining) == 1032
assert can_partition_remaining(remaining, 516) == True
```

#### Test 5.2: Cross-Reference with Advent of Code System
**Objective:** Verify answer is accepted by the Advent of Code system

**Validation:**
- Run the solution on the actual input
- Submit the answer to Advent of Code 2015 Day 24 Part 1
- If incorrect, the system will provide feedback
- Debug and resubmit until correct

**Note:** This is the ultimate validation that our solution is correct.

### 6. Regression Tests

#### Test 6.1: Example Case Regression
**Objective:** Ensure example case always returns 99

**Validation:**
```python
def test_example_case():
    packages = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    result = solve(packages)
    assert result == 99, f"Expected 99, got {result}"
```

**Run after any code changes:** Ensure we haven't broken the basic algorithm

## Testing Execution Plan

### Phase 1: Unit Testing
1. Write and run test for `parse_input()`
2. Write and run tests for `can_partition_remaining()` (4 test cases)
3. Write and run tests for `calculate_qe()` (4 test cases)
4. Fix any issues found

### Phase 2: Integration Testing
1. Test with example case (expected: 99)
2. If fails, debug:
   - Check Group 1 combinations generated
   - Check subset sum validation
   - Check QE calculation
3. Once example passes, test with actual input
4. Measure runtime and verify < 30 seconds

### Phase 3: Edge Case Validation
1. Test indivisible total (if applicable to problem)
2. Test multiple valid configurations (verify minimum QE chosen)
3. Document any edge cases that cause issues

### Phase 4: Final Validation
1. Run solution on actual input
2. Print the optimal Group 1 configuration
3. Manually verify:
   - Group 1 sum = 516
   - QE calculation correct
   - Remaining can be split
4. Submit answer

## Test Data Summary

| Test | Input | Expected Output | Purpose |
|------|-------|-----------------|---------|
| Example | 1,2,3,4,5,7,8,9,10,11 | 99 | Verify correctness |
| Actual Input | 28 packages from input.md | Positive integer | Get solution |
| Subset Sum - Valid | [1,2,3,4,5,6], target=9 | True | Validate DP |
| Subset Sum - Invalid | [5,7,11], target=10 | False | Validate DP |
| QE Calculation | [11,9] | 99 | Verify product |
| Performance | Actual input | Runtime < 30s | Efficiency |

## Success Criteria

1. ✓ All unit tests pass
2. ✓ Example case returns 99
3. ✓ Actual input produces a positive integer
4. ✓ Runtime < 30 seconds
5. ✓ Manual verification of final answer confirms correctness
6. ✓ Answer matches known solution (if available)

## Debugging Strategy

If tests fail:

1. **Example case fails:**
   - Print all Group 1 candidates at each size
   - Verify combinations generation
   - Check subset sum validation logic
   - Verify QE calculation

2. **Actual input fails or times out:**
   - Add progress logging to see which group size being tested
   - Check if stuck in infinite loop
   - Verify early stopping logic
   - Consider additional optimizations

3. **Wrong answer on actual input:**
   - Print the optimal Group 1 found
   - Manually verify sum = 516
   - Manually verify QE calculation
   - Check if remaining packages can actually be split
   - Review partition validation logic

## Summary of Test Corrections

| Original Issue | Correction Made | Test Reference |
|----------------|-----------------|----------------|
| Test 1.2 Case D had incorrect logic | Fixed to use `target=5` with `sum=10` instead of `target=10` with `sum=10` | Test 1.2 Case D |
| Test 1.1 used string instead of file | Updated to use temporary file with proper I/O | Test 1.1 |
| Test 3.1 had wrong total | Changed to use total=16 (not divisible by 3) | Test 3.1 |
| Test 3.2 admitted difficulty | Added concrete example with [9,3,3,3] packages | Test 3.2 |
| Test 3.4 was incomplete | Added validation logic and expected outcomes | Test 3.4 |
| Test 4.2 had no implementation | Added tracemalloc code for memory monitoring | Test 4.2 |
| Test 5.2 was vague | Changed to "submit to AoC system" | Test 5.2 |
| Missing invalid input tests | Added Test 3.0 for empty, negative, zero weights | Test 3.0 |

## Test Execution Checklist

- [ ] Parse input correctly (Test 1.1)
- [ ] Subset sum DP works for simple cases (Test 1.2 A-D)
- [ ] QE calculation correct (Test 1.3)
- [ ] Helper function works (get_remaining_packages)
- [ ] Invalid inputs handled (Test 3.0)
- [ ] Example case returns 99 (Test 2.1)
- [ ] Actual input completes in < 30 seconds (Test 4.1)
- [ ] Memory usage reasonable (Test 4.2)
- [ ] Final answer verified manually (Test 5.1)
- [ ] Answer accepted by AoC system (Test 5.2)
- [ ] No runtime errors or exceptions
- [ ] Code is readable and well-commented
