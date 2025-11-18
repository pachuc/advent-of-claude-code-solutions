# Test Plan: Fractal Art Pattern Enhancement (Part 2)

## Testing Objectives
1. Verify the algorithm correctly performs 18 iterations
2. Ensure pattern matching works correctly across all iterations
3. Validate grid division and reassembly logic at various grid sizes
4. Confirm the final pixel count is accurate
5. Check performance is acceptable for the large grid size

## Test Strategy Overview
Since Part 2 reuses Part 1's code with only the iteration count changed, we can leverage Part 1's correctness as a foundation. We'll verify:
- Part 1 behavior is preserved (first 5 iterations)
- Iterations 6-18 execute correctly
- Final result is accurate

## Test Cases

### Test 1: Verify Part 1 Consistency
**Purpose:** Ensure changing to 18 iterations doesn't break the first 5 iterations

**Steps:**
1. Temporarily modify the code to run only 5 iterations
2. Execute the program
3. Compare output to Part 1 answer (173)

**Expected Result:** Output should be exactly 173

**Why this matters:** If this test fails, we've introduced a bug when adapting the code

---

### Test 2: Grid Size Progression Validation
**Purpose:** Verify the grid grows according to the expected pattern

**Steps:**
1. Add debug output to print grid size after each iteration
2. Run the program and capture grid sizes
3. Verify against expected progression (note: algorithm checks `size % 2 == 0` first):
   - Start: 3
   - Iter 1: 4 (3 divisible by 3 → 3×3 blocks become 4×4)
   - Iter 2: 6 (4 divisible by 2 → 2×2 blocks become 3×3)
   - Iter 3: 9 (6 divisible by 2 → size × 3/2)
   - Iter 4: 12 (9 divisible by 3 → size × 4/3)
   - Iter 5: 18 (12 divisible by 2 → size × 3/2)
   - Iter 6: 27 (18 divisible by 2 → size × 3/2)
   - Iter 7: 36 (27 divisible by 3 → size × 4/3)
   - Iter 8: 54 (36 divisible by 2 → size × 3/2)
   - Iter 9: 81 (54 divisible by 2 → size × 3/2)
   - Iter 10: 108 (81 divisible by 3 → size × 4/3)
   - Iter 11: 162 (108 divisible by 2 → size × 3/2)
   - Iter 12: 243 (162 divisible by 2 → size × 3/2)
   - Iter 13: 324 (243 divisible by 3 → size × 4/3)
   - Iter 14: 486 (324 divisible by 2 → size × 3/2)
   - Iter 15: 729 (486 divisible by 2 → size × 3/2)
   - Iter 16: 972 (729 divisible by 3 → size × 4/3)
   - Iter 17: 1458 (972 divisible by 2 → size × 3/2)
   - Iter 18: 2187 (1458 divisible by 2 → size × 3/2)

**Implementation:**
```python
for iteration in range(num_iterations):
    grid_size = len(grid)
    print(f"Iteration {iteration}: Grid size = {grid_size}")
    # ... rest of iteration logic
```

**Expected Pattern:**
- Sizes divisible by 2 grow by factor of 3/2
- Sizes divisible by 3 (but not 2) grow by factor of 4/3

**Why this matters:** Incorrect grid division would cascade errors through all subsequent iterations

---

### Test 3: Pattern Matching Coverage
**Purpose:** Ensure all patterns encountered during 18 iterations can be matched in the rules

**Steps:**
1. Run the program normally
2. Monitor for KeyError exceptions (which would indicate an unmatched pattern)
3. The program should complete without exceptions

**Expected Result:** No KeyError exceptions should occur

**Why this matters:** Missing pattern matches would cause the program to crash

**Note:** The Part 1 solution already handles all 8 orientations (rotations + flips), so this should work automatically

---

### Test 4: Intermediate Iteration Spot Check
**Purpose:** Verify correctness at a midpoint (e.g., iteration 10)

**Steps:**
1. Manually verify a few iterations can be traced:
   - Check that the starting grid (`.#.`, `..#`, `###`) is correct
   - Verify the first transformation happens correctly
   - Spot-check a random intermediate iteration

**Implementation:**
```python
# After iteration 1, print a sample of the grid
if iteration == 0:
    print("After iteration 1:")
    for row in grid:
        print(row)
```

**Expected Result:**
- Iteration 0 (initial): Grid is 3×3 with pattern `.#.`, `..#`, `###`
- Iteration 1: Grid becomes 4×4 (since 3 is divisible by 3)
- The transformed pattern should match the rule for `.#./..#/###`

**Why this matters:** Catching errors early in the iteration sequence prevents debugging large grids

---

### Test 5: Block Division and Reassembly Integrity
**Purpose:** Ensure blocks are correctly divided and reassembled at various grid sizes

**Steps:**
1. For iterations with grid size divisible by 2 (e.g., iterations 2, 3, 5):
   - Verify `divide_grid()` creates the correct number of 2×2 blocks
   - Verify each block is enhanced to 3×3
   - Verify reassembly creates a grid of correct size

2. For iterations with grid size divisible by 3 (e.g., iterations 1, 4, 6):
   - Verify `divide_grid()` creates the correct number of 3×3 blocks
   - Verify each block is enhanced to 4×4
   - Verify reassembly creates a grid of correct size

**Implementation:**
```python
blocks = divide_grid(grid, block_size)
print(f"Number of block rows: {len(blocks)}")
print(f"Number of blocks per row: {len(blocks[0])}")
# Expected: grid_size / block_size
```

**Expected Results:**
- For a 6×6 grid with block_size=2: 3 block rows, 3 blocks per row
- For a 9×9 grid with block_size=3: 3 block rows, 3 blocks per row
- Reassembled grid size = (number of blocks per row) × (enhanced block size)

**Why this matters:** Division/reassembly bugs would corrupt the grid structure

---

### Test 6: Pixel Count Sanity Check
**Purpose:** Verify the final pixel count is reasonable

**Steps:**
1. Run the program for 18 iterations
2. Record the final grid size
3. Record the final pixel count
4. Verify: 0 < pixel_count < (grid_size × grid_size)

**Expected Result:**
- Grid size after 18 iterations: exactly 2187×2187 = 4,782,969 total pixels
- Pixel count: Based on Part 1 data (173/324 ≈ 53% density), expect roughly 1-3 million active pixels
- The exact value depends on the enhancement rules, but should be within reasonable bounds

**Why this matters:** A count of 0 or greater than grid_size² indicates a critical bug

---

### Test 7: Full Execution Test
**Purpose:** Run the complete program and verify it produces an answer

**Steps:**
1. Run the program with 18 iterations
2. Capture the output
3. Verify the output is a single integer

**Expected Result:**
- Program completes without errors
- Output is a positive integer
- Runtime is under 5 minutes (acceptable for this problem)
- Based on grid growth, iterations 15-18 will take progressively longer as they handle the largest grids

**Why this matters:** This is the final acceptance test

---

### Test 8: Performance Test (Optional)
**Purpose:** Ensure the program runs in reasonable time

**Steps:**
1. Time the execution of the program
2. Note which iterations take the longest
3. Verify total runtime is acceptable

**Expected Result:**
- Later iterations (15-18) will take the most time due to large grid sizes
- Iteration 18 processes a 2187×2187 grid and should dominate runtime
- Total runtime should be under 5 minutes on modern hardware (likely 30 seconds to 2 minutes)
- Most time should be spent in iteration 18 (largest grid)

**Why this matters:** If performance is unacceptable, we may need optimization (though it should be fine)

---

## Validation Strategy

### Manual Verification Steps
1. **Start state verification:**
   - Print the initial grid and verify it matches `.#./..#/###`

2. **First transformation verification:**
   - Look up the rule for `.#./..#/###` in the input
   - Verify the grid after iteration 1 matches that rule's output

3. **Final count verification:**
   - Count '#' characters in the final grid manually (via code)
   - Verify it matches the program output

### Debugging Approach
If any test fails:
1. Add debug prints to show grid state after each iteration
2. Check the grid size progression matches the expected pattern
3. Verify pattern matching is working (print patterns that are being looked up)
4. Inspect a small sample of blocks to ensure correct transformation

## Edge Cases to Test

### Edge Case 1: Pattern Orientation Matching
**Scenario:** A pattern that requires rotation or flipping to match

**Test:** The Part 1 solution already handles all 8 orientations, so this should work automatically. We can verify by checking that no KeyError occurs during execution.

### Edge Case 2: Grid Divisibility
**Scenario:** Ensuring the grid size is always divisible by either 2 or 3

**Test:** At each iteration, verify `grid_size % 2 == 0` or `grid_size % 3 == 0` (at least one must be true)

**Mathematical proof:**
- Start: 3 (divisible by 3) ✓
- If divisible by 3: new_size = old_size × 4/3
  - If old_size = 3k: new_size = 4k (divisible by 2) ✓
- If divisible by 2: new_size = old_size × 3/2
  - If old_size = 2k: new_size = 3k (divisible by 3) ✓

This ensures the grid is always divisible by at least one of {2, 3}.

### Edge Case 3: All Pixels On or Off
**Scenario:** Although unlikely, verify the code handles grids that are all '#' or all '.'

**Test:** Not necessary to test explicitly (rules determine this), but the counting logic should handle both cases correctly.

## Success Criteria
The solution is correct if:
1. ✓ Test 1 passes (first 5 iterations match Part 1)
2. ✓ Test 2 passes (grid sizes follow expected progression)
3. ✓ Test 3 passes (no pattern matching errors)
4. ✓ Test 7 passes (program completes and outputs an integer)
5. ✓ The output is a reasonable positive integer

## Test Implementation Notes
- Most tests involve adding temporary debug output
- Debug output should be commented out or removed in the final solution
- The primary test is simply: "Does it run and produce an answer?"
- Since we're solving a puzzle (not production code), exhaustive testing is not required
- Focus on verifying the algorithm executes correctly for 18 iterations

## Quick Test Checklist
- [ ] Initial grid is correct (`.#./..#/###`)
- [ ] First 5 iterations produce the same result as Part 1 (173 pixels)
- [ ] Grid sizes match expected progression (see Test 2 for all 18 sizes)
- [ ] Program completes 18 iterations without errors
- [ ] Final grid size is exactly 2187×2187
- [ ] Final pixel count is a positive integer in a reasonable range (1-3 million estimated)
- [ ] Output matches the expected answer for the puzzle
