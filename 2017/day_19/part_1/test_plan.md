# Testing Plan: Network Packet Routing

## Testing Strategy

Since this is a script to solve a specific problem (not production code), we focus on:
1. Validating core algorithm correctness
2. Testing key edge cases that could occur in the input
3. Verifying the actual input produces correct output
4. Testing critical path-following rules (especially `+` behavior and crossing paths)

We do NOT need to test:
- Error handling for malformed input
- Performance under extreme loads
- Input validation and sanitization
- Comprehensive boundary case coverage

## Pre-Implementation Validation

### Step 0: Inspect Actual Input File
**Purpose**: Validate assumptions about the input before implementing.

**Actions**:
1. Open and visually inspect input.md
2. Verify there is a `|` character in the first row
3. Note the approximate grid dimensions
4. Check for any unusual characters or formatting
5. Verify the file contains ASCII art as expected

**Why this matters**: Ensures our implementation assumptions match reality.

## Test Categories

### 1. Example Test (Mandatory)
**Purpose**: Verify the implementation matches the problem's example.

**Test Case**: The provided example from problem.md
```
     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
```

**Expected Output**: `ABCDEF`

**Why this matters**:
- Validates basic algorithm correctness
- Tests all major features: straight lines, turns at `+`, letters on path
- If this fails, fundamental logic is wrong

**How to test**:
1. Create a test file with the example grid
2. Run solution on it
3. Assert output equals "ABCDEF"

**Implementation**:
```python
def test_example():
    example_input = """     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+"""

    # Write to temporary file
    with open('test_example.txt', 'w') as f:
        f.write(example_input)

    # Run solution
    grid = parse_input('test_example.txt')
    start = find_start(grid)
    result = follow_path(grid, start[0], start[1])

    assert result == "ABCDEF", f"Expected 'ABCDEF', got '{result}'"
    print("✓ Example test passed")
```

### 2. Directional Movement Tests

#### Test 2.1: Straight Line Down
**Purpose**: Verify basic downward movement with letters.

**Input**:
```
|
A
B
C
|
```

**Expected Output**: `ABC`

**What this tests**:
- Vertical movement
- Letter collection in sequence
- Simple path with no turns

#### Test 2.2: Straight Line Right
**Purpose**: Verify horizontal movement.

**Input**:
```
     |
     +--A--B--C--
```

**Expected Output**: `ABC`

**What this tests**:
- Horizontal movement
- Turn from vertical to horizontal at `+`

#### Test 2.3: Multiple Turns
**Purpose**: Verify turning logic at corners.

**Input**:
```
     |
     A
     +---B
         |
         C
```

**Expected Output**: `ABC`

**What this tests**:
- Multiple `+` corner turns
- Direction changes

### 3. Edge Cases

#### Test 3.1: Letter at Start
**Purpose**: Ensure we collect letter at starting position.

**Input**:
```
A
|
B
```

**Expected Output**: `AB`

**What this tests**:
- Letter collection at first position
- Not skipping the starting character

#### Test 3.2: Letter at End
**Purpose**: Ensure we collect the last letter before stopping.

**Input**:
```
|
A
B
```

**Expected Output**: `AB`

**What this tests**:
- Letter collection at final position
- Proper termination

#### Test 3.3: Minimal Path
**Purpose**: Minimal valid path that matches problem constraints.

**Input**:
```
|
A
```

**Expected Output**: `A`

**What this tests**:
- Minimal input handling
- Path starting with `|` as required
- Immediate termination after one letter

**Note**: Per problem description, starting position must be a `|` in the top row.

#### Test 3.4: Continue Straight Through Plus
**Purpose**: Verify we continue straight through `+` when possible (don't turn unnecessarily).

**Input**:
```
     |
     A
     +
     B
     |
```

**Expected Output**: `AB`

**What this tests**:
- **CRITICAL**: Plus sign does NOT force a turn
- Continuing straight through `+` when the current direction has a valid continuation
- This is the "try straight first, only turn if necessary" rule

**Why critical**: If this fails, the algorithm will incorrectly turn at every `+` even when it should continue straight.

#### Test 3.5: Wide Grid with Padding
**Purpose**: Verify handling of varying line lengths and padding.

**Input**:
```
     |
     A--+
        |
        B
```

**Expected Output**: `AB`

**What this tests**:
- Inconsistent line lengths
- Trailing spaces don't affect path
- Grid padding works correctly

### 4. Direction Change Logic Tests

#### Test 4.1: Turn at Plus Sign (Required Turn)
**Purpose**: Verify we DO turn at `+` when we cannot continue straight.

**Input**:
```
|
+--A
```

**Expected Output**: `A`

**What this tests**:
- Turn at `+` when straight continuation is blocked
- Perpendicular direction search when needed

**Contrast with Test 3.4**: Test 3.4 verifies we DON'T turn through `+` when we CAN continue straight. This test verifies we DO turn when we MUST.

#### Test 4.2: Dead End Turn (Implicit)
**Purpose**: Verify turning when reaching end of line segment.

**Input**:
```
     |
     A--
        |
        B
```

**Expected Output**: `AB`

**What this tests**:
- Implicit turn when can't continue straight
- No `+` required if only one valid direction

#### Test 4.3: Crossing Paths Without Plus
**Purpose**: Verify we continue straight when paths cross without `+`.

**Input**:
```
     |
     A
   --|--
     B
     |
```

**Expected Output**: `AB`

**What this tests**:
- Continuing straight when vertical path crosses horizontal path
- Not turning at intersections that aren't marked with `+`
- Following the "don't turn at crossings" rule

**Note**: This differs from Test 3.4 which has a `+` at the crossing.

### 5. Actual Input Test

#### Test 5.1: Full Input Validation
**Purpose**: Verify solution works on the actual problem input.

**Approach**:
1. Run solution on `input.md`
2. Get the output string
3. Verify output is reasonable:
   - Contains only uppercase letters
   - Non-empty
   - Has reasonable length (likely 10-20 letters)
4. Check execution time is reasonable (< 1 second)

**Manual Verification**:
- Visually trace a few steps of the path to ensure algorithm is following correctly
- Check starting position is reasonable (top row has `|`)
- Verify first letter makes sense based on visual inspection
- Spot-check a few more positions along the path

**Implementation**:
```python
import time

def test_actual_input():
    grid = parse_input('input.md')
    start = find_start(grid)

    # Basic sanity checks
    assert start is not None, "Should find a starting position"
    assert start[0] == 0, "Start should be in first row"
    assert grid[start[0]][start[1]] == '|', "Start position should be a |"

    # Time the execution
    start_time = time.time()
    result = follow_path(grid, start[0], start[1])
    elapsed = time.time() - start_time

    # Output validation
    assert len(result) > 0, "Output should not be empty"
    assert result.isalpha(), "Output should only contain letters"
    assert result.isupper(), "Output should only contain uppercase letters"
    assert len(result) < 100, "Output length should be reasonable"
    assert elapsed < 1.0, f"Should complete in < 1 second (took {elapsed:.2f}s)"

    print(f"Actual input test passed: {result}")
    print(f"Execution time: {elapsed:.3f} seconds")
    return result
```

### 6. Path Following Correctness

#### Test 6.1: No Backtracking
**Purpose**: Ensure we never revisit positions (would indicate a loop or backtrack).

**Approach**:
- Track visited positions during path following
- Assert we never visit same position twice

**Implementation**:
```python
def follow_path_with_tracking(grid, start_row, start_col):
    """Modified version that tracks visited positions."""
    letters = []
    visited = set()
    row, col = start_row, start_col
    direction = DOWN

    while True:
        # Check for loops
        if (row, col) in visited:
            raise Exception(f"Loop detected at ({row}, {col})")
        visited.add((row, col))

        current_char = grid[row][col]
        if current_char.isalpha() and current_char.isupper():
            letters.append(current_char)

        next_move = get_next_position(grid, row, col, direction)
        if next_move is None:
            break

        row, col, direction = next_move

    return ''.join(letters)
```

**Why this matters**:
- Validates path is truly linear
- Catches logic errors that cause backtracking or loops

## Test Execution Plan

### Phase 0: Pre-Implementation Inspection
**Before writing any code**, inspect the input file:
1. Open input.md and visually examine it
2. Verify format matches problem description
3. Note starting position and first few letters visually
4. Check grid dimensions

### Phase 1: Unit Tests (Small Examples)
Run tests in this order:
1. Example test (ABCDEF) - **MANDATORY first test**
2. Straight line tests (2.1, 2.2)
3. **CRITICAL**: Test 3.4 (Continue straight through `+`)
4. **CRITICAL**: Test 4.1 (Turn at `+` when required)
5. **CRITICAL**: Test 4.3 (Crossing paths without `+`)
6. Other turn tests (4.2)
7. Other edge cases (3.1, 3.2, 3.3, 3.5)

**Success Criteria**: All tests pass

**If failures occur**:
- Debug the specific failing test
- Fix the logic issue
- Re-run all tests

**Critical tests**: Tests 3.4, 4.1, and 4.3 are critical for validating the core "try straight first" rule. These must pass.

### Phase 2: Path Validation Test
Run the no-backtracking test on ALL test cases (not just example).

**Success Criteria**: No loops detected in any test case

**Implementation**: Use `follow_path_with_tracking` on each test input

**If failure occurs**:
- Review direction change logic
- Check perpendicular direction search
- Ensure we're not doubling back

### Phase 3: Actual Input Test
Run solution on `input.md`.

**Success Criteria**:
- Output is valid (letters only, reasonable length)
- No crashes or infinite loops
- Execution completes in < 1 second
- Output looks plausible

**Manual verification steps**:
1. Look at input.md visually
2. Find the starting `|` in row 0 (should be around column 19-20 based on inspection)
3. Trace first 3-4 moves by hand
4. Verify solution's first 3-4 letters match
5. Spot-check a few more positions in the middle of the path
6. Verify solution completes and finds end of path

### Phase 4: Visual Path Trace (Optional)
For additional confidence, modify solution to print the path visually:
- Mark each visited position
- Show direction at each step
- Highlight collected letters

**Purpose**: Visual debugging and confidence building

**Implementation**:
```python
def visualize_path(grid, start_row, start_col):
    """Print the path taken through the grid."""
    path_positions = []
    row, col = start_row, start_col
    direction = DOWN

    while True:
        path_positions.append((row, col, grid[row][col]))
        next_move = get_next_position(grid, row, col, direction)
        if next_move is None:
            break
        row, col, direction = next_move

    # Print path summary
    for i, (r, c, char) in enumerate(path_positions[:20]):  # First 20 steps
        print(f"Step {i}: ({r}, {c}) = '{char}'")
```

## Expected Test Results

### Example Input
- **Expected**: `ABCDEF`
- **Confidence**: 100% (provided in problem)

### Actual Input
- **Expected**: Unknown, but should be:
  - 10-30 characters long
  - All uppercase letters
  - Forms a valid English-looking sequence
- **Confidence**: High (if all other tests pass)

## Debugging Strategy

If tests fail, check in this order:

1. **Parsing Issues**:
   - Print grid dimensions
   - Print first few rows
   - Check for line width inconsistencies

2. **Start Position Issues**:
   - Print found starting position
   - Verify it's in row 0
   - Check character at that position is `|`

3. **Direction Logic Issues**:
   - Add debug prints in `get_next_position`
   - Print current position, direction, and next move
   - Trace first 5-10 moves manually

4. **Path Following Issues**:
   - Print each position visited
   - Print each letter collected
   - Check for premature termination

5. **Character Validation Issues**:
   - Print each character checked
   - Verify `is_path_char` logic
   - Check for whitespace issues

## Test Files Structure

```
test_solution.py        # Test runner with all test cases
test_example.txt        # Example input for testing
solution.py             # Main solution (to be tested)
input.md                # Actual problem input
```

## Success Criteria Summary

The solution is considered correct when:
1. Pre-inspection confirms input.md matches expected format
2. Example test produces "ABCDEF"
3. **CRITICAL**: Test 3.4 passes (continue straight through `+`)
4. **CRITICAL**: Test 4.1 passes (turn at `+` when required)
5. **CRITICAL**: Test 4.3 passes (cross paths without turning)
6. All other unit tests pass
7. No loops detected in path following (all test cases)
8. Actual input produces valid output (uppercase letters only)
9. Actual input completes in < 1 second
10. Manual verification of first few steps matches solution
11. Solution completes without errors or crashes

**Priority order**:
- **Must pass**: Tests 1, 2, 3, 4, 5 (these validate core algorithm)
- **Should pass**: Tests 6, 7, 8, 9 (these validate correctness and efficiency)
- **Nice to have**: Tests 10, 11 (these build confidence)

## Time Estimate

- Pre-inspection of input: ~5 minutes
- Writing tests: ~15 minutes
- Running tests: ~1 minute
- Debugging (if needed): ~10-30 minutes
- Manual verification: ~5 minutes

**Total**: ~35-55 minutes for comprehensive testing

## Key Additions Based on Critique

The following improvements were made based on the critique:

1. **Added Step 0 pre-inspection** to validate input file before implementation
2. **Added critical Test 3.4** for continuing straight through `+`
3. **Added Test 4.3** for crossing paths without `+`
4. **Clarified Test 4.1** to contrast with Test 3.4 (turn vs. continue)
5. **Fixed Test 3.3** to start with `|` as required by problem constraints
6. **Added timing check** to Test 5.1 for performance validation
7. **Expanded Phase 2** to run no-backtracking on all tests, not just example
8. **Added manual spot-checking** to Phase 3 verification
9. **Prioritized critical tests** in execution plan
10. **Improved success criteria** with clear priority levels
