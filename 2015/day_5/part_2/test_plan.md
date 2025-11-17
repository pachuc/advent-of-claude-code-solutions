# Test Plan: String Classification (Nice vs Naughty)

## Testing Strategy
The testing approach will validate both individual conditions and the integrated solution, focusing on edge cases and the provided examples.

## Test Categories

### 1. Unit Tests for Condition 1: Non-overlapping Pairs

#### Test Case 1.1: Basic Non-overlapping Pair (True)
- **Input**: `"xyxy"`
- **Expected**: `True`
- **Rationale**: Pair "xy" appears at positions 0-1 and 2-3 without overlapping

#### Test Case 1.2: Non-overlapping Pair with Gap (True)
- **Input**: `"aabcdefgaa"`
- **Expected**: `True`
- **Rationale**: Pair "aa" appears at positions 0-1 and 8-9 without overlapping

#### Test Case 1.3: Overlapping Pair Only (False)
- **Input**: `"aaa"`
- **Expected**: `False`
- **Rationale**: "aa" at 0-1 overlaps with "aa" at 1-2; no non-overlapping occurrence

#### Test Case 1.4: No Repeated Pairs (False)
- **Input**: `"abcdefgh"`
- **Expected**: `False`
- **Rationale**: No pair appears more than once

#### Test Case 1.5: Overlapping Then Non-overlapping (True)
- **Input**: `"aaaa"`
- **Expected**: `True`
- **Rationale**: "aa" at 0-1 and "aa" at 2-3 don't overlap

#### Test Case 1.6: Multiple Different Pairs (True)
- **Input**: `"abcabc"`
- **Expected**: `True`
- **Rationale**: "ab", "bc", or "ca" appear twice non-overlapping

#### Test Case 1.7: Similar Pairs But Not Repeating (False)
- **Input**: `"xyyx"`
- **Expected**: `False`
- **Rationale**: Contains pairs "xy", "yy", "yx" but none appear twice - no pair repeats

#### Test Case 1.8: Too Short (False)
- **Input**: `"abc"`
- **Expected**: `False`
- **Rationale**: Cannot have non-overlapping pairs with length < 4

#### Test Case 1.9: Edge Case - Pair at Start and End (True)
- **Input**: `"abcdefab"`
- **Expected**: `True`
- **Rationale**: "ab" appears at beginning and end

#### Test Case 1.10: All Same Character Short (True)
- **Input**: `"aaaa"`
- **Expected**: `True`
- **Rationale**: "aa" appears at positions 0-1 and 2-3 (non-overlapping)

### 2. Unit Tests for Condition 2: Letter Repeat with One Between

#### Test Case 2.1: Basic Pattern (True)
- **Input**: `"xyx"`
- **Expected**: `True`
- **Rationale**: 'x' at positions 0 and 2 with 'y' between

#### Test Case 2.2: Pattern in Middle (True)
- **Input**: `"abcdefeghi"`
- **Expected**: `True`
- **Rationale**: 'e' at positions 4 and 6 with 'f' between

#### Test Case 2.3: Triple Letter (True)
- **Input**: `"aaa"`
- **Expected**: `True`
- **Rationale**: 'a' at positions 0 and 2 with 'a' between

#### Test Case 2.4: No Such Pattern (False)
- **Input**: `"abcdef"`
- **Expected**: `False`
- **Rationale**: No letter repeats with exactly one between

#### Test Case 2.5: Pattern at Start (True)
- **Input**: `"aba"`
- **Expected**: `True`
- **Rationale**: Minimum viable string with this pattern

#### Test Case 2.6: Pattern at End (True)
- **Input**: `"xyzaz"`
- **Expected**: `True`
- **Rationale**: 'z' at positions 2 and 4 with 'a' between

#### Test Case 2.7: Multiple Patterns (True)
- **Input**: `"abacad"`
- **Expected**: `True`
- **Rationale**: 'a' repeats multiple times with one letter between

#### Test Case 2.8: Too Short (False)
- **Input**: `"ab"`
- **Expected**: `False`
- **Rationale**: Cannot have pattern with length < 3

#### Test Case 2.9: Letters Two Apart (False)
- **Input**: `"abca"`
- **Expected**: `False`
- **Rationale**: 'a' appears but not with exactly one letter between (has 2 between)

### 3. Integration Tests: Combined Classification

#### Test Case 3.1: Nice String Example 1 (True)
- **Input**: `"qjhvhtzxzqqjkmpb"`
- **Expected**: `True`
- **Details**:
  - Condition 1: "qj" appears at positions 0 and 10
  - Condition 2: "zxz" at positions 6-8

#### Test Case 3.2: Nice String Example 2 (True)
- **Input**: `"xxyxx"`
- **Expected**: `True`
- **Details**:
  - Condition 1: "xx" appears at positions 1 and 3
  - Condition 2: "xyx" at positions 2-4

#### Test Case 3.3: Naughty String Example 1 (False)
- **Input**: `"uurcxstgmygtbstg"`
- **Expected**: `False`
- **Details**:
  - Condition 1: "tg" appears twice (True)
  - Condition 2: No repeat with one between (False)

#### Test Case 3.4: Naughty String Example 2 (False)
- **Input**: `"ieodomkazucvgmuy"`
- **Expected**: `False`
- **Details**:
  - Condition 1: No non-overlapping pair (False)
  - Condition 2: "odo" at positions 2-4 (True)

#### Test Case 3.5: Both Conditions False (False)
- **Input**: `"abcdefgh"`
- **Expected**: `False`
- **Details**: Neither condition satisfied

#### Test Case 3.6: Edge Case - Empty String (False)
- **Input**: `""`
- **Expected**: `False`
- **Rationale**: Cannot satisfy either condition

#### Test Case 3.7: Edge Case - Single Character (False)
- **Input**: `"a"`
- **Expected**: `False`
- **Rationale**: Too short for either condition

#### Test Case 3.8: Minimum Nice String (True)
- **Input**: `"xyxyx"`
- **Expected**: `True`
- **Details**:
  - Condition 1: "xy" at positions 0-1 and 3-4 (non-overlapping)
  - Condition 2: "xyx" pattern at positions 0-2 (x repeats with y between)

### 4. Verification Tests with Actual Input

#### Test Case 4.1: Count Sample Strings
Manually verify the first 10-20 strings from `input.md`:
- Read each string
- Manually check both conditions
- Verify classification matches expected result
- Track count to ensure accuracy

**Example verification for first 3 strings**:
1. `"uxcplgxnkwbdwhrp"`:
   - Check for pairs: "xn" at positions 5,9? No. Need manual verification
   - Check for xyx pattern: scan through

2. `"suerykeptdsutidb"`:
   - Check for pairs
   - Check for xyx pattern

3. `"dmrtgdkaimrrwmej"`:
   - Check for pairs: "mr" appears twice
   - Check for xyx pattern: scan through

#### Test Case 4.2: Full Input Count
- Run solution on complete `input.md` (1000 strings)
- Expected: A single integer output
- Validation: The answer should be reasonable (between 0 and 1000)

#### Test Case 4.3: Known Statistics
Based on the conditions:
- Estimate ~30-50% of random strings might have non-overlapping pairs
- Estimate ~40-60% of random strings might have the xyx pattern
- Combined (both): Estimate ~15-30% might be "nice"
- Expected answer range: 150-300 (rough estimate for validation)

### 5. Edge Case and Boundary Tests

#### Test Case 5.1: All Same Character
- **Input**: `"aaaaaaa"`
- **Expected**: `True`
- **Details**:
  - Condition 1: Many non-overlapping "aa" pairs
  - Condition 2: Many "aaa" patterns

#### Test Case 5.2: Alternating Two Characters
- **Input**: `"ababab"`
- **Expected**: `True`
- **Details**:
  - Condition 1: "ab" and "ba" appear multiple times
  - Condition 2: "aba" and "bab" patterns exist

#### Test Case 5.3: Long String Without Repeats
- **Input**: `"abcdefghijklmnop"`
- **Expected**: `False`
- **Details**: No character repeats at all

#### Test Case 5.4: Pair Near Boundary
- **Input**: `"abxab"`
- **Expected**: `False`
- **Details**:
  - Condition 1: "ab" appears at positions 0-1 and 3-4 (True)
  - Condition 2: No letter repeats with one between (False)
  - Overall: False (needs both conditions)

### 6. Manual Verification Process

#### Step 1: Unit Test Execution
- Create a test file with all unit test cases
- Run each condition function independently
- Verify all unit tests pass

#### Step 2: Integration Test Execution
- Test provided examples first
- Verify output matches expected nice/naughty classification

#### Step 3: Spot Check Input Strings
- Randomly select 5-10 strings from input.md
- Manually verify classification:
  - List all pairs in the string
  - Check for non-overlapping occurrences
  - Check for xyx pattern
  - Confirm final classification

#### Step 4: Final Count Validation
- Run solution on full input
- Verify output is a single integer
- Check if count is within expected range (150-300)
- If count seems unreasonable, recheck logic

### 7. Testing Implementation Approach

Since we're building a simple script (not production code), we'll use a streamlined testing approach:

1. **Manual Testing**: Add test cases directly to the script with a `test()` function
2. **Assertion-based**: Use simple `assert` statements for validation
3. **Print Debugging**: Output intermediate results for verification

**Test function structure**:
```python
def test():
    # Condition 1 tests
    assert has_non_overlapping_pair("xyxy") == True
    assert has_non_overlapping_pair("aaa") == False
    # ... more tests

    # Condition 2 tests
    assert has_repeat_with_one_between("xyx") == True
    assert has_repeat_with_one_between("abc") == False
    # ... more tests

    # Integration tests
    assert is_nice("qjhvhtzxzqqjkmpb") == True
    assert is_nice("uurcxstgmygtbstg") == False
    # ... more tests

    print("All tests passed!")
```

### 8. Expected Output Format Validation

- Output must be a single integer
- No additional text or formatting
- Newline at end is acceptable
- Must represent count of nice strings (0 ≤ count ≤ 1000)

### 9. Performance Validation

- Solution should run in under 1 second for 1000 strings
- No memory issues expected with this input size
- Can manually time execution to ensure efficiency

## Test Execution Order

1. Run unit tests for Condition 1
2. Run unit tests for Condition 2
3. Run integration tests with provided examples
4. Perform manual verification on sample strings
5. Run full solution on complete input
6. Validate output format and reasonableness
7. If time permits, re-verify a random sample of classifications

## Success Criteria

- All unit tests pass
- All provided examples classify correctly
- Output is a single integer in reasonable range
- Manual spot-checks confirm correct classification
- Solution runs efficiently (< 1 second)
