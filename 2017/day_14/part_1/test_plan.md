# Testing Plan: Disk Defragmentation Grid Analysis

## Testing Philosophy
We need to verify correctness at multiple levels:
1. Individual component functions (unit tests)
2. Integration between components
3. Known example validation
4. Actual puzzle input validation

Since this is a script to solve a specific problem (not production code), we focus on:
- Correctness of the algorithm
- Validation against known test cases
- Edge cases specific to the problem domain
- No need for extensive error handling or input validation beyond the given input

## Test Strategy Overview

### 1. Unit Tests (Component Level)
Test each function individually with known inputs/outputs

### 2. Integration Tests
Test the full pipeline with the example case

### 3. Validation Tests
Verify against the provided example and actual input

## Detailed Test Cases

### Test Group 1: Knot Hash Validation
**Purpose**: Ensure knot hash implementation is correct (already tested in Day 10, but verify here)

**Test Case 1.1: Known Hash Values**
- **Test 1.1a**: Empty string hash
  - Input: `''` (empty string)
  - Expected: `a2582a3a0e66e6e86e3812dcb672a272`
  - Action: Compute `compute_knot_hash('')`
  - Validation: Exact match with known hash value
  - Purpose: Verify knot hash algorithm is implemented correctly

- **Test 1.1b**: Format validation
  - Input: `flqrgnkx-0`
  - Action: Compute `compute_knot_hash('flqrgnkx-0')` and verify format
  - Validation:
    - Output is string
    - Length is exactly 32 characters
    - All characters are valid hex (0-9, a-f)
    - All characters are lowercase

**Test Case 1.2: Hash Consistency**
- Input: Same string twice
- Expected: Identical outputs
- Action: Compute hash of `jxqlasbh-0` twice
- Validation: Results must be identical (deterministic)

**Test Case 1.3: Hash Uniqueness**
- Input: Different row numbers
- Expected: Different hashes
- Action: Compute hashes for `jxqlasbh-0`, `jxqlasbh-1`, `jxqlasbh-2`
- Validation: All three hashes should be different

### Test Group 2: Hex to Binary Conversion
**Purpose**: Verify correct conversion from hex to binary

**Test Case 2.1: Simple Hex Values**
- Test inputs and expected outputs (function works with any hex string length):
  - `'0'` → `'0000'` (single char: 4 bits)
  - `'f'` → `'1111'` (single char: all ones)
  - `'a'` → `'1010'` (single char: mixed)
  - `'00'` → `'00000000'` (two chars: 8 bits)
  - `'ff'` → `'11111111'` (two chars: 8 bits)
- Purpose: Verify character-by-character conversion works correctly

**Test Case 2.2: Full Hash Conversion**
- Input: 32-character hex string (all zeros)
- Expected: 128-character binary string (all zeros)
- Test: `hex_to_binary('0' * 32)` → `'0' * 128`
- Validation: Length exactly 128

**Test Case 2.3: Full Hash Conversion (all ones)**
- Input: `'f' * 32`
- Expected: `'1' * 128`
- Validation: Length exactly 128, all ones

**Test Case 2.4: Mixed Hex String**
- Input: `'a0c2'` (first 4 chars from example)
- Expected: `'1010000011000010'` (16 bits)
- Validation: Correct bit pattern, proper length

**Test Case 2.5: Leading Zeros Preservation**
- Input: `'0' + 'f' * 31` (starts with 0)
- Expected: Should start with `'0000'` (not strip leading zeros)
- Validation: First 4 bits are `'0000'`

### Test Group 3: Row Input Generation
**Purpose**: Verify correct formatting of row inputs

**Test Case 3.1: First Row**
- Input: key=`'jxqlasbh'`, row=0
- Expected: `'jxqlasbh-0'`
- Validation: Exact string match

**Test Case 3.2: Last Row**
- Input: key=`'jxqlasbh'`, row=127
- Expected: `'jxqlasbh-127'`
- Validation: Exact string match

**Test Case 3.3: Example Key**
- Input: key=`'flqrgnkx'`, row=0
- Expected: `'flqrgnkx-0'`
- Validation: Exact string match

**Test Case 3.4: Format Consistency**
- Action: Generate inputs for rows 0, 10, 100
- Validation:
  - All contain hyphen separator
  - No extra whitespace
  - Correct row number in string

### Test Group 4: Bit Counting
**Purpose**: Verify accurate counting of '1' bits

**Test Case 4.1: All Zeros**
- Input: `'0' * 128`
- Expected: 0
- Validation: Count is exactly 0

**Test Case 4.2: All Ones**
- Input: `'1' * 128`
- Expected: 128
- Validation: Count is exactly 128

**Test Case 4.3: Mixed Pattern**
- Input: `'10' * 64` (alternating)
- Expected: 64
- Validation: Count is exactly 64

**Test Case 4.4: Single One**
- Input: `'0' * 127 + '1'`
- Expected: 1
- Validation: Count is exactly 1

**Test Case 4.5: Known Binary String**
- Input: `'10100000110000100000000101110000'` (32-bit example)
- Expected: 9 (count the ones: positions 0,2,8,9,13,24,26,27,28)
- Action: Count and verify
- Note: Corrected count - there are 9 ones in this string, not 7

### Test Group 5: Integration Testing
**Purpose**: Test the complete pipeline with known example

**Test Case 5.1: Example Key - Full Computation**
- Input: key = `'flqrgnkx'`
- Expected output: 8108 used squares
- Process:
  1. Generate all 128 row inputs
  2. Compute hash for each row
  3. Convert each hash to binary
  4. Count ones in each binary string
  5. Sum all counts
- Validation: Final result must be exactly 8108

**Test Case 5.2: First Row of Example**
- Input: `'flqrgnkx-0'`
- Process:
  1. Compute hash
  2. Convert to binary
  3. Count ones
- Validation:
  - Binary string length is 128
  - Count is reasonable (between 0 and 128)

**Test Case 5.3: Multiple Rows Summation**
- Input: key = `'flqrgnkx'`, rows 0-9 only
- Process: Compute used squares for first 10 rows
- Validation:
  - Result is non-negative integer
  - Result is <= 1280 (10 rows × 128 bits max)
  - Can be used as partial validation

### Test Group 6: Actual Input Validation
**Purpose**: Verify solution works with actual puzzle input

**Test Case 6.1: Input File Reading**
- Action: Read `input.md`
- Validation:
  - File exists and is readable
  - Content is `'jxqlasbh'` (stripped of whitespace)
  - No extra characters or newlines after stripping

**Test Case 6.2: Full Solution with Actual Input**
- Input: key = `'jxqlasbh'`
- Process: Run full calculation
- Validation:
  - Result is non-negative integer
  - Result is <= 16384 (128 rows × 128 bits max)
  - Result is > 0 (statistically very unlikely to be 0)
  - Result is reasonable (likely in range 6000-10000 based on expected hash distribution)

### Test Group 7: Edge Cases and Boundary Conditions
**Purpose**: Test potential edge cases

**Test Case 7.1: First and Last Rows**
- Input: Rows 0 and 127
- Validation: Both compute successfully without errors

**Test Case 7.2: Hash Distribution**
- Action: Compute hashes for all 128 rows
- Validation:
  - No duplicate hashes (statistical check - very unlikely to have duplicates)
  - All hashes are valid 32-char hex strings

**Test Case 7.3: Binary String Properties**
- Action: Convert several hashes to binary
- Validation:
  - All binary strings are exactly 128 bits
  - All contain only '0' and '1' characters
  - No unexpected characters or formatting

**Test Case 7.4: Count Accumulation**
- Process: Track running total as we process rows
- Validation:
  - Total never decreases
  - Total increases by reasonable amounts (0-128 per row)
  - Final total is sum of all individual row counts

## Test Implementation Strategy

### Structure in solution.py

```python
# Test functions
def test_knot_hash():
    """Test knot hash implementation with known value"""
    # Test case 1.1a - verify algorithm correctness
    result = compute_knot_hash('')
    expected = 'a2582a3a0e66e6e86e3812dcb672a272'
    assert result == expected, f"Knot hash failed: expected {expected}, got {result}"

    # Test case 1.1b - verify format for actual input
    result = compute_knot_hash('flqrgnkx-0')
    assert isinstance(result, str), "Hash must be string"
    assert len(result) == 32, f"Hash must be 32 chars, got {len(result)}"
    assert all(c in '0123456789abcdef' for c in result), "Hash must be lowercase hex"

    print("✓ Knot hash tests passed")

def test_hex_to_binary():
    """Test hex to binary conversion"""
    # Test cases 2.1 - single and multi-character hex strings
    assert hex_to_binary('0') == '0000', "Single '0' failed"
    assert hex_to_binary('f') == '1111', "Single 'f' failed"
    assert hex_to_binary('a') == '1010', "Single 'a' failed"
    assert hex_to_binary('00') == '00000000', "Double '00' failed"
    assert hex_to_binary('ff') == '11111111', "Double 'ff' failed"

    # Test case 2.2 - full hash with all zeros
    assert hex_to_binary('0' * 32) == '0' * 128, "All zeros failed"

    # Test case 2.3 - full hash with all ones
    assert hex_to_binary('f' * 32) == '1' * 128, "All ones failed"

    # Test case 2.4 - mixed hex string
    assert hex_to_binary('a0c2') == '1010000011000010', "Mixed hex failed"

    # Test case 2.5 - leading zeros preservation
    result = hex_to_binary('0' + 'f' * 31)
    assert result[:4] == '0000', "Leading zeros not preserved"
    assert len(result) == 128, f"Length should be 128, got {len(result)}"

    print("✓ Hex to binary conversion tests passed")

def test_generate_row_input():
    """Test row input generation"""
    # Test cases 3.1-3.4
    assert generate_row_input('jxqlasbh', 0) == 'jxqlasbh-0', "Row 0 failed"
    assert generate_row_input('jxqlasbh', 127) == 'jxqlasbh-127', "Row 127 failed"
    assert generate_row_input('flqrgnkx', 0) == 'flqrgnkx-0', "Example key failed"
    assert '-' in generate_row_input('test', 10), "Missing hyphen separator"

    print("✓ Row input generation tests passed")

def test_count_used_bits():
    """Test bit counting"""
    # Test cases 4.1-4.5
    assert count_used_bits('0' * 128) == 0, "All zeros should be 0"
    assert count_used_bits('1' * 128) == 128, "All ones should be 128"
    assert count_used_bits('10' * 64) == 64, "Alternating pattern failed"
    assert count_used_bits('0' * 127 + '1') == 1, "Single one failed"
    assert count_used_bits('10100000110000100000000101110000') == 9, "Known pattern failed"

    print("✓ Bit counting tests passed")

def test_example_case():
    """Test with known example"""
    # Test case 5.1
    result = calculate_used_squares('flqrgnkx')
    expected = 8108
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Example case passed: {result} used squares")

if __name__ == "__main__":
    print("Running tests...\n")

    print("Unit tests:")
    test_knot_hash()
    test_hex_to_binary()
    test_generate_row_input()
    test_count_used_bits()

    print("\nIntegration test:")
    test_example_case()

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)

    # Compute actual answer
    print("\nComputing answer for actual input...")
    with open('input.md', 'r') as f:
        key = f.read().strip()

    result = calculate_used_squares(key)

    print(f"\nFINAL ANSWER: {result}")
```

## Expected Test Results

### Success Criteria
1. All unit tests pass (functions work correctly in isolation)
2. Example case produces exactly 8108 used squares
3. Actual input produces a valid result (integer between 0 and 16384)
4. No runtime errors or exceptions
5. Reasonable execution time (<5 seconds for all tests)

### Debugging Strategy (if tests fail)

**If example case fails (result ≠ 8108)**:
1. Test knot hash for `flqrgnkx-0` separately
2. Verify hex to binary conversion for that hash
3. Count bits manually for first few rows
4. Check if issue is in accumulation or individual row computation

**If hex to binary fails**:
1. Test with single hex characters first
2. Verify leading zero preservation
3. Check length of output
4. Test with known hex patterns

**If bit counting fails**:
1. Print binary strings to verify content
2. Manually count for small examples
3. Check for unexpected characters in strings

**If actual input fails validation**:
1. Print the result to see what we got
2. Compare with example case to see if pattern is similar
3. Verify input file was read correctly
4. Re-run with verbose output to see intermediate values

## Test Execution Order

1. **First**: Run unit tests (fast, catch basic errors)
2. **Second**: Run example integration test (validates algorithm)
3. **Third**: Run actual input test (produces answer)
4. **Finally**: Display results

## Coverage Analysis

This test plan covers:
- ✅ All new functions (hex_to_binary, generate_row_input, count_used_bits, calculate_used_squares)
- ✅ Knot hash correctness (via example case validation)
- ✅ Boundary conditions (first/last rows, min/max values)
- ✅ Integration (full pipeline with known example)
- ✅ Actual input (real puzzle)
- ✅ Edge cases (all zeros, all ones, leading zeros)
- ✅ Format validation (string lengths, character sets)

We do NOT need to test:
- ❌ Invalid inputs (not part of the problem)
- ❌ File I/O errors (assume input file exists and is valid)
- ❌ Network or external dependencies (none exist)
- ❌ Concurrency or race conditions (single-threaded script)
- ❌ Memory limits (problem size is fixed and small)
- ❌ Different input formats (only one input format specified)
