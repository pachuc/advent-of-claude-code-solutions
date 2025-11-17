# Test Plan: Gift Ribbon Calculator

## Updates Based on Critique

This plan has been enhanced based on review feedback:

1. **Dimension order independence test**: Added explicit test (Test 2.1b) to verify sorting optimization
2. **Integrated test execution**: Tests are now built into the solution script, runnable via `python solution.py test`
3. **Clearer verification methods**: Added specific commands (e.g., `wc -l`) for line count verification
4. **Performance verification details**: Added specific examples using `time` command and Python's time module
5. **Streamlined test organization**: Single `run_tests()` function with all critical tests
6. **Better test failure messages**: Assert statements include descriptive error messages

## Testing Strategy

Verify correctness through multiple levels of testing:
1. Unit tests for individual functions
2. Integration tests with example cases
3. Validation with actual input
4. Edge case verification

## Test Cases

### 1. Example Validation Tests

These tests verify the examples provided in the problem statement.

#### Test 1.1: Example 1 - Present 2x3x4
**Input**: `2x3x4`
**Expected calculation**:
- Dimensions: length=2, width=3, height=4
- Face perimeters:
  - 2×(2+3) = 10
  - 2×(3+4) = 14
  - 2×(2+4) = 12
- Smallest perimeter: 10 (wrapping ribbon)
- Volume: 2×3×4 = 24 (bow ribbon)
- Total: 10 + 24 = **34 feet**

**Verification**: `calculate_ribbon_for_present(2, 3, 4)` should return 34

#### Test 1.2: Example 2 - Present 1x1x10
**Input**: `1x1x10`
**Expected calculation**:
- Dimensions: length=1, width=1, height=10
- Face perimeters:
  - 2×(1+1) = 4
  - 2×(1+10) = 22
  - 2×(1+10) = 22
- Smallest perimeter: 4 (wrapping ribbon)
- Volume: 1×1×10 = 10 (bow ribbon)
- Total: 4 + 10 = **14 feet**

**Verification**: `calculate_ribbon_for_present(1, 1, 10)` should return 14

### 2. Edge Case Tests

#### Test 2.1: Cube (all dimensions equal)
**Input**: `5x5x5`
**Expected calculation**:
- All face perimeters are equal: 2×(5+5) = 20
- Smallest perimeter: 20
- Volume: 5×5×5 = 125
- Total: 20 + 125 = **145 feet**

**Purpose**: Verify algorithm works when all perimeters are identical

#### Test 2.1b: Dimension order independence
**Purpose**: Verify that the result is the same regardless of dimension order (validates sorting optimization)
- `calculate_ribbon_for_present(2, 3, 4)` = 34
- `calculate_ribbon_for_present(3, 4, 2)` = 34
- `calculate_ribbon_for_present(4, 2, 3)` = 34
- `calculate_ribbon_for_present(4, 3, 2)` = 34
- `calculate_ribbon_for_present(3, 2, 4)` = 34
- `calculate_ribbon_for_present(2, 4, 3)` = 34

All permutations must return the same value, confirming the sorting approach correctly finds the smallest perimeter.

#### Test 2.2: Flat box (one dimension is 1)
**Input**: `1x10x20`
**Expected calculation**:
- Face perimeters: 2×(1+10)=22, 2×(10+20)=60, 2×(1+20)=42
- Smallest perimeter: 22
- Volume: 1×10×20 = 200
- Total: 22 + 200 = **222 feet**

**Purpose**: Verify handling of very flat boxes

#### Test 2.3: Minimum dimensions (all 1s)
**Input**: `1x1x1`
**Expected calculation**:
- Smallest perimeter: 2×(1+1) = 4
- Volume: 1×1×1 = 1
- Total: 4 + 1 = **5 feet**

**Purpose**: Test minimum possible dimensions

#### Test 2.4: Large dimensions
**Input**: `30x30x30`
**Expected calculation**:
- Smallest perimeter: 2×(30+30) = 120
- Volume: 30×30×30 = 27000
- Total: 120 + 27000 = **27120 feet**

**Purpose**: Verify no integer overflow with large dimensions

#### Test 2.5: Two dimensions equal, one different
**Input**: `5x5x10`
**Expected calculation**:
- Face perimeters: 2×(5+5)=20, 2×(5+10)=30, 2×(5+10)=30
- Smallest perimeter: 20
- Volume: 5×5×10 = 250
- Total: 20 + 250 = **270 feet**

**Purpose**: Verify correct selection when two perimeters are equal

### 3. Parsing Tests

#### Test 3.1: Standard format
**Input string**: `"29x13x26"`
**Expected output**: `(29, 13, 26)`

#### Test 3.2: With whitespace
**Input string**: `"29x13x26\n"`
**Expected output**: `(29, 13, 26)`

**Purpose**: Verify whitespace handling (trailing newlines, spaces)

#### Test 3.3: Single digit dimensions
**Input string**: `"1x2x3"`
**Expected output**: `(1, 2, 3)`

#### Test 3.4: Two digit and three digit dimensions
**Input string**: `"5x15x125"`
**Expected output**: `(5, 15, 125)` (if applicable)

### 4. Integration Tests

#### Test 4.1: Multiple presents
**Input file content**:
```
2x3x4
1x1x10
```
**Expected total**: 34 + 14 = **48 feet**

**Purpose**: Verify accumulation across multiple presents

#### Test 4.2: Empty line handling
**Input file content**:
```
2x3x4

1x1x10
```
**Expected total**: 34 + 14 = **48 feet**

**Purpose**: Verify empty lines don't cause errors

### 5. Actual Input Validation

#### Test 5.1: First few lines manual verification
Manually verify calculation for first 3-5 presents from actual input:
- Line 1: `29x13x26` → wrapping: 2×(13+26)=78, bow: 29×13×26=9802, total: 9880
- Line 2: `11x11x14` → wrapping: 2×(11+11)=44, bow: 11×11×14=1694, total: 1738
- Line 3: `27x2x5` → wrapping: 2×(2+5)=14, bow: 27×2×5=270, total: 284
- Expected sum of first 3: 9880 + 1738 + 284 = **11902**

**Verification method**: Create a test file with just these 3 lines and verify output

#### Test 5.2: Full input run
- Run solution on complete `input.md` file
- Verify program completes without errors
- Record the output for final submission
- Verify output is a reasonable positive integer

#### Test 5.3: Line count verification
**Expected**: 1000 presents processed
**Verification method**:
```bash
wc -l input.md  # Should show 1000 (or 1001 if there's a trailing newline)
```
Alternatively, add a counter in the code during testing to verify 1000 presents are processed.

## Testing Implementation

### Integrated Test Function

The tests are integrated directly into the solution script via a `run_tests()` function:

```python
def run_tests():
    """Run basic tests to verify correctness."""
    # Test example 1: 2x3x4
    assert calculate_ribbon_for_present(2, 3, 4) == 34, "Example 1 failed"

    # Test example 2: 1x1x10
    assert calculate_ribbon_for_present(1, 1, 10) == 14, "Example 2 failed"

    # Test dimension order independence (validates sorting optimization)
    assert calculate_ribbon_for_present(2, 3, 4) == calculate_ribbon_for_present(3, 4, 2), "Order independence failed"
    assert calculate_ribbon_for_present(2, 3, 4) == calculate_ribbon_for_present(4, 2, 3), "Order independence failed"

    # Test cube (all dimensions equal)
    assert calculate_ribbon_for_present(5, 5, 5) == 145, "Cube test failed"

    # Test flat box
    assert calculate_ribbon_for_present(1, 10, 20) == 222, "Flat box failed"

    # Test minimum dimensions
    assert calculate_ribbon_for_present(1, 1, 1) == 5, "Minimum dimensions failed"

    # Test parsing
    assert parse_line("29x13x26") == (29, 13, 26), "Parsing failed"
    assert parse_line("1x2x3\n") == (1, 2, 3), "Parsing with newline failed"

    # Test first three lines of actual input
    result = 0
    result += calculate_ribbon_for_present(29, 13, 26)  # 9880
    result += calculate_ribbon_for_present(11, 11, 14)  # 1738
    result += calculate_ribbon_for_present(27, 2, 5)    # 284
    assert result == 11902, f"First 3 lines failed: expected 11902, got {result}"

    print("All tests passed!")
```

### How to Run Tests

Execute tests by running:
```bash
python solution.py test
```

This will run all tests and print "All tests passed!" if successful, or raise an assertion error with details if any test fails.

## Manual Verification Steps

1. **Run integrated tests**: `python solution.py test`
   - Verify both examples return correct values
   - Verify edge cases pass
   - Verify parsing works correctly
   - Verify first few lines of actual input
   - Confirm "All tests passed!" message appears

2. **Verify line count**: `wc -l input.md` should show 1000 lines

3. **Run full solution**: `python solution.py`
   - Execute on complete input file
   - Verify output is a single integer
   - Sanity check: output should be > 0 and less than ~10 million (rough upper bound)

4. **Manual spot checks** (optional):
   - Pick a random line from input
   - Manually calculate expected ribbon
   - Add temporary print statement to verify calculation matches

## Expected Results

- All unit tests should pass
- Example tests should return 34 and 14 respectively
- First 3 lines should total to 11902
- Full input should return a positive integer
- No errors or exceptions during execution

## Debugging Strategy

If tests fail:
1. **Check parsing**: Print parsed dimensions to verify correct extraction
2. **Check calculation**: Print intermediate values (perimeters, volume)
3. **Check accumulation**: Print running total to see where it diverges
4. **Verify algorithm**: Double-check sorting optimization gives smallest perimeter

## Performance Verification

For this problem size (1000 presents), performance is not a concern, but can be verified:

### Using time command:
```bash
time python solution.py
```
Expected: < 100ms total execution time

### Using Python's time module (optional):
Add timing to main function:
```python
import time
start = time.time()
result = calculate_total_ribbon(input_file)
end = time.time()
print(f"Result: {result}")
print(f"Time: {(end - start) * 1000:.2f}ms")
```

### Memory verification:
- Memory usage should remain constant (O(1) space)
- No large data structures created
- Single pass through input confirms efficient processing
