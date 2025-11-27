# Test Plan: Fuel Requirement Calculator

## Overview
This test plan outlines the strategy for verifying the correctness of the fuel requirement calculator solution.

## Testing Strategy

### 1. Unit Tests for Fuel Calculation Formula

#### 1.1 Verify Against Provided Examples
The problem statement provides 4 test cases. These are the most critical tests:

| Mass   | Expected Fuel | Calculation              |
|--------|---------------|--------------------------|
| 12     | 2             | floor(12/3) - 2 = 4 - 2  |
| 14     | 2             | floor(14/3) - 2 = 4 - 2  |
| 1969   | 654           | floor(1969/3) - 2 = 656 - 2 |
| 100756 | 33583         | floor(100756/3) - 2 = 33585 - 2 |

**Test code:**
```python
def test_provided_examples():
    assert calculate_fuel(12) == 2
    assert calculate_fuel(14) == 2
    assert calculate_fuel(1969) == 654
    assert calculate_fuel(100756) == 33583
```

#### 1.2 Edge Cases for Fuel Formula

**Boundary values around floor division behavior:**
- Mass = 9 → fuel = 9 // 3 - 2 = 3 - 2 = 1 (smallest mass yielding positive fuel)
- Mass = 8 → fuel = 8 // 3 - 2 = 2 - 2 = 0 (yields zero fuel)
- Mass = 6 → fuel = 6 // 3 - 2 = 2 - 2 = 0 (exactly divisible by 3)
- Mass = 3 → fuel = 3 // 3 - 2 = 1 - 2 = -1 (negative fuel - theoretical edge case)

**Test code:**
```python
def test_edge_cases():
    assert calculate_fuel(9) == 1
    assert calculate_fuel(8) == 0
    assert calculate_fuel(6) == 0
    assert calculate_fuel(3) == -1  # NOT clamped in Part 1
```

**Note:** The actual input contains masses ranging from ~50,000 to ~150,000, so negative/zero fuel is not a concern. Per the problem statement, we do NOT clamp negative values to zero for Part 1 - the formula is applied exactly as given.

#### 1.3 Floor Division Verification
Ensure the implementation correctly floors the division:
- Mass = 10 → 10 // 3 = 3 (not 3.33), fuel = 3 - 2 = 1
- Mass = 11 → 11 // 3 = 3 (not 3.67), fuel = 3 - 2 = 1
- Mass = 13 → 13 // 3 = 4 (not 4.33), fuel = 4 - 2 = 2

```python
def test_floor_division():
    assert calculate_fuel(10) == 1
    assert calculate_fuel(11) == 1
    assert calculate_fuel(13) == 2
```

### 2. Integration Tests

#### 2.1 Sum of Multiple Modules
Test that summing works correctly:

```python
def test_sum_of_examples():
    masses = [12, 14, 1969, 100756]
    expected = 2 + 2 + 654 + 33583  # = 34241
    assert calculate_total_fuel(masses) == 34241
```

#### 2.2 Empty Input
Verify handling of empty input (edge case):
```python
def test_empty_input():
    assert calculate_total_fuel([]) == 0
```

#### 2.3 Single Module
```python
def test_single_module():
    assert calculate_total_fuel([12]) == 2
```

### 3. Input Parsing Tests

#### 3.1 Basic Parsing
Verify that input file is correctly parsed:
- Count of masses should be 100
- All values should be positive integers
- First value should be 80891
- Last value should be 125521

```python
def test_input_parsing():
    masses = read_masses('input.md')
    assert len(masses) == 100
    assert masses[0] == 80891
    assert masses[-1] == 125521
    assert all(isinstance(m, int) and m > 0 for m in masses)
```

#### 3.2 Handling Trailing Newlines
The input file may have a trailing newline. Ensure this doesn't create an empty/invalid entry. The `line.strip()` check in the implementation handles this.

### 4. Validation of Final Answer

#### 4.1 Sanity Check on Result Range
Given:
- 100 modules
- Masses range from ~50,000 to ~150,000
- Fuel ≈ mass / 3 - 2

Expected total fuel range:
- Minimum estimate: 100 × (50,000 / 3 - 2) ≈ 1,666,467
- Maximum estimate: 100 × (150,000 / 3 - 2) ≈ 4,999,800

The final answer should be within this range.

```python
def test_answer_in_expected_range():
    masses = read_masses('input.md')
    total = calculate_total_fuel(masses)
    assert 1_600_000 < total < 5_000_000
```

#### 4.2 Manual Spot Check
Calculate fuel for a few specific entries from input and verify:
- Mass 80891: fuel = 80891 // 3 - 2 = 26963 - 2 = 26961
- Mass 109412: fuel = 109412 // 3 - 2 = 36470 - 2 = 36468
- Mass 149508: fuel = 149508 // 3 - 2 = 49836 - 2 = 49834

```python
def test_spot_check_input_values():
    assert calculate_fuel(80891) == 26961    # First input value
    assert calculate_fuel(109412) == 36468   # Second input value
    assert calculate_fuel(149508) == 49834   # Third input value
```

#### 4.3 Independent Cross-Check
To provide an additional verification layer, calculate total using alternative method:

```python
def test_mathematical_consistency():
    """Verify mathematical properties of the solution."""
    masses = read_masses('input.md')

    # Sum of individual fuels using our function
    total_fuel = calculate_total_fuel(masses)

    # Alternative calculation: sum each fuel individually using inline formula
    alternative_sum = 0
    for mass in masses:
        alternative_sum += mass // 3 - 2

    assert total_fuel == alternative_sum
```

### 5. Test Execution Plan

#### Step 1: Run Unit Tests (No File Dependencies)
These tests verify the core calculation logic without requiring any input files:
```python
def run_unit_tests():
    test_provided_examples()
    test_edge_cases()
    test_floor_division()
    test_sum_of_examples()
    test_empty_input()
    test_single_module()
    test_spot_check_input_values()
    print("All unit tests passed!")
```

#### Step 2: Run Integration Tests (With Input File)
These tests verify the solution works with the actual input:
```python
def run_integration_tests():
    test_input_parsing()
    test_answer_in_expected_range()
    test_mathematical_consistency()
    print("All integration tests passed!")
```

#### Step 3: Run on Full Input
Execute the solution on `input.md` and obtain the result.

#### Step 4: Sanity Check Result
- Verify result is a positive integer
- Verify result falls within expected range (1.6M - 5M)
- Verify no runtime errors occurred

### 6. Potential Issues to Watch For

1. **Integer Division**: Make sure using `//` not `/` for floor division
2. **Off-by-one errors**: Double-check the -2 subtraction
3. **Input parsing**: Ensure all 100 values are read correctly
4. **Data types**: Ensure we're working with integers, not strings
5. **Empty lines**: Ensure empty/blank lines don't cause issues
6. **Negative fuel (Part 1)**: We do NOT clamp to zero - formula applied exactly as given

### 7. Complete Test File Structure

```python
# test_solution.py

from solution import calculate_fuel, calculate_total_fuel, read_masses

# ============ Unit Tests (No File Dependencies) ============

def test_provided_examples():
    """Test against the 4 examples from problem statement."""
    assert calculate_fuel(12) == 2
    assert calculate_fuel(14) == 2
    assert calculate_fuel(1969) == 654
    assert calculate_fuel(100756) == 33583

def test_edge_cases():
    """Test boundary values for the formula."""
    assert calculate_fuel(9) == 1   # smallest positive fuel
    assert calculate_fuel(8) == 0   # zero fuel
    assert calculate_fuel(6) == 0   # exactly divisible by 3
    assert calculate_fuel(3) == -1  # negative fuel (NOT clamped in Part 1)

def test_floor_division():
    """Ensure floor division behavior is correct."""
    assert calculate_fuel(10) == 1
    assert calculate_fuel(11) == 1
    assert calculate_fuel(13) == 2

def test_sum_of_examples():
    """Test summing functionality."""
    total = calculate_total_fuel([12, 14, 1969, 100756])
    assert total == 34241

def test_empty_input():
    """Empty list should return 0."""
    assert calculate_total_fuel([]) == 0

def test_single_module():
    """Single module should return its fuel value."""
    assert calculate_total_fuel([12]) == 2

def test_spot_check_input_values():
    """Verify calculations for specific input file values."""
    assert calculate_fuel(80891) == 26961
    assert calculate_fuel(109412) == 36468
    assert calculate_fuel(149508) == 49834

# ============ Integration Tests (With File Dependencies) ============

def test_input_count():
    """Verify we read the correct number of masses."""
    masses = read_masses('input.md')
    assert len(masses) == 100

def test_input_boundaries():
    """Verify first and last values are read correctly."""
    masses = read_masses('input.md')
    assert masses[0] == 80891
    assert masses[-1] == 125521

def test_answer_sanity():
    """Verify answer is in reasonable range."""
    masses = read_masses('input.md')
    total = calculate_total_fuel(masses)
    assert 1_600_000 < total < 5_000_000

def test_mathematical_consistency():
    """Verify sum is calculated correctly using alternative method."""
    masses = read_masses('input.md')
    total_fuel = calculate_total_fuel(masses)
    alternative_sum = sum(mass // 3 - 2 for mass in masses)
    assert total_fuel == alternative_sum

# ============ Test Runner ============

if __name__ == '__main__':
    # Unit tests (no file dependencies)
    print("Running unit tests...")
    test_provided_examples()
    test_edge_cases()
    test_floor_division()
    test_sum_of_examples()
    test_empty_input()
    test_single_module()
    test_spot_check_input_values()
    print("All unit tests passed!")

    # Integration tests (with input file)
    print("\nRunning integration tests...")
    test_input_count()
    test_input_boundaries()
    test_answer_sanity()
    test_mathematical_consistency()
    print("All integration tests passed!")

    print("\nAll tests passed!")
```

## Success Criteria

The solution is considered correct when:
1. All 4 provided examples produce the expected output
2. The sum of examples equals 34241
3. Input parsing reads exactly 100 masses
4. First and last values match expected (80891, 125521)
5. Final answer is within expected range (1.6M - 5M)
6. Mathematical consistency check passes
7. No runtime errors occur

## Test Isolation Note

The test plan separates tests into two categories:
1. **Unit tests** - Test core logic without file dependencies (can run anywhere, test the algorithm)
2. **Integration tests** - Test with actual input file (require `input.md` to exist, test the full solution)

This separation allows for faster feedback during development and ensures the core algorithm is correct independent of file I/O. Unit tests can be run immediately to validate the formula implementation before testing with the actual input.

## Race Conditions and Concurrency

This problem has no concurrency requirements - all operations are sequential and deterministic. No race conditions are possible since:
- File reading is a single operation
- All calculations are pure functions with no side effects
- No shared state between calculations
- No parallel processing required or implemented

## Notes on Part 1 vs Part 2 Differences

This test plan is specifically for **Part 1** of the problem, which uses the simple formula `mass // 3 - 2` applied once per module. Key characteristics:
- Formula applied exactly once per module
- Negative results are NOT clamped to zero
- No recursive fuel calculation for the fuel itself

If Part 2 requires recursive fuel calculation (fuel for the fuel), the tests would need to be adjusted accordingly.
