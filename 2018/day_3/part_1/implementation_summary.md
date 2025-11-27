# Implementation Summary: Fabric Claim Overlap

## Problem Overview
Calculate the number of square inches of fabric that are claimed by 2 or more Elves. Each claim specifies a rectangular area on a fabric grid (at least 1000x1000 inches), and we need to find overlapping regions.

## Solution Approach
I implemented a 2D grid-based solution that tracks how many claims cover each square inch of fabric:

1. **Parse Claims**: Used regex pattern `#(\d+) @ (\d+),(\d+): (\d+)x(\d+)` to extract claim ID, left, top, width, and height from each line
2. **Dynamic Fabric Sizing**: Calculated required fabric dimensions by finding the maximum extents of all claims (ensuring at least 1000x1000)
3. **Grid Marking**: Created a 2D array where each cell stores the count of claims covering that position
4. **Overlap Counting**: Counted all cells with a value of 2 or more

## Implementation Details

### Data Structures
- **Claim**: Used `namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])` for clean, readable code
- **Fabric Grid**: 2D list `[[0] * width for _ in range(height)]` where each cell stores claim count

### Key Functions
1. `parse_claim(line)`: Parses claim format using regex
2. `get_fabric_dimensions(claims)`: Calculates required grid size
3. `create_fabric_grid(width, height)`: Initializes grid to zeros
4. `mark_claim_on_grid(grid, claim)`: Increments cells covered by a claim
5. `count_overlaps(grid)`: Counts cells with 2+ claims

### Coordinate System
- Origin (0,0) at top-left corner
- X axis (left) increases rightward
- Y axis (top) increases downward
- Rectangle at (left, top) with (width, height) covers cells from (left, top) to (left+width-1, top+height-1) inclusive

## Files Created
- **solution.py**: Main implementation with all functions and the main program
- **test_example.txt**: Test file with the example from the problem statement

## Testing Process

### Test 1: Example from Problem Statement
**Input**:
```
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
```
**Expected**: 4 overlapping square inches
**Result**: ✓ PASSED (output: 4)

### Test 2: No Overlaps
**Input**: Three spatially separated 5x5 claims
**Expected**: 0 overlapping square inches
**Result**: ✓ PASSED (output: 0)

### Test 3: Complete Overlap
**Input**: Three identical 3x3 claims at the same position
**Expected**: 9 overlapping square inches (all cells claimed by 3+ claims)
**Result**: ✓ PASSED (output: 9)

### Test 4: Adjacent Claims
**Input**: Two 3x3 claims that touch but don't overlap
**Expected**: 0 overlapping square inches
**Result**: ✓ PASSED (output: 0)

### Test 5: Single Claim
**Input**: One 10x10 claim
**Expected**: 0 overlapping square inches
**Result**: ✓ PASSED (output: 0)

### Test 6: Actual Input
**Input**: 1285 claims from input.md
**Metrics**:
- Total claims parsed: 1285
- Fabric dimensions: 1000x1000
- Max claim dimensions: 29x29
- Max positions: right=999, bottom=1000

**Result**: ✓ PASSED
**Answer**: **107820 square inches**

## Performance Analysis

### Time Complexity
- Parsing: O(n) where n = number of claims (1285)
- Grid marking: O(n × w × h) where w, h are average claim dimensions (~20×20)
- Counting: O(fabric_width × fabric_height) = O(1000 × 1000)
- Overall: O(n × w × h + fabric_size) ≈ 1.5M operations

### Space Complexity
- Grid storage: O(fabric_width × fabric_height) = 1,000,000 cells
- Claims list: O(n) = 1,285 claims
- Total: ~8-28 MB (Python integer objects)

### Actual Performance
- Execution time: < 1 second
- Memory usage: Minimal (within acceptable limits)
- No errors or warnings during execution

## Edge Cases Handled

1. ✓ Empty lines in input (skipped)
2. ✓ Malformed input (error handling with ValueError)
3. ✓ Claims extending beyond 1000x1000 (dynamic sizing)
4. ✓ No overlaps (returns 0)
5. ✓ Complete overlaps (counts correctly)
6. ✓ Adjacent non-overlapping claims (returns 0)
7. ✓ Single claim (returns 0)
8. ✓ Multiple claims on same cell (counted once, not multiple times)

## Correctness Verification

The solution was verified to be correct through:
1. ✓ Example test case from problem statement (4 overlaps)
2. ✓ Multiple edge case tests (all passed)
3. ✓ Actual input produces reasonable output (107,820)
4. ✓ Sanity checks:
   - Output is positive integer
   - Output < total fabric area (1,000,000)
   - All claims parsed successfully
   - No runtime errors

## Final Answer
**107,820 square inches** of fabric are within two or more claims.

## Code Quality

The implementation follows best practices:
- Clean, readable function names
- Proper documentation with docstrings
- Error handling for malformed input
- Efficient algorithms for the problem size
- Well-structured code with separation of concerns
- Comprehensive testing
