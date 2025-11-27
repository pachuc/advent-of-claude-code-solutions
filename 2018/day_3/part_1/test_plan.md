# Testing Plan: Fabric Claim Overlap

## Testing Strategy

### 1. Unit Tests
Test individual functions in isolation to ensure correctness.

### 2. Integration Tests
Test the complete workflow with known inputs and expected outputs.

### 3. Edge Case Tests
Verify behavior with boundary conditions and special cases.

## Detailed Test Cases

### Test 0: Rectangle Edge Inclusion Test

**Purpose**: Verify that rectangle edges are correctly inclusive/exclusive

**Input**:
```
#1 @ 2,2: 3x3
#2 @ 5,2: 3x3
```

**Expected Output**: `0`

**Reasoning**:
- Claim 1 covers columns 2,3,4 and rows 2,3,4 (right edge at column 4, bottom edge at row 4)
- Claim 2 covers columns 5,6,7 and rows 2,3,4 (left edge at column 5)
- These rectangles are adjacent but don't overlap (column 5 ≠ column 4)
- Confirms that a claim at (left, top) with (width, height) covers:
  - Columns from left to (left + width - 1) inclusive
  - Rows from top to (top + height - 1) inclusive

**Verification Method**:
- Run solution with test input
- Assert output equals 0
- Critical for verifying correct boundary behavior

### Test 1: Parse Claim Function

**Purpose**: Verify claim parsing extracts correct values

**Test Cases**:

```python
# Test 1.1: Standard claim
input: "#123 @ 3,2: 5x4"
expected: Claim(id=123, left=3, top=2, width=5, height=4)

# Test 1.2: Single digit values
input: "#1 @ 0,0: 1x1"
expected: Claim(id=1, left=0, top=0, width=1, height=1)

# Test 1.3: Large values
input: "#1286 @ 999,999: 29x29"
expected: Claim(id=1286, left=999, top=999, width=29, height=29)

# Test 1.4: Multiple digit positions
input: "#456 @ 123,456: 12x34"
expected: Claim(id=456, left=123, top=456, width=12, height=34)

# Test 1.5: Extra whitespace
input: "#123  @  3,2:  5x4"
expected: Claim(id=123, left=3, top=2, width=5, height=4)

# Test 1.6: Malformed input (should raise ValueError)
input: "invalid claim format"
expected: ValueError exception
```

**Verification Method**:
- Parse each test input
- Assert returned Claim namedtuple matches expected values
- Verify all values are integers
- Test that malformed input raises ValueError

### Test 2: Example from Problem Statement

**Purpose**: Verify solution works for the given example

**Input**:
```
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
```

**Expected Output**: `4`

**Reasoning**:
- Claim 1 covers: (1,3) to (4,6) - 16 cells
- Claim 2 covers: (3,1) to (6,4) - 16 cells
- Claim 3 covers: (5,5) to (6,6) - 4 cells
- Overlap between 1 and 2: cells (3,3), (3,4), (4,3), (4,4) = 4 cells
- No overlap with claim 3

**Verification Method**:
- Create test input file or string
- Run complete solution
- Assert output equals 4
- Optionally verify grid state visually

### Test 3: No Overlaps

**Purpose**: Verify correct behavior when claims don't overlap

**Input**:
```
#1 @ 0,0: 5x5
#2 @ 10,10: 5x5
#3 @ 20,20: 5x5
```

**Expected Output**: `0`

**Reasoning**: All claims are spatially separated

**Verification Method**:
- Run solution with test input
- Assert output equals 0

### Test 4: Complete Overlap

**Purpose**: Verify handling of multiple claims on same area

**Input**:
```
#1 @ 5,5: 3x3
#2 @ 5,5: 3x3
#3 @ 5,5: 3x3
```

**Expected Output**: `9`

**Reasoning**: All 9 cells are claimed by 3 different claims (count = 3 for each cell)

**Verification Method**:
- Run solution with test input
- Assert output equals 9
- Verify each cell in the region has count >= 2

### Test 5: Partial Overlaps

**Purpose**: Test various overlap configurations

**Input**:
```
#1 @ 0,0: 4x4
#2 @ 2,2: 4x4
#3 @ 4,4: 4x4
```

**Expected Output**: `8`

**Reasoning**:
- Claim 1 and 2 overlap in 2x2 area (cells (2,2) to (3,3)) = 4 cells
- Claim 2 and 3 overlap in 2x2 area (cells (4,4) to (5,5)) = 4 cells
- Total overlapping cells = 8

**Verification Method**:
- Run solution with test input
- Assert output equals 8

### Test 6: Adjacent Claims (No Overlap)

**Purpose**: Verify adjacent claims don't count as overlaps

**Input**:
```
#1 @ 0,0: 5x5
#2 @ 5,0: 5x5
#3 @ 0,5: 5x5
```

**Expected Output**: `0`

**Reasoning**: Claims touch edges but don't share any cells

**Verification Method**:
- Run solution with test input
- Assert output equals 0

### Test 7: Single Claim

**Purpose**: Verify single claim produces no overlaps

**Input**:
```
#1 @ 100,100: 10x10
```

**Expected Output**: `0`

**Reasoning**: Only one claim, no overlap possible

**Verification Method**:
- Run solution with test input
- Assert output equals 0

### Test 8: Grid Boundary Cases

**Purpose**: Verify claims at grid edges work correctly

**Input**:
```
#1 @ 0,0: 5x5
#2 @ 0,0: 3x3
#3 @ 994,994: 6x6
#4 @ 996,996: 4x4
```

**Expected Output**: `9 + 16 = 25`

**Reasoning**:
- Top-left corner: claims 1 and 2 overlap in 3x3 area = 9 cells
- Bottom-right corner:
  - Claim 3 covers (994,994) to (999,999) - 6x6 = 36 cells
  - Claim 4 covers (996,996) to (999,999) - 4x4 = 16 cells
  - Overlap: (996,996) to (999,999) = 4x4 = 16 cells

**Verification Method**:
- Run solution with test input
- Assert output equals 25
- Verify no index out of bounds errors
- This tests that grid dimensions are calculated correctly from claims

### Test 9: Three-Way Overlap

**Purpose**: Verify cells with 3+ claims are counted correctly (once each)

**Input**:
```
#1 @ 0,0: 4x4
#2 @ 1,1: 4x4
#3 @ 2,2: 4x4
```

**Expected Output**: `15`

**Reasoning** (simplified example for easier verification):
- Claim 1: (0,0) to (3,3) - 16 cells total
- Claim 2: (1,1) to (4,4) - 16 cells total
- Claim 3: (2,2) to (5,5) - 16 cells total
- Overlap between 1&2: (1,1) to (3,3) = 3x3 = 9 cells
- Overlap between 2&3: (2,2) to (4,4) = 3x3 = 9 cells
- Overlap between 1&3: (2,2) to (3,3) = 2x2 = 4 cells (subset of both above)
- Three-way overlap (1&2&3): (2,2) to (3,3) = 2x2 = 4 cells
- Total unique cells with ≥2 claims: 9 + 9 - 4 = 14... Let me recalculate:
  - Cells with count=2: (1&2 only)+(2&3 only) = (9-4)+(9-4) = 5+5 = 10 cells
  - Cells with count=3: (1&2&3) = 4 cells
  - Total = 10 + 4 = 14 cells... Actually:
  - Row 1: cols 1,2,3 (3 cells, count=2 from claims 1&2)
  - Row 2: col 1 (1 cell, count=2 from 1&2), cols 2,3 (2 cells, count=3 from 1&2&3), col 4 (1 cell, count=2 from 2&3)
  - Row 3: col 1 (1 cell, count=2 from 1&2), cols 2,3 (2 cells, count=3 from 1&2&3), col 4 (1 cell, count=2 from 2&3)
  - Row 4: cols 2,3,4 (3 cells, count=2 from 2&3)
  - Total: 3 + 4 + 4 + 3 = 14 cells

Wait, let me recount more carefully:
- (1,1): claims 1,2 → count=2 ✓
- (1,2): claims 1,2 → count=2 ✓
- (1,3): claims 1,2 → count=2 ✓
- (2,1): claims 1,2 → count=2 ✓
- (2,2): claims 1,2,3 → count=3 ✓
- (2,3): claims 1,2,3 → count=3 ✓
- (2,4): claims 2,3 → count=2 ✓
- (3,1): claims 1,2 → count=2 ✓
- (3,2): claims 1,2,3 → count=3 ✓
- (3,3): claims 1,2,3 → count=3 ✓
- (3,4): claims 2,3 → count=2 ✓
- (4,2): claims 2,3 → count=2 ✓
- (4,3): claims 2,3 → count=2 ✓
- (4,4): claims 2,3 → count=2 ✓
Total: 14 cells

**Expected Output**: `14`

**Verification Method**:
- Run solution with test input
- Assert output equals 14
- This verifies cells with 3 claims are counted once (not multiple times)

### Test 10: Actual Input Validation

**Purpose**: Verify solution works on the actual problem input

**Input**: Use provided input.md file (1286 claims)

**Expected Output**: Unknown (to be calculated by the solution)

**Verification Method**:
- Run solution on actual input
- Verify output is a positive integer
- Sanity check bounds:
  - Should be > 0 (given 1286 claims, overlaps are highly likely)
  - Should be < total grid area (upper bound)
  - Reasonable range: likely between 10,000 and 500,000 square inches

**Additional Checks**:
- Ensure all 1286 claims are parsed successfully
- Verify no parsing errors or exceptions
- Check execution time (should be < 2 seconds)
- Verify memory usage is reasonable (< 100 MB)
- If this is an Advent of Code problem, the answer can be verified by submitting

## Testing Implementation Strategy

### Manual Testing Steps

1. **Create test files**: Save each test case input to a temporary file
2. **Run solution**: Execute solution with test input
3. **Verify output**: Compare actual output to expected output
4. **Debug if needed**: Print grid state for visual verification

### Automated Testing Approach

```python
def test_parse_claim():
    """Test claim parsing"""
    test_cases = [
        ("#123 @ 3,2: 5x4", (123, 3, 2, 5, 4)),
        ("#1 @ 0,0: 1x1", (1, 0, 0, 1, 1)),
        # ... more cases
    ]
    for input_str, expected in test_cases:
        result = parse_claim(input_str)
        assert result == expected, f"Failed for {input_str}"

def test_example():
    """Test example from problem statement"""
    claims = [
        parse_claim("#1 @ 1,3: 4x4"),
        parse_claim("#2 @ 3,1: 4x4"),
        parse_claim("#3 @ 5,5: 2x2")
    ]
    grid = create_fabric_grid(10, 10)
    for claim in claims:
        mark_claim_on_grid(grid, claim)
    result = count_overlaps(grid)
    assert result == 4, f"Expected 4, got {result}"

def test_no_overlap():
    """Test non-overlapping claims"""
    # Similar structure...
```

### Visual Verification Helper

```python
def print_grid(grid, max_rows=20, max_cols=20):
    """Print grid for visual inspection (for small grids)"""
    for i, row in enumerate(grid[:max_rows]):
        print(''.join(str(min(cell, 9)) for cell in row[:max_cols]))
```

## Success Criteria

### Unit Tests
- ✓ All claim parsing tests pass
- ✓ Grid creation produces correct dimensions
- ✓ Claim marking correctly increments cells
- ✓ Overlap counting correctly identifies cells with 2+ claims

### Integration Tests
- ✓ Example from problem statement produces correct output (4)
- ✓ All edge case tests produce expected outputs
- ✓ No runtime errors or exceptions

### Performance Tests
- ✓ Actual input processes in < 1 second
- ✓ Memory usage < 100 MB
- ✓ No integer overflow issues

### Correctness Validation
- ✓ Output is a non-negative integer
- ✓ Output is less than total fabric area (1,000,000)
- ✓ For actual input, output should be reasonable (likely 10,000-500,000 range)

## Debugging Strategies

If tests fail:

1. **Parse errors**: Print parsed claim tuples, verify regex pattern
2. **Wrong overlap count**: Print small grid visually, check indexing
3. **Index errors**: Verify grid dimensions, check boundary conditions
4. **Logic errors**: Test with minimal example (2 overlapping 2x2 claims)

## Test Execution Order

1. Test parsing function first (foundation) - Test 1
2. Test rectangle edge inclusion (critical boundary behavior) - Test 0
3. Test example from problem (integration) - Test 2
4. Test edge cases (comprehensive) - Tests 3-9
5. Test actual input (final validation) - Test 10

## Updates Based on Critique

### Critical Fixes Applied

1. **Test 8 (Grid Boundary Cases)**:
   - Fixed index out of bounds issue
   - Changed from claims extending to (1000,1000) to (999,999)
   - Adjusted expected output from 18 to 25 based on correct calculations

2. **Test 9 (Three-Way Overlap)**:
   - Completed the manual calculation that was missing
   - Simplified the example from 6x6 claims to 4x4 claims for easier verification
   - Provided complete cell-by-cell enumeration
   - Corrected expected output to 14 cells

3. **Test 1 (Parse Claim Function)**:
   - Updated to use Claim namedtuple instead of plain tuple
   - Added Test 1.5 for extra whitespace handling
   - Added Test 1.6 for malformed input error handling

### Additional Improvements

4. **Test 0 (Rectangle Edge Inclusion)**:
   - Added new test to verify off-by-one boundary behavior
   - Critical for confirming inclusive/exclusive edge semantics
   - Tests that adjacent rectangles don't overlap

5. **Test 10 (Actual Input)**:
   - Clarified that expected output is unknown (to be calculated)
   - Added note about Advent of Code verification if applicable
   - Refined sanity check ranges

### Tests Consistency with Implementation Plan

All tests now align with the updated implementation plan:
- Grid dimensions are dynamically calculated (fixes Test 8 issue)
- Uses Claim namedtuple (fixes Test 1)
- Includes error handling for malformed input (Test 1.6)
- Coordinate system is clearly documented (Test 0)
