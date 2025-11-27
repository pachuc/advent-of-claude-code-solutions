# Testing Plan: The Stars Align

## Overview
Comprehensive testing strategy to verify the solution correctly identifies when points align and displays the message.

## Test Categories

### 1. Unit Tests for Input Parsing

#### Test 1.1: Parse Single Line
**Objective**: Verify parsing of a single input line with various formats.

**Test Cases**:
```python
# Standard format
"position=< 9,  1> velocity=< 0,  2>"
Expected: (9, 1, 0, 2)

# Negative values
"position=<-39892,  -9859> velocity=< 4,  1>"
Expected: (-39892, -9859, 4, 1)

# Mixed signs
"position=< 10130,  10163> velocity=<-1, -1>"
Expected: (10130, 10163, -1, -1)

# Large negative values
"position=<-49939,  50212> velocity=< 5, -5>"
Expected: (-49939, 50212, 5, -5)
```

**Validation**: Ensure all four integers are correctly extracted.

#### Test 1.2: Parse Multiple Lines
**Objective**: Verify parsing of entire input file.

**Test Cases**:
- Parse the full input.md (356 lines based on actual count)
- Verify count matches expected number of points
- Verify no parsing errors or exceptions
- Spot-check first, middle, and last entries

**Validation**:
```python
# First verify actual line count in input.md
# wc -l input.md shows 356 lines
assert len(points) == 356
# Verified against actual input.md:
assert points[0] == (-39892, -9859, 4, 1)  # First line from input.md
assert points[-1] == (-9860, -9862, 1, 1)  # Last line (356) from input.md
assert points[100] == (30189, -9863, -3, 1)  # Middle check
```

### 2. Unit Tests for Position Calculation

#### Test 2.1: Position at t=0
**Objective**: Verify initial positions are unchanged.

**Test Cases**:
```python
point = (9, 1, 0, 2)
positions = calculate_positions([point], t=0)
Expected: [(9, 1)]
```

#### Test 2.2: Position at t=1
**Objective**: Verify single time step calculation.

**Test Cases**:
```python
point = (9, 1, 0, 2)
positions = calculate_positions([point], t=1)
Expected: [(9, 3)]  # y increases by 2

point = (10, 5, -2, -1)
positions = calculate_positions([point], t=1)
Expected: [(8, 4)]
```

#### Test 2.3: Position at Large t
**Objective**: Verify calculation with large time values.

**Test Cases**:
```python
point = (0, 0, 3, -4)
positions = calculate_positions([point], t=10000)
Expected: [(30000, -40000)]
```

**Validation**: Check for integer overflow (Python handles big integers natively).

#### Test 2.4: Multiple Points
**Objective**: Verify batch calculation.

**Test Cases**:
```python
points = [(0, 0, 1, 1), (10, 10, -1, -1)]
positions = calculate_positions(points, t=5)
Expected: [(5, 5), (5, 5)]  # Points converge!
```

### 3. Unit Tests for Bounding Box

#### Test 3.1: Single Point
**Objective**: Verify bounding box for single point.

**Test Cases**:
```python
positions = [(5, 10)]
bbox = get_bounding_box(positions)
Expected: (5, 10, 5, 10)
Width: 0, Height: 0, Area: 0
```

#### Test 3.2: Two Points
**Objective**: Verify bounding box calculation.

**Test Cases**:
```python
positions = [(0, 0), (10, 20)]
bbox = get_bounding_box(positions)
Expected: (0, 0, 10, 20)
Width: 10, Height: 20, Area: 200
```

#### Test 3.3: Negative Coordinates
**Objective**: Verify handling of negative coordinates.

**Test Cases**:
```python
positions = [(-10, -5), (10, 5)]
bbox = get_bounding_box(positions)
Expected: (-10, -5, 10, 5)
Width: 20, Height: 10, Area: 200
```

#### Test 3.4: Large Coordinate Range
**Objective**: Verify with input-scale coordinates.

**Test Cases**:
```python
positions = [(-50000, -50000), (50000, 50000)]
bbox = get_bounding_box(positions)
Expected: (-50000, -50000, 50000, 50000)
Width: 100000, Height: 100000
```

### 4. Integration Tests for Alignment Detection

#### Test 4.1: Simple Convergence
**Objective**: Verify detection of alignment time with a minimal example.

**Test Cases**:
Create a simple scenario where points converge at known time:
```python
# Points converge at t=5
points = [
    (0, 0, 1, 1),
    (10, 10, -1, -1)
]
# At t=5: both at (5, 5) - minimum area = 0
# At t=4: Point 1=(4, 4), Point 2=(6, 6) - area = (6-4) * (6-4) = 4
# At t=6: Point 1=(6, 6), Point 2=(4, 4) - area = (6-4) * (6-4) = 4

alignment_time = find_alignment_time(points)
Expected: 5
```

#### Test 4.2: Area Monotonicity Check
**Objective**: Verify that area decreases then increases around alignment.

**Test Cases**:
- For a known convergence scenario, track area over time
- Verify area[t-1] > area[t] < area[t+1] at alignment time
- Ensure no premature termination

#### Test 4.3: No Exact Convergence
**Objective**: Verify handling when points don't converge to single point.

**Test Cases**:
```python
# Points form a small box at best alignment
points = [
    (0, 0, 1, 0),
    (100, 0, -1, 0)
]
# Converge around t=50 but don't overlap
# Should still find minimum area
```

### 5. Visualization Tests

#### Test 5.1: Single Point
**Objective**: Verify visualization of single point.

**Test Cases**:
```python
positions = [(0, 0)]
visual = visualize_points(positions)
Expected: "#"
```

#### Test 5.2: Horizontal Line
**Objective**: Verify simple pattern.

**Test Cases**:
```python
positions = [(0, 0), (1, 0), (2, 0)]
visual = visualize_points(positions)
Expected: "###"
```

#### Test 5.3: Vertical Line
**Objective**: Verify multi-line output.

**Test Cases**:
```python
positions = [(0, 0), (0, 1), (0, 2)]
visual = visualize_points(positions)
Expected:
"#\n#\n#"
```

#### Test 5.4: Letter Pattern
**Objective**: Verify readable letter formation.

**Test Cases**:
Create positions that form a simple letter (e.g., "L"):
```python
positions = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4)]
# Should form:
# #
# #
# #
# #
# ###
```

#### Test 5.5: Negative Coordinate Normalization
**Objective**: Verify coordinate normalization handles negative coordinates.

**Test Cases**:
```python
# Test with negative coordinates
positions = [(-5, -3), (-4, -3), (-3, -3)]
visual = visualize_points(positions)
# After normalization, should start at (0, 0)
Expected: "###"
```

### 6. End-to-End Tests

#### Test 6.1: Small Example (if available)
**Objective**: Verify against any provided examples.

**Details**:
- Test against example data if available from problem statement
- Verify both alignment time and visual output
- Note: The problem description mentions an example but doesn't provide the actual test data
- Skip this test if example data is not available

#### Test 6.2: Actual Input
**Objective**: Verify solution on actual input.

**Test Strategy**:
1. Run solution on input.md
2. Verify alignment time is reasonable (estimated 10000-15000)
3. Verify visualization produces readable output
4. Verify output dimensions are reasonable (likely 60-80 chars wide, 8-10 lines tall for capital letters)

**Validation Checks**:
```python
# Verify alignment time is reasonable
assert 0 <= alignment_time < 100000, f"Alignment time {alignment_time} out of range"

# Verify visualization contains expected characters
lines = visualization.split('\n')
all_chars = set(''.join(lines))
assert all_chars <= {'#', ' '}, f"Unexpected characters: {all_chars - {'#', ' '}}"

# Verify visualization has multiple lines (capital letters are ~8 lines tall)
assert len(lines) >= 6, f"Expected at least 6 lines, got {len(lines)}"

# Verify all lines have consistent length
line_lengths = set(len(line) for line in lines)
assert len(line_lengths) == 1, f"Inconsistent line lengths: {line_lengths}"

# Verify contains '#' characters
assert '#' in visualization, "Visualization should contain '#' characters"

# Verify reasonable aspect ratio (message width > height for text)
height = len(lines)
width = len(lines[0]) if lines else 0
assert width > height, f"Expected width ({width}) > height ({height}) for text"
```

#### Test 6.3: Manual Verification
**Objective**: Human verification of message.

**Process**:
1. Print visualization to console
2. Manually read the letters
3. Verify message makes sense (usually a short phrase or word)
4. This is the final answer to submit

### 7. Performance Tests

#### Test 7.1: Execution Time
**Objective**: Verify solution runs in reasonable time.

**Test Method**:
```python
import time

start = time.time()
main()
elapsed = time.time() - start

assert elapsed < 5.0, f"Took {elapsed:.2f}s, expected < 5s"
print(f"Performance: Solution completed in {elapsed:.2f}s")
```

**Acceptance Criteria**:
- Full solution completes in < 5 seconds
- With ~356 points and ~10000-15000 iterations, this should be easily achievable

#### Test 7.2: Memory Usage
**Objective**: Verify no excessive memory consumption.

**Acceptance Criteria**:
- Memory footprint remains small (< 100 MB)
- No memory leaks during iteration

### 8. Edge Case Tests

#### Test 8.1: All Stationary Points
**Objective**: Verify handling of zero velocities.

**Test Cases**:
```python
points = [(0, 0, 0, 0), (1, 0, 0, 0), (2, 0, 0, 0)]
# Area never changes - will hit MAX_ITERATIONS limit
# This edge case is unlikely in actual AoC input
# Skip this test as it represents unrealistic input
```

**Note**: This edge case would cause the algorithm to hit the MAX_ITERATIONS limit. However, this scenario is unrealistic for the actual problem and can be skipped.

#### Test 8.2: Diverging Points
**Objective**: Verify handling of points that only diverge.

**Test Cases**:
```python
points = [(0, 0, 1, 1), (0, 0, -1, -1)]
# Start together, diverge immediately
# At t=0: area = 0
# At t=1: area > 0
# Algorithm should detect increase and return max(0, 1-1) = 0

alignment_time = find_alignment_time(points)
Expected: 0
```

**Note**: The implementation needs special handling: when area increases at t=1, return max(0, t-1) = 0.

#### Test 8.3: Very Large Velocities
**Objective**: Verify correct calculation with large velocity values.

**Test Cases**:
- Points with velocities that cause rapid convergence
- Ensure no integer overflow or precision issues

#### Test 8.4: Grid Boundary Alignment
**Objective**: Verify visualization when message is at extreme coordinates.

**Test Cases**:
- Points that form message with very negative coordinates
- Points that form message with very positive coordinates
- Verify normalization to (0,0) origin works correctly

### 9. Correctness Verification Strategy

#### Step-by-Step Validation:
1. **Parse Verification**: Print first 5 parsed points, manually verify against input.md
2. **Position Verification**: Calculate position manually for 2-3 points at t=1, compare with code
3. **Bounding Box Verification**: Print bounding box area for t=0, t=100, t=1000 to observe decrease
4. **Alignment Time Verification**:
   - Print area for times around detected alignment
   - Verify it's a minimum: area[t-10] > area[t-1] > area[t] < area[t+1] < area[t+10]
   - Note: No local minima expected in this physics simulation
5. **Visualization Verification**:
   - Print visualization at t=0 (should be huge and scattered - may be too large to display)
   - Print visualization at alignment time (should be readable capital letters)
   - Print visualization at t=alignment+100 (should be scattered again)
6. **Message Format Verification**:
   - Verify message is approximately 8 lines tall (typical for AoC capital letters)
   - Verify message width is greater than height
   - Verify only contains '#' and space characters

#### Statistical Validation:
- Verify that bounding box area at alignment is << 1% of area at t=0
- Verify message has reasonable aspect ratio (width ≈ 6-10x height for text)
- Verify message contains reasonable density of points (not too sparse, not too dense)

## Testing Execution Order

1. Run unit tests for parsing (Tests 1.x)
2. Run unit tests for position calculation (Tests 2.x)
3. Run unit tests for bounding box (Tests 3.x)
4. Run integration tests for alignment (Tests 4.x)
5. Run visualization tests (Tests 5.x)
6. Run end-to-end test with actual input (Test 6.2)
7. Manually verify output message (Test 6.3)
8. Run performance check (Tests 7.x)

## Success Criteria

The solution is considered correct when:

1. All unit tests pass
2. Algorithm correctly identifies alignment time
3. Visualization produces readable capital letters
4. Message can be manually read from output
5. Solution runs in under 5 seconds
6. No errors or exceptions during execution

## Debugging Strategy

If tests fail:

1. **Parsing issues**: Print raw input lines and parsed tuples side-by-side
2. **Position calculation issues**: Print step-by-step calculation for single point
3. **Alignment detection issues**: Plot area over time to visualize convergence
4. **Visualization issues**: Print coordinate set and grid dimensions separately

## Notes

- This is a puzzle solution, not production code - focus on correctness over robustness
- Manual verification of final message is acceptable and expected
- The actual message content is unknown until we solve it
- Automated OCR for ASCII art is unnecessary complexity for this problem
- This is Advent of Code 2018 Day 10 Part 1
- Messages in AoC are typically 8 lines tall with capital letters
- Use spaces (not dots) for empty positions in visualization
- Test data expectations verified against actual input.md file
