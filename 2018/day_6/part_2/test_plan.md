# Test Plan: Safe Region Based on Total Manhattan Distance

## Testing Strategy

The testing approach focuses on verifying correctness through:
1. **Example validation** - Using the provided example from the problem
2. **Edge case testing** - Handling boundary conditions
3. **Algorithmic verification** - Ensuring distance calculations are correct
4. **Search space validation** - Confirming we're searching an adequate area
5. **Manual spot checks** - Verifying specific locations

## Test 1: Example from Problem Statement (HIGH PRIORITY)

### Purpose
Validate that the algorithm works correctly on the known example.

### Test Data
Create file `test_example.txt`:
```
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
```

### Expected Behavior
- Threshold: 32 (not 10000)
- Expected region size: **16**
- This is explicitly stated in the problem

### Test Procedure
1. Create test file `test_example.txt` with the 6 coordinates above
2. Run: `python solution.py test_example.txt 32`
3. Verify output is exactly `16`

### Manual Verification
From the problem, location (4, 3):
- Distance to (1,1): |4-1| + |3-1| = 3 + 2 = 5
- Distance to (1,6): |4-1| + |3-6| = 3 + 3 = 6
- Distance to (8,3): |4-8| + |3-3| = 4 + 0 = 4
- Distance to (3,4): |4-3| + |3-4| = 1 + 1 = 2
- Distance to (5,5): |4-5| + |3-5| = 1 + 2 = 3
- Distance to (8,9): |4-8| + |3-9| = 4 + 6 = 10
- **Total: 30 < 32** ✓ (should be in region)

### Success Criteria
- Output equals 16
- Manual check of (4,3) confirms it's included
- Manual check of edge locations confirms they're excluded

## Test 2: Single Coordinate Edge Case (MEDIUM PRIORITY)

### Purpose
Verify behavior with minimal input and ensure special case handling works.

### Test Data
Create file `test_single.txt`:
```
5, 5
```

### Expected Behavior
- For a single coordinate at (5,5), a location (x,y) is safe if |x-5| + |y-5| < threshold
- This creates a diamond shape centered at (5,5)
- **Use smaller threshold for practical testing**

### Test Procedure (threshold=50)
1. Create test file with single coordinate at (5,5)
2. Run: `python solution.py test_single.txt 50`
3. Verify result matches expected count

### Manual Calculation (threshold=50)
- Region is all points where |x-5| + |y-5| < 50
- This is a diamond with "radius" 49
- Formula: sum from d=0 to 49 of (number of points at exactly distance d)
- For distance d: there are 4*d points (except d=0 which has 1 point)
- Total = 1 + sum(4*d for d in 1 to 49) = 1 + 4*(1+2+...+49) = 1 + 4*1225 = **4901**

### Alternative Test (threshold=10)
- Run: `python solution.py test_single.txt 10`
- Diamond with radius 9
- Expected: 1 + 4*(1+2+...+9) = 1 + 4*45 = **181**

### Success Criteria
- Program doesn't crash
- Result matches expected count (4901 for threshold=50, or 181 for threshold=10)
- Validates special case handling for single coordinate

## Test 3: Two Coordinates Symmetry

### Purpose
Test with simple symmetric case for easy verification.

### Test Data
```
0, 0
10, 0
```

### Expected Behavior (threshold=25)
- Centroid at (5, 0)
- Location (5, 0): distance to (0,0) = 5, to (10,0) = 5, total = 10 < 25 ✓
- Location (0, 0): distance to (0,0) = 0, to (10,0) = 10, total = 10 < 25 ✓
- Location (5, 10): distance to (0,0) = 15, to (10,0) = 15, total = 30 ≥ 25 ✗
- Location (5, 7): distance to (0,0) = 12, to (10,0) = 12, total = 24 < 25 ✓

### Test Procedure
1. Create test file
2. Run with threshold=25
3. Manually verify several specific locations
4. Check symmetry (region should be symmetric around centroid)

### Success Criteria
- Specific locations verified manually
- Result is reasonable for given threshold

## Test 4: Search Space Adequacy Validation (HIGH PRIORITY)

### Purpose
Ensure the search space is large enough to capture the entire safe region without missing boundary locations.

### Test Approach
The implementation includes `validate_search_space()` function that checks boundary points. This test verifies the validation works correctly.

### Expected Behavior
- The solution should automatically detect if search space is inadequate
- If validation detects boundary points in the safe region, it should expand the buffer
- Final result should have NO boundary points in the safe region

### Test Procedure
1. Run on actual input: `python solution.py input.md`
2. Optionally add debug output to show if buffer was expanded
3. Verify solution completes successfully

### Manual Verification
After getting the answer, manually check a few boundary points:
```python
# If search space was (-346, 757) to (-307, 747)
# Check corner points like (-346, -307), (-346, 747), (757, -307), (757, 747)
# Calculate total distance for each
# Verify all are >= 10000 (not in safe region)
```

### Success Criteria
- Solution produces a result without errors
- If verbose output is added, verify buffer expansion logic works if triggered
- Boundary points confirmed to be outside safe region (total distance >= threshold)

## Test 5: Actual Input Validation (HIGH PRIORITY)

### Purpose
Solve the actual puzzle and validate the result through spot checks.

### Test Data
Use `input.md` with 50 coordinates

### Test Procedure
1. First verify with example: `python solution.py test_example.txt 32` → expect 16
2. Run actual solution: `python solution.py input.md` (uses default threshold 10000)
3. Verify output is a positive integer
4. Perform manual spot checks to validate correctness

### Expected Result Characteristics
Given:
- 50 coordinates
- Threshold 10000
- Coordinate range: (54, 40) to (357, 347)
- Expected region size: TBD, but likely in the range of 30,000-50,000 locations

### Manual Spot Checks
Perform these verifications to confirm algorithm correctness:

#### Check 1: Center Location (should be IN safe region)
Pick location near center of coordinates, e.g., (200, 180):
- Calculate total distance to all 50 coordinates
- Should be well below 10000 (likely around 8,000-9,000)
- This validates that the center is correctly included

#### Check 2: Far Location (should be OUT of safe region)
Pick location far from all coordinates, e.g., (0, 0):
- Calculate total distance to all 50 coordinates
- Should be well above 10000 (likely 20,000+)
- This validates that distant points are correctly excluded

#### Check 3: Edge Cases
- Verify the solution handles all 50 coordinates correctly
- Check that no parsing errors occurred

### Validation Script
Create a small validation script to verify specific locations:
```python
coordinates = [(181, 47), (337, 53), ...]  # all 50 from input.md
location = (200, 180)
total_dist = sum(abs(x - location[0]) + abs(y - location[1])
                 for x, y in coordinates)
print(f"Total distance from {location}: {total_dist}")
# Should be < 10000 if location is in safe region
```

### Success Criteria
- Example test passes (output = 16)
- Actual input produces a positive integer
- Center location spot check shows total distance < 10000
- Far location spot check shows total distance >= 10000
- Result is in reasonable range for the given parameters

## Test 6: Distance Calculation Correctness (OPTIONAL)

### Purpose
Verify Manhattan distance calculation is correct. (Note: This function is reused from Part 1 where it was already tested and used successfully.)

### Test Cases
If desired, add these assertions to verify:
```python
assert manhattan_distance(0, 0, 0, 0) == 0
assert manhattan_distance(0, 0, 3, 4) == 7
assert manhattan_distance(5, 5, 5, 5) == 0
assert manhattan_distance(1, 1, 4, 5) == 7
assert manhattan_distance(10, 20, 5, 10) == 15
# Negative coordinates
assert manhattan_distance(-5, -5, 5, 5) == 20
```

### Success Criteria
All assertions pass. (Low priority since function was proven correct in Part 1.)

## Test 7: Early Termination Optimization (LOW PRIORITY - OPTIONAL)

### Purpose
Verify that the early termination optimization doesn't affect correctness.

### Test Approach
The early termination optimization is straightforward (break when sum >= threshold), making bugs unlikely. This test is optional defensive programming.

### Simple Verification
Add a counter to track how often early termination occurs:
```python
early_termination_count = 0
for x in range(...):
    for y in range(...):
        total_distance = 0
        for cx, cy in coordinates:
            total_distance += manhattan_distance(x, y, cx, cy)
            if total_distance >= threshold:
                early_termination_count += 1
                break
        ...
# Print early_termination_count to verify optimization is working
```

### Success Criteria
- Solution produces correct results (verified by other tests)
- Early termination counter shows optimization is being triggered
- (Optional) Compare runtime with/without optimization to show performance gain

## Test 8: Threshold Parameter Testing (MEDIUM PRIORITY)

### Purpose
Verify solution works correctly with different thresholds and that region size increases monotonically.

### Test Cases
Using actual input.md:
1. `python solution.py input.md 100` → Very small region (possibly 0)
2. `python solution.py input.md 1000` → Small region
3. `python solution.py input.md 5000` → Medium region
4. `python solution.py input.md 10000` → Normal case (puzzle answer)
5. `python solution.py input.md 20000` → Large region

### Expected Behavior
- As threshold increases, region size should monotonically increase
- Smaller thresholds may result in zero or very small regions
- Each result should be <= the next (monotonic increase)

### Test Procedure
1. Run solution with each threshold value
2. Record results in order
3. Verify: result[i] <= result[i+1] for all i

### Combined with Search Space Validation
Note: For larger thresholds, the search space validation should automatically expand the buffer to ensure adequate coverage.

### Success Criteria
- All runs complete without errors
- Region size increases monotonically with threshold
- No unexpected jumps or decreases
- Search space validation works for all thresholds tested

## Test 9: Input Parsing Robustness (LOW PRIORITY - OPTIONAL)

### Purpose
Ensure coordinate parsing handles various input formats correctly. (Note: Parser is reused from Part 1 where it was already tested.)

### Test Cases (Optional)
1. Empty file → should return 0
2. File with blank lines → should skip them
3. File with extra whitespace → should parse correctly

### Success Criteria
- Program doesn't crash on malformed input (reused parser already handles this)

## Test 10: Performance Validation (MEDIUM PRIORITY)

### Purpose
Ensure solution runs in reasonable time.

### Test Procedure
1. Time the execution on actual input: `time python solution.py input.md`
2. Verify it completes in acceptable time (< 30 seconds)

### Expected Performance
Based on implementation plan estimates:
- Search space: ~1103 × 1107 = ~1,220,000 locations
- Calculations per location: up to 50 distance calculations (often fewer due to early termination)
- Total operations: ~61 million in worst case
- Expected time: 2-10 seconds on modern hardware (Python is slower than compiled languages)

### Success Criteria
- Solution completes in reasonable time (< 30 seconds acceptable for one-off script)
- If runtime is concerning, it validates correctness over speed for this use case

## Summary of Expected Results

| Test | Input | Threshold | Expected Output | Priority |
|------|-------|-----------|----------------|----------|
| Example | 6 coords | 32 | **16** | HIGH |
| Single coord | (5,5) | 10 | **181** | MEDIUM |
| Single coord | (5,5) | 50 | **4901** | MEDIUM |
| Two coords | (0,0), (10,0) | 25 | Manual verify | MEDIUM |
| Actual input | 50 coords | 10000 | TBD | HIGH |
| Search space | 50 coords | 10000 | Auto-validation | HIGH |
| Threshold variations | 50 coords | 100-20000 | Monotonic increase | MEDIUM |
| Performance | 50 coords | 10000 | < 30 seconds | MEDIUM |

## Test Execution Order (Priority-Based)

### Phase 1: Critical Tests (Must Pass)
1. **Example validation** (Test 1) - Known correct answer (16)
2. **Actual input solution** (Test 5) - Get the puzzle answer
3. **Manual spot checks** (Test 5) - Verify center/far locations

### Phase 2: Validation Tests (Should Pass)
4. **Search space validation** (Test 4) - Ensure adequacy
5. **Single coordinate edge case** (Test 2) - Test special case handling
6. **Threshold variations** (Test 8) - Verify monotonic behavior

### Phase 3: Optional Tests (Nice to Have)
7. **Two coordinates symmetry** (Test 3) - Additional validation
8. **Performance validation** (Test 10) - Ensure acceptable runtime
9. **Early termination** (Test 7) - Verify optimization
10. **Distance calculations** (Test 6) - Already proven in Part 1
11. **Input parsing** (Test 9) - Already proven in Part 1

## Acceptance Criteria

The solution is considered correct if:
1. ✓ Example test produces output of **16** (Test 1)
2. ✓ Single coordinate test produces expected counts (Test 2)
3. ✓ Search space validation passes (Test 4)
4. ✓ Actual input produces a positive integer (Test 5)
5. ✓ Manual spot checks confirm algorithm correctness (Test 5):
   - Center location (e.g., 200, 180) has total distance < 10000
   - Far location (e.g., 0, 0) has total distance >= 10000
6. ✓ Threshold variations show monotonic increase (Test 8)
7. ✓ Solution runs in reasonable time (< 30 seconds) (Test 10)

## Key Improvements from Critique

1. **Threshold parameterization**: CLI accepts threshold as second argument
2. **Search space validation**: Automatic validation with buffer expansion
3. **Realistic test expectations**: Fixed Test 2 to use smaller thresholds
4. **Priority-based testing**: Focus on high-priority tests first
5. **Better integration**: Implementation and test plans align on parameters
6. **Special case handling**: Explicit handling for single coordinate edge case
