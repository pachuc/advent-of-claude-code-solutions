# Testing Plan: One-Time Pad Key Generation

## Overview
Comprehensive testing strategy to verify the correctness of the one-time pad key generation solution.

## Test Categories

### 1. Unit Tests - Individual Functions

#### Test 1.1: Hash Generation
**Function**: `generate_hash(salt, index)`

**Test Cases**:
1. **Basic hash generation**
   - Input: `salt="abc"`, `index=0`
   - Expected: Verify it produces a 32-character hex string
   - Verify: All characters in [0-9a-f]

2. **Hash uniqueness**
   - Generate hashes for `salt="abc"`, indices 0, 1, 2
   - Expected: All three hashes should be different

3. **Deterministic behavior**
   - Generate same hash twice: `salt="abc"`, `index=5`
   - Expected: Both calls produce identical output

4. **Problem example hash**
   - Input: `salt="abc"`, `index=39`
   - Verify: Hash contains triplet "eee" (use find_first_triplet to verify)
   - Note: Don't hardcode the exact hash; verify the triplet is present

#### Test 1.2: Triplet Detection
**Function**: `find_first_triplet(hash_str)`

**Test Cases**:
1. **Hash with no triplet**
   - Input: `"0123456789abcdef0123456789abcdef"`
   - Expected: `None`

2. **Hash with one triplet**
   - Input: `"abc77789def"`
   - Expected: `"7"`

3. **Hash with multiple triplets** (CRITICAL)
   - Input: `"aaa123bbb456"`
   - Expected: `"a"` (first triplet only)
   - Verify it doesn't return "b"

4. **Triplet at start**
   - Input: `"fff123456789"`
   - Expected: `"f"`

5. **Triplet at end**
   - Input: `"123456789ccc"`
   - Expected: `"c"`

6. **All same character**
   - Input: `"00000000000000000000000000000000"`
   - Expected: `"0"`

#### Test 1.3: Quintuplet Detection
**Function**: `contains_quintuplet(hash_str, char)`

**Test Cases**:
1. **Hash with quintuplet**
   - Input: `hash="abc88888def"`, `char="8"`
   - Expected: `True`

2. **Hash without quintuplet**
   - Input: `hash="abc8888def"`, `char="8"` (only 4)
   - Expected: `False`

3. **Hash with wrong character quintuplet**
   - Input: `hash="aaaaa123"`, `char="b"`
   - Expected: `False`

4. **Quintuplet with 6+ repetitions**
   - Input: `hash="00000000"`, `char="0"`
   - Expected: `True` (6 zeros contains 5)

### 2. Integration Tests - Function Combinations

#### Test 2.1: Hash Caching
**Function**: `get_hash(salt, index, cache)`

**Test Cases**:
1. **Cache miss then hit**
   - First call: `get_hash("abc", 5, cache)` - cache empty
   - Verify: Hash is generated and stored in cache
   - Second call: `get_hash("abc", 5, cache)`
   - Verify: Same hash returned without regeneration
   - Verify: Cache contains exactly one entry

2. **Multiple cache entries**
   - Generate hashes for indices 0, 1, 2
   - Verify: Cache has 3 entries
   - Verify: All entries are correct

#### Test 2.2: Key Validation Logic
**Function**: `is_valid_key(salt, index, hash_cache)`

**Test Cases**:
1. **Invalid - no triplet**
   - Create index where hash has no triplet
   - Expected: `False`

2. **Invalid - triplet but no quintuplet in range**
   - Example from problem: index 18 with salt "abc"
   - Expected: `False`

3. **Valid - triplet with quintuplet in range**
   - Example from problem: index 39 with salt "abc"
   - Expected: `True`
   - Verify: Cache is populated with hashes from range [40, 1039]

4. **Edge case - quintuplet at exact boundary**
   - If triplet at index N, quintuplet at index N+1000 (last position)
   - Expected: `True`

5. **Edge case - quintuplet at index N+1** (first position in range)
   - Expected: `True`

6. **Multiple triplets with only second quintuplet present** (CRITICAL)
   - Setup: Create scenario where hash at index N contains "aaa...bbb" (first triplet is 'a')
   - Setup: Indices [N+1, N+1000] contain "bbbbb" but no "aaaaa"
   - Expected: `False` (quintuplet must match FIRST triplet only)
   - Purpose: Verify implementation uses only the first triplet, not any triplet

7. **Quintuplet just outside range** (CRITICAL BOUNDARY TEST)
   - Setup: Index N has triplet 'e', no "eeeee" in [N+1, N+1000]
   - Setup: Index N+1001 has "eeeee"
   - Expected: `False` (outside the 1000-hash window)
   - Purpose: Verify range is exactly `range(index+1, index+1001)`

### 3. End-to-End Tests

#### Test 3.1: Example Validation
**Function**: `find_64th_key(salt)`

**Test Cases**:
1. **Known example from problem**
   - Input: `salt="abc"`
   - Expected: `22728`
   - **CRITICAL**: This is the primary validation test
   - Timeout: Allow up to 60 seconds for completion

2. **First few keys for "abc"**
   - Manually verify indices 39, 92 produce keys
   - Count first 5-10 keys and verify indices match expected pattern

#### Test 3.2: Actual Input
**Test Cases**:
1. **Production salt "ihaygndm"**
   - Run full solution
   - Verify: Returns an integer
   - Verify: Integer is positive
   - Performance expectations:
     - Expected time: 5-15 seconds (with proper caching)
     - Maximum acceptable: 60 seconds
     - If > 60 seconds: cache is likely not working correctly
   - Verify: Result is consistent across multiple runs

### 4. Edge Cases and Boundary Conditions

#### Test 4.1: Overlapping Validation Windows
**Scenario**: Index N is a key, index N+500 is also a key
- Verify: Both are counted as separate keys
- Verify: Keys_found counter increments correctly

#### Test 4.2: Sequential Triplets
**Scenario**: Hash contains "aaabbb"
- Verify: Only "a" is considered (first triplet)
- Verify: "b" is ignored

#### Test 4.3: Large Index Numbers
**Scenario**: Testing around index 20,000+
- Verify: String concatenation works correctly (e.g., "abc20000")
- Verify: No integer overflow issues
- Verify: Hash generation remains consistent

#### Test 4.4: Cache Memory Usage
**Scenario**: After finding 64 keys
- Verify: Cache size is reasonable (< 30,000 entries)
- Verify: No memory leaks or excessive growth

## Testing Execution Strategy

### Phase 1: Unit Testing (Bottom-Up)
1. Test `generate_hash()` - verify MD5 computation
2. Test `find_first_triplet()` - verify pattern detection
3. Test `contains_quintuplet()` - verify search logic
4. Run all unit tests, fix any failures

### Phase 2: Integration Testing
1. Test `get_hash()` with caching
2. Test `is_valid_key()` with sample indices
3. Verify cache behavior across multiple validations

### Phase 3: Example Validation (CRITICAL)
1. Run full solution with salt "abc"
2. Expected output: 22728
3. **If this fails, debug thoroughly before proceeding**
4. Add intermediate print statements to track:
   - Keys found counter
   - Indices where keys are found
   - First 5-10 key indices

### Phase 4: Production Run
1. Run with actual salt "ihaygndm"
2. Verify output is reasonable
3. Record execution time

## Verification Checklist

- [ ] Hash generation produces 32-char hex strings
- [ ] Triplet detection finds FIRST triplet only
- [ ] Quintuplet detection works for target character
- [ ] Cache prevents redundant hash computation
- [ ] Validation checks exactly 1000 future hashes using `range(index+1, index+1001)`
- [ ] Only FIRST triplet is used for quintuplet matching (not any triplet)
- [ ] Quintuplet at index+1001 does NOT validate (boundary test)
- [ ] Quintuplet at index+1000 DOES validate (boundary test)
- [ ] Key counter increments correctly
- [ ] Example input "abc" produces 22728
- [ ] Actual input produces valid integer result
- [ ] Execution completes in 5-15 seconds (expected), < 60 seconds (max)
- [ ] No crashes or exceptions during execution

## Debugging Strategy (If Tests Fail)

### If example test fails (abc != 22728):
1. Add logging for first 10 keys found
2. Compare with problem statement (index 39, 92, etc.)
3. Check off-by-one errors:
   - Range should be `range(index+1, index+1001)`
   - This produces [index+1, index+2, ..., index+1000] - exactly 1000 hashes
   - Common mistake: using `range(index+1, index+1000)` (only 999 hashes)
   - Common mistake: using `range(index+1, index+1001+1)` (1001 hashes)
4. Verify triplet detection returns first occurrence only
5. Verify only FIRST triplet is used for quintuplet matching
6. Print sample hashes to manually verify triplet/quintuplet

### If solution is too slow:
1. Verify cache is being used (not regenerating hashes)
2. Check for unnecessary iterations
3. Profile code to find bottleneck
4. Consider using compiled regex if needed

### If hash values seem wrong:
1. Verify encoding: should be UTF-8
2. Verify lowercase hexadecimal output
3. Test against online MD5 calculator with "abc0", "abc1", etc.

## Success Criteria
1. All unit tests pass
2. Example input "abc" returns 22728
3. Production input returns a consistent answer
4. Execution time < 2 minutes
5. No errors or exceptions during execution
