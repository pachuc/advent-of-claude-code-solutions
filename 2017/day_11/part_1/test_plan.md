# Testing Plan: Hexagonal Grid Navigation Distance

## Testing Strategy

We need to verify that our solution correctly calculates the minimum distance for various path configurations on a hexagonal grid. Testing will focus on correctness of the cube coordinate system, move processing, and distance calculation.

## Test Categories

### 1. Example Test Cases (from problem statement)

These are the provided examples that our solution MUST pass.

#### Test 1.1: Straight Line Movement
- **Input**: `ne,ne,ne`
- **Expected Output**: `3`
- **Rationale**: Three steps in the same direction = 3 steps away
- **Verification**: Final position should be (3, 0, -3), distance = (3+0+3)/2 = 3

#### Test 1.2: Opposite Cancellation
- **Input**: `ne,ne,sw,sw`
- **Expected Output**: `0`
- **Rationale**: Opposite directions cancel out, back at origin
- **Verification**: Final position should be (0, 0, 0), distance = 0

#### Test 1.3: Move Simplification
- **Input**: `ne,ne,s,s`
- **Expected Output**: `2`
- **Rationale**: Can be simplified to se,se (2 steps)
- **Verification**: Final position should be (2, -2, 0), distance = (2+2+0)/2 = 2

#### Test 1.4: Complex Path Simplification
- **Input**: `se,sw,se,sw,sw`
- **Expected Output**: `3`
- **Rationale**: Can be simplified to s,s,sw (3 steps)
- **Verification**: Final position should be (-1, -2, 3), distance = (1+2+3)/2 = 3

**Implementation**:
```python
def test_examples():
    """Test all provided examples."""
    test_cases = [
        ("ne,ne,ne", 3),
        ("ne,ne,sw,sw", 0),
        ("ne,ne,s,s", 2),
        ("se,sw,se,sw,sw", 3)
    ]

    for input_str, expected in test_cases:
        moves = input_str.split(',')
        x, y, z = calculate_final_position(moves)
        distance = calculate_distance(x, y, z)
        assert distance == expected, f"Failed for {input_str}: got {distance}, expected {expected}"

    print("All example tests passed!")
```

### 2. Edge Cases

#### Test 2.1: Empty Input
- **Input**: `` (empty string)
- **Expected Output**: `0`
- **Rationale**: No moves = stay at origin
- **Edge Case**: Tests handling of empty input - parsing should return empty list, not ['']
- **Note**: Important because `"".split(',')` returns `['']`, which must be handled

#### Test 2.2: Single Move
- **Input**: `n`
- **Expected Output**: `1`
- **Rationale**: One move = 1 step away
- **Edge Case**: Minimal non-empty input

#### Test 2.3: All Six Directions Once
- **Input**: `n,ne,se,s,sw,nw`
- **Expected Output**: `0`
- **Rationale**: All directions form a complete cycle, return to origin
- **Verification**: Final position (0, 0, 0)
- **Edge Case**: Tests that opposite directions properly cancel

#### Test 2.4: Large Number of Same Direction
- **Input**: `n,n,n,n,n,n,n,n,n,n` (10 times)
- **Expected Output**: `10`
- **Rationale**: 10 steps north = 10 steps away
- **Edge Case**: Repeated same direction

**Implementation**:
```python
def test_edge_cases():
    """Test edge cases."""
    test_cases = [
        ("", 0),  # Empty input
        ("n", 1),  # Single move
        ("n,ne,se,s,sw,nw", 0),  # All six directions (should return to origin)
        (",".join(["n"] * 10), 10)  # Many moves in same direction
    ]

    for input_str, expected in test_cases:
        # Use the actual parse_input function to match implementation
        if input_str:
            moves = [move.strip() for move in input_str.split(',') if move.strip()]
        else:
            moves = []

        x, y, z = calculate_final_position(moves)
        distance = calculate_distance(x, y, z)
        assert distance == expected, f"Failed for '{input_str}': got {distance}, expected {expected}"

    print("All edge case tests passed!")
```

### 3. Cube Coordinate System Verification

These tests verify the mathematical correctness of our cube coordinate implementation.

#### Test 3.1: Verify Invariant (x + y + z = 0)
- **Purpose**: Ensure all positions maintain the cube coordinate invariant
- **Method**: After processing any set of moves, verify x + y + z = 0
- **Test Cases**: Run on all test inputs

#### Test 3.2: Verify Direction Deltas
- **Purpose**: Ensure each direction delta maintains the invariant
- **Method**: For each direction, verify dx + dy + dz = 0

**Implementation**:
```python
def test_cube_coordinate_invariant():
    """Verify cube coordinate invariant is maintained."""
    # Test that all direction deltas sum to 0
    for direction, (dx, dy, dz) in DIRECTION_DELTAS.items():
        assert dx + dy + dz == 0, f"Direction {direction} breaks invariant"

    # Test that all positions maintain invariant
    # Note: Only use valid hexagonal directions (n, ne, se, s, sw, nw)
    # NOT 'e' and 'w' which don't exist in hexagonal grids
    test_inputs = [
        "ne,ne,ne",
        "ne,ne,sw,sw",
        "se,sw,se,sw,sw",
        "n,s,ne,sw,nw,se"  # Fixed: removed invalid 'e' and 'w'
    ]

    for input_str in test_inputs:
        moves = input_str.split(',')
        x, y, z = calculate_final_position(moves)
        assert x + y + z == 0, f"Position ({x},{y},{z}) breaks invariant for {input_str}"

    print("Cube coordinate invariant verified!")
```

### 4. Distance Calculation Verification

#### Test 4.1: Known Distance Points
- **Purpose**: Verify distance formula for known positions
- **Test Cases**:
  - (1, 0, -1): distance = 1 (one step NE)
  - (2, 0, -2): distance = 2 (two steps NE)
  - (1, 1, -2): distance = 2 (one NE + one N)
  - (3, -1, -2): distance = 3 (complex position)

#### Test 4.2: Symmetric Distances
- **Purpose**: Verify that opposite directions yield same distance
- **Method**: Compare distance for direction D vs opposite of D

**Implementation**:
```python
def test_distance_calculation():
    """Test distance calculation for known positions."""
    test_cases = [
        ((1, 0, -1), 1),    # One NE
        ((2, 0, -2), 2),    # Two NE
        ((1, 1, -2), 2),    # NE + N
        ((3, -1, -2), 3),   # Complex
        ((0, 0, 0), 0),     # Origin
        ((-5, 2, 3), 5)     # Negative coordinates
    ]

    for (x, y, z), expected in test_cases:
        distance = calculate_distance(x, y, z)
        assert distance == expected, f"Distance for ({x},{y},{z}): got {distance}, expected {expected}"

    print("Distance calculation tests passed!")
```

### 5. Opposite Direction Tests

#### Test 5.1: All Opposite Pairs
- **Purpose**: Verify each opposite pair cancels correctly
- **Test Cases**:
  - `n,s` → 0
  - `ne,sw` → 0
  - `se,nw` → 0

#### Test 5.2: Multiple Cancellations
- **Input**: `n,s,n,s,ne,sw,ne,sw`
- **Expected**: `0`

**Implementation**:
```python
def test_opposite_directions():
    """Test that opposite directions cancel out."""
    opposite_pairs = [
        ("n,s", 0),
        ("ne,sw", 0),
        ("se,nw", 0),
        ("n,s,n,s,ne,sw,ne,sw", 0)
    ]

    for input_str, expected in opposite_pairs:
        moves = input_str.split(',')
        x, y, z = calculate_final_position(moves)
        distance = calculate_distance(x, y, z)
        assert distance == expected, f"Failed for {input_str}: got {distance}, expected {expected}"

    print("Opposite direction tests passed!")
```

### 6. Path Equivalence Tests

Test that different paths to the same position yield the same distance.

#### Test 6.1: Different Paths, Same Destination
- **Path A**: `ne,ne` (2 steps northeast)
- **Path B**: `n,se,ne` (north, southeast, northeast)
- **Expected**: Both should end at position (2, 0, -2) with distance 2
- **Rationale**: Different paths, same final position and distance

**Implementation**:
```python
def test_path_equivalence():
    """Test that different paths to same position have same distance."""
    # Paths that should end at same position
    # Verified by manual calculation:
    # ne,ne: (0,0,0) -> (1,0,-1) -> (2,0,-2)
    # n,se,ne: (0,0,0) -> (0,1,-1) -> (1,0,-1) -> (2,0,-2)
    equivalent_paths = [
        (["ne", "ne"], ["n", "se", "ne"], (2, 0, -2)),
        (["s", "s"], ["se", "sw"], (0, -2, 2)),
        (["n", "n", "n"], ["ne", "nw", "n"], (0, 3, -3))
    ]

    for path1, path2, expected_pos in equivalent_paths:
        x1, y1, z1 = calculate_final_position(path1)
        x2, y2, z2 = calculate_final_position(path2)

        # Verify both paths reach expected position
        assert (x1, y1, z1) == expected_pos, f"Path 1 didn't reach expected position: got {(x1,y1,z1)}, expected {expected_pos}"
        assert (x2, y2, z2) == expected_pos, f"Path 2 didn't reach expected position: got {(x2,y2,z2)}, expected {expected_pos}"

        # Verify same final position
        assert (x1, y1, z1) == (x2, y2, z2), f"Paths don't lead to same position"

        # Verify same distance
        dist1 = calculate_distance(x1, y1, z1)
        dist2 = calculate_distance(x2, y2, z2)
        assert dist1 == dist2, f"Same position, different distances: {dist1} vs {dist2}"

    print("Path equivalence tests passed!")
```

### 7. Actual Input Validation

#### Test 7.1: Input File Processing
- **Purpose**: Verify the actual input file is processed correctly
- **Method**:
  - Check that input is parsed into correct number of moves
  - Verify no empty strings in move list
  - Verify all moves are valid directions (n, ne, se, s, sw, nw)
  - Verify whitespace handling (trailing newlines, spaces around commas)

#### Test 7.2: Solution Bounds Check
- **Purpose**: Sanity check on the solution
- **Method**:
  - Distance should be ≤ number of moves (can't be farther than total steps)
  - Distance should be ≥ 0
  - Distance should be an integer

**Implementation**:
```python
def test_actual_input():
    """Test the actual input file."""
    # Parse actual input
    moves = parse_input('input.md')

    # Verify parsing
    assert len(moves) > 0, "Input should not be empty"
    assert all(isinstance(move, str) and move for move in moves), "All moves should be non-empty strings"
    assert all(move in DIRECTION_DELTAS for move in moves), "All moves should be valid directions (n, ne, se, s, sw, nw)"

    # Verify no whitespace in parsed moves
    assert all(move == move.strip() for move in moves), "Moves should have whitespace stripped"

    # Calculate solution
    x, y, z = calculate_final_position(moves)
    distance = calculate_distance(x, y, z)

    # Sanity checks
    assert distance >= 0, "Distance should be non-negative"
    assert distance <= len(moves), "Distance can't exceed total moves"
    assert isinstance(distance, int), "Distance should be an integer"

    # Verify invariant
    assert x + y + z == 0, f"Final position {(x,y,z)} should maintain cube coordinate invariant (x+y+z=0)"

    print(f"Actual input test passed!")
    print(f"  - Total moves: {len(moves)}")
    print(f"  - Final position: ({x}, {y}, {z})")
    print(f"  - Distance: {distance}")
    return distance
```

### 8. Input Validation Tests

#### Test 8.1: Whitespace Handling
- **Purpose**: Ensure parsing handles whitespace correctly
- **Test Cases**:
  - Input with trailing newline: `"ne,ne,ne\n"`
  - Input with spaces around commas: `"ne, ne, ne"`
  - Input with mixed whitespace: `" ne , ne , ne "`
- **Expected**: All should parse correctly and yield same result as `"ne,ne,ne"`

#### Test 8.2: Invalid Direction Handling
- **Purpose**: Verify that invalid directions are caught
- **Test Cases**:
  - Invalid direction: `"ne,east,ne"` (should raise ValueError)
  - Typo: `"ne,nn,ne"` (should raise ValueError)
  - Empty move: `"ne,,ne"` (should be filtered out or raise error)

**Implementation**:
```python
def test_input_validation():
    """Test input parsing and validation."""
    # Test whitespace handling
    test_inputs = [
        "ne,ne,ne",
        "ne,ne,ne\n",
        "ne, ne, ne",
        " ne , ne , ne "
    ]

    expected_moves = ["ne", "ne", "ne"]
    for input_str in test_inputs:
        if input_str:
            moves = [move.strip() for move in input_str.strip().split(',') if move.strip()]
        else:
            moves = []
        assert moves == expected_moves, f"Whitespace handling failed for '{input_str}': got {moves}"

    # Test invalid direction detection
    invalid_inputs = [
        "ne,east,ne",  # Invalid direction
        "ne,nn,ne",    # Typo
    ]

    for input_str in invalid_inputs:
        moves = [move.strip() for move in input_str.split(',') if move.strip()]
        try:
            calculate_final_position(moves)
            assert False, f"Should have raised ValueError for invalid input: {input_str}"
        except ValueError as e:
            # Expected - invalid direction should raise ValueError
            assert "Invalid direction" in str(e)

    print("Input validation tests passed!")

def run_all_tests():
    """Run all test suites."""
    print("=" * 50)
    print("Running Hexagonal Grid Distance Tests")
    print("=" * 50)

    test_examples()
    test_edge_cases()
    test_cube_coordinate_invariant()
    test_distance_calculation()
    test_opposite_directions()
    test_path_equivalence()
    test_input_validation()
    distance = test_actual_input()

    print("=" * 50)
    print("ALL TESTS PASSED!")
    print(f"Final Answer: {distance}")
    print("=" * 50)
```

## Manual Verification Steps

### Step 1: Verify Examples by Hand
- For each example, manually trace through moves
- Calculate expected cube coordinates
- Verify distance calculation

### Step 2: Check Sample Paths
- Pick random sequences of moves
- Trace path on hex grid diagram
- Verify computed distance matches manual count

### Step 3: Validate Against Problem Statement
- Ensure solution matches all 4 provided examples exactly
- Verify understanding of hexagonal grid geometry

## Success Criteria

The solution is considered correct if:
1. ✅ All 4 provided examples pass
2. ✅ All edge cases pass
3. ✅ Cube coordinate invariant maintained throughout
4. ✅ Distance calculation verified for known positions
5. ✅ Opposite directions properly cancel
6. ✅ Path equivalence verified
7. ✅ Actual input produces valid result within expected bounds
8. ✅ No runtime errors or exceptions

## Test Execution Order

1. Run example tests first (quick validation)
2. Run edge cases (boundary conditions)
3. Run mathematical verification tests (cube coordinates, distance)
4. Run equivalence tests (correctness verification)
5. Run actual input test last (final solution)

This ensures we catch basic errors early before running on the full input.
