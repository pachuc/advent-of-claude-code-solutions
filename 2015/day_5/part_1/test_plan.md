# Testing Plan: String Classification (Nice vs Naughty)

## Testing Strategy Overview

We need to verify correctness of:
1. Individual classification functions (unit tests)
2. Combined classification logic (integration tests)
3. File reading and counting (end-to-end tests)
4. Edge cases and boundary conditions

## Test Levels

### Level 1: Unit Tests for Individual Functions

#### Test 1.1: `has_three_vowels()` Function

**Test cases**:

| Input | Expected | Reason |
|-------|----------|--------|
| `"aei"` | True | Exactly 3 vowels |
| `"xazegov"` | True | Exactly 3 vowels (a,e,o) |
| `"aeiouaeiou"` | True | Many vowels (10 total) |
| `"aaa"` | True | Same vowel repeated (counts each) |
| `"aeiobcd"` | True | 4 vowels (a,e,i,o) |
| `"dvszwmarrgswjxmb"` | False | Only 1 vowel (a) |
| `"bcdfghjklmnpqrstvwxyz"` | False | No vowels |
| `"ae"` | False | Only 2 vowels |
| `"xyz"` | False | No vowels |
| `""` | False | Empty string |
| `"a"` | False | Single vowel |

**Validation method**:
```python
def test_has_three_vowels():
    assert has_three_vowels("aei") == True
    assert has_three_vowels("xazegov") == True  # a, e, o = 3
    assert has_three_vowels("aeiouaeiou") == True  # 10 vowels
    assert has_three_vowels("aaa") == True  # 3 same vowels
    assert has_three_vowels("aeiobcd") == True  # 4 vowels
    assert has_three_vowels("dvszwmarrgswjxmb") == False  # only 1
    assert has_three_vowels("bcdfghjklmnpqrstvwxyz") == False  # none
    assert has_three_vowels("ae") == False  # only 2
    assert has_three_vowels("xyz") == False  # none
    print("✓ has_three_vowels tests passed")
```

**Note**: Empty string test omitted here because the input reader filters empty lines. The functions should still handle empty strings gracefully (returning False) if called directly.

#### Test 1.2: `has_double_letter()` Function

**Test cases**:

| Input | Expected | Reason |
|-------|----------|--------|
| `"xx"` | True | Simple double |
| `"abcdde"` | True | Double in middle |
| `"aabbccdd"` | True | Multiple doubles (first one counts) |
| `"aaa"` | True | Triple (contains double) |
| `"abc"` | False | No doubles |
| `"abcdefg"` | False | All unique consecutive |
| `"a"` | False | Single character |
| `""` | False | Empty string |
| `"abcdefghijklmnopqrstuvwxyz"` | False | All alphabet, no doubles |

**Validation method**:
```python
def test_has_double_letter():
    assert has_double_letter("xx") == True
    assert has_double_letter("abcdde") == True
    assert has_double_letter("aabbccdd") == True
    assert has_double_letter("aaa") == True
    assert has_double_letter("abc") == False
    assert has_double_letter("abcdefg") == False
    assert has_double_letter("a") == False
    assert has_double_letter("") == False
    print("✓ has_double_letter tests passed")
```

#### Test 1.3: `no_forbidden_substrings()` Function

**Test cases**:

| Input | Expected | Reason |
|-------|----------|--------|
| `"hello"` | True | No forbidden substrings |
| `"abcde"` | False | Contains "ab" and "cd" |
| `"xyz"` | False | Contains "xy" |
| `"pqrst"` | False | Contains "pq" |
| `"cdrom"` | False | Contains "cd" |
| `"xylem"` | False | Contains "xy" |
| `"aeiou"` | True | Vowels only, no forbidden |
| `"bcefghij"` | True | No forbidden patterns |
| `"aa"` | True | Double letter but no forbidden |
| `"ba"` | True | Reverse of "ab" is okay |
| `"dc"` | True | Reverse of "cd" is okay |
| `"qp"` | True | Reverse of "pq" is okay |
| `"yx"` | True | Reverse of "xy" is okay |

**Validation method**:
```python
def test_no_forbidden_substrings():
    assert no_forbidden_substrings("hello") == True
    assert no_forbidden_substrings("abcde") == False
    assert no_forbidden_substrings("xyz") == False
    assert no_forbidden_substrings("pqrst") == False
    assert no_forbidden_substrings("cdrom") == False
    assert no_forbidden_substrings("ba") == True
    assert no_forbidden_substrings("dc") == True
    assert no_forbidden_substrings("qp") == True
    assert no_forbidden_substrings("yx") == True
    print("✓ no_forbidden_substrings tests passed")
```

### Level 2: Integration Tests for `is_nice()` Function

#### Test 2.1: Known Examples from Problem Statement

**Test cases from problem**:

| Input | Expected | Reason |
|-------|----------|--------|
| `"ugknbfddgicrmopn"` | True | 3+ vowels (u,i,o), double (dd), no forbidden |
| `"aaa"` | True | 3+ vowels (aaa), double (aa), no forbidden |
| `"jchzalrnumimnmhp"` | False | Has vowels but NO double letter |
| `"haegwjzuvuyypxyu"` | False | Has vowels and double (yy) but contains "xy" |
| `"dvszwmarrgswjxmb"` | False | Only 1 vowel (needs 3+) |

**Validation method**:
```python
def test_is_nice_known_examples():
    # Nice examples
    assert is_nice("ugknbfddgicrmopn") == True
    assert is_nice("aaa") == True

    # Naughty examples
    assert is_nice("jchzalrnumimnmhp") == False  # no double
    assert is_nice("haegwjzuvuyypxyu") == False  # has xy
    assert is_nice("dvszwmarrgswjxmb") == False  # only 1 vowel

    print("✓ Known examples tests passed")
```

#### Test 2.2: Edge Cases for Combined Logic

**Test cases**:

| Input | Vowels? | Double? | No Forbidden? | Nice? | Notes |
|-------|---------|---------|---------------|-------|-------|
| `"aabbcc"` | False | True | True | False | Missing vowel criterion |
| `"aeiou"` | True | False | True | False | Missing double criterion |
| `"aaabbb"` | True | True | False | False | Has "ab" forbidden |
| `"eee"` | True | True | True | True | All checks pass |
| `"iii"` | True | True | True | True | All checks pass |
| `"ooo"` | True | True | True | True | All checks pass |
| `"uuu"` | True | True | True | True | All checks pass |
| `"xyzzaeiou"` | True | True | False | False | Has "xy" despite other passes |

**Validation method**:
```python
def test_is_nice_edge_cases():
    assert is_nice("aabbcc") == False  # no vowels
    assert is_nice("aeiou") == False   # no double
    assert is_nice("aaabbb") == False  # has ab
    assert is_nice("eee") == True      # all pass
    assert is_nice("iii") == True      # all pass
    assert is_nice("ooo") == True      # all pass
    assert is_nice("uuu") == True      # all pass
    assert is_nice("xyzzaeiou") == False  # has xy
    print("✓ Edge cases tests passed")
```

### Level 3: File Reading and Counting Tests

#### Test 3.1: Sample Input File Test

**Goal**: Verify file reading works correctly

**Test method**:
1. Create a small test file with known strings
2. Manually calculate expected nice count
3. Run program and verify count matches

**Test file contents** (`test_input.txt`):
```
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
```

**Expected result**: 2 nice strings (first two)

**Validation**:
```python
def test_with_sample_file():
    import os
    # Create test file
    test_strings = [
        "ugknbfddgicrmopn",  # nice
        "aaa",                # nice
        "jchzalrnumimnmhp",  # naughty
        "haegwjzuvuyypxyu",  # naughty
        "dvszwmarrgswjxmb"   # naughty
    ]
    with open('test_input.txt', 'w') as f:
        f.write('\n'.join(test_strings))

    result = count_nice_strings('test_input.txt')
    assert result == 2, f"Expected 2, got {result}"

    # Cleanup
    os.remove('test_input.txt')
    print("✓ Sample file test passed")
```

#### Test 3.2: Actual Input Verification

**Goal**: Verify solution works on actual input.md

**Test method**:
1. Run solution on input.md
2. Manually verify a sample of strings from input
3. Check result is reasonable (not 0, not 1000, etc.)

**Manual verification samples** (from input.md):

Checking first 5 strings manually to verify correctness:

1. `uxcplgxnkwbdwhrp`
   - vowels: u (only 1) ❌
   - Result: NAUGHTY (fails vowel requirement)

2. `suerykeptdsutidb`
   - vowels: u,e,u,i (4 vowels) ✓
   - doubles: none visible ❌
   - Result: NAUGHTY (fails double letter requirement)

3. `dmrtgdkaimrrwmej`
   - vowels: a,i,e (3 vowels) ✓
   - doubles: rr ✓
   - forbidden: none ✓
   - Result: NICE ✓

4. `ztxhjwllrckhakut`
   - vowels: a,u (only 2) ❌
   - Result: NAUGHTY (fails vowel requirement)

5. `gdnzurjbbwmgayrg`
   - vowels: u,a (only 2) ❌
   - Result: NAUGHTY (fails vowel requirement)

**Validation method**:
```python
def verify_sample_strings():
    # Manually verify strings from actual input
    assert is_nice("uxcplgxnkwbdwhrp") == False, "Should fail: only 1 vowel"
    assert is_nice("suerykeptdsutidb") == False, "Should fail: no double letter"
    assert is_nice("dmrtgdkaimrrwmej") == True, "Should pass: all criteria met"
    assert is_nice("ztxhjwllrckhakut") == False, "Should fail: only 2 vowels"
    assert is_nice("gdnzurjbbwmgayrg") == False, "Should fail: only 2 vowels"
    print("✓ Sample string verification passed")
```

### Level 4: Comprehensive Test Suite

**Complete test runner**:
```python
def run_all_tests():
    print("Running comprehensive test suite...")
    print()

    print("Level 1: Unit Tests")
    test_has_three_vowels()
    test_has_double_letter()
    test_no_forbidden_substrings()
    print()

    print("Level 2: Integration Tests")
    test_is_nice_known_examples()
    test_is_nice_edge_cases()
    print()

    print("Level 3: File Processing Tests")
    test_with_sample_file()
    verify_sample_strings()
    print()

    print("All tests passed! ✓✓✓")
```

## Edge Cases Checklist

- [x] Empty strings (handled by input filtering; functions should still work if called directly)
- [x] Single character strings
- [x] Strings with only vowels
- [x] Strings with only consonants
- [x] Strings with multiple forbidden substrings
- [x] Strings where forbidden substring is at start/end
- [x] Strings with triple letters (should count as double)
- [x] Strings with exactly 3 vowels
- [x] Strings with many vowels (10+)
- [x] Very short strings (1-2 chars)
- [x] Reversed forbidden substrings (ba, dc, qp, yx - should be OK)

**Note on empty strings**: The `read_input()` function filters empty lines, so empty strings won't reach the classification functions in normal operation. However, unit tests verify that the individual functions handle empty strings correctly if called directly.

## Final Verification Steps

### Step 1: Run Unit Tests
Execute all unit tests and verify they pass

### Step 2: Run Integration Tests
Execute integration tests with known examples

### Step 3: Run on Actual Input
Execute solution on input.md and get final count

### Step 4: Sanity Check Result
- Result should be between 1 and 999 (unlikely to be 0 or 1000)
- Based on problem examples, roughly 20-40% of strings are typically nice
- Expected range: ~200-400 nice strings
- Quick timing check: should complete in well under 1 second for 1000 strings

### Step 5: Spot Check Random Samples
- Randomly pick 5-10 strings from input
- Manually verify classification matches program output
- This catches any systematic errors

## Verification Script

```python
if __name__ == '__main__':
    import time

    # Run all tests first
    run_all_tests()

    # Then run on actual input
    print("\nRunning on actual input...")
    start_time = time.time()
    result = count_nice_strings('input.md')
    elapsed = time.time() - start_time

    print(f"Total nice strings: {result}")
    print(f"Execution time: {elapsed:.4f} seconds")

    # Sanity checks
    if 0 < result < 1000:
        print("✓ Result is in reasonable range")
    else:
        print("⚠ Result seems unusual, verify manually")

    if elapsed < 1.0:
        print("✓ Performance is acceptable")
    else:
        print("⚠ Performance seems slow, consider optimization")
```

## Success Criteria

✅ All unit tests pass
✅ All integration tests pass
✅ Known examples produce correct results
✅ Edge cases handled correctly
✅ File reading works properly
✅ Final count is reasonable (not 0 or 1000)
✅ Manual spot checks confirm accuracy

## Notes on Testing Approach

**Why this is sufficient**:
- We're solving a specific problem, not building production software
- Unit tests cover all individual components
- Integration tests verify combined logic
- Known examples validate against problem statement
- Edge cases ensure robustness
- We don't need to test every possible string permutation

**What we're NOT testing** (and why that's OK):
- Performance under extreme load (not required for 1000 strings)
- Concurrent access (single-threaded script)
- Invalid file formats (input is given and well-formed)
- Unicode/special characters (problem states lowercase a-z only)
- Memory leaks (Python handles this, script is short-lived)

This testing plan ensures correctness while remaining pragmatic for the scope of the problem.
