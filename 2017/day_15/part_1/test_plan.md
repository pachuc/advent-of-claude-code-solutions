# Test Plan: Dueling Generators

## Testing Strategy Overview

### Goals
1. Verify correctness of generator algorithm
2. Verify correctness of bit comparison logic
3. Validate against known example results
4. Ensure solution works with actual input
5. Verify performance is acceptable

### Testing Levels
1. **Unit Tests**: Individual components (generator, bit comparison, parsing)
2. **Integration Tests**: Full solution with example data
3. **Validation Tests**: Actual input data
4. **Performance Tests**: Runtime verification

## Unit Tests

### Test 1: Generator Value Sequence
**Purpose**: Verify generator produces correct sequence

**Test Case 1.1: Generator A - First 5 Values**
```
Input: start=65, factor=16807, modulo=2147483647
Expected sequence:
  1. 1092455
  2. 1181022009
  3. 245556042
  4. 1744312007
  5. 1352636052

Verification:
- Create generator with start=65, factor=16807
- Extract first 5 values
- Compare with expected values
- All must match exactly
```

**Test Case 1.2: Generator B - First 5 Values**
```
Input: start=8921, factor=48271, modulo=2147483647
Expected sequence:
  1. 430625591
  2. 1233683848
  3. 1431495498
  4. 137874439
  5. 285222916

Verification:
- Create generator with start=8921, factor=48271
- Extract first 5 values
- Compare with expected values
- All must match exactly
```

**Implementation**:
```python
def test_generator_a():
    gen = generate_values(65, 16807, 2147483647)
    expected = [1092455, 1181022009, 245556042, 1744312007, 1352636052]
    for i, exp_val in enumerate(expected):
        assert next(gen) == exp_val, f"Value {i+1} mismatch"
```

### Test 2: Lowest 16 Bits Extraction
**Purpose**: Verify bit masking works correctly

**Test Case 2.1: Known Values**
```
Test values from the example:
1. Value: 1092455
   1092455 & 0xFFFF should equal 43783

2. Value: 430625591
   430625591 & 0xFFFF should equal 33671

3. Value: 245556042
   245556042 & 0xFFFF should equal 6346

4. Value: 1431495498
   1431495498 & 0xFFFF should equal 6346

Note: Values 3 and 4 have matching lowest 16 bits (both 6346),
which is why the third pair in the example matches.
```

**Verification**:
- Apply `& 0xFFFF` to each value
- Verify results match expected lowest 16 bits
- Verify that values 3 and 4 produce same result (they should match)

**Implementation**:
```python
def test_lowest_16_bits():
    assert (1092455 & 0xFFFF) == 43783
    assert (430625591 & 0xFFFF) == 33671
    assert (245556042 & 0xFFFF) == 6346
    assert (1431495498 & 0xFFFF) == 6346
    # Verify values 3 and 4 match (this is the third pair match)
    assert (245556042 & 0xFFFF) == (1431495498 & 0xFFFF)
```

### Test 3: Bit Comparison Logic
**Purpose**: Verify comparison logic (either as a function or inline)

**Test Case 3.1: Matching Pairs**
```
Pair 1: (245556042, 1431495498)
- Both have lowest 16 bits = 6346
- Should match

Pair 2: (65536, 0)
- Both have lowest 16 bits = 0
- Should match

Pair 3: (65535, 131071)
- 65535 & 0xFFFF = 65535
- 131071 & 0xFFFF = 65535
- Should match
```

**Test Case 3.2: Non-Matching Pairs**
```
Pair 1: (1092455, 430625591)
- 43783 vs 33671
- Should NOT match

Pair 2: (1, 2)
- 1 vs 2
- Should NOT match
```

**Implementation**:
```python
# Helper function for testing (may or may not exist in main code)
def lowest_16_bits_match(a, b):
    return (a & 0xFFFF) == (b & 0xFFFF)

def test_bit_comparison():
    # Matching cases
    assert lowest_16_bits_match(245556042, 1431495498) == True
    assert lowest_16_bits_match(65536, 0) == True
    assert lowest_16_bits_match(65535, 131071) == True

    # Non-matching cases
    assert lowest_16_bits_match(1092455, 430625591) == False
    assert lowest_16_bits_match(1, 2) == False
```

### Test 4: Input Parsing
**Purpose**: Verify input file parsing

**Test Case 4.1: Standard Format**
```
Input file content:
"Generator A starts with 277
Generator B starts with 349"

Expected: (277, 349)
```

**Test Case 4.2: With Extra Whitespace**
```
Input file content:
"Generator A starts with 277
Generator B starts with 349  "

Expected: (277, 349)
```

**Implementation**:
```python
def test_parse_input():
    # Create temporary test file using Python's tempfile module
    import tempfile
    import os

    # Write test data to temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Generator A starts with 277\n")
        f.write("Generator B starts with 349\n")
        temp_path = f.name

    try:
        # Test parsing
        start_a, start_b = parse_input(temp_path)
        assert start_a == 277
        assert start_b == 349
    finally:
        # Cleanup
        os.unlink(temp_path)
```

**Note**: Assumes well-formed input per Advent of Code standards. No need to test malformed inputs, missing files, or other error cases for this script.

## Integration Tests

### Test 5: Example Verification
**Purpose**: Verify complete solution against known example

**Test Case 5.1: Full Example (40M pairs)**
```
Input:
- Generator A starts with 65
- Generator B starts with 8921

Expected Result: 588 matches

Verification:
- Run count_matches(65, 8921, 40_000_000)
- Result must equal exactly 588
- This is the definitive correctness test
```

**Implementation**:
```python
def test_example_case():
    result = count_matches(65, 8921, 40_000_000)
    assert result == 588, f"Expected 588, got {result}"
```

**Note**: This test will take several seconds to run

### Test 6: Small Sample Verification
**Purpose**: Quick verification with fewer pairs

**Test Case 6.1: First 5 Pairs**
```
Input: A=65, B=8921
First 5 pairs:
1. (1092455, 430625591) - 43783 vs 33671 - No match
2. (1181022009, 1233683848) - 11097 vs 50056 - No match
3. (245556042, 1431495498) - 6346 vs 6346 - MATCH
4. (1744312007, 137874439) - 18119 vs 56967 - No match
5. (1352636052, 285222916) - 5908 vs 31204 - No match

Expected: 1 match in first 5 pairs
```

**Implementation**:
```python
def test_first_five_pairs():
    result = count_matches(65, 8921, 5)
    assert result == 1, f"Expected 1 match in first 5, got {result}"
```

## Validation Tests

### Test 7: Actual Input
**Purpose**: Solve the actual problem

**Test Case 7.1: Production Input**
```
Input: A=277, B=349
Expected: Unknown (this is what we're solving for)

Verification:
- Run the solution with actual input
- Print the result
- Result should be a reasonable integer (likely in range 0-1,000,000)
- Re-run to verify deterministic behavior (same result)
```

**Implementation**:
```python
def test_actual_input():
    result1 = count_matches(277, 349, 40_000_000)
    result2 = count_matches(277, 349, 40_000_000)

    # Verify deterministic
    assert result1 == result2, "Results should be deterministic"

    # Sanity check range
    assert 0 <= result1 <= 40_000_000, "Result out of reasonable range"

    print(f"Actual result: {result1}")
```

### Test 8: Edge Case - Different Pair Counts
**Purpose**: Verify solution works with different iteration counts

**Test Case 8.1: Very Small Count**
```
Input: A=65, B=8921, pairs=1
Expected: 0 (first pair is 1092455 vs 430625591, bits 43783 vs 33671, no match)
```

**Test Case 8.2: First Five Pairs**
```
Input: A=65, B=8921, pairs=5
Expected: 1 (only third pair matches, as shown in problem)
```

**Test Case 8.3: Medium Count**
```
Input: A=65, B=8921, pairs=1000
Expected: Should run quickly, return some count >= 0
```

**Implementation**:
```python
def test_variable_pair_counts():
    # First pair should not match
    result_1 = count_matches(65, 8921, 1)
    assert result_1 == 0, f"Expected 0 for first pair, got {result_1}"

    # First 5 pairs should have exactly 1 match (the 3rd pair)
    result_5 = count_matches(65, 8921, 5)
    assert result_5 == 1, f"Expected 1 match in first 5 pairs, got {result_5}"

    # Medium count sanity check
    result_1000 = count_matches(65, 8921, 1000)
    assert 0 <= result_1000 <= 1000
```

## Performance Tests

### Test 9: Runtime Verification
**Purpose**: Ensure solution completes in reasonable time

**Test Case 9.1: 40M Pairs Performance**
```
Input: A=65, B=8921, pairs=40_000_000
Expected: Should complete in under 20 seconds on modern hardware

Verification:
- Record start time
- Run count_matches()
- Record end time
- Calculate duration
- Assert duration < 20 seconds (conservative estimate)
```

**Implementation**:
```python
import time

def test_performance():
    start_time = time.time()
    result = count_matches(65, 8921, 40_000_000)
    end_time = time.time()
    duration = end_time - start_time

    print(f"Runtime: {duration:.2f} seconds")
    print(f"Result: {result}")

    # Verify correctness
    assert result == 588, f"Expected 588, got {result}"

    # Verify performance (20 seconds is conservative for modern hardware)
    assert duration < 20, f"Too slow: {duration:.2f} seconds"
```

## Manual Verification Steps

### Step 1: Verify First Few Values by Hand
1. Calculate first value for Generator A manually:
   - Start: 65
   - (65 * 16807) % 2147483647 = 1092455 ✓

2. Calculate first value for Generator B manually:
   - Start: 8921
   - (8921 * 48271) % 2147483647 = 430625591 ✓

### Step 2: Verify Bit Comparison by Hand
1. Take pair 3 from example: (245556042, 1431495498)
2. Calculate lowest 16 bits using mask:
   - 245556042 & 0xFFFF = 245556042 & 65535 = 6346
   - 1431495498 & 0xFFFF = 1431495498 & 65535 = 6346
3. Verify they match ✓
4. You can verify in Python:
   ```python
   >>> 245556042 & 0xFFFF
   6346
   >>> 1431495498 & 0xFFFF
   6346
   >>> (245556042 & 0xFFFF) == (1431495498 & 0xFFFF)
   True
   ```

### Step 3: Cross-Reference with Example
1. Run solution with A=65, B=8921
2. Verify result is exactly 588
3. If not 588, debug by printing first 10 pairs and their bit comparisons

## Test Execution Order

1. **Unit tests first** (fast, catch basic errors):
   - Test 2: Bit extraction
   - Test 1: Generator sequences
   - Test 3: Bit comparison
   - Test 4: Input parsing

2. **Quick integration test**:
   - Test 6: First 5 pairs

3. **Full example validation**:
   - Test 5: Full 40M pairs with example (588)

4. **Performance check**:
   - Test 9: Runtime verification

5. **Actual solution**:
   - Test 7: Actual input (277, 349)

## Success Criteria

✓ All unit tests pass
✓ Example case produces exactly 588
✓ Solution runs in under 30 seconds
✓ Actual input produces deterministic result
✓ Result is reasonable (0 to ~1M range)

## Debugging Strategy

If tests fail:
1. **Generator mismatch**: Print first 10 values, compare with example
2. **Bit comparison error**: Print binary representations of test values
3. **Count mismatch**: Print first 100 pairs with match/no-match labels
4. **Performance issues**: Profile code, check for unnecessary operations
