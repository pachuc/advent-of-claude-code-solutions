# Test Plan: Santa's House Delivery Tracker

## Testing Strategy Overview

The goal is to verify that our solution correctly counts unique houses visited by Santa based on directional input. We'll test with provided examples, edge cases, and validate against the actual input.

## Test Categories

### 1. Example Test Cases (from problem statement)

#### Test 1.1: Single Move East
**Input**: `>`
**Expected Output**: `2`
**Rationale**: Starting position (0,0) + one move east to (1,0) = 2 unique houses
**Verification**:
- Starting position should be counted
- One additional position to the right
- Set should contain: {(0,0), (1,0)}

#### Test 1.2: Square Path
**Input**: `^>v<`
**Expected Output**: `4`
**Rationale**:
- Start at (0,0)
- North to (0,1)
- East to (1,1)
- South to (1,0)
- West back to (0,0) - revisit starting position
- Unique positions: {(0,0), (0,1), (1,1), (1,0)} = 4 houses
**Verification**: Should form a square and return to start, but count start only once

#### Test 1.3: Back and Forth
**Input**: `^v^v^v^v^v`
**Expected Output**: `2`
**Rationale**:
- Alternating north and south movements
- Only visits (0,0) and (0,1) repeatedly
- Set should contain: {(0,0), (0,1)}
**Verification**: Tests that revisiting houses doesn't increase count

### 2. Edge Case Tests

#### Test 2.1: Empty Input
**Input**: `` (empty string)
**Expected Output**: `1`
**Rationale**: Santa delivers to starting house even with no moves
**Verification**: Set should contain only {(0,0)}

#### Test 2.2: Single Character - All Directions
Test each direction individually:
- `^` → `2` (north to (0,1))
- `v` → `2` (south to (0,-1))
- `>` → `2` (east to (1,0))
- `<` → `2` (west to (-1,0))
**Verification**: Each direction moves correctly from origin

#### Test 2.3: Straight Line
**Input**: `>>>>>>>>` (8 moves east)
**Expected Output**: `9`
**Rationale**: Start + 8 unique positions = 9 houses
**Verification**: Linear path with no revisits

#### Test 2.4: Return to Position Later
**Input**: `>^<v>`
**Expected Output**: `4`
**Rationale**:
- Start (0,0)
- East to (1,0)
- North to (1,1)
- West to (0,1)
- South to (0,0) - revisit
- East to (1,0) - revisit
- Unique: {(0,0), (1,0), (1,1), (0,1)} = 4
**Verification**: Multiple revisits should not increase count

#### Test 2.5: Complex Overlapping Path
**Input**: `^>v<^>v<`
**Expected Output**: `4`
**Rationale**: Two squares on top of each other, same 4 positions
**Verification**: Complete path overlap detection

### 3. Coordinate System Tests

#### Test 3.1: Negative Coordinates
**Input**: `<v`
**Expected Output**: `3`
**Rationale**:
- Start (0,0)
- West to (-1,0)
- South to (-1,-1)
- All negative coordinates should work
**Verification**: Confirms grid works in all quadrants

#### Test 3.2: Large Coordinates
**Input**: `>>>>>>>>>>>>>>>>>>>` (20 moves east)
**Expected Output**: `21`
**Rationale**: Tests that large positive coordinates work
**Verification**: No overflow or boundary issues

#### Test 3.3: All Four Quadrants
**Input**: `>^<<<<vv>>>`
**Expected Output**: `12`
**Rationale**: Tests that Santa can move freely in infinite grid
**Position Trace**:
- Start (0,0) → (1,0) → (1,1) → (0,1) → (-1,1) → (-2,1) → (-3,1) → (-3,0) → (-3,-1) → (-2,-1) → (-1,-1) → (0,-1)
- Unique positions: 12 houses across all 4 quadrants
**Verification**: Positions appear in (+,+), (+,-), (-,+), (-,-) quadrants

### 4. Input Format Tests

#### Test 4.1: Input with Newlines/Whitespace
**Input**: `^>v<\n` (with trailing newline)
**Expected Output**: Same as `^>v<`
**Rationale**: Verify input is properly stripped
**Verification**: Whitespace handling

### 5. Actual Input Validation

#### Test 5.1: Run Against Provided Input
**Input**: Content from `input.md`
**Expected Output**: To be determined on first run and recorded for regression testing
**Verification Method**:
1. Run the solution against actual input
2. Verify result is reasonable (between 1 and input_length+1)
3. Record the output as the expected answer for future regression testing
4. Re-run to ensure deterministic result (should get same answer)
5. Manual spot-check: Sample a few positions to verify tracking

**Reasonableness checks**:
- Result should be > 1 (at least starting position)
- Result should be ≤ (input_length + 1) (can't have more unique houses than moves + start)
- For 8000+ character input, expect result in range ~2000-8000 (accounting for some revisits)

**Post-execution**: Once the correct answer is obtained, document it here for regression testing

### 6. Performance Tests (Optional)

*Note: These tests are nice-to-have but not essential. The actual input (~8000 chars) is sufficient for performance validation.*

#### Test 6.1: Large Input Performance (Optional)
**Input**: Very long string (100,000+ characters)
**Expected Behavior**:
- Completes in < 1 second
- No memory issues
- Correct result
**Verification**: Tests scalability of solution
**Status**: Optional - actual input size is adequate for validation

#### Test 6.2: Worst Case - All Unique (Optional)
**Input**: Spiral pattern that never revisits
**Expected Output**: Length + 1 (all positions unique)
**Verification**: Maximum memory usage scenario
**Status**: Optional - complex to generate, not essential

#### Test 6.3: Best Case - All Same (Optional)
**Input**: `^^^^...` (all same direction, 10,000 characters)
**Expected Output**: 10,001 (linear path)
**Verification**: Linear time verification
**Status**: Optional - can use actual input for performance check

## Testing Execution Plan

### Phase 1: Example Validation (Essential)
1. Test the three provided examples from problem statement:
   - `>` → 2
   - `^>v<` → 4
   - `^v^v^v^v^v` → 2
2. Verify outputs match expected results exactly
3. If any fail, debug before proceeding

### Phase 2: Edge Case Validation (Essential)
1. Test empty input → 1
2. Test single characters in each direction
3. Test a path with revisits
4. Verify all pass

### Phase 3: Actual Input (Essential)
1. Run solution on provided input.md
2. Record the output as the expected answer
3. Verify output is within reasonable bounds (>1 and ≤input_length+1)
4. Re-run to ensure deterministic result (must get same answer)

### Phase 4: Manual Verification (Optional but Recommended)
For validation confidence:
1. Trace first 10-20 moves manually from actual input
2. Verify positions are tracked correctly
3. Check that revisits are handled properly
4. Confirms logic is sound

### Phase 5: Performance Check (Optional)
- Verify solution runs quickly on actual input (should be near-instant)
- If needed, test with a larger generated input

## Test Implementation Approach

### Practical Testing Strategy

For a script of this complexity, manual testing with prepared test inputs is more practical than building an automated test framework.

### Recommended Approach:

**Option 1: Manual Test Files**
1. Create separate test input files: `test1.txt`, `test2.txt`, etc.
2. Temporarily modify solution to read from different file or use command-line argument
3. Run solution against each test file
4. Compare output to expected result

**Option 2: Inline Testing Function**
```python
def run_test(input_str, expected, test_name):
    """Simple test function that doesn't modify input.md"""
    visited = set()
    x, y = 0, 0
    visited.add((x, y))

    direction_map = {'^': (0, 1), 'v': (0, -1), '>': (1, 0), '<': (-1, 0)}

    for direction in input_str:
        dx, dy = direction_map[direction]
        x += dx
        y += dy
        visited.add((x, y))

    result = len(visited)
    status = "PASS" if result == expected else "FAIL"
    print(f"{status}: {test_name} - Expected {expected}, Got {result}")
    return result == expected

# Test suite
if __name__ == "__main__":
    # Run all example tests
    run_test(">", 2, "Single move east")
    run_test("^>v<", 4, "Square path")
    run_test("^v^v^v^v^v", 2, "Back and forth")
    run_test("", 1, "Empty input")
    # ... etc
```

**Option 3: Simple Manual Execution**
1. Run solution with example inputs by temporarily replacing input.md content
2. Verify output matches expected
3. Restore original input.md
4. Run against actual input for final answer

### Recommended for This Problem
Use **Option 2** or **Option 3** - keep testing simple and focused on validation rather than infrastructure

## Success Criteria

✓ All example cases pass
✓ All edge cases pass
✓ Actual input produces result in valid range
✓ Performance acceptable for large inputs
✓ Results are deterministic (same output every run)
✓ No crashes or errors

## Debugging Strategy

If tests fail:
1. **Wrong count (off by 1)**: Check if starting position is added
2. **Too high count**: Verify set is being used (not list)
3. **Too low count**: Check all directions mapped correctly
4. **Crashes**: Check input parsing, direction map completeness
5. **Wrong positions**: Verify coordinate system (y-axis direction)

## Manual Verification Example

For input `^>v<`:
```
Start: (0,0) → visited = {(0,0)}
  ^  : (0,1) → visited = {(0,0), (0,1)}
  >  : (1,1) → visited = {(0,0), (0,1), (1,1)}
  v  : (1,0) → visited = {(0,0), (0,1), (1,1), (1,0)}
  <  : (0,0) → visited = {(0,0), (0,1), (1,1), (1,0)} [no change]
Result: 4 ✓
```

## Notes

- **No extensive error handling tests**: Input guaranteed valid
- **No boundary tests**: Infinite grid, no boundaries
- **Focus on correctness**: Core logic validation
- **Simple test structure**: Script-level testing, not unit tests
- **Deterministic tests**: No randomness, reproducible results
- **Results documentation**: After running tests, record actual outputs for regression testing
- **Practical over perfect**: For a script solution, manual verification of key test cases is more practical than building extensive test infrastructure
