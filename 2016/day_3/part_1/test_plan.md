# Test Plan: Triangle Validation

## Plan Status
**Status**: Corrected and Approved (based on critique feedback)
**Last Updated**: After fixing calculation errors identified in critique

**Key Corrections Made**:
1. Fixed manual calculations in Test 3.2 (lines 6, 8, and 9 were incorrectly marked as VALID)
2. Corrected expected count for first 10 lines from 6 to 3 valid triangles
3. Added Test 4.6 for "large side with two medium sides" pattern
4. Added Test 4.7 for negative number handling
5. Updated sanity check estimates based on corrected spot-check results

**Critical Insight from Corrections**:
The triangle inequality requires ALL three conditions to be strictly greater than (>). If any sum equals (rather than exceeds) the third side, the triangle is INVALID. This is why (5,5,10), (910,265,611), and (894,252,545) are all invalid.

## Testing Strategy

Since we're writing a script to solve a specific problem (not production code), testing will focus on:
1. Correctness of the core algorithm
2. Handling of the actual input file
3. Key edge cases that might appear in the input

We do NOT need to test:
- Extensive error handling for malformed input
- Performance benchmarks
- Cross-platform compatibility
- Production-level edge cases

## Test Categories

### 1. Algorithm Correctness Tests

#### Test 1.1: Invalid Triangle (Example from Problem)
**Input**: `5 10 25`
**Expected**: Invalid (not counted)
**Validation**:
```python
assert is_valid_triangle(5, 10, 25) == False
```
**Reason**: 5 + 10 = 15, which is NOT > 25

#### Test 1.2: Valid Equilateral Triangle
**Input**: `5 5 5`
**Expected**: Valid
**Validation**:
```python
assert is_valid_triangle(5, 5, 5) == True
```
**Checks**: All sides equal, all inequalities satisfied

#### Test 1.3: Valid Scalene Triangle
**Input**: `3 4 5`
**Expected**: Valid (right triangle)
**Validation**:
```python
assert is_valid_triangle(3, 4, 5) == True
```
**Checks**:
- 3 + 4 = 7 > 5 ✓
- 3 + 5 = 8 > 4 ✓
- 4 + 5 = 9 > 3 ✓

#### Test 1.4: Valid Isosceles Triangle
**Input**: `5 5 8`
**Expected**: Valid
**Validation**:
```python
assert is_valid_triangle(5, 5, 8) == True
```

#### Test 1.5: Invalid - Sum Equals Third Side
**Input**: `1 2 3`
**Expected**: Invalid
**Validation**:
```python
assert is_valid_triangle(1, 2, 3) == False
```
**Reason**: 1 + 2 = 3, which is NOT > 3 (must be strictly greater)

#### Test 1.6: Invalid - One Side Too Long
**Input**: `1 1 100`
**Expected**: Invalid
**Validation**:
```python
assert is_valid_triangle(1, 1, 100) == False
```

#### Test 1.7: Large Valid Triangle
**Input**: `999 999 999`
**Expected**: Valid
**Validation**:
```python
assert is_valid_triangle(999, 999, 999) == True
```
**Purpose**: Test with larger numbers from actual input

### 2. Input Parsing Tests

#### Test 2.1: Standard Format
**Input Line**: `"566  477  376\n"`
**Expected**: `(566, 477, 376)`
**Validation**:
```python
assert parse_line("566  477  376\n") == (566, 477, 376)
```

#### Test 2.2: Extra Whitespace
**Input Line**: `"  575   488   365  \n"`
**Expected**: `(575, 488, 365)`
**Purpose**: Ensure strip() and split() handle whitespace

#### Test 2.3: Mixed Spacing (from input)
**Input Line**: `" 50   18  156\n"`
**Expected**: `(50, 18, 156)`
**Purpose**: Real example with variable spacing

### 3. Integration Tests

#### Test 3.1: Small Sample Input
**Input File Content**:
```
5 10 25
3 4 5
1 2 3
5 5 8
```
**Expected Count**: 2 (lines 2 and 4 are valid)
**Validation**:
- Create temporary test file
- Run count_valid_triangles()
- Verify result is 2

#### Test 3.2: First Few Lines of Actual Input
**Input**: Lines 1-10 from input.md
**Manual Verification**:
- Line 1: `566 477 376` → 566+477=1043>376 ✓, 566+376=942>477 ✓, 477+376=853>566 ✓ → **VALID**
- Line 2: `575 488 365` → 575+488=1063>365 ✓, 575+365=940>488 ✓, 488+365=853>575 ✓ → **VALID**
- Line 3: `50 18 156` → 50+18=68 NOT > 156 ✗ → **INVALID**
- Line 4: `558 673 498` → 558+673=1231>498 ✓, 558+498=1056>673 ✓, 673+498=1171>558 ✓ → **VALID**
- Line 5: `133 112 510` → 133+112=245 NOT > 510 ✗ → **INVALID**
- Line 6: `670 613 25` → 670+613=1283>25 ✓, 670+25=695>613 ✓, 613+25=638 NOT > 670 ✗ → **INVALID**
- Line 7: `84 197 643` → 84+197=281 NOT > 643 ✗ → **INVALID**
- Line 8: `910 265 611` → 910+265=1175>611 ✓, 910+611=1521>265 ✓, 265+611=876 NOT > 910 ✗ → **INVALID**
- Line 9: `894 252 545` → 894+252=1146>545 ✓, 894+545=1439>252 ✓, 252+545=797 NOT > 894 ✗ → **INVALID**
- Line 10: `581 3 598` → 581+3=584 NOT > 598 ✗ → **INVALID**

**Expected for first 10 lines**: 3 valid triangles (lines 1, 2, and 4 only)

### 4. Edge Cases

#### Test 4.1: All Zero (Edge Case)
**Input**: `0 0 0`
**Expected**: Invalid
**Reason**: 0 + 0 is NOT > 0

#### Test 4.2: One Zero
**Input**: `0 5 5`
**Expected**: Invalid
**Reason**: 0 + 5 = 5, NOT > 5

#### Test 4.3: Order Independence
**Input Sets**:
- `3 4 5`
- `4 5 3`
- `5 3 4`

**Expected**: All should give same result (valid)
**Purpose**: Verify algorithm doesn't depend on side order

#### Test 4.4: Boundary Case - Just Valid
**Input**: `5 5 9`
**Expected**: Valid
**Validation**: 5 + 5 = 10 > 9 ✓

#### Test 4.5: Boundary Case - Just Invalid
**Input**: `5 5 10`
**Expected**: Invalid
**Validation**: 5 + 5 = 10, NOT > 10

#### Test 4.6: Large Side with Two Medium Sides (Pattern that Caused Errors)
**Input**: `100 40 50`
**Expected**: Invalid
**Validation**: 40 + 50 = 90, NOT > 100
**Purpose**: Test the specific pattern where two smaller sides nearly (but don't quite) sum to exceed the largest side

#### Test 4.7: Negative Numbers
**Input**: `-5 10 10`
**Expected**: Invalid
**Validation**: -5 + 10 = 5, NOT > 10
**Purpose**: Verify negative side lengths are properly handled (even though they shouldn't appear in input)

### 5. Full Input Test

#### Test 5.1: Complete Input File
**Method**:
1. Run solution on complete input.md
2. Verify output is a positive integer
3. Check range is reasonable (0 to 1993)

**Verification Strategy**:
- Cannot manually verify all 1993 lines
- Spot-check random samples
- Ensure no crashes or errors
- Verify output is plausible

**Sanity Checks**:
- Result should be > 0 (at least some valid triangles exist)
- Result should be < 1993 (not all triangles are valid)
- Based on spot checks of first 10 lines (3 out of 10 valid = 30%), the actual percentage may be lower than initially estimated
- The exact count will be verified through running the complete solution

## Test Execution Plan

### Phase 1: Unit Tests
1. Test `is_valid_triangle()` with all algorithm correctness tests (1.1-1.7)
2. Test `parse_line()` with parsing tests (2.1-2.3)
3. Verify edge cases (4.1-4.7)

### Phase 2: Integration Tests
1. Test with small sample file (3.1)
2. Test with first 10 lines of actual input (3.2)
3. Verify manual calculations match code output

### Phase 3: Full Solution Test
1. Run on complete input.md (5.1)
2. Verify output format (single integer)
3. Sanity check the result

## Success Criteria

The solution is correct if:
1. ✓ All unit tests pass
2. ✓ Integration tests produce expected counts
3. ✓ Full input produces a single integer output
4. ✓ Spot-checked triangles are correctly classified
5. ✓ No runtime errors or crashes

## Manual Verification Examples

For manual spot-checking, use these calculations:

**Triangle**: `566 477 376`
- 566 + 477 = 1043 > 376? YES ✓
- 566 + 376 = 942 > 477? YES ✓
- 477 + 376 = 853 > 566? YES ✓
- **Result: VALID**

**Triangle**: `50 18 156`
- 50 + 18 = 68 > 156? NO ✗
- **Result: INVALID** (can stop after first failure)

## Test Implementation Method

Create a simple test file `test_solution.py`:
```python
from solution import is_valid_triangle, parse_line, count_valid_triangles

# Run unit tests
def run_tests():
    # Test 1.1
    assert is_valid_triangle(5, 10, 25) == False, "Test 1.1 failed"

    # Test 1.2
    assert is_valid_triangle(5, 5, 5) == True, "Test 1.2 failed"

    # Test 1.3
    assert is_valid_triangle(3, 4, 5) == True, "Test 1.3 failed"

    # ... (continue for all tests)

    print("All tests passed!")

if __name__ == '__main__':
    run_tests()
```

## Expected Final Answer

The final answer will be a specific integer representing the count of valid triangles in the input. This will be verified by:
1. Ensuring it's reasonable (between 1 and 1993)
2. Spot-checking a sample of triangles manually
3. Confirming the algorithm logic is sound
