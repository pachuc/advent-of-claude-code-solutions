# Test Plan - Part 2: Maximum Distance During Journey

## Testing Strategy
Verify that the solution correctly tracks the maximum distance reached at any point during the hexagonal grid navigation, not just at the final position.

## Test Categories

### 1. Basic Functionality Tests

#### Test 1.1: Simple Linear Path
**Input**: `ne,ne,ne`
**Expected Output**: `3`
**Rationale**: Moving in one direction continuously, max distance is at the end
**Verification**:
- After move 1: distance = 1
- After move 2: distance = 2
- After move 3: distance = 3
- Max = 3

#### Test 1.2: Path Returning to Origin
**Input**: `ne,ne,sw,sw`
**Expected Output**: `2`
**Rationale**: Returns to origin but max distance was 2 after the first two moves
**Verification**:
- After ne: (1,0,-1), distance = 1
- After ne: (2,0,-2), distance = 2
- After sw: (1,0,-1), distance = 1
- After sw: (0,0,0), distance = 0
- Max = 2 (critical test - final position is origin!)

#### Test 1.3: Oscillating Path
**Input**: `n,s,n,s,n`
**Expected Output**: `1`
**Rationale**: Moves back and forth, max distance is always 1
**Verification**:
- After n: distance = 1
- After s: distance = 0
- After n: distance = 1
- After s: distance = 0
- After n: distance = 1
- Max = 1

### 2. Edge Cases

#### Test 2.1: Empty Input
**Input**: `` (empty string)
**Expected Output**: `0`
**Rationale**: No moves means we stay at origin
**Verification**: max_distance should remain 0

#### Test 2.2: Single Move
**Input**: `n`
**Expected Output**: `1`
**Rationale**: One step from origin in any direction
**Verification**: All six directions should give distance 1

**Extended Test - All Six Directions**:
Each individual direction should produce max distance of 1:
- `n` → 1
- `ne` → 1
- `se` → 1
- `s` → 1
- `sw` → 1
- `nw` → 1

#### Test 2.3: Immediate Return to Origin
**Input**: `n,s`
**Expected Output**: `1`
**Rationale**: Max was 1 after first move, even though we return to origin
**Verification**: Critical difference from Part 1 (which would give 0)

### 3. Complex Paths

#### Test 3.1: Spiral Pattern
**Input**: `ne,se,s,sw,nw,n,ne,se`
**Expected Output**: `2`
**Rationale**: Tests non-linear path with varying distances
**Verification**: Calculate distance after each move, confirm max is correct
**Trace**:
- Start: (0,0,0), distance = 0, max = 0
- After ne: (1,0,-1), distance = 1, max = 1
- After se: (2,-1,-1), distance = 2, max = 2
- After s: (2,-2,0), distance = 2, max = 2
- After sw: (1,-2,1), distance = 2, max = 2
- After nw: (0,-1,1), distance = 1, max = 2
- After n: (0,0,0), distance = 0, max = 2
- After ne: (1,0,-1), distance = 1, max = 2
- After se: (2,-1,-1), distance = 2, max = 2
- **Maximum distance reached: 2**

#### Test 3.2: Path with Multiple Peaks
**Input**: `ne,ne,ne,sw,sw,sw,ne,ne,ne,ne,sw,sw,sw,sw`
**Expected**: Should find the highest peak among multiple local maxima
**Rationale**: Tests that we don't just find first peak
**Verification**:
- First peak at 3 steps NE: distance = 3
- Return to origin after 6 moves
- Second peak at 4 steps NE: distance = 4
- Max should be 4

#### Test 3.3: Example from Part 1
**Input**: `ne,ne,s,s`
**Expected**: `2`
**Rationale**: Part 1 answer was 2 (final position), but need to verify max during journey is also 2
**Verification**:
- Start: (0,0,0), distance = 0
- After ne: (1,0,-1), distance = 1
- After ne: (2,0,-2), distance = 2
- After s: (2,-1,-1), distance = (2+1+1)/2 = 2
- After s: (2,-2,0), distance = (2+2+0)/2 = 2
- Max = 2

### 4. Validation Tests

#### Test 4.1: Invalid Direction
**Input**: `ne,invalid,se`
**Expected**: ValueError with informative message
**Rationale**: Input validation should catch bad moves
**Verification**: Error should occur and be clear

#### Test 4.2: Whitespace Handling
**Input**: `ne, ne , sw` (spaces around commas)
**Expected**: Should parse correctly and give proper result
**Rationale**: Input parser should handle whitespace
**Verification**: Should work same as `ne,ne,sw`

#### Test 4.3: Cube Coordinate Invariant
**Input**: Any valid sequence of moves
**Expected**: The invariant x + y + z = 0 must be maintained after every move
**Rationale**: Verifies the mathematical correctness of the cube coordinate system
**Verification**: Add assertion in debug mode to check `x + y + z == 0` after each position update
**Test Cases**:
- `ne,ne,sw,sw` → Check invariant after each move
- `n,s,e,w,ne,sw` → Various directions should all maintain invariant
- Can be combined with any other test by adding invariant checks

### 5. Performance Tests

#### Test 5.1: Actual Input File
**Input**: Read from `input.md` (the actual puzzle input with ~19,000+ moves)
**Expected**: Should complete in reasonable time (< 1 second)
**Rationale**: Verify O(n) algorithm handles real input efficiently
**Verification**:
- Check that result is computed quickly
- Result should be ≥ 687 (the Part 1 answer, since max ≥ final)
- Likely result will be significantly higher than 687

#### Test 5.2: Long Uniform Path
**Input**: `"n," * 10000` (10,000 moves north)
**Expected Output**: `10000`
**Rationale**: Stress test with many moves in one direction
**Verification**: Should handle large input without performance issues

### 6. Correctness Verification Strategy

#### Manual Verification Method
For small test cases:
1. Create a table with columns: Step#, Move, Position(x,y,z), Distance, Running Max
2. Trace through each move manually
3. Verify final max matches expected output

#### Automated Testing Approach
```python
def test_max_distance():
    test_cases = [
        ("ne,ne,ne", 3),
        ("ne,ne,sw,sw", 2),  # Critical: returns to origin
        ("n,s,n,s,n", 1),
        ("", 0),
        ("n", 1),
        ("n,s", 1),  # Critical: different from final distance
        ("se,sw,se,sw,sw", 3),  # From Part 1 examples
        ("ne,se,s,sw,nw,n,ne,se", 2),  # Spiral pattern
        ("ne,ne,s,s", 2),  # Part 1 example
    ]

    for input_str, expected in test_cases:
        result = solve_with_input(input_str)
        assert result == expected, f"Failed for {input_str}: got {result}, expected {expected}"

def test_all_six_directions():
    """Test that each individual direction produces distance 1"""
    for direction in ['n', 'ne', 'se', 's', 'sw', 'nw']:
        result = solve_with_input(direction)
        assert result == 1, f"Failed for direction {direction}: got {result}, expected 1"

def test_cube_coordinate_invariant():
    """Verify x + y + z = 0 is maintained throughout journey"""
    # This would require exposing position tracking or adding debug mode
    # Can be implemented by modifying find_max_distance to optionally check invariant
    pass
```

## Key Differences from Part 1 Testing

1. **Focus on Journey vs Destination**: Part 2 tests must verify intermediate distances, not just final
2. **Return-to-Origin Cases**: Critical to test paths that return to origin or backtrack
3. **Max Tracking**: Verify that maximum is preserved even as distance decreases later
4. **Expected Values**: Many test cases will have different expected outputs than Part 1

## Comparison Tests

### Test 7.1: Part 1 vs Part 2 on Same Input
**Approach**: Run both solutions on the actual puzzle input
**Expected**: Part 2 answer ≥ Part 1 answer (687)
**Rationale**: Maximum distance during journey can't be less than final distance
**Verification**: `max_distance >= final_distance` must always hold

### Test 7.2: Monotonic Paths
**Input**: Any path that only moves away from origin (e.g., `ne,ne,ne,n,n,n`)
**Expected**: Part 1 and Part 2 should give same answer
**Rationale**: If we never backtrack, max distance = final distance
**Verification**: For monotonic paths, both answers should match

## Test Execution Order
1. Run edge cases first (empty, single move)
2. Run basic functionality tests
3. Run validation tests to ensure error handling
4. Run complex path tests
5. Run performance test on actual input
6. Run comparison tests against Part 1

## Success Criteria
- All unit tests pass
- Performance test completes in < 1 second
- Part 2 answer ≥ Part 1 answer (687) for puzzle input
- Manual trace verification matches automated results for sample inputs
- Solution correctly identifies maximum distance even when path returns toward origin

## Debugging Strategy
If tests fail:
1. Print position and distance after each move for failing test
2. Verify cube coordinate invariant (x + y + z = 0) is maintained
3. Check that distance formula is applied correctly
4. Verify max comparison logic (using max() function or manual comparison)
5. Trace through example manually to find discrepancy
