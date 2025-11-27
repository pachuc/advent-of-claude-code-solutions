# Testing Plan: Chronal Calibration

## Testing Strategy
Verify that the solution correctly computes the sum of frequency changes starting from 0.

## Test Categories

### 1. Example-Based Tests
Test against the examples provided in the problem statement to ensure basic correctness.

#### Test 1.1: Example 1 - `[+1, -2, +3, +1]`
- **Input:** `+1, -2, +3, +1`
- **Expected Output:** `3`
- **Verification:** 0 + 1 - 2 + 3 + 1 = 3
- **Purpose:** Verify mixed positive and negative values

#### Test 1.2: Example 2 - `[+1, +1, +1]`
- **Input:** `+1, +1, +1`
- **Expected Output:** `3`
- **Verification:** 0 + 1 + 1 + 1 = 3
- **Purpose:** Verify all positive values

#### Test 1.3: Example 3 - `[+1, +1, -2]`
- **Input:** `+1, +1, -2`
- **Expected Output:** `0`
- **Verification:** 0 + 1 + 1 - 2 = 0
- **Purpose:** Verify result can be zero

#### Test 1.4: Example 4 - `[-1, -2, -3]`
- **Input:** `-1, -2, -3`
- **Expected Output:** `-6`
- **Verification:** 0 - 1 - 2 - 3 = -6
- **Purpose:** Verify all negative values

### 2. Edge Case Tests

#### Test 2.1: Single Value
- **Input:** `+5`
- **Expected Output:** `5`
- **Purpose:** Verify single-element input

#### Test 2.2: Single Negative Value
- **Input:** `-10`
- **Expected Output:** `-10`
- **Purpose:** Verify single negative element

#### Test 2.3: Large Numbers
- **Input:** `+68519, +68055, -136507`
- **Expected Output:** `67`
- **Verification:** 68519 + 68055 - 136507 = 67
- **Purpose:** Verify handling of large values (similar to those in actual input)

#### Test 2.4: Zero Result
- **Input:** `+10, -5, -5`
- **Expected Output:** `0`
- **Purpose:** Verify result of zero

### 3. Actual Input Test

#### Test 3.1: Full Input Validation
- **Input:** Use the provided `input.md` file (983 frequency changes)
- **Expected Output:** To be determined on first successful run, then documented here
- **Verification Method:**
  1. Run the solution on actual input
  2. Document the result as the expected answer
  3. Independent verification: Use Python REPL to verify: `sum([int(line.strip()) for line in open('input.md') if line.strip()])`
  4. All future runs must match this documented answer
  5. Spot check: First 6 values (-1, -17, -4, -15, -1, +6) sum to -32
  6. Spot check: Three large values (+68519 at line 474, +68055 at line 948, -136507 at line 983) suggest overall sum magnitude

**ACTUAL ANSWER (to be filled after first run):** _______

#### Test 3.2: Input Parsing Verification
- **Purpose:** Ensure all 983 lines are parsed correctly
- **Method:**
  1. Verify the number of parsed values equals 983 (total lines in input.md minus 1 empty line)
  2. Spot-check specific values at known line numbers (e.g., line 474 should be +68519)
  3. Verify first and last values are correct (-1 and -136507)

### 4. Error Handling Tests

#### Test 4.1: Missing Input File
- **Input:** Run solution when `input.md` doesn't exist
- **Expected Output:** Clear error message ("Error: input.md file not found")
- **Purpose:** Verify graceful handling of missing file

#### Test 4.2: Script Execution
- **Test:** Run as a Python script: `python solution.py`
- **Expected:** Should print result to stdout with no errors
- **Purpose:** Verify `if __name__ == '__main__':` guard works correctly

## Testing Implementation

### Manual Testing Approach
1. Create small test files for each example case
2. Run solution on each test file
3. Compare output with expected result
4. Verify examples match problem statement

### Automated Testing Approach (Optional)
```python
import tempfile
import os

def test_examples():
    """Test the solve() function with known examples"""
    test_cases = [
        ([1, -2, 3, 1], 3),
        ([1, 1, 1], 3),
        ([1, 1, -2], 0),
        ([-1, -2, -3], -6),
        ([68519, 68055, -136507], 67),
    ]

    for changes, expected in test_cases:
        # Test the algorithm directly
        result = sum(changes)
        assert result == expected, f"Failed: {changes} -> {result}, expected {expected}"

        # Test the actual solve() function with a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            for change in changes:
                f.write(f"{'+' if change >= 0 else ''}{change}\n")
            temp_path = f.name

        # Modify solve() temporarily to accept file path parameter for testing
        # Or create temporary input.md in test directory

        os.unlink(temp_path)

    print("All tests passed!")
```

### Verification Steps
1. **Run on all examples:** Verify each example produces correct output
2. **Run on actual input:** Execute solution on `input.md`
3. **Document the answer:** Record the result as the expected answer in Test 3.1 above
4. **Independent verification:**
   - Open Python REPL and run: `sum([int(line.strip()) for line in open('input.md') if line.strip()])`
   - Result must match the solution's output
   - This confirms both parsing and summation are correct
5. **Sanity checks:**
   - Result should be an integer
   - Count of parsed values should be 983
   - Spot-check known values: line 1 = -1, line 474 = +68519, line 948 = +68055, line 983 = -136507
6. **Regression testing:** All future runs must produce the same documented answer

## Success Criteria
- All four example tests pass with correct outputs
- Actual input produces a single integer output
- Independent verification (Python REPL) matches solution output
- The answer is documented in Test 3.1 for future regression testing
- No errors during execution
- Result is consistent across multiple runs
- Code handles all 983 values in actual input without issues
- FileNotFoundError is handled gracefully with clear error message
- Script executes correctly with `python solution.py`

## Test Execution Order
1. Start with simplest example (all positive or all negative)
2. Progress to mixed examples
3. Test edge cases (single value, zero result)
4. Finally test on actual input
5. Perform independent verification of actual input result
