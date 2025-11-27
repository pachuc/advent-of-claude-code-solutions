# Testing Plan - Part 2: Finding Non-Overlapping Claim

## Testing Objectives
1. Verify the solution correctly identifies the single non-overlapping claim
2. Ensure grid-based overlap detection works correctly
3. Validate parsing and claim processing logic (inherited from Part 1)
4. Confirm edge cases are handled properly

## Test Strategy
Since this is a script to solve a specific puzzle, we focus on:
- Verifying correct output for the provided input
- Testing with the given example
- Validating key edge cases that could affect correctness
- NO need for extensive error handling or production-level testing

---

## Test Case 1: Example from Problem Statement

### Input
```
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
```

### Expected Behavior
- Claim #1: overlaps with claim #2 (4 cells at positions (3,3), (3,4), (4,3), (4,4))
- Claim #2: overlaps with claim #1 (same 4 cells)
- Claim #3: does NOT overlap with any claim (all cells unique)

### Expected Output
```
3
```

### How to Test
Option A: Temporarily replace input.md with example content, run script, then restore
Option B: Create small manual test by verifying logic with debugger on example
Option C: Add a command-line argument to specify input file (optional enhancement)

**Recommended approach for quick testing**: Manually trace through the logic with the
example to verify correctness before running on full input, since it's only 3 claims.

### What This Tests
- Grid building logic
- Overlap detection logic
- Non-overlapping claim identification
- Basic correctness of the algorithm

---

## Test Case 2: Actual Puzzle Input

### Input
- File: `input.md`
- Contains: 1,286 fabric claims
- From Part 1, we know: 107,820 square inches have overlaps

### Expected Behavior
- Grid should be built correctly with all 1,286 claims
- Exactly ONE claim should have all its cells with count == 1
- That claim's ID should be returned

### Expected Output
- A single integer (the claim ID)
- Cannot predict exact value without running, but should be in range [1, 1286]

### How to Test
1. Run: `python part_2_solution.py`
2. Verify output is a single integer
3. Verify it's within valid claim ID range
4. Cross-check: Re-run to ensure deterministic output

### What This Tests
- Handles real input size (1,286 claims)
- Grid dimensions calculated correctly
- Performance is acceptable (should complete in < 1 second)
- Finds the unique non-overlapping claim

---

## Test Case 3: Verify Grid Construction Correctness

### Test Method: Visual Inspection with Small Example
Using the example from Test Case 1, manually verify the grid state:

Expected grid (showing claim counts):
```
........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
```
Where numbers show claim count per cell:
- "." = 0 (no claims)
- "1" = 1 (single claim)
- "2" = 2 (two claims overlap)
- "X" = 2 (overlap between claims #1 and #2, shown for emphasis)

### Manual Verification Steps
1. Add debug print to show grid after all claims marked
2. For claim #3 at (5,5) with 2x2:
   - Cells: (5,5), (5,6), (6,5), (6,6)
   - All should have count == 1
3. For claim #1 and #2:
   - Overlap cells at (3,3), (3,4), (4,3), (4,4)
   - Should have count == 2

### What This Tests
- Grid cell values are correct
- Claim marking logic is accurate
- No off-by-one errors in indexing

---

## Test Case 4: Edge Case - Claim at Grid Boundaries

### Scenario
Verify claims at edges of the fabric are handled correctly.

### Test Method
- Examine input.md for claims with:
  - left = 0 (leftmost edge)
  - top = 0 (topmost edge)
  - left + width = max (rightmost edge)
  - top + height = max (bottommost edge)

### Expected Behavior
- No index out of bounds errors
- Grid dimensions accommodate all claims
- Edge claims processed correctly

### How to Test
1. Run solution on full input
2. No crashes = edge claims handled correctly
3. Optional: Add assertion in code to verify no claim exceeds grid bounds

### What This Tests
- Grid dimension calculation is correct
- No array index errors
- Boundary handling

---

## Test Case 5: Verify Claim Parsing

### Test Method
Reuse parsing logic from Part 1 (already proven to work).

### Spot Check
- Claim #1 in input: `#1 @ 82,901: 26x12`
- Should parse as: Claim(id=1, left=82, top=901, width=26, height=12)

### How to Test
- Add debug print statement showing first parsed claim
- Verify values match expected

### What This Tests
- Parsing regex works correctly
- All fields extracted properly
- Integer conversion successful

---

## Test Case 6: Verify Only One Non-Overlapping Claim

### Assumption to Verify
Problem states exactly one claim doesn't overlap.

### Test Method
Add an assertion in the main solution to validate this assumption.

### How to Test
Add optional validation to main() function:
```python
# Optional assertion to verify exactly one non-overlapping claim exists
non_overlapping_count = 0
result_id = None
for claim in claims:
    if is_claim_non_overlapping(grid, claim):
        non_overlapping_count += 1
        result_id = claim.id

assert non_overlapping_count == 1, f"Expected 1 non-overlapping claim, found {non_overlapping_count}"
print(result_id)
```
This can be part of the solution code, not just a test.

### What This Tests
- Problem assumption holds
- Algorithm doesn't find multiple or zero claims
- Validates correctness of solution

---

## Test Case 7: Performance Validation

### Requirements
- Should complete in reasonable time (< 2 seconds for this input size)

### Test Method
1. Add timing instrumentation:
```python
import time
start = time.time()
# ... main logic ...
end = time.time()
print(f"Execution time: {end - start:.3f} seconds")
```

2. Run on full input
3. Verify runtime is acceptable

### Expected Performance
- Grid creation: O(W × H) ≈ 1,000,000 operations → instant
- Marking claims: O(N × A) where A is average claim area
  - With ~1,286 claims and typical areas of a few hundred square inches
  - Approximate: 1,286 claims × ~300 avg area ≈ 385,800 operations → < 0.1s
- Checking claims: O(N × A) ≈ same → < 0.1s
- **Total expected**: < 0.5 seconds

Note: Average area estimate based on typical claim dimensions (15-25 inches per side)

### What This Tests
- Algorithm efficiency is acceptable
- No performance bottlenecks
- Scales appropriately with input size

---

## Test Case 8: Compare Grid State with Part 1

### Cross-Validation Strategy
Both Part 1 and Part 2 build the same grid. The Part 1 answer (107,820 square inches
with overlaps) is used here ONLY for validation, NOT as input to Part 2.

### Test Method
1. In Part 1 solution, count cells with value >= 2 → 107,820 (verified answer)
2. In Part 2 solution, same grid should exist
3. Optional: Add assertion to verify overlap count matches

### How to Test
```python
# After building grid in part_2_solution.py
# This is for validation only - Part 2 doesn't need Part 1's answer as input
overlap_count = sum(1 for row in grid for cell in row if cell >= 2)
assert overlap_count == 107820, f"Grid mismatch: expected 107820, got {overlap_count}"
```

### What This Tests
- Grid construction is consistent between parts
- Part 1 logic was correctly reused
- No regression in grid building
- Confirms Part 1 answer is used correctly (for validation, not as input)

---

## Regression Testing

### Approach
- After implementing Part 2, verify Part 1 still works
- Run Part 1 solution: should still output 107820

### Why Important
- Ensures we didn't break shared logic
- Validates both solutions work with same input

---

## Final Validation Checklist

Before considering the solution complete, verify:

- [ ] Example test case outputs `3`
- [ ] Actual input produces a single integer
- [ ] No runtime errors or crashes
- [ ] Execution completes in < 2 seconds
- [ ] Output is deterministic (same answer on multiple runs)
- [ ] Claim parsing works correctly (spot check)
- [ ] Grid dimensions accommodate all claims
- [ ] Only one non-overlapping claim found
- [ ] Grid overlap count matches Part 1 answer (107,820)

---

## Debugging Strategy (If Tests Fail)

### If wrong answer for example:
1. Print the grid visually
2. Print each claim's overlap status
3. Verify cell counting logic

### If wrong answer for actual input:
1. Verify grid dimensions are correct
2. Check if multiple claims are non-overlapping (should be exactly 1)
3. Add logging to show which claim is found

### If performance issues:
1. Profile code to find bottleneck
2. Verify grid size is reasonable (not exceeding ~1000x1000)
3. Check for inefficient nested loops

### If crashes:
1. Check for index out of bounds
2. Verify grid dimensions calculation
3. Ensure all claims are within grid bounds
