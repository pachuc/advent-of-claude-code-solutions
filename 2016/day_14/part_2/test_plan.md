# Test Plan: One-Time Pad Key Generation with Key Stretching (Part 2)

## Testing Objectives
1. Verify key stretching is implemented correctly (2017 total MD5 operations)
2. Ensure validation logic still works correctly with stretched hashes
3. Confirm the solution produces the correct answer for the given input
4. Validate performance is acceptable despite increased computational cost

## Test Categories

### 1. Key Stretching Correctness Tests

#### Test 1.1: Verify Single Hash Stretching
**Purpose**: Confirm the key stretching algorithm produces correct output

**Test case**:
```python
salt = 'abc'
index = 0
expected_initial = '577571be4de9dcce85a041ba0410f29f'
expected_final = 'a107ff634856bb300138cac6568c0f24'
```

**Procedure**:
1. Compute MD5('abc0')
2. Verify initial hash matches expected_initial
3. Apply 2016 additional MD5 iterations
4. Verify final result matches expected_final

**Success criteria**: Both intermediate and final hash match expected values

**Why this matters**: This is the core algorithm change; if this is wrong, everything fails

#### Test 1.2: Verify Iteration Count (Optional)
**Purpose**: Ensure exactly 2017 MD5 operations are performed

**Test case**:
```python
# Instrument the code to count MD5 calls
# Should be exactly 2017 per hash generation
```

**Procedure**:
1. Add a counter to track MD5 operations
2. Generate one stretched hash
3. Verify counter equals 2017

**Success criteria**: Exactly 2017 MD5 operations

**Why this matters**: Off-by-one errors would produce wrong results

**Note**: This test requires code instrumentation. Test 1.1 (output verification) already validates correctness, so this is confirmatory rather than essential.

#### Test 1.3: Lowercase Hexadecimal Output
**Purpose**: Verify hash format matches requirements

**Test case**:
```python
# All output should be lowercase hex
assert all(c in '0123456789abcdef' for c in stretched_hash)
assert stretched_hash == stretched_hash.lower()
```

**Success criteria**: All characters are lowercase hexadecimal

### 2. Validation Logic Tests

#### Test 2.1: Triplet Detection Still Works
**Purpose**: Ensure triplet finding works with stretched hashes

**Test case**:
```python
# Use salt='abc' with stretching
# Index 10 should have triplet 'eee'
hash_10 = generate_stretched_hash('abc', 10)
triplet = find_first_triplet(hash_10)
assert triplet == 'e'
```

**Success criteria**: Correct triplet character identified

#### Test 2.2: Quintuplet Detection Still Works
**Purpose**: Verify quintuplet checking works correctly

**Test case**:
```python
# Index 89 with salt='abc' should contain 'eeeee'
hash_89 = generate_stretched_hash('abc', 89)
assert contains_quintuplet(hash_89, 'e') == True
```

**Success criteria**: Quintuplet correctly detected

#### Test 2.3: First Key Detection
**Purpose**: Verify the first valid key is found correctly

**Test case**:
```python
# With salt='abc' and stretching:
# First key should be at index 10 (triplet 'eee', quintuplet at 89)
salt = 'abc'
# Check that index 10 is detected as a valid key
```

**Success criteria**: Index 10 is correctly identified as the first key

### 3. End-to-End Validation Tests

#### Test 3.1: Example Salt Verification
**Purpose**: Verify solution works on the provided example

**Test case**:
```python
salt = 'abc'
expected_64th_key = 22551
result = find_64th_key(salt)
assert result == expected_64th_key
```

**Success criteria**: Returns 22551 for salt 'abc'

**Why this matters**: This is the provided example; if this fails, implementation is wrong

**Note**: This is the MOST IMPORTANT test - if this passes, high confidence in correctness

#### Test 3.2: Actual Input Solution
**Purpose**: Get the answer for the actual puzzle input

**Test case**:
```python
salt = 'ihaygndm'
result = find_64th_key(salt)
# Result should be different from Part 1 answer (15035)
assert result != 15035
```

**Success criteria**:
- Returns an integer
- Different from Part 1 answer
- Completes in reasonable time (< 5 minutes)

#### Test 3.3: Comparison with Part 1 (Optional)
**Purpose**: Verify Part 2 produces different results due to key stretching

**Test case**:
```python
# Generate same index hash with and without stretching
hash_unstretched = generate_hash('ihaygndm', 0)  # Part 1
hash_stretched = generate_stretched_hash('ihaygndm', 0)  # Part 2
assert hash_unstretched != hash_stretched
```

**Success criteria**: Hashes are different, confirming stretching is active

**Note**: Requires keeping Part 1's generate_hash() function or reimplementing it. Nice sanity check but not critical.

### 4. Performance and Caching Tests

#### Test 4.1: Cache Effectiveness
**Purpose**: Verify caching prevents redundant computation

**Test case**:
```python
# Check that hash for same index is only computed once
cache = {}
hash1 = get_hash('abc', 100, cache)
# Should retrieve from cache on second call (not recompute)
hash2 = get_hash('abc', 100, cache)
assert hash1 is hash2  # Same object reference
assert len(cache) == 1
```

**Success criteria**: Cache is populated and reused

#### Test 4.2: Memory Usage Reasonable
**Purpose**: Ensure cache doesn't consume excessive memory

**Test case**:
```python
# After finding 64th key, cache size should be reasonable
# Approximately 25,000 entries * ~50 bytes = ~1.25 MB
assert len(hash_cache) < 30000
```

**Success criteria**: Cache size is reasonable (< 30k entries)

#### Test 4.3: Runtime Performance
**Purpose**: Verify solution completes in acceptable time

**Test case**:
```python
import time
start = time.time()
result = find_64th_key('ihaygndm')
elapsed = time.time() - start
assert elapsed < 300  # Should complete within 5 minutes
```

**Success criteria**: Completes within 5 minutes

### 5. Edge Case Tests

#### Test 5.1: Triplet at Hash Boundaries
**Purpose**: Verify triplet detection at start/end of hash

**Test case**:
```python
# Test hash starting with triplet: "aaab123..."
# Test hash ending with triplet: "...123bbb"
# Both should correctly identify the triplet
```

**Success criteria**: Triplets detected regardless of position

**Note**: Since we're using real MD5 hashes, need to find actual examples in the search rather than constructing test cases. This is covered by the comprehensive example test (3.1).

#### Test 5.2: Multiple Triplets in One Hash
**Purpose**: Verify only FIRST triplet is used

**Test case**:
```python
# Create/find hash with multiple triplets
# Verify only first one is used for quintuplet matching
```

**Success criteria**: First triplet takes precedence

#### Test 5.3: Hash That Is Both Key and Confirmation
**Purpose**: Verify hash can serve dual purposes

**Test case**:
```python
# A hash at index N could:
# 1. Be a valid key (has triplet + quintuplet in next 1000)
# 2. Contain quintuplet confirming earlier key
# Both should be handled correctly
```

**Success criteria**: No indices are skipped; all are checked

## Testing Execution Order

### Phase 1: Unit Tests (Fast)
1. Test 1.1: Key stretching correctness ⭐ CRITICAL
2. Test 1.2: Iteration count
3. Test 1.3: Output format
4. Test 2.1: Triplet detection
5. Test 2.2: Quintuplet detection

**Expected time**: < 1 minute
**Gate**: Must pass before proceeding

### Phase 2: Integration Tests (Medium)
1. Test 2.3: First key detection (may take 30-60 seconds for indices 0-89)
2. Test 4.1: Cache effectiveness
3. Test 3.3: Part 1 vs Part 2 difference (optional)

**Expected time**: 1-2 minutes
**Gate**: Must pass before full solution

### Phase 3: End-to-End Tests (Slow)
1. Test 3.1: Example salt verification ⭐ CRITICAL
2. Test 3.2: Actual input solution ⭐ FINAL ANSWER

**Expected time**: 2-5 minutes each
**Gate**: Test 3.1 must pass before trusting Test 3.2 result

### Phase 4: Validation Tests (Optional)
1. Test 4.2: Memory usage
2. Test 4.3: Runtime performance
3. Test 5.1-5.3: Edge cases

**Expected time**: Variable
**Gate**: Nice to have but not critical for correctness

## Success Criteria Summary

### Minimum Viable Tests (Must Pass)
1. ✅ Test 1.1: Key stretching produces correct hash for 'abc' index 0
2. ✅ Test 3.1: Returns 22551 for salt 'abc' (64th key)
3. ✅ Test 3.2: Returns valid answer for salt 'ihaygndm' (different from 15035)

### Confidence Tests (Should Pass)
1. ✅ Test 2.3: First key correctly identified for example salt
2. ✅ Test 4.1: Caching works correctly
3. ✅ Test 1.2: Exactly 2017 MD5 operations per hash (optional - requires instrumentation)

### Quality Tests (Nice to Have)
1. ✅ All edge case tests pass
2. ✅ Performance within acceptable bounds
3. ✅ Memory usage reasonable

## Debugging Strategy

### If Test 1.1 Fails (Key Stretching)
- Check iteration count (should be 2016 additional, 2017 total)
- Verify encoding (should be UTF-8)
- Verify hexdigest format (lowercase)
- Check if hashing the string or bytes correctly

### If Test 3.1 Fails (Example Salt)
- Verify key stretching first (Test 1.1)
- Manually check first few keys
- Compare triplet/quintuplet logic with Part 1
- Verify lookahead window is [index+1, index+1000]

### If Test 3.2 Times Out
- Expected behavior (key stretching is expensive)
- Verify caching is working (Test 4.1)
- Consider if machine is particularly slow
- Wait up to 5 minutes before concluding failure

## Test Implementation Approach

Since this is a script for solving a puzzle (not production code):
1. **Primary validation**: Run with example salt 'abc', verify returns 22551 (GOLD STANDARD)
2. **Secondary validation**: Run with actual input 'ihaygndm', get answer
3. **Spot checks**: Manually verify first stretched hash (abc0 → a107ff...24) before full run
4. **No formal test framework needed**: Direct assertions in code or manual verification
5. **Focus on correctness over coverage**: The example test is the gold standard
6. **Pragmatic approach**: If example test passes, very high confidence in implementation correctness

## Expected Final Output

For input 'ihaygndm':
- Output: Single integer (the 64th key index with key stretching)
- Format: Plain integer, no formatting
- Verification: Different from Part 1 answer (15035)
- Likely range: 20,000-25,000 based on example pattern
