# Test Plan: Cave Risk Level Calculation

## Updates from Critique

This plan has been updated based on feedback to include:
1. **Fixed arithmetic error** - Corrected Test Case 1.2.3 expected value from 60144 to 19778
2. **Stricter performance threshold** - Updated Test 6.1 from 1 second to 0.5 seconds
3. **Clarified unit test limitations** - Added note about Test 1.4.5 being somewhat artificial
4. **Enhanced debugging strategy** - Added specific expected values for first few cells
5. **Loop order emphasis** - Highlighted that y-outer, x-inner is CRITICAL
6. **Input assumptions** - Noted well-formed input assumption per AoC standards

## Testing Strategy

We need to verify that our implementation correctly:
1. Parses input
2. Calculates geologic indices according to all rules
3. Computes erosion levels correctly
4. Determines risk levels properly
5. Sums risk levels for the entire region
6. Handles the dependency ordering correctly

## Test Categories

### 1. Unit Tests (Component Testing)

Test individual functions in isolation to ensure correctness.

#### Test 1.1: Input Parsing
**Function**: `parse_input()`

**Test Case 1.1.1**: Example input
- Input file content:
  ```
  depth: 510
  target: 10,10
  ```
- Expected output: `(510, 10, 10)`

**Test Case 1.1.2**: Actual input
- Input file: `input.md`
- Expected output: `(3558, 15, 740)`

**Test Case 1.1.3**: Different formatting (spaces)
- Input file content:
  ```
  depth:510
  target:10,10
  ```
- Expected output: `(510, 10, 10)`

**Note**: For Advent of Code, we assume input is well-formed. No extensive error handling needed for malformed input.

**Verification**: Print parsed values and visually inspect

---

#### Test 1.2: Erosion Level Calculation
**Function**: `calculate_erosion_level()`

**Test Case 1.2.1**: Zero geologic index
- Input: `geologic_index=0, depth=510`
- Expected: `(0 + 510) % 20183 = 510`

**Test Case 1.2.2**: Example from problem
- Input: `geologic_index=0, depth=510`
- Expected: `510`

**Test Case 1.2.3**: Large geologic index
- Input: `geologic_index=100000, depth=510`
- Expected: `(100510) % 20183 = 19778`
- Verify calculation: 100510 // 20183 = 4, remainder = 100510 - 4*20183 = 100510 - 80732 = 19778

**Test Case 1.2.4**: Modulo wrapping
- Input: `geologic_index=20000, depth=500`
- Expected: `(20500) % 20183 = 317`

**Verification**: Assert actual == expected for each case

---

#### Test 1.3: Risk Level Calculation
**Function**: `calculate_risk_level()`

**Test Case 1.3.1**: Rocky region
- Input: `erosion_level=510` (510 % 3 = 0)
- Expected: `0`

**Test Case 1.3.2**: Wet region
- Input: `erosion_level=511` (511 % 3 = 1)
- Expected: `1`

**Test Case 1.3.3**: Narrow region
- Input: `erosion_level=512` (512 % 3 = 2)
- Expected: `2`

**Test Case 1.3.4**: Various erosion levels
- Input: `erosion_level=0` → Expected: `0`
- Input: `erosion_level=1` → Expected: `1`
- Input: `erosion_level=2` → Expected: `2`
- Input: `erosion_level=3` → Expected: `0`
- Input: `erosion_level=100` → Expected: `1`

**Verification**: Assert actual == expected for each case

---

#### Test 1.4: Geologic Index Calculation
**Function**: `calculate_geologic_index()`

**Setup**: Create a small erosion_levels array for testing rule 5

**Note**: Test 1.4.5 requires setting up a partial erosion_levels array, which is somewhat artificial. The integration tests will more naturally verify this functionality, but unit testing the logic is still valuable.

**Test Case 1.4.1**: Cave mouth (0,0)
- Input: `x=0, y=0, target=(10,10), erosion_levels=...`
- Expected: `0`

**Test Case 1.4.2**: Target position
- Input: `x=10, y=10, target=(10,10), erosion_levels=...`
- Expected: `0`

**Test Case 1.4.3**: Top edge (Y=0, X>0)
- Input: `x=1, y=0, target=(10,10), erosion_levels=...`
- Expected: `1 * 16807 = 16807`
- Input: `x=5, y=0, target=(10,10), erosion_levels=...`
- Expected: `5 * 16807 = 84035`

**Test Case 1.4.4**: Left edge (X=0, Y>0)
- Input: `x=0, y=1, target=(10,10), erosion_levels=...`
- Expected: `1 * 48271 = 48271`
- Input: `x=0, y=5, target=(10,10), erosion_levels=...`
- Expected: `5 * 48271 = 241355`

**Test Case 1.4.5**: Interior cell (rule 5)
- Setup: Pre-populate erosion_levels with:
  - `erosion_levels[0][1] = 100`
  - `erosion_levels[1][0] = 200`
- Input: `x=1, y=1, target=(10,10), erosion_levels=...`
- Expected: `100 * 200 = 20000`

**Verification**: Assert actual == expected for each case

---

### 2. Integration Tests

Test the complete calculation with known examples.

#### Test 2.1: Provided Example
**Function**: `calculate_total_risk()`

**Input**:
- `depth = 510`
- `target = (10, 10)`

**Expected Output**: `114`

**Verification Steps**:
1. Run calculate_total_risk(510, 10, 10)
2. Assert result == 114
3. If failed, manually verify a few cells:
   - Cell (0,0): geologic=0, erosion=510, risk=0
   - Cell (1,0): geologic=16807, erosion=(16807+510)%20183=17317, risk=17317%3=1
   - Cell (0,1): geologic=48271, erosion=(48271+510)%20183=8415, risk=8415%3=0
   - Cell (1,1): geologic=17317*8415=145722555, erosion=(145722555+510)%20183=1805, risk=1805%3=1

**Why this test matters**: This is the official example provided in the problem statement. If this fails, our algorithm is fundamentally wrong.

---

#### Test 2.2: Trivial Case - Target at Origin
**Function**: `calculate_total_risk()`

**Input**:
- `depth = 100` (arbitrary)
- `target = (0, 0)`

**Expected Output**:
- Only one cell (0,0)
- Geologic index = 0
- Erosion level = (0 + 100) % 20183 = 100
- Risk level = 100 % 3 = 1
- Total = `1`

**Verification**: Assert result == 1

---

#### Test 2.3: Single Row
**Function**: `calculate_total_risk()`

**Input**:
- `depth = 510`
- `target = (3, 0)`

**Expected Calculation**:
- (0,0): geo=0, ero=510, risk=0
- (1,0): geo=16807, ero=17317, risk=1
- (2,0): geo=33614, ero=13940, risk=1
- (3,0): geo=50421, ero=10563, risk=0
- Total = 0+1+1+0 = `2`

**Verification**: Manually calculate and assert result == 2

---

#### Test 2.4: Single Column
**Function**: `calculate_total_risk()`

**Input**:
- `depth = 510`
- `target = (0, 3)`

**Expected Calculation**:
- (0,0): geo=0, ero=510, risk=0
- (0,1): geo=48271, ero=8415, risk=0
- (0,2): geo=96542, ero=16320, risk=0
- (0,3): geo=144813, ero=4042, risk=1
- Total = 0+0+0+1 = `1`

**Verification**: Manually calculate and assert result == 1

---

#### Test 2.5: Small Square
**Function**: `calculate_total_risk()`

**Input**:
- `depth = 510`
- `target = (2, 2)`

**Purpose**: Verify interior cell calculations with multiple dependencies

**Verification**: Calculate manually or use example logic to determine expected value

---

### 3. Actual Input Validation

#### Test 3.1: Actual Problem Input
**Function**: Full solution with `input.md`

**Input**:
- `depth = 3558`
- `target = (15, 740)`

**Expected Output**: Unknown (this is what we're solving for)

**Verification Steps**:
1. Run the solution
2. Get the result
3. Sanity checks:
   - Result should be >= 0
   - Result should be <= (15+1) * (740+1) * 2 = 23,712 (max if all cells are narrow)
   - Result should not be 0 (statistically unlikely for this size)
4. Re-run to ensure deterministic output (same result every time)

---

### 4. Edge Case Tests

#### Test 4.1: Target Position Correctness
**Purpose**: Verify that target position has geologic index 0

**Test**:
- Create a case where target is not at (0,0)
- Verify that the target cell itself has geologic index 0 (not using rule 5)

**Implementation**:
- Add debug print in calculate_geologic_index for target position
- Verify it returns 0 via rule 2

---

#### Test 4.2: Dependency Order
**Purpose**: Ensure cells are calculated in correct order

**Test**:
- Add assertions in calculate_geologic_index rule 5
- Assert that erosion_levels[y][x-1] and erosion_levels[y-1][x] are already computed (non-zero when expected)
- Should never raise IndexError

**Implementation**:
- In the main loop, verify we process row by row (y outer loop, x inner loop)
- **CRITICAL**: The loop order y-outer, x-inner is the ONLY correct order that satisfies dependencies

---

#### Test 4.3: Boundary Cells
**Purpose**: Verify all boundary cells use correct rules

**Test Cases**:
- Top-left (0,0): Should use rule 1
- Top-right (15,0): Should use rule 3 (unless it's the target)
- Bottom-left (0,740): Should use rule 4 (unless it's the target)
- Bottom-right (15,740): Should use rule 2 (since it's the target)

**Verification**: Add debug prints or assertions

---

### 5. Algorithm Verification Tests

#### Test 5.1: Manual Calculation for Small Grid
**Purpose**: Completely verify algorithm by hand

**Input**:
- `depth = 10`
- `target = (2, 2)`

**Manual Calculation**:
```
(0,0): geo=0, ero=10, risk=1
(1,0): geo=16807, ero=16817%20183=16817, risk=1
(2,0): geo=33614, ero=33624%20183=13441, risk=2

(0,1): geo=48271, ero=48281%20183=7915, risk=2
(1,1): geo=16817*7915=133139155, ero=(133139155+10)%20183=1523, risk=2
(2,1): geo=13441*7915=106405915, ero=(106405915+10)%20183=18661, risk=1

(0,2): geo=96542, ero=96552%20183=15820, risk=1
(1,2): geo=1523*15820=24093860, ero=(24093860+10)%20183=13987, risk=1
(2,2): geo=0 (target), ero=10, risk=1

Total = 1+1+2+2+2+1+1+1+1 = 12
```

**Verification**: Assert result == 12

---

### 6. Performance Tests

#### Test 6.1: Runtime Check
**Purpose**: Ensure solution completes in reasonable time

**Test**:
- Time the execution of calculate_total_risk(3558, 15, 740)
- Should complete in < 0.5 seconds (expected < 100ms based on complexity analysis)

**Verification**: Use time module, assert elapsed_time < 0.5

---

#### Test 6.2: Memory Check
**Purpose**: Ensure solution doesn't use excessive memory

**Test**:
- Memory usage should be roughly (16 * 741 * 8 bytes) ≈ 95 KB for erosion levels
- Plus overhead, should be well under 10 MB

**Verification**: Visual check (no explicit test needed for this problem size)

---

## Test Execution Order

1. **Unit tests first** (Tests 1.1 - 1.4)
   - Verify individual components work correctly
   - Easy to debug if failures occur

2. **Integration tests** (Tests 2.1 - 2.5)
   - Start with the provided example (Test 2.1) - CRITICAL
   - Then test edge cases (trivial, single row/column)
   - Finally test small square

3. **Actual input** (Test 3.1)
   - Run with real input
   - Perform sanity checks

4. **Edge cases** (Tests 4.1 - 4.3)
   - Verify correctness of special positions

5. **Algorithm verification** (Test 5.1)
   - Complete manual verification

6. **Performance** (Test 6.1)
   - Ensure acceptable runtime

## Success Criteria

The solution is considered correct if:
1. ✓ All unit tests pass
2. ✓ **The provided example (depth=510, target=10,10) returns 114**
3. ✓ All integration tests pass
4. ✓ The actual input produces a reasonable result (within bounds)
5. ✓ Re-running produces the same result (deterministic)
6. ✓ Runtime is under 1 second

## Debugging Strategy

If tests fail:

1. **Example test fails (Test 2.1)** - MOST CRITICAL:
   - Print out the full grid for the example
   - Manually verify first few cells match expected values shown in Test 2.1:
     - Cell (0,0): geologic=0, erosion=510, risk=0
     - Cell (1,0): geologic=16807, erosion=17317, risk=1
     - Cell (0,1): geologic=48271, erosion=8415, risk=0
     - Cell (1,1): geologic=145722555, erosion=1805, risk=1
   - Check each rule in calculate_geologic_index
   - Verify target position (10,10) correctly returns geologic index 0

2. **Wrong total**:
   - Verify summation loop covers correct range (0 to target_x inclusive, 0 to target_y inclusive)
   - Check off-by-one errors
   - Verify array bounds are target_x+1 and target_y+1

3. **Index errors**:
   - Verify loop order is y (outer) then x (inner) - NOT reversed
   - Check array access pattern: erosion_levels[y][x]
   - Verify dependencies are accessed correctly

4. **Wrong values**:
   - Verify constants (16807, 48271, 20183) match problem specification
   - Check modulo operations
   - Ensure risk level calculation is erosion % 3, not something else

## Test Implementation

Tests can be implemented as:
- Simple Python script with assertions
- Print statements for manual verification
- Comparison with expected values

**Minimal test script structure**:
```python
def run_tests():
    # Test 2.1: Example
    result = calculate_total_risk(510, 10, 10)
    assert result == 114, f"Example failed: expected 114, got {result}"
    print("✓ Example test passed")

    # Test 3.1: Actual input
    depth, tx, ty = parse_input("input.md")
    result = calculate_total_risk(depth, tx, ty)
    print(f"Actual input result: {result}")
    assert 0 < result <= 23712, "Result out of expected range"
    print("✓ Actual input test passed")

if __name__ == "__main__":
    run_tests()
```
