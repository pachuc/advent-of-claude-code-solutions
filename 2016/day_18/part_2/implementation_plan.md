# Implementation Plan: Safe Tile Counter (Part 2)

## Overview
Part 2 scales Part 1 from 40 rows to 400,000 rows. The algorithm and rules remain identical. The Part 1 solution is already efficient and memory-conscious, so minimal changes are required.

## Algorithm Analysis

### Time Complexity
- **O(n × m)** where n = number of rows (400,000), m = row length (~100)
- Total operations: ~40 million
- Each operation is a simple character comparison and string building
- Expected runtime: < 10 seconds on modern hardware

### Space Complexity
- **O(m)** - only stores current row, not all rows
- Memory usage: negligible (< 1 KB for row storage)
- Part 1 solution already optimized for this

### Why Part 1 Solution is Sufficient
1. Already uses iterative row generation (no recursion)
2. Only stores current row in memory (not all 400,000 rows)
3. Counts safe tiles incrementally per row
4. No exponential growth or inefficient data structures
5. Simple string operations are fast in Python

## Implementation Steps

### Step 1: Copy and Adapt Part 1 Solution
- Copy the entire `part_1_solution.py` as the base
- The core algorithm functions require **zero changes**:
  - `is_trap()` - unchanged
  - `generate_next_row()` - unchanged
  - `count_safe_tiles()` - unchanged (already parameterized for row count)
  - `parse_input()` - unchanged

### Step 2: Update Main Function
- Modify the `main()` function to change row count from 40 to 400,000
- **Change required**: `count_safe_tiles(first_row, 40)` → `count_safe_tiles(first_row, 400000)`
- That's the only modification needed!

### Step 3: Add Input Validation
- After reading input, add validation checks:
  - Verify input length is correct (should be 100 characters)
  - Verify input contains only valid characters ('.' and '^')
- This prevents silent failures from malformed input
- **Implementation**:
  ```python
  assert len(first_row) == 100, f"Input should be 100 characters, got {len(first_row)}"
  assert all(c in '.^' for c in first_row), "Input contains invalid characters"
  ```

### Step 4: Verify Input Reading
- Ensure `parse_input()` correctly reads from `input.md`
- Input should be the same as Part 1: `.^^^^^.^^.^^^.^...^..^^.^.^..^^^^^^^^^^..^...^^.^..^^^^..^^^^...^.^.^^^^^^^^....^..^^^^^^.^^^.^^^.^^`
- No changes needed to parsing logic

### Step 5: Add Row Count Verification
- Add verification that exactly 400,000 rows are processed
- This catches typos like 40,000 or 4,000,000
- **Implementation options**:
  - Add debug output showing final row number (0-indexed: should be 399,999)
  - Add assertion after loop: `assert row_num == total_rows - 1`
  - Both approaches ensure correct row count

### Step 6: Optional Progress Indication
- For 400,000 rows (potentially 10-15 seconds), consider progress output
- **Implementation** (optional):
  ```python
  if row_num % 100000 == 0 and row_num > 0:
      print(f"Processing row {row_num}...", file=sys.stderr)
  ```
- This helps user know the program hasn't frozen
- Output to stderr to keep stdout clean for the answer

### Step 7: Output Format
- Print single integer result (total safe tiles across 400,000 rows)
- Same format as Part 1
- No changes needed to output logic

## Detailed Code Structure

```python
# Part 1 functions - NO CHANGES NEEDED
def parse_input(filename='input.md'):
    # Reads first row from input file
    pass

def is_trap(left, center, right):
    # Returns True if left != right
    pass

def generate_next_row(current_row):
    # Generates next row based on trap rules
    pass

def count_safe_tiles(first_row, total_rows):
    # Iteratively generates rows and counts safe tiles
    # ALREADY PARAMETERIZED - works for any row count
    # OPTIONAL: Add progress output and verification
    pass

# UPDATED: Add validation and verification
def main():
    first_row = parse_input('input.md')

    # NEW: Input validation
    assert len(first_row) == 100, f"Input should be 100 characters, got {len(first_row)}"
    assert all(c in '.^' for c in first_row), "Input contains invalid characters"

    # CHANGED: Row count from 40 to 400,000
    result = count_safe_tiles(first_row, 400000)
    print(result)
```

## Implementation Checklist

1. **Reuse Part 1 Code**
   - [ ] Copy all helper functions unchanged
   - [ ] Copy `count_safe_tiles()` unchanged
   - [ ] Verify the simplified rule `left != right` is used

2. **Update Configuration**
   - [ ] Change row count parameter from 40 to 400,000 in `main()`

3. **Add Validation and Verification**
   - [ ] Add input validation (length = 100, characters in '.^')
   - [ ] Add row count verification (assert or debug output)
   - [ ] Optional: Add progress indication for user feedback

4. **Verify I/O**
   - [ ] Confirm input file is `input.md`
   - [ ] Confirm output is single integer to stdout
   - [ ] Confirm progress messages (if any) go to stderr

5. **Code Quality**
   - [ ] Keep docstrings from Part 1 (already well documented)
   - [ ] No additional error handling needed (out of scope)
   - [ ] No logging needed (out of scope)

## Optimization Considerations

### Current Algorithm is Already Optimal
- **String operations**: Python's string methods are C-optimized
- **Counting**: `str.count('.')` is highly efficient
- **Memory**: Only one row stored at a time (O(m) space)
- **No premature optimization needed**

### Why NOT to Change Anything
1. List building for next row is fine (100 chars × 400k rows = manageable)
2. String joins are efficient in Python
3. No benefit from numpy/arrays for this problem size
4. Code clarity > micro-optimizations for this use case

### If Performance Issues Arise (unlikely)
- Could use list of characters instead of strings
- Could use boolean arrays (0/1 instead of './^')
- Could use bitwise operations
- **But these are NOT needed for 400k rows**

## Expected Behavior

### Runtime
- Part 1 (40 rows): near-instantaneous
- Part 2 (400,000 rows): 5-15 seconds expected
- Linear scaling: 10,000× more rows = ~10,000× more time

### Output
- Single integer representing total safe tiles
- Should be significantly larger than Part 1's answer (1989)
- Rough estimate: 1989 × 10,000 ≈ 20 million (ballpark)

## Risk Assessment

### Low Risk Items
- Algorithm correctness: Part 1 already validated
- Memory usage: Only stores one row
- Integer overflow: Python handles arbitrary precision

### No Risks
- Stack overflow: iterative, not recursive
- Timeout: O(n×m) is efficient for this size
- Off-by-one errors: Part 1 already handled boundaries

## Summary

This is a **trivial port** from Part 1 to Part 2. The only change required is updating the row count parameter from 40 to 400,000. The Part 1 solution was already designed efficiently and handles the scale increase without any algorithmic modifications.
