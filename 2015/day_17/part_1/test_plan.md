# Testing Plan: Container Combination Counter

## Testing Strategy Overview

The testing approach will validate:
1. **Correctness:** Algorithm produces correct results
2. **Edge cases:** Handles boundary conditions properly
3. **Performance:** Runs efficiently for given input size
4. **Input parsing:** Correctly reads and processes input

## Test Cases

### Test 1: Example from Problem Statement
**Purpose:** Verify algorithm correctness with known example

**Input:**
```
20
15
10
5
5
```

**Target:** 25 liters

**Expected Output:** 4 combinations
- 15 + 10 = 25
- 20 + 5 (first) = 25
- 20 + 5 (second) = 25
- 15 + 5 + 5 = 25

**Test Method:**
1. Create test file with example data
2. Run solution with target=25
3. Verify output equals 4

**Pass Criteria:** Output is exactly 4

---

### Test 2: Single Container Exact Match
**Purpose:** Test simplest valid case

**Input:**
```
150
```

**Target:** 150 liters

**Expected Output:** 1 combination

**Reasoning:** Only one container, and it exactly matches target

**Pass Criteria:** Output is exactly 1

---

### Test 3: No Valid Combinations
**Purpose:** Verify handling when no combination works

**Input:**
```
10
20
30
```

**Target:** 150 liters

**Expected Output:** 0 combinations

**Reasoning:** Sum of all containers (60) < target (150), impossible to reach

**Pass Criteria:** Output is exactly 0

---

### Test 4: Multiple Containers, One Solution
**Purpose:** Test case with unique solution

**Input:**
```
100
50
```

**Target:** 150 liters

**Expected Output:** 1 combination
- 100 + 50 = 150

**Pass Criteria:** Output is exactly 1

---

### Test 5: All Containers Match Target
**Purpose:** Test case where every container equals target

**Input:**
```
150
150
150
```

**Target:** 150 liters

**Expected Output:** 3 combinations
- First container
- Second container
- Third container

**Pass Criteria:** Output is exactly 3

---

### Test 6: Two Identical Containers
**Purpose:** Verify distinct containers are counted separately

**Input:**
```
75
75
50
```

**Target:** 150 liters

**Expected Output:** 1 combination
- First 75 + second 75 = 150

**Reasoning:** Only one way to combine these containers to reach 150

**Pass Criteria:** Output is exactly 1

---

### Test 7: Multiple Paths to Same Sum
**Purpose:** Test complex case with many valid combinations

**Input:**
```
50
50
50
25
25
```

**Target:** 100 liters

**Expected Output:** 6 combinations

**Manual Enumeration:**
1. 50₁ + 50₂ = 100
2. 50₁ + 50₃ = 100
3. 50₂ + 50₃ = 100
4. 50₁ + 25₁ + 25₂ = 100
5. 50₂ + 25₁ + 25₂ = 100
6. 50₃ + 25₁ + 25₂ = 100

**Pass Criteria:** Output is exactly 6

---

### Test 8: Empty Input
**Purpose:** Handle edge case of no containers

**Input:** (empty file or no containers)

**Target:** 150 liters

**Expected Output:** 0 combinations

**Pass Criteria:** Output is exactly 0, no errors

---

### Test 9: Single Container Too Small
**Purpose:** Verify rejection when container < target

**Input:**
```
10
```

**Target:** 150 liters

**Expected Output:** 0 combinations

**Pass Criteria:** Output is exactly 0

---

### Test 10: All Containers Must Be Used
**Purpose:** Verify algorithm considers all containers and doesn't stop early

**Input:**
```
50
50
50
```

**Target:** 150 liters

**Expected Output:** 1 combination
- All three containers: 50 + 50 + 50 = 150

**Reasoning:** This tests that the algorithm explores deep enough to use all containers when necessary

**Pass Criteria:** Output is exactly 1

---

### Test 11: Actual Problem Input
**Purpose:** Solve the actual problem

**Input:** Use the provided input.md with 20 containers

**Target:** 150 liters

**Expected Output:** To be verified by alternative implementation

**Test Method:**
1. Run recursive backtracking solution with actual input
2. Run alternative bit-manipulation solution with same input (see implementation plan lines 191-214)
3. Verify both solutions produce identical results
4. Verify output is reasonable:
   - Should be > 0 (at least one combination should exist)
   - Should be << 2^20 (not all subsets will sum to 150)
   - Typical range might be hundreds to thousands
5. Manual spot-check: verify a few combinations by hand if possible

**Pass Criteria:**
- Both implementations produce the same output
- Output is a positive integer
- Output is reasonable (0 < result < 100,000 expected)
- Program completes in reasonable time (< 5 seconds)
- No errors or crashes

**Verification Strategy:**
Since this is an Advent of Code problem, the final verification would be submitting the answer to the AoC website. For our purposes, matching results from two independent implementations provides high confidence in correctness.

---

## Verification Methods

### Method 1: Manual Verification (Small Inputs)
For small test cases (≤5 containers):
1. Manually enumerate all possible combinations
2. Check which ones sum to target
3. Compare with algorithm output

### Method 2: Alternative Implementation
Implement a second version using bit manipulation approach (from implementation plan):
1. Write iterative bit-manipulation solution (see implementation plan lines 191-214)
2. Run both implementations on same input
3. Verify outputs match exactly

**Bit Manipulation Implementation:**
```python
def count_combinations_iterative(containers, target):
    """
    Use bit manipulation to iterate through all 2^n subsets.
    """
    count = 0
    n = len(containers)

    # Iterate through all possible subsets (2^n combinations)
    for mask in range(1 << n):  # 2^n
        subset_sum = 0
        for i in range(n):
            if mask & (1 << i):  # Check if i-th bit is set
                subset_sum += containers[i]

        if subset_sum == target:
            count += 1

    return count
```

This provides independent verification of correctness.

### Method 3: Property-Based Testing
Verify algorithmic properties:
1. **Non-negative output:** Result should always be ≥ 0
2. **Upper bound:** Result ≤ 2^n (can't have more combinations than total subsets)
3. **Deterministic:** Same input always produces same output
4. **Subset verification:** For small n, enumerate all subsets and verify count

**Implementation of Property Tests:**
```python
def test_properties(containers, target, result):
    """Test that result satisfies mathematical properties."""
    # Property 1: Non-negative
    assert result >= 0, f"Result must be non-negative, got {result}"

    # Property 2: Upper bound
    max_combinations = 2 ** len(containers)
    assert result <= max_combinations, f"Result {result} exceeds maximum possible {max_combinations}"

    # Property 3: Deterministic (run multiple times)
    for _ in range(3):
        new_result = count_combinations(containers, target)
        assert new_result == result, "Results should be deterministic"

    return True
```

### Method 4: Boundary Value Analysis
Test boundary conditions:
- Empty container list
- Single container
- All containers identical
- Target = 0
- Target = sum of all containers
- Target > sum of all containers
- Target < smallest container

---

## Performance Testing

### Performance Test 1: Timing for n=20
**Purpose:** Ensure solution runs efficiently for actual input size

**Method:**
1. Measure execution time for actual input (20 containers)
2. Verify completion in reasonable time

**Pass Criteria:** Completes in < 5 seconds

### Performance Test 2: Scaling Test
**Purpose:** Understand performance characteristics

**Method:**
1. Test with n = 10, 15, 20 containers
2. Measure execution time for each
3. Verify roughly exponential growth (expected for O(2^n))

**Expected Times:**
- n=10: < 0.01 seconds
- n=15: < 0.1 seconds
- n=20: < 2 seconds

---

## Integration Testing

### Test: Full Pipeline
**Purpose:** Verify entire solution from input to output

**Steps:**
1. Create input file with test data
2. Run `python solution.py`
3. Capture output
4. Verify output format (single integer)
5. Verify output value is correct

**Pass Criteria:** All steps complete successfully

---

## Regression Testing

### Test: Consistency Check
**Purpose:** Ensure solution remains consistent across runs

**Method:**
1. Run solution multiple times with same input
2. Verify output is identical each time

**Pass Criteria:** All runs produce same output

---

## Testing Execution Order

1. **Start with simple cases:** Tests 1-5 (validate basic correctness)
2. **Edge cases:** Tests 6-10 (handle boundary conditions and special cases)
3. **Alternative implementation:** Implement bit manipulation version for cross-validation
4. **Actual input:** Test 11 (solve the real problem using both implementations)
5. **Property-based tests:** Verify mathematical properties hold
6. **Performance testing:** Verify efficiency
7. **Regression testing:** Ensure consistency

---

## Debugging Strategy

If tests fail:

1. **Wrong count on example:**
   - Add print statements to show all found combinations
   - Manually verify each combination sums to target
   - Check for duplicates or missing combinations

2. **Performance issues:**
   - Profile the code to find bottlenecks
   - Consider memoization if necessary
   - Verify input size is as expected

3. **Parsing errors:**
   - Print parsed container list
   - Verify against input file
   - Check for whitespace or formatting issues

---

## Success Criteria

The solution is considered correct and complete when:

1. ✅ All basic test cases (1-10) pass
2. ✅ Actual input (Test 11) produces valid output
3. ✅ Both implementations (recursive and iterative) produce identical results
4. ✅ Property-based tests pass (non-negative, upper bound, deterministic)
5. ✅ Performance is acceptable (< 5 seconds)
6. ✅ No errors or exceptions during execution
7. ✅ Output format is correct (single integer)

---

## Quick Validation Script

Create a separate `test_solution.py` file for automated testing:

```python
from solution import count_combinations

def test_example():
    """Test the example from problem statement."""
    containers = [20, 15, 10, 5, 5]
    result = count_combinations(containers, 25)
    assert result == 4, f"Expected 4, got {result}"
    print("✓ Test 1 passed: Example case")

def test_single_match():
    """Test single container exact match."""
    containers = [150]
    result = count_combinations(containers, 150)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test 2 passed: Single container match")

def test_no_solution():
    """Test case with no valid combinations."""
    containers = [10, 20, 30]
    result = count_combinations(containers, 150)
    assert result == 0, f"Expected 0, got {result}"
    print("✓ Test 3 passed: No solution")

def test_two_identical():
    """Test with two identical containers."""
    containers = [75, 75, 50]
    result = count_combinations(containers, 150)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test 6 passed: Two identical containers")

def test_multiple_paths():
    """Test multiple valid combinations."""
    containers = [50, 50, 50, 25, 25]
    result = count_combinations(containers, 100)
    assert result == 6, f"Expected 6, got {result}"
    print("✓ Test 7 passed: Multiple paths")

def test_all_containers_used():
    """Test that all containers can be used."""
    containers = [50, 50, 50]
    result = count_combinations(containers, 150)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test 10 passed: All containers used")

def test_upper_bound_property():
    """Test that result doesn't exceed 2^n."""
    containers = [20, 15, 10, 5, 5]
    result = count_combinations(containers, 25)
    max_possible = 2 ** len(containers)
    assert result <= max_possible, f"Result {result} exceeds max {max_possible}"
    print("✓ Property test passed: Upper bound")

# Run all tests
if __name__ == '__main__':
    test_example()
    test_single_match()
    test_no_solution()
    test_two_identical()
    test_multiple_paths()
    test_all_containers_used()
    test_upper_bound_property()
    print("\n✓ All tests passed!")
```

This provides quick automated validation during development.
