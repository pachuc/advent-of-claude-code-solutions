# Testing Plan: Part 2 - Position-Based Password Generation

## Testing Strategy Overview
This plan covers verification of the position-based password generation algorithm. Focus is on correctness of position handling, duplicate rejection, and proper character placement.

## Test Execution Order
Tests should be executed in the following order to maximize efficiency:
1. **Test 1** (Example validation) - Quick sanity check with known answer
2. **Test 8** (Five zeros detection) - Verify basic hash filtering works
3. **Test 5** (Hash generation correctness) - Ensure MD5 computation is correct
4. **Test 2** (Actual input with verification) - Generate and verify real solution
5. **Tests 3, 4, 6, 7, 9** (Edge cases and validation) - Detailed validation
6. **Test 10** (Final integration) - End-to-end confirmation

Running tests in this order ensures basic functionality works before investing time in long-running tests.

## Test 1: Example Case Validation

### Objective
Verify the algorithm works correctly on the provided example.

### Test Data
- Door ID: `abc`
- Expected password: `05ace8e3`

### Procedure
1. Create a test version or modify the main script to accept `abc` as input
2. Run the algorithm
3. Verify the password matches `05ace8e3`

### Expected Intermediate Results (from problem statement)
- Index `3231929`: hash `0000015...` → position `1`, character `5`
- Index `5017308`: hash `000008f...` → position `8` (INVALID) → should be skipped
- Index `5357525`: hash `000004e...` → position `4`, character `e`

### Validation Points
- Invalid position `8` should be rejected
- Final password should be exactly `05ace8e3`
- All positions 0-7 should be filled

### Pass Criteria
✓ Password matches expected output exactly

## Test 2: Actual Input Validation with Mandatory Verification

### Objective
Generate the password for the actual puzzle input AND verify all hashes are correct.

### Test Data
- Door ID: `ugkcyxxp` (from input.md)

### Procedure
1. Run the main solution script
2. Capture the generated password
3. Verify it's an 8-character hexadecimal string
4. **MANDATORY**: Run the verification step that re-computes all hashes
5. Confirm all 8 hashes can be re-computed and are valid

### Validation Points
- Password length is exactly 8 characters
- All characters are in range [0-9a-f]
- All 8 positions (0-7) are filled
- Algorithm terminates properly
- **Verification step passes**: All stored hashes re-compute correctly
- All hashes start with '00000'
- All position and character extractions are correct

### Pass Criteria
✓ 8-character password generated
✓ All characters are valid hexadecimal
✓ Program terminates successfully
✓ **All verification checks pass** (re-computed hashes match)
✓ Console shows "All validations passed!" message

## Test 3: Hash Parsing and Position Validation

### Objective
Verify that both position extraction and character extraction are correct, and that invalid positions are properly rejected.

### Test Cases

#### Case 3.1: Position out of range (8, 9)
- Hash with 6th character = '8' should be **rejected**
- Hash with 6th character = '9' should be **rejected**

#### Case 3.2: Hexadecimal position characters (a-f)
- Hash with 6th character = 'a' should be **rejected**
- Hash with 6th character = 'f' should be **rejected**

#### Case 3.3: Valid positions (0-7)
- Hash with 6th character in '01234567' should be **accepted** (if position not filled)

#### Case 3.4: Character extraction (merged from old Test 10)
- Hash `0000037a...` → position `3` (valid), character `a` (7th char, index 6)
- Verify correct indexing: position = hash_result[5], character = hash_result[6]

### Procedure
1. Monitor debug output or add logging for rejected hashes
2. Verify that hashes with positions 8, 9, a-f are skipped
3. Confirm only positions 0-7 are accepted
4. For accepted hashes, verify character is extracted from index 6 (7th character)

### Pass Criteria
✓ Positions >= 8 are rejected
✓ Hexadecimal positions (a-f) are rejected
✓ Only positions 0-7 can fill password slots
✓ Character extraction uses index 6 (7th character)
✓ Position extraction uses index 5 (6th character)
✓ No off-by-one errors in indexing

## Test 4: Duplicate Position Handling

### Objective
Verify that only the **first** valid hash for each position is used.

### Test Cases

#### Case 4.1: First occurrence wins
- If position `3` is found at index X, and later position `3` is found at index Y (Y > X)
- The character from index X should be in the final password
- The character from index Y should be **ignored**

### Procedure
1. Add a counter or logging to track when duplicate positions are encountered
   - Example: Count how many times `position in password` evaluates to True
   - Or: Add debug print when a duplicate is rejected
2. Run the algorithm and capture all "duplicate rejected" events
3. Verify that for each position, only the first occurrence is used
4. Confirm the counter shows > 0 duplicates were encountered

### Validation Method
- The `found_hashes` list should contain exactly 8 entries (one per position)
- After completion, verify that for each position 0-7, the character in the password matches the first occurrence in the iteration order
- Confirm later duplicates were skipped (counter > 0)

### Pass Criteria
✓ Each position 0-7 appears exactly once in final password
✓ `found_hashes` list has exactly 8 entries
✓ Later occurrences of same position are rejected
✓ Evidence of duplicates being rejected (counter > 0 or log messages)

## Test 5: Hash Generation Correctness

### Objective
Verify MD5 hashes are computed correctly.

### Procedure
1. Select a few indices from the algorithm's output
2. Manually verify the MD5 hash computation:
   - Concatenate door_id + index
   - Compute MD5
   - Check it starts with `00000`
   - Verify 6th and 7th characters

### Example Verification
If algorithm reports:
- Index `12345`: hash `00000ab...` → position `a` (should be rejected)
- Manually verify: `md5(ugkcyxxp12345)` produces that hash

### Pass Criteria
✓ Re-computed hashes match stored hashes
✓ All stored hashes start with `00000`
✓ Position and character extraction is correct

## Test 6: Completeness Check

### Objective
Ensure all 8 positions are filled before termination.

### Procedure
1. Check the final password dictionary/list
2. Verify all positions 0-7 have values
3. Confirm no positions are None/empty

### Edge Cases to Consider

#### Case 6.1: Missing position scenario
- What if theoretically a position is never found?
- In practice, with random hash distribution, this is extremely unlikely
- Algorithm should eventually find all positions

#### Case 6.2: Early termination
- Verify loop continues until exactly 8 positions filled
- Not 7, not 9, exactly 8

### Pass Criteria
✓ Final password has exactly 8 characters
✓ Positions 0-7 all present in dictionary/list
✓ No None or empty values

## Test 7: Password Assembly

### Objective
Verify correct ordering of final password string.

### Procedure
1. Check that characters are assembled in position order (0→7)
2. Verify the password is not scrambled or reversed

### Example
If positions filled as:
- Position 0: '0'
- Position 1: '5'
- Position 2: 'a'
- Position 3: 'c'
- Position 4: 'e'
- Position 5: '8'
- Position 6: 'e'
- Position 7: '3'

Final password should be: `05ace8e3` (NOT `3e8eca50` or any other ordering)

### Pass Criteria
✓ Characters appear in position order 0→7
✓ Final string is correctly assembled

## Test 8: Edge Case - Five Zeros Detection

### Objective
Verify that only hashes starting with exactly five zeros in the specific format are accepted.

### Test Cases

#### Case 8.1: Valid five-zero prefix
- `00000abc...` → VALID
- `00000123...` → VALID

#### Case 8.2: Invalid prefixes
- `0000abc...` (only 4 zeros) → INVALID
- `000001ab...` (6th char is not position) → depends on 6th char
- `10000abc...` → INVALID

### Procedure
1. Verify the code checks `.startswith('00000')`
2. Confirm no off-by-one errors in prefix checking

### Pass Criteria
✓ Only hashes with exactly five leading zeros are processed
✓ Hashes with < 5 or different patterns are rejected

## Test 7: Performance Validation

### Objective
Ensure algorithm completes in reasonable time.

### Metrics
- Total indices checked
- Time to completion
- Indices per character found (average)

### Expected Performance
- Based on Part 1: ~20M indices for 8 sequential characters
- Part 2 expectation: 25-35M indices due to rejections (tightened from original estimate)
- Completion time: several minutes (acceptable for puzzle solution)

### Procedure
1. Time the full execution
2. Log total indices checked
3. Verify it's in the expected range

### Pass Criteria
✓ Completes within 10 minutes (tightened from 15 minutes)
✓ Total indices checked is reasonable (< 35M, tightened from 50M)
✓ No infinite loops or hangs
✓ If exceeds 35M indices, investigate potential algorithm issues

## Test 8: Input Validation

### Objective
Verify the script handles input edge cases properly.

### Test Cases

#### Case 8.1: Empty input file
- If input.md is empty, script should fail with assertion error

#### Case 8.2: Input with whitespace
- If input.md has trailing newlines or spaces, `.strip()` should handle it
- Example: `ugkcyxxp\n` should be read as `ugkcyxxp`

#### Case 8.3: Input with multiple lines
- If input.md has multiple lines, only first line (after strip) should be used
- `.strip()` handles this by removing all leading/trailing whitespace

### Procedure
1. Test with normal input (should work)
2. Test with input containing newlines (should work due to .strip())
3. Optionally test with empty input (should fail gracefully with assertion)

### Pass Criteria
✓ Normal input works correctly
✓ Input with whitespace is handled by .strip()
✓ Empty input fails with clear assertion error

## Test 9: Final Integration Test

### Objective
End-to-end validation of the complete solution.

### Procedure
1. Start with clean state
2. Run solution with actual input `ugkcyxxp`
3. Capture output password
4. Verify password format
5. Confirm all verification steps pass automatically
6. Submit to puzzle validator (if available)

### Expected Output Format
```
Password: [8 hexadecimal characters]
Total indices checked: [number]

Verification:
✓ Index X: hash... -> position 'Y'
(8 verification lines)
All validations passed!
```

### Pass Criteria
✓ Script runs without errors
✓ Produces 8-character hexadecimal password
✓ All 8 positions filled
✓ Verification section shows all checks passed
✓ Password accepted by puzzle system (if testable)

## Debugging Checklist

If tests fail, check:
- [ ] Input file read correctly (no extra whitespace)
- [ ] MD5 hash computed on correct string (door_id + str(index))
- [ ] Hash string is lowercase hexadecimal
- [ ] Position validation is correct (0-7 only)
- [ ] Character extraction is from index 6 (7th character)
- [ ] Position extraction is from index 5 (6th character)
- [ ] Duplicate positions are rejected
- [ ] Final password assembled in correct order (0→7)
- [ ] Loop termination condition is correct (all 8 positions filled)

## Summary of Critical Test Points

**Priority Order:**
1. **Test 1 - Example validation**: abc → 05ace8e3 (Quick sanity check)
2. **Test 8 (old) - Five zeros detection**: Basic hash filtering
3. **Test 5 - Hash correctness**: MD5 computed and re-verified properly
4. **Test 2 - Actual input with verification**: ugkcyxxp produces valid 8-char password with verified hashes
5. **Test 3 - Position filtering**: Only 0-7 accepted, character extraction correct
6. **Test 4 - Duplicate rejection**: First occurrence wins
7. **Test 6 - Completeness**: All 8 positions filled
8. **Test 6 (old) - Assembly order**: Positions 0→7 in sequence
9. **Test 7 - Performance**: Completes in < 10 min with < 35M indices
10. **Test 8 - Input validation**: Handles whitespace, empty input
11. **Test 9 - Final integration**: End-to-end confirmation

**Key Changes from Original Plan:**
- Merged old Test 10 (character extraction) into Test 3 (position validation)
- Removed regression testing (Part 1 is separate script)
- Added Test 8 for input validation
- Strengthened Test 2 with mandatory verification requirement
- Tightened performance bounds in Test 7
- Added explicit test execution order at top of document
