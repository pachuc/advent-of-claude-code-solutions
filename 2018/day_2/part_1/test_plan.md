# Testing Plan: Inventory Management System Checksum

## Testing Strategy Overview

We need to verify:
1. Correct parsing of input
2. Accurate letter frequency counting
3. Proper identification of exact-count matches
4. Correct checksum calculation
5. Handling of edge cases

## Test Categories

### 1. Unit Tests for Individual Functions

#### Test 1.1: `has_exact_count()` - Basic Functionality
**Purpose**: Verify correct detection of exact letter counts

**Test Cases**:
| Box ID | Target Count | Expected Result | Reason |
|--------|-------------|-----------------|---------|
| `"abcdef"` | 2 | False | No letter appears twice |
| `"abcdef"` | 3 | False | No letter appears three times |
| `"abbcde"` | 2 | True | 'b' appears exactly twice |
| `"abbcde"` | 3 | False | No letter appears three times |
| `"abcccd"` | 3 | True | 'c' appears exactly three times |
| `"abcccd"` | 2 | False | No letter appears exactly twice |
| `"bababc"` | 2 | True | 'a' appears exactly twice |
| `"bababc"` | 3 | True | 'b' appears exactly three times |

**Implementation**:
```python
def test_has_exact_count():
    assert has_exact_count("abcdef", 2) == False
    assert has_exact_count("abcdef", 3) == False
    assert has_exact_count("abbcde", 2) == True
    assert has_exact_count("abbcde", 3) == False
    assert has_exact_count("abcccd", 3) == True
    assert has_exact_count("abcccd", 2) == False
    assert has_exact_count("bababc", 2) == True
    assert has_exact_count("bababc", 3) == True
```

#### Test 1.2: `has_exact_count()` - Edge Cases
**Purpose**: Test boundary conditions

**Test Cases**:
| Box ID | Target Count | Expected Result | Reason |
|--------|-------------|-----------------|---------|
| `"aabcdd"` | 2 | True | Multiple letters appear twice (a, d) - should still return True once |
| `"ababab"` | 3 | True | Multiple letters appear three times (a, b) - should still return True once |
| `"aa"` | 2 | True | Minimum case - exactly one letter twice |
| `"aaa"` | 3 | True | Minimum case - exactly one letter three times |
| `"aaa"` | 2 | False | Letter appears 3 times, not 2 |
| `"aaaa"` | 2 | False | Letter appears 4 times, not 2 |
| `"aaaa"` | 3 | False | Letter appears 4 times, not 3 |
| `"abcdee"` | 2 | True | 'e' appears exactly twice |
| `""` | 2 | False | Empty string edge case (won't occur with proper input parsing) |

**Implementation**:
```python
def test_has_exact_count_edge_cases():
    # Multiple letters with same count
    assert has_exact_count("aabcdd", 2) == True
    assert has_exact_count("ababab", 3) == True

    # Minimum cases
    assert has_exact_count("aa", 2) == True
    assert has_exact_count("aaa", 3) == True

    # Near misses - must be EXACT count
    assert has_exact_count("aaa", 2) == False
    assert has_exact_count("aaaa", 2) == False
    assert has_exact_count("aaaa", 3) == False

    # Normal case
    assert has_exact_count("abcdee", 2) == True

    # Empty string (if it occurs)
    assert has_exact_count("", 2) == False
```

#### Test 1.3: `parse_input()` - Input Parsing
**Purpose**: Verify correct file reading and parsing

**Test Setup**: Create a temporary test file with known content

**Test Cases**:
1. File with multiple lines
2. File with trailing newline
3. File with empty lines mixed in
4. File with whitespace around box IDs

**Expected Behavior**:
- Should return list of non-empty, stripped strings
- Should handle trailing newlines gracefully
- Should filter out empty lines

**Implementation**:
```python
def test_parse_input():
    # Create a temporary test file
    import tempfile
    import os

    test_content = "abc\ndef\n\nghi  \n  jkl\n\n"

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(test_content)
        temp_path = f.name

    try:
        result = parse_input(temp_path)

        # Should have 4 entries (abc, def, ghi, jkl)
        assert len(result) == 4

        # All should be stripped
        assert result == ["abc", "def", "ghi", "jkl"]

        # No empty strings
        assert all(len(box_id) > 0 for box_id in result)
    finally:
        os.unlink(temp_path)
```

#### Test 1.4: `calculate_checksum()` - Simple Cases
**Purpose**: Unit test the checksum calculation with simple inputs

**Test Cases**:
| Input | Twos Count | Threes Count | Expected Checksum | Reason |
|-------|-----------|-------------|-------------------|---------|
| `["aa"]` | 1 | 0 | 0 | Only has twos |
| `["aaa"]` | 0 | 1 | 0 | Only has threes |
| `["aa", "bbb"]` | 1 | 1 | 1 | One two, one three |
| `["aa", "bb"]` | 2 | 0 | 0 | Two boxes with twos |
| `["aaa", "bbb"]` | 0 | 2 | 0 | Two boxes with threes |
| `["aa", "bbb", "cc", "ddd"]` | 2 | 2 | 4 | 2 × 2 |

**Implementation**:
```python
def test_calculate_checksum_simple():
    # Only twos
    assert calculate_checksum(["aa"]) == 0  # 1 × 0

    # Only threes
    assert calculate_checksum(["aaa"]) == 0  # 0 × 1

    # One of each
    assert calculate_checksum(["aa", "bbb"]) == 1  # 1 × 1

    # Multiple twos
    assert calculate_checksum(["aa", "bb"]) == 0  # 2 × 0

    # Multiple threes
    assert calculate_checksum(["aaa", "bbb"]) == 0  # 0 × 2

    # Balanced
    assert calculate_checksum(["aa", "bbb", "cc", "ddd"]) == 4  # 2 × 2
```

### 2. Integration Tests

#### Test 2.1: Example from Problem Statement
**Purpose**: Verify complete algorithm with known example

**Input**:
```
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
```

**Expected Analysis**:
- `abcdef`: neither (no 2s or 3s)
- `bababc`: both (a=2, b=3)
- `abbcde`: twos (b=2)
- `abcccd`: threes (c=3)
- `aabcdd`: twos (a=2, d=2)
- `abcdee`: twos (e=2)
- `ababab`: threes (a=3, b=3)

**Expected Counts**:
- Twos: 4 (bababc, abbcde, aabcdd, abcdee)
- Threes: 3 (bababc, abcccd, ababab)
- Checksum: 4 × 3 = 12

**Implementation**:
```python
def test_example_checksum():
    box_ids = [
        "abcdef",
        "bababc",
        "abbcde",
        "abcccd",
        "aabcdd",
        "abcdee",
        "ababab"
    ]
    result = calculate_checksum(box_ids)
    assert result == 12
```

#### Test 2.2: Edge Case - All Same
**Purpose**: Test when all box IDs have same characteristics

**Test Cases**:
1. All box IDs have twos and threes
   - Input: `["aabbbc", "xxyyyzzz", "pqqrrrsss"]`
   - Expected: 3 × 3 = 9

2. No box IDs have twos or threes
   - Input: `["abcdefg", "hijklmn", "opqrstu"]`
   - Expected: 0 × 0 = 0

3. All have twos, none have threes
   - Input: `["aabbcd", "eeffgh", "iijjkl"]`
   - Expected: 3 × 0 = 0

**Implementation**:
```python
def test_edge_case_all_same():
    # All have both twos and threes
    box_ids = ["aabbbc", "xxyyyzz", "pqqrrrsss"]
    result = calculate_checksum(box_ids)
    assert result == 9  # 3 × 3

    # None have twos or threes
    box_ids = ["abcdefg", "hijklmn", "opqrstu"]
    result = calculate_checksum(box_ids)
    assert result == 0  # 0 × 0

    # All have twos, none have threes
    box_ids = ["aabbcd", "eeffgh", "iijjkl"]
    result = calculate_checksum(box_ids)
    assert result == 0  # 3 × 0
```

#### Test 2.3: Edge Case - Single Box ID
**Purpose**: Test minimal input

**Test Cases**:
1. Single box with both: checksum = 1 × 1 = 1
2. Single box with only twos: checksum = 1 × 0 = 0
3. Single box with only threes: checksum = 0 × 1 = 0
4. Single box with neither: checksum = 0 × 0 = 0

**Implementation**:
```python
def test_single_box_id():
    # Both twos and threes
    assert calculate_checksum(["aabbbc"]) == 1  # 1 × 1

    # Only twos
    assert calculate_checksum(["aabb"]) == 0  # 1 × 0

    # Only threes
    assert calculate_checksum(["aaabbb"]) == 0  # 0 × 1

    # Neither
    assert calculate_checksum(["abcdefg"]) == 0  # 0 × 0
```

### 3. Important Edge Cases to Verify

#### Test 3.1: Multiple Letters with Same Count
**Purpose**: Ensure box ID counts only once even if multiple letters match

**Critical Test**:
- Box ID: `"aabbccdd"` (four letters appear exactly twice)
- Should increment twos counter by 1 (not 4)
- Box ID: `"aaabbbccc"` (three letters appear exactly three times)
- Should increment threes counter by 1 (not 3)

**Implementation**:
```python
def test_multiple_letters_same_count():
    # Multiple letters with same frequency - should count only once

    # Four letters appear exactly twice
    box_ids = ["aabbccdd"]
    result = calculate_checksum(box_ids)
    assert result == 0  # 1 two × 0 threes = 0

    # Three letters appear exactly three times
    box_ids = ["aaabbbccc"]
    result = calculate_checksum(box_ids)
    assert result == 0  # 0 twos × 1 three = 0

    # Verify the has_exact_count returns True (counts once)
    assert has_exact_count("aabbccdd", 2) == True
    assert has_exact_count("aaabbbccc", 3) == True
```

#### Test 3.2: Box ID Contributing to Both Counters
**Purpose**: Verify independent counting

**Test**:
- Box ID: `"aabbbc"` (a=2, b=3, c=1)
- Should increment both twos and threes counters
- Not an either/or situation

**Implementation**:
```python
def test_box_contributes_to_both():
    # Single box with both characteristics
    box_ids = ["aabbbc"]  # a=2, b=3, c=1
    result = calculate_checksum(box_ids)
    assert result == 1  # 1 two × 1 three = 1

    # Multiple boxes, some with both
    box_ids = ["aabbbc", "xxyyyzzz"]  # First has both, second has both
    result = calculate_checksum(box_ids)
    assert result == 4  # 2 twos × 2 threes = 4
```

#### Test 3.3: Near Misses
**Purpose**: Ensure exact matching only

**Test Cases**:
- `"aaaa"` - 4 occurrences should NOT count as 2 or 3
- `"a"` - 1 occurrence should NOT count as 2 or 3
- `"aaaaa"` - 5 occurrences should NOT count as 2 or 3

**Implementation**:
```python
def test_near_misses():
    # 4 occurrences should not count as 2 or 3
    assert has_exact_count("aaaa", 2) == False
    assert has_exact_count("aaaa", 3) == False

    # 1 occurrence should not count as 2 or 3
    assert has_exact_count("a", 2) == False
    assert has_exact_count("a", 3) == False

    # 5 occurrences should not count as 2 or 3
    assert has_exact_count("aaaaa", 2) == False
    assert has_exact_count("aaaaa", 3) == False

    # These should produce 0 checksum
    assert calculate_checksum(["aaaa"]) == 0
    assert calculate_checksum(["a"]) == 0
    assert calculate_checksum(["aaaaa"]) == 0
```

### 4. Actual Input Validation

#### Test 4.1: Input File Format
**Purpose**: Verify input meets expectations

**Checks**:
1. Count number of box IDs (should be ~250)
2. Verify all box IDs are lowercase letters only
3. Check length of box IDs (should be consistent ~26 chars)
4. Ensure no unexpected characters

**Implementation**:
```python
def test_input_format():
    box_ids = parse_input('input.md')

    # Should have many box IDs
    assert len(box_ids) > 0

    # All should be non-empty strings
    assert all(isinstance(bid, str) and len(bid) > 0 for bid in box_ids)

    # All should be lowercase letters only
    assert all(bid.islower() and bid.isalpha() for bid in box_ids)
```

#### Test 4.2: Manual Spot Check
**Purpose**: Manually verify a few box IDs from actual input

**Process**:
1. Take first 3-5 box IDs from input.md
2. Manually count letter frequencies
3. Verify our function produces correct results
4. Compare with algorithm output

**Example Spot Checks**:
- `"xrysntkqrduheficajodiglvzw"`: manually count each letter
- `"xzymntkqrbuhefmcajodiflvzw"`: manually count each letter

### 5. Output Validation

#### Test 5.1: Output Format
**Purpose**: Ensure output matches requirements

**Checks**:
- Output is a single integer
- No additional text or formatting
- No trailing newline issues

#### Test 5.2: Reasonableness Check
**Purpose**: Sanity check on final answer

**Expectations**:
- Given ~250 box IDs
- Checksum should be reasonable (likely in range 1,000 - 100,000)
- Should not be 0 (very unlikely all lack 2s or 3s)
- Should not be impossibly large

## Testing Execution Order

1. **Start with unit tests** - test `has_exact_count()` thoroughly
2. **Test example** - verify with problem's example (expected: 12)
3. **Test edge cases** - ensure corner cases work
4. **Validate input** - check input file is well-formed
5. **Run actual input** - get final answer
6. **Manual verification** - spot check a few box IDs by hand

## Success Criteria

The solution is correct if:
1. All unit tests pass
2. Example test produces checksum = 12
3. Edge cases handled correctly
4. Actual input produces a reasonable integer result
5. Spot checks of individual box IDs match algorithm output

## Debugging Strategy

If tests fail:
1. Print intermediate values (twos_count, threes_count)
2. Print frequency dictionaries for failing box IDs
3. Verify Counter is working correctly
4. Check for off-by-one errors
5. Ensure not using elif when should use independent ifs

## Summary of Plan Updates

Based on critique feedback, this plan now includes:

1. **Complete Test Implementations**: All critical tests now have full Python implementations, not just descriptions
2. **Added Unit Tests for `calculate_checksum()`**: New Test 1.4 provides simple unit tests for the checksum function
3. **Implemented Critical Edge Cases**: Tests 3.1, 3.2, and 3.3 now include full implementations to verify:
   - Multiple letters with same count only count once per box ID
   - Box IDs can contribute to both twos and threes counters
   - Exact count matching (no near misses)
4. **Parse Input Testing**: Added complete implementation for testing input parsing with temporary files
5. **Integration Tests**: All edge case tests (Test 2.2, 2.3) now have implementations
6. **Ready to Execute**: All test code can now be directly used to verify the solution
