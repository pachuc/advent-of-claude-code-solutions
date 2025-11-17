# Test Plan: String Encoding

## Testing Strategy

Test the solution with examples from the problem statement, edge cases, and verify against the actual input.

## Test Categories

### 1. Example Test Cases (from problem statement)

These are the canonical examples that must pass:

#### Test 1.1: Empty String
```python
Input:  '""'
Original length: 2
Encoded: '"\"\""'
Encoded length: 6
Expected difference: +4
```

**Verification Logic**:
- `"` → `\"` (2 chars)
- `"` → `\"` (2 chars)
- Add outer quotes: +2
- Total: 6 chars, diff = 6 - 2 = 4

#### Test 1.2: Simple String
```python
Input:  '"abc"'
Original length: 5
Encoded: '"\"abc\""'
Encoded length: 9
Expected difference: +4
```

**Verification Logic**:
- `"` → `\"` (2 chars)
- `a` → `a` (1 char)
- `b` → `b` (1 char)
- `c` → `c` (1 char)
- `"` → `\"` (2 chars)
- Add outer quotes: +2
- Total: 9 chars, diff = 9 - 5 = 4

#### Test 1.3: String with Escaped Quote
```python
Input:  '"aaa\"aaa"'
Original length: 10
Encoded: '"\"aaa\\\"aaa\""'
Encoded length: 16
Expected difference: +6
```

**Verification Logic**:
- `"` → `\"` (2 chars)
- `a` → `a` (1 char)
- `a` → `a` (1 char)
- `a` → `a` (1 char)
- `\` → `\\` (2 chars)
- `"` → `\"` (2 chars)
- `a` → `a` (1 char)
- `a` → `a` (1 char)
- `a` → `a` (1 char)
- `"` → `\"` (2 chars)
- Add outer quotes: +2
- Total: 16 chars, diff = 16 - 10 = 6

#### Test 1.4: String with Hex Escape
```python
Input:  '"\x27"'
Original length: 6
Encoded: '"\"\\x27\""'
Encoded length: 11
Expected difference: +5
```

**Verification Logic**:
- `"` → `\"` (2 chars)
- `\` → `\\` (2 chars)
- `x` → `x` (1 char)
- `2` → `2` (1 char)
- `7` → `7` (1 char)
- `"` → `\"` (2 chars)
- Add outer quotes: +2
- Total: 11 chars, diff = 11 - 6 = 5

### 2. Edge Case Tests

#### Test 2.0: Consecutive Escape Sequences
```python
Input:  '"\\\\\\\\"'
Original length: 8
Four backslashes in a row: \\\\
```

**Verification**:
- `"` → `\"` (2 chars)
- `\` → `\\` (2 chars)
- `\` → `\\` (2 chars)
- `\` → `\\` (2 chars)
- `\` → `\\` (2 chars)
- `"` → `\"` (2 chars)
- Add outer quotes: +2
- Total: 14 chars, diff = 14 - 8 = 6

This test ensures the algorithm doesn't get confused by consecutive backslashes.

#### Test 2.1: Only Backslashes
```python
Input:  '"\\\\"'
Original length: 4
Each \ needs escaping, so we have 2 backslashes in original
Encoded: '"\"\\\\\\\\\""'
```

**Verification**:
- `"` → `\"` (2 chars)
- `\` → `\\` (2 chars)
- `\` → `\\` (2 chars)
- `"` → `\"` (2 chars)
- Add outer quotes: +2
- Total: 10 chars, diff = 10 - 4 = 6

#### Test 2.2: Only Quotes
```python
Input:  '"\"\""'
Original length: 6
Encoded: '"\"\\\"\\\"\""'
```

**Verification**:
- `"` → `\"` (2 chars)
- `\` → `\\` (2 chars)
- `"` → `\"` (2 chars)
- `\` → `\\` (2 chars)
- `"` → `\"` (2 chars)
- `"` → `\"` (2 chars)
- Add outer quotes: +2
- Total: 14 chars, diff = 14 - 6 = 8

#### Test 2.3: Mixed Special Characters
```python
Input:  '"\\\"\\"\\\""'
Original length: 12
Contains: ", \, ", \, ", \, ", "
Test that consecutive special characters are handled correctly
```

**Verification**:
- Each `"` → `\"` (2 chars)
- Each `\` → `\\` (2 chars)
- There are 5 quotes and 3 backslashes in the input
- Encoded: 5×2 + 3×2 + 2 (outer quotes) = 18 chars
- Difference: 18 - 12 = 6

#### Test 2.4: No Special Characters
```python
Input:  '"abcdef"'
Original length: 8
Only the surrounding quotes need escaping
Encoded: '"\"abcdef\""'
Encoded length: 12
Difference: +4
```

This should always add exactly 4 characters for strings with no special chars.

#### Test 2.5: Very Long String
```python
Create a test with 1000+ character string to ensure no performance issues
Should complete in under 1 second

For a string with N total characters:
- If no special chars (only outer quotes): difference = +4
- If all backslashes: difference = 2 + N
- If all quotes: difference = 2 + N
```

**Verification**:
Test a 1000-character string with known composition and verify the formula holds.

### 3. Real Input Validation

#### Test 3.1: Sample Lines from Actual Input
Test a few specific lines from input.md:

```python
Line 1: "azlgxdbljwygyttzkfwuxv"
- 24 chars total
- Only outer quotes need escaping
- Expected difference: +4

Line 2: "v\xfb\"lgs\"kvjfywmut\x9cr"
- Count: " v \ x f b \ " l g s \ " k v j f y w m u t \ x 9 c r "
- Multiple backslashes and quotes
- Manual calculation for verification
```

#### Test 3.2: Complete Input File
```python
Process entire input.md file
Compare result against any known solution or:
- Manually verify subset of lines
- Use alternative implementation to cross-check
- Ensure result is reasonable (positive integer)

# Sanity bounds calculation:
# Each line has minimum difference of +4 (only outer quotes escaped)
# Maximum difference per line: 2 + N where N is line length
# For 300 lines with average ~30 chars: rough upper bound ~10,000
```

**Better Sanity Check**:
```python
assert result > 300 * 4, "Minimum should be 4 per line"
assert result < sum(len(line) + 2 for line in lines), "Should not exceed theoretical maximum"
```

### 4. Structural Tests

#### Test 4.1: Empty Input File
```python
Input: Empty file or file with only whitespace
Expected: 0 difference
Verify no crashes or errors
```

#### Test 4.2: Single Line
```python
Input: File with exactly one string literal
Verify single-line processing works correctly
```

#### Test 4.3: Input with Trailing/Leading Whitespace
```python
Ensure .strip() handles various whitespace scenarios
Test lines with \n, \r\n, spaces, tabs
```

## Testing Implementation

### Test Script Structure

```python
def test_examples():
    """Test cases from problem statement"""
    test_cases = [
        ('""', 4),
        ('"abc"', 4),
        ('"aaa\\"aaa"', 6),
        ('"\\x27"', 5),
    ]

    for input_str, expected_diff in test_cases:
        result = calculate_encoded_difference(input_str)
        assert result == expected_diff, f"Failed for {input_str}: got {result}, expected {expected_diff}"

    print("✓ All example tests passed")

def test_edge_cases():
    """Test edge cases"""
    # Test only backslashes
    # Test only quotes
    # Test no special chars
    # etc.

def test_real_input():
    """Test against actual input file"""
    result = solve('input.md')
    print(f"Result for input.md: {result}")

    # Sanity checks
    assert result > 0, "Result should be positive"
    assert result < 10000, "Result seems too large, check logic"

def calculate_encoded_difference(line):
    """Helper function to calculate difference for a single line"""
    original_length = len(line)
    encoded_length = 2

    for char in line:
        if char == '"' or char == '\\':
            encoded_length += 2
        else:
            encoded_length += 1

    return encoded_length - original_length

if __name__ == "__main__":
    test_examples()
    test_edge_cases()
    test_real_input()
    print("✓ All tests passed!")
```

## Manual Verification Method

For small examples, manually verify by:

1. **Write out the original string character by character**
   - Count total characters including quotes

2. **Write out the encoded string character by character**
   - Add opening quote
   - For each character in original:
     - If `"` write `\"`
     - If `\` write `\\`
     - Otherwise write the character as-is
   - Add closing quote

3. **Count and compare**

Example walkthrough for `"a\"b"`:
```
Original: " a \ " b "  (6 chars)
Encoded:  " \" a \\ \" b \" "  (12 chars)
          ^ opening quote
            ^^ escaped opening quote of original
               ^ regular 'a'
                  ^^ escaped backslash
                     ^^ escaped quote
                        ^ regular 'b'
                           ^^ escaped closing quote of original
                              ^ closing quote
Difference: 12 - 6 = 6
```

## Success Criteria

1. ✓ All example tests pass with correct differences
2. ✓ Edge cases handle special characters correctly
3. ✓ Real input produces a reasonable result
4. ✓ No errors or crashes on valid input
5. ✓ Performance is acceptable (< 1 second for 300 lines)
6. ✓ Manual verification of sample lines matches computed results

## Debugging Strategy

If tests fail:
1. Print original string character-by-character with indices
2. Print character codes for non-printable characters
3. Manually count expected encoded length
4. Compare with computed value
5. Check for off-by-one errors in counting outer quotes

## Updates Based on Critique

The following enhancements have been incorporated based on feedback:

1. **Test 2.0 Added**: Consecutive escape sequences test to ensure algorithm handles multiple backslashes correctly
2. **Test 2.2 Enhanced**: Added specific character-by-character calculation with expected value (diff = 8)
3. **Test 2.3 Enhanced**: Added specific calculation showing 5 quotes + 3 backslashes → diff = 6
4. **Test 2.5 Enhanced**: Added formulas for different character compositions
5. **Test 3.2 Enhanced**: Replaced arbitrary sanity check with calculated bounds based on theoretical min/max

These changes make the test plan more specific and easier to verify, while maintaining the appropriate scope for a scripting task.
