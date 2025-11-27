# Test Plan: Fuel Requirement Calculator (Part 2 - Recursive Fuel)

## Overview

This test plan ensures the Part 2 solution correctly calculates total fuel requirements including the recursive fuel-for-fuel calculation.

## Test Strategy

Since this is a script solution (not production code), we focus on:
1. Verifying against provided examples from the problem statement
2. Testing edge cases that could cause incorrect results
3. Ensuring the result is consistent with Part 1 (i.e., greater than Part 1 answer)
4. Manual spot-checks for sample input values

## Test Categories

### Category 1: Provided Examples (Critical)

These are the most critical tests as they come directly from the problem statement.

#### Test 1.1: Mass of 14
- **Input**: 14
- **Expected Output**: 2
- **Calculation**:
  - Fuel: 14 // 3 - 2 = 4 - 2 = 2
  - Fuel for 2: 2 // 3 - 2 = 0 - 2 = -2 (negative, stop)
  - Total: 2

#### Test 1.2: Mass of 1969
- **Input**: 1969
- **Expected Output**: 966
- **Calculation**:
  | Step | Input Mass | Fuel Calculated |
  |------|------------|-----------------|
  | 1    | 1969       | 654             |
  | 2    | 654        | 216             |
  | 3    | 216        | 70              |
  | 4    | 70         | 21              |
  | 5    | 21         | 5               |
  | 6    | 5          | -1 (stop)       |
  - Total: 654 + 216 + 70 + 21 + 5 = **966**

#### Test 1.3: Mass of 100756
- **Input**: 100756
- **Expected Output**: 50346
- **Calculation**:
  | Step | Input Mass | Fuel Calculated |
  |------|------------|-----------------|
  | 1    | 100756     | 33583           |
  | 2    | 33583      | 11192           |
  | 3    | 11192      | 3728            |
  | 4    | 3728       | 1240            |
  | 5    | 1240       | 411             |
  | 6    | 411        | 135             |
  | 7    | 135        | 43              |
  | 8    | 43         | 12              |
  | 9    | 12         | 2               |
  | 10   | 2          | -2 (stop)       |
  - Total: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = **50346**

### Category 2: Edge Cases

#### Test 2.1: Mass of 0 (Extreme Edge Case)
- **Mass 0**: 0 // 3 - 2 = -2 → **Expected: 0**
- This tests that the algorithm handles zero mass gracefully

#### Test 2.2: Very Small Masses (Negative Initial Fuel)
- **Mass 1**: 1 // 3 - 2 = -2 → **Expected: 0**
- **Mass 2**: 2 // 3 - 2 = -2 → **Expected: 0**
- **Mass 5**: 5 // 3 - 2 = -1 → **Expected: 0**

#### Test 2.3: Boundary Case - Zero Initial Fuel
- **Mass 6**: 6 // 3 - 2 = 0 → **Expected: 0**
- **Mass 7**: 7 // 3 - 2 = 0 → **Expected: 0**
- **Mass 8**: 8 // 3 - 2 = 0 → **Expected: 0**

#### Test 2.4: Boundary Case - Just Positive Initial Fuel
- **Mass 9**: 9 // 3 - 2 = 1, then 1 // 3 - 2 = -2 (stop) → **Expected: 1**
- **Mass 10**: 10 // 3 - 2 = 1 → **Expected: 1**
- **Mass 11**: 11 // 3 - 2 = 1 → **Expected: 1**

#### Test 2.5: Part 1 Example Mass
- **Mass 12**: 12 // 3 - 2 = 2, then 2 // 3 - 2 = -2 (stop) → **Expected: 2**

#### Test 2.6: Masses Where Part 2 = Part 1
For masses where initial fuel is in [1, 8], the fuel-for-fuel calculation yields ≤ 0, so Part 2 = Part 1:
- Mass 9-11: fuel = 1, fuel-for-fuel = -2 → Part 2 = 1 = Part 1
- Mass 12-14: fuel = 2, fuel-for-fuel = -2 → Part 2 = 2 = Part 1
- Mass 27-29: fuel = 7, fuel-for-fuel = 0 → Part 2 = 7 = Part 1
- Mass 30-32: fuel = 8, fuel-for-fuel = 0 → Part 2 = 8 = Part 1

### Category 3: Base Function Verification

Verify the `calculate_fuel` function from Part 1 works correctly:

| Mass   | Expected Fuel |
|--------|---------------|
| 12     | 2             |
| 14     | 2             |
| 1969   | 654           |
| 100756 | 33583         |

### Category 4: Consistency and Sanity Checks

#### Test 4.1: Part 2 ≥ Part 1 (Always True)
- For any mass M: `calculate_recursive_fuel(M) >= calculate_fuel(M)` when Part 1 fuel > 0
- For any mass M: `calculate_recursive_fuel(M) >= 0` always

#### Test 4.2: Part 2 > Part 1 Threshold
The threshold where Part 2 starts exceeding Part 1 is when the initial fuel itself requires positive fuel:
- Initial fuel of 9 → `9 // 3 - 2 = 1` (positive fuel-for-fuel)
- So when `calculate_fuel(M) >= 9`, Part 2 > Part 1

| Initial Fuel | Fuel-for-Fuel | Part 2 vs Part 1 |
|--------------|---------------|------------------|
| ≤ 0          | N/A           | Both = 0         |
| 1-8          | ≤ 0           | Equal            |
| ≥ 9          | ≥ 1           | Part 2 > Part 1  |

#### Test 4.3: Final Answer Bounds
- **Lower bound**: Must be > Part 1 answer (3,267,638)
- **Upper bound sanity check**: Should be < 2 × Part 1 answer (fuel-for-fuel won't double the total)
- **Expected range**: Approximately 1.4x to 1.6x Part 1 answer

### Category 5: Spot Check with Manual Calculation

#### Test 5.1: First Input Mass (80891)
Manual calculation:
```
80891 // 3 - 2 = 26961
26961 // 3 - 2 = 8985
8985 // 3 - 2 = 2993
2993 // 3 - 2 = 995
995 // 3 - 2 = 329
329 // 3 - 2 = 107
107 // 3 - 2 = 33
33 // 3 - 2 = 9
9 // 3 - 2 = 1
1 // 3 - 2 = -2 (stop)

Total: 26961 + 8985 + 2993 + 995 + 329 + 107 + 33 + 9 + 1 = 40413
```
**Expected Output for mass 80891: 40413**

## Test Implementation

### Test Script: `test_solution.py`

```python
def test_calculate_fuel():
    """Test base fuel calculation (from Part 1)."""
    from solution import calculate_fuel

    assert calculate_fuel(12) == 2
    assert calculate_fuel(14) == 2
    assert calculate_fuel(1969) == 654
    assert calculate_fuel(100756) == 33583
    print("  calculate_fuel tests passed")


def test_provided_examples():
    """Test recursive fuel calculation with provided examples."""
    from solution import calculate_recursive_fuel

    # Example 1: Mass of 14
    assert calculate_recursive_fuel(14) == 2, f"Expected 2, got {calculate_recursive_fuel(14)}"

    # Example 2: Mass of 1969
    assert calculate_recursive_fuel(1969) == 966, f"Expected 966, got {calculate_recursive_fuel(1969)}"

    # Example 3: Mass of 100756
    assert calculate_recursive_fuel(100756) == 50346, f"Expected 50346, got {calculate_recursive_fuel(100756)}"

    print("  Provided example tests passed")


def test_edge_cases():
    """Test edge cases for small masses."""
    from solution import calculate_recursive_fuel

    # Mass 0 (extreme edge case)
    assert calculate_recursive_fuel(0) == 0, "Mass 0 should produce 0 fuel"

    # Very small masses (negative initial fuel)
    assert calculate_recursive_fuel(1) == 0, "Mass 1 should produce 0 fuel"
    assert calculate_recursive_fuel(2) == 0, "Mass 2 should produce 0 fuel"
    assert calculate_recursive_fuel(5) == 0, "Mass 5 should produce 0 fuel"

    # Boundary: zero initial fuel
    assert calculate_recursive_fuel(6) == 0, "Mass 6 should produce 0 fuel"
    assert calculate_recursive_fuel(7) == 0, "Mass 7 should produce 0 fuel"
    assert calculate_recursive_fuel(8) == 0, "Mass 8 should produce 0 fuel"

    # Boundary: just positive
    assert calculate_recursive_fuel(9) == 1, "Mass 9 should produce 1 fuel"
    assert calculate_recursive_fuel(10) == 1, "Mass 10 should produce 1 fuel"
    assert calculate_recursive_fuel(11) == 1, "Mass 11 should produce 1 fuel"

    # Mass 12 (Part 1 example)
    assert calculate_recursive_fuel(12) == 2, "Mass 12 should produce 2 fuel"

    print("  Edge case tests passed")


def test_part2_geq_part1():
    """Verify Part 2 answer is always >= Part 1 for same mass."""
    from solution import calculate_fuel, calculate_recursive_fuel

    test_masses = [0, 1, 5, 9, 12, 14, 33, 50, 100, 500, 1000, 1969, 100756]

    for mass in test_masses:
        part1 = calculate_fuel(mass)
        part2 = calculate_recursive_fuel(mass)

        # Part 2 is always >= 0
        assert part2 >= 0, f"Part 2 ({part2}) should be >= 0 for mass {mass}"

        # Part 2 is always >= Part 1 when Part 1 > 0
        if part1 > 0:
            assert part2 >= part1, f"Part 2 ({part2}) should be >= Part 1 ({part1}) for mass {mass}"

        # If Part 1 fuel >= 9, Part 2 must be strictly greater (because fuel-for-fuel is positive)
        if part1 >= 9:
            assert part2 > part1, f"Part 2 ({part2}) should be > Part 1 ({part1}) for mass {mass} (fuel >= 9)"

    print("  Part 2 >= Part 1 tests passed")


def test_spot_check_first_input():
    """Manually verify calculation for first input mass."""
    from solution import calculate_recursive_fuel

    # First mass in input.md is 80891
    result = calculate_recursive_fuel(80891)
    expected = 40413
    assert result == expected, f"Expected {expected} for mass 80891, got {result}"

    print("  Spot check for mass 80891 passed")


def test_full_solution():
    """Test the complete solution against actual input."""
    from solution import read_masses, calculate_total_fuel

    masses = read_masses('input.md')

    # Verify we read 100 masses
    assert len(masses) == 100, f"Expected 100 masses, got {len(masses)}"

    total_fuel = calculate_total_fuel(masses)

    # Must be greater than Part 1 answer
    part1_answer = 3267638
    assert total_fuel > part1_answer, f"Part 2 ({total_fuel}) should be > Part 1 ({part1_answer})"

    # Sanity check: shouldn't be unreasonably large
    assert total_fuel < 2 * part1_answer, f"Part 2 answer seems too large: {total_fuel}"

    print(f"  Full solution test passed")
    print(f"    Part 1 answer: {part1_answer}")
    print(f"    Part 2 answer: {total_fuel}")
    print(f"    Additional fuel: {total_fuel - part1_answer}")
    print(f"    Ratio (Part2/Part1): {total_fuel / part1_answer:.4f}")


def run_all_tests():
    """Run all tests."""
    print("Running tests...\n")
    test_calculate_fuel()
    test_provided_examples()
    test_edge_cases()
    test_part2_geq_part1()
    test_spot_check_first_input()
    test_full_solution()
    print("\n" + "=" * 40)
    print("ALL TESTS PASSED!")
    print("=" * 40)


if __name__ == '__main__':
    run_all_tests()
```

## Verification Process

### Step 1: Run Example Tests
```bash
python -c "from solution import calculate_recursive_fuel; print(calculate_recursive_fuel(14))"  # Should print 2
python -c "from solution import calculate_recursive_fuel; print(calculate_recursive_fuel(1969))"  # Should print 966
python -c "from solution import calculate_recursive_fuel; print(calculate_recursive_fuel(100756))"  # Should print 50346
```

### Step 2: Run Full Test Suite
```bash
python test_solution.py
```

### Step 3: Run Solution
```bash
python solution.py
```

### Step 4: Validate Final Answer
1. Output should be a single positive integer
2. Output must be > 3,267,638 (Part 1 answer)
3. Output should be < 6,535,276 (2x Part 1 as sanity check)

## Potential Issues to Watch For

1. **Off-by-one in loop termination**:
   - Stop when `fuel <= 0`, not just `fuel < 0`
   - Ensure we correctly handle the case where fuel is exactly 0

2. **Integer division correctness**:
   - Python 3's `//` operator handles floor division correctly for positive numbers
   - For negative numbers, Python rounds toward negative infinity, but all our inputs are positive

3. **Empty input handling**:
   - Sum of empty list is 0 (Python handles this correctly)

4. **Large numbers**:
   - Python handles arbitrary precision integers, no overflow concerns

5. **Input parsing**:
   - Ensure blank lines are skipped
   - Ensure whitespace is stripped

## Expected Test Results Summary

| Test                          | Expected Result |
|-------------------------------|-----------------|
| Mass 0                        | 0               |
| Mass 14                       | 2               |
| Mass 1969                     | 966             |
| Mass 100756                   | 50346           |
| Mass 1-8                      | 0               |
| Mass 9                        | 1               |
| Mass 80891 (spot check)       | 40413           |
| Full solution                 | > 3,267,638     |
| Number of input masses        | 100             |

## Cross-Check: Mathematical Relationship

The threshold for Part 2 exceeding Part 1 is based on when fuel-for-fuel becomes positive:

| Condition | Fuel-for-Fuel | Result |
|-----------|---------------|--------|
| `M // 3 - 2 <= 0` | N/A (no initial fuel) | Part 2 = 0 |
| `M // 3 - 2` is 1-8 | ≤ 0 | Part 2 = Part 1 |
| `M // 3 - 2 >= 9` | ≥ 1 | Part 2 > Part 1 |

**Key threshold**: When initial fuel >= 9, additional fuel starts accumulating.
- Fuel of 9 → `9 // 3 - 2 = 1` (first positive fuel-for-fuel)
- Fuel of 8 → `8 // 3 - 2 = 0` (no additional fuel)

This invariant can be used to verify correctness of the implementation.
