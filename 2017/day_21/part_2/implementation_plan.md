# Implementation Plan: Fractal Art Pattern Enhancement (Part 2)

## Overview
Part 2 requires running the exact same algorithm as Part 1 but for **18 iterations** instead of 5. The Part 1 solution can be reused with minimal modifications.

## Key Insight
The Part 1 solution (`part_1_solution.py`) is already well-structured and efficient. The only required change is updating the number of iterations from 5 to 18.

## Implementation Steps

### Step 1: Copy and Adapt Part 1 Solution
**What to do:**
- Copy the entire `part_1_solution.py` code as the foundation
- The algorithm, data structures, and helper functions are all reusable

**Why this works:**
- Part 1 and Part 2 use identical enhancement rules and logic
- The only difference is the iteration count parameter

### Step 2: Update the Iteration Count
**What to do:**
- In the `main()` function, change line 165 from:
  ```python
  final_grid = perform_iterations(initial_grid, rules, 5)
  ```
  to:
  ```python
  final_grid = perform_iterations(initial_grid, rules, 18)
  ```

**Why:**
- This is the only algorithmic difference between Part 1 and Part 2
- All other logic remains unchanged

### Step 3: Verify File I/O
**What to do:**
- Ensure the input file path is correct (`input.md`)
- The input rules are the same for both parts

**Why:**
- The same enhancement rules apply to both Part 1 and Part 2
- No changes needed to the rule parsing logic

### Step 4: Test Memory and Performance (Optional Monitoring)
**What to do:**
- Optionally add progress indicators to monitor iteration progress
- This is helpful for debugging but not required for correctness

**Implementation example:**
```python
for iteration in range(num_iterations):
    # Optional: print(f"Iteration {iteration + 1}/{num_iterations}, Grid size: {len(grid)}")
    grid_size = len(grid)
    # ... rest of the logic
```

**Why:**
- 18 iterations will take longer than 5
- Progress indicators help verify the program is running correctly
- Not required for the solution, just helpful for monitoring

## Algorithm Analysis

### Grid Size Progression
The grid grows according to this pattern:
- Start: 3×3
- After iteration 1: 4×4 (3 divisible by 3 → 3×3 blocks become 4×4)
- After iteration 2: 6×6 (4 divisible by 2 → 2×2 blocks become 3×3)
- After iteration 3: 9×9 (6 divisible by 2 → size × 3/2)
- After iteration 4: 12×12 (9 divisible by 3 → size × 4/3)
- After iteration 5: 18×18 (12 divisible by 2 → size × 3/2)
- After iteration 6: 27×27 (18 divisible by 2 → size × 3/2)
- After iteration 7: 36×36 (27 divisible by 3 → size × 4/3)
- After iteration 8: 54×54 (36 divisible by 2 → size × 3/2)
- After iteration 9: 81×81 (54 divisible by 2 → size × 3/2)
- After iteration 10: 108×108 (81 divisible by 3 → size × 4/3)
- After iteration 11: 162×162 (108 divisible by 2 → size × 3/2)
- After iteration 12: 243×243 (162 divisible by 2 → size × 3/2)
- After iteration 13: 324×324 (243 divisible by 3 → size × 4/3)
- After iteration 14: 486×486 (324 divisible by 2 → size × 3/2)
- After iteration 15: 729×729 (486 divisible by 2 → size × 3/2)
- After iteration 16: 972×972 (729 divisible by 3 → size × 4/3)
- After iteration 17: 1458×1458 (972 divisible by 2 → size × 3/2)
- After iteration 18: 2187×2187 (1458 divisible by 2 → size × 3/2)

### Growth Pattern Formula
- When size is divisible by 2: new_size = size × 3/2
- When size is divisible by 3: new_size = size × 4/3

### Time Complexity
- **Per iteration:** O(grid_size²) for dividing, enhancing, and reassembling
- **Total:** O(iterations × average_grid_size²)
- With 18 iterations and exponential growth, the final iteration dominates
- Expected runtime: seconds to low minutes (acceptable for this problem)

### Space Complexity
- **Grid storage:** O(final_grid_size²) = O(2187²) = 4,782,969 characters
- **Rules dictionary:** O(number_of_rules × pattern_length) ≈ constant (108 rules)
- **Temporary blocks:** O(grid_size²) during reassembly
- Total memory usage: ~10-20 MB (very manageable)

## Code Reuse from Part 1

### Functions to Reuse (No Changes Needed)
1. `pattern_to_grid()` - Converts pattern strings to grid format
2. `grid_to_pattern()` - Converts grid to pattern strings
3. `rotate_grid()` - Rotates grid 90 degrees clockwise
4. `flip_grid()` - Flips grid horizontally
5. `generate_all_orientations()` - Generates all 8 orientations for pattern matching
6. `parse_rules()` - Parses input rules and creates lookup dictionary
7. `divide_grid()` - Divides grid into blocks
8. `enhance_block()` - Applies enhancement rule to a single block
9. `reassemble_grid()` - Reassembles enhanced blocks
10. `perform_iterations()` - Main iteration loop (works for any iteration count)
11. `count_on_pixels()` - Counts '#' pixels in final grid

### What Changes
- **Only the iteration count parameter:** Change from 5 to 18 in the `main()` function

## Edge Cases to Consider
1. **Pattern matching:** All orientations are already handled by Part 1 code
2. **Grid division:** The logic correctly handles both size%2==0 and size%3==0 cases
3. **Block boundaries:** Reassembly logic correctly handles any block configuration
4. **Large grids:** Python's string and list handling is efficient enough for ~2187×2187

## Expected Output
- A single integer representing the count of '#' pixels after 18 iterations
- The value will be significantly larger than Part 1's answer (173)
- Expected range: Based on Part 1 data (173 pixels / 324 total ≈ 53% density), we can estimate Part 2 to have roughly 1-3 million active pixels out of 4,782,969 total pixels (2187²)

## Implementation Checklist
- [ ] Copy all helper functions from Part 1 solution
- [ ] Copy the main iteration and parsing logic
- [ ] Update iteration count from 5 to 18
- [ ] Verify input file path is correct
- [ ] Test with the provided input
- [ ] Count and output the final '#' pixel count
