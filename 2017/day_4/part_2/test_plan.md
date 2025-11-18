# Testing Plan - Part 2: Anagram Detection in Passphrases

## Testing Strategy
Verify that the solution correctly identifies anagrams and counts valid passphrases according to the stricter Part 2 rules.

## Test Categories

### 1. Example-Based Testing

#### Test the provided examples from problem.md
These are critical baseline tests:

**Test Case 1**: `abcde fghij`
- Expected: VALID
- Reason: No words are anagrams of each other
- Sorted forms: `abcde`, `fghij` (all unique)

**Test Case 2**: `abcde xyz ecdab`
- Expected: INVALID
- Reason: "ecdab" is an anagram of "abcde"
- Sorted forms: `abcde`, `xyz`, `abcde` (duplicate sorted form)

**Test Case 3**: `a ab abc abd abf abj`
- Expected: VALID
- Reason: Different lengths, all letters must be used
- Sorted forms: `a`, `ab`, `abc`, `abd`, `abf`, `abj` (all unique)

**Test Case 4**: `iiii oiii ooii oooi oooo`
- Expected: VALID
- Reason: Different letter frequencies
- Sorted forms: `iiii`, `iiio`, `iioo`, `iooo`, `oooo` (all unique)

**Test Case 5**: `oiii ioii iioi iiio`
- Expected: INVALID
- Reason: All contain 3 i's and 1 o (all anagrams of each other)
- Sorted forms: `iiio`, `iiio`, `iiio`, `iiio` (all identical)

### 2. Edge Case Testing

#### Empty and whitespace handling
**Test Case 6**: Empty string or blank line
- Expected: Should be skipped/ignored
- Implementation already handles this with `line.strip()` check

**Test Case 7**: Single word passphrase
- Input: `hello`
- Expected: VALID (no pairs to form anagrams)

#### Boundary cases
**Test Case 8**: Two identical words
- Input: `abc abc`
- Expected: INVALID (identical words are also anagrams)
- Sorted forms: `abc`, `abc` (duplicate)

**Test Case 9**: Two words that are anagrams
- Input: `listen silent`
- Expected: INVALID
- Sorted forms: `eilnst`, `eilnst` (duplicate)

**Test Case 10**: Three words, only two are anagrams
- Input: `abc def bca`
- Expected: INVALID ("abc" and "bca" are anagrams)
- Sorted forms: `abc`, `def`, `abc` (duplicate abc)

**Test Case 11**: All unique words
- Input: `cat dog bird fish`
- Expected: VALID
- Sorted forms: `act`, `dgo`, `bdir`, `fhis` (all unique)

### 3. Character Frequency Testing

**Test Case 12**: Same letters, different counts
- Input: `aaa aa a`
- Expected: VALID (different frequencies)
- Sorted forms: `aaa`, `aa`, `a` (all unique)

**Test Case 13**: Same character count, different letters
- Input: `abc def ghi`
- Expected: VALID (different letters)
- Sorted forms: `abc`, `def`, `ghi` (all unique)

**Test Case 14**: Permutations
- Input: `abc acb bac bca cab cba`
- Expected: INVALID (all are anagrams of each other)
- Sorted forms: all `abc` (all identical)

### 4. Full Input Validation

#### Test against actual input.md
**Test Case 15**: Run against full input
- Read all ~512 lines from input.md
- Count valid passphrases
- Expected result: Integer less than 455 (Part 1 answer)
- Verification: The result should be reasonable (likely in range 200-450)

#### Spot check specific lines from input.md
**Test Case 16**: Line 7 from input (verify after reading file)
- Input: `srceh xdwao reshc shecr`
- Analysis (to be verified):
  - `srceh` → `cehrs`
  - `xdwao` → `adowx`
  - `reshc` → `cehrs` (matches srceh!)
  - `shecr` → `cehrs` (also matches!)
- Expected: INVALID (multiple anagrams) - **verify this manually**

**Test Case 17**: Line 1 from input
- Input: `bdwdjjo avricm cjbmj ran lmfsom ivsof`
- Analysis:
  - `bdwdjjo` → `bdddjjo`
  - `avricm` → `acimrv`
  - `cjbmj` → `bcjjm`
  - `ran` → `anr`
  - `lmfsom` → `flmmos`
  - `ivsof` → `fiosv`
- Expected: VALID (all sorted forms are unique)

### 5. Algorithm Correctness Testing

#### Verify sorting approach works correctly
**Test Case 18**: Case sensitivity (if applicable)
- Input should only contain lowercase per problem spec
- No need to test uppercase

**Test Case 19**: Special characters
- Problem states only lowercase letters
- No special character handling needed

### 6. Performance Testing

**Test Case 20**: Large passphrase
- Input: `one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty`
- Expected: VALID (all unique words with unique sorted forms)
- Should complete quickly (milliseconds)
- Verify O(m * k log k) complexity is acceptable

**Test Case 21**: Full input performance
- Run on all 512 lines
- Expected: Complete in under 100 milliseconds (likely < 10ms)
- Given O(70,000) operations, this should be nearly instantaneous
- If takes > 1 second, there's likely an efficiency bug

## Test Execution Plan

### Recommended Test Order
Tests should be executed in this specific order to catch bugs early:

**Phase 1: Verify Examples (CRITICAL)**
1. First, manually test all 5 provided examples from problem.md
2. These are the baseline - if these fail, implementation is wrong
3. Do NOT proceed to full input until all examples pass

**Phase 2: Edge Cases**
4. Test single word, empty lines, identical words
5. Test anagram permutations
6. Test character frequency variations

**Phase 3: Full Input**
7. Run on actual input.md
8. Verify result is < 455 (Part 1 answer)
9. If result ≥ 455, there's a bug - debug before continuing

### Manual Testing Steps
1. Create a test file with the example cases
2. Run the solution on each test case
3. Verify output matches expected results
4. If any fail, use debug mode to print sorted forms

### Automated Testing Approach
```python
def test_validation():
    test_cases = [
        ("abcde fghij", True),
        ("abcde xyz ecdab", False),
        ("a ab abc abd abf abj", True),
        ("iiii oiii ooii oooi oooo", True),
        ("oiii ioii iioi iiio", False),
        # ... more test cases
    ]

    for passphrase, expected_valid in test_cases:
        result = is_valid_passphrase(passphrase)
        assert result == expected_valid, f"Failed for: {passphrase}"
```

### Integration Testing
1. Run solution on actual input.md
2. Verify output is a single integer
3. **CRITICAL**: Verify output < 455 (Part 1 answer)
   - If output = 455: Implementation likely checking duplicates, not anagrams
   - If output > 455: Serious bug - impossible result
   - If output < 455: Likely correct, but verify examples passed
4. Compare with expected answer if available

### Failure Criteria
The solution has FAILED if:
- ❌ Any of the 5 provided examples produce incorrect output
- ❌ Output on full input is ≥ 455
- ❌ Output is not a single integer
- ❌ Solution crashes or raises errors
- ❌ Edge cases (single word, duplicates) fail

## Verification Checklist

Execute in order:
- [ ] **PHASE 1**: All 5 provided examples pass (MUST pass before continuing)
- [ ] **PHASE 2**: Edge cases (empty, single word, duplicates) handled correctly
- [ ] **PHASE 2**: Anagram detection works for various permutations
- [ ] **PHASE 2**: Character frequency tests pass
- [ ] **PHASE 3**: Full input produces reasonable result (< 455)
- [ ] **PHASE 3**: Solution runs efficiently (< 100ms)
- [ ] **PHASE 3**: Output format is correct (single integer)
- [ ] **ALL PHASES**: No crashes or errors on any input

**If any item fails, STOP and debug before proceeding to next phase.**

## Expected Results Summary

- **Part 1 answer**: 455 valid passphrases (duplicate check)
- **Part 2 answer**: Should be < 455 (stricter anagram check)
- **Difference**: Lines that have duplicate words were already caught in Part 1, but Part 2 also catches anagrams that aren't exact duplicates

## Success Criteria
The solution is correct if:
1. ✅ All 5 provided examples produce correct output
2. ✅ Edge cases are handled properly
3. ✅ Full input produces a reasonable integer result
4. ✅ Result is strictly less than Part 1's answer (< 455)
5. ✅ No runtime errors or crashes occur
6. ✅ Performance is acceptable (< 100ms for full input)

## Debugging Strategy
If tests fail, use this approach:
1. **Add debug output**: Print sorted forms for failing test cases
2. **Manual verification**: Manually sort words for failing examples
3. **Check set logic**: Verify that duplicate sorted forms are being detected
4. **Boundary check**: Ensure comparison is `len(canonical) == len(set(canonical))`
5. **Input parsing**: Verify words are being split correctly on spaces
