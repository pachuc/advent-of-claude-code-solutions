# Testing Plan: Spiral Memory Manhattan Distance

## Testing Strategy

### Objectives
1. Verify correctness of the spiral coordinate calculation
2. Validate Manhattan distance computation
3. Ensure all example cases pass
4. Test edge cases and boundary conditions
5. Verify the actual input produces correct output

## Test Categories

### 1. Example Test Cases (Given in Problem)

These are the test cases explicitly provided in the problem statement:

| Input | Expected Output | Description |
|-------|----------------|-------------|
| 1 | 0 | Center square (base case) |
| 12 | 3 | Example from problem |
| 23 | 2 | Example from problem |
| 1024 | 31 | Example from problem |

**Validation Method**:
```python
assert spiral_manhattan_distance(1) == 0
assert spiral_manhattan_distance(12) == 3
assert spiral_manhattan_distance(23) == 2
assert spiral_manhattan_distance(1024) == 31
```

### 2. Ring Boundary Test Cases

Test numbers at the corners and edges of each ring to ensure correct ring identification:

**Ring 1 (values 2-9, side length 3):**
- Value 2: (1, 0), distance = 1
- Value 3: (1, 1) top-right corner, distance = 2
- Value 4: (0, 1), distance = 1
- Value 5: (-1, 1) top-left corner, distance = 2
- Value 6: (-1, 0), distance = 1
- Value 7: (-1, -1) bottom-left corner, distance = 2
- Value 8: (0, -1), distance = 1
- Value 9: (1, -1) bottom-right corner, distance = 2

**Ring 2 (values 10-25, side length 5):**
- Value 10: (2, -1) start of ring, distance = 3
- Value 11: (2, 0), distance = 2
- Value 12: (2, 1), distance = 3
- Value 13: (2, 2) top-right corner, distance = 4
- Value 15: (0, 2), distance = 2
- Value 17: (-2, 2) top-left corner, distance = 4
- Value 19: (-2, 0), distance = 2
- Value 21: (-2, -2) bottom-left corner, distance = 4
- Value 23: (0, -2), distance = 2
- Value 25: (2, -2) bottom-right corner, distance = 4

**Validation Method**:
```python
# Ring 1 tests
assert spiral_manhattan_distance(2) == 1
assert spiral_manhattan_distance(3) == 2
assert spiral_manhattan_distance(4) == 1
assert spiral_manhattan_distance(5) == 2
assert spiral_manhattan_distance(9) == 2

# Ring 2 tests
assert spiral_manhattan_distance(10) == 3
assert spiral_manhattan_distance(11) == 2
assert spiral_manhattan_distance(13) == 4
assert spiral_manhattan_distance(17) == 4
assert spiral_manhattan_distance(21) == 4
assert spiral_manhattan_distance(25) == 4
```

### 3. Middle-of-Side Test Cases

Test values in the middle of each side of a ring (should have minimum distance for that ring):

**Pattern**: For ring k, the minimum distance is k (achieved at middle of each side where one coordinate is 0)

**Ring 1 middle positions (distance = 1):**
- Value 2: (1, 0) → distance 1 (middle of right side)
- Value 4: (0, 1) → distance 1 (middle of top side)
- Value 6: (-1, 0) → distance 1 (middle of left side)
- Value 8: (0, -1) → distance 1 (middle of bottom side)

**Ring 2 middle positions (distance = 2):**
- Value 11: (2, 0) → distance 2 (middle of right side)
- Value 15: (0, 2) → distance 2 (middle of top side)
- Value 19: (-2, 0) → distance 2 (middle of left side)
- Value 23: (0, -2) → distance 2 (middle of bottom side) ✓ matches given example!

**Validation Method**:
```python
# Ring 1 middle positions (distance = 1)
assert spiral_manhattan_distance(2) == 1
assert spiral_manhattan_distance(4) == 1
assert spiral_manhattan_distance(6) == 1
assert spiral_manhattan_distance(8) == 1

# Ring 2 middle positions (distance = 2)
assert spiral_manhattan_distance(11) == 2
assert spiral_manhattan_distance(15) == 2
assert spiral_manhattan_distance(19) == 2
assert spiral_manhattan_distance(23) == 2  # This matches given example!
```

### 4. Perfect Square Test Cases

Test perfect squares of odd numbers (these are bottom-right corners of rings):

- 9 = 3²: end of ring 1, at (1, -1), distance = 2
- 25 = 5²: end of ring 2, at (2, -2), distance = 4
- 49 = 7²: end of ring 3, at (3, -3), distance = 6
- 121 = 11²: end of ring 5, at (5, -5), distance = 10
- 1024 = 32² (even, so not a corner, but good test case - given in examples)

**Pattern**: Odd perfect square (2k+1)² ends at (k, -k) with distance 2k

**Validation Method**:
```python
assert spiral_manhattan_distance(9) == 2  # (1, -1)
assert spiral_manhattan_distance(25) == 4  # (2, -2)
assert spiral_manhattan_distance(49) == 6  # (3, -3)
assert spiral_manhattan_distance(121) == 10  # (5, -5)
```

### 5. Sequential Values Test

Test a sequence of consecutive numbers to verify the spiral path is correct:

**Values 1-10** (covers ring 0, ring 1, and start of ring 2):

Expected coordinates and distances:
- 1: (0, 0) → 0
- 2: (1, 0) → 1
- 3: (1, 1) → 2
- 4: (0, 1) → 1
- 5: (-1, 1) → 2
- 6: (-1, 0) → 1
- 7: (-1, -1) → 2
- 8: (0, -1) → 1
- 9: (1, -1) → 2
- 10: (2, -1) → 3

**Validation Method**:
```python
expected_distances = [0, 1, 2, 1, 2, 1, 2, 1, 2, 3]
for i, expected in enumerate(expected_distances, start=1):
    assert spiral_manhattan_distance(i) == expected, f"Failed for n={i}"
```

### 6. Large Value Test

Test the actual input value:

- Input: 289326
- Method: Since we can't manually verify, we'll check:
  1. Result is a positive integer
  2. Result is reasonable (not larger than would be expected)
  3. For ring k, max distance is 2k, min distance is k

**Validation Method**:
```python
result = spiral_manhattan_distance(289326)
assert isinstance(result, int)
assert result > 0

# Verify it's within reasonable bounds
# sqrt(289326) ≈ 538.08, ceil to odd = 539
# ring = 539 // 2 = 269
# Distance should be between 269 (min for ring) and 538 (max for ring)
assert 269 <= result <= 538
```

### 7. Coordinate Verification Test

For select test cases, manually verify the coordinates are correct:

**Manual Verification Grid** (for small values):
```
17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
```

Coordinates (with (0,0) at center, +X right, +Y up):
- 1: (0, 0)
- 2: (1, 0)
- 3: (1, 1)
- 4: (0, 1)
- 5: (-1, 1)
- 11: (2, 0)
- 12: (2, 1)
- 13: (2, 2)
- 23: (0, -2)

**Validation Method**: Create helper function to get coordinates and verify:
```python
def get_coordinates(n):
    """Extract coordinate calculation from main function"""
    # ... same logic as main function but return (x, y)

# Verify specific coordinates
assert get_coordinates(1) == (0, 0)
assert get_coordinates(2) == (1, 0)
assert get_coordinates(3) == (1, 1)
assert get_coordinates(4) == (0, 1)
assert get_coordinates(11) == (2, 0)
assert get_coordinates(12) == (2, 1)
assert get_coordinates(23) == (0, -2)
```

## Test Execution Plan

### Phase 1: Unit Tests
1. Create a test file `test_solution.py`
2. Implement all test cases above
3. Run tests and verify all pass
4. Fix any failures

### Phase 2: Manual Verification
1. For values 1-25, manually draw the spiral and verify coordinates
2. Check that calculated coordinates match the drawn spiral
3. Verify Manhattan distances are correct

### Phase 3: Actual Input Test
1. Run the solution with the actual input (289326)
2. Verify output is produced without errors
3. Check output is reasonable

### Phase 4: Edge Case Verification
1. Test with n=1 (minimum value)
2. Test with very large values (10^6, 10^9) to ensure no overflow
3. Verify performance is acceptable (should be near-instant)

## Success Criteria

✅ All example test cases pass
✅ All ring boundary tests pass
✅ All middle-of-side tests pass
✅ Sequential values produce expected pattern
✅ Coordinate verification matches manual calculation
✅ Actual input produces a reasonable result
✅ Solution runs in less than 1 second for all inputs
✅ No runtime errors or exceptions

## Test Implementation Structure

```python
def test_examples():
    """Test the provided examples"""
    assert spiral_manhattan_distance(1) == 0
    assert spiral_manhattan_distance(12) == 3
    assert spiral_manhattan_distance(23) == 2
    assert spiral_manhattan_distance(1024) == 31
    print("✓ Example tests passed")

def test_ring_boundaries():
    """Test corner and edge values of rings"""
    # Ring 1
    assert spiral_manhattan_distance(2) == 1
    assert spiral_manhattan_distance(9) == 2
    # Ring 2
    assert spiral_manhattan_distance(10) == 3
    assert spiral_manhattan_distance(25) == 4
    print("✓ Ring boundary tests passed")

def test_middle_positions():
    """Test middle of each side (minimum distance for ring)"""
    assert spiral_manhattan_distance(2) == 1
    assert spiral_manhattan_distance(4) == 1
    assert spiral_manhattan_distance(6) == 1
    assert spiral_manhattan_distance(8) == 1
    print("✓ Middle position tests passed")

def test_sequential():
    """Test first 10 values"""
    expected = [0, 1, 2, 1, 2, 1, 2, 1, 2, 3]
    for i, exp in enumerate(expected, 1):
        result = spiral_manhattan_distance(i)
        assert result == exp, f"n={i}: expected {exp}, got {result}"
    print("✓ Sequential tests passed")

def test_actual_input():
    """Test with the actual problem input"""
    result = spiral_manhattan_distance(289326)
    assert isinstance(result, int)
    assert result > 0
    print(f"✓ Actual input test passed: {result}")

def run_all_tests():
    """Run complete test suite"""
    test_examples()
    test_ring_boundaries()
    test_middle_positions()
    test_sequential()
    test_actual_input()
    print("\n✅ All tests passed!")
```

## Notes

- Tests are designed to be lightweight and fast
- Focus on correctness rather than exhaustive coverage
- Manual verification for small values provides confidence
- Actual input test ensures solution works for the problem at hand
