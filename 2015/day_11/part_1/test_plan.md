# Test Plan: Password Generation Algorithm

## Overview
Comprehensive testing strategy to verify the password generation algorithm works correctly for all validation rules and edge cases.

## Updates Based on Critique
This test plan has been updated to address the following issues:
1. Fixed Test 1.4 input to have 8 characters (was 7)
2. Added Test 1.8 for forbidden character during carry propagation
3. Added Test 4.4 for already-valid password input
4. Corrected Test 4.2 description to clarify only 'i', 'o', 'l' are forbidden
5. Enhanced Test 2.14 explanation about unique pair counting
6. Removed unrealistic boundary test (zzzzzzzz) and focused on practical edge cases

## Test Categories

### Category 1: Unit Tests for Increment Function

#### Test 1.1: Basic Increment
**Input:** `"aaaaaaaa"`
**Expected:** `"aaaaaaab"`
**Purpose:** Verify simple increment of last character

#### Test 1.2: Single Position Carry
**Input:** `"aaaaaaaz"`
**Expected:** `"aaaaaaba"`
**Purpose:** Verify wrap-around and carry to next position

#### Test 1.3: Multiple Position Carry
**Input:** `"aaaaaazz"`
**Expected:** `"aaaaabaa"`
**Purpose:** Verify carry propagates multiple positions

#### Test 1.4: Full Carry Propagation
**Input:** `"azzzzzzz"`
**Expected:** `"baaaaaaa"`
**Purpose:** Verify carry propagates to leftmost position

#### Test 1.5: Forbidden Character Skip - 'i'
**Input:** `"aaaaaahh"`
**Expected:** `"aaaaajaa"` (skips 'i')
**Purpose:** Verify optimization skips 'i' and resets right positions

#### Test 1.6: Forbidden Character Skip - 'o'
**Input:** `"aaaaannn"`
**Expected:** `"aaaaapaa"` (skips 'o')
**Purpose:** Verify optimization skips 'o'

#### Test 1.7: Forbidden Character Skip - 'l'
**Input:** `"aaaaaakk"`
**Expected:** `"aaaaamma"` (skips 'l')
**Purpose:** Verify optimization skips 'l'

#### Test 1.8: Forbidden Character During Carry Propagation
**Input:** `"aaahzzzz"`
**Expected:** `"aaajaaaa"` (carry propagates, hits 'i', skips to 'j', resets right positions)
**Purpose:** Verify forbidden character optimization works during multi-position carries

### Category 2: Unit Tests for Validation Functions

#### Test 2.1: Forbidden Characters - Valid
**Input:** `"abcdefgh"`
**Expected:** `True`
**Purpose:** No forbidden characters present

#### Test 2.2: Forbidden Characters - Contains 'i'
**Input:** `"abcdefgi"`
**Expected:** `False`
**Purpose:** Detect 'i'

#### Test 2.3: Forbidden Characters - Contains 'o'
**Input:** `"abcdofgh"`
**Expected:** `False`
**Purpose:** Detect 'o'

#### Test 2.4: Forbidden Characters - Contains 'l'
**Input:** `"lbcdefgh"`
**Expected:** `False`
**Purpose:** Detect 'l'

#### Test 2.5: Forbidden Characters - Multiple
**Input:** `"ioldefgh"`
**Expected:** `False`
**Purpose:** Detect multiple forbidden characters

#### Test 2.6: Increasing Straight - At Beginning
**Input:** `"abcdefgh"`
**Expected:** `True`
**Purpose:** Straight at start (abc)

#### Test 2.7: Increasing Straight - At End
**Input:** `"aaaaaxyz"`
**Expected:** `True`
**Purpose:** Straight at end (xyz)

#### Test 2.8: Increasing Straight - In Middle
**Input:** `"aaabcdaa"`
**Expected:** `True`
**Purpose:** Straight in middle (bcd)

#### Test 2.9: Increasing Straight - None Present
**Input:** `"aabbccdd"`
**Expected:** `False`
**Purpose:** No consecutive increasing sequence

#### Test 2.10: Increasing Straight - Non-Consecutive
**Input:** `"aaceggaa"`
**Expected:** `False`
**Purpose:** Letters skip (a,c,e not consecutive)

#### Test 2.11: Two Pairs - Valid Different Pairs
**Input:** `"aabbccdd"`
**Expected:** `True`
**Purpose:** Multiple valid pairs (aa, bb, cc, dd)

#### Test 2.12: Two Pairs - Exactly Two
**Input:** `"aabbcdee"`
**Expected:** `True`
**Purpose:** Exactly two pairs (aa, bb, ee)

#### Test 2.13: Two Pairs - Only One Pair
**Input:** `"aabcdefg"`
**Expected:** `False`
**Purpose:** Only one pair present

#### Test 2.14: Two Pairs - Same Letter Repeated
**Input:** `"aaaaabcd"`
**Expected:** `False`
**Purpose:** Multiple 'aa' pairs count as only one unique pair (algorithm finds pairs at positions 0 and 2, both are 'a', so set(['a']) has length 1)

#### Test 2.15: Two Pairs - Non-Overlapping Check
**Input:** `"aaabbbcd"`
**Expected:** `True`
**Purpose:** Triple letters create non-overlapping pairs (aaa→aa, bbb→bb)

#### Test 2.16: Two Pairs - Triple Creates One Pair
**Input:** `"aaabcdef"`
**Expected:** `False`
**Purpose:** 'aaa' only counts as one pair, need second different pair

### Category 3: Integration Tests for Complete Validation

#### Test 3.1: Valid Password - All Requirements
**Input:** `"abcdffaa"`
**Expected:** `True`
**Purpose:** Has straight (bcd), pairs (ff, aa), no forbidden chars

#### Test 3.2: Invalid - Has Forbidden Char
**Input:** `"abciefaa"`
**Expected:** `False`
**Purpose:** Has 'i' (forbidden)

#### Test 3.3: Invalid - No Straight
**Input:** `"aabbccdd"`
**Expected:** `False`
**Purpose:** Has pairs but no increasing straight

#### Test 3.4: Invalid - No Pairs
**Input:** `"abcdefgh"`
**Expected:** `False`
**Purpose:** Has straight but no pairs

#### Test 3.5: Invalid - Only One Pair
**Input:** `"abcdefaa"`
**Expected:** `False`
**Purpose:** Has straight and one pair, but needs two pairs

### Category 4: End-to-End Tests with Examples

#### Test 4.1: Example from Problem
**Input:** `"abcdefgh"`
**Expected:** `"abcdffaa"`
**Purpose:** Verify against provided example

**Verification Steps:**
1. Increment from "abcdefgh"
2. First valid password should be "abcdffaa"
3. Check validation: has 'bcd' straight, has 'ff' and 'aa' pairs, no forbidden chars

#### Test 4.2: Example from Problem with Forbidden Skip
**Input:** `"ghijklmn"`
**Expected:** `"ghjaabcc"`
**Purpose:** Verify skipping of forbidden characters

**Verification Steps:**
1. Input "ghijklmn" contains forbidden 'i' and 'l'
2. Algorithm should skip passwords containing 'i', 'o', or 'l' (only these three are forbidden)
3. First valid is "ghjaabcc"
4. Verify: has no forbidden chars ('i', 'o', 'l'), has increasing straight, has two pairs

#### Test 4.3: Actual Input
**Input:** `"vzbxkghb"`
**Expected:** (unknown, but should complete in reasonable time)
**Purpose:** Verify solution for actual problem input

#### Test 4.4: Already Valid Password
**Input:** `"abcdffaa"` (already valid)
**Expected:** Next valid password after this one (e.g., `"abcdffbb"` or similar)
**Purpose:** Verify algorithm increments at least once even if input is already valid

### Category 5: Edge Cases and Boundary Conditions

#### Test 5.1: Password Already Contains Increasing Straight
**Input:** `"aabcdefg"`
**Expected:** Should find next valid (might be close)
**Purpose:** Test when one requirement already met

#### Test 5.3: Early Alphabet Password
**Input:** `"aaaaaaaa"`
**Expected:** Find first valid from beginning (e.g., first password with straight, pairs, no forbidden chars)
**Purpose:** Test from minimal starting point

#### Test 5.4: Multiple Forbidden Characters in Input
**Input:** `"aiolaiol"`
**Expected:** Should skip ahead quickly due to optimizations
**Purpose:** Verify optimization handles multiple forbidden chars

### Category 6: Performance Tests

#### Test 6.1: Iteration Count Check
**Purpose:** Count how many increments needed for test inputs
**Method:**
- Add counter in main loop
- Print iteration count for each test
- Verify completes in < 1 million iterations for typical inputs

#### Test 6.2: Timing Test
**Purpose:** Ensure solution runs in reasonable time
**Method:**
- Time execution for actual input
- Should complete in < 10 seconds
- If slower, optimization may be needed

## Test Execution Strategy

### Phase 1: Unit Testing (Individual Functions)
1. Test `increment_password()` with all increment test cases
2. Test `has_no_forbidden_chars()` with forbidden character tests
3. Test `has_increasing_straight()` with straight tests
4. Test `has_two_pairs()` with pair tests
5. Verify each function works correctly in isolation

### Phase 2: Integration Testing (Combined Validation)
1. Test `is_valid_password()` with complete validation tests
2. Verify all three requirements checked properly
3. Verify short-circuit evaluation works

### Phase 3: End-to-End Testing
1. Test `find_next_password()` with provided examples
2. Test with actual input
3. Verify output format is correct

### Phase 4: Edge Case Testing
1. Run boundary condition tests
2. Run performance tests
3. Verify no infinite loops or crashes

## Test Implementation Approach

Since this is a script (not production code), we'll use simple assertion-based testing:

```python
# Simple test runner
def test_function():
    result = function_to_test(input)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Test passed: {test_name}")
```

Run all tests before considering solution complete.

## Success Criteria

1. ✓ All unit tests pass for individual functions
2. ✓ Integration tests confirm all validation rules work together
3. ✓ Example inputs produce expected outputs
4. ✓ Actual problem input produces an answer in < 10 seconds
5. ✓ Output format matches specification (8 lowercase letters, plain text)
6. ✓ No infinite loops or crashes on any test case

## Manual Verification

For the final answer from actual input:
1. Manually verify it has no 'i', 'o', or 'l'
2. Manually identify the increasing straight sequence
3. Manually identify the two non-overlapping pairs
4. Confirm it's larger than the input (incremented at least once)
