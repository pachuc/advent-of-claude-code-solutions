# Test Plan: Knot Hash Algorithm - Full Implementation (Part 2)

## Overview
The test plan validates each component of the Knot Hash algorithm and verifies against known examples. Since Part 2 builds on Part 1's core algorithm, we can leverage confidence in the circular reversal logic while focusing on new components.

## Test Strategy

### 1. Unit Tests (Component-Level)
Test each function independently with known inputs/outputs

### 2. Integration Tests (Example-Based)
Verify complete hash computation against provided examples

### 3. Validation Tests (Actual Input)
Ensure the actual puzzle input produces a valid 32-character hex hash

## Detailed Test Cases

### Test 1: ASCII Input Parsing
**Function**: `parse_input_as_ascii()`

**Test Case 1.1**: Simple string "1,2,3"
```python
def test_parse_simple_ascii():
    input_str = "1,2,3"
    result = parse_input_as_ascii(input_str)

    # Expected ASCII codes
    expected_ascii = [49, 44, 50, 44, 51]  # '1', ',', '2', ',', '3'
    expected_with_suffix = [49, 44, 50, 44, 51, 17, 31, 73, 47, 23]

    assert result == expected_with_suffix
    print("✓ Simple ASCII parsing passed")
```

**Test Case 1.2**: Empty string
```python
def test_parse_empty_ascii():
    input_str = ""
    result = parse_input_as_ascii(input_str)

    # Should only have suffix
    expected = [17, 31, 73, 47, 23]

    assert result == expected
    print("✓ Empty string ASCII parsing passed")
```

**Test Case 1.3**: Whitespace handling
```python
def test_parse_ascii_whitespace():
    # Input with leading/trailing whitespace
    input_str = "  AoC 2017  "
    result = parse_input_as_ascii(input_str)

    # Should strip whitespace
    # 'AoC 2017' → [65, 111, 67, 32, 50, 48, 49, 55]
    expected_ascii = [65, 111, 67, 32, 50, 48, 49, 55]
    expected_with_suffix = expected_ascii + [17, 31, 73, 47, 23]

    assert result == expected_with_suffix
    print("✓ Whitespace handling passed")
```

**Test Case 1.4**: Actual puzzle input
```python
def test_parse_actual_input():
    input_str = "130,126,1,11,140,2,255,207,18,254,246,164,29,104,0,224"
    result = parse_input_as_ascii(input_str)

    # Verify it starts with ASCII codes
    assert result[0] == ord('1')  # '1' = 49
    assert result[1] == ord('3')  # '3' = 51
    assert result[2] == ord('0')  # '0' = 48

    # Verify suffix is appended
    assert result[-5:] == [17, 31, 73, 47, 23]

    # Verify length (59 chars + 5 suffix = 64)
    assert len(result) == 64

    print("✓ Actual input parsing passed")
```

**Edge Cases to Consider**:
- Empty string (only suffix)
- String with whitespace
- Special characters (ensure all ASCII values 0-255 handled)

---

### Test 2: Multi-Round Knot Hash
**Function**: `knot_hash_rounds()`

**Test Case 2.1**: State persistence across rounds
```python
def test_state_persistence():
    # Use simple case to verify state carries over
    lengths = [17, 31, 73, 47, 23]  # Just the suffix

    # Run for 2 rounds
    result = knot_hash_rounds(lengths, num_rounds=2, list_size=256)

    # Verify it's a valid permutation
    assert len(result) == 256
    assert sorted(result) == list(range(256))

    # The result should differ from single round
    single_round = knot_hash_rounds(lengths, num_rounds=1, list_size=256)
    assert result != single_round, "State should carry across rounds"

    print("✓ State persistence test passed")
```

**Test Case 2.2**: 64 rounds produce valid permutation
```python
def test_64_rounds_validity():
    lengths = [65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]
    result = knot_hash_rounds(lengths, num_rounds=64)

    # Must still be a valid permutation
    assert len(result) == 256
    assert sorted(result) == list(range(256))
    assert set(result) == set(range(256))

    print("✓ 64 rounds validity test passed")
```

**Critical Verification**:
- current_position and skip_size increment continuously (not reset)
- After 64 rounds, list is still a permutation of [0-255]
- No elements are lost or duplicated

---

### Test 3: Dense Hash Creation
**Function**: `create_dense_hash()`

**Test Case 3.1**: Known XOR example from problem
```python
def test_dense_hash_xor():
    # Example from problem statement
    sparse_block = [65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]

    # Create sparse hash with this as first block
    sparse_hash = sparse_block + [0] * 240  # Fill rest with zeros

    dense = create_dense_hash(sparse_hash)

    # First element should be 64 (from problem statement)
    expected_first = 65 ^ 27 ^ 9 ^ 1 ^ 4 ^ 3 ^ 40 ^ 50 ^ 91 ^ 7 ^ 6 ^ 0 ^ 2 ^ 5 ^ 68 ^ 22
    assert expected_first == 64, f"Expected 64, calculated {expected_first}"
    assert dense[0] == 64

    # Verify length
    assert len(dense) == 16

    # All other blocks XOR to 0 (since all elements are 0)
    for i in range(1, 16):
        assert dense[i] == 0

    print("✓ Dense hash XOR test passed")
```

**Test Case 3.2**: All same values
```python
def test_dense_hash_uniform():
    # Sparse hash with all 255s
    sparse_hash = [255] * 256
    dense = create_dense_hash(sparse_hash)

    # 16 values XORed together (even count) → 0
    # 255 ^ 255 = 0, repeated 8 times
    for val in dense:
        assert val == 0

    print("✓ Dense hash uniform values test passed")
```

**Test Case 3.3**: Alternating values
```python
def test_dense_hash_alternating():
    # Sparse hash alternating 0 and 255
    sparse_hash = [0, 255] * 128
    dense = create_dense_hash(sparse_hash)

    # Each block has 8 zeros and 8 255s
    # 0 ^ 255 ^ 0 ^ 255 ... (16 times) = 0
    for val in dense:
        assert val == 0

    print("✓ Dense hash alternating test passed")
```

**Edge Cases**:
- All zeros → dense hash all zeros
- All same values → XOR result based on count
- Known XOR calculation from problem

---

### Test 4: Hexadecimal Conversion
**Function**: `to_hex_string()`

**Test Case 4.1**: Basic conversion
```python
def test_hex_conversion_basic():
    dense = [64, 7, 255]
    result = to_hex_string(dense)

    # 64 = 0x40, 7 = 0x07, 255 = 0xff
    assert result.startswith("4007ff")

    print("✓ Basic hex conversion passed")
```

**Test Case 4.2**: Leading zeros
```python
def test_hex_conversion_leading_zeros():
    dense = [0, 1, 15, 16, 255]
    result = to_hex_string(dense)

    # Must have leading zeros
    # 0=00, 1=01, 15=0f, 16=10, 255=ff
    assert result.startswith("00010f10ff")

    print("✓ Hex leading zeros test passed")
```

**Test Case 4.3**: Full 16-element conversion
```python
def test_hex_conversion_full():
    dense = list(range(16))  # [0, 1, 2, ..., 15]
    result = to_hex_string(dense)

    # Should be "000102030405060708090a0b0c0d0e0f"
    expected = "000102030405060708090a0b0c0d0e0f"
    assert result == expected
    assert len(result) == 32

    print("✓ Full hex conversion test passed")
```

**Test Case 4.4**: Lowercase verification
```python
def test_hex_lowercase():
    dense = [10, 11, 12, 13, 14, 15]  # a, b, c, d, e, f
    result = to_hex_string(dense)

    # Must be lowercase
    assert "A" not in result
    assert "B" not in result
    assert "a" in result or "b" in result  # Has lowercase letters

    print("✓ Hex lowercase test passed")
```

**Edge Cases**:
- Value 0 → "00"
- Value 255 → "ff"
- Values 10-15 → "0a" through "0f" (lowercase)
- Exactly 32 characters output

---

### Test 5: Complete Hash Examples
**Function**: `compute_knot_hash()`

**Test Case 5.1**: Empty string
```python
def test_example_empty_string():
    input_str = ""
    result = compute_knot_hash(input_str)
    expected = "a2582a3a0e66e6e86e3812dcb672a272"

    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 32
    print("✓ Empty string example passed")
```

**Test Case 5.2**: "AoC 2017"
```python
def test_example_aoc_2017():
    input_str = "AoC 2017"
    result = compute_knot_hash(input_str)
    expected = "33efeb34ea91902bb2f59c9920caa6cd"

    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 32
    print("✓ 'AoC 2017' example passed")
```

**Test Case 5.3**: "1,2,3"
```python
def test_example_1_2_3():
    input_str = "1,2,3"
    result = compute_knot_hash(input_str)
    expected = "3efbe78a8d82f29979031a4aa0b16a9d"

    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 32
    print("✓ '1,2,3' example passed")
```

**Test Case 5.4**: "1,2,4"
```python
def test_example_1_2_4():
    input_str = "1,2,4"
    result = compute_knot_hash(input_str)
    expected = "63960835bcdc130f0b66d7ff4f6a5a8e"

    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 32
    print("✓ '1,2,4' example passed")
```

**Critical Verification**:
These tests validate the entire pipeline against known outputs. If all pass, the implementation is correct.

---

### Test 6: Actual Puzzle Input Validation
**Function**: Full solution with actual input

**Test Case 6.1**: Read and process actual input
```python
def test_actual_puzzle_input():
    with open('input.md', 'r') as f:
        input_string = f.read()

    result = compute_knot_hash(input_string)

    # Validation checks (no known answer yet)
    assert isinstance(result, str), "Result must be string"
    assert len(result) == 32, f"Result must be 32 chars, got {len(result)}"

    # Verify hex format
    valid_hex_chars = set('0123456789abcdef')
    assert all(c in valid_hex_chars for c in result), "Invalid hex characters"

    # Verify lowercase
    assert result == result.lower(), "Hash must be lowercase"

    print(f"Actual input hash: {result}")
    print("✓ Actual puzzle input validation passed")

    return result
```

**Test Case 6.2**: Input parsing verification
```python
def test_actual_input_details():
    with open('input.md', 'r') as f:
        input_string = f.read()

    # The input should be treated as raw string
    stripped = input_string.strip()

    # Verify what we're hashing
    print(f"Input string: '{stripped}'")
    print(f"Input length: {len(stripped)}")
    print(f"First char: '{stripped[0]}' (ASCII {ord(stripped[0])})")
    print(f"Last char: '{stripped[-1]}' (ASCII {ord(stripped[-1])})")

    # Parse as ASCII
    lengths = parse_input_as_ascii(input_string)
    print(f"Length sequence size: {len(lengths)}")
    print(f"First 5 lengths: {lengths[:5]}")
    print(f"Last 5 lengths (suffix): {lengths[-5:]}")

    assert lengths[-5:] == [17, 31, 73, 47, 23], "Suffix not appended correctly"

    print("✓ Actual input details verified")
```

---

## Test Execution Strategy

**Recommended order** (unit tests → examples → actual input):

1. **ASCII parsing tests** - Catch input conversion errors early
2. **Hex conversion tests** - Simple output formatting validation
3. **Dense hash tests** - XOR logic verification
4. **Multi-round tests** - State persistence validation
5. **Example tests** - Full pipeline with known outputs (most important!)
6. **Actual input test** - Final solution

**Why this order?** Running the 4 example tests (#5) is the most critical validation step. If all examples pass, the solution is virtually guaranteed correct. Unit tests (#1-4) help debug if examples fail.

## Success Criteria

The solution is correct if:
1. ✓ All 4 provided examples produce exact matching hashes
2. ✓ Actual input produces a valid 32-character lowercase hex string
3. ✓ All unit tests pass (parsing, XOR, hex conversion)
4. ✓ State persistence verified (no reset between rounds)

## Common Issues and Debugging

### Issue 1: Wrong hash on examples
**Likely causes**:
- Resetting current_position or skip_size between rounds
- Not appending standard suffix
- Parsing input as integers instead of ASCII

**Debug strategy**:
- Print sparse hash after 64 rounds
- Print dense hash before hex conversion
- Verify length sequence includes suffix

### Issue 2: Invalid hex output
**Likely causes**:
- Using uppercase hex (use '02x' not '02X')
- Missing leading zeros (use format width '02')
- Wrong dense hash length (should be exactly 16)

**Debug strategy**:
- Print each dense hash value and its hex conversion
- Verify dense hash has exactly 16 elements

### Issue 3: Wrong XOR calculation
**Likely causes**:
- Using wrong operator (+ instead of ^)
- Wrong block boundaries (should be 16 elements per block)

**Debug strategy**:
- Manually calculate XOR for first block
- Print each block before XORing

## Test Suite Structure

**Recommended test execution order**:

```python
if __name__ == "__main__":
    print("Running Knot Hash Part 2 Tests\n")

    # Unit tests
    print("Testing ASCII parsing...")
    test_parse_simple_ascii()
    test_parse_empty_ascii()
    test_parse_ascii_whitespace()
    test_parse_actual_input()

    print("\nTesting hex conversion...")
    test_hex_conversion_basic()
    test_hex_conversion_leading_zeros()
    test_hex_conversion_full()
    test_hex_lowercase()

    print("\nTesting dense hash...")
    test_dense_hash_xor()
    test_dense_hash_uniform()
    test_dense_hash_alternating()

    print("\nTesting multi-round logic...")
    test_state_persistence()
    test_64_rounds_validity()

    # Integration tests with examples
    print("\nTesting examples...")
    test_example_empty_string()
    test_example_aoc_2017()
    test_example_1_2_3()
    test_example_1_2_4()

    # Actual input
    print("\nTesting actual puzzle input...")
    test_actual_input_details()
    result = test_actual_puzzle_input()

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print(f"FINAL ANSWER: {result}")
    print("="*50)
```

**Note**: The verbose output helps with debugging. You can simplify this further if desired, but the structure above provides good visibility into test progress.

## Performance Notes

**Expected runtime**: < 500ms for all tests

**Note**: Performance testing is not required for this puzzle script. The algorithm has O(1) complexity for fixed input size and will complete quickly. This section is informational only.

## Edge Cases Summary

| Category | Edge Case | Expected Behavior |
|----------|-----------|-------------------|
| Input | Empty string | Only suffix, hash: a2582a3a... |
| Input | Whitespace | Strip before processing |
| Input | Long input | Handle any ASCII string |
| Hash | All zeros | Valid hash (not all '00') |
| Hash | Same rounds | Deterministic result |
| XOR | Even count | Can result in 0 |
| Hex | Value 0-15 | Leading zero required |
| Hex | Value 255 | Converts to 'ff' |

## Final Validation Checklist

Before submitting the solution:
- [ ] All 4 example hashes match exactly
- [ ] Actual input produces 32-character lowercase hex string
- [ ] No uppercase letters in output
- [ ] All hex values have exactly 2 digits
- [ ] Hash is deterministic (same input → same output)
- [ ] No errors or warnings during execution
- [ ] Code completes in under 1 second
