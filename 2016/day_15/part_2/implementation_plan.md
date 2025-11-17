# Implementation Plan - Part 2: Disc Timing Puzzle

## Overview
This implementation plan outlines a minimal-modification approach to solve Part 2 by reusing the Part 1 solution. The only required change is adding a single line of code to append the 7th disc to the disc list.

## Problem Summary
Find the earliest time to press a button to drop a capsule through 7 rotating discs (6 original discs from Part 1 + 1 new disc). The new 7th disc has 11 positions and starts at position 0.

## Key Insight: Reuse Part 1 Solution
The Part 1 solution (`part_1_solution.py`) already implements an efficient algorithm using LCM-based optimization. **We can reuse nearly all of this code** with only a single line modification to add the 7th disc.

## Algorithm Overview (from Part 1)
The algorithm solves a system of modular congruences optimally:
- For each disc i: `(initial_position[i] + T + i) % positions[i] == 0`
- Uses iterative approach: finds T for disc 1, then finds T for discs 1&2, then 1&2&3, etc.
- Key optimization: After satisfying disc i, step size becomes `lcm(previous_step, positions[i])`
- Time complexity: O(n × max_lcm) where n is number of discs
- Space complexity: O(n) for storing disc data

## Implementation Steps

### Step 1: Copy and Adapt Part 1 Code Structure
- Copy the entire `part_1_solution.py` as the starting point
- Keep all existing functions: `parse_input()`, `find_earliest_time()`, `is_valid_time()`, `main()`
- The core algorithm in `find_earliest_time()` requires **no changes**

### Step 2: Modify `main()` to Add 7th Disc
After parsing the 6 original discs from input file, programmatically add the 7th disc:
```python
# Parse the original 6 discs
discs = parse_input('input.md')

# Add the 7th disc: disc_num=7, positions=11, initial=0
discs.append((7, 11, 0))
```

**Location**: In `main()` function, immediately after line 59 (the parse_input call), before the print statements

### Step 3: Verify Disc Ordering (Optional Validation)
After adding the 7th disc, optionally verify sequential ordering:
- The parser validates sequential ordering for parsed discs (lines 23-25)
- The manually appended disc #7 should maintain this sequence
- No additional validation required unless debugging

### Step 4: Update Output Messages
No changes needed to print statements:
- The existing loop iterates over all discs in the list
- Adding the 7th disc to the list automatically includes it in output
- All verification messages work for any number of discs

### Step 5: Preserve Verification Logic
The existing verification in Part 1 is comprehensive:
- `is_valid_time(result, discs)` - verifies all discs align at time T
- Minimality check - verifies T-1 doesn't work
- Keep both checks unchanged

## Expected Behavior
1. Parse 6 discs from input.md
2. Programmatically add 7th disc (11 positions, starts at position 0)
3. Run `find_earliest_time()` with all 7 discs
4. Verify the result satisfies all 7 constraints
5. Output the earliest time T

## Why This Approach is Efficient
- **LCM optimization**: Step size grows exponentially (1 → 13 → 221 → 4199 → 29393 → 146965 → 440895 → 4849845)
- **Early constraint satisfaction**: Once disc i is satisfied, we only test multiples that preserve it
- **No brute force**: Never test consecutive integers after first few discs
- **Scalability**: Can handle very large position values efficiently

## Mathematical Foundation
Each disc creates a constraint:
- Disc 1: `T ≡ -11 (mod 13)` → `T ≡ 2 (mod 13)`
- Disc 2: `T ≡ -17 (mod 17)` → `T ≡ 0 (mod 17)`
- Disc 3: `T ≡ -20 (mod 19)` → `T ≡ 18 (mod 19)`
- Disc 4: `T ≡ -5 (mod 7)` → `T ≡ 2 (mod 7)`
- Disc 5: `T ≡ -5 (mod 5)` → `T ≡ 0 (mod 5)`
- Disc 6: `T ≡ -7 (mod 3)` → `T ≡ 2 (mod 3)`
- Disc 7: `T ≡ -7 (mod 11)` → `T ≡ 4 (mod 11)`

The algorithm finds the minimum non-negative T satisfying all constraints.

## Code Modifications Summary
**Changed**:
- `main()` function: Add one line to append 7th disc after line 59

**Unchanged**:
- `parse_input()` - still parses same input format
- `find_earliest_time()` - algorithm works for any disc count
- `is_valid_time()` - verification works for any disc count
- Print statements - loop automatically includes all discs in list
- Imports and overall structure

## Implementation Checklist
1. Copy `part_1_solution.py` content
2. Add `discs.append((7, 11, 0))` immediately after line 59 in `main()`
3. Verify the appended disc maintains sequential ordering (disc #7)
4. Test with input.md to ensure 7 discs are processed
5. Verify output is correct using built-in validation checks
