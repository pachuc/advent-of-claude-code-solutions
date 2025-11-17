# Testing Plan: AdventCoin Mining (Part 2)

## Testing Objectives
1. Verify the algorithm correctly identifies MD5 hashes starting with six zeroes
2. Ensure the solution finds the *lowest* positive integer
3. Validate the solution works with the given input
4. Check edge cases and correctness of hash computation

## Test Strategy

### 1. Unit Tests

#### Test 1.1: MD5 Hash Computation Correctness
**Purpose**: Verify MD5 hash is computed correctly

**Test cases**:
```python
# Known MD5 hash values
test_cases = [
    ("", "d41d8cd98f00b204e9800998ecf8427e"),
    ("test", "098f6bcd4621d373cade4e832627b4f6"),
    ("hello", "5d41402abc4b2a76b9719d911017c592"),
]
```

**Validation**:
- Compare computed hash with known correct values
- Ensures hashlib is being used correctly
- These are standard test vectors for MD5

#### Test 1.2: Hex String Prefix Checking
**Purpose**: Verify the prefix checking logic works correctly

**Test cases**:
```python
test_cases = [
    ("000000abcdef", 6, True),   # Exactly 6 zeroes
    ("0000000abcdef", 6, True),  # More than 6 zeroes
    ("00000abcdef", 6, False),   # Only 5 zeroes
    ("100000abcdef", 6, False),  # Doesn't start with zero
]
```

**Validation**:
- Test boundary conditions (exactly 6, more than 6, less than 6)
- Ensure `startswith('000000')` logic is correct

#### Test 1.3: Integer Sequencing
**Purpose**: Verify we start from 1 and increment correctly

**Test cases**:
- Ensure first candidate is 1 (not 0)
- Ensure sequential increment without skips
- Mock the hash check to verify iteration order

### 2. Integration Tests

#### Test 2.1: Known Examples from Part 1
**Purpose**: Verify the algorithm works with known examples (using 5 zeroes)

**Test cases**:
```python
# From Advent of Code 2015 Day 4 Part 1 examples
test_cases = [
    ("abcdef", 5, 609043),   # abcdef609043 -> hash starts with 00000
    ("pqrstuv", 5, 1048970), # pqrstuv1048970 -> hash starts with 00000
]
```

**Validation**:
- Run algorithm with `num_zeroes=5` on known examples
- Verify we get the expected answers
- Confirms our algorithm logic is correct

#### Test 2.2: Small Search Space Test
**Purpose**: Test with a modified condition to verify search works

**Test case**:
```python
# Find hash starting with just "00" (2 zeroes) - should be very fast
secret_key = "ckczppom"
result = find_adventcoin(secret_key, num_zeroes=2)
```

**Validation**:
- Should complete very quickly (within seconds)
- Manually verify the result produces a hash starting with "00"
- Confirms the search loop terminates correctly

### 3. Functional Tests

#### Test 3.1: Main Problem Solution
**Purpose**: Solve the actual problem with the given input

**Steps**:
1. Run the solution with input "ckczppom" and 6 zeroes
2. Record the answer (let's call it `n`)
3. Verify: `MD5(ckczppom + n)` starts with "000000"
4. Verify: `MD5(ckczppom + (n-1))` does NOT start with "000000"

**Validation**:
- The answer produces a hash with 6+ leading zeroes
- The integer immediately before (n-1) does NOT satisfy the condition
- This confirms we found the *lowest* integer satisfying the condition

#### Test 3.2: Hash Format Verification
**Purpose**: Ensure hash is in correct hexadecimal format

**Validation**:
- Hash should be 32 characters long (MD5 produces 128 bits = 32 hex chars)
- Hash should only contain valid hex characters (0-9, a-f)
- Hash should be lowercase (default for `hexdigest()`)

### 4. Edge Cases

#### Test 4.1: Input Parsing
**Purpose**: Verify input is read correctly

**Test cases**:
- Input with trailing newline: `"ckczppom\n"` → should strip to `"ckczppom"`
- Input with spaces: `" ckczppom "` → should strip to `"ckczppom"`
- Input with multiple lines → should handle gracefully

**Validation**:
- Use `.strip()` to remove whitespace
- Verify no extra characters in concatenated string

### 5. Performance Tests

#### Test 5.1: Runtime Measurement
**Purpose**: Ensure solution completes in reasonable time

**Test**:
```python
import time
start = time.time()
result = find_adventcoin(secret_key, num_zeroes=6)
end = time.time()
print(f"Time taken: {end - start} seconds")
```

**Expected**:
- Should complete within 2-5 minutes on modern hardware, up to 10 minutes on slower CPUs
- If taking significantly longer than 10 minutes, investigate optimization issues

#### Test 5.2: Progress Monitoring (Optional)
**Purpose**: Monitor progress during long-running execution

**Test**:
```python
# Add progress printing every 100,000 iterations
if n % 100000 == 0:
    print(f"Checked {n} candidates...")
```

**Validation**:
- Ensures the loop is progressing
- Helps identify if stuck or making progress

### 6. Consistency Verification

#### Test 6.1: Determinism Check
**Purpose**: Verify multiple runs produce identical results

**Test**:
- Run the solution 2-3 times
- Verify the same answer each time
- MD5 is deterministic, so results must be identical

**Validation**:
- Confirms implementation is deterministic
- Rules out any potential randomness or non-deterministic behavior

### 7. Manual Verification Steps

#### Final Verification Checklist:
1. ✓ Read the final answer from program output
2. ✓ Manually compute MD5 of `ckczppom{answer}` using online MD5 calculator or separate script
3. ✓ Verify the hash starts with exactly "000000" (six zeroes)
4. ✓ Count the leading zeroes (should be at least 6)
5. ✓ Test answer - 1 to ensure it doesn't have 6 leading zeroes
6. ✓ Submit answer to Advent of Code (if applicable)

## Test Execution Order and Priority

### Essential Tests (MUST RUN)
1. **Test 2.1**: Integration test with known examples (abcdef, pqrstuv with 5 zeroes)
   - Fast validation that algorithm logic is correct
   - Uses known-good test data from Part 1
2. **Test 3.1**: Functional test - solve actual problem and verify n and n-1
   - Primary verification of correctness
   - Confirms we found the *lowest* integer

### Recommended Tests (SHOULD RUN)
3. **Test 2.2**: Small search space test (2 zeroes)
   - Quick verification that search loop works correctly
   - Completes in seconds
4. **Test 4.1**: Input parsing edge cases
   - Ensures whitespace handling works
5. **Manual Verification (Section 7)**: Double-check the answer

### Optional Tests
6. **Test 1.1-1.3**: Unit tests for hash computation and prefix checking
   - Useful for thoroughness but less critical for a puzzle script
7. **Test 5.1**: Runtime measurement
8. **Test 6.1**: Consistency verification

## Test Data Required

1. **Input file**: `input.md` with content "ckczppom"
2. **Known examples**: From AoC 2015 Day 4 Part 1 (abcdef, pqrstuv)
3. **Manual verification tools**: Online MD5 calculator or Python REPL

## Success Criteria

### Critical Requirements
- ✓ Known examples (Part 1) produce correct answers (Test 2.1)
- ✓ Final answer produces a hash starting with "000000" (Test 3.1)
- ✓ Final answer - 1 does NOT produce a hash starting with "000000" (Test 3.1)
- ✓ Solution completes in reasonable time (< 10 minutes on modern hardware)

### Verification Requirements
- ✓ Multiple runs produce identical results
- ✓ Hash is properly formatted (32 hex characters, lowercase)
- ✓ Input parsing handles whitespace correctly

## Test Implementation Notes

Tests can be implemented in a separate `test_solution.py` file using pytest or unittest, or can be simple verification scripts. Given the scope (solving a puzzle, not production code), simple verification functions are sufficient.
