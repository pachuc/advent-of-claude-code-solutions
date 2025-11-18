# Test Plan: Circular Digit Sum (Inverse Captcha)

## Testing Strategy

We'll use a combination of:
1. **Example-based testing**: Verify against provided examples
2. **Edge case testing**: Test boundary conditions
3. **Manual verification**: Spot-check sections of the actual input
4. **Property-based reasoning**: Verify algorithm logic

**Implementation**: Tests will use simple assertions with descriptive error messages (no external testing framework needed for this scripting solution).

**Expected Output Format**: Single integer printed to stdout (e.g., `1234`), no additional formatting.

**Cross-reference**: See `implementation_plan.md` for algorithm details.

## Test Cases

### 1. Provided Examples (from problem.md)

These are our ground truth tests:

| Input | Expected Output | Reason |
|-------|----------------|---------|
| `1122` | `3` | First `1` matches second `1` (1), third `2` matches fourth `2` (2). Sum: 1+2=3 |
| `1111` | `4` | All four `1`s match their next neighbor: 1+1+1+1=4 |
| `1234` | `0` | No consecutive matches |
| `91212129` | `9` | Only last `9` matches first `9` (circular): 9 |

**Verification Method**: Run each example and assert output matches expected value.

### 2. Edge Cases

#### Test 2.1: Single Digit Matching Itself
- **Input**: `5`
- **Expected**: `5`
- **Rationale**: With length 1, the digit compares with itself via circular wrap
- **Tests**: Boundary case of minimum meaningful input

#### Test 2.2: Single Digit (variant)
- **Input**: `7`
- **Expected**: `7`
- **Rationale**: Confirms consistent behavior with different digits

#### Test 2.3: Two Matching Digits
- **Input**: `88`
- **Expected**: `16`
- **Rationale**: First `8` matches second (8), second `8` matches first via wrap (8). Sum: 8+8=16

#### Test 2.4: Two Non-Matching Digits
- **Input**: `12`
- **Expected**: `0`
- **Rationale**: `1` != `2` and `2` != `1` (circular)

#### Test 2.5: All Same Digit
- **Input**: `9999999999` (10 nines)
- **Expected**: `90`
- **Rationale**: Every digit matches its neighbor, sum = 9*10 = 90
- **Tests**: Uniform sequences

#### Test 2.6: No Matches at All
- **Input**: `123456789`
- **Expected**: `0`
- **Rationale**: No consecutive digits match

#### Test 2.7: Only Circular Match
- **Input**: `5123125`
- **Expected**: `10`
- **Rationale**: First `5` matches last `5` (circular), both contribute: wait, only the LAST `5` when comparing with next (first). Let me recalculate:
  - Position 0: `5` vs `1` - no match
  - Position 1: `1` vs `2` - no match
  - Position 2: `2` vs `3` - no match
  - Position 3: `3` vs `1` - no match
  - Position 4: `1` vs `2` - no match
  - Position 5: `2` vs `5` - no match
  - Position 6: `5` vs `5` (wraps to position 0) - MATCH, add 5
- **Expected**: `5`

#### Test 2.8: Alternating Pattern
- **Input**: `121212`
- **Expected**: `0`
- **Rationale**: No consecutive matches in alternating pattern

#### Test 2.9: Zero Digits
- **Input**: `001100`
- **Expected**: `2`
- **Breakdown**:
  - Position 0: `0==0`, add 0
  - Position 1: `0==1`, no match
  - Position 2: `1==1`, add 1
  - Position 3: `1==0`, no match
  - Position 4: `0==0`, add 0
  - Position 5: `0!=0` (wraps to position 0, which is '0'), actually `0==0`, add 0
- **Wait, let me recalculate**: `001100`
  - Position 0: '0' vs '0' (pos 1) -> match, add 0
  - Position 1: '0' vs '1' (pos 2) -> no match
  - Position 2: '1' vs '1' (pos 3) -> match, add 1
  - Position 3: '1' vs '0' (pos 4) -> no match
  - Position 4: '0' vs '0' (pos 5) -> match, add 0
  - Position 5: '0' vs '0' (pos 0, wrap) -> match, add 0
- **Sum**: 0+1+0+0 = 1
- **Expected**: `1`
- **Rationale**: Tests that zero digits are handled correctly (they contribute 0 to sum when matched)

#### Test 2.10: Multiple Consecutive Matches
- **Input**: `1112223333`
- **Expected**: `15`
- **Breakdown**:
  - Positions 0-1: `1==1`, add 1
  - Positions 1-2: `1==1`, add 1
  - Positions 2-3: `1!=2`, skip
  - Positions 3-4: `2==2`, add 2
  - Positions 4-5: `2==2`, add 2
  - Positions 5-6: `2!=3`, skip
  - Positions 6-7: `3==3`, add 3
  - Positions 7-8: `3==3`, add 3
  - Positions 8-9: `3==3`, add 3
  - Position 9 wraps: `3!=1`, skip
- **Sum**: 1+1+2+2+3+3+3 = 15

### 3. Actual Input Verification

For the 2000-digit input, we'll perform manual spot checks:

#### Test 3.1: First Few Digits Check
- Extract first 20 characters: `95148459654114155731`
- Manually trace through first 5-10 comparisons
- Verify our algorithm produces same partial result

#### Test 3.2: Circular Wrap Verification
- Check last digit of input: `1`
- Check first digit of input: `9`
- Verify: `1 != 9`, so no contribution from circular wrap

#### Test 3.3: Pattern Analysis
- Scan input for obvious patterns (consecutive same digits)
- Manually identify a few matching pairs
- Verify they're included in sum

#### Test 3.4: Statistical Sanity Check
- With 2000 digits, random would give ~200 matches (10% probability)
- Each digit averages 4.5, so expected sum ~900 for random data
- Verify output is in a reasonable range (not 0, not 18000)

### 4. Algorithm Logic Verification

#### Test 4.1: Circular Index Calculation
- **Verify**: For sequence of length `n`, position `n-1` wraps to position `0`
- **Method**: Print or assert `(n-1 + 1) % n == 0` for various n values

#### Test 4.2: No Double Counting
- **Concern**: Each digit should only contribute once (not when it's matched FROM the previous)
- **Test Input**: `11`
  - Position 0: `1==1`, add 1
  - Position 1: `1==1`, add 1
  - Total: 2 (not 1, not 4)
- **Expected**: `2`

#### Test 4.3: Character Comparison
- Verify we're comparing characters correctly before converting to int
- String comparison should work: `'5' == '5'` is True

### 5. Test Execution Plan

#### Phase 1: Unit Tests (All Example Cases)
```python
def test_examples():
    assert solve_captcha("1122") == 3
    assert solve_captcha("1111") == 4
    assert solve_captcha("1234") == 0
    assert solve_captcha("91212129") == 9
```

#### Phase 2: Edge Case Tests
Run all edge cases (2.1 through 2.10) and verify outputs

#### Phase 3: Real Input Test
1. Run solution on actual input from `input.md`
2. Print the result
3. Perform manual verification on subsections
4. Check circular wrap behavior with first/last digits

#### Phase 4: Manual Verification Samples
For concrete verification, check these specific segments of the actual input:
1. **First 10 digits** (`9514845965`): Manually trace comparisons
2. **Positions 995-1005** (middle section): Verify algorithm handles mid-sequence correctly
3. **Last 10 digits** (ending with `...21`): Verify circular wrap from last to first digit
4. **Any sequence of repeated digits** found in input: Verify matching logic

## Success Criteria

✅ All provided examples pass
✅ All edge cases produce expected results
✅ Real input produces a reasonable integer result
✅ Manual spot-checks confirm algorithm correctness
✅ Circular wrap is demonstrably working (verified on last->first digit)

## Testing Implementation

**Approach**: Add test functions directly in `solution.py` or create a separate `test_solution.py`

**Method**: Use simple assertions with descriptive messages:
```python
def run_tests():
    # Example tests
    assert solve_captcha("1122") == 3, "Example 1 failed"
    assert solve_captcha("1111") == 4, "Example 2 failed"
    # ... more tests
    print("All tests passed!")
```

**Execution**:
1. Run all test functions
2. If all pass, run on actual input
3. Print result for actual input
4. Perform manual spot-checks as described in Phase 4

## Known Limitations

Since this is a scripting solution (not production code):
- **No error handling**: Problem guarantees valid digit input, so no need to test malformed input
- **No performance testing**: 2000 characters is trivial for O(n) algorithm
- **No stress testing**: Not testing with massive inputs beyond problem scope
- **No invalid input testing**: Not testing non-digit characters or edge cases outside problem specification
- **Output format**: Simple print statement, no logging or formatted output required

## Manual Verification Example

For input `1122`:
```
Position 0: '1' vs '1' (position 1) -> MATCH, sum += 1, total = 1
Position 1: '1' vs '2' (position 2) -> no match, total = 1
Position 2: '2' vs '2' (position 3) -> MATCH, sum += 2, total = 3
Position 3: '2' vs '1' (position 0, wrap) -> no match, total = 3
Final: 3 ✓
```

This manual process should be repeated for at least 2-3 examples and one subsection of the real input.
