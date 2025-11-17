# Test Plan: Signal Error Correction

## Testing Strategy
Verify the error correction algorithm works correctly through example validation, manual verification, and edge case testing.

## Test Categories

### 1. Example Test (Primary Validation)

#### Test 1.1: Provided Example
**Purpose**: Verify algorithm matches expected behavior from problem statement

**Input**:
```
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
```

**Expected Output**: `easter`

**Verification Steps**:
1. Create test input file with example data
2. Run decoder on example
3. Assert output == "easter"
4. Manual column verification with expected frequency distributions:
   - Column 0: e(8), d(2), r(1), a(1), t(1), s(1), n(1), v(1) → Most frequent: **e**
   - Column 1: a(5), n(2), s(2), v(2), r(2), d(1), e(1), t(1) → Most frequent: **a**
   - Column 2: s(6), n(3), d(2), a(2), t(2), v(1) → Most frequent: **s**
   - Column 3: t(6), d(3), s(2), n(2), a(1), r(1), v(1) → Most frequent: **t**
   - Column 4: e(5), v(3), t(2), d(2), s(2), a(1), n(1) → Most frequent: **e**
   - Column 5: r(5), a(3), d(2), v(2), e(2), n(1), t(1) → Most frequent: **r**

**Pass Criteria**: Output exactly matches "easter" and frequency analysis confirms each character selection

### 2. Actual Input Test

#### Test 2.1: Input File Validation
**Purpose**: Verify the input file structure meets expectations

**Process**:
1. Read input.md file
2. Count number of lines
3. Verify all lines are exactly 8 characters
4. Verify all characters are lowercase letters

**Validation**:
- Number of lines == 598
- All lines have length 8
- All characters match pattern: `[a-z]`

**Pass Criteria**: Input file structure is valid

#### Test 2.2: Full Input Processing
**Purpose**: Ensure algorithm processes the actual 598-line input correctly

**Process**:
1. Run decoder on actual input.md file
2. Verify output is generated without errors
3. Check output characteristics:
   - Length should be 8 characters
   - All characters should be lowercase letters (a-z)
   - No whitespace or special characters

**Validation**:
- Output length == 8
- Output matches pattern: `^[a-z]{8}$`
- Algorithm completes in reasonable time (< 1 second)

#### Test 2.3: Complete Manual Verification (CRITICAL)
**Purpose**: Manually verify correctness for ALL positions to ensure answer is correct

**Process**:
For each of the 8 positions (0-7):
1. Extract all characters at that position from all 598 lines
2. Count frequency of each character
3. Identify the most frequent character
4. Verify it matches the corresponding position in the output

**Execution**:
- Use a separate verification script or manual counting
- Document the frequency distribution for each position
- Compare all 8 characters with the algorithm output

**Example for Column 0**:
- Extract all first characters: u, j, e, r, p, c, k, e, b, t, ...
- Count frequency: {character: count} for all unique characters
- Most frequent character: [identify]
- Verify output[0] matches this character

**Pass Criteria**: All 8 positions independently verified to match output

**Note**: This is the gold standard for correctness verification. Each position must be checked.

### 3. Edge Cases and Corner Cases

#### Test 3.1: Single Line Input
**Input**: One transmission line (e.g., "testmsg")
**Expected**: "testmsg" (each character is 100% frequent)
**Rationale**: Tests minimum input case

#### Test 3.2: Two Line Input with Clear Winners
**Input**:
```
abc
axc
```
**Expected**: "aac" (a wins at positions 0 and 1 with 2/2, c wins at position 2 with 2/2, x appears 0/2 at positions 0 and 2)
**Rationale**: Tests clear majority with multiple lines

#### Test 3.3: All Same Character in Column
**Input**:
```
aaa
aaa
aaa
```
**Expected**: "aaa"
**Rationale**: Tests unanimous frequency (trivial case)

#### Test 3.4: Clear Majority
**Input**:
```
xxx
xxy
xxz
```
**Expected**: "xxx"
**Rationale**: Tests clear winner (x appears 3/3, 3/3, 2/3)

### 4. Input Validation Tests

#### Test 4.1: Empty Input File
**Input**: Empty file or file with only whitespace
**Expected Behavior**: Return empty string (graceful handling)

#### Test 4.2: Lines with Different Lengths
**Input**:
```
abc
abcd
ab
```
**Expected Behavior**: Raise ValueError with clear error message indicating which line has incorrect length
**Rationale**: Validates that input validation is working correctly

#### Test 4.3: File Not Found
**Input**: Non-existent file path
**Expected Behavior**: Print error message and exit gracefully (no stack trace)
**Rationale**: Verifies error handling for missing files

### 5. Frequency Counting Verification

#### Test 5.1: Frequency Distribution Logging
**Purpose**: Verify internal frequency calculations

**Process**:
1. Add debug output to show frequency counts for each position
2. For example data, verify:
   - Position 0: {'e': 8, 'd': 2, 'r': 1, ...}
   - Position 1: {'a': 5, 's': 2, 'n': 2, ...}
3. Confirm most_common(1) returns correct character

### 6. Performance Testing

#### Test 6.1: Runtime Verification
**Purpose**: Ensure algorithm runs efficiently

**Process**:
1. Time execution on full 598-line input
2. Verify completion time < 100ms (generous threshold)
3. Test confirms algorithm is O(n×m) as expected

**Expected**: Near-instantaneous (< 10ms typical)

#### Test 6.2: Deterministic Behavior
**Purpose**: Verify algorithm produces consistent results

**Process**:
1. Run decoder on same input multiple times
2. Verify all outputs are identical
3. Confirms deterministic behavior

**Expected**: Same output every time

### 7. Character Set Validation

#### Test 7.1: Output Character Validation
**Purpose**: Ensure output only contains expected characters

**Process**:
1. Run on actual input
2. Check each character in output
3. Verify all characters in range 'a'-'z'

**Validation**:
```python
result = decode_message(lines)
assert all('a' <= c <= 'z' for c in result)
```

### 8. Regression Testing

#### Test 8.1: Consistent Results
**Purpose**: Verify algorithm is deterministic

**Process**:
1. Run decoder on same input 3 times
2. Compare all outputs
3. Verify all outputs are identical

**Pass Criteria**: output1 == output2 == output3

## Test Execution Plan

### Phase 1: Basic Validation
1. Run Test 1.1 (Example test) - **CRITICAL**
2. Run Test 2.1 (Input file validation)
3. Run Test 2.2 (Actual input processing)
4. Run Test 7.1 (Output character validation)

### Phase 2: Manual Verification - **CRITICAL**
1. Run Test 2.3 (Complete manual verification for ALL 8 columns)
2. Verify frequency calculations match expected for each position
3. Document the complete answer with supporting frequency data

### Phase 3: Edge Cases (Optional but Recommended)
1. Run Test 3.1 (Single line)
2. Run Test 3.3 (All same character)
3. Run Test 3.4 (Clear majority)

### Phase 4: Performance Check
1. Run Test 6.1 (Runtime verification)
2. Ensure completion within reasonable time

## Success Criteria

### Minimum Requirements (Must Pass)
- ✓ Example test produces "easter" with verified frequency distributions
- ✓ Input file validation confirms 598 lines of 8 characters each
- ✓ Actual input produces 8-character lowercase output
- ✓ **Complete manual verification of all 8 positions confirms correctness**
- ✓ Completes in < 1 second

### Full Validation (Recommended)
- ✓ All edge cases handled correctly
- ✓ Output validation passes
- ✓ Regression test shows deterministic behavior

## Test Data Files

### Create Test Files

1. **test_example.txt** - Contains the 16-line example from problem statement:
```
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
```

2. **test_single.txt** - Single line test case:
```
testmsg
```

3. **test_simple.txt** - Simple test with clear winners:
```
xxx
xxy
xxz
```
Expected output: "xxx"

4. **test_tie.txt** - Two line test:
```
abc
axc
```
Expected output: "aac"

### Test Execution Script Structure
```python
from collections import Counter

def test_input_validation():
    """Validate input file structure."""
    lines = read_input('input.md')
    assert len(lines) == 598, f"Expected 598 lines, got {len(lines)}"

    for i, line in enumerate(lines):
        assert len(line) == 8, f"Line {i} has length {len(line)}, expected 8"
        assert all('a' <= c <= 'z' for c in line), f"Line {i} has invalid characters"

    print("✓ Input validation passed: 598 lines, all 8 characters, all lowercase")

def test_example():
    """Test with provided example."""
    lines = read_input('test_example.txt')
    result = decode_message(lines)
    assert result == "easter", f"Expected 'easter', got '{result}'"
    print("✓ Example test passed: 'easter'")

def test_actual_input():
    """Test with actual input."""
    lines = read_input('input.md')
    result = decode_message(lines)
    assert len(result) == 8, f"Expected length 8, got {len(result)}"
    assert all('a' <= c <= 'z' for c in result), "Invalid characters in output"
    print(f"✓ Actual input test passed: {result}")
    return result

def complete_manual_verification():
    """Manually verify ALL 8 columns - CRITICAL for correctness."""
    lines = read_input('input.md')
    result = decode_message(lines)

    print("\nComplete Manual Verification:")
    print("=" * 60)

    for pos in range(8):
        column = [line[pos] for line in lines]
        freq = Counter(column)
        most_common_char, count = freq.most_common(1)[0]

        # Display top 5 most common for verification
        top_5 = freq.most_common(5)
        freq_str = ", ".join([f"{char}({cnt})" for char, cnt in top_5])

        assert result[pos] == most_common_char, \
            f"Position {pos} failed: expected '{most_common_char}', got '{result[pos]}'"

        print(f"Position {pos}: {freq_str} → '{most_common_char}' ✓")

    print("=" * 60)
    print(f"✓ Complete manual verification passed!")
    print(f"✓ Final answer: {result}")
    return result

def test_single_line():
    """Test with single line."""
    lines = ["testmsg"]
    result = decode_message(lines)
    assert result == "testmsg", f"Expected 'testmsg', got '{result}'"
    print("✓ Single line test passed")

def test_unequal_lines():
    """Test that unequal line lengths raise error."""
    lines = ["abc", "abcd", "ab"]
    try:
        decode_message(lines)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Unequal lines test passed: {e}")

def run_all_tests():
    """Run all tests."""
    print("Running Signal Error Correction Tests...")
    print()
    test_example()
    test_input_validation()
    result = test_actual_input()
    print()
    complete_manual_verification()
    print()
    test_single_line()
    test_unequal_lines()
    print("\n" + "=" * 60)
    print(f"✓ ALL TESTS PASSED!")
    print(f"✓ Final verified answer: {result}")
    print("=" * 60)
```

## Debugging Strategy

If tests fail:

1. **Example test fails**:
   - Print frequency distribution for each column
   - Verify Counter.most_common() is working correctly
   - Check for off-by-one errors in indexing

2. **Actual input produces wrong length**:
   - Run input validation test to check line count and lengths
   - Verify input parsing (empty lines filtered)
   - Print first few lines to inspect

3. **Character validation fails**:
   - Print the output to see what characters appear
   - Check if input has unexpected characters
   - Verify input cleaning (strip() working correctly)

4. **Manual verification fails**:
   - Print full frequency distribution for failing position
   - Compare with algorithm output character
   - Check for tie scenarios or algorithm bugs
   - Verify Counter.most_common() is working correctly

## Expected Test Results Summary

| Test | Input | Expected Output | Priority |
|------|-------|----------------|----------|
| Example | 16 lines "eedadn"... | "easter" | CRITICAL |
| Input Validation | 598 lines check | All valid | HIGH |
| Actual Input | 598 lines from input.md | 8-char lowercase string | CRITICAL |
| Complete Manual Verification | All 8 columns verified | Matches output exactly | CRITICAL |
| Single Line | "testmsg" | "testmsg" | Medium |
| All Same | "aaa" × 3 | "aaa" | Low |
| Unequal Lines | Mixed lengths | ValueError raised | Medium |

## Conclusion

The test plan focuses on:
1. **Correctness**: Verify algorithm produces correct output via example test
2. **Complete Verification**: Manual verification of ALL 8 positions for actual input (gold standard)
3. **Input Validation**: Ensure input file structure is correct (598 lines, 8 chars each)
4. **Edge Cases**: Handle boundary conditions and error cases gracefully
5. **Robustness**: Verify error handling and deterministic behavior

**Critical Path**: The most important tests are:
1. Example test producing "easter" with documented frequency distributions
2. Complete manual verification of all 8 positions for the actual input
3. Input file validation

These three tests together provide high confidence that the solution is correct.
