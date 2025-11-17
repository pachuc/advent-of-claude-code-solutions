# Test Plan - Dragon Curve Checksum Part 2

## Testing Strategy
The solution for Part 2 uses the same algorithm as Part 1 with a larger input size. We'll verify correctness through incremental testing and validate the final answer.

## 0. Input Validation

### Test 0.1: Verify Input File
**Purpose:** Ensure input.md contains the expected initial state

**Verification:**
```python
initial_state = read_input('input.md')
assert initial_state == '11011110011011101'
assert len(initial_state) == 17
assert all(c in '01' for c in initial_state)
```

## 1. Verify Part 1 Test Cases Still Work

### Test 1.1: Small Example from Problem Description
**Purpose:** Verify dragon curve generation with the documented example

**Input:**
- Initial state: `1`
- Disk length: 3

**Expected behavior:**
- After 1 iteration: `100`
- Truncated to 3: `100`

**Verification:**
```python
assert dragon_curve_step('1') == '100'
assert generate_data('1', 3) == '100'
```

### Test 1.2: Another Small Example
**Purpose:** Verify multi-step generation

**Input:**
- Initial state: `0`
- Disk length: 3

**Expected:**
- After 1 iteration: `001`

**Verification:**
```python
assert dragon_curve_step('0') == '001'
assert generate_data('0', 3) == '001'
```

### Test 1.3: Longer Example
**Purpose:** Verify the example from problem description

**Input:**
- Initial state: `11111`

**Expected:**
- After 1 iteration: `11111000000`

**Verification:**
```python
assert dragon_curve_step('11111') == '11111000000'
```

### Test 1.4: Complete Example from Problem
**Purpose:** Verify the full workflow with disk length 20

**Input:**
- Initial state: `10000`
- Disk length: 20

**Expected:**
- Final data (truncated): `10000011110010000111`
- Final checksum: `01100`

**Verification:**
```python
data = generate_data('10000', 20)
assert data == '10000011110010000111'
checksum = compute_final_checksum(data)
assert checksum == '01100'
```

## 2. Verify Checksum Logic

### Test 2.1: Checksum Step Function
**Purpose:** Verify single checksum iteration works correctly

**Test cases:**
```python
# Matching pairs -> 1, different pairs -> 0
assert calculate_checksum_step('110010110100') == '110101'
assert calculate_checksum_step('110101') == '100'

# All matching
assert calculate_checksum_step('1111') == '11'
assert calculate_checksum_step('0000') == '11'

# All different
assert calculate_checksum_step('1010') == '00'
```

### Test 2.2: Odd-Length Termination
**Purpose:** Verify checksum stops at odd length

**Test cases:**
```python
# Length 4 -> 2 -> 1 (odd, stop)
data = '1100'
checksum = compute_final_checksum(data)
assert len(checksum) % 2 == 1

# Length 12 -> 6 -> 3 (odd, stop)
data = '110010110100'
checksum = compute_final_checksum(data)
assert checksum == '100'
assert len(checksum) == 3
```

## 3. Validate Part 1 Answer

### Test 3.1: Reproduce Part 1 Result
**Purpose:** Ensure our code produces the known correct answer for Part 1

**Input:**
- Initial state: `11011110011011101` (from input.md)
- Disk length: 272

**Expected output:**
- `00000100100001100` (from part_1_answer.txt)

**Verification:**
```python
result = solve('input.md', disk_length=272)
assert result == '00000100100001100'
```

**Status:** CRITICAL - Must pass before attempting Part 2

## 4. Performance Testing

### Test 4.1: Verify Iteration Count
**Purpose:** Confirm the number of dragon curve iterations needed

**Expected:**
- Starting length: 17
- Target length: 35_651_584
- After n iterations: length ≈ 17 × 2^n
- Need: 17 × 2^n ≥ 35_651_584, so 2^n ≥ 2_097_152 ≈ 2^21
- Iterations needed: ~21

**Verification:**
```python
data = '11011110011011101'
iterations = 0
while len(data) < 35_651_584:
    data = dragon_curve_step(data)
    iterations += 1
print(f"Iterations needed: {iterations}")
assert iterations >= 20  # Should be exactly 21
assert iterations <= 22
```

### Test 4.2: Runtime Check
**Purpose:** Ensure solution completes in reasonable time

**Expected runtime:** < 10 seconds (likely 2-5 seconds)

**Verification:**
```python
import time
start = time.time()
result = solve('input.md', disk_length=35_651_584)
elapsed = time.time() - start
print(f"Runtime: {elapsed:.2f} seconds")
assert elapsed < 10  # Should complete quickly
if elapsed > 5:
    print("Warning: Runtime slower than expected")
```

## 5. Edge Cases and Correctness

### Test 5.1: Truncation Works Correctly
**Purpose:** Verify data is truncated to exact disk length

**Verification:**
```python
data = generate_data('11011110011011101', 35_651_584)
assert len(data) == 35_651_584
assert all(c in '01' for c in data)  # Only binary digits
```

### Test 5.1b: Truncation Edge Case
**Purpose:** Verify truncation behavior when exceeding disk length

**Verification:**
```python
# Generate more data than needed and verify truncation
data = generate_data('1', 10)
assert len(data) == 10
# Verify it's truncated from a longer sequence
full_data = '1'
while len(full_data) < 10:
    full_data = dragon_curve_step(full_data)
assert data == full_data[:10]
```

### Test 5.2: Checksum Properties
**Purpose:** Verify checksum output properties

**Expected:**
- Checksum length is odd
- Checksum contains only '0' and '1'
- For disk_length = 35_651_584 = 2^21 × 17, expect final checksum length = 17

**Verification:**
```python
result = solve('input.md', disk_length=35_651_584)
assert len(result) % 2 == 1  # Odd length
assert all(c in '01' for c in result)  # Binary string
assert len(result) < 30  # Should be exactly 17
print(f"Checksum length: {len(result)}")
print(f"Expected length: 17 (from factorization 35_651_584 = 2^21 × 17)")
assert len(result) == 17  # Exact expected length
```

### Test 5.3: Bit Flipping Correctness
**Purpose:** Verify bit flipping works correctly

**Test cases:**
```python
# Test the bit flipping logic used in dragon_curve_step
def flip_bits(s):
    return ''.join('1' if c == '0' else '0' for c in s)

assert flip_bits('0') == '1'
assert flip_bits('1') == '0'
assert flip_bits('101010') == '010101'
assert flip_bits('11110000') == '00001111'
assert flip_bits('11011110011011101') == '00100001100100010'
```

## 6. Final Validation

### Test 6.1: Run Complete Solution
**Purpose:** Execute the full Part 2 solution and verify output format

**Steps:**
1. Run the solution with disk_length=35_651_584
2. Verify output is a binary string
3. Verify output has odd length
4. Print the result for submission

**Verification:**
```python
result = solve('input.md', disk_length=35_651_584)
print(f"Part 2 Answer: {result}")
print(f"Answer length: {len(result)}")
print(f"Answer is odd length: {len(result) % 2 == 1}")
```

### Test 6.2: Sanity Checks
**Purpose:** Ensure answer makes sense

**Checks:**
- Result is not empty
- Result is different from Part 1 answer (different disk size)
- Result length is 17 (based on factorization)
- Both Part 1 and Part 2 checksums have odd length

**Verification:**
```python
result = solve('input.md', disk_length=35_651_584)
part1_answer = '00000100100001100'

assert len(result) > 0
assert result != part1_answer  # Different disk size -> different answer
assert len(result) == 17  # Expected from 35_651_584 = 2^21 × 17
assert len(part1_answer) == 17  # Part 1 also has length 17 (272 = 2^4 × 17)
print(f"Part 1 checksum length: {len(part1_answer)} (272 = 2^4 × 17)")
print(f"Part 2 checksum length: {len(result)} (35_651_584 = 2^21 × 17)")
print("Both checksums reduce to length 17!")
```

## Test Execution Order

1. **Input validation** (Test 0.1): Verify input file is correct
2. **Unit tests** (Tests 1.1 - 2.2): Verify individual functions
3. **Part 1 validation** (Test 3.1): MUST PASS - confirms correctness
4. **Performance tests** (Tests 4.1 - 4.2): Check efficiency
5. **Edge cases** (Tests 5.1 - 5.3): Verify robustness
6. **Final solution** (Tests 6.1 - 6.2): Get Part 2 answer

## Success Criteria

✅ All unit tests pass
✅ Part 1 answer is correctly reproduced
✅ Solution completes in < 10 seconds
✅ Final answer is an odd-length binary string of length 17
✅ Output format is valid for submission

## Notes

- The most important test is reproducing the Part 1 answer (Test 3.1) - this validates our implementation is correct
- Part 2 has no example answer to compare against, so we rely on algorithm correctness
- Performance should not be an issue - the Part 1 code is already optimal
- **Key insight**: Both disk lengths share a factor of 17:
  - Part 1: 272 = 2^4 × 17 → checksum length = 17
  - Part 2: 35_651_584 = 2^21 × 17 → checksum length = 17
  - This means both checksums will have the same length, though different values!
