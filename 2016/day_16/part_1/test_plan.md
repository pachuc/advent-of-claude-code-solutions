# Test Plan: Dragon Curve Checksum

## Testing Strategy

Since this is a script to solve a specific problem (not production code), testing will focus on:
1. Validating against provided examples
2. Testing individual components with known outputs
3. Verifying edge cases relevant to the algorithm
4. Confirming correct behavior with actual input

## Unit Tests for Individual Components

### Test 1: Dragon Curve Step Function

**Purpose**: Verify single iteration of dragon curve algorithm

**Test Cases**:

| Input          | Expected Output                |
|----------------|--------------------------------|
| `"1"`          | `"100"`                        |
| `"0"`          | `"001"`                        |
| `"11111"`      | `"11111000000"`                |
| `"111100001010"` | `"1111000010100101011110000"` |

**Verification Method**:
```python
def test_dragon_curve_step():
    assert dragon_curve_step("1") == "100"
    assert dragon_curve_step("0") == "001"
    assert dragon_curve_step("11111") == "11111000000"
    assert dragon_curve_step("111100001010") == "1111000010100101011110000"
```

**What we're testing**:
- Correct reversal of string
- Correct bit flipping (0→1, 1→0)
- Correct concatenation with separator "0"
- Works for various lengths

### Test 2: Data Generation Function

**Purpose**: Verify data generation expands and truncates correctly

**Test Cases**:

| Initial State | Disk Length | Expected Output Length | Notes |
|---------------|-------------|------------------------|-------|
| `"10000"`     | 20          | 20                     | From example |
| `"1"`         | 5           | 5                      | Small case |
| `"11111"`     | 11          | 11                     | Exact match after 1 iteration |
| `"10000"`     | 20          | 20                     | Requires truncation |

**Verification Method**:
```python
def test_generate_data():
    # Test from problem example
    result = generate_data("10000", 20)
    assert len(result) == 20
    assert result == "10000011110010000111"

    # Test various lengths
    result = generate_data("1", 5)
    assert len(result) == 5

    result = generate_data("11111", 11)
    assert len(result) == 11
    assert result == "11111000000"

    # Test edge case: initial state already meets disk length
    result = generate_data("10101", 5)
    assert len(result) == 5
    assert result == "10101"

    # Test edge case: initial state exceeds disk length
    result = generate_data("11111000000", 5)
    assert len(result) == 5
    assert result == "11111"
```

**What we're testing**:
- Loop continues until data >= disk_length
- Truncation produces exact length
- No off-by-one errors
- Works for different disk lengths
- Correctly handles edge case where initial state already meets or exceeds disk length

### Test 3: Single Checksum Step Function

**Purpose**: Verify one iteration of checksum calculation

**Test Cases**:

| Input              | Expected Output | Notes |
|--------------------|-----------------|-------|
| `"110010110100"`   | `"110101"`      | From example (length 12 → 6) |
| `"110101"`         | `"100"`         | From example (length 6 → 3) |
| `"11"`             | `"1"`           | Same pair |
| `"01"`             | `"0"`           | Different pair |
| `"1100"`           | `"10"`          | Two pairs |

**Verification Method**:
```python
def test_calculate_checksum_step():
    assert calculate_checksum_step("110010110100") == "110101"
    assert calculate_checksum_step("110101") == "100"
    assert calculate_checksum_step("11") == "1"
    assert calculate_checksum_step("01") == "0"
    assert calculate_checksum_step("1100") == "10"
```

**What we're testing**:
- Correct pairing (non-overlapping)
- Correct comparison logic (same → 1, different → 0)
- Output is exactly half input length
- Works for various lengths

### Test 4: Final Checksum Function

**Purpose**: Verify checksum loop terminates at odd length

**Test Cases**:

| Input                  | Expected Output | Iterations | Notes |
|------------------------|-----------------|------------|-------|
| `"110010110100"`       | `"100"`         | 2          | Length 12 → 6 → 3 |
| `"10000011110010000111"` | `"01100"`      | 2          | Length 20 → 10 → 5 |

**Verification Method**:
```python
def test_compute_final_checksum():
    # From problem examples
    result = compute_final_checksum("110010110100")
    assert result == "100"
    assert len(result) % 2 == 1  # Must be odd

    result = compute_final_checksum("10000011110010000111")
    assert result == "01100"
    assert len(result) % 2 == 1  # Must be odd
```

**What we're testing**:
- Loop continues while length is even
- Stops when length becomes odd
- Produces correct final result
- Termination guarantee

## Integration Tests

### Test 5: Complete Example from Problem

**Purpose**: Validate end-to-end solution with provided example

**Test Case**:
- Initial state: `"10000"`
- Disk length: 20
- Expected checksum: `"01100"`

**Verification Method**:
```python
import tempfile
import os

def test_complete_example():
    # Create temporary test input using tempfile for proper cleanup
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("10000")
        temp_path = f.name

    try:
        result = solve(temp_path, disk_length=20)
        assert result == "01100"
        assert len(result) % 2 == 1
    finally:
        os.unlink(temp_path)  # Clean up temporary file
```

**What we're testing**:
- Full pipeline: read → generate → checksum
- Matches expected output from problem
- Confirms algorithm correctness
- Proper file cleanup with tempfile module

### Test 6: Actual Input

**Purpose**: Verify solution works with actual puzzle input

**Test Case**:
- Initial state: `"11011110011011101"`
- Disk length: 272

**Verification Method**:
```python
def test_actual_input():
    result = solve('input.md', disk_length=272)
    # Verify properties of result
    assert len(result) % 2 == 1  # Must be odd length
    assert all(c in '01' for c in result)  # Only binary digits
    assert len(result) > 0  # Non-empty
    print(f"Actual result: {result}")
```

**What we're testing**:
- Solution runs without errors
- Result has correct properties (odd length, binary)
- Can print result for verification

## Edge Cases and Special Scenarios

### Test 7: Checksum Length Progression

**Purpose**: Verify checksum reduces correctly for disk length 272

**Test Case**:
- Generate data of length 272
- Track checksum length at each iteration

**Verification Method**:
```python
def test_checksum_progression():
    # Generate data of length 272
    data = generate_data("11011110011011101", 272)
    assert len(data) == 272

    # Manually track iterations
    checksum = data
    lengths = [len(checksum)]

    while len(checksum) % 2 == 0:
        checksum = calculate_checksum_step(checksum)
        lengths.append(len(checksum))

    # Verify progression
    # 272 = 16 × 17, so 272 → 136 → 68 → 34 → 17
    assert lengths == [272, 136, 68, 34, 17]
    assert len(checksum) == 17
    assert len(checksum) % 2 == 1
```

**What we're testing**:
- Correct halving at each step
- Expected number of iterations
- Terminates at correct odd length (17)

### Test 8: Data Generation Iterations with Content Verification

**Purpose**: Verify number of dragon curve iterations for actual input and validate content

**Test Case**:
- Initial state length: 17
- Disk length: 272

**Verification Method**:
```python
def test_generation_iterations():
    data = "11011110011011101"
    lengths = [len(data)]

    # Manually verify first iteration for content correctness
    first_iteration = dragon_curve_step(data)
    # data reversed: "10110110011111011"
    # data flipped:  "01001001100000100"
    expected_first = "11011110011011101" + "0" + "01001001100000100"
    assert first_iteration == expected_first, "First iteration content mismatch"

    # Continue tracking lengths
    data = first_iteration
    lengths.append(len(data))

    while len(data) < 272:
        data = dragon_curve_step(data)
        lengths.append(len(data))

    # Verify iteration count and final length
    # Expected: 17 → 35 → 71 → 143 → 287
    assert lengths == [17, 35, 71, 143, 287]
    assert len(data) >= 272
```

**What we're testing**:
- Correct growth pattern (approximately doubles each time)
- Expected number of iterations (4)
- Exceeds disk length after expected iterations
- **Content correctness** for first iteration (catches bit-flipping errors early)

### Test 9: Bit Flipping Correctness

**Purpose**: Ensure bit flipping is correct (not just reversal)

**Test Case**:
- Input with mixed 0s and 1s

**Verification Method**:
```python
def test_bit_flipping():
    # For input "10", reversed is "01", flipped is "10"
    # Result should be "10" + "0" + "10" = "10010"
    result = dragon_curve_step("10")
    assert result == "10010"

    # For input "01", reversed is "10", flipped is "01"
    # Result should be "01" + "0" + "01" = "01001"
    result = dragon_curve_step("01")
    assert result == "01001"
```

**What we're testing**:
- Bit flipping is applied (not just reversal)
- Distinguish between reverse and flip operations

### Test 10: Minimal and Performance Cases

**Purpose**: Test boundary conditions and verify performance

**Test Cases**:

| Input | Disk Length | Expected Behavior |
|-------|-------------|-------------------|
| `"1"` | 1           | Returns `"1"` (already correct length) |
| `"0"` | 1           | Returns `"0"` (already correct length) |
| `"1"` | 3           | Returns `"100"` (one iteration) |

**Verification Method**:
```python
def test_minimal_cases():
    # Already at disk length
    result = generate_data("1", 1)
    assert result == "1"

    result = generate_data("0", 1)
    assert result == "0"

    # One iteration needed
    result = generate_data("1", 3)
    assert result == "100"

def test_performance():
    """Optional: Verify solution completes in reasonable time"""
    import time
    start = time.time()
    result = solve('input.md', disk_length=272)
    duration = time.time() - start
    assert duration < 1.0, f"Took {duration:.2f}s, expected < 1s"
    print(f"Performance: {duration:.3f}s")
```

**What we're testing**:
- Handles case where initial state already meets disk length
- Works with minimal inputs
- Solution completes in reasonable time (< 1 second)

## Manual Verification Steps

### Step 1: Run with Example Input
Execute solution with example from problem statement:
- Input: `10000`, Disk length: 20
- Verify output: `01100`
- **Also verify intermediate steps**:
  - After generation and truncation: `10000011110010000111` (20 chars)
  - After first checksum: `0111110101` (10 chars)
  - After second checksum: `01100` (5 chars, odd - stop)

### Step 2: Verify First Dragon Curve Iteration for Actual Input
Manually trace the first iteration:
- Input: `11011110011011101`
- Reversed: `10110110011111011`
- Flipped: `01001001100000100`
- Result: `11011110011011101` + `0` + `01001001100000100` = (35 chars)
- This catches bit-flipping errors early

### Step 3: Run with Actual Input
Execute solution with actual puzzle input:
- Input: `11011110011011101`, Disk length: 272
- Record the output
- Verify output has odd length (should be 17)
- Verify only contains '0' and '1'

### Step 4: Verify Final Answer (if possible)
For Advent of Code problems:
- If this is an AoC problem, submit the answer to verify correctness
- Alternatively, compare with known solutions online (if available after solving)
- Document the final answer for future reference

## Test Execution Order

1. Run unit tests for individual functions (Tests 1-4)
2. Verify first dragon curve iteration with actual input content (Test 8 - first part)
3. Run integration test with example (Test 5)
4. Run edge case tests (Tests 7-10)
5. Run with actual input (Test 6)
6. Perform manual verification steps
7. Optional: Run performance test

## Success Criteria

- All unit tests pass
- Example from problem produces correct output (`01100`)
- Actual input produces odd-length binary string
- No runtime errors or infinite loops
- Solution completes in reasonable time (< 1 second for disk length 272)

## Debugging Approach (if tests fail)

1. **Dragon curve fails**: Check reversal and bit flipping separately
   - Print reversed string before flipping
   - Print flipped string before concatenation
   - Verify separator "0" is present
2. **Data generation fails**: Print intermediate lengths to verify growth
   - Check if loop terminates correctly
   - Verify truncation uses correct slice `[:disk_length]`
3. **Checksum fails**: Print checksum at each iteration to trace issue
   - Verify pairs are non-overlapping (step by 2)
   - Check comparison logic (same → 1, different → 0)
   - Confirm loop continues while length is even
4. **Wrong final answer**:
   - Compare with manual calculation for small example
   - Trust the algorithm over problem examples' intermediate steps
   - Verify only the final checksum against expected answer
   - If this is AoC, the submission system is the ultimate arbiter of correctness

## Important Notes

1. **Trust the algorithm**: If intermediate steps don't match problem examples exactly, trust the algorithm implementation. The problem description is authoritative, not the worked examples.
2. **Focus on final answer**: The checksum result is what matters, not intermediate data generation steps.
3. **Use tempfile**: Always use the tempfile module for test files to ensure proper cleanup.
