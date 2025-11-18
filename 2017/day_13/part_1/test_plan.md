# Test Plan: Firewall Packet Scanner

## Testing Strategy Overview

The testing approach will validate:
1. **Correctness**: Solution produces correct output for given examples
2. **Edge cases**: Handles boundary conditions properly
3. **Scanner behavior**: Oscillation pattern is correctly modeled
4. **Mathematical accuracy**: Period calculation and modulo arithmetic work correctly

## Test Categories

### 1. Example-Based Testing

#### Test 1.1: Provided Example
**Input**:
```
0: 3
1: 2
4: 4
6: 4
```

**Expected behavior**:
- Layer 0 (range 3): packet enters at t=0, scanner at position 0 → CAUGHT
  - Severity: 0 × 3 = 0
- Layer 1 (range 2): packet enters at t=1, scanner position?
  - Period = 2(2-1) = 2
  - At t=1: position = 1 % 2 = 1 → NOT CAUGHT
- Layer 4 (range 4): packet enters at t=4, scanner position?
  - Period = 2(4-1) = 6
  - At t=4: t_in_cycle = 4 % 6 = 4; since 4 >= 4 (range), scanner is going up
  - Position = 6 - 4 = 2 → NOT CAUGHT
- Layer 6 (range 4): packet enters at t=6, scanner position?
  - Period = 2(4-1) = 6
  - At t=6: 6 % 6 = 0 → CAUGHT
  - Severity: 6 × 4 = 24

**Expected output**: 24

**Validation**: Run solution and verify output matches expected value.

### 2. Unit Testing

#### Test 2.1: Scanner Position Calculation
Test the scanner oscillation pattern for various ranges.

**Test Case: Range = 3**
- Period = 2(3-1) = 4
- Positions over time: 0, 1, 2, 1, 0, 1, 2, 1, 0...
- Verify at times: 0→0, 1→1, 2→2, 3→1, 4→0, 5→1, 6→2, 7→1, 8→0

**Test Case: Range = 4**
- Period = 2(4-1) = 6
- Positions over time: 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0...
- Verify at times: 0→0, 1→1, 2→2, 3→3, 4→2, 5→1, 6→0, 7→1

**Test Case: Range = 2**
- Period = 2(2-1) = 2
- Positions over time: 0, 1, 0, 1, 0, 1...
- Verify at times: 0→0, 1→1, 2→0, 3→1, 4→0

#### Test 2.2: Caught Detection
Test the `is_caught` function directly.

**Test cases**:
- `is_caught(0, 3)` → True (0 % 4 = 0, caught)
- `is_caught(1, 2)` → False (1 % 2 ≠ 0)
- `is_caught(2, 2)` → True (2 % 2 = 0)
- `is_caught(6, 4)` → True (6 % 6 = 0)
- `is_caught(4, 4)` → False (4 % 6 ≠ 0)
- `is_caught(8, 3)` → True (8 % 4 = 0, caught)
- `is_caught(10, 3)` → False (10 % 4 = 2, not caught)

#### Test 2.3: Input Parsing
Test the parser with various input formats.

**Test Case: Standard input**
```
0: 3
1: 2
4: 4
```
Expected: `[(0, 3), (1, 2), (4, 4)]`

**Test Case: Extra whitespace**
```
0:3
  1 : 2
4:4
```
Expected: Same as above

**Test Case: Empty lines**
```
0: 3

1: 2
```
Expected: `[(0, 3), (1, 2)]`

### 3. Edge Case Testing

#### Test 3.1: Range = 1 (Division by Zero Edge Case)
Scanner never moves, always at position 0. Period would be 0, so this must be handled specially.

**Input**:
```
0: 1
5: 1
10: 1
```

**Expected**:
- All layers caught (scanner always at position 0)
- Severity: 0×1 + 5×1 + 10×1 = 15
- **CRITICAL**: Verify no division-by-zero errors occur
- Code must check `range == 1` BEFORE computing modulo

#### Test 3.2: Depth = 0 Only
First layer always entered at time 0 when scanner is at position 0.

**Input**:
```
0: 5
```

**Expected**:
- Caught at layer 0
- Severity: 0 × 5 = 0

#### Test 3.3: No Layers Caught
Design input where no scanner is at position 0 when packet enters.

**Input**:
```
1: 3
3: 5
```

**Analysis**:
- Layer 1, range 3: period = 4, 1 % 4 = 1 → not caught
- Layer 3, range 5: period = 8, 3 % 8 = 3 → not caught

**Expected**: 0

#### Test 3.4: All Layers Caught
Design input where all layers catch the packet.

**Input**:
```
0: 2
2: 2
4: 3
```

**Analysis**:
- Layer 0: always caught → 0×2 = 0
- Layer 2, range 2: period = 2, 2 % 2 = 0 → caught → 2×2 = 4
- Layer 4, range 3: period = 4, 4 % 4 = 0 → caught → 4×3 = 12

**Expected**: 16

#### Test 3.5: Large Depth Values
Test with large depths to ensure no integer overflow.

**Input**:
```
1000: 10
```

**Analysis**:
- Period = 2(10-1) = 18
- 1000 % 18 = 10 → not caught

**Expected**: 0

#### Test 3.6: Large Range Values
Test with large ranges.

**Input**:
```
100: 100
```

**Analysis**:
- Period = 2(100-1) = 198
- 100 % 198 = 100 → not caught

**Expected**: 0

#### Test 3.7: Empty Input
Test with empty or whitespace-only input file.

**Input**: Empty file or only whitespace

**Expected**: 0 (no layers means no severity)

### 4. Actual Input Testing

#### Test 4.1: Run on Provided Input
Execute solution on the actual input.md file.

**Validation steps**:
1. Parse all 43 layers successfully
2. Verify no parsing errors
3. Calculate severity
4. Manually verify a few key layers:
   - Layer 0 (range 3): 0 % 4 = 0 → CAUGHT → 0
   - Layer 2 (range 4): 2 % 6 = 2 → NOT caught
   - Layer 4 (range 6): 4 % 10 = 4 → NOT caught
   - Layer 6 (range 4): 6 % 6 = 0 → CAUGHT → 24

#### Test 4.2: Verify Calculation Manually
Manually calculate severity for first 5-10 layers and compare with code output (can add debug prints).

### 5. Mathematical Verification Tests

#### Test 5.1: Scanner Period Validation
Verify the period formula for various ranges.

**Test cases**:
- Range 2: period = 2, positions cycle: 0,1,0,1...
- Range 3: period = 4, positions cycle: 0,1,2,1,0,1,2,1...
- Range 5: period = 8, positions cycle: 0,1,2,3,4,3,2,1,0...

**Method**: Manually trace scanner movement and verify it matches formula.

#### Test 5.2: Modulo Arithmetic Verification
For specific test cases, manually verify that `depth % (2 * (range - 1)) == 0` correctly identifies when scanner is at position 0.

**Test Cases**:

1. **Depth=0, Range=3**: period=4, 0 % 4 = 0 → caught ✓
   - Manual trace: Scanner starts at position 0 at t=0

2. **Depth=6, Range=4**: period=6, 6 % 6 = 0 → caught ✓
   - Manual trace: Positions at times 0,1,2,3,4,5,6 are: 0,1,2,3,2,1,0

3. **Depth=4, Range=4**: period=6, 4 % 6 = 4 → not caught ✓
   - Manual trace: Position at t=4 is 2 (not 0)

4. **Depth=8, Range=3**: period=4, 8 % 4 = 0 → caught ✓
   - Manual trace: Positions cycle every 4: 0,1,2,1,0,1,2,1,0

5. **Depth=10, Range=3**: period=4, 10 % 4 = 2 → not caught ✓
   - Manual trace: Position at t=10 is 2 (not 0)

**Method**: For each case, manually trace scanner positions and verify the modulo check gives the correct result.

## Testing Execution Plan

### Phase 1: Unit Tests
1. Test input parsing with various formats
2. Test `is_caught()` function with known cases
3. Test scanner position calculation (if implemented)

### Phase 2: Integration Tests
1. Run example from problem statement
2. Verify output matches expected (24)

### Phase 3: Edge Case Tests
1. Test all edge cases listed above
2. Verify each produces correct output

### Phase 4: Actual Input
1. Run on provided input.md
2. Check for parsing errors
3. Verify output is a reasonable number
4. Spot-check specific layers manually:
   - Select 2-3 layers where `depth % period == 0` (should be caught)
   - Select 2-3 layers where `depth % period != 0` (should not be caught)
   - Verify the code's determination matches manual calculation

### Phase 5: Manual Verification
1. Pick 3-5 random layers from actual input
2. Manually calculate if caught and severity
3. Compare with code's determination

## Test Implementation

Create a test file `test_solution.py` with:

```python
def test_example():
    # Test the provided example
    assert calculate_severity([(0,3), (1,2), (4,4), (6,4)]) == 24

def test_range_one():
    # All scanners always at position 0
    assert calculate_severity([(0,1), (5,1), (10,1)]) == 15

def test_no_caught():
    # No layers catch the packet
    assert calculate_severity([(1,3), (3,5)]) == 0

def test_all_caught():
    # All layers catch the packet
    assert calculate_severity([(0,2), (2,2), (4,3)]) == 16

def test_is_caught_function():
    # Direct function tests
    assert is_caught(0, 3) == True   # 0 % 4 = 0
    assert is_caught(1, 2) == False  # 1 % 2 = 1
    assert is_caught(2, 2) == True   # 2 % 2 = 0
    assert is_caught(6, 4) == True   # 6 % 6 = 0
    assert is_caught(4, 4) == False  # 4 % 6 = 4
    assert is_caught(8, 3) == True   # 8 % 4 = 0
    assert is_caught(10, 3) == False # 10 % 4 = 2

def test_range_one_no_division_error():
    # Critical test: range=1 should not cause division by zero
    assert is_caught(0, 1) == True
    assert is_caught(5, 1) == True
    assert is_caught(100, 1) == True

def test_empty_input():
    # Empty layers list should return 0
    assert calculate_severity([]) == 0
```

## Success Criteria

✓ All unit tests pass
✓ Example test produces output of 24
✓ Edge cases handled correctly (especially range=1 without division errors)
✓ Actual input produces a valid integer output
✓ Manual verification of sample layers confirms correctness
✓ No runtime errors or exceptions (especially no ZeroDivisionError)
✓ Solution completes in under 1 second
✓ Results are deterministic (running twice gives same answer)

## Debugging Strategy

If tests fail:
1. **Check division by zero**: Ensure range=1 is handled before modulo operations
2. **Verify period calculation**: Ensure `2 * (range - 1)` is correct
3. **Check modulo arithmetic**: Verify caught condition for specific failing cases
4. **Inspect parsing**: Print parsed layers to ensure correct format
5. **Manual trace**: Step through algorithm for small example by hand
6. **Scanner position verification**: If available, use `get_scanner_position()` to verify exact positions

## Additional Notes

### Solution File Name
The solution will be implemented in `solution.py`, and tests will be in `test_solution.py`.

### Spot-Check Examples for Actual Input
For the provided input.md, here are specific layers to manually verify:

**Expected to be caught** (depth % period == 0):
- Layer 0, range 3: period=4, 0 % 4 = 0 ✓ Severity: 0×3 = 0
- Layer 6, range 4: period=6, 6 % 6 = 0 ✓ Severity: 6×4 = 24
- Layer 8, range 6: period=10, 8 % 10 = 8 ✗ NOT caught
- Layer 12, range 6: period=10, 12 % 10 = 2 ✗ NOT caught

**Expected NOT to be caught**:
- Layer 2, range 4: period=6, 2 % 6 = 2 ✓ Not caught
- Layer 4, range 6: period=10, 4 % 10 = 4 ✓ Not caught

Use these specific examples when doing Phase 4 spot-checks.
