# Test Plan: Finding Prototype Fabric Box IDs (Part 2)

## Testing Strategy Overview

Since we're solving a specific puzzle with a single input file, our testing approach focuses on:
1. Validating the solution with the provided example
2. Verifying individual function behavior
3. Testing the actual input to ensure correct answer
4. Checking edge cases relevant to the problem domain

## Test 1: Example from Problem Statement

### Purpose
Verify the solution works correctly with the provided example

### Test Data
```
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
```

### Expected Behavior
1. **count_differences("fghij", "fguij")** → 1
2. **count_differences("abcde", "axcye")** → 2
3. **get_common_letters("fghij", "fguij")** → "fgij"
4. **find_prototype_boxes()** → "fgij"

### Test Method
- Create a small test file with the example data
- Run the solution against it
- Verify output is exactly "fgij" with no extra whitespace or formatting

### Success Criteria
- Output matches expected result exactly: "fgij"

## Test 2: Unit Test for count_differences()

### Purpose
Ensure the difference counting function works correctly in all cases

### Test Cases

| String 1 | String 2 | Expected Differences | Description |
|----------|----------|---------------------|-------------|
| "fghij" | "fguij" | 1 | Example case - one difference |
| "abcde" | "axcye" | 2 | Example case - two differences |
| "abcde" | "abcde" | 0 | Identical strings |
| "abcdefghijklmnopqrstuvwxyz" | "zbcdefghijklmnopqrstuvwxya" | 2 | First and last differ |
| "aaaa" | "aaab" | 1 | Last position differs |
| "aaaa" | "baaa" | 1 | First position differs |
| "aaaa" | "abaa" | 1 | Middle position differs |
| "abcd" | "dcba" | 4 | All positions differ |

### Test Method
- Call `count_differences()` with each test case
- Assert the returned count matches expected value

### Success Criteria
- All test cases pass with correct counts

## Test 3: Unit Test for get_common_letters()

### Purpose
Verify common letter extraction works correctly

### Test Cases

| String 1 | String 2 | Expected Output | Description |
|----------|----------|-----------------|-------------|
| "fghij" | "fguij" | "fgij" | Example case |
| "abcde" | "axcye" | "acye" | Two differences - still extracts common |
| "abcde" | "abcde" | "abcde" | Identical strings |
| "abc" | "xyz" | "" | No common characters (won't occur in practice) |
| "xpysntkqrbuhefmcajodiglvzw" | "xpysntkqrbuhefmcajodiglvzw" | "xpysntkqrbuhefmcajodiglvzw" | Full length identical |

**Note**: The "no common characters" case won't occur in the actual problem since the main algorithm only calls this function when exactly 1 difference exists, but it's included for completeness.

### Test Method
- Call `get_common_letters()` with each test case
- Assert the returned string matches expected output exactly

### Success Criteria
- All test cases return correct common letter strings

## Test 4: Actual Input Validation

### Purpose
Verify the solution produces a valid answer for the actual puzzle input

### Test Method
1. Run the complete solution against `input.md`
2. Verify the output is a string of exactly 25 characters (26 original - 1 differing)
3. Verify the output contains only lowercase letters
4. Verify the output has no whitespace

### Expected Output Characteristics
- Length: 25 characters (one less than the 26-character box IDs)
- Character set: lowercase letters only [a-z]
- Format: single line, no extra whitespace

### Success Criteria
- Output length is 25
- All characters are lowercase letters
- No whitespace in output

## Test 5: Verify Exactly One Pair Exists (Optional)

### Purpose
Confirm the assumption that exactly one pair of box IDs differs by one character

**Note**: This test is optional since Test 6 (Manual Verification) already validates this assumption more thoroughly. If reconstruction finds exactly 2 box IDs, then exactly one pair exists.

### Test Method
1. Modify `find_prototype_boxes()` temporarily to count ALL pairs with exactly one difference
2. Run against actual input
3. Verify count is exactly 1

### Expected Behavior
- Counter should increment exactly once
- This validates the problem's guarantee

### Success Criteria
- Exactly one pair found with one character difference

### Priority
**Low** - Can be skipped if time is limited since Test 6 provides equivalent validation.

## Test 6: Manual Verification of Result

### Purpose
Double-check the correctness of the final answer

### Test Method
1. Run the solution to get the result string (let's call it `result`)
2. Manually search for two box IDs in input.md where:
   - Removing one character from each produces `result`
   - The two box IDs differ at exactly one position
3. Verify these two box IDs exist in the input

### Verification Steps
1. Take the output string (25 chars)
2. For each position 0-25, try inserting each letter a-z
3. Check if the resulting 26-char string exists in the input
4. Should find exactly 2 such strings (the prototype pair)

### Success Criteria
- Can reconstruct exactly 2 box IDs from the result
- Both reconstructed box IDs exist in input.md
- The two box IDs differ by exactly one character

## Test 7: Edge Case - Position of Difference

### Purpose
Ensure the solution works regardless of where the differing character is located

### Test Cases
Create mini test sets where the difference is at:
- First position (index 0)
- Last position (index 25)
- Middle position (index 13)

### Test Data Examples

**Difference at start:**
```
abcdefghij
xbcdefghij
```
Expected: "bcdefghij"

**Difference at end:**
```
abcdefghij
abcdefghix
```
Expected: "abcdefghi"

**Difference in middle:**
```
abcdefghij
abcdxfghij
```
Expected: "abcdfghij"

### Success Criteria
- Correctly extracts common letters regardless of difference position

## Test 8: Performance Verification (Low Priority)

### Purpose
Ensure the solution runs efficiently on the actual input

**Note**: With only 250 box IDs and simple comparison logic, performance testing is somewhat overkill for a one-time puzzle solution. This test can be combined with Test 4 by simply noting execution time.

### Test Method
1. Time the execution of the solution (can be combined with Test 4)
2. Measure on the full 250 box ID input

### Expected Performance
- Runtime: < 1 second (should be much faster, likely < 100ms)
- No memory issues
- No timeout or hanging

### Success Criteria
- Completes in reasonable time (< 1 second)

### Priority
**Low** - Can be combined with Test 4 rather than run separately.

## Test 9: Input Parsing Validation

### Purpose
Verify input is parsed correctly (reused from Part 1)

### Test Method
1. Run `parse_input('input.md')`
2. Check the returned list:
   - Length is 250 (count of box IDs)
   - All elements are strings
   - All strings have length 26
   - No empty strings
   - No strings with whitespace

### Success Criteria
- List has 250 elements
- All elements are 26-character strings
- No whitespace in any string

## Test 10: Output Format Validation

### Purpose
Ensure output matches the exact format requirements

### Test Method
1. Capture the stdout from running `main()`
2. Verify:
   - Single line output
   - No extra newlines (besides the one from print())
   - No extra text or labels
   - Just the common letters string

### Expected Output Format
```
<25 lowercase letters>\n
```

### Success Criteria
- Output is exactly the result string followed by a single newline
- No additional formatting, labels, or text

## Final Integration Test

### Purpose
End-to-end validation of the complete solution

### Test Steps
1. Start with clean environment
2. Run: `python solution.py`
3. Capture output
4. Verify output is a 25-character lowercase string
5. Verify the answer is reasonable (matches expected characteristics)

### Success Criteria
- Script runs without errors
- Produces valid output
- Output format is correct
- Result is a valid answer (can be manually verified by searching input.md)

## Test Implementation Approach

### How to Structure Tests
**Recommended approach**: Create a separate `test_solution.py` file with simple assert statements

**Example structure**:
```python
# test_solution.py
from solution import count_differences, get_common_letters, find_prototype_boxes, parse_input

def test_count_differences():
    assert count_differences("fghij", "fguij") == 1
    assert count_differences("abcde", "axcye") == 2
    assert count_differences("abcde", "abcde") == 0
    print("✓ count_differences tests passed")

def test_get_common_letters():
    assert get_common_letters("fghij", "fguij") == "fgij"
    assert get_common_letters("abcde", "abcde") == "abcde"
    print("✓ get_common_letters tests passed")

# ... more test functions

if __name__ == '__main__':
    test_count_differences()
    test_get_common_letters()
    # ... call other test functions
```

**For the example test**: Create a temporary `test_input.txt` file with the example data.

**Alternative**: Use pytest framework if preferred, but simple assert statements are sufficient for a puzzle script.

## Testing Execution Order

**Recommended testing sequence:**
1. **Test 2** (count_differences unit tests) - validate core logic
2. **Test 3** (get_common_letters unit tests) - validate extraction logic
3. **Test 1** (example from problem) - validate complete flow on known data
4. **Test 9** (input parsing) - validate input handling
5. **Test 4** (actual input validation + performance note) - run on real data, note execution time
6. **Test 6** (manual verification) - double-check correctness (also validates Test 5's assumption)
7. **Test 7** (edge cases) - test different scenarios
8. **Test 10** (output format) - validate output
9. **Final integration test** - complete validation

**Optional/Skippable**:
- Test 5 (verify exactly one pair) - redundant with Test 6
- Test 8 (performance) - can be combined with Test 4

## Success Criteria Summary

The solution is considered correct if:
1. ✅ All unit tests pass
2. ✅ Example test produces "fgij"
3. ✅ Actual input produces a 25-character lowercase string
4. ✅ Manual verification confirms the result is correct
5. ✅ Exactly one pair of box IDs differs by one character
6. ✅ Performance is acceptable (< 1 second)
7. ✅ Output format matches requirements exactly
