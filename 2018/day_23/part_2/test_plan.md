# Test Plan: Part 2 - Optimal Teleportation Position

## Testing Strategy Overview

We need to verify:
1. **Correctness**: Algorithm finds position with maximum nanobot coverage
2. **Tiebreaking**: When multiple positions have same coverage, closest to origin is chosen
3. **Edge Cases**: Handle unusual inputs correctly
4. **Performance**: Solution completes in reasonable time for actual input

## Test Cases

### Test 1: Example from Problem Statement
**Purpose**: Verify basic correctness with known answer

**Input**:
```
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
```

**Expected Output**: 36

**Verification**:
- Position (12,12,12) should be in range of 5 nanobots
- Distance from origin: |12| + |12| + |12| = 36
- Check that no other position has more than 5 nanobots in range
- If tied at 5, verify (12,12,12) is closest to origin

**Test Method**:
```python
def test_example():
    test_input = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""

    # Write to temporary file
    with open('test_input.txt', 'w') as f:
        f.write(test_input)

    nanobots = parse_input('test_input.txt')
    position, count, distance = find_optimal_position(nanobots)

    assert count == 5, f"Expected 5 nanobots in range, got {count}"
    assert distance == 36, f"Expected distance 36, got {distance}"
    assert position == (12, 12, 12), f"Expected position (12,12,12), got {position}"

    print("✓ Example test passed")
```

### Test 2: Origin is Optimal
**Purpose**: Verify algorithm works when origin (0,0,0) is the answer

**Input**:
```
pos=<0,0,0>, r=5
pos=<1,0,0>, r=5
pos=<0,1,0>, r=5
pos=<0,0,1>, r=5
```

**Expected**:
- Position (0,0,0) in range of all 4 nanobots
- Distance = 0

**Verification**:
- Ensure distance_to_origin = 0
- Ensure all nanobots counted

### Test 3: Tiebreaker - Closest to Origin
**Purpose**: Verify tiebreaking logic when multiple positions have same coverage

**Input**:
```
pos=<5,0,0>, r=10
pos=<-5,0,0>, r=10
```

**Analysis**:
- Many positions are in range of both bots
- The optimal position should be (0,0,0) with distance 0
- Both nanobots can reach origin: distance 5 ≤ 10

**Expected Output**: 0

**Verification**:
```python
def test_tiebreaker():
    # Set up nanobots
    nanobots = [(5, 0, 0, 10), (-5, 0, 0, 10)]

    position, count, distance = find_optimal_position(nanobots)

    assert count == 2, f"Expected 2 bots in range, got {count}"
    assert distance == 0, f"Expected distance 0, got {distance}"

    print("✓ Tiebreaker test passed")
```

### Test 4: Single Nanobot
**Purpose**: Edge case with only one nanobot

**Input**:
```
pos=<10,20,30>, r=15
```

**Analysis**:
- Nanobot at (10,20,30) with radius 15
- Manhattan distance from origin to nanobot: 10 + 20 + 30 = 60
- Optimal position should be closest point to origin within range
- The closest point would be at distance 60-15 = 45 from origin

**Expected**:
- Count = 1 (only the single nanobot in range)
- Distance should be approximately 45 (may vary slightly due to integer coordinates)

**Verification**:
```python
def test_single_nanobot():
    nanobots = [(10, 20, 30, 15)]
    position, count, distance = find_optimal_position(nanobots)

    assert count == 1, f"Expected 1 bot in range, got {count}"
    # Distance should be close to 45 (60 - 15), allowing for integer coordinate effects
    assert 40 <= distance <= 50, f"Expected distance near 45, got {distance}"
    # Verify position is actually in range
    assert manhattan_distance(position, (10, 20, 30)) <= 15

    print("✓ Single nanobot test passed")
```

### Test 5: No Overlap - Disjoint Ranges
**Purpose**: Nanobots with no overlapping coverage

**Input**:
```
pos=<0,0,0>, r=1
pos=<100,100,100>, r=1
pos=<200,200,200>, r=1
```

**Expected**:
- Maximum coverage is 1 nanobot
- Optimal position is (0,0,0) - closest to origin among options

**Verification**:
```python
def test_no_overlap():
    nanobots = [(0,0,0,1), (100,100,100,1), (200,200,200,1)]
    position, count, distance = find_optimal_position(nanobots)

    assert count == 1, f"Expected 1 bot in range, got {count}"
    assert distance == 0, f"Expected distance 0 at origin, got {distance}"

    print("✓ No overlap test passed")
```

### Test 6: All Same Position
**Purpose**: All nanobots at same location

**Input**:
```
pos=<5,5,5>, r=10
pos=<5,5,5>, r=20
pos=<5,5,5>, r=15
```

**Analysis**:
- All three nanobots are at (5,5,5) with radii 10, 20, and 15
- Any position within Manhattan distance 10 (smallest radius) is in range of all 3
- Position (5,5,5) has count=3, distance=15 from origin
- But position (0,0,5) has distance 10 from (5,5,5) and distance 5 from origin
  - In range of all 3 nanobots (distance 10 ≤ 10), count=3
  - Closer to origin (distance 5 < 15)
- Optimal: one of (0,0,5), (0,5,0), or (5,0,0)

**Expected**:
- Count = 3 (all nanobots in range)
- Distance = 5 (closest to origin while maintaining max coverage)

**Verification**:
```python
def test_same_position():
    nanobots = [(5,5,5,10), (5,5,5,20), (5,5,5,15)]
    position, count, distance = find_optimal_position(nanobots)

    assert count == 3, f"Expected 3 bots in range, got {count}"
    assert distance == 5, f"Expected distance 5, got {distance}"
    # Position should be one of the three closest points
    assert position in [(0,0,5), (0,5,0), (5,0,0)], f"Unexpected position {position}"

    print("✓ Same position test passed")
```

### Test 7: Negative Coordinates
**Purpose**: Verify algorithm handles negative coordinates correctly

**Input**:
```
pos=<-10,-10,-10>, r=15
pos=<10,10,10>, r=15
```

**Analysis**:
- First nanobot at (-10,-10,-10) with radius 15
- Second nanobot at (10,10,10) with radius 15
- Origin (0,0,0) is at distance 30 from each nanobot
- Origin is in range of first bot: 30 > 15, NO
- Origin is not in range of either bot
- Closest point to origin in range of first bot: approximately (-10,-10,-10) direction
- Closest point to origin in range of second bot: approximately (10,10,10) direction

**Expected**:
- Count = 1 (can only be in range of one bot at a time)
- Distance should be minimized, likely around 15 from origin

**Verification**:
```python
def test_negative_coordinates():
    nanobots = [(-10,-10,-10,15), (10,10,10,15)]
    position, count, distance = find_optimal_position(nanobots)

    assert count == 1, f"Expected 1 bot in range, got {count}"
    # Should pick the position closest to origin that's in range of one bot
    assert distance <= 20, f"Expected distance <= 20, got {distance}"

    print("✓ Negative coordinates test passed")
```

### Test 8: Large Coordinate Values
**Purpose**: Ensure algorithm handles large numbers efficiently

**Input**: Use subset of actual input with large coordinates (millions)

**Verification**:
- Algorithm completes in reasonable time (< 60 seconds)
- Doesn't overflow or crash
- Returns valid answer

### Test 9: Very Large Radius
**Purpose**: Test when a nanobot can reach origin from far away

**Input**:
```
pos=<100,100,100>, r=1000
```

**Expected**:
- Origin (0,0,0) is at distance 300 from nanobot
- Origin is in range (300 <= 1000)
- Count = 1, Distance = 0

**Verification**:
```python
def test_large_radius():
    nanobots = [(100,100,100,1000)]
    position, count, distance = find_optimal_position(nanobots)

    assert count == 1, f"Expected 1 bot in range, got {count}"
    assert distance == 0, f"Expected distance 0 at origin, got {distance}"

    print("✓ Large radius test passed")
```

### Test 10: Actual Puzzle Input
**Purpose**: Final verification with real input

**Input**: The 1000-nanobot input from `input.md`

**Verification**:
- Algorithm completes successfully
- Returns a single integer distance
- Manual spot-check: verify the returned position is actually in range of claimed number of nanobots

**Spot Check Code**:
```python
def verify_solution(position, nanobots):
    """
    Manual verification that the solution is correct.
    """
    count = count_bots_in_range(position, nanobots)
    distance = manhattan_distance(position, (0, 0, 0))

    print(f"Position: {position}")
    print(f"Nanobots in range: {count}")
    print(f"Distance from origin: {distance}")

    # Verify no nearby position is better
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                neighbor = (position[0]+dx, position[1]+dy, position[2]+dz)
                neighbor_count = count_bots_in_range(neighbor, nanobots)
                neighbor_dist = manhattan_distance(neighbor, (0, 0, 0))

                if neighbor_count > count:
                    print(f"WARNING: Neighbor {neighbor} has more coverage: {neighbor_count}")
                elif neighbor_count == count and neighbor_dist < distance:
                    print(f"WARNING: Neighbor {neighbor} has same coverage but closer: {neighbor_dist}")

    return count, distance
```

## Helper Function Tests

### Test: manhattan_distance
```python
def test_manhattan_distance():
    assert manhattan_distance((0,0,0), (0,0,0)) == 0
    assert manhattan_distance((0,0,0), (1,2,3)) == 6
    assert manhattan_distance((1,2,3), (4,5,6)) == 9
    assert manhattan_distance((-1,-2,-3), (1,2,3)) == 12
    print("✓ Manhattan distance tests passed")
```

### Test: max_bots_for_box
```python
def test_max_bots_for_box():
    """Verify upper bound estimation is correct."""
    nanobots = [(0,0,0,5), (10,10,10,5)]

    # Box containing origin - should detect first nanobot
    box1 = ((-5,5), (-5,5), (-5,5))
    assert max_bots_for_box(box1, nanobots) >= 1

    # Box far away - should detect neither
    box2 = ((100,110), (100,110), (100,110))
    assert max_bots_for_box(box2, nanobots) == 0

    print("✓ Box estimation tests passed")
```

### Test: subdivide_box
```python
def test_subdivide_box():
    """Verify box subdivision creates correct octants."""
    box = ((0, 10), (0, 10), (0, 10))
    octants = subdivide_box(box)

    # Should create 8 octants
    assert len(octants) == 8

    # Each octant should be smaller
    for octant in octants:
        assert get_box_size(octant) < get_box_size(box)

    print("✓ Box subdivision tests passed")
```

## Performance Benchmarks

### Benchmark 1: Algorithm Complexity
**Goal**: Verify O(n log range) behavior

**Method**:
- Time execution with different input sizes
- Plot runtime vs input size
- Ensure reasonable scaling

### Benchmark 2: Real Input Timeout
**Goal**: Solution completes in < 60 seconds

**Method**:
```python
import time

def benchmark_real_input():
    start = time.time()
    nanobots = parse_input('input.md')
    position, count, distance = find_optimal_position(nanobots)
    end = time.time()

    elapsed = end - start
    print(f"Execution time: {elapsed:.2f} seconds")

    assert elapsed < 60, f"Too slow: {elapsed} seconds"
    print("✓ Performance benchmark passed")
```

## Integration Testing

### Full Pipeline Test
```python
def test_full_pipeline():
    """Test complete workflow from input to output."""

    # 1. Parse input
    nanobots = parse_input('input.md')
    assert len(nanobots) == 1000, "Should have 1000 nanobots"

    # 2. Find optimal position
    position, count, distance = find_optimal_position(nanobots)

    # 3. Verify solution
    assert isinstance(distance, int), "Distance should be integer"
    assert distance >= 0, "Distance should be non-negative"
    assert count > 0, "Should have at least one nanobot in range"

    # 4. Spot check
    verify_solution(position, nanobots)

    print(f"✓ Full pipeline test passed")
    print(f"Final answer: {distance}")
```

## Test Execution Order

1. **Unit tests first**: Test individual helper functions (manhattan_distance, max_bots_for_box, subdivide_box)
2. **Example test**: Verify with known answer from problem statement (Test 1)
3. **Edge case tests**: Cover corner cases (Tests 2-9)
4. **Performance test**: Ensure reasonable runtime (Benchmark tests)
5. **Full integration test**: End-to-end with actual input (Test 10)

## Success Criteria

- ✓ All unit tests pass
- ✓ Example test returns 36
- ✓ Edge cases handled correctly
- ✓ Real input completes in < 60 seconds
- ✓ Spot check confirms solution is locally optimal
- ✓ Answer is a positive integer representing Manhattan distance
