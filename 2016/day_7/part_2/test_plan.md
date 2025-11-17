# Test Plan: IPv7 SSL Support Detection (Part 2)

## Testing Strategy
We need to verify that the solution correctly identifies ABA/BAB patterns and determines SSL support according to the rules. Testing will focus on pattern detection accuracy, parsing correctness, and edge case handling.

## Test Categories

### 1. Basic Functionality Tests

#### Test 1.1: Simple Valid SSL Address
**Input**: `aba[bab]xyz`
**Expected**: Supports SSL (count = 1)
**Rationale**:
- ABA "aba" in supernet "aba"
- Corresponding BAB "bab" in hypernet "bab"
**Verification**: Parse sequences, verify ABA detection, verify BAB detection, confirm match

#### Test 1.2: Simple Invalid SSL Address (No Corresponding BAB)
**Input**: `xyx[xyx]xyx`
**Expected**: Does NOT support SSL (count = 0)
**Rationale**:
- ABA "xyx" exists in supernets
- BAB should be "yxy" but hypernet only contains "xyx"
**Verification**: Confirm ABA found, confirm BAB "yxy" NOT found

#### Test 1.3: Invalid ABA Pattern (Triple Character)
**Input**: `aaa[kek]eke`
**Expected**: Supports SSL (count = 1)
**Rationale**:
- "aaa" is NOT a valid ABA (middle char must differ)
- Valid ABA "eke" in supernet "eke"
- Corresponding BAB "kek" in hypernet "kek"
**Verification**: Confirm "aaa" ignored, "eke" detected, match with "kek"

#### Test 1.4: Overlapping ABA Patterns
**Input**: `zazbz[bzb]cdb`
**Expected**: Supports SSL (count = 1)
**Rationale**:
- Supernet "zazbz" contains overlapping ABAs: "zaz" (positions 0-2) and "zbz" (positions 2-4)
- Hypernet "bzb" matches BAB for "zbz" ABA
**Verification**: Confirm both "zaz" and "zbz" detected, "bzb" matches "zbz"

### 2. Pattern Detection Tests

#### Test 2.1: Multiple ABAs in Single Sequence
**Input**: `xyzyx[nothing]test`
**Expected**: Does NOT support SSL (count = 0)
**Rationale**:
- "xyzyx" contains two ABAs: "xyx" and "yxy"
- No matching BABs in hypernet
**Verification**: Confirm both ABAs detected, no matches found

#### Test 2.2: Multiple Sequences with Multiple Patterns
**Input**: `aba[bab]cdc[dcd]efe`
**Expected**: Supports SSL (count = 1)
**Rationale**:
- Supernet sequences: "aba", "cdc", "efe"
- Supernet ABAs: "aba", "cdc", "efe"
- Hypernet sequences: "bab", "dcd"
- Hypernet ABAs (which are BABs): "bab", "dcd"
- Corresponding BABs for supernet ABAs: "aba" → "bab", "cdc" → "dcd", "efe" → "fef"
- Matches found: "bab" matches, "dcd" matches (either one makes it valid)
**Verification**: Confirms handling of multiple sequences with multiple ABA/BAB pairs

#### Test 2.3: ABA at Sequence Boundaries
**Input**: `aba[test]xyz`
**Expected**: Check based on actual patterns
**Rationale**: Verify ABA detection works at start/end of sequences

### 3. Parsing Tests

#### Test 3.1: No Hypernet Sequences
**Input**: `abcdefghijk`
**Expected**: Does NOT support SSL (count = 0)
**Rationale**: No hypernet means no place for BAB to exist
**Verification**: Confirm supernets parsed correctly, hypernets empty

#### Test 3.2: Multiple Hypernet Sequences
**Input**: `abc[def]ghi[jkl]mno[pqr]stu`
**Expected Parse Result**:
- Supernets: ["abc", "ghi", "mno", "stu"] (4 sequences)
- Hypernets: ["def", "jkl", "pqr"] (3 sequences)
**Rationale**: Verify parser handles multiple alternating sequences
**Verification**: Manually verify `parse_address()` returns these exact lists

#### Test 3.3: Empty Sequences Between Brackets
**Input**: `abc[]def[ghi]jkl`
**Expected**: Parser handles gracefully
**Rationale**: Edge case for parsing logic
**Verification**: Confirm empty hypernet doesn't cause errors

#### Test 3.4: Consecutive Brackets
**Input**: `abc[def][ghi]jkl`
**Expected**: Parser handles as separate hypernets
**Rationale**: Edge case testing
**Verification**: Confirm two hypernet sequences, supernets between

### 4. Edge Cases

#### Test 4.1: Minimum Length Sequences
**Input**: `ab[cd]ef`
**Expected**: Does NOT support SSL (count = 0)
**Rationale**: All sequences are length 2, cannot contain 3-char ABAs
**Verification**: Confirm no ABAs found

#### Test 4.2: Exact 3-Character Sequences
**Input**: `aba[bab]cdc`
**Expected**: Supports SSL (count = 1)
**Rationale**: Sequences are exactly 3 chars (minimum for ABA)
**Verification**: Confirm ABAs detected in minimal sequences

#### Test 4.3: Very Long Sequence with Many Patterns
**Input**: `abacadaeafaga[babcadaeafaga]test`
**Expected**: Check for matches
**Rationale**: Stress test pattern detection with many overlapping ABAs
**Verification**: Verify all ABAs found, performance acceptable

#### Test 4.4: All Same Character
**Input**: `aaaaaaa[bbbbbbb]ccccccc`
**Expected**: Does NOT support SSL (count = 0)
**Rationale**: No valid ABAs (all would have same inner/outer chars)
**Verification**: Confirm no ABAs detected

#### Test 4.5: No Matching BAB
**Input**: `xyz[abc]def`
**Expected**: Does NOT support SSL (count = 0)
**Rationale**:
- Supernet ABAs: "xyx" (from "xyz"), "efe" (from "def")
- Actually "xyz" gives no ABAs, "def" gives no ABAs (no valid ABA patterns)
- No ABAs means no SSL support
**Verification**: Confirm sequences with no valid patterns return false
**Note**: Removed case sensitivity test as typical Advent of Code input is lowercase only

### 5. Integration Tests with Actual Input

#### Test 5.1: Sample of Real Input Lines
**Approach**:
1. Extract first 10 lines from input.md
2. Manually verify expected SSL support for each
3. Run solution and compare counts
**Verification**: Manual calculation vs automated result

#### Test 5.2: Full Input Processing
**Approach**:
1. Run solution on complete input.md
2. Verify no errors/crashes
3. Result is positive integer
4. Execution time < 1 second (efficiency check - algorithm should be very fast)
**Verification**: Solution completes successfully and efficiently

#### Test 5.3: Count Sanity Check
**Expected Range**: Between 1 and 2000 (some but not all addresses support SSL)
**Rationale**: Extremely unlikely to be 0 or 2000
**Verification**: Final answer is reasonable

### 6. Correctness Verification Tests

#### Test 6.1: Manual Verification of Examples
For each example in problem.md:
- `aba[bab]xyz` → Should return True (supports SSL)
- `xyx[xyx]xyx` → Should return False
- `aaa[kek]eke` → Should return True
- `zazbz[bzb]cdb` → Should return True

**Approach**: Create small test file with just these 4 lines
**Expected**: count = 3 (three support SSL)
**Verification**: Direct comparison with problem statement

#### Test 6.2: ABA to BAB Conversion Verification
**Test Cases**:
- "aba" → "bab" ✓
- "xyx" → "yxy" ✓
- "eke" → "kek" ✓
- "zbz" → "bzb" ✓

**Approach**: Unit test the `aba_to_bab()` function
**Verification**: All conversions match expected output

#### Test 6.3: ABA Detection Verification

**Test Cases for `find_abas()` function**:

1. **Test Sequence**: "zazbz"
   - **Expected ABAs**: {"zaz", "zbz"}
   - **Verification**: Set equality check

2. **Test Sequence**: "aaaa"
   - **Expected ABAs**: {} (empty set)
   - **Verification**: No invalid ABAs detected (all same char)

3. **Test Sequence**: "" (empty string)
   - **Expected ABAs**: set()
   - **Verification**: Handles empty input without error

4. **Test Sequence**: "ab" (too short)
   - **Expected ABAs**: set()
   - **Verification**: Sequences shorter than 3 return empty set

5. **Test Sequence**: "abcdef" (no palindromes)
   - **Expected ABAs**: set()
   - **Verification**: No ABAs when no valid patterns exist

6. **Test Sequence**: "aba" (exact 3 chars)
   - **Expected ABAs**: {"aba"}
   - **Verification**: Minimal valid case works

**Approach**: Unit test `find_abas()` function with all cases above

### 7. Comparison Tests

#### Test 7.1: Different Result from Part 1
**Approach**:
- Part 1 answer was 118 (TLS support)
- Part 2 should be different (SSL uses different rules)
- Verify final count ≠ 118
**Rationale**: Different patterns mean different counts
**Verification**: Answers differ

#### Test 7.2: Some Overlap Expected
**Approach**: Manually find 2-3 addresses that support BOTH TLS and SSL
**Rationale**: Some addresses may satisfy both criteria
**Verification**: Understanding that SSL and TLS are independent checks

## Testing Execution Plan

### Phase 1: Unit Tests
**Approach**: For a puzzle-solving script, use simple assertion blocks or manual Python REPL testing

1. **Test `aba_to_bab()` with manual conversions**:
   - Create simple test cases: assert aba_to_bab("aba") == "bab"
   - Test all examples from problem.md
   - Can be verified via Python REPL or assertion block

2. **Test `find_abas()` with known sequences**:
   - Test all cases from Test 6.3 above
   - Use assertion blocks or manual verification
   - Verify empty inputs, short inputs, valid patterns, invalid patterns

3. **Test `parse_address()` (reused from Part 1)**:
   - Should work as-is from Part 1
   - Quick spot check with one test case to confirm

### Phase 2: Function Tests
1. Test `supports_ssl()` with problem.md examples
2. Create small test file with 4 example addresses
3. Verify count = 3

### Phase 3: Edge Case Tests
1. Run edge case inputs (empty, short, long sequences)
2. Verify no crashes or errors
3. Confirm logical outputs

### Phase 4: Full Integration
1. Run on complete input.md
2. Verify result is reasonable (1 < count < 2000)
3. Verify execution time acceptable
4. Verify result ≠ 118 (different from Part 1)

### Phase 5: Manual Validation
1. Pick 5 random addresses from input
2. Manually trace through SSL logic
3. Confirm solution produces correct results

## Success Criteria
- All problem.md examples produce correct results (3 out of 4 should support SSL)
- No errors/crashes on full input
- Solution completes in < 1 second (should be much faster with ~100K operations)
- Final count is reasonable positive integer (between 1 and 2000)
- Final count differs from Part 1 answer (118) - different algorithm means different result
- Manual verification of sample addresses confirms correctness
- Edge cases handled gracefully (empty strings, short sequences, no patterns)

## Debugging Strategy
If tests fail:
1. **Wrong count on examples**: Debug `supports_ssl()` logic, verify ABA/BAB detection
2. **Parsing errors**: Check `parse_address()` with problematic address
3. **Pattern detection issues**: Debug `find_abas()` with verbose output
4. **Performance issues**: Profile code, check for unnecessary loops
5. **Off-by-one errors**: Verify sliding window indices (i to i+3)
