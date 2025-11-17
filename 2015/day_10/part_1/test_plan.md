# Testing Plan: Look-and-Say Sequence

## Testing Strategy Overview

We need to verify:
1. The look-and-say transformation logic is correct
2. The iteration mechanism works properly
3. The final result length is accurate
4. The solution handles the specific input correctly

## Test Categories

### 1. Unit Tests for Core Transformation Function

**Test Case 1.1: Single digit**
- Input: `"1"`
- Expected Output: `"11"`
- Rationale: Simplest case - one occurrence of digit 1

**Test Case 1.2: Two same digits**
- Input: `"11"`
- Expected Output: `"21"`
- Rationale: Two consecutive 1s

**Test Case 1.3: Two different digits**
- Input: `"21"`
- Expected Output: `"1211"`
- Rationale: One 2, one 1

**Test Case 1.4: Complex pattern from problem**
- Input: `"1211"`
- Expected Output: `"111221"`
- Rationale: One 1, one 2, two 1s

**Test Case 1.5: Another complex pattern**
- Input: `"111221"`
- Expected Output: `"312211"`
- Rationale: Three 1s, two 2s, one 1

**Test Case 1.6: Multiple different runs**
- Input: `"123"`
- Expected Output: `"111213"`
- Rationale: One 1, one 2, one 3

**Test Case 1.7: Long run of same digit**
- Input: `"1111"`
- Expected Output: `"41"`
- Rationale: Four 1s

**Test Case 1.8: Mixed long and short runs**
- Input: `"3331"`
- Expected Output: `"3311"`
- Rationale: Three 3s, one 1

**Test Case 1.9: All different digits**
- Input: `"1234567890"`
- Expected Output: `"11121314151617181910"`
- Rationale: Each digit appears once

**Test Case 1.10: Edge case - empty string**
- Input: `""`
- Expected Output: `""`
- Rationale: Handle empty input gracefully
- Note: This won't occur with our actual input, but validates robustness

### 2. Sequential Iteration Tests

**Test Case 2.1: First 5 iterations from "1"**
- Iteration 0: `"1"`
- Iteration 1: `"11"` (length 2)
- Iteration 2: `"21"` (length 2)
- Iteration 3: `"1211"` (length 4)
- Iteration 4: `"111221"` (length 6)
- Iteration 5: `"312211"` (length 6)
- Rationale: Verify iteration mechanism with known sequence

**Test Case 2.2: Length growth tracking**
- Start with `"1"`
- Track length after each iteration for first 10 iterations
- Verify lengths are monotonically increasing (or stable)
- Expected approximate growth factor: ~1.3 per iteration

**Test Case 2.3: Idempotency check**
- If we reach iteration N and apply the transformation, we should get iteration N+1
- No transformation should be skipped or duplicated

### 3. Integration Tests

**Test Case 3.1: Actual input with small iterations**
- Input: `"1321131112"`
- Iterations: 5
- Verify the transformation produces a deterministic result
- Check the length is correct and consistent
- First transformation: `"1321131112"` → `"11131221131112"` (manual verification recommended)

**Test Case 3.2: Actual input with medium iterations**
- Input: `"1321131112"`
- Iterations: 10
- Verify the result length is reasonable
- Expected length: approximately 10 × 1.303577^10 ≈ 130-140 characters
- Compare growth rate with expected Conway's constant

**Test Case 3.3: Full problem - 40 iterations**
- Input: `"1321131112"`
- Iterations: 40
- Verify the final length is produced
- Expected range: approximately 3-4 million characters (based on Conway's constant)
- The exact value should be deterministic and consistent across runs

### 4. Property-Based Tests

**Test Case 4.1: Length always increases or stays same**
- Property: `len(look_and_say(s)) >= len(s)` for most cases
- Exception: This is not always true (e.g., "1111" → "41"), but over iterations, growth occurs
- Verify no unexpected length collapse

**Test Case 4.2: Output only contains digits**
- Property: The result should only contain digit characters '0'-'9'
- No special characters, letters, or whitespace

**Test Case 4.3: Counts can be multi-digit**
- Property: When we have runs of 10+ identical digits, the count itself becomes multi-digit
- Example: `"11111111111"` (11 ones) → `"1111"` (count "11" + digit "1")
- Rationale: Verify the implementation handles multi-digit counts correctly
- This means the output can have consecutive identical digits in the count portion

**Test Case 4.4: Even length for most sequences**
- Property: Output length is usually even (count + digit pairs)
- Verify our final result has even length

### 5. Performance and Stress Tests

**Test Case 5.1: Runtime reasonable**
- Full 40 iterations should complete in < 30 seconds
- Measure actual runtime
- If too slow, optimization needed

**Test Case 5.2: Memory usage reasonable**
- Monitor memory usage during execution
- Should not exceed ~100 MB for 40 iterations
- No memory leaks between iterations

**Test Case 5.3: Large count handling**
- Input: `"11111111111111111"` (17 ones)
- Verify counts > 9 are handled correctly
- Expected: `"1711"` (count "17" + digit "1")

## Testing Implementation Approach

### Manual Testing Process

1. **Create test file** (`test_solution.py`)
2. **Implement unit tests** for `look_and_say` function
3. **Run each example** from problem statement
4. **Verify with small iterations** (1, 2, 3, 5, 10)
5. **Run full 40 iterations** and check result

### Test Script Structure

```python
def test_look_and_say():
    """Test the core transformation function"""
    test_cases = [
        ("1", "11"),
        ("11", "21"),
        ("21", "1211"),
        ("1211", "111221"),
        ("111221", "312211"),
        ("123", "111213"),
        ("1111", "41"),
        ("3331", "3311"),
    ]

    for input_str, expected in test_cases:
        result = look_and_say(input_str)
        assert result == expected, f"Failed for {input_str}: got {result}, expected {expected}"
        print(f"✓ {input_str} → {result}")

def test_iterations():
    """Test multiple iterations"""
    result = "1"
    expected_sequence = ["1", "11", "21", "1211", "111221", "312211"]

    for i, expected in enumerate(expected_sequence):
        assert result == expected, f"Iteration {i} failed"
        print(f"✓ Iteration {i}: {result} (length {len(result)})")
        if i < len(expected_sequence) - 1:
            result = look_and_say(result)

def test_actual_input():
    """Test with actual input"""
    input_str = "1321131112"

    # Test small iterations
    result = apply_iterations(input_str, 10)
    print(f"After 10 iterations: length = {len(result)}")

    # Test full 40 iterations
    result = apply_iterations(input_str, 40)
    length = len(result)
    print(f"After 40 iterations: length = {length}")

    # Sanity check: based on Conway's constant, should be 3-4M characters
    assert 3_000_000 < length < 4_500_000, f"Length {length} seems unreasonable"
```

## Verification Strategy

### Step 1: Verify Core Logic
- Run all unit tests for `look_and_say`
- Confirm all examples from problem statement work
- Check edge cases

### Step 2: Verify Iteration Mechanism
- Test with 1, 2, 3, 5, 10 iterations
- Compare intermediate results with manual calculations
- Ensure no iteration is skipped

### Step 3: Verify Final Result
- Run with full 40 iterations
- Check the length is a reasonable number
- Estimate expected length using Conway's constant: 10 × 1.303577^40 ≈ 3.6M
- Actual result should be in the range 3.0M - 4.5M characters
- Save the result for regression testing

### Step 4: Cross-Verification
- Implement a second version using manual while-loop (instead of groupby) and compare
- Verify result is deterministic: run multiple times and check same answer
- For small iterations, manually verify the transformation is correct
- Check that intermediate outputs look reasonable (count-digit patterns)

## Success Criteria

The solution is correct if:
1. ✓ All unit tests pass
2. ✓ All examples from problem statement produce correct output
3. ✓ Iteration mechanism works for small counts (verified manually)
4. ✓ Final result length is within expected range (3.0M - 4.5M characters)
5. ✓ Final output only contains digits
6. ✓ Runtime is acceptable (< 30 seconds)
7. ✓ No errors or exceptions during execution
8. ✓ Result is deterministic and consistent across multiple runs

## Known Edge Cases to Consider

1. **Large counts**: If more than 9 consecutive digits, count becomes 2 digits (e.g., "11" for 11 occurrences)
   - Example: `"11111111111"` (11 ones) → `"1111"` NOT `"111"`
2. **Empty string**: Should handle gracefully with validation error (though not in our input)
3. **Single digit input**: Should produce correct 2-digit output
4. **Growth rate**: Should be approximately exponential with factor ~1.3 (Conway's constant)
5. **Input validation**: Input file contains raw digits, need to strip whitespace
6. **Multi-digit counts in output**: The count portion can itself have repeated digits

## Regression Testing

After implementation:
- Save the final result length for 40 iterations of `"1321131112"`
- Any code changes should produce the exact same result
- If result changes, investigate why (likely a bug introduced)
- This is Advent of Code Day 10 Part 1, so the answer should match the expected solution

## Additional Validation

1. **Input File Format**: Verify `input.md` contains only the raw string `1321131112` (possibly with trailing newline)
2. **Determinism**: Run the solution multiple times - should always get the same answer
3. **Manual Verification**: For iteration 1, manually verify:
   - `"1321131112"` → `"11131221131112"`
   - Break down: one 1, one 3, two 1s, one 3, two 1s, two 1s
4. **Progress Logging**: Consider enabling progress output to monitor the 40 iterations
5. **Part 2 Preparation**: Keep iterations as a parameter since part 2 may require 50 iterations
