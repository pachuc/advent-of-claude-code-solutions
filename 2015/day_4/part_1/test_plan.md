# Test Plan: AdventCoin Mining

## Testing Strategy Overview
Verify that the solution correctly finds the lowest positive integer that produces an MD5 hash starting with five hexadecimal zeroes when appended to the secret key.

## Test Categories

### 1. Example-Based Verification Tests
**Purpose**: Validate against known correct answers from problem statement

#### Test 1.1: Example with "abcdef"
```python
secret_key = "abcdef"
expected = 609043
```
- **Expected hash**: `abcdef609043` → MD5 starts with `000001dbbfa...`
- **Validation**:
  - Result equals 609043
  - Hash of `abcdef609043` starts with `00000`
  - Hash of `abcdef609042` does NOT start with `00000`

#### Test 1.2: Example with "pqrstuv"
```python
secret_key = "pqrstuv"
expected = 1048970
```
- **Expected hash**: `pqrstuv1048970` → MD5 starts with `000006136ef...`
- **Validation**:
  - Result equals 1048970
  - Hash of `pqrstuv1048970` starts with `00000`
  - Hash of `pqrstuv1048969` does NOT start with `00000`

#### Test 1.3: Actual Input "ckczppom"
```python
secret_key = "ckczppom"
```
- **Validation**:
  - Result is a positive integer
  - Hash of `ckczppom{result}` starts with `00000`
  - Hash of `ckczppom{result-1}` does NOT start with `00000`
  - Result is repeatable (deterministic)

### 2. Hash Correctness Tests
**Purpose**: Ensure MD5 hashing is implemented correctly

#### Test 2.1: Known MD5 Values
```python
test_cases = [
    ("hello", "5d41402abc4b2a76b9719d911017c592"),
    ("", "d41d8cd98f00b204e9800998ecf8427e"),
    ("The quick brown fox", "a2004f37730b9445670a738fa0fc9ee5")
]
```
- Verify `compute_md5_hex()` produces correct hashes

#### Test 2.2: Hash Format Validation
- Verify hash is exactly 32 characters long
- Verify hash contains only hexadecimal characters (0-9, a-f)
- Verify hash is lowercase

### 3. Prefix Checking Tests
**Purpose**: Ensure five-zero detection works correctly

#### Test 3.1: Positive Cases
```python
test_hashes = [
    "00000abcdef123456789012345678901",  # Exactly 5 zeroes
    "000000bcdef123456789012345678901",  # 6 zeroes (still valid)
    "00000000000000000000000000000000",  # All zeroes
]
```
- All should return `True` from `starts_with_five_zeroes()`

#### Test 3.2: Negative Cases
```python
test_hashes = [
    "0000abcdef1234567890123456789012",  # Only 4 zeroes - should return False
    "10000abcdef123456789012345678901",  # Starts with 1 - should return False
    "a0000abcdef123456789012345678901",  # Starts with 'a' - should return False
    "",                                  # Empty string - should return False
]
```
- All should return `False` from `starts_with_five_zeroes()`
- Note: In practice, MD5 always returns exactly 32 hex characters, so short strings won't occur in actual usage

### 4. Input Handling Tests
**Purpose**: Verify input parsing works correctly

#### Test 4.1: Whitespace Handling
```python
test_inputs = [
    "ckczppom\n",      # Trailing newline
    " ckczppom",       # Leading space
    "ckczppom ",       # Trailing space
    "  ckczppom  \n",  # Multiple whitespace
]
```
- All should be stripped to `"ckczppom"`

#### Test 4.2: Input File Reading
- Verify file `input.md` can be read
- Verify content is correctly extracted

### 5. Edge Cases and Boundary Conditions

#### Test 5.1: Small Numbers
- Verify algorithm starts at 1 (not 0)
- Check that numbers 1-10 are tested correctly

#### Test 5.2: String Concatenation and Conversion
```python
secret_key = "test"
number = 12345
combined = secret_key + str(number)
expected = "test12345"
```
- Verify `str(number)` produces correct string representation (e.g., "12345", not "12345.0")
- Verify concatenation produces correct string format
- No extra characters, spaces, or separators
- Test with various number sizes: 1, 99, 1000, 609043

#### Test 5.3: Large Numbers
- Verify algorithm can handle 6-7 digit numbers (based on examples)
- No integer overflow issues (Python handles arbitrary precision)

### 6. Determinism Test
**Purpose**: Ensure same input always produces same output

#### Test 6.1: Multiple Runs
- Run the solution 3 times with same input
- For efficiency: run once for each example, three times for actual input only if time permits
- Verify all runs produce identical results
- Confirms no randomness or state issues
- MD5 is deterministic, so this mainly verifies no unintended state between runs

### 7. Performance Validation
**Purpose**: Ensure solution completes in reasonable time

#### Test 7.1: Runtime Check
- Time the execution for actual input
- Expected: < 30 seconds (generous upper bound)
- If examples (609043, 1048970) complete in under 5 seconds each, expect actual solution in similar timeframe
- If exceeds 1 minute, investigate efficiency issues

#### Test 7.2: Progress Verification (Optional)
- Add counter to verify iterations are happening
- For answer around 600k, should iterate ~600k times

## Testing Implementation Approach

### Test Execution Order (Recommended)
For faster feedback during development, run tests in this order:
1. **Fast tests first** (~instant): MD5 correctness, prefix checking, input parsing
2. **Medium tests** (~1-5 seconds): Small examples or custom quick tests
3. **Slow tests** (~5-30 seconds): Full examples (abcdef, pqrstuv), actual input

This provides quick validation before running computationally expensive tests.

### Manual Testing Script
```python
import hashlib

def test_examples():
    """Test against known examples."""
    # Import the solution functions
    from solution import find_advent_coin, compute_md5_hex

    # Test example 1
    result1 = find_advent_coin("abcdef")
    assert result1 == 609043, f"Expected 609043, got {result1}"
    hash1 = compute_md5_hex("abcdef609043")
    assert hash1.startswith("00000"), f"Hash doesn't start with 00000: {hash1}"
    print("✓ Example 1 passed")

    # Test example 2
    result2 = find_advent_coin("pqrstuv")
    assert result2 == 1048970, f"Expected 1048970, got {result2}"
    hash2 = compute_md5_hex("pqrstuv1048970")
    assert hash2.startswith("00000"), f"Hash doesn't start with 00000: {hash2}"
    print("✓ Example 2 passed")

    print("All example tests passed!")

def test_md5_correctness():
    """Test MD5 implementation."""
    from solution import compute_md5_hex

    assert compute_md5_hex("hello") == "5d41402abc4b2a76b9719d911017c592"
    assert compute_md5_hex("") == "d41d8cd98f00b204e9800998ecf8427e"
    print("✓ MD5 correctness tests passed")

def test_actual_solution():
    """Test with actual input and verify properties."""
    from solution import find_advent_coin, compute_md5_hex, read_input

    secret_key = read_input()
    result = find_advent_coin(secret_key)

    # Verify result is positive
    assert result > 0, f"Result must be positive, got {result}"

    # Verify hash starts with 00000
    hash_result = compute_md5_hex(secret_key + str(result))
    assert hash_result.startswith("00000"), f"Hash doesn't start with 00000: {hash_result}"

    # Verify it's the lowest (previous number doesn't work)
    hash_prev = compute_md5_hex(secret_key + str(result - 1))
    assert not hash_prev.startswith("00000"), f"Previous number also works: {result-1}"

    print(f"✓ Actual solution: {result}")
    print(f"  Hash: {hash_result[:16]}... (full: {hash_result})")
    print(f"  Verified: {secret_key}{result} produces hash starting with 00000")

    return result

if __name__ == '__main__':
    test_md5_correctness()
    test_examples()
    result = test_actual_solution()
    print(f"\nFinal answer: {result}")
```

## Verification Checklist

- [ ] Solution produces correct answer for "abcdef" (609043)
- [ ] Solution produces correct answer for "pqrstuv" (1048970)
- [ ] MD5 hashing is correct (verified with known hashes)
- [ ] Hash starts with exactly "00000" (five zeroes)
- [ ] Previous number (answer - 1) does NOT produce valid hash
- [ ] Result is deterministic (same answer on multiple runs)
- [ ] Solution completes in reasonable time (< 30 seconds)
- [ ] Input is correctly read and whitespace stripped
- [ ] Actual input "ckczppom" produces a valid result

## Success Criteria

The solution is correct if:
1. Both example test cases pass (609043 and 1048970)
2. The actual input produces a positive integer result
3. The hash of `{secret_key}{result}` starts with "00000"
4. The hash of `{secret_key}{result-1}` does NOT start with "00000"
5. The result is repeatable across multiple runs
6. Execution completes in reasonable time

## Known Limitations (Acceptable for Script)

- No timeout handling (assumes answer exists)
- No progress output (would slow down execution)
- No validation of input file format (trusts input)
- No handling of malformed input (unnecessary for this problem)
- No unit test framework (manual testing sufficient)

## Optional Enhancement: Regression Testing

Once the actual answer is found, consider adding it as a hardcoded test case:
```python
def test_regression():
    """Prevent accidental bugs in future modifications."""
    from solution import find_advent_coin
    # Once answer is known, uncomment and add:
    # assert find_advent_coin("ckczppom") == KNOWN_ANSWER
```
This is low priority for a one-time script but useful if the code might be modified later.
