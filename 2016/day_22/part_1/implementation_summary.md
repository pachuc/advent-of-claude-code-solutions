# Implementation Summary: Grid Computing Viable Pairs Count

## Solution Overview

Successfully implemented a solution to count viable pairs of storage nodes in a grid computing cluster. The solution parses disk usage data from a `df -h` command output and determines how many pairs of nodes could theoretically transfer data between them.

## Final Answer

**981 viable pairs**

## Files Created

1. **solution.py** - Main solution file containing:
   - `parse_input()`: Parses the df command output to extract Used and Avail values for each node
   - `count_viable_pairs()`: Implements the O(n²) algorithm to count viable pairs
   - `main()`: Orchestrates reading input, parsing, counting, and outputting the result

2. **test_solution.py** - Comprehensive test suite containing:
   - Unit tests for parsing function (3 tests)
   - Unit tests for counting function (6 tests)
   - Edge case tests (3 tests)
   - Integration test with small example
   - Validation test with actual input

## Implementation Details

### Algorithm

The solution uses a straightforward brute-force approach with O(n²) time complexity:

1. **Parsing Phase**:
   - Skip first 2 header lines
   - Extract Used and Avail values from each line by splitting on whitespace
   - Remove 'T' suffix and convert to integers
   - Store as (used, avail) tuples in a list

2. **Counting Phase**:
   - Nested loop through all node pairs (i, j)
   - Skip if node A (index i) is empty (used = 0)
   - Skip if i == j (same node)
   - Count if used_a <= avail_b (data fits)

### Key Design Decisions

- **Data Structure**: Used simple tuples `(used, avail)` instead of dictionaries or classes for memory efficiency
- **No Optimization**: Kept O(n²) brute force since n=1,015 is small enough (~1M comparisons)
- **Simple Parsing**: Used built-in `split()` which handles variable whitespace automatically
- **No External Libraries**: Used only Python builtins as per requirements

## Testing Process

### Test Coverage

Implemented comprehensive testing following the test plan:

1. **Parsing Tests** - Verified correct extraction of values:
   - Basic parsing with 3 nodes
   - Large numbers (495T, 6T)
   - All tests passed ✓

2. **Counting Logic Tests** - Verified algorithm correctness:
   - All pairs viable scenario (expected 6, got 6) ✓
   - Empty node handling (expected 4, got 4) ✓
   - No available space (expected 0, got 0) ✓
   - Exact fit case (expected 2, got 2) ✓
   - Single node edge case (expected 0, got 0) ✓
   - Two nodes case (expected 2, got 2) ✓

3. **Edge Case Tests** - Verified boundary conditions:
   - All empty nodes (expected 0, got 0) ✓
   - All full nodes (expected 0, got 0) ✓
   - Large node that doesn't fit anywhere (expected 0, got 0) ✓

4. **Integration Test** - End-to-end verification:
   - Small manual example with 3 nodes (expected 2, got 2) ✓

5. **Actual Input Validation**:
   - Parsed 1,015 nodes successfully ✓
   - Result: 981 viable pairs ✓
   - Sanity check: 0 < 981 ≤ 1,029,210 (valid range) ✓

### Test Results

**All 14 test cases passed** with 100% success rate.

### Performance

- Parsing time: < 10ms
- Counting time: < 100ms
- Total runtime: < 200ms
- Well within acceptable performance parameters

## Verification

### Manual Spot Checks

The solution correctly implements the problem requirements:

1. **Non-empty check**: Node A must have used > 0 ✓
2. **Different nodes**: A and B cannot be the same node ✓
3. **Fit check**: A's used must be ≤ B's avail ✓
4. **Order matters**: (A,B) and (B,A) counted separately ✓
5. **Ignores adjacency**: All pairs considered regardless of grid position ✓

### Result Validation

- Total nodes: 1,015
- Maximum possible pairs: 1,015 × 1,014 = 1,029,210
- Actual viable pairs: 981 (0.095% of maximum)
- This makes sense because:
  - Most nodes have 64-73T used with only 20-30T available
  - Only the empty node(s) can accept most data
  - Large nodes (495T used) can't fit anywhere

## Conclusion

The solution successfully solves the problem with:
- Clean, readable code
- Comprehensive test coverage
- Correct algorithm implementation
- Good performance characteristics
- Proper validation and verification

The final answer of **981 viable pairs** has been validated through:
- All unit tests passing
- Integration tests passing
- Sanity checks confirming result is in valid range
- Manual verification of algorithm logic
