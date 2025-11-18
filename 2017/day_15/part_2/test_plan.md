# Test Plan: Dueling Generators Part 2

## Overview
This test plan ensures the Part 2 solution correctly implements filtered generator comparison with 5 million pairs.

## Test Strategy

### 1. Unit Tests
Test individual components in isolation.

### 2. Integration Tests
Test the complete workflow with known examples.

### 3. Validation Tests
Verify correctness against problem examples and edge cases.

## Detailed Test Cases

### Test 1: Input Parsing
**Objective:** Verify that starting values are correctly extracted from input.txt

**Test Steps:**
1. Read input.txt
2. Parse using `parse_input('input.txt')`
3. Verify `start_a == 277`
4. Verify `start_b == 349`

**Expected Result:** Both values correctly extracted

**Why Important:** Incorrect starting values would invalidate all results

---

### Test 2: Filtered Generator Produces Correct Sequence
**Objective:** Verify that filtering preserves the underlying sequence order

**Test Steps:**
1. Manually calculate first 20 values from generator A with start=65
2. Identify which of those 20 values are multiples of 4
3. Create filtered generator A with start=65, factor=16807, modulo=2147483647, filter=4
4. Generate first 5 filtered values
5. Verify they match the multiples of 4 from the manual calculation (in order)

**Expected Result:** Filtered values are a subset of the full sequence, in correct order

**Why Important:** Confirms filtering doesn't corrupt the underlying sequence - it just skips values

**Note:** This test validates that we filter AFTER generation, not before. The filtered sequence should match the multiples-of-4 values from the unfiltered sequence.

---

### Test 3: Generator A Filtering (Multiples of 4)
**Objective:** Verify Generator A only yields multiples of 4

**Test Steps:**
1. Create filtered generator A with start=277, factor=16807, modulo=2147483647, filter=4
2. Generate first 100 values
3. Verify every value satisfies: `value % 4 == 0`

**Expected Result:** All 100 values are multiples of 4

**Why Important:** Core filtering logic must be correct

---

### Test 4: Generator B Filtering (Multiples of 8)
**Objective:** Verify Generator B only yields multiples of 8

**Test Steps:**
1. Create filtered generator B with start=349, factor=48271, modulo=2147483647, filter=8
2. Generate first 100 values
3. Verify every value satisfies: `value % 8 == 0`

**Expected Result:** All 100 values are multiples of 8

**Why Important:** Core filtering logic must be correct for both generators

---

### Test 5: Example Verification (Start Values A=65, B=8921)
**Objective:** Verify solution produces correct results for the provided example

**Test Steps:**
1. Use example starting values: A=65, B=8921
2. Generate first 5 filtered pairs
3. Verify they match the expected sequence from problem statement:

```
Generator A     Generator B
1352636452      1233683848
1992081072      862516352
530830436       1159784568
1980017072      1616057672
740335192       412269392
```

4. Verify each Generator A value is divisible by 4
5. Verify each Generator B value is divisible by 8

**Expected Result:** All 5 pairs match exactly

**Why Important:** This is the official example; if this fails, the algorithm is wrong

---

### Test 6: Lowest 16 Bits Extraction
**Objective:** Verify bit masking correctly extracts lowest 16 bits

**Test Steps:**
1. Test with known values:
   - 1352636452 & 0xFFFF should equal 50244
   - 1233683848 & 0xFFFF should equal 27528
2. Verify these don't match (50244 ≠ 27528)

**Expected Result:** Bit extraction works correctly

**Why Important:** Comparison logic depends on this

---

### Test 7: First Few Pairs Don't Match (Example)
**Objective:** Verify that with example values, first 5 pairs don't match in lowest 16 bits

**Test Steps:**
1. Use A=65, B=8921
2. Generate first 5 filtered pairs
3. For each pair, extract lowest 16 bits
4. Verify none of them match

**Expected Result:** 0 matches in first 5 pairs

**Why Important:** Confirms comparison logic and that we're not getting false positives

---

### Test 8: Small Scale Full Count (Example - 5 Million Pairs)
**Objective:** Verify complete solution on example input

**Test Steps:**
1. Run `count_matches(65, 8921, 5_000_000)`
2. Verify result equals 309 (as stated in problem)

**Expected Result:** Exactly 309 matches

**Why Important:** This is the complete example validation - if this passes, algorithm is likely correct

**Note:** This may take a few seconds to run

---

### Test 9: Actual Input Solution
**Objective:** Generate the final answer for the actual puzzle input

**Test Steps:**
1. Run `count_matches(277, 349, 5_000_000)`
2. Verify the result is a reasonable positive integer
3. Check that 0 <= result <= 5,000,000 (can't have more matches than pairs)

**Expected Result:** A valid count in the range [0, 5,000,000]

**Why Important:** This is the actual puzzle answer

**Note:** Do not compare to Part 1's answer of 592 - the filtering and different pair count make this comparison meaningless.

---

### Test 10: Generator Independence
**Objective:** Verify generators work independently with different skip rates

**Test Steps:**
1. Create both filtered generators with actual starting values (277, 349)
2. Generate 1000 filtered pairs
3. Understand that:
   - Generator A (filter=4) yields approximately 1/4 of generated values (keeps multiples of 4)
   - Generator B (filter=8) yields approximately 1/8 of generated values (keeps multiples of 8)
   - Therefore A yields about 2x as frequently as B

**Expected Result:**
- On average, Generator A needs ~4 internal iterations per valid value
- On average, Generator B needs ~8 internal iterations per valid value
- Both successfully complete 1000 pairs
- The generators advance independently (A doesn't wait for B and vice versa)

**Why Important:** Confirms generators operate independently as specified

**Note:** The test verifies behavior, not exact internal iteration counts (which would require instrumentation).

---

### Test 11: Actual Generated Values Meet Filter Criteria
**Objective:** Verify real generated values pass their respective filters

**Test Steps:**
1. Generate first 100 values from filtered generator A (start=277, filter=4)
2. Verify all values satisfy `value % 4 == 0`
3. Verify at least some values also satisfy `value % 8 == 0` (multiples of 8 are also multiples of 4)
4. Generate first 100 values from filtered generator B (start=349, filter=8)
5. Verify all values satisfy `value % 8 == 0`
6. Verify all these values also satisfy `value % 4 == 0` (all multiples of 8 are multiples of 4)

**Expected Result:** All generated values meet their filter criteria, and mathematical relationships hold

**Why Important:** Validates filtering on actual data from the generators, not theoretical values

**Note:** We don't test with 0, 4, 8 directly because the generator never produces 0 (starting values are positive and the modulo operation preserves positivity).

---

### Test 12: Performance Test
**Objective:** Ensure solution completes in reasonable time

**Test Steps:**
1. Run full solution with actual input (5 million pairs)
2. Measure execution time
3. Verify completion within reasonable timeframe (< 15 seconds)

**Expected Result:** Completes in under 15 seconds (estimated 5-15 seconds based on implementation plan)

**Why Important:** Solution must be practical to run

**Note:** Threshold is tighter than original 30 seconds to catch potential inefficiencies while allowing reasonable headroom.

---

### Test 13: Consistency Test
**Objective:** Verify solution is deterministic

**Test Steps:**
1. Run `count_matches(277, 349, 5_000_000)` multiple times
2. Verify all runs produce identical results

**Expected Result:** Same answer every time

**Why Important:** Confirms no randomness or state corruption

---

### Test 14: Sequence Correctness After Filtering (Optional - Thorough Validation)
**Objective:** Verify internal sequence advances correctly even when filtering

**Priority:** Optional - Test 5 (example validation) provides sufficient proof if this is too complex

**Test Steps:**
1. Generate first 50 unfiltered values from A starting at 65 (would need unfiltered generator or manual calculation)
2. Identify which ones are multiples of 4
3. Create filtered generator A starting at 65 with filter=4
4. Generate values from filtered generator
5. Verify filtered values appear in same order as multiples of 4 from unfiltered sequence

**Expected Result:** Filtered sequence is a subset of unfiltered sequence in correct order

**Why Important:** Confirms filtering doesn't corrupt the underlying sequence

**Implementation Note:** This requires either keeping the Part 1 unfiltered generator or manually calculating values. Mark as lower priority; Test 5 validates correctness more practically.

---

## Test Execution Order

### Phase 1: Component Validation
1. Test 1 - Input Parsing
2. Test 2 - Basic Generator Sequence
3. Test 3 - Generator A Filtering
4. Test 4 - Generator B Filtering
5. Test 6 - Lowest 16 Bits Extraction

### Phase 2: Integration Validation
6. Test 5 - Example Verification (first 5 pairs)
7. Test 7 - First Few Pairs Don't Match
8. Test 14 - Sequence Correctness After Filtering

### Phase 3: Full Solution Validation
9. Test 8 - Small Scale Full Count (example)
10. Test 9 - Actual Input Solution
11. Test 13 - Consistency Test

### Phase 4: Additional Validation
12. Test 10 - Generator Independence
13. Test 11 - Filter Edge Cases
14. Test 12 - Performance Test

## Success Criteria

### Minimum Requirements (Must Pass)
- Test 1 must pass (correct input parsing)
- Test 5 must pass (first 5 example pairs match exactly)
- Test 8 must pass (example produces 309)
- Test 9 must produce a valid answer
- Test 13 must pass (deterministic results)

### Full Validation
- All non-optional tests pass (Tests 1-13, excluding optional Test 14)
- Performance is acceptable (< 15 seconds)
- Example answer matches exactly (309)

### Optional
- Test 14 (if time permits and complexity is manageable)

## Edge Cases Covered

1. ✓ Values that are multiples of both 4 and 8
2. ✓ Values that are multiples of 4 but not 8
3. ✓ First generated values might not pass filter
4. ✓ Generators advance at different rates
5. ✓ Large iteration counts (5 million pairs)
6. ✓ Bit extraction at boundaries
7. ✓ Different starting values
8. ✓ Deterministic behavior

## What We're NOT Testing

(As per instructions - we're solving a specific puzzle, not building production code)

1. Invalid input formats (we know the input format)
2. Negative starting values (not in problem domain)
3. Non-integer inputs (input is guaranteed valid)
4. File I/O errors (input.txt exists and is readable)
5. Memory limits (5M pairs is well within Python's capabilities)
6. Concurrent access (single-threaded solution)
7. Floating point precision (all integer arithmetic)
8. Comparison to Part 1's answer (not meaningful due to different filtering and pair counts)

## Manual Verification Steps

After running automated tests:

1. **Visual inspection of first 5 filtered pairs** - compare with problem example (must match exactly)
2. **Verify answer is reasonable** - should be a positive integer in range [0, 5,000,000]
3. **Check runtime** - should complete in 5-15 seconds
4. **Understand Part 1 vs Part 2 differences** - Part 2 uses filtering and different pair count, making direct comparison not meaningful

## Test Automation Strategy

**Recommended approach:**
- Create a separate test file `test_solution.py` with all test cases
- Use Python's `assert` statements for validation
- Run tests before submitting the final answer
- Alternatively, implement critical tests (1, 5, 8) as functions called from main during development

**Minimum viable testing:**
- At minimum, verify Test 8 passes (example produces 309)
- This validates the entire solution end-to-end

## Debugging Strategy (If Tests Fail)

### If Test 2 fails:
- Basic generator is broken, check modulo arithmetic

### If Test 3 or 4 fails:
- Filtering logic is incorrect, check `% filter_divisor == 0` condition

### If Test 5 fails:
- Either generator sequence or filtering is wrong
- Print first 20 unfiltered values and manually check which should pass filter

### If Test 8 fails (example doesn't give 309):
- Either filtering, comparison, or counting is wrong
- Add debug prints to see matches found at each step
- Verify example values manually

### If Test 9 produces unreasonable result:
- Check if starting values were parsed correctly
- Verify we're using 5 million pairs, not 40 million
- Compare with Part 1 logic

## Conclusion

This test plan provides comprehensive coverage of:
- Individual component correctness
- Integration between components
- Known example validation
- Edge case handling
- Performance characteristics

Passing all tests ensures the solution correctly implements the Part 2 requirements.
