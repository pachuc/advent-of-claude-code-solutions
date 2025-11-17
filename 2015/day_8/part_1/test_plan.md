# Testing Plan: String Literal Character Count

## Testing Strategy Overview
This plan focuses on verifying correctness through:
1. Example test cases from the problem statement
2. Edge case validation
3. Escape sequence handling verification
4. Full input validation
5. Manual spot-checking of complex cases

## Test Categories

### 1. Example Test Cases (from Problem Statement)
**Purpose**: Verify the implementation matches the expected behavior from examples

**Test Cases**:
| Input | Expected Code | Expected Memory | Expected Diff | Description |
|-------|--------------|-----------------|---------------|-------------|
| `""` | 2 | 0 | 2 | Empty string |
| `"abc"` | 5 | 3 | 2 | Simple string |
| `"aaa\"aaa"` | 10 | 7 | 3 | Escaped quote |
| `"\x27"` | 6 | 1 | 5 | Hex escape only |

**Combined Expected Result**: 2 + 2 + 3 + 5 = 12

**Test Implementation**:
```python
def test_examples():
    # IMPORTANT: Use raw strings (r"...") to avoid Python's own escape processing
    # This ensures the test strings match the actual input format
    test_cases = [
        (r'""', 2, 0),
        (r'"abc"', 5, 3),
        (r'"aaa\"aaa"', 10, 7),
        (r'"\x27"', 6, 1)
    ]

    for line, expected_code, expected_memory in test_cases:
        code = count_code_chars(line)
        memory = count_memory_chars(line)
        assert code == expected_code, f"Code count failed for {line}"
        assert memory == expected_memory, f"Memory count failed for {line}"
        print(f"✓ {line}: code={code}, memory={memory}, diff={code-memory}")

    # Test combined difference
    total_diff = sum(code - memory for _, code, memory in test_cases)
    assert total_diff == 12, f"Expected 12, got {total_diff}"
    print(f"✓ Combined example difference: {total_diff}")
    print("✓ All examples from problem statement passed!")
```

### 2. Edge Cases
**Purpose**: Test boundary conditions and unusual inputs

**Test Cases**:

#### 2.1 Minimum Cases
- `""` - Empty string (shortest possible)
- `"a"` - Single character
- Code: 3, Memory: 1, Diff: 2

#### 2.2 Backslash Variations
- `"\\"` - Single escaped backslash
  - Code: 4, Memory: 1, Diff: 3
- `"\\\\"` - Two escaped backslashes
  - Code: 6, Memory: 2, Diff: 4
- `"\\\\\\\\"` - Four escaped backslashes
  - Code: 10, Memory: 4, Diff: 6

#### 2.3 Quote Variations
- `"\""` - Single escaped quote
  - Code: 4, Memory: 1, Diff: 3
- `"\"\""` - Two escaped quotes
  - Code: 6, Memory: 2, Diff: 4

#### 2.4 Hex Escape Variations
- `"\x00"` - Null character
  - Code: 6, Memory: 1, Diff: 5
- `"\xff"` - Max byte value
  - Code: 6, Memory: 1, Diff: 5
- `"\x27\x27"` - Two consecutive hex escapes
  - Code: 10, Memory: 2, Diff: 8
- `"\x27\x27\x27"` - Three consecutive hex escapes
  - Code: 14, Memory: 3, Diff: 11
- `"abc\x27"` - Hex escape at end of string
  - Code: 9, Memory: 4, Diff: 5

#### 2.5 Mixed Escape Sequences
- `"\\\""`  - Backslash then quote
  - Code: 6, Memory: 2, Diff: 4
- `"\\\x27"` - Backslash immediately followed by hex escape
  - Code: 8, Memory: 2, Diff: 6
- `"a\\b\"c\x27d"` - Mixed everything (regular + backslash + quote + hex)
  - Code: 14, Memory: 6, Diff: 8
  - Breakdown: a(1) + \\(1) + b(1) + \"(1) + c(1) + \x27(1) + d(1) = 6 memory chars

**Test Implementation**:
```python
def test_edge_cases():
    # NOTE: All test strings use raw string literals (r"...") to preserve
    # the escape sequences as they appear in the input file
    edge_cases = [
        (r'""', 2, 0, "empty string"),
        (r'"a"', 3, 1, "single char"),
        (r'"\\"', 4, 1, "single backslash"),
        (r'"\\\\"', 6, 2, "two backslashes"),
        (r'"\""', 4, 1, "single quote"),
        (r'"\"\""', 6, 2, "two quotes"),
        (r'"\x00"', 6, 1, "hex null"),
        (r'"\xff"', 6, 1, "hex max"),
        (r'"\x27\x27"', 10, 2, "two hex escapes"),
        (r'"\x27\x27\x27"', 14, 3, "three hex escapes"),
        (r'"abc\x27"', 9, 4, "hex at end"),
        (r'"\\\""', 6, 2, "backslash + quote"),
        (r'"\\\x27"', 8, 2, "backslash + hex"),
    ]

    for line, expected_code, expected_memory, desc in edge_cases:
        code = count_code_chars(line)
        memory = count_memory_chars(line)
        assert code == expected_code, f"Code failed for {desc}: {line}"
        assert memory == expected_memory, f"Memory failed for {desc}: {line}"
        print(f"✓ {desc}: {line} -> code={code}, memory={memory}")

    print(f"✓ All {len(edge_cases)} edge cases passed!")
```

### 3. Real Input Validation
**Purpose**: Test against actual input data and verify specific tricky cases

**Approach**:
1. Run the solution against the full input.md
2. Manually verify a sample of complex lines
3. Check that the result is reasonable

**Sample Lines to Manually Verify**:

#### Line 2: `"v\xfb\"lgs\"kvjfywmut\x9cr"`
- Code: 28 characters (raw string including quotes)
- Memory breakdown:
  - v (1)
  - \xfb (1)
  - \" (1)
  - lgs (3)
  - \" (1)
  - kvjfywmut (9)
  - \x9c (1)
  - r (1)
  - Total: 18
- Diff: 28 - 18 = 10

#### Line 8: `"kbngyfvvsdismznhar\\p\"\"gpryt\"jaeh"`
- Code: 38
- Memory breakdown:
  - kbngyfvvsdismznhar (18)
  - \\ (1)
  - p (1)
  - \" (1)
  - \" (1)
  - gpryt (5)
  - \" (1)
  - jaeh (4)
  - Total: 32
- Diff: 38 - 32 = 6

#### Line 76: `"\xcdvryveteqzxrgopmdmihkcgsuozips"`
- Code: 36
- Memory breakdown:
  - \xcd (1)
  - vryveteqzxrgopmdmihkcgsuozips (29)
  - Total: 30
- Diff: 36 - 30 = 6

**Test Implementation**:
```python
def test_sample_lines():
    # CRITICAL: Use raw strings (r"...") to avoid Python's escape processing
    # These test strings must match the exact input format
    samples = [
        (r'"v\xfb\"lgs\"kvjfywmut\x9cr"', 28, 18, "line 2"),
        (r'"kbngyfvvsdismznhar\\p\"\"gpryt\"jaeh"', 38, 32, "line 8"),
        (r'"\xcdvryveteqzxrgopmdmihkcgsuozips"', 36, 30, "line 76"),
    ]

    for line, expected_code, expected_memory, desc in samples:
        code = count_code_chars(line)
        memory = count_memory_chars(line)
        print(f"{desc}: code={code} (expected {expected_code}), "
              f"memory={memory} (expected {expected_memory})")
        assert code == expected_code, f"Code mismatch for {desc}"
        assert memory == expected_memory, f"Memory mismatch for {desc}"
        print(f"✓ {desc} verified")

    print("✓ All sample lines from actual input verified!")
```

### 4. Integration Test
**Purpose**: Verify the complete solution works end-to-end

**Test Steps**:
1. Run the solution with the full input.md file
2. Verify the output is a single integer
3. Check the result is in a reasonable range:
   - Minimum possible: 2 per line × 300 lines = 600 (only quotes, no content)
   - Most likely range: 1200-1800 (based on typical escape sequence density)
   - Maximum reasonable: ~10 per line × 300 lines = 3000
   - (Each line has at least 2 quotes, most lines have 2-5 escape sequences)

**Test Implementation**:
```python
def test_full_input():
    lines = read_input('input.md')

    # Verify we read the correct number of lines
    assert len(lines) == 300, f"Expected 300 lines, got {len(lines)}"
    print(f"✓ Read {len(lines)} lines")

    # Calculate result
    result = calculate_difference(lines)

    # Sanity check the result
    assert isinstance(result, int), "Result should be an integer"
    assert 1200 <= result <= 1800, f"Result {result} outside expected range [1200, 1800]"
    print(f"✓ Final result: {result}")
    print(f"✓ Result is within expected range [1200, 1800]")

    return result
```

**Note**: The expected range [1200, 1800] is based on:
- 300 lines with average 4-6 character difference per line
- If the result falls outside this range, it may still be correct, but warrants investigation

### 5. Character-by-Character Validation
**Purpose**: Ensure escape sequence parsing is correct

**Test Approach**:
Create a debug function that shows the parsing process for a given string

```python
def debug_parse(line):
    """Show step-by-step parsing of a string literal"""
    print(f"\nParsing: {line}")
    print(f"Code characters: {len(line)}")

    content = line[1:-1]
    print(f"Content (no quotes): {content}")

    memory_chars = []
    i = 0
    while i < len(content):
        if content[i] == '\\' and i + 1 < len(content):
            next_char = content[i + 1]
            if next_char == '\\':
                memory_chars.append('\\')
                print(f"  [{i}:{i+2}] '\\\\' -> '\\'")
                i += 2
            elif next_char == '"':
                memory_chars.append('"')
                print(f"  [{i}:{i+2}] '\\"' -> '\"'")
                i += 2
            elif next_char == 'x':
                hex_code = content[i+2:i+4]
                memory_chars.append(f'<{hex_code}>')
                print(f"  [{i}:{i+4}] '\\x{hex_code}' -> <hex>")
                i += 4
        else:
            memory_chars.append(content[i])
            print(f"  [{i}] '{content[i]}' -> '{content[i]}'")
            i += 1

    print(f"Memory characters: {len(memory_chars)}")
    print(f"Difference: {len(line) - len(memory_chars)}")
```

## Test Execution Plan

### Phase 1: Unit Tests
1. Run example test cases
2. Run edge case tests
3. Verify each test passes individually

### Phase 2: Sample Validation
1. Manually verify 3-5 complex lines from input
2. Use debug_parse() to understand parsing
3. Confirm calculations are correct

### Phase 3: Integration Test
1. Run against full input.md
2. Verify result is reasonable
3. Check for any unexpected errors

### Phase 4: Spot Checks
1. Use debug_parse() on 5-10 randomly selected lines from input
2. Manually verify the character counts make sense
3. Confirm no obvious parsing errors

**Optional Automated Spot Check**:
```python
import random

def automated_spot_check():
    lines = read_input('input.md')
    sample_lines = random.sample(list(enumerate(lines, 1)), 5)

    print("\n=== Spot Check: 5 Random Lines ===")
    for line_num, line in sample_lines:
        code = count_code_chars(line)
        memory = count_memory_chars(line)
        print(f"\nLine {line_num}: {line[:50]}{'...' if len(line) > 50 else ''}")
        print(f"  Code: {code}, Memory: {memory}, Diff: {code - memory}")
        # Use debug_parse if needed for detailed analysis
```

## Expected Results Validation

### Reasonableness Checks
For the 300-line input:
- Average line length: ~30-40 characters
- Each line has minimum 2 quotes (diff of at least 2)
- Most lines have 2-5 escape sequences
- Expected average difference per line: ~4-6 characters
- **Expected total range: 1200-1800**

### Common Mistakes to Watch For
1. **Off-by-one errors**: Forgetting to skip all 4 characters in `\x##`
2. **Not removing quotes**: Including opening/closing quotes in memory count
3. **Wrong escape handling**: Treating `\\` as 2 characters instead of 1
4. **Index overflow**: Not checking bounds when looking ahead for escape sequences
5. **String escaping in tests**: Using regular strings instead of raw strings in test cases, causing Python to process escapes before the test runs
6. **Double-counting in invalid escapes**: Processing the same character twice when handling unexpected escape sequences

## Success Criteria
- ✓ All example tests pass with expected combined difference of 12
- ✓ All edge cases pass (including consecutive hex escapes)
- ✓ Sample lines from actual input verified manually
- ✓ Full input produces result in range [1200, 1800]
- ✓ No runtime errors or exceptions
- ✓ Result is a single integer value
- ✓ All test strings use raw string literals (r"...") to avoid confusion

## Final Answer Verification
Once the solution is run and produces a final answer, that answer should be:
1. Recorded for future reference
2. Verified against Advent of Code if possible (submit and check if correct)
3. Used as the expected value in a final assertion test

```python
def test_final_answer():
    """Test against the known correct answer (once determined)"""
    result = test_full_input()
    # TODO: Replace None with actual correct answer once known
    EXPECTED_ANSWER = None  # e.g., 1371
    if EXPECTED_ANSWER is not None:
        assert result == EXPECTED_ANSWER, f"Expected {EXPECTED_ANSWER}, got {result}"
        print(f"✓ CORRECT ANSWER: {result}")
    else:
        print(f"Answer to verify: {result}")
```

## Debugging Strategy
If tests fail:
1. **Verify test string format**: Ensure test strings use raw literals (r"...")
2. Use `debug_parse()` on failing test case to see step-by-step parsing
3. Check escape sequence detection logic (especially the if-elif chain)
4. Verify index advancement (2 for `\\` and `\"`, 4 for `\x##`, 1 for regular)
5. Print intermediate values (i, content[i], memory_count) to trace execution
6. Test simpler substrings to isolate the issue
7. Manually count expected characters and compare with actual

## Performance Testing (Optional)
While not critical for this input size, it's good practice to verify efficiency:

```python
import time

def test_performance():
    start_time = time.time()
    result = test_full_input()
    elapsed_time = time.time() - start_time

    print(f"\n=== Performance ===")
    print(f"Execution time: {elapsed_time:.4f} seconds")
    assert elapsed_time < 1.0, f"Solution too slow: {elapsed_time:.4f}s"
    print("✓ Solution runs efficiently (< 1 second)")
```
