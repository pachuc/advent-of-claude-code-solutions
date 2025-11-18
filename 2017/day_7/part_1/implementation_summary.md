# Implementation Summary: Recursive Circus - Finding the Bottom Program

## Problem Overview
The task was to find the bottom program (root node) in a tower of programs arranged in a tree structure. Programs are stacked on top of each other, with one program at the bottom supporting the entire tower. The input is an unordered list of program descriptions where each line contains a program name, weight, and optionally a list of child programs it holds.

## Solution Approach

### Algorithm: Set Difference
The solution uses a simple and efficient set-based approach:
1. Parse all program names into a set (`all_programs`)
2. Parse all child program names into another set (`all_children`)
3. The root is the single program in `all_programs` that is not in `all_children`
4. Time Complexity: O(n), Space Complexity: O(n)

### Implementation Details

The solution is implemented in `solution.py` with the following key components:

1. **Input Preprocessing**
   - Strip whitespace from input
   - Split into lines
   - Filter out empty/whitespace-only lines

2. **Parsing Logic**
   - For each line, split by `->` to separate parent from children
   - Extract parent name (text before `(`)
   - If children exist, split by `,` and collect all child names
   - Add parent to `all_programs` set
   - Add all children to `all_children` set

3. **Root Finding**
   - Compute `root_set = all_programs - all_children`
   - Assert exactly one root exists (sanity check)
   - Return the single root program name

## Files Created
- **solution.py**: Main solution file containing:
  - `find_bottom_program(input_data: str) -> str`: Core algorithm implementation
  - `main()`: Entry point that reads input.md and prints the result

## Testing Process

### Test Suite Executed
All tests passed successfully:

1. **Test 1.1 - Basic Example** ✓
   - Input: 13-line example from problem statement
   - Expected: `tknk`
   - Result: `tknk` ✓

2. **Test 1.2 - Single Program** ✓
   - Input: Single program with no children
   - Expected: `solo`
   - Result: `solo` ✓

3. **Test 1.3 - Linear Chain** ✓
   - Input: Three programs in a linear hierarchy
   - Expected: `bottom`
   - Result: `bottom` ✓

4. **Test 2.1 - Multiple Leaf Nodes** ✓
   - Input: Tree with multiple leaf nodes
   - Expected: `root`
   - Result: `root` ✓

5. **Test 2.2 - Varying Whitespace** ✓
   - Input: Programs with inconsistent whitespace formatting
   - Expected: `root`
   - Result: `root` ✓

6. **Test 2.3 - Single Child** ✓
   - Input: Parent with only one child
   - Expected: `root`
   - Result: `root` ✓

7. **Test 5.1 - Empty Lines** ✓
   - Input: Program descriptions with empty lines interspersed
   - Expected: `root`
   - Result: `root` ✓

### Actual Input Test
- **Input Size**: 1,337 lines (non-empty)
- **Result**: `wiapj`
- **Execution Time**: < 1 second
- **Verification**: ✓ Confirmed that `wiapj` appears as a parent in the input but never as a child

### Verification Details
The result was verified by:
1. Confirming `wiapj` appears in the input as a program definition
2. Confirming `wiapj` never appears in any children list (after `->`)
3. Found line: `wiapj (55) -> djzjiwd, lsire, vlbivgc, xdctkbj, ygvpk`

## Final Answer
**The bottom program is: `wiapj`**

## Code Quality
- Clean, readable implementation following the plan
- Proper documentation with docstrings
- Efficient O(n) algorithm
- Handles edge cases (whitespace, empty lines, various formats)
- Includes sanity check assertion for data validation

## Conclusion
The implementation successfully solves the problem using a simple and efficient set-based approach. All test cases pass, including the actual input file containing 1,337 programs. The solution is fast, correct, and maintainable.
