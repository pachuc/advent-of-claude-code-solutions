# Test Plan: Recursive Decompression (Part 2)

## Testing Strategy

The testing approach will verify:
1. **Correctness**: Solution matches expected outputs for given examples
2. **Recursion**: Nested markers are properly handled
3. **Edge cases**: Boundary conditions and special inputs
4. **Regression**: Part 1 behavior still works for non-nested cases

## Test Cases

### 1. Basic Examples from Problem Statement

#### Test 1.1: No nested markers
**Input**: `(3x3)XYZ`
**Expected Output**: `9`
**Rationale**: Simple marker with no recursion
- Takes 3 characters: `XYZ`
- No markers inside, so length is 3
- Repeat 3 times: 3 * 3 = 9

#### Test 1.2: Single level nesting
**Input**: `X(8x2)(3x3)ABCY`
**Expected Output**: `20`
**Rationale**: Tests basic recursive processing
- `X` = 1
- Marker `(8x2)` takes `(3x3)ABC` (8 chars)
  - Inside this: `(3x3)ABC`
  - Marker `(3x3)` takes `ABC` → length 3
  - Repeat 3 times: 3 * 3 = 9
  - So `(3x3)ABC` has decompressed length 9
  - Repeat 2 times: 9 * 2 = 18
- `Y` = 1
- Total: 1 + 18 + 1 = 20

#### Test 1.3: Deep nesting
**Input**: `(27x12)(20x12)(13x14)(7x10)(1x12)A`
**Expected Output**: `241920`
**Rationale**: Tests multiple levels of recursive expansion
- Outer marker repeats inner content 12 times
- Each level multiplies the expansion factor
- Verifies recursive depth handling

#### Test 1.4: Multiple nested markers (CORRECTED)
**Input**: `(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX`
**Expected Output**: `76`
**Rationale**: Tests multiple markers within a single data section
- The marker `(25x3)` takes the next 25 characters: `(3x3)ABC(2x3)XY(5x2)PQRST`
- Remaining after extraction: `X`
- Recursively decompress `(3x3)ABC(2x3)XY(5x2)PQRST`:
  - `(3x3)` takes `ABC` → length 3, repeat 3 times = 9
  - `(2x3)` takes `XY` → length 2, repeat 3 times = 6
  - `(5x2)` takes `PQRST` → length 5, repeat 2 times = 10
  - Total: 9 + 6 + 10 = 25
- Multiply by 3 (outer repetition): 25 × 3 = 75
- Add trailing `X`: 75 + 1 = 76

### 2. Edge Cases

#### Test 2.1: No markers (plain text)
**Input**: `ADVENT`
**Expected Output**: `6`
**Rationale**: Base case - no recursion needed

#### Test 2.2: Empty string
**Input**: `` (empty)
**Expected Output**: `0`
**Rationale**: Boundary condition

#### Test 2.3: Only whitespace
**Input**: `   \n\t  `
**Expected Output**: `0`
**Rationale**: Whitespace should be ignored

#### Test 2.4: Marker with whitespace (CLARIFIED)
**Input**: `(3x3) XY` (note space before XY)
**Expected Output**: `6`
**Rationale**:
- **Whitespace handling**: When extracting "next A characters", whitespace counts as a position. When calculating length, whitespace is ignored.
- Takes next 3 character positions: ` XY` (space + X + Y)
- Recursively decompress ` XY`: whitespace ignored → length is 2 (X and Y)
- Repeat 3 times: 2 × 3 = 6

#### Test 2.4b: Whitespace within data (NEW)
**Input**: `(4x2)A B `
**Expected Output**: `4`
**Rationale**:
- Takes next 4 character positions: `A B ` (A, space, B, space)
- Recursively decompress `A B `: whitespace ignored → length is 2 (A and B)
- Repeat 2 times: 2 × 2 = 4

#### Test 2.5: Single character repetition
**Input**: `(1x1000)A`
**Expected Output**: `1000`
**Rationale**: Large repetition factor with simple character

#### Test 2.6: Marker at end
**Input**: `ABC(2x2)XY`
**Expected Output**: `7`
**Rationale**: `ABC` = 3, `XY` repeated 2 times = 4, total = 7

#### Test 2.7: Empty data section (NEW)
**Input**: `(0x5)ABC`
**Expected Output**: `3`
**Rationale**:
- Marker `(0x5)` takes 0 characters, repeat 5 times = 0
- Continue with `ABC` = 3
- Total: 3

### 3. Regression Tests (Part 1 Examples)

These should still work correctly with the recursive solution:

#### Test 3.1: Part 1 Example 1
**Input**: `A(1x5)BC`
**Expected Output**: `7`
**Rationale**: `A` + `B` repeated 5 times + `C` = 1 + 5 + 1 = 7

#### Test 3.2: Part 1 Example 2
**Input**: `(3x3)XYZ`
**Expected Output**: `9`

#### Test 3.3: Part 1 Example 3
**Input**: `A(2x2)BCD(2x2)EFG`
**Expected Output**: `11`
**Rationale**: `A` + `BC` repeated 2 times + `D` + `EF` repeated 2 times + `G` = 1 + 4 + 1 + 4 + 1 = 11

#### Test 3.4: Part 1 Example with nested-looking marker (CLARIFIED)
**Input**: `(6x1)(1x3)A`
**Part 1 Expected**: `6` (markers treated as literal)
**Part 2 Expected**: `3` (markers processed recursively)
**Rationale**:
- Marker `(6x1)` takes next 6 characters: `(1x3)A` (counting each character: `(`, `1`, `x`, `3`, `)`, `A`)
- For Part 1 (non-recursive): These 6 characters are treated as literal text, repeated once = 6
- For Part 2 (recursive): Recursively decompress `(1x3)A`:
  - Marker `(1x3)` takes `A` → length 1
  - Repeat 3 times: 1 × 3 = 3
  - Total: 3
- Repeat 1 time: 3 × 1 = 3
- **This demonstrates the key difference between Part 1 and Part 2**

#### Test 3.5: Part 1 Example with nested-looking markers
**Input**: `X(8x2)(3x3)ABCY`
**Part 1 Expected**: `18` (markers inside treated as literal)
**Part 2 Expected**: `20` (markers inside processed recursively)

This shows the difference between Part 1 and Part 2.

### 4. Actual Input Validation

#### Test 4.1: Run with actual input
**Input**: Content from `input.md`
**Expected Output**: Unknown (but should be much larger than Part 1's 98135)
**Validation Steps**:
1. First verify Part 1 solution on the input produces 98135 (matching `part_1_answer.txt`)
2. Run Part 2 solution on the same input
3. Verify result is > 98135 (likely in millions or billions given recursive expansion)
4. Should complete in reasonable time (< 10 seconds)
5. No errors or crashes
6. Optionally: Manually verify a small portion of input by hand to build confidence

#### Test 4.2: Comparison with Part 1
**Input**: Same input file
**Part 1 Result**: 98135
**Part 2 Result**: Should be significantly larger
**Rationale**: Recursive processing causes exponential expansion

### 5. Stress Tests

#### Test 5.1: Maximum nesting depth (CORRECTED)
**Input**: `(45x2)(35x2)(25x2)(15x2)(5x2)ABCDE`
**Expected**: Should complete without stack overflow; verify calculation
**Calculation**:
- `(5x2)` takes `ABCDE` → length 5, repeat 2 = 10
- `(15x2)` takes `(5x2)ABCDE` (15 chars) → decompressed length 10, repeat 2 = 20
- `(25x2)` takes `(15x2)(5x2)ABCDE` (25 chars) → decompressed length 20, repeat 2 = 40
- `(35x2)` takes `(25x2)(15x2)(5x2)ABCDE` (35 chars) → decompressed length 40, repeat 2 = 80
- `(45x2)` takes the rest (45 chars) → decompressed length 80, repeat 2 = 160
**Rationale**: Verify recursion depth handling with properly nested markers

#### Test 5.2: Large repetition factor
**Input**: `(100x1000000)` followed by 100 characters with markers
**Expected**: Very large number, but should calculate quickly
**Rationale**: We're not building the string, just calculating length

## Testing Procedure

### Manual Testing Steps

1. **Create test file**: `test_solution.py`
2. **Implement test cases**: Use simple assertions or print statements
3. **Run each test**: Verify outputs match expected values
4. **Document failures**: If any test fails, debug and fix

### Test Implementation Approach

```python
def test_solution():
    from solution import calculate_decompressed_length_recursive

    tests = [
        # Basic examples
        ("(3x3)XYZ", 9),
        ("X(8x2)(3x3)ABCY", 20),
        ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
        ("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX", 76),  # CORRECTED from 445

        # Edge cases
        ("ADVENT", 6),
        ("", 0),
        ("(0x5)ABC", 3),

        # Regression tests from Part 1
        ("A(1x5)BC", 7),
        ("(3x3)XYZ", 9),
        ("A(2x2)BCD(2x2)EFG", 11),
        ("(6x1)(1x3)A", 3),  # Different from Part 1's 6

        # Whitespace tests
        ("(3x3) XY", 6),
        ("(4x2)A B ", 4),
    ]

    for i, (input_str, expected) in enumerate(tests):
        result = calculate_decompressed_length_recursive(input_str)
        if result == expected:
            print(f"Test {i+1} PASSED: {input_str} → {result}")
        else:
            print(f"Test {i+1} FAILED: {input_str} → {result} (expected {expected})")
```

### Success Criteria

1. All example tests pass
2. All edge cases handled correctly
3. Actual input produces a result larger than Part 1
4. No stack overflow or memory errors
5. Execution time < 10 seconds for actual input

## Debugging Strategy

If tests fail:

1. **Add debug prints**: Show recursion depth, current substring, calculated lengths
2. **Test incrementally**: Start with simplest cases, add complexity
3. **Verify marker parsing**: Ensure `(AxB)` is extracted correctly
4. **Check substring extraction**: Verify correct A characters are taken
5. **Trace recursion**: Print each recursive call to see the flow

## Expected Behavior Differences from Part 1

| Aspect | Part 1 | Part 2 |
|--------|--------|--------|
| `(6x1)(1x3)A` | 6 | 3 |
| `X(8x2)(3x3)ABCY` | 18 | 20 |
| Actual input | 98135 | Much larger |
| Processing | Linear scan | Recursive |

## Final Validation

After all tests pass:
1. Run with actual input from `input.md`
2. Verify output is a reasonable large number (likely millions or more)
3. Compare with Part 1 to ensure it's larger
4. Document the final answer
