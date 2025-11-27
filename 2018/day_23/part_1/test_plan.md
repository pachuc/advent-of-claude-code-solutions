# Testing Plan: Nanobot Signal Range Analysis

## Testing Strategy

### Goals
1. Verify correctness of Manhattan distance calculation
2. Validate parsing logic handles input format correctly
3. Confirm strongest nanobot identification works
4. Ensure in-range counting is accurate
5. Validate solution with provided example
6. Test edge cases

### Testing Approach
- Unit tests for individual functions
- Integration test with example data
- Validation with actual input
- Manual calculation verification for small cases

## Test Cases

### Test 1: Manhattan Distance Function

**Purpose:** Verify Manhattan distance calculation is correct

**Test cases:**

| Point 1 | Point 2 | Expected Distance | Rationale |
|---------|---------|-------------------|-----------|
| (0,0,0) | (0,0,0) | 0 | Same point |
| (0,0,0) | (1,0,0) | 1 | One axis change |
| (0,0,0) | (1,1,1) | 3 | All axes change |
| (0,0,0) | (4,0,0) | 4 | Larger distance |
| (1,2,3) | (4,6,8) | 12 | All positive: \|1-4\| + \|2-6\| + \|3-8\| = 3+4+5 |
| (0,0,0) | (-5,-5,-5) | 15 | All negative coords |
| (5,5,5) | (-5,-5,-5) | 30 | Crossing origin |
| (-10,20,-30) | (10,-20,30) | 120 | Large mixed coordinates |

**Implementation:**
```python
def test_manhattan_distance():
    test_cases = [
        ((0,0,0), (0,0,0), 0),
        ((0,0,0), (1,0,0), 1),
        ((0,0,0), (1,1,1), 3),
        ((0,0,0), (4,0,0), 4),
        ((1,2,3), (4,6,8), 12),
        ((0,0,0), (-5,-5,-5), 15),
        ((5,5,5), (-5,-5,-5), 30),
        ((-10,20,-30), (10,-20,30), 120),
    ]
    for pos1, pos2, expected in test_cases:
        result = manhattan_distance(pos1, pos2)
        assert result == expected, f"Failed: {pos1} to {pos2}, got {result}, expected {expected}"
    print("✓ All Manhattan distance tests passed")
```

### Test 2: Input Parsing

**Purpose:** Verify parsing extracts correct values from input format

**Test input:**
```
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<-5,-10,15>, r=100
pos=<999999999,888888888,777777777>, r=123456789
```

**Expected output:**
```python
[
    (0, 0, 0, 4),
    (1, 0, 0, 1),
    (-5, -10, 15, 100),
    (999999999, 888888888, 777777777, 123456789)
]
```

**Validation checks:**
- Correct number of nanobots parsed
- Coordinates are integers (not strings)
- Negative coordinates handled
- Large numbers handled
- Radius correctly extracted

**Implementation:**
```python
def test_parse_input():
    import tempfile
    import os

    # Create temporary test file
    test_data = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<-5,-10,15>, r=100
pos=<999999999,888888888,777777777>, r=123456789"""

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(test_data)
        temp_path = f.name

    try:
        # Parse the file
        result = parse_input(temp_path)

        # Expected values
        expected = [
            (0, 0, 0, 4),
            (1, 0, 0, 1),
            (-5, -10, 15, 100),
            (999999999, 888888888, 777777777, 123456789)
        ]

        # Verify correct parsing
        assert len(result) == 4, f"Expected 4 nanobots, got {len(result)}"
        assert result == expected, f"Parsed data doesn't match expected"

        # Verify types are integers
        for bot in result:
            assert all(isinstance(val, int) for val in bot), "All values should be integers"

        print("✓ All parsing tests passed")
    finally:
        # Clean up temp file
        os.unlink(temp_path)
```

### Test 3: Find Strongest Nanobot

**Purpose:** Verify identification of nanobot with largest radius

**Implementation:**
```python
def test_find_strongest_nanobot():
    # Test case 1: Single maximum
    nanobots = [
        (0, 0, 0, 4),
        (1, 0, 0, 1),
        (4, 0, 0, 3),
        (0, 2, 0, 1),
    ]
    result = find_strongest_nanobot(nanobots)
    assert result == (0, 0, 0, 4), f"Expected (0,0,0,4), got {result}"

    # Test case 2: Maximum at end
    nanobots = [
        (0, 0, 0, 1),
        (1, 0, 0, 2),
        (4, 0, 0, 3),
        (0, 2, 0, 10),
    ]
    result = find_strongest_nanobot(nanobots)
    assert result == (0, 2, 0, 10), f"Expected (0,2,0,10), got {result}"

    # Test case 3: Multiple with same max (tie) - first one found
    nanobots = [
        (0, 0, 0, 5),
        (1, 0, 0, 5),
        (4, 0, 0, 3),
    ]
    result = find_strongest_nanobot(nanobots)
    assert result == (0, 0, 0, 5), f"Expected (0,0,0,5), got {result}"

    # Test case 4: Single nanobot
    nanobots = [(10, 20, 30, 100)]
    result = find_strongest_nanobot(nanobots)
    assert result == (10, 20, 30, 100), f"Expected (10,20,30,100), got {result}"

    print("✓ All find strongest nanobot tests passed")
```

### Test 4: Count in Range

**Purpose:** Verify counting logic correctly identifies nanobots in range

**Implementation:**
```python
def test_count_in_range():
    # Test case 1: Simple case - all in range
    nanobots = [
        (0, 0, 0, 10),
        (1, 0, 0, 1),
        (2, 0, 0, 1),
    ]
    strongest = (0, 0, 0, 10)
    result = count_in_range(nanobots, strongest)
    assert result == 3, f"Expected 3, got {result}"

    # Test case 2: Some out of range
    nanobots = [
        (0, 0, 0, 4),
        (1, 0, 0, 1),   # distance 1 ≤ 4 ✓
        (4, 0, 0, 3),   # distance 4 ≤ 4 ✓
        (5, 0, 0, 1),   # distance 5 > 4 ✗
    ]
    strongest = (0, 0, 0, 4)
    result = count_in_range(nanobots, strongest)
    assert result == 3, f"Expected 3, got {result}"

    # Test case 3: Boundary case (exactly at radius)
    nanobots = [
        (0, 0, 0, 5),
        (5, 0, 0, 1),   # distance exactly 5
    ]
    strongest = (0, 0, 0, 5)
    result = count_in_range(nanobots, strongest)
    assert result == 2, f"Expected 2, got {result}"

    # Test case 4: Only strongest in range
    nanobots = [
        (0, 0, 0, 1),
        (10, 10, 10, 1),
        (20, 20, 20, 1),
    ]
    strongest = (0, 0, 0, 1)
    result = count_in_range(nanobots, strongest)
    assert result == 1, f"Expected 1, got {result}"

    print("✓ All count in range tests passed")
```

### Test 5: Example from Problem Statement

**Purpose:** Validate complete solution with provided example

**Input:**
```
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
```

**Expected output:** 7

**Validation steps:**
1. Parse input correctly (9 nanobots)
2. Identify strongest: (0,0,0) with r=4
3. Calculate distances from (0,0,0):
   - (0,0,0): 0 ≤ 4 ✓
   - (1,0,0): 1 ≤ 4 ✓
   - (4,0,0): 4 ≤ 4 ✓
   - (0,2,0): 2 ≤ 4 ✓
   - (0,5,0): 5 > 4 ✗
   - (0,0,3): 3 ≤ 4 ✓
   - (1,1,1): 3 ≤ 4 ✓
   - (1,1,2): 4 ≤ 4 ✓
   - (1,3,1): 5 > 4 ✗
4. Count: 7

**Manual verification:**
- (1,3,1) distance: |0-1| + |0-3| + |0-1| = 1+3+1 = 5 ✓
- (0,5,0) distance: |0-0| + |0-5| + |0-0| = 0+5+0 = 5 ✓

### Test 6: Edge Cases

**Implementation:**
```python
def test_edge_cases():
    # Test case 1: Strongest nanobot at origin
    nanobots = [(0, 0, 0, 10), (5, 5, 5, 1)]
    strongest = find_strongest_nanobot(nanobots)
    result = count_in_range(nanobots, strongest)
    assert result == 2, f"Expected 2, got {result}"

    # Test case 2: Strongest nanobot far from origin
    nanobots = [
        (1000000, 1000000, 1000000, 100),
        (1000001, 1000000, 1000000, 1),
    ]
    strongest = find_strongest_nanobot(nanobots)
    result = count_in_range(nanobots, strongest)
    assert result == 2, f"Expected 2 (distance 1 from strongest), got {result}"

    # Test case 3: All nanobots at same position
    nanobots = [
        (5, 5, 5, 10),
        (5, 5, 5, 5),
        (5, 5, 5, 3),
    ]
    strongest = find_strongest_nanobot(nanobots)
    result = count_in_range(nanobots, strongest)
    assert result == 3, f"Expected 3 (all at distance 0), got {result}"

    # Test case 4: Zero radius
    nanobots = [
        (0, 0, 0, 0),
        (0, 0, 0, 5),
    ]
    strongest = find_strongest_nanobot(nanobots)
    result = count_in_range(nanobots, strongest)
    assert result == 2, f"Expected 2, got {result}"

    # Test case 5: Negative coordinates
    nanobots = [
        (-10, -20, -30, 100),
        (-11, -20, -30, 1),
    ]
    strongest = find_strongest_nanobot(nanobots)
    result = count_in_range(nanobots, strongest)
    assert result == 2, f"Expected 2 (distance 1), got {result}"

    print("✓ All edge case tests passed")
```

## Integration Testing

### Test 7: Full Pipeline with Example

**Implementation:**
```python
def test_example():
    import tempfile
    import os

    # Example data from problem statement
    example_data = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(example_data)
        temp_path = f.name

    try:
        # Parse and solve
        nanobots = parse_input(temp_path)
        assert len(nanobots) == 9, f"Expected 9 nanobots, got {len(nanobots)}"

        strongest = find_strongest_nanobot(nanobots)
        assert strongest == (0, 0, 0, 4), f"Expected strongest at (0,0,0) with r=4, got {strongest}"

        result = count_in_range(nanobots, strongest)
        assert result == 7, f"Expected 7 nanobots in range, got {result}"

        print("✓ Example test passed (result=7)")
    finally:
        os.unlink(temp_path)
```

**Verification checks:**
- Number of nanobots parsed: 9
- Strongest nanobot position: (0,0,0)
- Strongest nanobot radius: 4
- Final count: 7

### Test 8: Full Pipeline with Actual Input

**Steps:**
1. Run solution with actual input.md
2. Verify output is a reasonable number (between 1 and 1000)
3. Perform sanity checks:
   - Total nanobots: 1000
   - Strongest radius > 0
   - Count ≥ 1 (at least includes itself)
   - Count ≤ 1000 (cannot exceed total)
4. **Record the result**: After first successful run, record the output value to use for regression testing in future runs

**Additional validation:**
- Find strongest nanobot in input manually (grep for largest r value)
- Spot-check a few distance calculations manually

**Regression testing:**
- Once the correct answer is verified, add it as a constant in tests
- Future test runs should verify the result hasn't changed

## Test Execution Plan

### Phase 1: Unit Tests (in order)
1. Test manhattan_distance function
2. Test parse_input function
3. Test find_strongest_nanobot function
4. Test count_in_range function

### Phase 2: Integration Tests
1. Test with problem example (should output 7)
2. Test with actual input

### Phase 3: Validation
1. Manual verification of example calculations
2. Sanity checks on actual input result
3. Performance check (should run in < 1 second)

## Test Implementation

**Create test file: `test_solution.py`**

```python
from solution import manhattan_distance, parse_input, find_strongest_nanobot, count_in_range, main
import time

def run_all_tests():
    print("Running unit tests...")
    test_manhattan_distance()
    test_parse_input()
    test_find_strongest_nanobot()
    test_count_in_range()
    test_edge_cases()

    print("\nRunning integration tests...")
    test_example()

    print("\nRunning performance test...")
    test_performance()

    print("\n" + "="*50)
    print("✓ All tests passed!")
    print("="*50)

def test_performance():
    """Verify solution completes in reasonable time."""
    start = time.time()
    # Run main with actual input
    result = main()
    elapsed = time.time() - start

    assert elapsed < 1.0, f"Solution too slow: {elapsed:.3f}s (expected < 1.0s)"
    assert 1 <= result <= 1000, f"Result {result} outside valid range [1, 1000]"

    print(f"✓ Performance test passed ({elapsed:.3f}s, result={result})")
    return result

if __name__ == "__main__":
    run_all_tests()
```

## Success Criteria

### All tests must pass:
- ✓ Manhattan distance calculations correct
- ✓ Parser extracts all values correctly
- ✓ Strongest nanobot identified
- ✓ Count includes boundary cases (distance = radius)
- ✓ Example produces output of 7
- ✓ Actual input produces reasonable result (1-1000)

### Performance criteria:
- ✓ Solution completes in < 1 second
- ✓ No memory errors with 1000 nanobots

## Manual Verification Steps

### For example data:
1. Count lines in input: should be 9
2. Find max radius visually: should be 4 at position (0,0,0)
3. Calculate 2-3 distances manually to verify formula
4. Count how many are ≤ 4: should be 7

### For actual input:
1. Count lines: `wc -l input.md` should show 1000
2. Find max radius:
   - Method 1: `grep -o 'r=[0-9]*' input.md | cut -d= -f2 | sort -n | tail -1`
   - Method 2 (modern grep): `grep -oP 'r=\K[0-9]+' input.md | sort -n | tail -1`
3. Find which nanobot has max radius: `grep "r=$(grep -oP 'r=\K[0-9]+' input.md | sort -n | tail -1)" input.md`
4. Spot-check distance calculations for a few nanobots

## Debugging Strategies

### If tests fail:

**Manhattan distance wrong:**
- Print intermediate values (x1-x2, y1-y2, z1-z2)
- Check abs() is being used
- Verify order of operations

**Parsing wrong:**
- Print raw line and parsed result
- Check regex pattern
- Verify integer conversion

**Wrong strongest found:**
- Print all radii
- Verify max() key function
- Check tuple indexing (radius is index 3)

**Wrong count:**
- Print distances for all nanobots
- Check <= vs < comparison
- Verify strongest nanobot position extraction

## Expected Results

### Example test:
```
Input: 9 nanobots
Strongest: pos=<0,0,0>, r=4
In range count: 7
```

### Actual input test:
```
Input: 1000 nanobots
Strongest: pos=<...>, r=<max_radius>
In range count: <result between 1 and 1000>
```

The count should be deterministic and reproducible across multiple runs.
