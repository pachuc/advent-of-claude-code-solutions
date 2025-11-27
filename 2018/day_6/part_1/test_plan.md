# Testing Plan: Largest Finite Area Using Manhattan Distance

## Testing Strategy

We need to verify correctness through:
1. Example test case validation (from problem statement)
2. Edge case testing
3. Visual verification (optional but helpful)
4. Full input validation

## Test 1: Example from Problem Statement

### Input
```
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
```

### Expected Behavior
- Coordinate at (1, 1) - labeled A - should have infinite area (touches boundary)
- Coordinate at (1, 6) - labeled B - should have infinite area (touches boundary)
- Coordinate at (8, 3) - labeled C - should have infinite area (touches boundary)
- Coordinate at (3, 4) - labeled D - should have area of 9
- Coordinate at (5, 5) - labeled E - should have area of 17
- Coordinate at (8, 9) - labeled F - should have infinite area (touches boundary)

### Expected Output
**17** (the largest finite area)

### Verification Steps
1. Run solution with example input
2. Verify output is exactly 17
3. Optionally: Print which coordinates have infinite areas and their counts for debugging

## Test 2: Edge Case - Single Coordinate

### Input
```
5, 5
```

### Expected Behavior
- Only one coordinate exists
- Its area extends to the bounding box boundary
- Therefore, it has infinite area
- No finite areas exist

### Expected Output
**0** - The single coordinate will touch the boundary and have infinite area, so there are no finite areas.

### Verification
- Ensure no crash
- Check that the single coordinate is correctly identified as infinite
- Result should be 0

## Test 3: Edge Case - Two Coordinates (Vertical Line)

### Input
```
5, 1
5, 10
```

### Expected Behavior
- Both coordinates are on the same vertical line
- Both should have infinite areas (touching top/bottom boundaries)
- Points exactly between them (same distance) should be ties

### Expected Output
**0** - Both coordinates touch boundaries, so no finite areas exist.

## Test 4: Edge Case - Three Coordinates (Triangle)

### Input
```
5, 5
10, 5
7, 10
```

### Expected Behavior
- Forms a triangle
- All three likely touch boundaries (infinite areas)
- Tests tie-breaking between three points

### Expected Output
Verify the algorithm correctly handles triangular configuration

## Test 5: Coordinates with Ties

### Input
```
0, 0
10, 0
0, 10
10, 10
```

### Expected Behavior
- Four coordinates at the corners of a 10x10 square
- Point (5, 5) is equidistant from all four corners (distance = 10 to each)
- Points along the line x=5 (like (5, 0) through (5, 10)) are equidistant from left and right pairs
- Points along the line y=5 are equidistant from top and bottom pairs
- Many cells will be equidistant from two or more coordinates
- Verify these tie points are not assigned to any coordinate (marked as None)

### Verification
- Check that tied cells are correctly excluded from all area counts
- Ensure no coordinate "wins" a tied cell
- Point (5, 5): distance to all corners = |5-0| + |5-0| = 10 ✓
- Point (5, 0): distance to (0,0) = 5, distance to (10,0) = 5 → tie ✓

## Test 6: Dense Cluster vs Isolated Point

### Input
```
5, 5
6, 5
5, 6
6, 6
50, 50
```

### Expected Behavior
- Four points form a tight cluster at (5,5) area
- One isolated point at (50, 50)
- The isolated point likely has infinite area (extends to boundary)
- The cluster points compete with each other, creating small finite areas

### Expected Output
Should correctly identify which has largest finite area

## Test 7: Grid with All Coordinates on Boundary

### Input
```
0, 0
0, 100
100, 0
100, 100
```

### Expected Behavior
- All four coordinates are at corners
- All have infinite areas
- No finite areas exist

### Expected Output
**0** - All coordinates are at corners and touch boundaries, so no finite areas exist.

## Test 8: Full Input Validation

### Input
Use the actual `input.md` file with 50 coordinates

### Verification Steps
1. Run the solution
2. Check that output is a positive integer
3. Verify runtime is reasonable (< 1 second)
4. Check no crashes or errors
5. **After verifying the answer is correct (via submission), add regression test**

### Expected Characteristics
- Should identify multiple coordinates with infinite areas (those near boundaries)
- Should find several coordinates with finite areas
- Largest finite area should be a reasonable number (likely hundreds to thousands)

### Regression Test
After confirming the correct answer:
```python
def test_full_input_regression():
    """Regression test - ensures answer doesn't change"""
    result = solve('input.md')
    # Replace EXPECTED with actual correct answer after verification
    assert result == EXPECTED, f"Expected {EXPECTED}, got {result}"
```

### Manual Validation Approach
- Plot the coordinates visually if needed
- Identify coordinates near the bounding box edges (these should be infinite)
- Identify coordinates in the interior (these are candidates for finite areas)
- The coordinate most "centered" and "isolated" in the interior likely has the largest area

## Test 9: Algorithm Correctness - Manhattan Distance

### Verification
Create a simple test case where Manhattan distances can be manually calculated:

### Input
```
2, 2
2, 4
```

### Manual Calculation
- Point (2, 3) should be a tie (distance 1 to both)
- Point (2, 1) is closest to (2, 2) - distance 1 vs 3
- Point (2, 5) is closest to (2, 4) - distance 1 vs 3
- Point (1, 3) is a tie (distance 2 to both)
- Point (3, 3) is a tie (distance 2 to both)

### Verification
Manually verify a few grid cells have correct assignments

## Test 10: Boundary Detection Correctness

### Verification Strategy
- After running on the example input, print which coordinates are identified as infinite
- Manually verify these are the ones touching the boundary
- For the example: A, B, C, F should be infinite; D, E should be finite

## Testing Implementation Approach

### Test Directory Structure
```
/app/agent_workspace/2018/day_6/part_1/
├── solution.py           # Main solution
├── test_solution.py      # Test runner
├── input.md             # Actual puzzle input
└── test_inputs/         # Test input files
    ├── example.txt      # Example from problem (expected: 17)
    ├── single.txt       # Single coordinate (expected: 0)
    ├── two_vertical.txt # Two points (expected: 0)
    └── four_corners.txt # Tie testing (expected: varies)
```

### Create test_solution.py
```python
from solution import solve

def test_example():
    """Test with the example from problem statement"""
    result = solve('test_inputs/example.txt')
    assert result == 17, f"Expected 17, got {result}"
    print("✓ Example test passed (result: 17)")

def test_single_coordinate():
    """Test with single coordinate - should be infinite"""
    result = solve('test_inputs/single.txt')
    assert result == 0, f"Expected 0, got {result}"
    print("✓ Single coordinate test passed (result: 0)")

def test_full_input():
    """Test with actual input"""
    result = solve('input.md')
    print(f"Result for full input: {result}")
    assert result > 0, "Should have a positive result"
    print("✓ Full input test passed")

def test_full_input_regression():
    """Regression test - add expected value after verification"""
    result = solve('input.md')
    # Uncomment after getting correct answer:
    # EXPECTED = ???  # Replace with actual answer
    # assert result == EXPECTED, f"Expected {EXPECTED}, got {result}"
    print(f"✓ Regression test: {result}")

def run_all_tests():
    """Run all test cases in recommended order"""
    print("Running tests...\n")

    # Critical tests first
    test_example()
    test_full_input()

    # Edge cases
    test_single_coordinate()

    # Regression
    test_full_input_regression()

    print("\n✅ All tests passed!")

if __name__ == '__main__':
    run_all_tests()
```

### Running Tests

**Setup**:
1. Create test input files in `test_inputs/` directory
2. Ensure `solution.py` is in the same directory

**Execute**:
```bash
# Run all tests
python test_solution.py

# Run solution on specific input
python solution.py input.md
python solution.py test_inputs/example.txt
```

**Test Creation**:
Create `test_inputs/example.txt`:
```
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
```

Create `test_inputs/single.txt`:
```
5, 5
```

## Visual Debugging (Recommended)

For understanding and debugging, **highly recommended** to create a visualization:
```python
def visualize_grid(grid, coordinates, min_x, max_x, min_y, max_y, infinite_coords):
    """
    Print a character grid showing which coordinate owns each cell.

    Legend:
    - 'A-Z' (uppercase): Infinite area coordinates
    - 'a-z' (lowercase): Finite area coordinates
    - '.': Tie (equidistant from multiple coordinates)
    - Numbers: If more than 26 coordinates
    """
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            coord_idx = grid.get((x, y))
            if coord_idx is None:
                row.append('.')
            elif coord_idx in infinite_coords:
                row.append(chr(ord('A') + coord_idx % 26))
            else:
                row.append(chr(ord('a') + coord_idx % 26))
        print(''.join(row))
```

**Why this is valuable**:
- Immediately spot incorrect assignments
- Verify boundary detection visually
- Confirm tie handling
- Match against problem examples
- Debug much faster than numeric output

**Usage**: Run on the example input first and verify the visualization matches the expected grid from the problem statement.

## Success Criteria

### Must Pass (Critical):
1. ✅ Example test returns exactly 17
2. ✅ Full input returns a positive integer
3. ✅ No runtime errors or crashes
4. ✅ Execution completes in under 1 second
5. ✅ Boundary coordinates correctly identified as infinite
6. ✅ Ties correctly handled (not assigned to any coordinate)
7. ✅ Manhattan distance calculation is accurate

### Should Pass (Important):
8. ✅ Single coordinate returns 0 (no finite areas)
9. ✅ All boundary coordinates returns 0 (no finite areas)
10. ✅ Visualization matches expected grid for example

### Nice to Have:
11. ✅ All edge case tests pass
12. ✅ Regression test maintains correct answer

## Debugging Checklist

If tests fail, check:
- [ ] Manhattan distance formula: `|x1 - x2| + |y1 - y2|`
- [ ] Boundary detection: checking all four edges (min_x, max_x, min_y, max_y)
- [ ] Tie handling: cells equidistant to multiple coordinates marked as None
- [ ] Index handling: coordinate indices consistent throughout
- [ ] Off-by-one errors: using inclusive ranges `range(min_x, max_x + 1)`
- [ ] Empty line handling in input parsing
