# Testing Plan: Spreadsheet Corruption Checksum

## Testing Strategy

Since this is a script to solve a specific problem (not production code), testing will focus on:
1. Verifying correctness with the provided example
2. Testing a few relevant edge cases
3. Validating the actual input produces a reasonable result

## Test Cases

### Test 1: Provided Example (Critical)
**Purpose**: Verify algorithm correctness against known answer

**Input**:
```
5 1 9 5
7 5 3
2 4 6 8
```

**Expected Output**: 18

**Calculation**:
- Row 1: max(5,1,9,5) - min(5,1,9,5) = 9 - 1 = 8
- Row 2: max(7,5,3) - min(7,5,3) = 7 - 3 = 4
- Row 3: max(2,4,6,8) - min(2,4,6,8) = 8 - 2 = 6
- Checksum: 8 + 4 + 6 = 18

**Test Method**:
1. Create test file `test_example.txt` with above input
2. Run solution on test file
3. Verify output equals 18

**Pass Criteria**: Output must be exactly 18

---

### Test 2: Single Row
**Purpose**: Verify handling of minimal valid input

**Input**:
```
10 20 5 15
```

**Expected Output**: 15

**Calculation**:
- Row 1: max(10,20,5,15) - min(10,20,5,15) = 20 - 5 = 15

**Test Method**: Create single-row test file and verify output

**Pass Criteria**: Output equals 15

---

### Test 3: Row with Single Value
**Purpose**: Verify edge case where max = min

**Input**:
```
100
200 50
```

**Expected Output**: 150

**Calculation**:
- Row 1: max(100) - min(100) = 100 - 100 = 0
- Row 2: max(200,50) - min(200,50) = 200 - 50 = 150
- Checksum: 0 + 150 = 150

**Test Method**: Create test file with single-value row

**Pass Criteria**: Output equals 150 (single-value row contributes 0)

---

### Test 4: Row with Identical Values
**Purpose**: Verify handling when all values in a row are the same

**Input**:
```
5 5 5 5
10 20 30
```

**Expected Output**: 20

**Calculation**:
- Row 1: max(5,5,5,5) - min(5,5,5,5) = 5 - 5 = 0
- Row 2: max(10,20,30) - min(10,20,30) = 30 - 10 = 20
- Checksum: 0 + 20 = 20

**Test Method**: Create test file with identical values in a row

**Pass Criteria**: Output equals 20

---

### Test 5: Negative Numbers
**Purpose**: Verify correct handling of negative values

**Input**:
```
-5 10 -20
0 5 -3
```

**Expected Output**: 38

**Calculation**:
- Row 1: max(-5,10,-20) - min(-5,10,-20) = 10 - (-20) = 30
- Row 2: max(0,5,-3) - min(0,5,-3) = 5 - (-3) = 8
- Checksum: 30 + 8 = 38

**Test Method**: Create test file with negative numbers

**Pass Criteria**: Output equals 38

---

### Test 6: Large Numbers
**Purpose**: Verify handling of large integer values

**Input**:
```
1000000 1
```

**Expected Output**: 999999

**Calculation**:
- Row 1: max(1000000,1) - min(1000000,1) = 1000000 - 1 = 999999

**Test Method**: Create test file with large values

**Pass Criteria**: Output equals 999999

---

### Test 7: Actual Input Validation
**Purpose**: Verify solution works on the real input and produces a reasonable result

**Input**: `input.md` (actual problem input)

**Expected Output**: Unknown, but should be:
- A positive integer
- Greater than 0 (since rows have varying values)
- Less than sum of all max values (sanity check)

**Test Method**:
1. Run solution on `input.md`
2. Verify output is a reasonable positive integer
3. Manual spot-check: Calculate first few rows manually and verify they match

**Manual Verification for First Three Rows**:
- Row 1: `179 2358 5197 867 163 4418 3135 5049 187 166 4682 5080 5541 172 4294 1397`
  - Max: 5541, Min: 163, Difference: 5541 - 163 = 5378
- Row 2: `2637 136 3222 591 2593 1982 4506 195 4396 3741 2373 157 4533 3864 4159 142`
  - Max: 4533, Min: 136, Difference: 4533 - 136 = 4397
- Row 3: `1049 1163 1128 193 1008 142 169 168 165 310 1054 104 1100 761 406 173`
  - Max: 1163, Min: 104, Difference: 1163 - 104 = 1059

**Verification Strategy**:
- Add debug output to print each row's max, min, and difference
- Compare first 3 rows against manual calculations above
- Verify they match exactly before trusting final checksum

**Pass Criteria**:
- Program executes without errors
- Output is a positive integer
- First three row differences match manual calculations: 5378, 4397, 1059

---

### Test 8: Empty Lines Handling
**Purpose**: Verify robustness against empty lines in input

**Input**:
```
5 10 15

20 25 30

```

**Expected Output**: 20

**Calculation**:
- Row 1: 15 - 5 = 10
- Row 2: 30 - 20 = 10
- Checksum: 10 + 10 = 20

**Note**: If empty lines are properly filtered, they contribute nothing

**Test Method**: Create file with blank lines

**Pass Criteria**: Empty lines are ignored, correct checksum calculated (output = 20)

---

## Testing Execution Plan

### Phase 1: Critical Validation
1. Run Test 1 (provided example) - **MUST PASS**
2. Verify output is exactly 18
3. If this fails, debug immediately before proceeding

### Phase 2: Edge Case Testing
1. Create test files for Tests 2-6 and Test 8
2. Run solution.py on each test file
3. Compare output with expected results
4. Document any failures

### Phase 3: Actual Input Testing
1. Add debug output to solution to print intermediate row calculations
2. Run solution on `input.md`
3. Manually verify first 3 rows match expected calculations (5378, 4397, 1059)
4. Verify final output is reasonable
5. Record the final answer
6. Remove debug output

## Test Implementation Approach

### Option 1: Simple Manual Testing
```bash
# Test the example
python solution.py  # (modify to read test_example.txt)
# Verify output is 18

# Test actual input
python solution.py  # (with input.md)
# Verify reasonable output
```

### Option 2: Quick Test Script
Create `test.py`:
```python
from solution import calculate_checksum
import tempfile
import os

def test_case(input_data, expected, description):
    # Write test data to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(input_data)
        temp_file = f.name

    try:
        result = calculate_checksum(temp_file)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: {description}")
        if result != expected:
            print(f"  Expected: {expected}, Got: {result}")
        return result == expected
    finally:
        os.unlink(temp_file)

# Run all tests
print("Running tests...")
all_pass = True
all_pass &= test_case("5 1 9 5\n7 5 3\n2 4 6 8\n", 18, "Test 1: Provided example")
all_pass &= test_case("10 20 5 15\n", 15, "Test 2: Single row")
all_pass &= test_case("100\n200 50\n", 150, "Test 3: Single value row")
all_pass &= test_case("5 5 5 5\n10 20 30\n", 20, "Test 4: Identical values")
all_pass &= test_case("-5 10 -20\n0 5 -3\n", 38, "Test 5: Negative numbers")
all_pass &= test_case("1000000 1\n", 999999, "Test 6: Large numbers")
all_pass &= test_case("5 10 15\n\n20 25 30\n\n", 20, "Test 8: Empty lines")

print(f"\nAll tests {'PASSED' if all_pass else 'FAILED'}")
```

**Chosen Approach**: Option 2 (automated test script) is recommended
- Minimal effort to implement (template above is complete)
- Provides better verification and catches regressions
- Can be reused if solution needs modification
- Takes seconds to run all tests

## Verification Checklist

- [ ] Solution produces 18 for the provided example
- [ ] All edge case tests pass (Tests 2-6, 8)
- [ ] Solution runs without errors on `input.md`
- [ ] Manual calculation of first 3 rows matches program output (5378, 4397, 1059)
- [ ] Output is a reasonable positive integer
- [ ] Solution handles rows with different lengths
- [ ] Empty lines don't cause errors

## Success Criteria

The solution is correct if:
1. ✓ Provided example returns exactly 18
2. ✓ Actual input produces a positive integer without errors
3. ✓ Manual spot-check of 2-3 rows confirms correct calculation
4. ✓ Code is readable and follows the algorithm specification

## Debugging Strategy (If Tests Fail)

If tests fail:
1. **Wrong answer on example**: Algorithm error - recheck min/max logic
2. **Parsing errors**: Check split() logic and empty line handling
3. **Type errors**: Verify int() conversion on parsed values
4. **Off-by-one in answer**: Check if accidentally including/excluding a row
