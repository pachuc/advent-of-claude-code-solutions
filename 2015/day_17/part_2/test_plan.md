# Testing Plan: Eggnog Container Combinations (Part 2)

## Testing Strategy Overview

The testing approach will verify:
1. **Correctness:** Solution finds the right minimum and counts correctly
2. **Algorithm Logic:** Iterative size-based approach works as expected
3. **Edge Cases:** Boundary conditions are handled properly
4. **Input Handling:** File parsing works correctly

## Test Cases

### Test 1: Example from Problem Statement
**Purpose:** Verify against known example

**Input:**
```
containers = [20, 15, 10, 5, 5]
target = 25
```

**Expected Behavior:**
1. Valid combinations:
   - [20, 5] (size 2) - first 5
   - [20, 5] (size 2) - second 5
   - [15, 10] (size 2)
   - [15, 5, 5] (size 3)
   - [10, 5, 5] (size 3)
2. Minimum size: 2 containers
3. Count at minimum size: 3 combinations

**Expected Output:** `3`

**Verification Method:**
- Create a test input file with these values
- Run solution manually or with test script
- Compare output to expected value

### Test 2: Actual Problem Input
**Purpose:** Solve the actual problem

**Input:** The provided input.md file
- 20 containers: [33, 14, 18, 20, 45, 35, 16, 35, 1, 13, 18, 13, 50, 44, 48, 6, 24, 41, 30, 42]
- Target: 150 liters

**Expected Behavior:**
- Should find minimum number of containers (estimated 4-6 based on average container size)
- Should count all combinations at that minimum size
- Should complete in reasonable time (<1 second)
- Output will be a positive integer representing the count

**Verification Method:**
- Run `python solution.py`
- Verify output is a positive integer
- Use manual verification script (see below) to confirm:
  - No combinations exist at size (minimum - 1)
  - The count at minimum size matches the output
  - Sample combinations at minimum size actually sum to 150
- Document the actual output for future regression testing

### Test 3: Single Container Solution
**Purpose:** Test edge case where one container exactly equals target

**Input:**
```
containers = [150, 50, 30, 20]
target = 150
```

**Expected Behavior:**
- Minimum size: 1 container
- Only one way: [150]

**Expected Output:** `1`

**Verification Method:**
- Algorithm should find solution at k=1
- Only one combination should sum to 150

### Test 4: Multiple Single-Container Solutions
**Purpose:** Test when multiple containers individually equal target

**Input:**
```
containers = [25, 25, 10, 15]
target = 25
```

**Expected Behavior:**
- Minimum size: 1 container
- Two ways: [25] (first one), [25] (second one)

**Expected Output:** `2`

**Verification Method:**
- Verify both individual 25-liter containers are counted separately

### Test 5: No Small Solution (Requires Many Containers)
**Purpose:** Verify algorithm works when minimum size is larger

**Input:**
```
containers = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
target = 5
```

**Expected Behavior:**
- Minimum size: 5 containers
- Multiple ways to select 5 ones from 10 available
- C(10, 5) = 10!/(5!×5!) = 252 ways (binomial coefficient)

**Expected Output:** `252`

**Verification Method:**
- Mathematically verify using combination formula: C(10,5) = 252
- Confirms algorithm doesn't stop too early
- All combinations of 5 containers from 10 identical ones are valid

### Test 6: Duplicate Container Values
**Purpose:** Verify algorithm treats duplicate values as separate containers

**Input:**
```
containers = [10, 10, 5, 5]
target = 15
```

**Expected Behavior:**
- Minimum size: 2 containers
- Valid combinations:
  - [10, 5] (first 10, first 5)
  - [10, 5] (first 10, second 5)
  - [10, 5] (second 10, first 5)
  - [10, 5] (second 10, second 5)
- Count: 4 ways

**Expected Output:** `4`

**Verification Method:**
- Ensures containers are treated by position, not value
- Each container is unique even with same capacity

### Test 7: All Containers Sum to Target
**Purpose:** Verify algorithm finds correct minimum even when all containers can be used

**Input:**
```
containers = [50, 30, 20, 10]
target = 110
```

**Expected Behavior:**
- Algorithm checks sizes in order: 1, 2, 3, 4
- Size 1: No single container = 110
- Size 2: Check all pairs (none sum to 110)
- Size 3: Check all triples (e.g., [50, 30, 20] = 100, [50, 30, 10] = 90, etc.)
- Size 4: [50, 30, 20, 10] = 110 ✓
- Minimum size is 4, count is 1

**Expected Output:** `1`

**Verification Method:**
- Verify the algorithm tries smaller sizes first and finds no valid combinations
- Confirms it correctly identifies size 4 as minimum
- Only counts the single valid combination using all containers

## Testing Methodology

### Manual Testing Steps

1. **Create Test Input Files:**
   - Create separate test input files for each test case
   - Name them: `test_input_1.txt`, `test_input_2.txt`, etc.

2. **Modify Solution for Testing:**
   - Temporarily modify `main()` to accept filename parameter
   - Or create a separate test harness script

3. **Run Each Test:**
   ```bash
   python solution.py  # for actual problem
   ```

4. **Verify Output:**
   - Compare output to expected value
   - Check for exact match (single integer)

### Automated Testing Approach

Create a simple test script `test_solution.py`:

```python
from solution import find_minimum_container_ways

def test_example():
    containers = [20, 15, 10, 5, 5]
    result = find_minimum_container_ways(containers, 25)
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Test 1 passed: Example case")

def test_single_container():
    containers = [150, 50, 30, 20]
    result = find_minimum_container_ways(containers, 150)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test 3 passed: Single container")

def test_multiple_singles():
    containers = [25, 25, 10, 15]
    result = find_minimum_container_ways(containers, 25)
    assert result == 2, f"Expected 2, got {result}"
    print("✓ Test 4 passed: Multiple single containers")

def test_many_containers():
    containers = [1] * 10
    result = find_minimum_container_ways(containers, 5)
    assert result == 252, f"Expected 252, got {result}"
    print("✓ Test 5 passed: Many containers")

def test_duplicates():
    containers = [10, 10, 5, 5]
    result = find_minimum_container_ways(containers, 15)
    assert result == 4, f"Expected 4, got {result}"
    print("✓ Test 6 passed: Duplicate values")

def test_all_containers():
    containers = [50, 30, 20, 10]
    result = find_minimum_container_ways(containers, 110)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test 7 passed: All containers needed")

if __name__ == "__main__":
    test_example()
    test_single_container()
    test_multiple_singles()
    test_many_containers()
    test_duplicates()
    test_all_containers()
    print("\n✓ All tests passed!")
```

### Manual Verification for Actual Input

For the actual problem input, perform spot checks:

1. **Run the solution:**
   ```bash
   python solution.py
   ```

2. **Note the output** (e.g., suppose output is 4 and count is 10)

3. **Manual verification:**
   - Try to find a few combinations of 4 containers that sum to 150
   - Verify they exist and sum correctly
   - Check that no combination of 3 containers sums to 150

4. **Sample verification code:**
   ```python
   from itertools import combinations

   containers = [33, 14, 18, 20, 45, 35, 16, 35, 1, 13,
                 18, 13, 50, 44, 48, 6, 24, 41, 30, 42]

   # First, determine the minimum size by running the solution
   # Suppose the solution output indicates minimum size is 4 with count X

   min_size = 4  # Replace with actual minimum from solution output

   # CRITICAL: Verify no solution exists at size (min_size - 1)
   count_smaller = sum(1 for c in combinations(containers, min_size - 1)
                       if sum(c) == 150)
   print(f"Size {min_size - 1} combinations: {count_smaller}")  # Should be 0

   # Count solutions at minimum size
   count_min = sum(1 for c in combinations(containers, min_size)
                   if sum(c) == 150)
   print(f"Size {min_size} combinations: {count_min}")  # Should match output

   # Show a few examples to verify correctness
   examples = [c for c in combinations(containers, min_size)
               if sum(c) == 150][:3]
   for ex in examples:
       print(f"Example: {ex} = {sum(ex)}")
   ```

## Edge Cases Checklist

- [x] Single container equals target
- [x] Multiple containers individually equal target
- [x] Duplicate container values (treated as separate)
- [x] Minimum requires many containers
- [x] Large input size (20 containers)
- [x] No solution exists (returns 0)
- [x] All containers sum to target

## Performance Testing

**Test:** Measure runtime for actual input
```python
import time
from solution import find_minimum_container_ways, parse_input

start = time.time()
containers = parse_input('input.md')
result = find_minimum_container_ways(containers, 150)
elapsed = time.time() - start
print(f"Result: {result}, Time: {elapsed:.3f}s")
```

**Expected:** < 1 second for 20 containers (likely < 100ms)

**Note:** Can be integrated into automated test script if desired, but not critical for correctness

## Acceptance Criteria

The solution is considered correct if:
1. ✓ Passes all test cases with expected outputs
2. ✓ Completes actual problem input in < 1 second
3. ✓ Output is a single integer with no formatting
4. ✓ Manual spot-check confirms valid combinations at minimum size
5. ✓ No valid combinations exist at smaller sizes than the found minimum

## Final Validation

Before submitting the solution:
1. Run solution on actual input: `python solution.py`
2. Capture the output number
3. Run manual verification script to confirm:
   - No solutions exist at smaller size
   - Count at minimum size matches output
   - A few sample combinations sum correctly to 150
4. Verify output format (single integer, no extra text)
